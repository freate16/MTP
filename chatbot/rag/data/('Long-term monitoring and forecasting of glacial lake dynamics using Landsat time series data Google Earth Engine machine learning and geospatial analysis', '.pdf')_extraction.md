

# **Abstract**

Long-term simultaneous tracking of the dynamics of regional glacial lakes can help in identifying lakes prone to climate change and Glacial Lake Outburst Flood (GLOF). This study demonstrates a methodology of tracking the dynamics of glacial lakes using Landsat time series data and SRTM DEM of Sikkim Himalaya over three decades (1987–2020), using a random forest classifier (RFC) and an artificial neural network (ANN). The classifiers were trained with features like slope, hillshade, automated water extraction index, band ratio, modified normalized difference water index, normalized difference water index, and water ratio index. The performance of the classifiers were measured using parameters like Accuracy, Kappa, Sensitivity, Specificity, Precision, F1 score, and Area under the curve. Furthermore, imbalance tests were performed to validate the predictions of the classifiers. On average, RFC marginally outperformed ANN with an accuracy of 98%. The slope was the most important determinant in mapping the glacial lakes, followed by the automated water extraction index. Time series data generated from this method was used in forecasting the fate of numerous glacial lakes of the Sikkim Himalaya. Models like Brown's and Holt's exponential smoothing, and the random walk model were applied for forecasting. The forecasts were validated with varying degrees of accuracy. The proposed methodology helps in overcoming the challenges of mapping glacial lakes over a vast geographic area over a prolonged period and generates time series data of their spatial extent. The methodology demonstrated here will be useful for the long-term mapping and monitoring of glacial lakes all over the world.

**Keywords** Glacial lake, Google earth engine, Machine learning, Random forest, Time series, Forecasting

# 1 Introduction

Glacial Lakes (GLs) are a product of the complex interactions between the glacial terrain, topography, geology, hydrology, and climatic variables of a region [1, 2]. The formation and evolution of these GLs are driven by processes involving the accumulation

Image /page/1/Picture/12 description: The image shows the logo for Discover. On the left is a dark blue, circular, wave-like symbol. To the right of the symbol, the word "Discover" is written in a dark blue, sans-serif font with a capital 'D'.

© The Author(s) 2025. **Open Access** This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License, which permits any non-commercial use, sharing, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons licence, and indicate if you modified the licensed material. You do not have permission under this licence to share adapted material derived from this article or parts of it. The images or other third party material in this article are included in the article's Creative Commons licence, unless indicated otherwise in a credit line to the material. If material is not included in the article's Creative Commons licence and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit http://creativecommons.org/licenses/by-nc-nd/4.0/.

Banerjee Discover Geoscience (2025) 3:159 Page 2 of 33

of meltwater from glaciers behind natural dams like ice dams, moraines, or bedrock [3, 4]. The formation and expansion of GLs depend on the retreat of glaciers during deglaciation periods [5]. The expansion of GLs is viewed as a significant indicator of climate change, glacial lake outburst flood (GLOF), and accelerated melting of glaciers [6-12].

The intensity of change and the fate of these lakes are highly uncertain as they are very sensitive to temperature and precipitation [13, 14]. The retreating glaciers often leave behind proglacial lakes. Such lakes are fed by the melting water of the glacier till a critical volume is achieved that breaks the lake's boundary wall, leading to a glacial lake outburst flood (GLOF). The increase in ambient air temperature and land surface temperature in mountainous regions in comparison to other places in the past few decades has made the issue of GLOF a matter of concern [15, 16]. Therefore, continuous monitoring of the long-term dynamics of GLs is necessary for understanding the impacts of global warming on the glacial lakes and for assessing the GLOF risk. However, mapping the glacial lake using coarse-resolution satellite images is a challenging task due to the presence of snow, melting glaciers, debris, and mountain shadows. To address these challenges, water indices, like NDWI, derived from the image bands are used to highlight the GLs from the non-GL objects in the image [17-19]. Other derived indices like NDSI [17], MNDWI [19-21], slope and hillshade [14, 22, 23] have also been used by various researchers for the identification of GLs. These input images are used by experts as well as machine learning algorithms to discriminate pixels belonging to GL from non-GL objects.

Manual digitization of GLs has also been attempted using False Colour Composite (FCC) image in the Pumqu River Basin of Tibet using Landsat 8 and SRTM DEM images [24]. Similarly, manual mapping of GLs of Sikkim Himalaya was done using NDSI and NDWI derived from Resourcesat-2, LISS III sensor images, and SRTM DEM [17]. However, manual digitization of GLs over a large region and several observation periods is prone to subjective error. Often, such methods lack reliability and reproducibility due to the limitation of model validation parameters that machine learning has [17, 25, 26].

Several strategies have been adopted to demarcate the GLs. For instance, global threshold as well as local threshold of NDWI were used to map GLs, along with static thresholds of slope and hillshade, iteratively to distinguish GLs from other objects using Landsat images and SRTM DEMs [14]. A similar method was used to delineate the GLs of Sikkim Himalaya using Resourcesat-1, LISS III and Cartosat-I images [27]. Threshold-based studies have been used to map high altitude GLs of Asia using NIR, SWIR bands, and NDWI derived from Landsat 8 images along with slope derived from ASTER GDEM [26]. Threshold methods like Double-Window Flexible Pace Search (DFPS) and edge detection were used to determine the NDWI threshold for mapping GLs of Gangotri glacier using Sentinel 2 A images [28]. Beyond the threshold method and manual tracing of GLs, semi-automatic methods [11, 14, 18, 22, 24, 27-29], and automatic methods [20, 26] have also been successfully applied in mapping of GLs. It is worth noting that threshold-based mapping of GLs is only appropriate for GLs that have high spectral contrast for features like NDWI, slope, etc., as compared to their surroundings [14, 27]. It becomes even more difficult to apply the threshold method for small GLs in coarseresolution imageries that have mixed pixels containing debris, snow, and glaciers along with water [30]. Furthermore, mapping of GLs using threshold-based methods gets

Banerjee Discover Geoscience (2025) 3:159 Page 3 of 33

more challenging while considering variation in spatial, spectral, and temporal resolutions, due to the use of different satellites.

Since 2020, GL mapping has slowly migrated away from manual digitization and threshold-based methods to machine learning methods. Threshold-based methods heavily depend on a static threshold or a fixed set of thresholds of one or two features for GL mapping [26, 31]. In contrast, machine learning-based methods can consider multiple features and have the innate adaptability to consider varied thresholds over a wide range of features to map GLs [21, 32]. This adaptability gives an advantage to machine learning in mapping glacial lakes in a coarse-resolution image. Machine learning-based techniques [33] like Random Forest Classifier (RFC) have proven highly effective in GL mapping [30]. Convolutional Neural Network (CNN) like U-Net have also yielded high-accuracy mapping of GLs [21, 34, 35]. In recent times, GL mapping has become much more reliable owing to the availability of satellite imageries, like Landsat 8 and Sentinel 1 A and 2 A, having high spatial, spectral, and temporal resolutions, in public data archives. Additionally, machine learning techniques like deep learning have further reduced the computation time and improved the accuracy of image classification. However, the performance of a neural network heavily depends on a large and balanced dataset as compared to other machine learning methods like RFC [36, 37]. Besides, such studies have only focused on the current state of the GLs and not on the long-term behaviour of the lakes, primarily due to the lack of reliable data sources [21, 34].

The reason for the limited number of long term studies so far on the dynamics of glacial lakes is due to the limited accessibility and heterogeneity of long-term time series data of satellite from different sensors. For instance, Landsat 5 carried 7 spectral bands, including a single thermal band at 120 m. Landsat 7, in contrast, provided 8 bands, with its thermal band operating at 60 m. Both satellites offered 8-bit radiometry, allowing 256 brightness levels [38]. A major improvement came with Landsat 8, which operates with 11 spectral bands, including two thermal bands at 100 m. The multispectral resolution across all Landsat missions remained at 30 m, while thermal bands were resampled to 30 m. The most significant leap with Landsat 8 was its radiometric depth, expanded to 12-bit, providing 4096 brightness levels [38]. Nevertheless, several regions of the world still have historically sparse Landsat coverage. Fortunately, cloud computing platforms such as Google Earth Engine (GEE) now provide access to a large volume of orthorectified surface reflectance products and georeferenced data, including the complete Landsat time series archive. Online geocomputation in GEE enables generation of georeferenced outputs over large areas in very short time frames [39–41].

Change detection of GLs so far has been focused on the changes in the shape, size, number, and type of GLs over time [24, 42–44]. Many of these studies have documented decadal changes in total area and total number of GLs [29], time series analysis of selected GLs [22, 33, 45], observation period-based change detection of total number, total area and total types of GLs [46]. Change detection of regional GLs is a crucial step towards validation of the impacts of climate change on the cryosphere and hydrological regime. Moreover, understanding the dynamics of GLs is of paramount importance in GLOF mitigation. However, change detection can only provide qualitative information about the fate of the GLs under consideration. Only time series analysis and forecasting of individual lakes over a prolonged period can provide reliable data to foresee their change in surface area and volume [46]. Unfortunately, time series analysis of lakes have

Banerjee Discover Geoscience (2025) 3:159 Page 4 of 33

been confined to only one or very few lakes. The selection of such lakes remain highly subjective. Such studies do not shed any light on the fate of all the GLs of a region. In contrast, time series analysis of regional GLs has been performed by clubbing the GLs together in terms of the total number and total area. This kind of analysis does not shed any light towards the dynamics of individual lakes in the region. Moreover, time series analysis of selected lakes over a brief period does not provide reliable information on the long-term dynamics of the lakes. Forecasting models of the long-term dynamics of all the GLs over a regional extent have not yet been attempted [47, 48]. Most of these studies have avoided using multiple satellite data sources for time series-based forecasting models [49, 50]. This is most likely due to the lack of geospatial techniques to track individual glacial lakes over a large geographic extent and for long durations, such as several decades. Instead, most authors have manually tracked a few lakes that they considered relevant for their study. Hence, a methodology is required that provides long-term regional GL dynamics.

The objective of this study is to address this research gap by developing a new methodology of time series analysis and forecasting of GLs over a long period. For this, geocomputing using Landsat time series data on the GEE cloud computing platform was performed to prepare triennial median water indices, along with topographic indices. These indices were used to train a random forest classifier and an artificial neural network to identify the GLs. In this study, a glacial lake is defined as a lake, or a water body, formed by the action of a glacier. The dynamics of individual GLs were tracked using a unique lake ID (ULID). The ULIDs were used to prepare a time series dataset of the size of the lakes. Based on the time series dataset, the size of the lakes were projected up to 2026 using forecast models.

# 2 Materials and methods

## 2.1 Case study for demonstration

The area of interest (AOI) in this study is the northern part of Sikkim. Sikkim is a northeastern state of India located in the eastern sector of the Himalayas. It is characterised by mountainous topography along and across its territory. The elevation varies from 280 m in the south at the border with West Bengal to 8,586 m at Mt. Kanchenjunga, bordering Nepal. Sikkim has the highest number of glaciers in comparison to other Indian states or union territories. One of the most prominent glaciers in Sikkim is the Zemu Glacier. It is the largest glacier in the Eastern Himalayas, with a length of approximately 26 km. It is a source of water for numerous rivers, including the River Teesta. Unfortunately, the Zemu Glacier has been receding since the last century at an alarming rate [51], leaving lateral moraine ridges on either side of the glacier. Many glaciers of Sikkim are debris-covered to a varying extent, making them prone to differential melting. The rapid melting of glaciers due to climate warming has resulted in the formation and expansion of many glacial lakes. Several of these lakes are supraglacial and periglacial in location. These lakes are moraine- and ice-dammed. Climate change-induced retreating glaciers [52], acute cloud bursts [53], and melting of ice dams [54] are putting several of these glacial lakes under the category of potentially dangerous glacial lakes (PDGLs). For instance, Sikkim Himalaya currently has 14 PDGLs [55] (Fig. 1).

Banerjee Discover Geoscience (2025) 3:159 Page 5 of 33

Image /page/5/Figure/1 description: A figure from a scientific paper titled "AREA OF INTEREST" showing a map of a study area in the Sikkim Himalaya. An inset map in the upper right corner shows the location of Sikkim, highlighted in red, within India, bordering Nepal, China, and Bangladesh. An arrow points from the inset to the main map. The main map is a satellite image of a mountainous region with a grid overlay. The longitude lines range from 88.0°E to 88.8°E, and the latitude lines range from 27.2°N to 28.0°N. A legend in the top left explains the map's features: red areas are 'Glacial lakes', blue outlines indicate 'Glacier extent', and a semi-transparent overlay represents the 'Area of Interest'. The text explains that the Area of Interest (AOI) is defined by a 10 km buffer from the current glacier extent. The map includes a north arrow and a scale bar showing 0, 7.5, and 15 km. The figure caption at the bottom identifies it as "Fig. 1" and describes the study area as the Northern part of Sikkim.

**Fig. 1** The study area or AOI considered in this study is the Northern part of Sikkim, encompassing the glaciers and glacial lakes

## 2.2 Preparation of environmental feature raster maps in Google Earth engine

Google Earth Engine (GEE) is an open cloud-based online platform that archives geospatial data and provides a coding environment for geospatial analysis. GEE was used to compute several triennial median water indices from the Landsat 5 to 8 Surface Reflectance (SR) Tier 1 (T1) image archive for the period 1987 to 2020 (Fig. 2). The computation of the indices were confined to AOI. The AOI was prepared by buffering the glacier polygons of the Global Land Ice Measurements from Space (GLIMS) – Current [56]

Banerjee Discover Geoscience (2025) 3:159 Page 6 of 33

Image /page/6/Figure/1 description: A dual-axis combination chart displaying the number of images per year and the cumulative sum of images from 1987 to 2020. The x-axis represents the year. The primary y-axis on the left, labeled 'Images per year', ranges from 0 to 25. The secondary y-axis on the right, labeled 'Cumulative sum of images', ranges from 0 to 500. Blue vertical bars represent the 'images per year', showing fluctuations with a general upward trend. The number of images per year varies, with notable peaks in 1992 (approx. 16), 2006 (approx. 17), and a significant increase from 2012 onwards, peaking in 2018 at about 23 images. There is a sharp drop in 2002 and 2003. An orange line represents the 'cumulative sum of images', showing a steady and accelerating increase from near 0 in 1987 to approximately 475 by 2020. The chart is annotated with brackets indicating time periods labeled 'L5' (approx. 1988-2011), 'L7' (approx. 2011-2015), and 'L8' (approx. 2015-2019).

**Fig. 2** Landsat time series data from 1987–2020 of the Sikkim Himalaya. L5 is the Landsat 5 ETM sensor, L7 is the Landsat 7 ETM+sensor, and L8 is the Landsat 8 OLI/TIRS sensor. L5 and L7 have 11 bands, while L8 has 12 bands. The images are atmospherically corrected surface reflectance products using the Landsat Ecosystem Disturbance Adaptive Processing System (LEDAPS)/ Land Surface Reflectance Code (LaSRC). The images are masked from the interferences caused by cloud, shadow, water, and snow using the C Function of Mask (CFMASK), as well as a perpixel saturation mask

Image /page/6/Figure/3 description: A flowchart illustrating a multi-step process, likely for geographic or environmental analysis, divided into 11 steps. A large, curved blue arrow indicates the overall workflow direction. Each step is represented by a box containing icons and text labels.

Step 1: Starts with GLIMS data, processed by GEE to create an AOI (Area of Interest).
Step 2: Landsat Time Series Data is processed by GEE to produce Triennial Water Indices Maps.
Step 3: SRTM DEM data is processed by GEE to create Topographic Indices Maps.
Step 4: JRC GSW Unchanged Extent data undergoes 'Clip + Data Pruning + Ground Truthing' to produce an AOI.
Step 5: The 'Unchanged Extent of GLs' is used to generate 'Random Points', resulting in 'Class-1 (True) Points'.
Step 6: Openstreet Map data is used to create an AOI. This is combined with the 'Unchanged Extent of GLs' through a 'Buffer + Clip' process. 'Random Points' are then generated, resulting in 'Class-0 (False) Points'.
Step 7: 'Triennial Water Indices Maps', 'Topographic Indices Maps', 'Class-1 (True) Points', and 'Class-0 (False) Points' are combined to create an 'ML Training-Testing Dataset'.
Step 8: The 'ML Training-Testing Dataset' is used for 'Model Performance Tests' and 'Imbalance Tests' to generate 'Prediction Maps'.
Step 9: 'Prediction Maps' undergo 'Vectorization' to create 'GL Vector Maps'. These are then processed by the 'ULID Method' to produce 'ULID Tagged Maps'.
Step 10: 'ULID Tagged Maps' and 'Buffered JRC GSW Maximum Extent' data are used for 'Selection by Location' to create 'Externally Validated GLs'. These are then processed by 'Selection by Attribute' to produce a 'GL Time Series Dataset'.
Step 11: The 'GL Time Series Dataset' is used to create 'Forecast Models' and conduct 'Model Performance Tests'.

**Fig. 3** Visual summary of the methodology. *AOI* Area of Interest, *GLIMS* Global Land Ice Measurements From Space, *GL* Glacial Lake, *ML* Machine learning algorithm, *SRTM DEM* Shuttle Radar Topography Mission digital elevation model, *GEE* Google Earth Engine cloud computing, *ULID* Unique Lake Identifier, *JRC GSW* Joint Research Centre Global Surface Water Mapping

by 10 km [42] and clipping them with the Sikkim administrative boundary vector map extracted from the OpenStreetMap [57] (Step 1, Fig. 3).

Median values of the triennial period were considered in this study as they are better representatives of the water indices that are influenced by temporal variabilities and missing data [7, 33]. Water indices considered for this study were selected to highlight the water body features based on the spectral signature in the visible and infrared spectra. They included Automated Water Extraction Index with No Shadow (AWEI<sub>nsh</sub>), and Automated Water Extraction Index with Shadow (AWEI<sub>sh</sub>) [58–60], Band Ratio [46, 61], Modified Normalized Difference Water Index (MNDWI) [20, 62, 63], Normalized

Banerjee Discover Geoscience (2025) 3:159 Page 7 of 33

Difference Water Index using the Blue band (NDWI<sub>b</sub>) and Normalized Difference Water Index using the Green band (NDWI<sub>g</sub>) [17, 30], and Water Ratio Index (WRI) [64–66]:

$$AWEI_{nsh} = 4 \times (GREEN - SWIR1) - (0.25 \times NIR + 2.75 \times SWIR2)$$
 (1)

$$AWEI_{sh} = BLUE + 2.5 \times GREEN - 1.5 \times (NIR + SWIR1) - 0.25 \times SWIR2$$
 (2)

$$Band Ratio = \frac{GREEN}{NIR} \tag{3}$$

$$MNDWI = \frac{GREEN - SWIR1}{GREEN + SWIR1} \tag{4}$$

$$NDWI_b = \frac{BLUE - NIR}{BLUE + NIR} \tag{5}$$

$$NDWI_g = \frac{GREEN - NIR}{GREEN + NIR} \tag{6}$$

$$WRI = \frac{GREEN + RED}{NIR + SWIR2} \tag{7}$$

Where, GREEN and BLUE are representative visible bands of the Landsat bands. The NIR, SWIR 1 and 2 are the Near Infrared and Short Wavelength Infrared bands 1 and 2 of the Landsat bands (Step 2, Fig. 3). Beyond the water indices, two topographic features, namely slope [14, 22, 26] and hillshade raster maps [14, 27] were calculated in the GEE framework from the Shuttle Radar Topography Mission (SRTM) Version 3 (V3) digital elevation data of 30-meter resolution [67] (Step 3, Fig. 3). The slope and hillshade raster maps were calculated to further purify the water body feature extraction criteria (Table 1).

## 2.3 Preparation of the machine learning dataset in the GIS environment

JRC GSW V 1.3 provides the changes in surface water bodies from 1984 to 2020 with epochs 1984–1999 and 2000–2020, the maximum extent of global surface water, and the average monthly extent of surface water [68]. The unchanged extent of the GLs of the AOI extracted from the JRC GSW V 1.3 was clipped by the AOI, and the product was validated by ground truthing using high-resolution images of Google Earth as well as Sentinel 2 A. The main purpose of this verification was to ensure that the polygons of GLs generated from JRC GSW V 1.3 were confined within the actual images of GLs (Step 4, Fig. 3). After confirmation, these polygons were used to generate 1000 random points. These points represented instances of places with GLs in the Sikkim Himalaya. The point vector map was considered as the GL instances (Class-1) of GLs (Step 5, Fig. 3). Next, a

**Table 1** Performance of RFC and ANN in the prediction of the GLs

| Dataset                                                                                  | Source              | Purpose                                |
|------------------------------------------------------------------------------------------|---------------------|----------------------------------------|
| Global Land Ice Measurements from Space (GLIMS)                                          | Google Earth Engine | Glacier extent map                     |
| Sikkim administrative boundary                                                           | OpenStreetMap       | Study area vector<br>map               |
| Landsat 5 to 8 Surface Reflectance (SR) Tier 1 (T1)                                      | Google Earth Engine | Water indices                          |
| Shuttle Radar Topography Mission (SRTM) Version 3 (V3)                                   | Google Earth Engine | Topographic indices                    |
| Joint Research Centre Global Surface Water Mapping Layers<br>Version 1.3 (JRC GSW V 1.3) | Google Earth Engine | Reference map for<br>visual validation |

Banerjee Discover Geoscience (2025) 3:159 Page 8 of 33

buffer of 250 m was created around the unchanged surface water extent polygons. The radius of 250 m of the buffer was determined considering the maximum variation in size of most of these GLs. This buffer was used to erase portions of the AOI vector map to generate the polygon without any GLs. The latter was used to generate 3000 random points as places without GLs in the Sikkim Himalaya. The point vector map was considered as the non-GL instances (Class-0) of GLs (Step 6, Fig. 3). The normalized triennial median water indices and terrain feature raster maps were used to seed the Class-1 point and Class-0-point vector maps [69]. The tables of these point vector maps were used for training the ML algorithms (Step 7, Fig. 3). Redundant data instances, like the ones with an incomplete set of feature values, were removed from the dataset.

## 2.4 Training and testing of machine learning algorithms using the dataset

The dataset was split into 75% for training and the rest for testing the predictions. Next, the algorithms were trained on a specific triennial period (e.g., 1987–1990 or 2017–2020). Two machine learning algorithms were considered for classification, namely ANN and RFC. CNN was not considered in this study as it was not a viable classifier for the study. Unlike the classification of a single image, as has been done in most studies involving U-Net [36, 48, 63], this study required the image classification of varied images from sources like Landsat 5 to 8 and SRTM data, at various times. At different times, the same lake may have a different shape, spectral signature, and snow thickness. Thereby, instead of relying on the image properties as used by CNN for image classification, pixel properties as used by RFC and ANN were incorporated to avoid misclassification of the images.

## 2.5 Machine learning algorithms

A neural network is inspired by the working of the brain, where neurons, the nerve cells, create a network of communication for information processing. An ANN includes an input layer, one or several hidden layers and an output layer. The input layer contains M nodes that receive the feature values from the feature matrix X of the training dataset. The nodes of the hidden layers accept a weighted linear combination of the feature values  $\alpha_m^T X$  along with a bias  $\alpha_{0m}$  and uses an activation function  $\sigma$  to generate derived features  $Z_m$  (Eq. 8) [70]:

$$Z_m = \sigma \left( \alpha_{0m} + \alpha_m^T X \right) \tag{8}$$

A weighted linear combination of the derived features generated from each hidden layer is forwarded to the next hidden layer. An activation function is used in the output layer to convert the response from the hidden layers into a classifier output as a Class-0 or Class-1 class pixel. A cost function, usually cross-entropy, is used to compare the agreement between the predicted and actual values of the target variable. The error is minimized by the backpropagation algorithm [70].

In contrast to the ANN, RF uses decision trees to classify the feature space. The decision tree is an algorithm that divides the feature space iteratively into regions  $R_m$  by selecting M splitting points called *nodes*,  $m=1,\cdots,M$ . A node splits the feature space along a specific feature dimension, subject to the minimization of the error function. In the process  $N_m$  instances of the training dataset end up belonging into  $R_m$  region of the feature space. These instances are then classified as the kth class from a set of classes

Banerjee Discover Geoscience (2025) 3:159 Page 9 of 33

 $k = 1, \dots, K$ , of the target variable. Hence, the proportion  $\widehat{p}_{mk}$  of training instances at node m representing kth class is represented as [70] (Eq. 9):

$$\widehat{p}_{mk} = \frac{1}{N_m} \sum_{x_i \in R_m} I(y_i = k) \tag{9}$$

The impurity of the classification is usually assessed by the Gini index or cross-entropy function. RF uses bootstrapping and bagging algorithms of the training dataset to reduce prediction errors [70].

## 2.6 Model performance and variable importance

The performance of the algorithms in classifying test instances correctly was estimated by model performance criteria [71, 72]. Accuracy is an overall measure of the model's performance. Sensitivity is the probability of correctly classifying Class-1 instances, while specificity is the probability of correctly classifying Class-0 instances out of the total positively classified instances. Precision is the probability of correctly classifying Class-1 instances from the total number of Class-1 instances. A model with a high F1 score indicates that the model has a balance between precision and sensitivity. Cohen's kappa is a measure of the agreement between the observed and the predicted values by considering whether the prediction is merely a chance event. Beyond the indices derived from the confusion matrix, another popular criterion is the Area Under the Curve (AUC) derived from the Receiver Operating Characteristic (ROC) curve. ROC curve plots the change in the sensitivity over the specificity of a prediction model. AUC nearing a value of one is a good measure of the model's performance. These criteria were used to select the best model to predict the category of the pixels of the entire AOI into GLs and non-GLs.

An imbalanced dataset was used to train the machine learning algorithms in this study. It has been observed that an imbalanced dataset may cause a certain degree of bias in the prediction process by a machine learning algorithm, giving favour to the majority class. To validate the use of the imbalanced dataset, four imbalance tests were performed on the dataset, namely, under-sampling [73, 74] of the majority class and over-sampling of the minority class by simple over-sampling, synthetic minority over-sampling technique (SMOTE), and random oversampling examples (ROSE) [73, 75–77] (Step 8, Fig. 3).

Variable importance measures how many times a feature or a predictor variable is called by a machine learning algorithm for the prediction. The more a feature is called for prediction, the greater its importance for the algorithm. In the case of the RFC, the mean decrease in impurity by the Gini index is used for measuring the variable importance [70].

## 2.7 Preparation of the time series dataset from prediction raster maps

The vectorized prediction maps of all the triennial intervals were edited to remove issues like holes inside the polygons, clusters of polygons representing a single GL, and misclassified polygons. The editing process involved the use of an elimination tool to remove the holes.

Union of all the triennial vector maps was done to prepare the historical maximum extent of the GLs. The polygons that were overlapping and in very close proximity to each other (30 m) were aggregated to generate the final vector map of the historical

Banerjee Discover Geoscience (2025) 3:159 Page 10 of 33

maximum extent of the GLs. The selection by location tool was used to link individual polygons of a specific triennial vector map with the vector map of the historical maximum extent of the GLs. In this process, each polygon of individual triennial vector maps was now linked with the unique *Object Identity (OID) of the polygons of the vector map of the historical maximum extent of the GLs, hereby called Unique Lake ID* (ULID) (Step 9, Fig. 3).

After this process, all the triennial vector maps were joined by attributes, based on the ULID common to the polygons of the triennial vector maps. The dissolve tool was used to pool the polygons with the same ULID into a single polygon for each triennial vector map. Next, the JRC GSW V 1.3 maximum surface water extent map was vectorized and buffered by a 250 m radius. Polygons belonging to the triennial GL-vector maps that intersected with the JRC GSW V 1.3 maximum surface water extent map were selected by location and exported as vector maps. The 250 m radius was considered to eliminate any possibility of ignoring a GL polygon that has possibly been overlooked in JRC GSW V 1.3. The triennial vector maps were then joined by attributes using ULID into a single table. Each column of this table represents the time series of individual GL area over the triennial intervals from 1987 to 2020 (Step 10, Fig. 3). The uncertainty of the prediction of GL area was estimated by considering an error of one pixel on either side of the glacial lake polygon perimeter (Eqs. 10–11):

$$e = n^{1/2} \times m \tag{10}$$

$$R = \frac{e}{A} \times 100\% \tag{11}$$

Where, e is the absolute area error in  $m^2$  of the GL, n is the number of pixels on the GL perimeter, approximated to the ratio of the GL perimeter to the spatial resolution of the satellite image, which is 30 m in the case of Landsat, m is the area of each pixel, and A is the GL area.

### 2.7.1 Time series model-based forecasting of glacial lake areas

Forecast modelling of the GLs was performed using the SPSS statistical package. The Expert Modeller extension of SPSS was used to automatically select the appropriate forecast model based on the performance criteria. The time series dataset used in this study was free of any seasonality and independent variables, apart from time. Thereby, three types of time series methods were used to forecast the dynamics of the GLs based on their performance over the time series dataset. Amongst them, Brown's Simple Exponential Smoothing [78] states that the forecast F at time t+1 is (Eq. 12) [79]:

$$F_{t+1} = \alpha A_t + (1 - \alpha) F_t \tag{12}$$

Given  $F_1=A_1$ . Here  $F_t$  and  $A_t$  are the forecasted and actual values of the lake area at time t.  $0 \le \alpha \le 1$  is the smoothing constant. A higher  $\alpha$  gives more weightage to the recent observations, while a lower  $\alpha$  makes the forecast more dependent on past observations. However, Brown's model fails to show any trend. The trend of a time series is captured in Holt's Linear Exponential Smoothing Model. According to this model (Eqs. 13–14) [79, 80]:

$$F_t = \alpha A_{t-1} + (1 - \alpha) (F_{t-1} + T_{t-1})$$
(13)

Banerjee Discover Geoscience (2025) 3:159 Page 11 of 33

$$T_{t} = \beta \left( F_{t} - F_{t-1} \right) + \left( 1 - \beta \right) T_{t-1} \tag{14}$$

$$F_{t+1} = F_t + T_t \tag{15}$$

Given  $F_1=A_1$  and  $T_1=0$ .  $0\leq \alpha \leq 1$  and  $0\leq \beta \leq 1$  are the smoothing constants. The forecast F at time t+1 is the sum of the forecast and trend T components at time t. The dependency of the trend component on the recent forecasts decline and shift towards the historical trend with the fall in  $\beta$ . Other parameters hold the same meaning as stated in Eq. 24. In the case of non-stationary random walk time series, the value of time t+1 is expressed as (Eq. 16):

$$A_{t+1} = A_t + w_t \tag{16}$$

where  $w_t$  is the residual. In general, a random walk model can be expressed as the sum of all the residuals of the time series. A differencing of lag 1 is used to estimate the statistics of the series. The mean of such a series will be zero, while the variance of the series will be time-dependent. Thereby, the forecast of such a series is (Eq. 17):

$$F_{t+1} = F_t + d \tag{17}$$

where  $d=\frac{(A_t-A_1)}{(t-1)}$  is the drift of the series. The non-stationary random walk model can be evaluated using the Autoregressive Integrated Moving Average (ARIMA) of the (0,1,0) type. Several time series model performance criteria were considered for this study, namely, Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), Mean Absolute Percentage Error (MAPE), R-squared, and Stationary R-squared [79, 81]. A time series model with RMSE and MAE close to zero, a low MAPE value and a stationary R-squared nearing one indicates a consistent time series and a good forecast model (Step 11, Fig. 3).

# 3 Results

## 3.1 Algorithm architecture

The Classification And REgression Training (CARET) package in the R programming language was used to construct the aforesaid machine learning algorithms. The Stuttgart Neural Network Simulator with two hidden layered backpropagation perceptron was used as the ANN [82]. Each hidden layer had 18 nodes. The logistic function was used as the default activation function in the hidden layers. The Identity activation function was used in the input layer to feed the GL and non-GL instances of the dataset into the ANN. The same function was also used as the output activation function in classifying the training instances. The architecture of the ANN was based on the trial-and-error method. The architecture of the RF included 500 decision trees. The optimal performance of the RF was achieved by randomly splitting two feature variables at a time from the feature space. The RF, as well as ANN, used tenfold cross-validation on the training dataset that had nine predictors and two classes. The average Out-of-the-Box error of RF was 0.65%.

## 3.2 Feature variables and their relationship with the target variables

Feature variables used as inputs in the training of the machine learning classifiers showed dynamic correlations over time. The average of the water indices of the time

Banerjee Discover Geoscience (2025) 3:159 Page 12 of 33

series was used for Pearson correlation analysis (Fig. 4). Hillshade was weakly correlated with all the other feature variables. Slope, in contrast, showed moderate negative correlations with Band ratio, MNDWI, NDWI<sub>b</sub>, NDWI<sub>g</sub>, and WRI, primarily attributed to the Class-1 instances responsible for GLs. AWEI<sub>nsh</sub> had a very strong positive correlation with AWEI<sub>sh</sub>, while a strong positive correlation with other water indices. AWEI<sub>sh</sub> had an overall moderate positive correlation with the Band ratio, and a strong correlation with MNDWI, NDWI<sub>b</sub>, NDWI<sub>g</sub>, and WRI. However, it was observed that AWEI<sub>sh</sub> had a moderate correlation with other water indices as far as Class-1 instances were concerned. Band ratio showed a very strong positive correlation with NDWI<sub>g</sub> and WRI, while a strong positive correlation with MNDWI and NDWI<sub>b</sub>, mainly due to the lower correlation value of Class-1 instances. MNDWI had a very strong positive correlation with NDWI<sub>g</sub> and WRI. NDWI<sub>b</sub> was very strongly correlated with NDWI<sub>g</sub>

Image /page/12/Figure/2 description: A scatterplot matrix, also known as a pair plot, displaying the relationships and correlations between several variables for two different groups, color-coded in red and teal. The variables analyzed are: hillshade, slope, Ave\_AWEInsh, Ave\_AWEIsh, Ave\_BandRatio, Ave\_MNDWI, Ave\_NDWIg, Ave\_WRI, and label. The matrix is structured as follows:

1. \*\*Diagonal Panels:\*\* These show the density plots for each variable, illustrating the distribution for the red group and the teal group separately.
2. \*\*Lower Triangle Panels:\*\* These contain scatter plots for each pair of variables. The points are colored red or teal, and a regression line is fitted for each color group to show the trend.
3. \*\*Upper Triangle Panels:\*\* These display the Pearson correlation coefficient ('Corr:') for each pair of variables, calculated separately for the two groups (labeled '0:' for red and '1:' for teal). The significance of the correlation is indicated by asterisks (e.g., \*, \*\*, \*\*\*). For example, the correlation between 'slope' and 'hillshade' is -0.150\*\*\* for group 0 and -0.164\*\* for group 1. The correlation between 'Ave\_AWEIsh' and 'Ave\_AWEInsh' is 0.903\*\*\* for group 0 and 0.867\*\*\* for group 1.
4. \*\*Last Column ('label'):\*\* This column contains box plots for each variable, showing the distribution and quartiles for the two groups side-by-side.
5. \*\*Last Row ('label'):\*\* This row contains histograms for each variable, again separated by the two color-coded groups.

**Fig. 4** Image matrix of Pearson correlation analysis of the machine learning model inputs. A correlation analysis was performed on the average values of the model inputs or feature variables. The diagonal images of this image matrix show the distribution of feature variable-wise distribution of Class-0 [Red] and Class-1 [Blue] instances, representing the non-glacial lake values and glacial lake values of the feature variable, respectively. The lower triangle of the image matrix shows the scatterplots of the feature variable values and their best-fitting linear regression curves of Class-0 [Red] and Class-1 [Blue] instances, respectively. The upper triangle of the image matrix shows the overall correlation between a pair of feature variables in black, while the red and blue values are the correlation values of Class-0 and Class-1 instances, respectively. The last row of the image matrix shows a histogram of the Class-0 [Red] and Class-1 [Blue] instances of the feature variables. The last column of the image matrix shows the proportion of Class-0 [Red] and Class-1 [Blue] instances considered for the correlation analysis

Banerjee Discover Geoscience (2025) 3:159 Page 13 of 33

and WRI, primarily due to Class-0 instances representing non-GLs.  $NDWI_g$  was very strongly correlated with WRI.

The density plots shown as the diagonal plots in Fig. 4 have revealed that topographic indices, namely hillshade and slope, have distinct distributions for GL (Class–1) and non-GL (Class–0) instances. While the Class–1 distribution showed leptokurtosis, the Class–0 distribution had platykurtosis. Similar distributions were observed in the cases of NDWI $_{\rm b}$ , MNDWI, and AWEI $_{\rm nsh}$ . In contrast, platykurtosis was observed in the Class–1 distribution and leptokurtosis in the Class–0 distribution in the cases of NDWI $_{\rm g}$  and Band ratio. Bimodal and partly overlapping distributions of Class–1 and Class–0 were observed in the cases of AWEI $_{\rm sh}$  and WRI.

## 3.3 Model performances

When the performance is compared, both ANN and RFC models are found to be efficient. However, on average, classifications done by RFC were better than those of ANN in terms of the performance criteria over all the triennial periods. A marginal decline in the sensitivity of RFC in comparison to ANN was observed in triennials like 1990–1993 and 2011–2014. However, in comparison to ANN, the performance of RFC marginally declined for the triennial period of 2002–2005 in terms of specificity and precision (Table 2). The high values of performance criteria in the imbalance tests have shown that the imbalanced data in the dataset did not create any bias in the prediction (Supplementary Table S1). The RFC-based image classification successfully traced the boundaries of GLs over all the triennials. This can be observed by comparing the RFC-generated vector map with the True Colour Combination (TCC) and False Colour Combination

**Table 2** Variable importance as percentage of the total usage of the variables used by RFC in the prediction

| Triennial-wise<br>performance of<br>the algorithms | Accuracy | Kappa | Sensitivity | Specificity | Precision | F1    | AUC   |
|----------------------------------------------------|----------|-------|-------------|-------------|-----------|-------|-------|
| RFC 1987–1990                                      | 0.994    | 0.983 | 0.995       | 0.989       | 0.996     | 0.996 | 0.992 |
| ANN 1987–1990                                      | 0.989    | 0.970 | 0.990       | 0.986       | 0.995     | 0.992 | 0.988 |
| RFC 1990–1993                                      | 0.992    | 0.978 | 0.994       | 0.983       | 0.994     | 0.994 | 0.992 |
| ANN 1990–1993                                      | 0.989    | 0.971 | 0.995       | 0.970       | 0.990     | 0.993 | 0.983 |
| RFC 1993–1996                                      | 0.992    | 0.978 | 0.994       | 0.983       | 0.994     | 0.994 | 0.989 |
| ANN 1993–1996                                      | 0.988    | 0.967 | 0.994       | 0.970       | 0.990     | 0.992 | 0.982 |
| RFC 1996–1999                                      | 0.992    | 0.978 | 0.995       | 0.981       | 0.994     | 0.994 | 0.988 |
| ANN 1996–1999                                      | 0.990    | 0.972 | 0.995       | 0.975       | 0.992     | 0.993 | 0.985 |
| RFC 1999–2002                                      | 0.992    | 0.980 | 0.995       | 0.985       | 0.995     | 0.995 | 0.990 |
| ANN 1999–2002                                      | 0.987    | 0.965 | 0.992       | 0.972       | 0.991     | 0.991 | 0.982 |
| RFC 2002–2005                                      | 0.993    | 0.980 | 0.997       | 0.979       | 0.993     | 0.995 | 0.988 |
| ANN 2002–2005                                      | 0.987    | 0.965 | 0.989       | 0.981       | 0.994     | 0.991 | 0.985 |
| RFC 2005–2008                                      | 0.993    | 0.980 | 0.996       | 0.984       | 0.995     | 0.995 | 0.990 |
| ANN 2005–2008                                      | 0.988    | 0.967 | 0.993       | 0.973       | 0.991     | 0.992 | 0.983 |
| RFC 2008–2011                                      | 0.993    | 0.981 | 0.997       | 0.980       | 0.994     | 0.995 | 0.989 |
| ANN 2008–2011                                      | 0.987    | 0.964 | 0.995       | 0.962       | 0.987     | 0.991 | 0.978 |
| RFC 2011–2014                                      | 0.993    | 0.982 | 0.996       | 0.986       | 0.996     | 0.996 | 0.991 |
| ANN 2011–2014                                      | 0.988    | 0.968 | 0.996       | 0.964       | 0.988     | 0.992 | 0.980 |
| RFC 2014–2017                                      | 0.993    | 0.981 | 0.995       | 0.986       | 0.995     | 0.995 | 0.991 |
| ANN 2014–2017                                      | 0.987    | 0.966 | 0.994       | 0.969       | 0.990     | 0.992 | 0.981 |
| RFC average                                        | 0.992    | 0.980 | 0.995       | 0.984       | 0.995     | 0.995 | 0.990 |
| ANN average                                        | 0.988    | 0.968 | 0.993       | 0.972       | 0.991     | 0.992 | 0.983 |

Banerjee Discover Geoscience (2025) 3:159 Page 14 of 33

(FCC) images as ground truth of selected GLs over the triennial periods (Fig. 5a, b). Furthermore, the selected GLs, predicted using the water indices generated from Landsat 8 time series data and topographic indices, were overlaid on Sentinel 2 A image for ground truthing (Fig. 6). Overall, RFC performed better than ANN in classifying AOI into GL and non-GL pixels. Thereby, the GL maps generated by RFC were considered as defaults for further analysis.

## 3.4 Variable importance

Based on the performance of RFC, Slope remained the most important determinant in identifying the GLs. It scored highest on the importance scale in all the triennials. AWEI $_{\rm sh}$  was the next most important contributor in identifying the GLs. Its contribution showed an increasing trend in the recent triennial periods. For instance, AWEI $_{\rm sh}$  significantly contributed to the identification of GLs in the triennials like 2002–2005, 2005–2008, 2008–2011, 2011–2014, and 2017–2020. In contrast, its importance was rather low in 1987–1990. AWEI $_{\rm nsh}$  showed the importance of the triennials like 2008–2011 and 2011–2014. NDWI $_{\rm b}$  was more important than NDWI $_{\rm g}$  in several triennials like 1987–1990, 1990–1993, 1993–1996, 1999–2002, 2005–2008, and 2008–2011 (Table 3).

## 3.5 Maps of the glacial lakes

A total of 492 polygons were traced by the RFC and vectorized in the GIS framework. However, only 406 such polygons were considered GLs, as the remainder were considered traces of streams, a reflection of snow, an area less than 0.01 km<sup>2</sup> or other forms of misclassifications. The spatial distribution of these GLs showed that most of the larger GLs, like GL- 46, 83, 81, 174, and 9, were located at the snout of glaciers and were essentially periglacial lakes. In contrast, some GLs were not fed by glaciers. These GLs are spatially isolated from their feeder glacier. These GLs are the erosion lakes, like GL 23, 270, and 266, to name a few (Fig. 7a – d). GLs of area no less than 0.1 km<sup>2</sup> were considered for a size-altitude-wise distribution analysis. It was shown that most of the GLs were confined to altitudes above 4000 m to 6000 m. The larger lakes were arbitrarily considered as GLs with an area greater than 0.4 km<sup>2</sup>. Lakes like 3, 5, 27, 34, 39, 49, 51, 81, 110, 121, and 174, were found to be large lakes (Fig. 8).

The relative error varied between 1.1% and 43.3%, with bulk error contributed by small GLs (0.01 to 0.02 km<sup>2</sup>) (Fig. 9). Lesser variation in relative error was observed in the triennial period of 1990–1993, and from 2005 to 2020. A look at the relation of error value and GL area showed that a lower GL area had an inflating effect on the relative error, indicating an exponential relationship between error and area.

## 3.6 Time series and forecast of glacial lakes

A total of 144 GLs had 11 observation periods, 39 GLs had 10 observation periods, 14 GLs had 9 observation periods, 16 GLs had 8 observation periods, 17 GLs had 7 observation periods, 20 GLs had 6 observation periods, 23 GLs had 5 observation periods, 18 GLs had 4 observation periods, 31 had 3 observation periods, 24 GLs had 2 observation periods and 60 GLs had only one observation period. The GLs showed varied patterns of change in their areas over the period considered. A detailed account of their behaviour over time can be observed in Supplementary Figure S1 a-h. Linear regression model and Lasso regression model were fit into the time series data with 11 and 10

Banerjee Discover Geoscience (2025) 3:159 Page 15 of 33

Image /page/15/Figure/1 description: A figure, labeled "Fig. 5 a", showing the temporal evolution of a glacial lake from 1990 to 2020. The figure is organized as a grid with three columns and eleven rows. The columns are titled "TCC Image", "FCC Image", and "Vector map". Each row corresponds to a specific year: 1990, 1993, 1996, 1999, 2002, 2005, 2008, 2011, 2014, 2017, and 2020. The "TCC Image" column displays true-color composite satellite images of the lake and surrounding glacier. The "FCC Image" column shows false-color composite images where the lake appears in shades of blue. The "Vector map" column presents a map with the lake's area outlined and filled with diagonal hatching. Across the years, the images in all three columns clearly show a significant increase in the size of the lake. The caption at the bottom reads: "Fig. 5 a Ground truth of South Lhonak Lake, GL – 83 (Coordinate: 27.9125, 88.1952) by comparing the Random..."

**Fig. 5** a Ground truth of South Lhonak Lake, GL – 83 (Coordinate: 27.9125, 88.1952) by comparing the Random Forest Classifier generated vector map with True Colour Combination (TCC), False Colour Combination (FCC) images. The vector map is superimposed over the high-resolution Google satellite image of the current state of the lake. TCC and FCC of the year 2014 have anomalies due to partial malfunction of the Landsat 7 Sensor in 2003, which led to the loss of a large number of satellite images (https://earthobservatory.nasa.gov/features/GlobalLandSurvey/page2.php). **b**: Ground truth of North Lhonak Lake, GL – 81 (Coordinate: 27.9193, 88.1591) by comparing the Random Forest Classifier generated vector map with True Colour Combination (TCC), False Colour Combination (FCC) images

Banerjee Discover Geoscience (2025) 3:159 Page 16 of 33

Image /page/16/Picture/1 description: A figure displaying a time-series of satellite imagery of a glacier from 1990 to 2020. The figure is organized into a grid with three columns and eleven rows. Each row corresponds to a specific year: 1990, 1993, 1996, 1999, 2002, 2005, 2008, 2011, 2014, 2017, and 2020. The three columns are labeled 'TCC' (True Color Composite), 'FCC' (False Color Composite), and 'Vector map'. The TCC column shows natural-color images of the glacier and a proglacial lake. The FCC column displays false-color images where the glacier and water are highlighted in shades of blue and cyan. The 'Vector map' column shows a grayscale image with a hatched black outline delineating the glacier's extent. Over the years, the images consistently show the glacier retreating and the lake at its terminus expanding. The images for 2014 have diagonal black stripes indicating missing data, and the images for 2020 are in grayscale. The bottom of the image has the text 'Fig. 5 (continued)'.

Fig. 5 (continued)

observation periods. Certain GLs like GL.9, GL.27, GL.49, etc. showed a robust increasing trend, while GLs like GL.19, 150, and 359 showed a decreasing trend. GLs with 11 and 10 observation periods were considered for time series analysis. The missing area value for GLs with 10 observation periods was calculated as the average of the predecessor and successor area values of the missing observation period. In most cases, GLs showed very irregular dynamics. Therefore, forecasting their future area dynamics was not viable using time series analysis (Supplementary Figure S2).

A total of 48 GLs were considered in this study based on their performances according to the time series forecast criteria (Table 4). Also, GLs with no clear trend were not considered for further interpretations. Out of these GLs, time series of 26 were forecasted

Banerjee Discover Geoscience (2025) 3:159 Page 17 of 33

Image /page/17/Figure/1 description: A figure, labeled Fig. 6, comparing satellite images of six glacial lakes from two different sources: Landsat 8 and Sentinel 2A MSI. The figure is a grid with two columns and six rows. The left column shows images from Landsat 8, and the right column shows higher-resolution images of the same lakes from Sentinel 2A MSI. Each row represents a different lake, labeled on the left as GL - 81, GL - 79, GL - 39, GL - 27, GL - 34, and GL - 3. The lakes, which are outlined in red, are shown in various shapes and sizes amidst mountainous and snowy terrain. The caption below the figure reads: 'Fig. 6. Ground truthing of glacial lakes of the Trippeal period 12/2014–12/2017 prepared from the median image.'

**Fig. 6** Ground truthing of glacial lakes of the Trinneal period 12/2014–12/2017 prepared from the median image of Landsat 8 OLI/TIRS Collection 2 atmospherically corrected surface reflectance of 30 m resolution by the median image of Sentinel-2 MSI Orthorectified Surface reflectance Level-2 A of 10 m resolution of the duration 01/2020–12/2021

Banerjee Discover Geoscience (2025) 3:159 Page 18 of 33

**Table 3** Performance of timeseries models

| Triennial periods | Environmental features |         |        |           |       |       |       |      |       |  |
|-------------------|------------------------|---------|--------|-----------|-------|-------|-------|------|-------|--|
|                   | hillshade              | AWEInsh | AWEIsh | BandRatio | MNDWI | NDWIb | NDWIg | WRI  | slope |  |
| 1987–1990         | 6.61                   | 9.20    | 9.21   | 8.56      | 6.50  | 8.21  | 8.60  | 6.80 | 36.33 |  |
| 1990–1993         | 7.30                   | 6.92    | 10.66  | 7.76      | 6.82  | 8.07  | 7.75  | 8.08 | 36.64 |  |
| 1993–1996         | 6.74                   | 5.62    | 10.31  | 5.96      | 5.71  | 7.48  | 5.91  | 6.95 | 45.32 |  |
| 1996–1999         | 6.53                   | 6.75    | 11.12  | 6.56      | 8.38  | 6.75  | 6.45  | 6.57 | 40.90 |  |
| 1999–2002         | 6.64                   | 7.22    | 10.42  | 6.83      | 6.74  | 9.92  | 6.19  | 8.05 | 38.00 |  |
| 2002–2005         | 7.84                   | 8.42    | 14.17  | 8.14      | 6.78  | 8.25  | 8.60  | 8.16 | 29.65 |  |
| 2005–2008         | 5.18                   | 6.54    | 16.85  | 6.07      | 5.95  | 6.06  | 5.57  | 6.68 | 41.10 |  |
| 2008–2011         | 7.23                   | 9.08    | 14.33  | 10.17     | 6.92  | 9.59  | 9.44  | 8.15 | 25.10 |  |
| 2011–2014         | 5.89                   | 10.03   | 15.63  | 7.17      | 5.73  | 10.80 | 8.19  | 5.02 | 31.56 |  |
| 2011–2017         | 6.46                   | 6.86    | 13.08  | 5.99      | 9.05  | 6.11  | 7.47  | 9.05 | 35.93 |  |
| 2017–2020         | 5.98                   | 7.06    | 14.74  | 7.21      | 9.53  | 6.50  | 7.28  | 8.44 | 33.26 |  |
| Average           | 6.58                   | 7.61    | 12.77  | 7.31      | 7.10  | 7.98  | 7.40  | 7.45 | 35.80 |  |

Image /page/18/Figure/3 description: A map titled "Historical maximum extent of the glacial lakes in the North-West Quadrant." The main map is a topographical representation of a mountainous region, showing features marked with latitude and longitude coordinates. On the right side, there are two smaller inset maps. The top one is a circular map showing the location of the area within the Himalayas, near India and Myanmar. An arrow points from this map to a second, lower inset map that shows the full watershed with its river systems. Another arrow points from the watershed map to the main, detailed map. The main map includes a legend in the bottom right corner that defines the symbols used: a blue line for Rivers, a red outline for Glacial lakes, a blue-hatched area for Glacier extent, and a black outline for the AOI\_fishnet\_grid. The map is populated with numerous red-outlined glacial lakes, each labeled with a number.

Fig. 7 a Historical maximum extent of the GLs of Sikkim Himalaya in the North-West quadrant of the area of interest. The lake polygons have been constructed by the union of all the lake polygons with the same Unique Lake ID (ULID) over various observation periods. The number adjacent to the polygons indicates the ULID of the lake. **b** Historical maximum extent of the GLs of Sikkim Himalaya in the North-East quadrant of the area of interest. The lake polygons have been constructed by the union of all the lake polygons with the same Unique Lake ID (ULID) over various observation periods. The number adjacent to the polygons indicates the ULID of the lake. **c** Historical maximum extent of the GLs of Sikkim Himalaya in the South-East quadrant of the area of interest. The lake polygons have been constructed by the union of all the lake polygons with the same Unique Lake ID (ULID) over various observation periods. The number adjacent to the polygons indicates the ULID of the lake. **d** Historical maximum extent of the GLs of Sikkim Himalaya in the South-West quadrant of the area of interest. The lake polygons have been constructed by the union of all the lake polygons with the same Unique Lake ID (ULID) over various observation periods. The number adjacent to the polygons indicates the ULID of the lake

by the Holt model, 10 by the Brown model, 7 by the Random Walk model and 4 by the Simple exponential model. Out of the 48 forecasts, 32 GLs were increasing, 12 were decreasing, and 4 showed irregular behaviour. On an average, larger GLs were increasing in size (Fig. 10a - d), while smaller GLs showed decreasing or irregular trends (Fig. 10e - g).

Banerjee Discover Geoscience (2025) 3:159 Page 19 of 33

Image /page/19/Figure/1 description: A geographical map titled "Historical maximum Extent of the glacial lakes in the North East Quadrant." The main map displays a mountainous region with topographical details, marked with latitude and longitude lines. It features blue lines representing rivers, numerous red-outlined shapes indicating glacial lakes (each with a number), and areas with diagonal hatching that represent glacier extent. A north arrow is in the top left, and a scale bar in kilometers is at the bottom. On the right, two inset maps provide context. The top circular inset shows the location of the area within India, near the Himalayas. Below it, a map of a larger river basin is shown, with an arrow pointing from it to the main detailed map. A legend in the bottom right corner clarifies the symbols: a blue line for Rivers, a red outline for Glacial lakes, a hatched pattern for Glacier extent, and a black outline for AOI\_fishnet\_grid.

Historical maximum extent of the glacial lakes in the North-East Quadrant

Fig. 7 (continued)

# 4 Discussion

The main purpose of this study was to present a methodology to map and track the spatial dynamics of GLs over a large AOI primarily through time series analysis. To achieve this goal, a time series dataset of Landsat imagery was used in the GEE platform to prepare triennial median water spectral indices from December 1987 to December 2020 along with topological indices like slope and hillshade. The dataset used for training the classifier algorithms yielded high-accuracy imageries of GLs. With the limited dataset of Landsat 5 imageries with very few bands, especially of the 1980s and 1990s, the accuracy achieved by the RFC was highly satisfactory. Unlike other contemporary studies [14, 17, 20, 43], many feature variables, namely, AWEI<sub>nsh</sub>, AWEI<sub>sh</sub>, Band Ratio, MNDWI, NDWI<sub>b</sub>, NDWI<sub>g</sub>, WRI, Slope and Hillshade, were considered in this study to encompass all the possible feature extraction for the mapping of the GLs. Median values of the water indices were considered in this study to negate the issues of limited time series images as well as annual and seasonal variations of the image qualities [33, 83].

Amongst the feature variables used as inputs in this study, the slope has been the most important feature in the mapping of the GLs, followed by  $AWEI_{sh}$ ,  $AWEI_{nsh}$ ,  $NDWI_b$  and WRI. The importance of slope in mapping the GLs is mainly due to its low value and homogeneous estimates in the case of GLs as compared to the heterogeneous and higher values estimated from the surrounding complex mountain terrain [34, 84, 85].  $AWEI_{sh}$  outperformed  $AWEI_{nsh}$  in predicting the GLs as  $AWEI_{sh}$  can discriminate shadowed regions, such as those cast by mountains or clouds, from water bodies in high-relief areas. Shadows can mimic water's spectral characteristics, leading to misclassification.  $AWEI_{sh}$  incorporates additional spectral adjustments to suppress shadowed areas that might otherwise be mistaken for water, improving the detection accuracy in mountainous or high-shadow environments [58, 59]. Other water indices contributed less than 8% each in the prediction of GLs.

The correlation analysis of feature variables showed that topographic variables, especially hillshade had a very weak correlation with other feature variables. However, the

Banerjee Discover Geoscience (2025) 3:159 Page 20 of 33

Image /page/20/Figure/1 description: A map titled "HISTORICAL MAXIMUM EXTENT OF THE GLACIAL LAKES IN THE SOUTH-EAST QUADRANT". The map shows a mountainous, topographical region with rivers marked in blue and glacial lakes outlined in red and labeled with numbers. A legend in the bottom left indicates the symbols for Rivers, Glacial lakes, Glacier extent (a hatched pattern), and AOI\_fishnet\_grid. The map includes a scale in kilometers and a north arrow. On the right side, there are two inset maps. The top one is a circular map showing the location of the area within India and near the Himalayas. The bottom inset shows the larger river basin, with an arrow pointing to the section detailed in the main map.

## Historical maximum extent of the glacial lakes in the South-East Quadrant

Fig. 7 (continued)

slope showed a weak negative correlation with water indices, indicating that at a lesser slope, which was true for GLs, the water indices have a higher value. MNDWI and NDWI<sub>b</sub> were strongly correlated, primarily due to their similar density distribution and the use of similar spectral information. The very strong positive correlation between the Band ratio and NDWI<sub>g</sub> was attributed to the use of the same bands in their calculations. The strong bimodal distributions of GL (Class – 1) and non-GL (Class – 0) instances in the case of slope, AWEI<sub>sh</sub> and NDWI<sub>b</sub> have been instrumental in discriminating GL pixels from non-GL pixels in this study.

Certain specific considerations were made while preparing the methodology of this study. For instance, unlike comparatively popular machine learning methods like CNN, which rely on context and patch-based semantic segmentation of the image, pixel-based machine learning, like RFC, was used for two-fold reasons. First, in the case of CNN, for each triennial period, a dataset of unique patch and mask images had to be prepared for prediction. In contrast, RFC, being a pixel-based classifier, had to be provided with pixels that belonged to GLs to prepare the dataset for prediction. Secondly, the computational cost and subjective bias in identifying the GL patches for CNN would have been a trade-off with the predictive capacity of the model while considering 11 observation periods spanning three decades, and three satellite images, namely Landsat 5, 7, and 8. The next consideration of this study was the use of the Unique Lake ID, which is based on a geospatial method called 'selection by location'. The Unique Lake ID helped in tracking the GLs over the 11 observation periods. For this, an innovative method is applied by preparing the maximum extent of GLs. The maximum extent of individual GLs ensured that the GLs of various observation periods were always a proper subset of the maximum extent of individual GLs, tagging each GL with a Unique Lake ID. This method helped in tracking the dynamics of all the individual GL polygons. Finally, the JRC GSW V 1.3 image was used to externally validate the identification of the GLs. The final consideration of this study was to generate the time series dataset to observe the dynamics of individual GL and forecast GL dynamics till the year 2026 using appropriate statistical models. For instance, the rapid growth of the South Lhonak Lake of North

Banerjee Discover Geoscience (2025) 3:159 Page 21 of 33

## Historical maximum extent of the glacial lakes in the South-West Quadrant

Image /page/21/Figure/2 description: A map titled "Historical maximum Extent of the glacial lakes in the South-West Quadrant". The main part of the image is a detailed topographical map of a mountainous region, showing glacier extents with blue hatching, glacial lakes outlined in red, and rivers as blue lines. The map includes latitude and longitude grid lines, with latitude ranging from approximately 27°28'N to 27°44'N and longitude from 88°6'E to 88°26'E. Several peaks are labeled with their elevations, such as "6806 m SINIOLCHU", "5135 m", and "4718 m". A scale bar at the bottom indicates distances in kilometers. In the top left corner, there are two inset maps. The first is a circular map showing the location of the region within India and the Himalayas. An arrow points from this to a second, smaller map of a larger watershed area, with the south-west quadrant highlighted, corresponding to the main map. A legend in the bottom left clarifies the symbols for Rivers, Glacial lakes, and Glacier extent. A north arrow is present in the lower right.

Fig. 7 (continued)

Image /page/21/Figure/4 description: A scatter plot titled "Lake area in terms of elevation". The x-axis represents "Elevation (m)" and ranges from 3000 to 6500. The y-axis represents "Lake area (Sq.km)" and ranges from 0.0 to 1.8. The plot displays numerous magenta circular data points. Most of the points are clustered at the bottom of the graph, below a lake area of 0.4 Sq.km, primarily between elevations of 4000m and 5500m. A horizontal dashed line is drawn at a lake area of 0.4. Several outlier points with larger lake areas are labeled with numbers. For example, point 46 is at an elevation of approximately 5200m with a lake area of about 1.8 Sq.km. Point 9 is near 5150m with an area of about 1.4 Sq.km. Point 83 is near 6200m with an area of about 1.3 Sq.km.

**Fig. 8** Distribution of the glacial lake area against the elevation of the glacial lake. Selected lakes of area more than  $0.4 \, \mathrm{km^2}$  have been identified by their ULID to identify the larger lakes

Banerjee Discover Geoscience (2025) 3:159 Page 22 of 33

Image /page/22/Figure/1 description: A figure titled "Error estimation of area of glacial Lakes (in %)" displays eleven scatter plots arranged in a grid. Each plot corresponds to a specific triennial period, starting from 1987-1990 and ending with 2017-2020. The periods shown are 1987-1990, 1990-1993, 1993-1996, 1996-1999, 1999-2002, 2002-2005, 2005-2008, 2008-2011, 2011-2014, 2014-2017, and 2017-2020. In each plot, the x-axis represents "Lake area (in Sq.Km)" from 0 to 1.5, and the y-axis represents "Error (in %)" from 0 to 40. The plots contain grey data points, a red trend line, and a shaded grey confidence interval. All plots consistently show that the error percentage is high for small lake areas and decreases rapidly as the lake area increases, eventually leveling off at a low error rate for larger lakes.

**Fig. 9** Relative error of area estimation of glacial lakes of various triennial periods. Points in the plots represent the relative error against the lake area, the red curve is the best fitting smooth curve considering error as a function of lake area, and the grey boundary represents the 95% confidence interval of the red curve

Sikkim, as observed in this study (Figs. 5a and 10b-GL~83), led to GLOF on 4 October 2023, causing 46 casualties, more than 77 people reported missing and impacting 88,400 people (https://iee.psu.edu/news/blog/glacier-lake-outburst-floods-loss-life-and-infrast ructure ).

Simultaneous time series analysis of individual GLs of a large AOI is a new type of method. The primary hindrance to this method has been the lack of infrastructure and computational speed required for processing big geodata, such as the Landsat image time series. Manual mapping is not viable for this type of study as it can lead to subjective bias due to poor interpretability of the images, especially in the face of a large database [17, 20, 24, 28, 29, 46]. Since 2010, the power of high-speed cloud-based geocomputation of big geodata has been possible using GEE to perform this type of study [86, 87]. Moreover, the applications of machine learning are rapidly increasing in geosciences due to the affordability of high-performance PCs [88–90]. Like this study, machine learning and its subset deep learning have been intensively used in the last decade to map GLs in varied locations [21, 30, 34]. However, these studies have heavily relied on the high spatial and spectral resolutions of recently launched satellites like Landsat 8 and Sentinel 1 and 2 to map the lakes. In contrast, this study used past images of Landsat 5 and 7. To compensate for the uncertainty related to the dataset generated from past images, multiple datasets of the individual triennial period were prepared specifically for the spectral properties of the satellites that have captured the images in the past. The binding factor of all these datasets was the common minimal GL polygon area that has remained unchanged over the two epochs of observations made by JRC GSW V 1.3. This type of approach is new, as other similar studies rely only on a single training dataset for a single image classification. Unlike other studies [34, 48] that have explored CNN, this study heavily relied on RFC. This was mainly because the instances of GL pixels were

Banerjee Discover Geoscience (2025) 3:159 Page 23 of 33

**Table 4** Performance of timeseries models

| ULID | Trend                                                                        | Performance | statistics              | Model type | Remark  |       |               |                               |
|------|------------------------------------------------------------------------------|-------------|-------------------------|------------|---------|-------|---------------|-------------------------------|
|      |                                                                              | Stationary  | R-squared               | RMSE       | MAPE    | MAE   |               |                               |
|      |                                                                              | R-squared   |                         |            |         |       | _             |                               |
|      |                                                                              | Ideal value |                         |            |         |       |               |                               |
|      |                                                                              | 1           | 1                       | 0          | 0       | 0     |               |                               |
| 9    | Increasing                                                                   | 0.521       | 0.578                   | 0.087      | 6.606   | 0.065 | Brown         |                               |
| 23   | Irregular                                                                    | -0.018      | 0.217                   | 0.01       | 3.26    | 0.007 | Simple        |                               |
| 27   | Increasing                                                                   | 0.822       | 0.713                   | 0.011      | 1.896   | 0.007 | Holt          |                               |
| 33   | Increasing                                                                   | 0.825       | 0.32                    | 0.002      | 19.578  | 0.001 | Holt          |                               |
| 42   | Increasing                                                                   | 0.843       | 0.52                    | 0.002      | 6.993   | 0.002 | Holt          |                               |
| 43   | Increasing                                                                   | 0.869       | 0.697                   | 0.004      | 22.29   | 0.003 | Holt          |                               |
| 45   | Increasing                                                                   | 0.894       | 0.369                   | 0.014      | 31.105  | 0.01  | Holt          |                               |
| 46   | Increasing                                                                   | 0.744       | 0.361                   | 0.04       | 1.836   | 0.029 | Holt          |                               |
| 49   | Increasing                                                                   | 0           | 0.728                   | 0.029      | 2.154   | 0.022 | ARIMA (0,1,0) |                               |
| 70   | Irregular                                                                    | -0.004      | 0.791                   | 0.039      | 17.282  | 0.021 | Brown         |                               |
| 73   | Increasing                                                                   | 0.866       | 0.335                   | 0.024      | 42.608  | 0.017 | Holt          |                               |
| 78   | Decreasing                                                                   | 0.845       | 0.436                   | 0.003      | 6.521   | 0.002 | Holt          |                               |
| 79   | Increasing                                                                   | 0           | 0.364                   | 0.022      | 6.71    | 0.019 | ARIMA (0,1,0) |                               |
| 81   | Increasing                                                                   | 0.824       | 0.828                   | 0.048      | 5.853   | 0.034 | Holt          |                               |
| 83   | Increasing                                                                   | 0.74        | 0.974                   | 0.051      | 5.857   | 0.041 | Brown         | After deletion of a timestamp |
| 86   | Increasing                                                                   | 0.659       | 0.467                   | 0.002      | 13.406  | 0.001 | Holt          |                               |
| 94   | Decreasing                                                                   | 0.881       | 0.395                   | 0.028      | 123.879 | 0.018 | Holt          |                               |
| 101  | Increasing                                                                   | 0.939       | 0.497                   | 0.004      | 17.956  | 0.003 | Holt          |                               |
| 102  | Decreasing                                                                   | 0.812       | 0.588                   | 0.004      | 6.276   | 0.003 | Holt          |                               |
| 122  | Increasing                                                                   | -0.068      | 0.355                   | 0.024      | 151.999 | 0.016 | Brown         |                               |
| 123  | Increasing                                                                   | 0.851       | 0.308                   | 0.002      | 14.701  | 0.002 | Holt          |                               |
| 124  | Decreasing                                                                   | 0.827       | 0.412                   | 0.033      | 38.648  | 0.024 | Holt          |                               |
| 125  | Increasing                                                                   | 0.886       | 0.48                    | 0.007      | 11.02   | 0.005 | Holt          |                               |
| 139  | Increasing                                                                   | 0           | 0.739                   | 0.015      | 24.701  | 0.01  | ARIMA (0,1,0) |                               |
| 142  | Irregular                                                                    | 0.029       | 0.13                    | 0.003      | 2.985   | 0.002 | Simple        |                               |
| 150  | Decreasing                                                                   | -0.125      | 0.465                   | 0.009      | 153.184 | 0.006 | Brown         |                               |
| 156  | Increasing                                                                   | 0.72        | 0.916                   | 0.022      | 14.659  | 0.018 | Holt          |                               |
| 165  | Increasing                                                                   | 0.56        | 0.451                   | 0.024      | 14.118  | 0.019 | Brown         |                               |
| 167  | Decreasing                                                                   | 0.468       | 0.545                   | 0.013      | 62.562  | 0.01  | Brown         | After creating a timestamp    |
| 168  | Decreasing                                                                   | 0.899       | 0.336                   | 0.009      | 140.145 | 0.007 | Holt          | After creating a timestamp    |
| 174  | Increasing                                                                   | 0           | 0.413                   | 0.195      | 138.937 | 0.12  | ARIMA (0,1,0) |                               |
| 175  | Decreasing                                                                   | 0.804       | 0.735                   | 0.015      | 62.607  | 0.012 | Holt          |                               |
| 183  | Decreasing                                                                   | 0.89        | 0.364                   | 0.008      | 5.223   | 0.006 | Holt          |                               |
| 209  | Decreasing                                                                   | 0.798       | 0.487                   | 0.017      | 72.223  | 0.014 | Holt          | After creating a timestamp    |
| 212  | Decreasing                                                                   | -0.074      | 0.46                    | 0.018      | 321.838 | 0.013 | Simple        | After creating a timestamp    |
| 222  | Increasing                                                                   | 0           | 0.667                   | 0.023      | 7.142   | 0.017 | ARIMA (0,1,0) | •                             |
| 227  | Increasing                                                                   | 0           | 0.352                   | 0.008      | 13.318  | 0.006 | ARIMA (0,1,0) |                               |
| 230  | Increasing                                                                   | 0.291       | 0.924                   | 0.029      | 44.406  | 0.024 | Brown         |                               |
| 235  | Increasing                                                                   | -0.05       | 0.665                   | 0.046      | 87.554  | 0.033 | Brown         |                               |
| 282  | Increasing                                                                   | 0.885       | 0.615                   | 0.004      | 3.806   | 0.003 | Holt          |                               |
| 314  | Increasing                                                                   | 0.793       | 0.286                   | 0.006      | 23.567  | 0.004 | Holt          |                               |
| 339  | Increasing                                                                   | 0.901       | 0.32                    | 0.004      | 15.679  | 0.003 | Holt          |                               |
| 340  | Irregular                                                                    | -0.013      | 0.337                   | 0.005      | 16.359  | 0.003 | Simple        |                               |
| 359  | Decreasing                                                                   | -0.174      | 0.32                    | 0.003      | 15.776  | 0.001 | Brown         |                               |
| 360  | Increasing                                                                   | 0.171       | 0.544                   | 0.005      | 24.695  | 0.002 | ARIMA (0,1,0) |                               |
| ULID | Trend Performance statistics Stationary R-squared R-squared Ideal value  1 1 | Performance | statistics              | Model type | Remark  |       |               |                               |
|      |                                                                              | •           | R-squared RMSE MAPE MAE |            |         |       |               |                               |
|      |                                                                              | Ideal value |                         |            |         |       |               |                               |
|      |                                                                              | 0           | 0                       | 0          |         |       |               |                               |
| 383  | Increasing                                                                   | 0.93        | 0.432                   | 0.004      | 4.839   | 0.003 | Holt          |                               |
| 398  | Increasing                                                                   | 0.887       | 0.49                    | 0.004      | 13.956  | 0.003 | Holt          |                               |

Banerjee Discover Geoscience (2025) 3:159 Page 24 of 33

Table 4 (continued)

very limited in contrast to the many non-GL pixels available in the AOI. RFC works very well in these types of skewed distributed training datasets [70]. ANN underperformed in this study as compared to RFC, as the former relies on a balanced set of GL and non-GL instances for effective predictions. In fact, like this study, RFC has been successfully applied in the mapping of GLs [30, 91].

A total of 492 GLs were identified in this study. However, 406 GLs were considered for detailed analysis as they conformed with the JRC GSW V1.3 map. These GLs were visually validated by overlaying on historic Landsat images, Sentinel 2 A and Google Earth high-resolution images. In contrast, 320 GLs [27], 143 GLs [92], 472 GLs [17], 463 GLs [46], and 419 GLs [18] were identified in Sikkim Himalaya. The ambiguity in the identification of the GLs of Sikkim Himalaya can be attributed to the variations in the temporal and spectral resolutions of the imagery databases used. Also, the variation in the methodologies used to identify and validate the findings should be considered. Imagebased decadal dynamics of selected GLs such as GL-5, GL-83, GL-174, and GL-221 have been reported in earlier work [46]. The dynamics of selected GLs at a lower temporal resolution than this study have also been demonstrated [17]. In contrast to these previous studies, the present work provides a much higher temporal resolution and spatial coverage for tracking the GL dynamics of the AOI. Being explorative, this study is confined to relatively small AOI and triennial periods. However, this methodology can be easily amended to cover large areas like the trans-Himalayan region and at a much higher temporal resolution to capture seasonal variations of the GL area over the past several decades. By increasing the GL instances and greater automation of the methodology, near real-time mappings of the GLs will be possible to anticipate their future dynamics using time series forecasting.

The major issue faced in this study was working with low spatial and spectral resolution imagery. Moreover, for the past datasets, especially of the 1980s and 1990s, external validations by declassified high-resolution satellite imagery can further substantiate the classification results. However, visual validation of the lake area was made with FCC and TCC images derived from the Landsat time series data, as well as Sentinel 2A images. The water spectral indices used in this study showed varied degrees of strong to very strong correlation, indicating a possible variable redundancy. This issue can be effectively addressed by manually removing the weak input variables or performing principal component analysis. The relative error of area estimation showed an error range of 1% to 43% over all the triennial periods, with the majority of errors confined to small glacial lakes ranging from 0.01 km² to 0.02 km². There errores can be reduced by considering higher resolution images, like Linear Imaging Self-Scanning (LISS) satellite images, such as LISS-4 and Sentinel 2A images. The size of a GL depends on geological, geomorphological, hydrological, climatological, and topographical factors. In contrast, the

Banerjee Discover Geoscience (2025) 3:159 Page 25 of 33

Image /page/25/Figure/1 description: A figure titled "Increasing glacial lakes" displays ten individual time-series plots arranged in a 5x2 grid. Each plot shows the change in area of a specific glacial lake over time. The x-axis for each plot is labeled "Time (in triennial period)" and ranges from 1990 to 2026. The y-axis is labeled "Area (in Square Km)" with varying scales for each plot. Within each plot, red dots represent the time series data, a solid black line represents the forecast, and a shaded grey ribbon represents the confidence limits. The plots are labeled as follows, from top to bottom, left to right: GL.8, GL.9, GL.27, GL.33, GL.42, GL.43, GL.45, GL.46, GL.49, and GL.73. All ten plots show a general increasing trend in the area of the glacial lakes over the time period shown. A caption at the bottom begins with "Fig. 10. a Time series (Red dots), forecast (Black line) and confidence limits (Grey ribbon) of selected GLs..."

**Fig. 10 a** Time series (Red dots), forecast (Black line) and confidence limits (Grey ribbon) of selected GLs (ULID is mentioned as the plot title) that showed increasing trends. A 95% confidence interval is used. **b** Time series (Red dots), forecast (Black line) and confidence limits (Grey ribbon) of selected GLs (ULID is mentioned as the plot title) that showed increasing trends. A 95% confidence interval is used. **c** Time series (Red dots), forecast (Black line) and confidence limits (Grey ribbon) of selected GLs (ULID is mentioned as the plot title) that showed increasing trends. A 95% confidence interval is used. **d** Time series (Red dots), forecast (Black line) and confidence limits (Grey ribbon) of selected GLs (ULID is mentioned as the plot title) that showed increasing trends. A 95% confidence interval is used. **e** Time series (Red dots), forecast (Black line) and confidence limits (Grey ribbon) of selected GLs (ULID is mentioned as the plot title) that showed irregular trends. A 95% confidence interval is used. **f** Time series (Red dots), forecast (Black line) and confidence limits (Grey ribbon) of selected GLs (ULID is mentioned as the plot title) that showed decreasing trends. A 95% confidence interval is used. **g** Time series (Red dots), forecast (Black line) and confidence limits (Grey ribbon) of selected GLs (ULID is mentioned as the plot title) that showed decreasing trends. A 95% confidence interval is used. **g** Time series (Red dots), forecast (Black line) and confidence limits (Grey ribbon) of selected GLs (ULID is mentioned as the plot title) that showed decreasing trends. A 95% confidence interval is used.

Banerjee Discover Geoscience (2025) 3:159 Page 26 of 33

Image /page/26/Figure/1 description: A figure titled "Increasing glacial lakes", labeled as "Fig. 10 (continued)", which displays ten individual scatter plots arranged in a 5x2 grid. Each plot shows the change in the area of a specific glacial lake over time. The x-axis for all plots is labeled "Time (in triennial period)" and ranges from 1990 to 2026. The y-axis is labeled "Area (in Square Km)", with the scale varying for each plot. Each plot contains red circular data points, a solid black trend line, and a shaded gray confidence interval. The plots are individually titled with identifiers: GL.79, GL.81, GL.83, GL.86, GL.101, GL.122, GL.123, GL.125, GL.139, and GL.156. Generally, all plots show an increasing trend in the area of the glacial lakes over the specified period, though the rate of increase and data variability differ among them. For example, GL.83 shows a strong, steady linear increase, while GL.122 shows a period of relative stability followed by a sharp increase after 2017.

Fig. 10 (continued)

prediction of the size of the GLs in this study solely depended on the past size of the GL. Therefore, the methodology needs further incorporation of these factors. The forecast made by the methodology presented here must be verified and backed by expertise from such fields. However, the forecasts made by the methodology presented here can act as a red flag for an early warning system. Furthermore, this study used JRC GSW V 1.3 as the external source for validating the predictions made by RFC. Thereby, the errors in the prediction of JRC GSW V 1.3 automatically propagate into this study.

To date, most likely no methodology has been developed to perform simultaneous time series analysis of individual GLs of a large AOI. This study is the first step to effectively address this research gap. This methodology can be further extended by

Banerjee Discover Geoscience (2025) 3:159 Page 27 of 33

Image /page/27/Figure/1 description: A figure titled "Increasing glacial lakes" displaying ten individual line graphs arranged in a 5x2 grid. Each graph shows the change in the area of a specific glacial lake over time. The x-axis for all graphs is labeled "Time (in triennial period)" and ranges from 1990 to 2026. The y-axis is labeled "Area (in Square Km)" and has a different scale for each graph. Each plot contains red dots representing data points, a solid black line showing the trend, and a grey shaded area representing a confidence interval. The ten graphs are labeled as follows: GL.165, GL.174, GL.222, GL.227, GL.230, GL.235, GL.282, GL.314, GL.339, and GL.360. Generally, all graphs show an increasing trend in the area of the glacial lakes over the specified time period, though with varying degrees of fluctuation and rates of increase. At the bottom left, there is a caption that reads "Fig. 10. (continued)".

Fig. 10 (continued)

considering climate change as the cause of GL dynamics. This can be achieved firstly by closely monitoring the dynamics of GLs at regional and global scales using high-resolution imagery. The time series data prepared from such monitoring can be used as the dependent variable. Atmospheric temperature, precipitation, glacial dynamics, composition and thickness of the glacial or moraine dams, and topography can serve as the independent variables. These inputs can then be applied in deep learning based time series models such as Long Short-Term Memory networks and multiscale geographically weighted regression to analyze changes over time. This type of state-of-the-art forecast model will help in understanding the triggering factors of events like GLOF, causative factors of an increase in GL area, and geographic factors behind differential growth of

Banerjee Discover Geoscience (2025) 3:159 Page 28 of 33

Image /page/28/Figure/1 description: A figure titled 'Increasing glacial lakes' containing two scatter plots side-by-side, labeled 'GL.383' and 'GL.398'. Both plots show the 'Area (in Square Km)' on the y-axis against 'Time (in triennial period)' on the x-axis, which ranges from 1990 to 2026. Each plot displays red circular data points, a black linear regression line indicating an increasing trend, and a gray shaded confidence interval around the line. For plot GL.383, the area ranges from approximately 0.04 to 0.06 square kilometers. For plot GL.398, the area ranges from approximately 0.01 to 0.04 square kilometers. Both plots illustrate a general increase in the area of the respective glacial lakes over the specified time period.

Image /page/28/Figure/2 description: A figure titled "Irregular glacial lakes" containing four line graphs arranged in a 2x2 grid. Each graph plots the area of a specific glacial lake over time. The x-axis for all graphs is labeled "Time (in triennial period)" and ranges from 1990 to 2026. The y-axis is labeled "Area (in Square Km)", with varying scales for each graph. Each plot includes red circular data points, a solid black trend line, and a shaded gray confidence band.

The top-left graph, labeled "GL.23", shows the area fluctuating between approximately 0.18 and 0.24 Square Km. The trend line dips around 2005 before rising again.

The top-right graph, labeled "GL.70", shows a wide range of area from 0.0 to 0.4 Square Km. The trend peaks around 1999, drops sharply to a low around 2008, and then gradually increases.

The bottom-left graph, labeled "GL.142", shows the area mostly varying between 0.07 and 0.08 Square Km, with a generally increasing trend after a slight dip around 1999.

The bottom-right graph, labeled "GL.340", shows the area ranging from about 0.01 to 0.05 Square Km. The trend line decreases to a minimum around 2002 and then increases, peaking around 2011.

Fig. 10 (continued)

GLs within an AOI. Furthermore, with the availability of cloud-free high-resolution SAR time series data from Sentinel 1 A, a CNN can be trained to monitor the growth of GLs in GLOF hazard-prone areas.

# 5 Conclusion

A methodology is presented in this study to combine the GEE-based geocomputation of Landsat time series data, RFC-based image classification and time series analysis for glacial lake area dynamics and forecasts. This methodology can expedite an accurate and large-scale study of glacial lakes in a short time. Thereby, this methodology has a substantial scope of applications in identifying rapidly growing glacial lakes of a large geographic area. The mapping process, especially of past scenarios, need external validations using high-resolution imagery. The methodology presented here can be further automated and use near-real-time Landsat and Sentinel time series data with a higher spatial, temporal, and spectral resolution to predict the future dynamics of GLs of interest. With the increase in GL instances of training, RFC can be replaced by deep learning algorithms. The time series database of GLs generated by this methodology can be coupled with Long Short-Term Memory network (LSTM) deep learning models and multiscale geographically weighted regression to identify the temporal trends of the explanatory variables of GLOF and climate change-induced dynamics of GLs. This methodology is also applicable to C-band Synthetic Aperture Radar Ground Range Detected time series imageries (Sentinel-1 SAR GRD) available since 2014. A convolutional neural network Banerjee Discover Geoscience (2025) 3:159 Page 29 of 33

Image /page/29/Figure/1 description: A figure titled "Decreasing glacial lakes" showing ten scatter plots arranged in a 5x2 grid. The figure is labeled "Fig. 10. (continued)" at the bottom. Each plot tracks the area of a specific glacial lake over time. The x-axis for all plots is "Time (in triennial period)" from 1990 to 2026. The y-axis is "Area (in Square Km)" with varying scales for each plot. The data is shown with red dots, a black trend line, and a grey shaded confidence interval. The plots are titled GL.78, GL.94, GL.102, GL.124, GL.150, GL.167, GL.168, GL.175, GL.183, and GL.209. Most plots show a clear decreasing trend in area over time. However, plots GL.150 and GL.167 show more complex, non-linear trends, with periods of both increase and decrease.

Fig. 10 (continued)

can be trained using SAR images to identify the GLs irrespective of the cloud cover. The study can facilitate policy intervention towards GLOF warning, mitigation and building evidence for climate action.

Banerjee Discover Geoscience (2025) 3:159 Page 30 of 33

Image /page/30/Figure/1 description: A figure titled "Decreasing glacial lakes" displays two line graphs side-by-side, labeled "GL.212" and "GL.359". Both graphs plot "Area (in Square Km)" on the y-axis against "Time (in triennial period)" on the x-axis, which ranges from 1990 to 2026. Each graph contains red circular data points, a solid black trend line, and a gray shaded confidence interval. In the left graph, "GL.212", the area fluctuates between approximately 0.03 and 0.07 square kilometers from 1990 to 2008, after which it shows a steep decline to near zero by 2020. The y-axis for this graph ranges from 0.00 to over 0.09. In the right graph, "GL.359", the area remains relatively stable, hovering around 0.02 square kilometers from 1990 to 2017, before showing a sharp decrease, dropping below zero by 2026. The y-axis for this graph ranges from -0.02 to 0.03.

Fig. 10 (continued)

# **Supplementary Information**

The online version contains supplementary material available at https://doi.org/10.1007/s44288-025-00280-w.

Supplementary Material 1

## Acknowledgements

I would like to thank Dr. Rayees Ahmed, Department of Central University of Kashmir, India, and Prof. Chandrashekhar Bhuiyan, Department of Civil Engineering, SMIT, Sikkim, India for their valuable suggestions and internal review of the manuscript.

## **Author contributions**

Polash Banerjee is the sole author of this research work.

## **Funding**

None.

## Data availability

The datasets generated during and/or analyzed during the current study are available from the corresponding author on reasonable request.

## **Declarations**

### Ethics approval and consent to participate

This study did not involve human participants or animals, and therefore formal ethical approval was not required. Not applicable. No human participants were involved in this study.

### Consent for publication

Not applicable.

### **Competing interests**

The authors declare no competing interests.

Received: 28 September 2024 / Accepted: 3 October 2025

Published online: 08 October 2025

