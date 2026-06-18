import os
import random
import argparse
import csv
import gc
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import segmentation_models_pytorch as smp
import pyarrow.parquet as pq
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.utils.data import DataLoader, IterableDataset
from tqdm import tqdm


# --- 1. Dataset & OOM-Proof DataLoader ---
class CryoSentinelDataset(IterableDataset):
    def __init__(self, data_dir, split="train", shuffle=True):
        """
        OOM-Proof IterableDataset for Kaggle.
        Bypasses Pandas entirely to save RAM and prevents DataLoader crashes.
        """
        self.data_dir = Path(data_dir)
        self.split = split
        self.shuffle = shuffle
        
        print(f"Scanning {self.data_dir} for {split} split...")
        parquet_files = sorted(list(self.data_dir.rglob("*.parquet")))
        if not parquet_files:
            raise FileNotFoundError(f"No .parquet files found in {self.data_dir}")
            
        self.parquet_files = parquet_files
        
        # Calculate total length for tqdm progress bar
        self.total_samples = 0
        for pf in self.parquet_files:
            table = pq.read_table(pf, columns=["split"])
            splits = np.array(table.column("split").to_pylist())
            self.total_samples += np.sum(splits == self.split)
            
        print(f"Indexed {self.total_samples} samples for {split} split.")

        # Normalization Stats (Exact values from your prompt)
        self.s2_mean = np.array([857.6, 1044.0, 1356.7, 1574.4, 1786.2, 2076.5, 2215.2, 2277.8, 2348.5, 2243.7, 2665.0, 2217.2], dtype=np.float32).reshape(12, 1, 1)
        self.s2_std  = np.array([626.3, 709.2, 748.7, 825.5, 773.5, 786.1, 810.8, 834.9, 833.6, 729.6, 875.7, 851.3], dtype=np.float32).reshape(12, 1, 1)
        self.s1_mean = np.array([-9.25, -18.00], dtype=np.float32).reshape(2, 1, 1)
        self.s1_std  = np.array([5.90, 5.92], dtype=np.float32).reshape(2, 1, 1)
        self.dem_mean = np.array([4299.8], dtype=np.float32).reshape(1, 1, 1)
        self.dem_std  = np.array([901.0], dtype=np.float32).reshape(1, 1, 1)

    def __len__(self):
        return self.total_samples

    def __iter__(self):
        # Distribute files if using multiple workers (though we use 0 to be safe)
        worker_info = torch.utils.data.get_worker_info()
        files = list(self.parquet_files)
        
        if self.shuffle:
            random.shuffle(files)
            
        if worker_info is not None:
            files = files[worker_info.id :: worker_info.num_workers]
            
        for pf in files:
            # Read PyArrow table (NO PANDAS!)
            table = pq.read_table(pf)
            splits = np.array(table.column("split").to_pylist())
            valid_indices = np.where(splits == self.split)[0]
            
            if len(valid_indices) == 0:
                del table
                continue
                
            if self.shuffle:
                np.random.shuffle(valid_indices)
                
            # Extract column references
            s2_bytes_col = table.column("s2_bytes")
            s2_shape_col = table.column("s2_shape")
            s1_bytes_col = table.column("s1_bytes")
            s1_shape_col = table.column("s1_shape")
            dem_bytes_col = table.column("dem_bytes")
            dem_shape_col = table.column("dem_shape")
            mask_bytes_col = table.column("mask_bytes")
            mask_shape_col = table.column("mask_shape")
            
            for idx in valid_indices:
                # Get shapes
                s2_shape = s2_shape_col[idx].as_py()
                s1_shape = s1_shape_col[idx].as_py()
                dem_shape = dem_shape_col[idx].as_py()
                mask_shape = mask_shape_col[idx].as_py()

                # Extract and decode raw bytes
                s2  = np.frombuffer(s2_bytes_col[idx].as_buffer(),  dtype=np.uint16).reshape(s2_shape).astype(np.float32)
                s1  = np.frombuffer(s1_bytes_col[idx].as_buffer(),  dtype=np.float32).reshape(s1_shape)
                dem = np.frombuffer(dem_bytes_col[idx].as_buffer(), dtype=np.int16).reshape(dem_shape).astype(np.float32)
                msk = np.frombuffer(mask_bytes_col[idx].as_buffer(), dtype=np.uint8).reshape(mask_shape).astype(np.float32)

                # Normalize using Z-score and clamp
                s2_norm  = np.clip((s2 - self.s2_mean) / self.s2_std, -10.0, 10.0)
                s1_norm  = np.clip((s1 - self.s1_mean) / self.s1_std, -10.0, 10.0)
                dem_norm = np.clip((dem - self.dem_mean) / self.dem_std, -10.0, 10.0)

                # Concatenate along channel axis -> (15, 224, 224)
                multimodal_tensor = np.concatenate([s2_norm, s1_norm, dem_norm], axis=0)

                # Ensure mask is (1, 224, 224)
                if msk.ndim == 2:
                    mask_tensor = msk[np.newaxis, ...]
                else:
                    mask_tensor = msk

                yield torch.from_numpy(multimodal_tensor), torch.from_numpy(mask_tensor)
            
            # Explicit garbage collection to prevent memory buildup
            del table
            del splits, valid_indices, s2_bytes_col, s2_shape_col, s1_bytes_col, s1_shape_col, dem_bytes_col, dem_shape_col, mask_bytes_col, mask_shape_col
            gc.collect()


# --- 2. Loss & Metrics ---
class BCEFocalDiceLoss(nn.Module):
    def __init__(self, bce_weight=0.33, focal_weight=0.33):
        super().__init__()
        self.bce = nn.BCEWithLogitsLoss()
        self.focal = smp.losses.FocalLoss(mode="binary")
        self.dice = smp.losses.DiceLoss(mode="binary", from_logits=True)
        self.bce_weight = bce_weight
        self.focal_weight = focal_weight
        self.dice_weight = 1.0 - (bce_weight + focal_weight)

    def forward(self, logits, targets):
        bce = self.bce(logits, targets)
        focal = self.focal(logits, targets)
        dice = self.dice(logits, targets)
        return (self.bce_weight * bce) + (self.focal_weight * focal) + (self.dice_weight * dice)


def calculate_iou(logits, targets, threshold=0.5):
    preds = torch.sigmoid(logits) >= threshold
    targets = targets >= 0.5
    
    tp = (preds & targets).sum().float()
    fp = (preds & ~targets).sum().float()
    fn = (~preds & targets).sum().float()
    
    return (tp / (tp + fp + fn + 1e-8)).item()


# --- 3. Training Loop ---
def train_one_epoch(model, loader, optimizer, criterion, device, scaler):
    model.train()
    total_loss = 0.0
    steps = 0

    pbar = tqdm(loader, desc="  train", leave=False)
    for images, masks in pbar:
        images = images.to(device, non_blocking=True)
        masks = masks.to(device, non_blocking=True)

        optimizer.zero_grad(set_to_none=True)
        
        with torch.amp.autocast(device_type="cuda", enabled=(device.type == "cuda")):
            logits = model(images)
            loss = criterion(logits, masks)

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        
        total_loss += loss.item()
        steps += 1
        pbar.set_postfix({"loss": f"{loss.item():.4f}"})

    return total_loss / max(1, steps)


@torch.no_grad()
def validate(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0
    total_iou = 0.0
    steps = 0

    pbar = tqdm(loader, desc="  val  ", leave=False)
    for images, masks in pbar:
        images = images.to(device, non_blocking=True)
        masks = masks.to(device, non_blocking=True)

        with torch.amp.autocast(device_type="cuda", enabled=(device.type == "cuda")):
            logits = model(images)
            loss = criterion(logits, masks)

        total_loss += loss.item()
        total_iou += calculate_iou(logits, masks)
        steps += 1

    return total_loss / max(1, steps), total_iou / max(1, steps)


# --- 4. Main Execution ---
def main():
    # =============== KAGGLE SETTINGS ===============
    DATA_DIR = r"cryosentinel_v3_train\data"
    OUTPUT_DIR = r"cryosentinel_v3_train\checkpoints"
    
    EPOCHS = 50
    BATCH_SIZE = 128
    LR = 3e-4
    
    # CRITICAL FIX FOR OOM: Set to 0. This forces data loading into the main process.
    # It prevents multiprocessing from hoarding memory and crashing Kaggle.
    NUM_WORKERS = 0
    # ===============================================

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    random.seed(42)
    np.random.seed(42)
    torch.manual_seed(42)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(42)

    # Dataloaders
    print("\nPreparing Training Data...")
    train_ds = CryoSentinelDataset(DATA_DIR, split="train", shuffle=True)
    # CRITICAL FIX FOR OOM: pin_memory=False stops PyTorch from exhausting locked page memory
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, num_workers=NUM_WORKERS, pin_memory=False)

    print("\nPreparing Validation Data...")
    val_ds = CryoSentinelDataset(DATA_DIR, split="val", shuffle=False)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, num_workers=NUM_WORKERS, pin_memory=False)

    # Model: U-Net with efficientnet-b4 encoder (ImageNet pretrained), 15 channels
    print("\nBuilding U-Net with efficientnet-b4 encoder (15 channels -> 1 channel)...")
    model = smp.Unet(
        encoder_name="efficientnet-b4",
        encoder_weights="imagenet",
        in_channels=15,
        classes=1,
        activation=None,
    ).to(device)

    if torch.cuda.device_count() > 1:
        print(f"Using {torch.cuda.device_count()} GPUs with nn.DataParallel!")
        model = nn.DataParallel(model)

    # Optimizer, Loss, Scaler
    optimizer = AdamW(model.parameters(), lr=LR, weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=EPOCHS, eta_min=1e-6)
    criterion = BCEFocalDiceLoss().to(device)
    scaler = torch.amp.GradScaler("cuda", enabled=(device.type == "cuda"))

    # Initialize CSV Logger
    log_file = Path(OUTPUT_DIR) / "training_log.csv"
    with open(log_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['epoch', 'train_loss', 'val_loss', 'val_iou', 'learning_rate'])

    # Training Loop
    best_iou = 0.0
    patience = 10
    epochs_no_improve = 0

    print(f"\nStarting training for {EPOCHS} epochs... (Early Stopping Patience: {patience})")
    for epoch in range(1, EPOCHS + 1):
        train_loss = train_one_epoch(model, train_loader, optimizer, criterion, device, scaler)
        val_loss, val_iou = validate(model, val_loader, criterion, device)
        scheduler.step()

        print(f"Epoch {epoch:03d}/{EPOCHS} | "
              f"Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f} | "
              f"Val IoU: {val_iou:.4f} | LR: {scheduler.get_last_lr()[0]:.2e}")

        # Write to CSV log
        with open(log_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([epoch, train_loss, val_loss, val_iou, scheduler.get_last_lr()[0]])

        if val_iou > best_iou:
            best_iou = val_iou
            epochs_no_improve = 0
            save_path = Path(OUTPUT_DIR) / "best_model.pth"
            
            # Unwrap model if using DataParallel
            state_dict = model.module.state_dict() if isinstance(model, nn.DataParallel) else model.state_dict()
            
            torch.save({
                "epoch": epoch,
                "state_dict": state_dict,
                "iou": best_iou
            }, save_path)
            print(f"  -> Saved new best model to {save_path.name} (IoU: {best_iou:.4f})")
        else:
            epochs_no_improve += 1
            print(f"  -> No improvement for {epochs_no_improve} epoch(s).")

        if epoch % 5 == 0:
            save_path = Path(OUTPUT_DIR) / f"epoch {epoch}.pth"
            state_dict = model.module.state_dict() if isinstance(model, nn.DataParallel) else model.state_dict()
            torch.save({
                "epoch": epoch,
                "state_dict": state_dict,
                "iou": val_iou
            }, save_path)
            print(f"  -> Saved model to {save_path.name}")
            
        if epochs_no_improve >= patience:
            print(f"\nEarly stopping triggered! Validation IoU did not improve for {patience} epochs.")
            print(f"Training stopped at epoch {epoch}. Best IoU was {best_iou:.4f}.")
            break


if __name__ == "__main__":
    main()



