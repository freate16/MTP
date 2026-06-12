
# Analyzing the triggering factors of glacial lake outburst floods with SAR and optical images: a case study in Jinweng Co, Tibet, China

Abstract On June 25, 2020, Jinweng Co in Yiga, Tibet, experienced an outburst flood that resulted in catastrophic damage to farmland and roads. The complex causal factors for glacial lake outburst flooding (GLOF) are not fully understood. This paper provides a systematic analysis of the contributing factors leading to the GLOF disaster in terms of meteorological triggering, glacial activity, lake expansion, landslide, and glacial collapse. The analysis is based on multi-source remote sensing approaches. Pixel offset tracking of Sentinel-1 images shows changes in the glacier flow velocity from 2017 to 2020. Sentinel-2 and Landsat-8 images and inventory data have revealed the expansion of the lake since 1998. The satellite precipitation measurements revealed that the highest daily rainfall in recent years occurred approximately 4 days before the GLOF. Time series synthetic aperture radar (SAR) backscattering images and interferograms suggest that a landslide had occurred from the western lateral moraine into the lake. Additionally, SAR images suggest possible ice collapse from the glacier tongue into the lake. The causal mechanism for the June 2020 GLOF event was likely the dam failure triggered by heavy rainfall and combined with landslides and ice collapses. Our research can provide a reference to identify and mitigate glacial lake outburst disasters in mountainous regions based on satellite optical and radar images.

**Keywords** Glacial lake outburst flood (GLOF)  $\cdot$  Glacier three-dimensional flow velocity  $\cdot$  Outburst mechanism  $\cdot$  Multi-source remote sensing

# Introduction

Glacial lake outburst flood (GLOF) is a sudden and rapid downstream discharge of a significant volume of water. Previous studies (Evans and Clague 1994; Nadim et al. 2006; Yamada 1998; Emmer and Cochachin 2013a, Emmer and Vilímek 2013b, Emmer 2017) identified two groups of factors that induce lake outbursts. The first set consists of dynamic causes, such as slope movement into the lake, earthquakes, heavy rainfall, or snowmelt. The second set includes long-term factors such as the melting of buried ice, hydrostatic pressure changes, and other long-term degradation processes. GLOFs often have catastrophic consequences for communities and infrastructure located downstream. Glacier recede and thinning in high mountains generate the formation and development of glacial lakes (Richardson and Reynolds 2000; Haeberli et al. 2001, 2002). Monitoring-related glacial movement and changes in glacier lakes and the surroundings help us better understand how the ice mass propagates in space, how their movements evolve over time, and how external factors control their

behaviors (Satyabala 2016; Ma et al. 2020). Owing to the inherently challenging landscapes, comprehensive remote sensing methods are needed to study and monitor GLOFs.

The outburst of Jinweng Co ("Co" refers to "lake" in Tibetan) in Yiga village, Tibet, caused intense and sudden flooding on June 25, 2020. This grave disaster inundated and destroyed 382.43 km<sup>2</sup> of farmland, washed away over 43.9 km of roads, and flooded 45% of the Yiga Scenic Area project (Wang et al. 2020a). Over 2,000 glacial lakes have been detected across the Himalayas (Fujita et al. 2013), so the potential for further hazards is significant. Moreover, the eastern Himalayas are considered as one of the most severely deformed areas due to intense tectonic activities and earthquakes. The melting, thinning, and receding of temperate glaciers leads to lake expansion and is related to slope movement. Extreme precipitation plays an important role in triggering slope movement, while an increase in temperature can result in increased melting, permafrost degradation, and rockfalls (Hu et al. 2019a; Wang et al. 2020a, b; Lu and Kim 2021).

Many studies have documented that snow/ice accumulation/ avalanches and landslides significantly impact outburst flooding (Allen et al. 2016; Clague and Evans 2000; O'Connor et al. 2001; Worni et al. 2012). The Jinweng Co disaster originated from a parent glacier and included an outburst of the proglacial lake. The real-time monitoring and analysis conducted shortly after the disaster suggested that the intensification of climate warming and cryosphere instability stimulated the occurrence of the GLOF (Wang et al. 2020a). However, the mechanism and triggering factors of the Jinweng Co GLOF process chain should be further investigated. The evolution of the glacier, the proglacial lake, and the surrounding area prior to the GLOF event has not yet been analyzed. A complete assessment of triggering factors (glacier activity, precipitation, air temperature, slope movement, and ice collapse) is still lacking.

Thus, this study addresses the following key question: Can we identify precursory characteristics of the 2020 GLOF at Jinweng Co in eastern Tibet? To address this question, we aimed to understand the movement of glaciers and the change in moraine-dammed lakes, as well as temperature and precipitation records in the study area. We used spaceborne C-band Sentinel-1 data to retrieve the time series two-dimensional (2D) displacement and three-dimensional (3D) glacier flow velocity. The interpretation was then augmented with Sentinel-2 and Landsat-8 optical images and inventory data to construct changes to the area of the lake before and after the event. Meteorological observations were examined to understand the climatic properties of the region. Additionally, we analyzed SAR intensity images and interferograms to infer the

Published online: 30 January 2022 Landslides

glacier tongue changes and identify landslide activity. This led to further clarification regarding the outburst triggering mechanisms.

# Study area

The study region is within the Tanggula Mountains, which are home to some of the highest mountains in the world. It is also the most humid region of the southeastern Qinghai-Tibet Plateau (QTP) (Fig. 1). The topography of the study area is affected by the compression of the Indian Ocean-Eurasian continental plate, uplift of the QTP, strong faulting activity, and fluvial incision. The climate is influenced by both East Asian and Indian monsoons (Ding 2013). Precipitation during the rainy season is mainly caused by airflow from the southwest, west, and northwest (Li et al. 2009). The temperate glaciers in this study area are small and primarily oriented in the north-south direction with large ice caps (You and Yang 2013). Consequently, the area is subject to glacial hazards such as glacier debris flows, GLOFs, and glacier surges, which are further increased by climate change (Allen et al. 2016; Bazai et al. 2021; Chiarle et al. 2007; Wang et al. 2020a, b; Kääb et al. 2021). Generally, a glacial lake outburst results from external forces such as ice or rock fall, snow avalanches, landslides, rainstorms, glacier surges, rapid snow melting, and/or internal processes such as the ablation of buried ice in moraines and the release of lake water inside the ice body (Wang et al. 2020a).

Jinweng Co (30.356 N°, 93.631 ° E) is a proglacial moraine-dammed lake (Fig. 2) and is also the largest glacial lake within the Nidou Zangbo basin ("Zangbo" refers to rivers in Tibetan) (Zheng et al. 2021). The lake is oriented in a north–south direction and is characterized by steep slopes and lateral moraines. The slopes are approximately 40°, and the average elevation of lateral moraines is more than 100 m above the lake level (Zheng et al. 2021). As shown in Fig. 2d, the length is approximately 1.8 km, and its width near the glacier tongue is 0.24 km, while the width near the dam was 0.33 km before the lake outburst. The parent glacier tongue enters

**Fig. 1** Overview of the study area showing Jinweng Co and coverage of multiple datasets outlined in purple (Sentinel-2), orange (Landsat-8), blue (Ascending Sentinel-1), and red (Descending Sentinel-1)

the lake after passing through a steep ice cliff approximately 350 m long with an average slope of approximately 35 ° (Fig. 2). The parent glacier is a temperate glacier with a mean annual temperature of approximately 0 °C. The snow basin at high altitude serves as the accumulation zone, while the tongue is the ablation zone. This study investigates the triggering factors for the June 2020 GLOF event in Jinweng Co by analyzing the movement of the parent glaciers and changes to the lake and surroundings using multi-satellite remote sensing datasets.

# Data and methods

The multi-track C-band Sentinel-1 synthetic aperture radar (SAR) data and Sentinel-2 and Landsat-8 optical images were used to investigate the triggering factors of the 2020 GLOF event (Fig. 3). The Copernicus Sentinel-1A/B and Sentinel-2 Level-1C images for this study are available free of cost from the Sentinel Scientific Data Hub of the European Space Agency. Multi-temporal Landsat images were obtained from the Geospatial Data Cloud (http://www.gscloud.cn/). In addition, daily and monthly precipitation measurements from the satellite Global Precipitation Measurement (GPM) (Skofronick 2017) were obtained to analyze the meteorological factors. In addition, inventory data from 1975 to 2018 were obtained from the National Tibetan Plateau Data Center (TPDC) to evaluate temporal variations in Jinweng Co (https://data.tpdc.ac.cn) (Wang 2015).

## **Satellite datasets**

Ninety-eight interferometric wide (IW) swath mode ascending Sentinel-1 and eighty-two descending Sentinel-1 images from March 2017 through October 2020 were acquired. The pixel spacing in the ground range and azimuth direction was ~4 m and ~14 m, respectively. Sentinel-2 data with multi-spectral instrument (MSI) images were acquired on May 1 and July 27, 2020, and provided a spatial resolution of 10 m. Landsat-8 MSI images from 2018 to 2019 with a spatial resolution

Image /page/1/Figure/11 description: A satellite map of a mountainous region, with longitude ranging from 93°25' to 93°55' and latitude from 30°15' to 30°35'. The map displays snow-covered mountains, glaciers, and lakes. Several colored outlines indicate the coverage areas of different satellites: a blue polygon for 'Ascending Sentinel-1', a red polygon for 'Descending Sentinel-1', an orange rectangle for 'Landsat-8', and a purple rectangle for 'Sentinel-2'. A legend in the bottom-left corner defines symbols for Glacier, Lake, and Main city. Key locations marked include the main city 'Yiga' and the lake 'Jinweng Co'. A blue arrow indicates the 'Flood direction' from west to east. A scale bar in the bottom-right shows a scale of 0 to 6 km.

Fig. 2 Overview of Jinweng Co and its parent glacier. a An overall view of Jinweng Co and surroundings. **b** The parent glacier before the GLOF event. **c** The crevassed glacier tongue terminated in Jinweng Co. d Morphological parameters of Jinweng Co. e The eastern lateral moraine and steep slopes. f The landslide zone at the western lateral moraine. **g** The parent glacier after the GLOF event. Photos: Q. Quying Source: Guoxiong Zheng (used with permission)

Image /page/2/Figure/1 description: A collage of seven images, labeled (a) through (g), showing various aerial and landscape views of a glacial environment. Each image includes a compass rose indicating the direction of North. 

Image (a) is a wide aerial view of a valley with snow-capped mountains. A glacier at the far end feeds into a lake labeled "Jinweng Co". A dashed white line with an arrow indicates the "Flow direction" down the valley.

Image (b) is a top-down aerial view of a mountainous, snow-covered landscape partially obscured by clouds.

Image (c) shows a glacier terminating in a milky green proglacial lake, with steep, rocky mountain slopes surrounding it.

Image (d) provides a view of the glacial lake with its dimensions annotated: 1.8 km in length, 0.33 km in width at the far end, and 0.24 km in width at the near end.

Image (e) is a similar view to (d), with a dashed white line highlighting the "Lateral moraine" along the side of the lake.

Image (f) shows the same lake and mountains, with a red dashed line and text identifying a "Landslide zone" on the slope adjacent to the lake. There is snow in the foreground.

Image (g) is another high-altitude aerial view looking down on a glacier and surrounding mountains, with some cloud cover.

of 30 m were added to derive the temporal changes of Jinweng Co. Information on the Sentinel-1/2 and Landsat data are listed in Table 1, and the data coverages are shown in boxes in Fig. 1.

## Mapping slope movement with SAR intensity images and interferograms

SAR intensity images can be used to detect landscape changes due to their sensitivity to terrain slope, surface roughness, and dielectric constant (e.g., Lu and Meyer 2002; Kim et al. 2017; Zribi and Dechambre 2017). Multi-temporal SAR backscattering intensity images were used in this study to infer changes in glaciers, lakes, and surroundings before the lake outburst event. Interferometric synthetic aperture radar (InSAR) can map surface deformation in the spatial–temporal view, which is a direct manifestation of slope movement (Hu et al. 2019a; Lu and Meyer 2002; Lu et al. 2003; Lu and Kim 2021).

## Change detection with optical images

The interpretation of optical images is commonly employed to support GLOF mapping and inventory (Strozzi et al. 2010). There are countless glaciers in this study area, which induce enormous glacial lakes as glacier recedes. The Sentinel-2 and Landsat-8 images

allow us to recognize geomorphological features related to ice mass movements, such as crevasses, debris flows, and outburst flooding. For instance, a glacial lake may have green patterns with fine texture in one optical image, and after the glacial lake outbursts or shrinks, its edge will form a gray-white submerged zone with obvious breaches and colluvial deposits. Using multi-temporal images, we can interpret the changes in glacial lakes and analyze the possibility of their collapse.

## Offset tracking method

We carried out the offset tracking procedure implemented by GAMMA software to estimate the two-dimensional displacement (Wegmuller et al. 1998; Werner and Wegmuller 2000; Gomez et al. 2019). Offset tracking includes intensity tracking and speckle tracking based on maximizing the cross-correlation of SAR image patches (e.g., Strozzi et al. 2002; Pritchard et al. 2005) to derive glacier displacement for pairs of images acquired at different times. The Shuttle Radar Topography Mission (SRTM) digital elevation model (DEM) was used to assist the co-registration of the SAR images to minimize geometric artifacts in offset-tracking displacements due to high topography (Kobayashi et al. 2009; Liu et al. 2020). A template of  $64 \times 64$  and  $4 \times 1$  was adopted in this study. Thresholds of amplitude correlation range between 0.2 and 0.4.

Table.1 Basic parameters of the SAR and optical datasets used in this study

| Data                            | Sentinel-1            |                       | Sentinel-2            | Landsat-8             |
|---------------------------------|-----------------------|-----------------------|-----------------------|-----------------------|
| Pixel Spacing (azimuth × range) | 14 m × 4 m            |                       | 10 m                  | 30 m                  |
| Number of SAR images            | 98(ascending)         | 82(descending)        | 2                     | 2                     |
| Acquisition period              | 2017/03/21-2020/10/31 | 2017/03/16-2020/10/26 | 2020/05/01-2020/07/27 | 2018/06/06-2019/06/25 |

**Fig. 3** Flow chart of remote sensing methods used in this study

Image /page/3/Figure/2 description: A flowchart titled 'Recent Landslides' illustrating a process for analyzing geological data from three different sources. The flowchart is organized into three parallel columns, each starting with a different data input and leading to a specific output. The first column starts with 'External DEM' (Digital Elevation Model), represented by a colorful topographic image. This data goes through 'Offset tracking', 'Stacking', and '3-D inversion' to produce 'Derivation of 3D annual flow velocity', shown as a 3D map with red and yellow areas. The middle column begins with 'Ascending and Descending SAR images', depicted as stacks of grayscale images. This data undergoes 'Co-registration' to create 'Original interferograms', which are then processed through 'Interferograms filtering' to result in 'Deformation interferograms', illustrated by a colorful, noisy-textured image. The third column uses 'Optical images', shown as a stack of color images, as input. This path involves 'Change detection', leading to 'Intensity change' (shown as a stack of grayscale images), and finally results in 'Optical interpretation', which is represented by two side-by-side maps showing changes in a landscape, possibly a glacier.

## Pixel offset tracking small baseline subsets (PO-SBAS)

Pixel offset (PO) tracking small baseline subsets (SBAS) (PO-SBAS) follows the same motivation as the SBAS-InSAR technique. A sequence of small baseline SAR image pairs that have been previously co-registered with respect to a common reference image was obtained as a starting point (Sansosti et al. 2006; Casu et al. 2011). Subsequently, instead of the phase difference of the selected SAR images, we used their intensities to calculate the pixel offset for both the line-of-sight (LOS) and azimuth directions. Then, the singular value decomposition (SVD) inversion method was applied for the estimated relative LOS and azimuth offsets to generate the corresponding offset-based deformation time series (Sansosti et al. 2006; Casu et al. 2011).

## **Derivation of 3D Glacier velocity**

To retrieve the 3D glacier flow velocity from ascending and descending SAR images, we first obtained displacement measurements in the azimuth and LOS directions based on small baseline image pairs from both descending and ascending tracks.

The 3D velocity field can be obtained from velocity measurements in four distinct directions (Li et al. 2018; Yang et al. 2020):

$$\left\{ \begin{array}{l} V_{LOS}^{i} = -V_{U}cos\:\theta^{i} + \bullet V_{E}sin(\alpha^{i} - 3\pi/2)sin\:\theta^{i} + V_{N}cos(\alpha^{i} - 3\pi/2)sin\:\theta^{i} \\ V_{AZ}^{i} = -V_{E}cos(\alpha^{i} - 3\pi/2) + V_{N}sin(\alpha^{i} - 3\pi/2) \end{array} \right.$$

where i stands for the orbit direction (A indicates the ascending track, and D indicates the descending track),  $\theta$  is the incidence

angle, and  $\alpha$  is the azimuth angle. E, N, and V refer to the east, north, and vertical directions, respectively. The matrix form is as follows:

$$BX = V (2)$$

 $X = \begin{bmatrix} V^{\text{U}} & V^{\text{E}} & V^{\text{N}} \end{bmatrix}^{\text{T}}$ ;  $L = \begin{bmatrix} V_{\text{LOS}}^{\text{A}} & V_{\text{AZ}}^{\text{A}} & V_{\text{LOS}}^{\text{D}} & V_{\text{AZ}}^{\text{D}} \end{bmatrix}^{\text{T}}$ ; and B is a design matrix composed of imaging geometry parameters.

# Results

## Changes in glacier velocity

In this study, the 2D and 3D glacial movements of Jinweng Co from 2017 to 2020 were derived (Fig. 4). The 3D glacier flow velocity during this period is shown in Fig. 4a. The vector arrows indicate the horizontal velocity, whereas the color shows the vertical velocity. In the horizontal direction, the north directed velocity mainly appeared in the glacier trunk of Jinweng Co, with a mean flow velocity of up to 200 m/year. In the vertical direction, the parent glacier moved downward at a velocity of 40 m/year. Owing to sparse acquisitions from descending Sentinel-1, we only obtained the long time series displacement from the ascending track to show the temporal variation (Fig. 4b). As shown in Fig. 4b, P1 was located at the glacier tongue near the lake. The mass transport is evident in the azimuth direction (approximately in the northern direction), as seen in the cumulative displacement of up to 18.4 m. Interestingly, the total displacement during the 2019-2020 cycle (October 2019 to June 2020) at the lower part of the glacier (close to the proglacial lake) is much larger than that observed in the previous years (Fig. 4b).

Image /page/4/Figure/0 description: The image contains two plots, labeled (a) and (b).

Plot (a) is a 3D surface plot illustrating velocity in a geographical area. The surface is colored according to a 'Vertical velocity (m/year)' scale, which ranges from -40 (blue) to 40 (red). The plot also displays black arrows indicating 'Horizontal velocity (m/year)', with a scale arrow representing 200 m/year. A location on the map is labeled 'Jinweng Co'. The x-axis ranges from approximately 93.64 to 93.665, and the y-axis ranges from approximately 30.325 to 30.365. A compass indicates the direction of North.

Plot (b) is a scatter plot showing 'Displacement (m)' on the y-axis versus 'Date (yyyy/m/d)' on the x-axis. The time period spans from 2017/3/1 to 2020/9/1. There are two data series: 'Azimuth', represented by red circles, and 'LOS', represented by blue triangles. The 'Azimuth' displacement shows a steady increase from about 2 m to over 17 m. An event labeled 'Outburst' is marked on the 'Azimuth' data around mid-2020. The 'LOS' displacement remains much lower, fluctuating between 0 m and approximately 3 m over the same period. The y-axis for displacement ranges from 0 to 20 m.

Fig. 4 a 3D glacier flows velocity during 2017–2020. The color indicates vertical velocities, and the arrow indicates horizontal velocities. **b** 2D time series displacement for P1 from the ascending track. The location of P1 is shown in a

## **Changes to Jinweng Co**

To investigate the historical evolution of Jinweng Co, we analyzed its extent of variation and frontal recede using the inventory data from TPDC and by interpreting optical images. Figure 5 shows the temporal variations in Jinweng Co from 1998 to 2020. By superimposing the lake boundaries in the image of 2015 (Fig. 5a), we clearly see that the lake expanded upstream, and the glacier tongue receded. From 1998 to 2020, the proglacial lake expanded dramatically at a mean rate of 21.73 m²/year, and the glacier receded at a mean rate of 0.13 m/year (Fig. 5b).

To better understand the changes to Jinweng Co before and after the catastrophic GLOF in June 2020, we interpreted four summertime optical images, including Sentinel-2 images and Landsat images, and analyzed the variations to the boundary of Jinweng Co, as shown in Fig. 6. The lake area experienced an increasing trend from 2018 to 2020. It showed 0.52 km² on June 6, 2018; 0.55 km² on June 25, 2019; and then 0.57 km² on May 1, 2020. After the GLOF event in June 2020, the lake area decreased to 0.32 km², as reflected in the July 2020 image. This resulted in a massive (~0.25² km) downstream water flow from the lake dam (Fig. 6d).

Image /page/4/Figure/5 description: A two-part figure, labeled (a) and (b), illustrating the changes in a glacial lake over time. Part (a) is a satellite image showing the expansion of a lake between 1998 and 2020. The image is marked with latitude and longitude coordinates (30°21' to 30°22' N, 93°37' to 93°38' E). A legend titled 'Acquisition Data (yyyy/mm/dd)' shows colored outlines for the lake's extent on different dates: 1998/10/19 (light blue), 2001/10/21 (green), 2011/11/10 (yellow), 2015/11/15 (red outline), 2018/10/15 (darker red outline), 2019/06/25 (pink outline), and 2020/05/01 (purple outline). An inset map shows a wider view of the lake dated 2020/7/27. Part (b) is a scatter plot showing the change in lake area and retreat distance over time, from 1998 to 2020. The x-axis represents the date. The left y-axis represents 'Lake area (km²)' and the right y-axis represents 'Retreat distance (m)'. There are two data series plotted. Red squares represent the lake area, which increases from about 0.4 km² to nearly 0.6 km². The linear fit for this data has a slope of 21.73 m²/year. Green circles represent the retreat distance, which increases from about 0.5 m to 1.2 m. The linear fit for this data has a slope of 0.13 m/year. Both linear fits are shown with their 95% confidence bands. The legend clarifies the symbols: red squares for 'Lake area (km²)', green circles for 'Retreat distance (km)', and lines and shaded areas for the linear fits and confidence bands.

**Fig. 5** Temporal evolution of the Jinweng Co during 1998–2020. **a** Lake boundaries derived from inventory data (1998, 2001, 2011, 2015) and interpretation of Landsat-8/Sentinel-2 images (2018, 2019, 2020); the inset map shows the lake boundary after the collapse. **b** Time series of the lake areas and glacier recede from 1998 to 2020. Red squares are measurements of the lake area in km2; the red line

is a linear regression fit of the area measurements, and aqua shading surrounding the red line refers to the 95% confidence interval of the lake area. Green circles are distance in km of parent glacier frontal recede; the green line is a linear regression fitting within a 95% confidence interval, indicted by pink shading

# **Recent Landslides**

Image /page/5/Figure/1 description: A series of four satellite images, labeled (a) through (d), showing a glacial landscape at different points in time. Each image includes a legend and scale. The dates for the images are: (a) 2018/6/6, (b) 2019/6/25, (c) 2020/5/1, and (d) 2020/7/27. The images depict a large glacier in shades of cyan, with surrounding land in brown, green, and red. A large, dark blue glacial lake is prominent in the upper left of each frame. A smaller, higher-elevation lake is visible in panel (a), but appears to have drained in the subsequent images. Key features are labeled, including the city of Yiga and elevations such as 3800m, 4845m, and 6838m. A legend in the bottom left of each panel defines symbols for City, Elevation, Glacier area, Lake area, Ice dam, Natural drainage channel, and Conduit. The legend for panel (d) also includes a symbol for Breach.

Fig. 6 A comparison of the Jinweng Co area and the surrounding glaciers before and after the GLOF: **a** June 6, 2018, Landsat-8 image; **b** June 25, 2019, Landsat-8 image; **c** May 1, 2020, Sentinel-2 image; and **d** July 27, 2020, Sentinel-2 image

# Discussions

## Meteorological conditions before the event

The intensity, duration, and frequency of precipitation, as well as temperature rise, can affect the timing and magnitude of glacier movements and GLOF events. To further understand the meteorological conditions before the 2020 event, we processed daily precipitation, monthly precipitation, and air temperature data. Figure 7 shows the meteorological conditions at Jinweng Co. The monthly precipitation fluctuates seasonally, with the rainy season lasting from February to July and very little precipitation during the intervening winter months. The highest monthly rainfall of up to 240 mm occurred during June 2020, and the heaviest daily rainfall reached 45 mm on June 21, 2020. This was approximately 4 days before the GLOF event. Moreover, air temperature changed periodically, with the hottest period of the year from late May to mid-August. Extreme rainfall and temperature conditions are important driving factors that increased discharge into the lake and led to the lake outburst (see discussion later).

It can be seen that the June 25, 2020, outburst occurred at the highest monthly/daily precipitation. The unusually heavy rainfall combined with the warmer summer temperature provides a plausible explanation for the Jinweng Co outburst for two reasons.

First, heavy rainfall increased water inflow to Jinweng Co and thus increased discharge. Second, the heavy rainfall on June 21 may have also acted as an indirect trigger of the outburst when this precipitation provoked slope movement into the lake.

The Jinweng Co outburst chain provides a strong example of the role of extreme precipitation and temperature change in a GLOF-related disaster. According to the meteorological reports, the weather has been warming at a rate of 0.5 °C per decade over the last 40 years (You et al. 2016). This suggests that the warming trend constantly persists over Tibet. Based on the results of the glacier movement and lake change, it is certain that climate warming has caused glacier tongue recede, thinning, and lake expansion.

## Slope movement and ice collapse before the GLOF event

To understand the factors associated with the June 2020 outburst, we used time series SAR intensity images and two-pass InSAR (e.g., Lu et al. 2003). Figure 8a-e show the time series SAR intensity images from May 28 to July 15 and reveal several changes. The lake expanded from May 28 to June 9, as indicated by the yellow arrows in Fig. 8a, b. In Fig. 8c-e, we found a section at the western lateral moraine moved downslope into the lake on or after June 21, and the deposit from the landslide can be

Fig. 7 Daily and monthly precipitation and air temperature records over the Jinweng Co area. Daily precipitation is shown as blue bars, monthly rainfall in black smoothed curve, and air temperature in purple dots

Image /page/5/Figure/12 description: A combination chart displaying climate data from late 2016 to mid-2020. The x-axis represents the date in yyyy/mm/d format, starting from 2016/12/1 and extending past 2020/6/1. There are two y-axes. The left y-axis, labeled in blue, represents daily precipitation in millimeters (mm) and ranges from 0 to 50. The right y-axis has two scales: one in magenta for Temperature in degrees Celsius (°C) ranging from -20 to 20, and another in black for Monthly precipitation (mm) ranging from 0 to 300. The chart displays three data series: Daily precipitation is shown as blue vertical bars, Monthly precipitation is a black line graph, and Temperature is represented by magenta dots. All three data series show a clear seasonal pattern, with peaks in the summer months and troughs in the winter months. A specific event labeled "Outburst" in red text is marked with a red dashed vertical line around May 2020, coinciding with a high peak in daily precipitation.

Image /page/6/Figure/0 description: A scientific figure composed of ten panels arranged in two rows and five columns, labeled (a) through (j). The top row, panels (a) to (e), displays a time series of grayscale images of a rugged terrain, dated 2020/5/28, 2020/6/9, 2020/6/21, 2020/7/3, and 2020/7/15 respectively. The bottom row, panels (f) to (j), shows colorful images of the same terrain over different time periods: (f) 2017/5/20-2017/7/31, (g) 2017/6/1-2017/8/24, (h) 2018/6/20-2018/8/7, (i) 2019/7/21-2019/8/26, and (j) 2020/8/8-2020/8/20. Each panel includes a circular magnified inset showing a detailed view of a specific area. Panel (a) contains a north arrow and a scale bar indicating 0, 0.5, and 1 Km. At the bottom right, a color scale bar for the colorful images ranges from 0 to 2.83 cm.

**Fig. 8** Map of the landslide activity. **a–e** Sentinel-1 intensity images of the Jinweng Co and its surroundings representing the situation on May 28, June 9, June 21, July 3, and July 15. SAR backscattering images over the landslide are enlarged in the inset to improve visibil-

ity. **f-j** Deformation interferograms of Jinweng Co and surroundings for several periods during 2017–2020. Each fringe (a complete cycle of color variations) represents a 2.83 cm range change in the radar look direction

seen in Fig. 8d, e. We used InSAR to study possible long-term deformation in the area around the landslide for several periods in 2017–2020 (Fig. 8f-j). Since interferometric coherence for C-band Sentinel-1 images are low in the Jinweng Co surroundings (where the surface is covered with snow in winter), we analyzed interferograms with high coherence acquired in summer (Fig. 8f-j). The baselines between the image pairs were less than 60 m, so the interferograms were insensitive to DEM errors. The deformation maps formed from independent image pairs with

very different atmospheric situations show essentially the same patterns at a section of the lateral moraine. This means that the fringes are a real deformation. Therefore, this section of the lateral moraine was experiencing long-term deformation and likely finally collapsed into the lake due to heavy rainfall on June 21, 2020. Therefore, the rainfall-triggered landslide that occurred on or after June 21, 2020, exerted an important effect on this lake outburst event because the water waves may have overflowed the dam and/or directly caused the rupture of the dam.

Image /page/6/Figure/5 description: A scientific figure presented in a grid format, comparing two grayscale images of a rugged, mountainous terrain. The figure is divided into two main columns. The left column contains two rectangular images labeled (a) and (b). Image (a) at the top left shows the terrain with a north arrow in the upper left corner, a scale bar labeled '0 0.5 1 Km' in the lower left, and three white circles numbered 1, 2, and 3 highlighting specific areas. Image (b) below it shows a similar view of the terrain without any annotations. The right column consists of a 2x3 grid of six circular, magnified images. The top row is labeled (a1), (a2), and (a3), and these correspond to the magnified views of the areas marked 1, 2, and 3 in image (a), respectively. The bottom row is labeled (b1), (b2), and (b3), which are the corresponding magnified views from image (b). Each pair of vertical images, such as (a1) and (b1), shows the same feature, allowing for a direct comparison between the two source images (a) and (b).

**Fig. 9** (a) Average Sentinel-1 intensity image based on SAR images of May 28 and June 9 2020. (b) Average Sentinel-1 intensity image based on SAR images of June 21, July 3, July 15, and July 27, 2020.

The changes in the glacier tongue, the landslide, and the southern end of the lake are shown by (a1) (b1), (a2) (b2), and (a3) (b3), respectively

# **Recent Landslides**

Image /page/7/Picture/1 description: A diagram illustrating the causes of recent landslides. The image shows a body of water labeled "Jinweng Co" surrounded by brown land labeled "Lateral moraine". On the left, a light blue "Glacier" is shown melting into the lake, indicated by a red arrow and the word "Melting". Above the scene, grey clouds are causing "Extreme rainfall". The combination of melting and rainfall leads to "Water rising", indicated by a yellow arrow pointing up from the water's surface. A green mass of earth, labeled "Landslide", is shown sliding from the moraine into the lake. On the far right, the lake has an "Outlet" where water flows out.

**Fig. 10** Schematic diagrams illustrating the triggering factors and final mechanism of dam failure

The time series SAR intensity images also indicate that significant changes occurred before the landslide on the southern end of the lake between June 9 and 21. We compared the average intensity images before and after June 9 (Fig. 9) to investigate this phenomenon. Figure 9 shows a clear difference in the glacier tongue (Fig. 9a1, b1). We suggest that the change in the lake surface on June 21 (Fig. 9, b3) resulted from the collapse of ice on a steep portion of the glacier tongue (Fig. 9(a1), (b1)). Such collapse and runout could also have trapped moraine on the path into the lake. Hence, between June 9 and 21, the ice collapsed under the steep topography and transported the iceberg and moraine into the front of the lake. This caused the obvious variation seen in the June 21 SAR image (Fig. 9). Moreover, the landslide that occurred in the western lateral moraine can be observed through Fig. 9a2, b2. The distinct sliding boundary further demonstrates that the landslide might cause harm to the lake by striking the lake body and may be one of the primary GLOF triggering factors.

## **Outburst mechanism of Jinweng Co**

Based on the displacement features of the parent glacier, the lake changes with SAR intensity, optical images, inventory data, and extreme meteorological conditions, there is evidence that the slope of the western lateral moraine was unstable due to glacier recede. The extremely high precipitation in June 2020 facilitated the erosion of the pre-weakening slope, finally inducing landslide activity. The sketch map in Fig. 10 shows the triggering factors and outburst mechanism of Jinweng Co. First, the hydrologically controlled glacier movement and melting generated masses of destabilizing sediments. Second, due to geomorphic conditions, the steep slopes above the lake produced huge kinetic energy when ice masses slid into the lake. Third, the daily precipitation about 4 days before the GLOF event was the largest in the past 3 years. Anomalous rain events or seasonal changes in the dynamics of the surrounding glaciers might be key triggering factors causing sudden hydro-fracturing and outburst floods in summer. Increased water inflow to the lake caused increased discharge from the morainedammed lake, which may have provoked increased erosion and incision

of the outflow channel into the dam body. More importantly, the landslide activity that occurred from the western lateral moraine on or after June 21 played a key role in the GLOF event because the fast slope movement into the lake is capable of producing water waves. This may have caused direct dam rupture. Overall, the causal chain for triggering the June 2020 outburst is a hydraulic connection established from a possible collapse of the glacial ice, a landslide, heavy precipitation, and warm temperature.

# **Conclusions**

Multi-source remote sensing datasets and processing methods combined with meteorological observations were used in this study for GLOF investigation. These were then applied to comprehend the recent movement of parent glaciers and reveal the mechanisms leading to the outburst flood. Offset tracking of multi-track Sentinel-1 images was combined to retrieve the long-term time series displacement and 3D glacier flow velocity field. Optical Sentinel-2 and Landsat-8 images and inventory data were interpreted to reconstruct the long-term changes in the glacial lake. SAR intensity images and interferograms were analyzed to characterize changes in the glacier tongue and lateral moraine collapse.

In this study, to analyze lake outburst factors, we identified two important critical stages for the Jinweng Co outburst. First, ice collapse occurred in the parent glacier from June 9 to 21, and this transported ice and moraine into the front of the lake. Second, a landslide originating from the western lateral moraine occurred forcefully from June 21 to 25 and placed additional deposits into the lake body. The water level increased due to the unusually heavy rainfall on June 21, 2020; when combined with meltwater from glaciers, it provoked anomalous water importation. Due to the availability of pre-weakening lateral moraine combined with heavy rainfall on June 21, landslide activity was a serious factor for triggering dam failure by producing displacement waves. Hence, the main mechanism may be that the landslide mobilized and entered the lake between June 21 and 25, which caused the surface waves, triggered overtopping, and finally caused dam rupture.

The kinetic movement and outburst mechanism factors of Jinweng Co revealed in this study can be used to assess the potential risks of other glacier lakes in the region. Further, with the rise in extreme precipitation and the rapid melting of glaciers that lead to the destabilization of glacial lakes, moraine instabilities under changing climate conditions could become more likely. Therefore, process chains such as Jinweng Co will become increasingly significant in the future.

# **Acknowledgements**

Sentinel-1/2 data were provided by the Sentinel Scientific Data Hub of the European Space Agency (ESA). Landsat-8 data were acquired using the Geospatial Data Cloud (http://www.gscloud.cn/). Lake inventory data were obtained from the National Tibetan Plateau Data Center (TPDC) (https://data.tpdc.ac.cn). We thank the editor and anonymous reviewers for their helpful suggestions and Zheng Guoxiong for providing the photos used in this investigation.

## **Funding**

This research was funded by the Scientific Innovation Practice Project of Postgraduates of Chang'an University (Grants No. 300103714010, 300203211263) and the Shuler-Foscue Endowment at Southern Methodist University.
