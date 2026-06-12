

Abstract. The melting of glaciers has led to an unprecedented increase in the number and size of glacial lakes, particularly in the Himalayan region. A glacial lake outburst flood (GLOF) is a natural hazard in which water from a glacial or glacier-fed lake is swiftly discharged. GLOFs can significantly harm life, infrastructure, and settlements located downstream and can have considerable ecological, economic, and social impacts. Based on a dam breach model, BREACH, and a hydrodynamic model, HEC-RAS (Hydrologic Engineering Centre's River Analysis System), we examined the potential consequences of a GLOF originating from the Thorthomi glacial lake, located within the Phochhu river basin, one of Bhutan's largest and rapidly expanding glacial lakes. Our analysis revealed that following a breach the Thorthomi glacial lake will likely discharge a peak flow of 16360 m<sup>3</sup> s<sup>-1</sup> within 4h. Such a discharge could potentially cause considerable damage, with an estimated 245 ha of agricultural land and over 1277 buildings at risk of inundation. To mitigate ecological, economic, and social impacts on downstream areas, our results emphasise an urgent need for understanding and preparing for the potential consequences of a GLOF from Thorthomi lake. Our findings provide valuable insights for policymakers and stakeholders involved in disaster management and preparedness.

# 1 Introduction

## 1.1 Glacial lakes and outburst floods

Floods are one of the most common natural disasters worldwide and can cause extensive socio-economic damage. Globally, over the last 2 decades, floods have affected approximately 2.3 billion people and have caused an estimated USD 622 billion in damage (UNISDR, 2015). Glacial lake outburst floods (GLOFs) are floods caused by sudden water release from glacial or glacier-fed lakes and cause a rapid rise in water level over a short time in downstream areas, resulting in devastating consequences (Gurung et al., 2017; Komori et al., 2012; Taylor et al., 2023). GLOFs are infrequent but highly destructive natural disasters that are difficult to predict. Prior to their occurrence, the extent of damage is also difficult to predict. Over the past few decades, the acceleration of glacier melt and recession, primarily driven by climate change, has led to a significant increase in the number of moraine-dammed (natural dams formed by glacial processes) glacial lakes (Sattar et al., 2021; Westoby et al., 2014; Worni et al., 2014). Taylor et al. (2023) estimated that approximately 15 million people are exposed to risks associated with potential GLOFs and that most of these populations are concentrated within High Mountain Asian (HMA) areas. Due to climate warming (Gardelle et al., 2011), the eastern Himalayan area, in particular, has seen a significant increase in the number and area of glacial lakes, thereby increasing the vulnerability of nearby communities to potential GLOF impacts (Hagg et al., 2021).

Although GLOF research and studies have gained global momentum in recent years, only a few studies have been per-formed in Bhutan. Numerous studies conducted in Nepal and

<sup>&</sup>lt;sup>1</sup>National Center for Hydrology and Meteorology, Thimphu, Bhutan

<sup>&</sup>lt;sup>2</sup>Department of Civil and Environmental Engineering, Nagoya University, Nagoya 464-8603, Aichi, Japan

China have simulated and assessed GLOF risks, although detailed studies on Bhutan's exposure to GLOF-related hazards are scarce. Such scarcity can be attributed to a lack of required field data, as well as to Bhutan's limited exposure to the global scientific community.

## 1.2 Past GLOF events in Bhutan

In the past, Bhutan has faced several GLOF events; however, many of these events were either not reported or not documented. One of the most catastrophic GLOFs took place on 6 October 1994, when the moraine dam of Luggye lake partially collapsed, leading to the release of a massive amount of water and debris downstream, destruction to infrastructure and farmland, and the death of 21 people (Watanabe and Rothacher, 1996; Leber et al., 2000). Another significant GLOF occurred in 2009, when an outburst from Tshojo lake, located at the headwaters of the Phochhu river, caused downstream flooding. Based on satellite imagery and a sedimentological and geomorphological analysis, Komori et al. (2012) attributed an outburst from the supraglacial lake on the Tshojo glacier to the event. The most recent GLOF, the Lemthang Tsho outburst, took place on 28 July 2015. Gurung et al. (2017) reported that heavy rainfall triggered the event and that  $0.37 \times 10^6 \,\mathrm{m}^3$  of water was discharged.

## 1.3 Potentially dangerous glacial lakes in Bhutan

Based on the latest report from the National Center for Hydrology and Meteorology (NCHM) in Bhutan, 567 glacial lakes in the country span an area of 55.04 km<sup>2</sup>, accounting for 19.03% of total water bodies (NCHM, 2021). In 2001, the Department of Geology and Mines (DGM) in Bhutan and the International Centre for Integrated Mountain Development (ICIMOD) performed the first-ever inventory of glaciers, glacial lakes, and potentially dangerous glacial lakes (PDGLs), and they identified 24 glacial lakes that fit this category (Mool et al., 2001). However, in 2019, using field-verified data and the latest Sentinel-2 satellite images, NCHM reassessed the number of PDGLs and revised the number to 25, with eight lakes now considered to be safe based on lake morphology, surrounding features, bathymetry conditions, and associated feeding glaciers (NCHM, 2019). Figure 1 provides a map of rivers and the river basin system within Bhutan, together with the distribution of glaciers and glacial lakes. The Punatsangchhu river basin contains 11 PDGLs, which is the largest number of PDGLs per basin the in the country. The Phochhu sub-basin contains nine PDGLs, making it a hotspot for GLOFs and glacially related disasters.

Warming climate exacerbates the hazards of GLOFs, so a comprehensive GLOF assessment is urgently needed since these risks will increase in the coming years. As such, a study assessing hazards associated with glacial lakes and GLOFs is crucial for understanding hazards, as well as their subsequent impacts on hydrological and socio-economic aspects within the Punatsangchhu river basin.

## 1.4 Increasing concern regarding a Thorthomi GLOF

Thorthomi lake is the largest of nine PDGLs within the Phochhu basin. Due to the significant potential risk posed to downstream settlements resulting from a GLOF, the Thorthomi glacial lake has become a serious concern due to the following factors: (1) rapid expansion of the Thorthomi supraglacial lake, (2) the size of glaciers and probable future lake size, (3) the weakened left lateral moraine of the lake due to the 1994 Luggye GLOF, (4) active sliding on the moraine wall separating the Thorthomi and Rapstreng lakes, (5) seepage from the lake, and (6) rock and snow avalanches, as summarised by Karma (2013). To address these factors, the government of Bhutan initiated a highpriority project, referred to as the National Adaptation Plan of Action (NAPA), under the United Nations Framework Convention on Climate Change (UNFCCC) funding scheme in 2006. The project sought to reduce the GLOF risk potential from Thorthomi lake and involved lowering the lake's water level over 4 years, resulting in a reduction of 3.68 m. However, due to challenging working conditions and health issues, the project fell 1.32 m short of its target, although approximately  $17 \times 10^6$  m<sup>3</sup> of lake water was artificially released. The project additionally included setting up a GLOF early warning system along the Punakha-Wangdue valley for alerting residents in the event of a GLOF.

## 1.5 The focus of our study

To contribute to risk management efforts, we evaluated the potential risk of a GLOF from Thorthomi lake. The physically based mathematical dam breach model, BREACH, was used to simulate a glacial lake dam breach and was coupled with the Hydrologic Engineering Centre's River Analysis System (HEC-RAS) to route the flood wave propagating downstream. We sought to simulate both the spatial extent and the lead time of flood wave arrival at several locations along the river. Prior to predicting Thorthomi GLOF hazards and potential risks, we reconstructed the 1994 Luggye GLOF event to validate the dam breach model and the flood wave routing model, which includes river topography and roughness

Our study is one of a few studies that has simulated probable floods from Thorthomi lake and that has estimated inundation extent and flood arrival times within a scientific setting. Such studies form an essential basis for flood risk assessments, early warning system installation, economic planning, countermeasure planning, design, and stakeholder education and awareness programmes.

The main components of our study are as follows:

Image /page/2/Figure/2 description: A map of Bhutan showing its river and basin systems, along with the distribution of potentially dangerous glacial lakes (PDGLs). The map includes a north arrow, latitude and longitude lines from 27°0'0"N to 28°0'0"N and 89°0'0"E to 92°0'0"E, and a scale bar in kilometers. The legend details various features: Rivers (blue lines), Sub-basin boundaries (dashed lines), the Punatsangchhu basin (shaded gray), the Bhutan boundary (solid outline), Glaciers (light blue areas in the north), Main Roads (brown lines), and Urban Areas (yellow patches). The map also plots PDGLs as circles, categorized into two groups. The first group, 'PDGLs(sq.km)', is shown in purple with sizes corresponding to areas: 0.1 - 0.67, 0.67 - 1.46, and 1.46 - 2.9 sq.km. The second group, 'PDGLs(sq.km)-safe', is shown in green with sizes for areas: 0-0.06, 0.06-0.34, and 0.34-0.58 sq.km. Several lakes in the northern region are labeled, including Rapstreng Lake, Thorthomi Lake, and Luggye Lake.

**Figure 1.** A map showing the rivers and basin system of Bhutan, as well as the distribution of potentially dangerous glacial lakes, the main road network, and major urban areas. Bubbles are scaled to total lake area and colour-coded for classification. PDGLs stand for potentially dangerous glacial lakes. Data source: National Center for Hydrology and Meteorology (NCHM).

- estimating the geometry and water volume of Thorthomi lake using available glacial lake geometry data;
- estimating the potential outburst flood hydrograph using a dam breach model, BREACH, with available physical parameters; and
- 3. assessing Thorthomi GLOF hazards and potential risks using a 2D hydraulic model.

## 1.6 Structure of the paper

The paper contains six sections. Section 1 introduces the overall concept of a GLOF and provides information obtained from previous studies and information related to GLOFs in the context of Bhutan. Section 2 describes the study area and the GLOF event used for model validation and calibration. We explain materials and methods in Sect. 3. Obtained results are reported in Sect. 4. Based on the results, we discuss the consequences of a Thorthomi GLOF in Sect. 5. We conclude our study in Sect. 6.

# 2 Study area and GLOF events

We assessed flood risk for a catchment of under-construction hydropower plants, specifically the Punatsangchhu Hydroelectric Project Authority (PHPA-I and II), caused by a GLOF from Thorthomi lake. The catchment is the upper part of the Punatsangchhu river basin (PRB), located within the central portion of Bhutan and indicated by the grey area in Fig. 2a. PRB is one of the largest basins in Bhutan, spanning an approximate area of 9760 km², which covers approximately 25 % of the total area of the country (38 394 km²), and is drained by the Phochhu and Mochhu rivers (Fig. 2a) to the Indian plains. The annual averaged discharge of the basin ranges from 194 to 374 m³ s<sup>-1</sup>, with the highest recorded discharge of 2654 m³ s<sup>-1</sup>, observed at the WangdiRapid station (location shown in Fig. 2c), occurring in 2009 during Cyclone Aila.

The Phochhu river, one of the main tributaries of the Punatsangchhu river, originates from the high mountains of Lunana, in northern Bhutan, and flows some 90 km downstream, where it joins Mochhu at Punakha Dzong (monastery) (Fig. 2c), and flows from this area as the Punatsangchhu river. The Thorthomi glacial lake, considered to be one of the most dynamic and dangerous glacial lakes within Bhutan, with an area of 4.3 km<sup>2</sup> (NCHM, 2019), is

Image /page/3/Figure/2 description: The image displays three maps labeled (a), (b), and (c), detailing a study area in Bhutan. Map (a) is an inset showing the location of the Punatsangchu Basin (shaded gray) and a smaller study basin (outlined in red) within Bhutan, which borders China and India. Map (b) is a topographic map of the study basin, with an elevation scale ranging from 1153 m to 7207 m and a distance scale up to 40 kilometers. Map (c) is the main, detailed map of the area. It includes a legend defining symbols for River, Glacial lake, Study Basin, Punatsangchu\_Basin, Settlement Points (circle), Gauging Station (green square), and Power Plant (green triangle). This map shows the Phochhu river and its tributaries, the Mochhu and Dangchhu. Key locations identified include the glacial lakes Thorthomi Lake and Luggye Lake, and settlement points such as Lhedi, Thanza, Dangsa, Samdingkha, Punakha Dzong, Khuruthang, Jagathang, and Bajo. It also marks the WangdiRapid Station (a gauging station), two hydropower plants under construction (PHPA-I & II), and the confluence points of the Phochhu with the Mochhu and Dangchhu rivers. The map indicates the flow direction of the Phochhu river and labels the administrative regions of GASA, PUNAKHA, and WANGDUE.

**Figure 2.** Map of the study area. (a) A Bhutan map showing rivers and river basins (the grey area shows the Punatsangchhu river basin). (b) The elevation distribution of the study area (the catchment area of PHPA-I and II excludes the Mochhu river basin). (c) Major settlement points within the study area.

located at the headwater of the Phochhu sub-basin at over 4440 m above sea level. The Thorthomi glacial lake is widely recognised as the likely consequence of climate warming and, since feeding glaciers terminating in the lake rapidly melt, is expanding each year. Based on a comprehensive analysis of cryospheric, geotechnical, and geomorphological factors, Rinzin et al. (2023) concluded that Thorthomi lake is highly susceptible to GLOF events.

The PRB consists of five administrative districts: Gasa, Punakha, Wangdue Phodrang, Dagana, and Tsirang. These districts constitute 16.6 % (735 533) of the total population of Bhutan (NSB, 2018). The Punakha and Wangdue Phodrang districts (Fig. 2) within the PRB are renowned as Bhutan's primary rice production regions, contributing 16 % and 11 %, respectively, to the nation's total rice output (NSB, 2021). The area is also rich in historical and cultural heritage, with notable landmarks such as Punakha Dzong, which served as the former capital of Bhutan. Fertile flood plains are located along the Phochhu and Punatsangchhu rivers, and the region encompasses settlements such as Samdingkha and Jagathang, together with major towns such as Khuruthang and Bajo. The floodplain of the Punatsangchhu river accommodates these settlements, while downstream, approximately 115 km away from Thorthomi lake, two significant

Image /page/3/Figure/6 description: A topographic map showing four glacial lakes in a mountainous region. The lakes are labeled from left to right (west to east): Rapstreng Lake, Thorthomi Lake, Luggye Lake, and DrukChung Lake. A river, identified as 'Lake Outflow', flows along the southern side of the lakes. An arrow indicates the 'Flow Direction' is from east to west (right to left). A legend in the top right corner defines the symbols used: a blue shape for 'Glacial lake', a thin blue line for 'Lake Outflow', and a black dot for 'Lake outlet'. Each lake has a designated outlet marked on the map. In the bottom left, there is a scale bar indicating a length of 4 kilometers. A north arrow is located in the top left corner. The background of the map consists of gray contour lines representing the terrain.

**Figure 3.** Four glacial lakes within the Lunana region (the Lunana complex).

hydropower plants, PHPA-I and II, are currently under construction (see the bottom of Fig. 2c for locations of the two hydropower plants). Given the exposure of critical infrastructure and settlements to potential GLOFs from PDGLs, especially the Thorthomi glacial lake, an assessment of hazards within this area is of paramount importance.

The Luggye glacial lake is one of the PDGLs in Lunana, Bhutan's northern region. The lake is one of four glacial lakes in an area that spans a few kilometres (Fig. 3) and had an outburst in 1994. Although there is no detailed official documentation on the GLOF at the Luggye glacial lake, reports and articles describing the event do exist (e.g. Koike and Takenaka, 2012; Meyer et al., 2006; Richardson and Reynolds, 2000; Watanabe and Rothacher, 1996). The event was also documented in a technical report (Leber et al., 2000), when the Royal Government of Bhutan launched a major investigative project in 2000 to study the cause of the event.

The 1994 Luggye GLOF was a cascading phenomenon, where sudden drainage of the upstream Druk Chung glacial lake (Fig. 3) into Luggye lake increased hydrostatic pressure on the moraine dam of Luggye lake, releasing  $18 \times 10^6$  m<sup>3</sup> of flood water (Leber et al., 2000). The 1994 Luggye GLOF claimed the lives of 21 people and inflicted major damage to infrastructure and downstream settlements; notably, the Punakha Dzong (monastery) suffered significant damage, although it is located 93 km downstream from the lake (Richardson and Reynolds, 2000; Watanabe and Rothacher, 1996). During this period, a peak flow rate of  $2539 \,\mathrm{m}^3 \,\mathrm{s}^{-1}$ was observed at the WangdiRapid gauging station, located 15 km downstream of Punakha Dzong (Fig. 2) and approximately 108 km downstream of the flood source (data from NCHM). Contributions from the Mochhu (96  $\mathrm{m}^3$  s<sup>-1</sup> on 7 October 1994), Dangchhu basins (no gauging station in the basin), and other small tributaries to the peak flow rate should have been minor due to limited base flow during the season.

To estimate the breach outflow hydrograph, several studies have attempted to reconstruct the 1994 Luggye GLOF event (e.g. JICA, 2001; Koike and Takenaka, 2012; Meyer et al., 2006). Koike and Takenaka (2012) estimated that peak discharge from the Luggye lake breach ranged from 1800 to

 $2500 \,\mathrm{m}^3 \,\mathrm{s}^{-1}$ , depending on inflow conditions measured by Yamada et al. (2004).

# 3 Materials and methods

A schematic diagram showing input data, used models/methods, and outputs is provided in Fig. 4. We reconstructed the 1994 GLOF event to verify (1) a glacial lake geometry estimation model, (2) a dam breach model, (3) a digital elevation model and its error correction method, and (4) Manning's coefficient. Then, the same models were used to predict the potential risk caused by a Thorthomi GLOF.

## 3.1 Uncertainty in GLOF bathymetry

The volume and geometry of a glacial lake are regulating factors of the glacial lake outburst process. Glacial lakes are generally formed from a depression left behind by retreating glaciers, which, in most cases, are produced when a moraine is filled with meltwater. Depending on geomorphology, the presence of sediment, and glacial over-deepening capacity, formed glacial lakes can manifest specific lake bathymetry and influence glacial hydrology (Cook and Swift, 2012). Due to remote locations and high elevations, accessing and conducting field surveys to map glacial lake bathymetry is challenging.

Despite challenges, measurements of lake bathymetry are crucial for determining a lake's volume and surface area and are necessary for assessing potential flood volumes and the risk of GLOFs. In 2019, the National Centre for Hydrology and Meteorology (NCHM) conducted bathymetric surveys in 14 of the 25 identified potentially dangerous glacial lakes and mapped their maximum depth and volume. However, even though the Thorthomi glacial lake is considered to be a critical lake that could burst in the future, due to the difficulty associated with conducting a survey, the bathymetry of the Thorthomi glacial lake remains unknown. Since lake geometry is a crucial parameter for dam breach modelling and subsequent hydraulic routing, lake depth and volume needed to be estimated.

## 3.2 Estimating geometries of glacial lakes

Estimating the potential flood volume of a glacial lake is critical for determining the magnitude of a GLOF. Bathymetry data are necessary for calculating lake volume as well as potential flood volume, but bathymetry for glacial lakes is scarce due to the challenging and inaccessible environments in which glacial lakes are often located, including for Thorthomi lake. Although several reports have estimated Thorthomi lake volume (Karma, 2013; Singh, 2009), no details on how volumes were estimated have been documented.

To address data scarcity for glacial lake geometries, various studies have proposed methods for estimating glacial lake depth and volume based on other more accessible pa-

rameters such as lake area (Cook and Quincey, 2015; Huggel et al., 2002; O'Connor et al., 2001; Sakai, 2012), as well as depression angle from the lakeshore (Fujita et al., 2013) and surrounding topography (Heathcote et al., 2015). Empirical relationships such as area–volume and area–depth are useful for estimating a lake's depth and potential flood volume. Cook and Quincey (2015) refined the area–volume relationship proposed by Huggel et al. (2002) by increasing sample size and removing duplicated samples. They also classified the predictability of lake volume and depth based on regions and lake types and determined that predictability is influenced by a lake's origin and evolution. The relationship proposed by Cook and Quincey (2015) takes the following form:

$$D_{\text{mean}} = 0.1697 A^{0.3778},\tag{1}$$

where  $D_{\text{mean}}$  is the mean depth (in m) and A is the area (in m<sup>2</sup>). The volume–area relationship (V, volume in m<sup>3</sup>) can simply be derived by multiplying the area of both sides, as follows:

$$V = 0.1697A^{1.3778}. (2)$$

Sakai (2012) used a similar approach and proposed a model for estimating maximum depth instead of mean depth. The bathymetric measurement data of 17 glacial lakes (15 moraine-dammed glacial lakes and 2 thermokarst lakes) from Bhutan, Nepal, and Tibet were used to derive an area—maximum depth—volume relationship, so estimations of depth and volume from the area of glacial lakes could be determined (Sakai, 2012). The regression equation took the following form:

$$D_{\text{max}} = 95.665 A^{0.489},\tag{3}$$

where  $D_{\text{max}}$  is maximum depth (in m) and A is area (in km<sup>2</sup>). The volume–area relationship (V, volume in  $10^6 \text{ m}^3$ ) takes the following form:

$$V = 43.24A^{1.5307}. (4)$$

For predicting the moraine dam breach process explained in the following section, lake geometries, especially the maximum depth, are crucial, so we employed the equations proposed by Sakai (2012). The equations allow the independent calculation of maximum depth and volume. As conceptualised by Cook and Quincey (2015), bathymetry of the lake was estimated based on idealised geometric shape. The lake bottom was also assumed to follow an elliptical shape, as commonly observed in most moraine-dammed glacial lakes in Bhutan.

## 3.3 The moraine dam breach and its modelling

### 3.3.1 Previous studies

GLOFs are triggered by a breach of a moraine dam that holds the lake in place and are caused by an external triggering

Image /page/5/Figure/2 description: A flowchart illustrating a methodology for creating an inundation map and hazard zonation. The chart uses a legend to define its components: gray rounded rectangles for 'Input Data', blue parallelograms for 'Model', and green rounded rectangles for 'Result'. The process starts with input data including 'Digital Elevation Model', 'Lake bathymetry data', and 'Lake moraine data'. These inputs, along with processed data like 'Field bathymetry data for GLOF reconstruction' and 'Regression analysis data for GLOF prediction', are fed into a 'Dam Breach Model'. The output of this model is a 'Breach flow hydrograph'. This result, along with the 'Digital Elevation Model' and other inputs like 'Land Use Land Cover Data' and 'Satellite imagery', goes into a 'Hydrodynamic Model'. The 'Hydrodynamic Model' produces 'Simulated flow Hydraulics'. This result, combined with 'Land Use Land Cover Data', 'Satellite imagery', and 'Settlement data', is processed by a 'GIS' model. The final output of the entire process is an 'Inundation Map Hazard Zonation'.

Figure 4. A schematic diagram of the methodology employed in our study.

event. While the structure of the dam itself is an important factor, destabilisation of a dam due to a trigger event is the primary cause of a breach. Since the overtopping of lake water is the major failure mode (Awal et al., 2010; Begam et al., 2018; Neupane et al., 2019), our study assumed that GLOFs are triggered by the overtopping of lake water.

To estimate flood flow and associated hazards resulting from a dam breach, several studies have simulated dam breach floods using dam breach models (Bajracharya et al., 2007; Hagg et al., 2021; Huggel et al., 2002; Koike and Takenaka, 2012; Maskey et al., 2020; Meyer et al., 2006; Shahrim and Ros, 2020; Wang et al., 2008; Worni et al., 2014). BREACH is a numerical model describing the dam breach process and the resulting outflow hydrograph. The model is based on fundamental principles of hydraulics, sediment transport, soil mechanics, and the physical properties of dam materials and the reservoir. The model is physically based and was designed to predict the size, shape, and time of dam breach development, as well as the resulting flow rate and the volume of water released. Unlike parametric models, physically based breach models, including BREACH, consider the geotechnical aspects of dam materials, as well as hydraulic and sediment transport (Fread, 1988; Maskey et al., 2020; Worni et al., 2014), which increases the predictive accuracy of future GLOF processes. Due to this, the BREACH model has been widely used in studies of dam breach flood hazards and risk assessments (Fread, 1988).

Koike and Takenaka (2012) used the BREACH model coupled with the flood flow model, FLO-2D, to perform a sce-

nario analysis on the risks of a GLOF on the Mangdechhu river basin, due to an outburst flood of the Metatshota glacial lake in Bhutan. The study concluded that although the breaching potential of the lake is low due to the wide crest and gentle slope of the moraine dam, a GLOF would affect several houses and farmland located on the flood plain (Koike and Takenaka, 2012). Hagg et al. (2021) performed a GLOF hazard assessment within the Mochhu basin in Bhutan using the HEC-RAS dam break module, simulating a dam breach of the Shintaphu glacial lake, and concluded that risk is comparably small.

Our study used BREACH for describing the dam breach process for target lakes due to its better predictive accuracy for a future extraordinary Thorthomi GLOF event. The dam is assumed to breach due to overtopping flow resulting from a trigger event, such as an ice calving/avalanche or a rock avalanche. Most of the geotechnical properties of dam materials required as an input parameter are available in the report published by the National Center for Hydrology and Meteorology (NCHM, 2020). A few properties were published by Koike and Takenaka (2012). Some unavailable data were estimated by referring to previous studies.

### 3.3.2 Reconstruction of the 1994 Luggye GLOF dam breach

For reconstruction of the 1994 Luggye GLOF, the dam breach outflow hydrograph was estimated using BREACH (Fread, 1988). The bathymetry of Luggye lake (Fig. 5) and

Image /page/6/Figure/2 description: A bathymetric map showing the depth elevation of a lake. The lake is elongated and slightly curved. A north arrow is in the top left corner. The legend in the bottom left indicates the lake boundary with a thin black line and the lake outlet with a red-brown circle, which is located at the westernmost tip of the lake. A scale bar at the bottom shows a total length of 1.3 kilometers, with marks at 0, 0.325, and 0.65 kilometers. On the right, a vertical color scale labeled "Bathymetry Depth elevation (m)" ranges from 4353.5 (dark purple, deeper) to 4465.8 (dark green, shallower). The map shows the lake is shallowest around the edges and has its deepest point in the central-eastern area. The easternmost part of the lake is a white area labeled "No Data".

Figure 5. The bathymetry of Luggye lake (data from NCHM).

the material properties of the moraine dam (the middle row of Table 1) required for the model were based on various reports (NCHM, 2019, 2020). Topographic data of the moraine dam were derived from the digital surface model (DSM). Since wave overtopping is a more common failure mode for moraine-dammed glacial lakes as compared to a piping failure (Neupane et al., 2019), to estimate breach outflow from Luggye lake, overtopping failure of the moraine dam was assumed. The properties of moraine dam material have a significant effect on the growth of a breach (Maskey et al., 2020; Westoby et al., 2014). The mechanism in which the formation of a breach largely occurs determines the shape of the breach outflow hydrograph (Westoby et al., 2014). Therefore, gathering accurate in situ data for reliable breach process reproduction is essential. Based on the estimation by Fujita et al. (2008), deduced from a combination of field measurements and remote-sensing observations, the level of lake water was reduced 19 m during the event.

### 3.3.3 The Thorthomi GLOF prediction

Breach initiation is assumed to occur due to an overtopping wave at the existing outlet (Fig. 3) induced by any probable triggering event. Moraine material properties and topographic data for the Thorthomi lake BREACH model were either estimated from available terrain data or adopted from available reports and research documents, and this is also listed in the right row of Table 1.

## 3.4 Flood routing

### 3.4.1 The hydrodynamic model

A hydrodynamic model is essential for understanding the characteristics of a flood wave caused by a GLOF propagating downstream, as well as for quantitatively evaluating the potential risks caused by a flood. To simulate the propagation of outflow from glacial lake breaches in Nepal, numerous studies, such as HEC-RAS used in Maskey et al. (2020), have employed various hydrodynamic models. Similar approaches that couple dam breach models to hydrodynamic models (e.g. Bajracharya et al., 2007; Koike and Takenaka, 2012; Westoby et al., 2015; Worni et al., 2014) have been

performed for modelling the GLOF process chain in various regions.

Worni et al. (2014) provided a summary of various hydrodynamic models that have been used to model GLOFs. Discussed models include HEC-RAS, FLO-2D, BASEMENT, and Delft3D. The choice of a hydrodynamic model depends on factors such as the end objective, data availability, and the available budget. Each model has its own level of accuracy; however, the accuracy of results is primarily dependent on the precision of the elevation model, including channel geometry and floodplain topography. Errors in the elevation model can lead to inaccuracies in results (Casas et al., 2006; Xu et al., 2021).

HEC-RAS is a commonly used hydrodynamic model that allows users to perform 1D and 2D steady/unsteady flow simulations (Brunner, 2016b). We used the HEC-RAS to perform a 2D unsteady flow simulation for floods caused by a glacial lake dam breach. Since they represent spatially varied flood hydraulics (Horritt and Bates, 2001), the twodimensional models employed are standard in flood modelling. In a 2D unsteady simulation, flow varies in time, along two spatial dimensions, and processes are predicted by the laws of conservation of mass (continuity) and the conservation of momentum for two horizontal directions. We used a full set of momentum equations (the shallow water equations) to simulate flooding as clear water flow. Although high-viscosity and hyper-concentrated (sediment entrained) flows are inherent to the GLOF phenomenon (Clague and Evans, 2000; Vuichard and Zimmermann, 1987), to simplify modelling complexity and data requirements, most studies (Hagg et al., 2021; Koike and Takenaka, 2012; Maskey et al., 2020; Rinzin et al., 2023) have simulated GLOFs as clear water flow.

Other important considerations in hydrodynamic modelling are Manning's roughness coefficient and channel geometry. Both have significant impacts in predicting inundation extent and flow characteristics (Mosquera-Machado and Ahmad, 2007; Ye et al., 2018; Zhu et al., 2019). Hagg et al. (2021) demonstrated the influence of Manning's roughness coefficient for glacial lake outburst floods from the Shintaphu glacial lake in Mochhu basin, Bhutan, and concluded that channel roughness is not essential for inundation extent but exerts a significant effect on flood velocity and flood arrival time.

Since such information is needed to estimate the area needed for evacuation and the lead time for evacuation, flood travel time and peak flow are essential parameters for early warning purposes. In this study, flood travel time was calculated based on timing of the breach outflow hydrograph and the flow hydrograph at the point of interest, when there was significant inundation depth and extent. Peak flow is the maximum simulated flow resulting from a dam breach.

| Moraine dam data                                 | 1994 Luggye GLOF | Thorthomi GLOF |
|--------------------------------------------------|------------------|----------------|
| Surface area of the lake (km2) (RSA)             | 1.46b            | 4.3b           |
| Volume of water in the lake (106 m3), Eq. (4)    | 65.19b           | 400a           |
| Maximum depth of the lake (m), Eq. (3)           | 96.93b           | 161a           |
| Top elevation of the dam (m) (HU)                | 4465a            | 4446a          |
| Toe elevation of the dam (m) (HL)                | 4370a            | 4345a          |
| Slope of the upstream face of the dam (1 : ZU)   | 1 : 4.8a         | 1 : 6.2a       |
| Slope of the downstream face of the dam (1 : ZU) | 1 : 6.5a         | 1 : 6.3a       |
| Dam material properties                          |                  |                |
| Grain size ( <i>D</i> 50) (mm)                   | 1.362b           | 2.01b          |
| Porosity (%)                                     | 36.5c            | 36.5c          |
| Cohesive strength (kN m-2)                       | 1.5b             | 1.5b           |
| Internal friction (°)                            | 41b              | 39b            |
| Unit weight (kN m-3)                             | 22.92b           | 22.43b         |
| Manning's coefficient (s m-1/3)                  | 0.07b            | 0.07b          |

Table 1. Input parameters for the 1994 Luggye GLOF reconstruction and the Thorthomi GLOF prediction.

### 3.4.2 Ground elevation models and pre-conditioning

The accuracy of hydrodynamic model results is heavily influenced by the quality of the elevation model used (Gyasi-Agyei et al., 1995; Yamazaki et al., 2014, 2017). Casas et al. (2006) demonstrated the effects of a topographic data source and resolution on flood peak discharge and the extent of inundation and then concluded that laser-based elevation data are a suitable source for hydraulic modelling. Similarly, the influence of grid size on inundation propagation and water depth under varied topographical settings in 2D modelling has been analysed (Tsubaki and Kawahara, 2013). Both fine grid size representing main topographic features of the floodplain and accurate elevations at each grid point are essential for simulating flood flow with less uncertainty. Therefore, using the best available elevation model for the hydrodynamic simulation of floods is essential.

Since an accurate elevation model is essential for accurate hydrodynamic simulations, various methods for correcting generic noise errors and biases originating from topography measurements have been proposed and have been used in elevation models prior to running hydrodynamic/hydrological analyses.

Below, we compare three different elevation models covering the study area. The first model, the Multi-Error-Removed Improved-Terrain (MERIT) Hydro DEM (Fig. 6a), was developed based on SRTM and AW3D DEM. Water layer data at a 3 arcsec resolution ( $\sim 90\,\mathrm{m}$ ) were developed for river hydrology analyses at global, as well as at local, scales (Yamazaki et al., 2017, 2019). Other bias-corrected elevation data are the Forest And Buildings removed Copernicus DEM (FABDEM) (Fig. 6b), developed from Copernicus DEM (COPDEM), where the height of trees and buildings

are removed using machine learning, and are also a preferable source for terrain data (Hawker et al., 2022). The AW3D digital surface model (DSM) (Fig. 6c) was jointly developed by the Remote Sensing Technology Centre (RESTEC) and the NTT DATA Corporation, utilising PRISM data acquired by the Advanced Land Observing Satellite (ALOS) of the Japan Aerospace Exploration Agency (JAXA). Roughresolution DSMs are distributed by several organisations free of charge; however, for our study, we used the finer commercial DSM product, AW3D 2.5 m, as the primary source of topography. The cell size of the DSM for the focus area was approximately  $2.2 \,\mathrm{m}$  for both the X and Y directions and was projected to WGS84 UTM zone 45N. The AW3D 2.5 m DSM represents details of topography, especially in the river valley and in the developed flood plain, much better than other models.

Since the AW3D DSM was obtained using satellite photogrammetry, representations of the river bottom, especially in forested and deep gorge areas, are sometimes inaccurate. If we directly used topography in hydrodynamic modelling, the DSM covered structures along the river, as well as bridges crossing the river, disturbing flood water flow. To avoid such anomalies in the elevation model and in the hydrodynamic simulation results, a river channel delineation was performed. The presence of spikes within the DSM, along the river's path, can obstruct flood water flow, resulting in the formation of non-existent deep pools. One way to improve topography surrounding a river is the use of bathymetric survey data. However, no such survey has been conducted within the study area. To improve representation for the river channel, our study utilised a rule-based correction method.

The Agriculture Conservation Planning Framework (ACPF) is a GIS-based tool developed by the United States

<sup>&</sup>lt;sup>a</sup> Estimated in this study. <sup>b</sup> NCHM (2020). <sup>c</sup> Koike and Takenaka (2012).

Image /page/8/Figure/2 description: A figure with three panels labeled (a), (b), and (c), showing topographic maps of the same area at different resolutions. The area shown is around Punakha Dzong. Panel (a) is a low-resolution, pixelated map with a scale bar from 0 to 1.2 kilometers. Panel (b) shows the same area at a higher resolution, with less prominent pixelation. Panel (c) is a high-resolution, smooth map that includes a legend for Punakha Dzong and a north arrow in the upper right corner. All three maps use a color gradient from brown for higher elevations to blue-green for lower elevations and show the location of Punakha Dzong with a black outline.

Figure 6. The Punakha Dzong region as represented by three different terrain models: (a) the MERIT HydroDEM 90 m, (b) the FABDEM-30 m, and (c) the AW3D 2.5 m DSM.

Department of Agriculture (USDA) to identify areas with impeded water flow and to improve hydrologic flow using flow direction and an accumulation analysis (Porter et al., 2016). While the ACPF is a valuable tool for hydrologic flow and watershed planning, it has limited applicability for terrain correction in hydrodynamic modelling because the ACPF does not allow users to define the bathymetry of a river channel.

Another widely used channel modification method is the inbuilt function of HEC-RAS. The Channel Design/Modification editor tool is a module used to modify an unrealistic cross-section or to introduce a user-defined channel crosssection (Brunner, 2016a). The tool effectively removes spikes in the elevation model along a river channel while maintaining the natural slope of the represented topography. The modified channel TIN (triangulated irregular network) can be overlain on the original DSM and exported as a single raster file with modified features. Rinzin et al. (2023) applied the method to modify terrain and to delineate river flow paths for a GLOF simulation. For our study, we used this tool to condition the DSM in the middle region of the model domain, a forested deep gorge, where huge spikes were included within the elevation model. The modification was only applied to the channel section, and the remaining portion was left as it was.

### 3.4.3 Implementation for GLOF reconstruction and prediction

Downstream propagation of the flood was simulated using the HEC-RAS model for the 1994 Luggye GLOF reconstruction. The calculation domain was defined by the 2D flow area. The overall size of the flow area was  $64 \,\mathrm{km^2}$ . The domain was modelled using a 20 m resolution computational grid, consisting of 157 188 computational cells, and solved with a time step of 1 s. The elevation of each grid cell was specified based on a 2.2 m, hydro-conditioned digital surface model, and Manning's n was set to 0.035, in the range provided by the HEC-RAS manual (Brunner, 2016a). The dam breach outflow hydrograph obtained from the BREACH

model was used as the upstream boundary; and normal depth, calculated based on downstream slopes derived from the DSM, was used as the downstream boundary condition.

For the Thorthomi GLOF prediction, we used a hydrodynamic model similar to the model used for the 1994 Luggye GLOF reconstruction. The domain was a bit shortened because the Thorthomi glacial lake is located 2 km downstream of the Luggye glacial lake. The overall size of the flow area was 62 km<sup>2</sup>. The domain was modelled using a 20 m resolution computational grid consisting of 153 790 computational cells with a temporal resolution of 1 s.

# 4 Results

## 4.1 The 1994 Luggye GLOF reconstruction

### 4.1.1 Dam breach processes

Simulated peak flow  $(Q_p)$  of the dam breach outflow hydrograph was  $6030\,\mathrm{m}^3\,\mathrm{s}^{-1}$ , and  $1.9\,\mathrm{h}$  ( $\sim 114\,\mathrm{min}$ ) was required to reach peak flow (the time to peak,  $T_p$ ) (Fig. 7a). The volume of the GLOF and the reduction of lake water level due to the event were  $21\times10^6\,\mathrm{m}^3$  and  $19\,\mathrm{m}$ , respectively, in agreement with the findings of Fujita et al. (2008), which was based on a combination of in situ observations and remotesensing data. Dimensions for the estimated breach of the dam are provided in Fig. 7b.

### 4.1.2 Downstream peak flow and flood travel time

Flow hydrographs at various locations along the flow path are provided in Fig. 8. Conforming to the findings of Meyer et al. (2006), after approximately 6 h, the GLOF had a peak discharge of 2897 m<sup>3</sup> s<sup>-1</sup> as it reached Punakha Dzong, located 93 km downstream of the lake. Peak flow at the WangdiRapid station (shown in Fig. 2c), 15 km downstream of Punakha Dzong, was 2455 m<sup>3</sup> s<sup>-1</sup>, close to the recorded value of 2539 m<sup>3</sup> s<sup>-1</sup>. Here, the recorded flow rate included the contribution of normal flow from tributaries, which was not ac-

Image /page/9/Figure/2 description: The image contains two diagrams labeled (a) and (b). Diagram (a) is a line graph titled "Flow vs. Time". The x-axis is labeled "Time (h)" and ranges from 0 to 24. The y-axis is labeled "Flow (m³ s⁻¹)" and ranges from 0 to 6000. The graph shows a sharp peak in flow, reaching approximately 6000 m³ s⁻¹ at around 2 hours, and then gradually decreasing over the 24-hour period. Diagram (b) is a 3D representation of a trapezoidal channel cross-section. The top width of the channel is labeled as 102 m. There are two vertical height measurements indicated: one is 19 m from the bottom of the channel to an intermediate level, and the other is the total height of 22 m from the bottom to the top.

Figure 7. (a) A breach outflow hydrograph from the BREACH model and (b) an illustration of breach parameters, breach width  $(\leftrightarrow)$ , breach depth  $(\updownarrow)$ , and the change in water surface elevation  $(\updownarrow)$ .

Image /page/9/Figure/4 description: A line graph showing Flow (m³ s⁻¹) versus Time (h). The y-axis, labeled "Flow (m³ s⁻¹)", ranges from 0 to 4000. The x-axis, labeled "Time (h)", ranges from 0 to 24. There are two curves on the graph. The black curve, labeled "Punakha Dzong", starts rising sharply around 5.5 hours, peaks at approximately 2900 m³/s at 6 hours, and then gradually decreases. The blue curve, labeled "WangdiRapid Station", starts rising around 7 hours, peaks at about 2500 m³/s around 8 hours, and then gradually decreases. A red horizontal arrow labeled "~ 6 h" and identified in the legend as "Flood Travel Time" extends from time 0 to the peak of the Punakha Dzong curve at 6 hours.

**Figure 8.** A simulated GLOF hydrograph at different locations along the flow path.

counted for in our analysis. Good agreement of results for simulated flow and flood travel time with observed data, as well as previous studies, indicated that the performance of the employed models and the modelling approach were adequate and capable of yielding satisfactory results for predictive modelling of the target lake. The total inundated area along the basin was approximately 13.1 km<sup>2</sup>.

## 4.2 Future Thorthomi GLOF prediction

### 4.2.1 Lake bathymetry

The estimated volume and maximum depth of Thorthomi lake based on Eqs. (3) and (4) were  $400 \times 10^6$  m<sup>3</sup> and 161 m, respectively (the top right of Table 1). The estimated volume and maximum depth of Thorthomi lake falls within the predicted band, considering a 95% confidence level. The utilised equations showed a good relationship between area and volume and between and area and maximum depth, with the prediction of  $400 \times 10^6$  m<sup>3</sup> for the mean and  $281 \times 10^6$  m<sup>3</sup> and  $560 \times 10^6$  m<sup>3</sup> for the lower bound and the upper bound, respectively. The prediction range for maximum depth was 161 m for the mean prediction (130 m and 270 m for the lower bound and the upper bound, respectively). Compared to other glacial lakes in Bhutan, the estimated parameters indicate that the Thorthomi glacial lake is one of the largest and deepest lakes. The bathymetry of Thorthomi lake, estimated based on the above parameters, is provided in Fig. 9.

A recent study from Nepal proposed a glacial lake volume estimation equation by considering the width and length ratio

Image /page/9/Figure/11 description: A bathymetric map of the Thorthomi Lake Area. The map includes a legend, a north arrow, a scale bar, and a color scale for elevation. The legend indicates symbols for Outlets (red circle), Outflow (wavy blue line), Thorthomi Lake Area (solid outline), PDGL area (dashed outline), and Glaciers (grey shaded area). The map shows the lake with a single outlet and outflow on its western side. Glaciers are located at the northern end of the lake, and a PDGL area is situated along the eastern side. The bathymetry, representing depth and elevation in meters, is shown with a color gradient from green (4446 m) to brown (4285 m), indicating the lake is deepest in its central and southern parts. A scale bar at the bottom is marked in increments up to 1.8 kilometers.

**Figure 9.** The estimated bathymetry of Thorthomi lake.

of the lake (Qi et al., 2022). Based on the equation provided in Qi et al. (2022), the water volume of Thorthomi lake can be estimated as  $227 \times 10^6 \, \text{m}^3$ . This volume is substantially small compared to the volume estimated by Eq. (4). The discrepancy may be related to the dataset used for each study, namely Eq. (4) is based on lakes in Bhutan, Nepal, and Tibet; and Qi et al. (2022) is based on lakes in the Peruvian Andes and other areas, including non-moraine-dammed lakes.

### 4.2.2 Dam breach processes

Different dam breach scenarios for maximum breach and a partial breach for a half breach width and depth (50% of maximum width and depth) were simulated to ascertain the potential risk under various breaching possibilities, including a partial dam breach, which occurred in 1994 (e.g. the 1994 Luggye GLOF). Simulated peak flow  $(Q_p)$  resulting from the Thorthomi dam breach under different breach scenarios ranged from  $9700 \,\mathrm{m}^3 \,\mathrm{s}^{-1}$  (for a 50 % breach depth) to 16 360 m<sup>3</sup> s<sup>-1</sup> (for maximum breach width and depth), with a time to peak  $(T_p)$  of 3.4 to 4 h, respectively (Fig. 10a). The bathymetry of the lake and the topography of the moraine dam dictate the total lake drawdown depth and the volume of the outburst flood. In this study, we estimated that 100 m of lake water depth will be lowered before the breach outflow channel becomes sufficiently stable, after sending  $283 \times 10^6 \,\mathrm{m}^3$  (approximately 70 % of estimated lake water) of flood water downstream (Fig. 10b). The breach outflow channel was assumed to be stable when its bottom elevation reached the natural bed level of the downstream channel and down-cutting ceased.

Image /page/10/Figure/2 description: The image contains two panels, labeled (a) and (b). Panel (a) is a line graph that plots Flow in cubic meters per second (m³ s⁻¹) against Time in hours (h). The x-axis ranges from 0 to 24 hours, and the y-axis ranges from 0 to 15,000 m³ s⁻¹. There are three curves on the graph, each representing a different scenario: 'Maximum Breach' (dark red line), 'Half Breach Width' (blue line), and 'Half Breach Depth' (black line). The 'Maximum Breach' curve peaks at the highest flow, over 15,000 m³ s⁻¹ at approximately 4 hours. The 'Half Breach Depth' curve peaks at around 13,500 m³ s⁻¹ at about 3.5 hours. The 'Half Breach Width' curve has the lowest peak, just under 10,000 m³ s⁻¹ at about 4.5 hours. Panel (b) is a 3D diagram of a trapezoidal channel, illustrating its dimensions. The top width is indicated as 225 m, and the depth is shown as 100 m.

Figure 10. (a) A dam breach outflow hydrograph obtained from the BREACH model for three different scenarios and (b) breach parameters, breach width  $(\leftarrow)$ , and breach depth  $(\cline{1})$  in metres for the maximum breach scenario.

## 4.3 Downstream peak flow and flood travel time

The simulated flow hydrographs for three different scenarios at eight major settlement areas are provided in Fig. 11. Peak flow of the GLOF gradually attenuated as it propagated downstream. Peak flow at Punakha Dzong ranged from 8900 to  $14\,130\,\mathrm{m}^3\,\mathrm{s}^{-1}$  and decreased from 8200 to  $11\,500\,\mathrm{m}^3\,\mathrm{s}^{-1}$  when it arrived at the hydropower plant (PHPA-I).

A schematic representation of an approximate distance, peak flow, averaged channel slope, and the estimated flood travel time for a maximum breach condition is provided in Fig. 12 (refer to Sect. 3.4.1 for the definition of the peak flow and flood travel time in this study). The estimated peak flow at Punakha Dzong,  $14\,130\,\mathrm{m}^3\,\mathrm{s}^{-1}$ , is expected to be over 5 times higher than the 1994 Luggye GLOF (the recorded value is  $2539\,\mathrm{m}^3\,\mathrm{s}^{-1}$ , and the value estimated in this study is  $2455\,\mathrm{m}^3\,\mathrm{s}^{-1}$ ).

# 5 Discussion

## 5.1 Inundation hazard in five vulnerable areas under the maximum breach scenario

The flood depth distribution, highlighting five vulnerable areas for a maximum breach scenario, is provided in Fig. 13. The villages of Thanza, Toncho, and Lhedi, located in the northernmost part of the study area (Fig. 2), are expected to be inundated under a Thorthomi GLOF scenario. The 1994 Luggye GLOF also caused major damage to these settlement areas, but a Thorthomi GLOF is expected to cause more severe damage due to larger flood volume and shorter lead time. Major settlements along the river basin lie in the lower valleys of the Punakha and Wangdue districts, where large areas are expected to be flooded. Major towns and settlements, such as Samdingkha, Khuruthang, and Bajo, are expected to be inundated. The Mochhu river converges with the Phochhu river at the top left of Fig. 13c. Substantial overflow surrounding the Mochhu river, around the confluence, has been predicted. This result is due to backwater flow from the Phochhu river. Water flow from the Mochhu river is not easy to accurately estimate in advance and was not accounted for in this study, so inundation surrounding Punakha Dzong may be underestimated. However, the contribution of water from the Mochhu river can be negligible because the base flow of the Mochhu river is approximately  $100\,\mathrm{m}^3\,\mathrm{s}^{-1}$ , which is substantially small compared to estimated peak flow in this area,  $14\,130\,\mathrm{m}^3\,\mathrm{s}^{-1}$ . Total inundated area due to a Thorthomi GLOF, with a maximum breach, was estimated to be approximately  $22\,\mathrm{km}^2$ , which is almost twice the area inundated under the Luggye GLOF simulation ( $13.1\,\mathrm{km}^2$ , estimated in this study).

## 5.2 A comparison between three scenarios

Figure 14 compares the maximum inundation depth and extent for three different scenarios for the town of Khuruthang. Simulation results for the three scenarios considered in this study revealed that the overall inundation extent and flood depths were higher for the maximum breach scenario. However, the depth and flood extent for the two other scenarios were comparable to the maximum breach scenario. The results indicate that even for a partial breach of the moraine dam, substantial damage within the downstream settlement areas (Punakha and Wangdue) is expected. The results imply that the difference in glacial lake bathymetry may also affect the maximum inundation in downstream areas but is not very sensitive because of the nature of the GLOF event (consisting of a rapid dam breach process and flood routing in steep valleys).

## 5.3 Time series change of flood depth distribution surrounding Punakha Dzong

The spatial distribution of flood depth for a maximum breach scenario, at different time steps, for Punakha Dzong and Khuruthang town are provided in Fig. 15. Due to higher peak flow and a longer flood duration, overall flood hazard potential for the inhabited area caused by the Thorthomi lake GLOF, as compared to damages during the 1994 Luggye GLOF, was significantly higher. Most of the flood path lies in the narrow V-shaped valley, where there are few to no settlements or infrastructure. We estimated that over 1277 houses, most in the lower region of the study area, will be inundated in a GLOF. Aside from this, infrastructure such as roads, bridges, and sand dredging equipment will be damaged.

Notable damage during the 1994 GLOF occurred in Punakha Dzong. The area near the Punakha Dzong was completely inundated in the 1994 Luggye GLOF. The simulated future GLOF indicates that the Punakha Dzong area will be completely flooded, with a maximum depth of over 10 m (Figs. 13 and 15).

## 5.4 Socio-economic impact

The Punakha (the middle downstream of the domain; see Fig. 13) and the Wangdue districts (consisting of the Bajo and Jagathang settlements, as well as the downstream do-

Image /page/11/Figure/2 description: An image displaying eight line graphs in a 2x4 grid, each showing simulated flood hydrographs for different locations. The locations are Lhedi, Samdingkha, Punakha Dzong, and Khuruthang in the top row, and Jagathang, Bajo, WangdiRapid station, and Hydropower plant in the bottom row. Each graph plots Flow in cubic meters per second (m³ s⁻¹) on the y-axis against Time in hours (h) on the x-axis, which ranges from 0 to 24. A legend in the top-left graph indicates three scenarios: 'Max' (red line), 'BRD-50%' (black line), and 'BRW-50%' (blue line). In all graphs, the 'Max' scenario shows the highest peak flow, followed by 'BRD-50%', and then 'BRW-50%'. The peak flows generally decrease and occur later in time for locations further down the grid. For example, in the 'Lhedi' graph, the 'Max' flow peaks at approximately 16,000 m³/s around 5 hours, while in the 'Hydropower plant' graph, the 'Max' flow peaks at approximately 11,000 m³/s around 9 hours.

**Figure 11.** A simulated flow hydrograph at important locations, derived from the HEC-RAS; result for each scenario (max: maximum breach; BRD-50 %: half of maximum breach depth; BRW-50 %: half of maximum breach width).

Image /page/11/Figure/4 description: A schematic diagram illustrating the characteristics of a flood along a river path, starting from Thorthomi Lake. The top part of the diagram shows a profile view of the river's elevation, which decreases as the distance from the lake increases. Key locations along the path are marked with their distances from the lake: Lhedi (19 km), Samdingkha (83 km), Punakha Dzong (90 km), Khuruthang (94 km), Bajo (103 km), and a Hydropower Plant (115 km). Below this profile, three horizontal bars provide quantitative data for different segments of the river. The first bar, labeled "Peak Flow (m³ s⁻¹)", shows a decreasing flow rate from 16,300 at Lhedi to 11,550 at the Hydropower Plant. The second bar, "Average Slope (dy/dx)", shows the slope for each segment, with values ranging from 0.001 to 0.038. The third bar, "Flood Travel Time (h)", indicates the time taken for the flood to traverse each segment, with values such as 2.6 hours for the first segment and 7.1 hours for the last.

Figure 12. A schematic representation of flood parameters at six important locations along the flow path for the maximum breach scenario.

main; see Figs. 2 and 13) are leading producers of rice, an essential crop for the country's GDP and food security. Any damage to agricultural land would have a devastating impact on farmers and the nation. Aside from potential damage to buildings and infrastructure, such as roads and bridges, agricultural land would also become submerged and destroyed by a flood. We estimated that approximately 193 to 245 ha of agricultural land will be inundated under different scenarios

in a Thorthomi GLOF event. Figure 16 shows the potential extent of floods for different land use classes and highlights probable damage to agricultural land, particularly in the areas of Samdingkha and Jagathang.

The overall hazard potential of a GLOF from Thorthomi lake under different scenarios is summarised in Table 2. Although the peak flow rate of each scenario is different (29 % to 37 % between the maximum and minimum for the result

Image /page/12/Figure/2 description: A figure displaying a series of maps illustrating flood inundation in a study area. The figure is composed of a central legend, a study area map, and five detailed maps labeled (a) through (e).

The legend defines symbols for Bridges, Education Centres, Health Care Centres, Historical Places, Road Network, Settlements, River, and Thorthomi\_Lake.

The study area map shows a river originating from Thorthomi\_Lake with five locations marked along its path: (a), (b), (c), (d), and (e).

Each of the five detailed maps shows a satellite view of one of these locations with a flood inundation overlay, a scale bar, and a legend for flood depth in meters (m).

- Map (a) Thanza: Shows a wide flooded area. The flood depth legend is: 0 - 5 m, 5.1 - 10 m, and 10.1 - 15.6 m. The scale bar goes up to 50 kilometers.
- Map (b) Samdingkha: Shows a flooded river channel. The flood depth legend is: 0 - 6 m, 6.1 - 12 m, and 12.1 - 18.7 m. The scale bar goes up to 1.6 kilometers.
- Map (c) Punakha Dzong: Shows a flooded area at a river confluence. The flood depth legend is: 0 - 7 m, 7.1 - 14 m, and 14.1 - 23.2 m. The scale bar goes up to 2 kilometers.
- Map (d) Khuruthang: Shows a flooded river bend. The flood depth legend is: 0 - 8 m, 8.1 - 15 m, and 15.1 - 25.8 m. The scale bar goes up to 3 kilometers.
- Map (e) Jagathang & Bajo: Shows a flooded winding river. The flood depth legend is: 0 - 7 m, 7.1 - 15 m, and 15.1 - 22.6 m. The scale bar goes up to 3 kilometers.

Each map uses shades of blue to represent flood depth, with darker shades indicating deeper water. Icons from the legend are placed on the maps to show the locations of infrastructure and settlements.

Figure 13. A maximum GLOF inundation map of the study area under the maximum breach scenario. Map data: © Google Earth 2023, CNES/Airbus, Maxar Technologies.

depicted in Fig. 11), the total inundation area, the number of submerged buildings, and the area of impacted cultivated land are not much different (12%, 22%, and 21%, respectively), implying that the estimated flood is significant even for the most minor flood scenario (BRW-50% scenario) for the Thorthomi GLOF. The scenarios indicate that most of the damage will occur for river properties and that farmland will be substantially damaged, even when a dam breach is not drastic. The soil in farmlands will also be eroded and covered by debris. Damage to irrigation is expected and may affect agriculture in farmland located behind flooded areas. Over the long term, damage to soil and irrigation would extensively reduce farmers' production. In advance, careful evacuation planning and business continuity planning (e.g. JICA,

2015), including a plan for agriculture, are essential for mitigating damage caused by a future Thorthomi GLOF.

## 5.5 Limitations of this study

Due to a lack of actual surveyed data, volume and maximum depth were estimated based on the statistical relationships established by past studies; an uncertainty for the estimated bathymetry of Thorthomi lake is a major limitation of our study. As compared to the bathymetry presented, the use of actual, surveyed bathymetric data may yield a more accurate prediction. An additional limitation of our study is the clear water assumption. Compared to clear water, hyperconcentrated water has different dynamic properties. Debris in flood water may cause substantial damage to farmland, in-

Image /page/13/Figure/2 description: A figure composed of four panels, labeled (a), (b), (c), and (d), illustrating a flood model for a river system. Panel (a) is a map showing the overall area. It includes a north arrow and a scale bar from 0 to 40 kilometers. The legend in panel (a) identifies symbols for Khuruthang Town, a River, the Model Domain, Thorthomi Lake, and the Maximum breach inundation extent. The map displays Thorthomi Lake at the top, feeding a river that flows downwards. A small rectangular area on the map is magnified in the other panels. Panels (b), (c), and (d) are three similar close-up aerial views of a town next to a river, showing flood inundation. Each of these panels includes a legend for water depth in meters (m), with three color-coded ranges: light gray for 0 - 10 m, medium blue for 10.1 - 15 m, and dark blue for 15.1 - 25.9 m. The blue overlay on the aerial images shows the extent and depth of the floodwaters, with the deepest water in the main river channel.

**Figure 14.** A comparison of inundation depth and extent for three breach scenarios within the Khuruthang study area. (a) A model domain highlighting Khuruthang town. (b) The maximum breach scenario. (c) A 50 % breach depth scenario. (d) A 50 % breach width scenario. Map data: © Google Earth 2023, CNES/Airbus, Maxar Technologies.

Image /page/13/Figure/4 description: A multi-panel figure, labeled Figure 15, illustrating the temporal change of the spatial extent of flood depth at Punakha Dzong and Khuruthang. Panel (a) is a map showing the model domain, which includes Thorthomi Lake in the north and a river flowing south. Two locations are marked: Punakha Dzong and Khuruthang Town. The legend indicates symbols for the river, model domain, and Thorthomi Lake. A scale bar shows distances up to 20 kilometers. Panels (b) through (g) show a time-series of the flood's progression in a zoomed-in area around Punakha Dzong and Khuruthang Town. Each of these panels has a legend for water depth in meters, categorized into three levels: 0-10 m (light blue), 10.1-15 m (medium blue), and 15.1-25.9 m (dark blue). The panels show the increasing extent and depth of the flood at different time steps: (b) 05:54, (c) 06:06, (d) 06:12, (e) 06:24, (f) 06:30, and (g) 08:00. The sequence shows the flood wave arriving, peaking in depth and extent around time step 06:30, and then beginning to recede by 08:00, with significant inundation affecting Khuruthang Town.

Figure 15. The temporal change of the spatial extent of flood depth at Punakha Dzong and Khuruthang. (a) The hydrodynamic model domain. (b-g) The inundation depth at six time steps.

frastructure, and human life. Research on glacial lakes and their outburst floods is an emerging field (e.g. Qi et al., 2022; Taylor et al., 2023). To obtain more accurate damage predictions, data and methods should be revised following research progress.

The close proximity of glacial lakes within the Lunana region, especially the Thorthomi and Rapstreng lakes (Fig. 3), poses an even greater potential risk due to a possible cascad-

ing GLOF event. Failure of the lateral moraine of Thorthomi lake would lead to lake water breaching into Rapstreng lake, which would consequently cause the failure of its moraine dam. Since our study considered failure of the terminal moraine in the direction of the existing outlet, it is highly unlikely for such an event to occur under the current scenario. Accordingly, a cascading GLOF was not assessed in our study, but such possibilities should also be explored to

Image /page/14/Figure/2 description: A figure displaying three land use maps of a mountainous region, with a comprehensive legend. The main map on the left shows a large area with a scale bar from 0 to 20 kilometers. It depicts a valley with various land use classes, including large areas of green (Alpine Scrubs; Forests; Meadows; Shrubs) and light blue (Moraines; Snow and Glacier). A white line delineates the 'Simulation Domain' along the valley. Two smaller, zoomed-in maps are on the right, labeled 'Samdingkha' and 'Jagathang', each with a scale bar from 0 to 1.2 kilometers. These maps show a more detailed, pixelated view of sections of the river, with a red line indicating the 'Inundation Boundary'. The legend provides a key for the 'Land use class' colors: Black for 'Built up', Blue for 'Water Bodies', Brown for 'Cultivated Agriculture', Green for 'Alpine Scrubs; Forests; Meadows; Shrubs', Light Blue for 'Moraines; Snow and Glacier', and Grey for 'Non Built up; Rocky Outcrops'. All maps include a north arrow.

Figure 16. The probable GLOF inundation extent on land use classes. (Land use data source: National Land Commission Secretariat, Bhutan.)

**Table 2.** The damage potential of a GLOF from Thorthomi lake.

| Hazards →<br>Scenarios↓                 | Total inundation area (km2) | Number of buildings inundated | Total cultivated agricultural land impacted (ha) |
|-----------------------------------------|-----------------------------|-------------------------------|--------------------------------------------------|
| Maximum breach                          | 22.7                        | 1277                          | 245.6                                            |
| Half of maximum breach depth (BRD-50 %) | 20.8                        | 1044                          | 206.4                                            |
| Half of maximum breach width (BRW-50 %) | 19.9                        | 1000                          | 193.4                                            |

better understand the potential risk of cascading events which may cause more severe damage to society.

# 6 Conclusion

We explored future hazards and damages arising from a GLOF from Thorthomi lake, one of the potentially dangerous glacial lakes in Bhutan but not well investigated within the scientific literature to date. To validate the approach used in our study and to calibrate the model, we reconstructed the 1994 Luggye lake GLOF prior to assessing the hazards of a Thorthomi GLOF. The BREACH model was used to es-

timate the outflow hydrograph emanating from a failure of moraine dams due to overtopping flow. Moraine materials and soil parameters used to parameterise the model were obtained from a report published by the National Center for Hydrology and Meteorology (NCHM), Bhutan. Propagation of the GLOF was simulated using a 2D routing module in HEC-RAS for modelling unsteady flow, which is an inherent characteristic of a GLOF where there is a sharp rise in the flow hydrograph.

The bathymetry of Thorthomi lake was estimated based on a regression equation derived from the relationship between lake area—depth—volume found within moraine lakes. We estimated that the total volume of the lake is approximately  $400 \times 10^6 \,\mathrm{m}^3$ , with a maximum depth of 161 m. According to the maximum breach scenario, the Thorthomi GLOF may release  $283 \times 10^6 \,\mathrm{m}^3$  of water in under 12 h, with a peak flow rate of  $16\,360 \,\mathrm{m}^3 \,\mathrm{s}^{-1}$ , occurring approximately 4 h following initiation of the breaching process. Outflow hydrographs estimated by the model were used as the upstream boundary condition in hydrodynamic modelling.

Flood routing was performed to reach a length of approximately 115 km, and then peak discharge, flood travel time, and flood depths at major downstream settlements were estimated. According to the maximum breach scenario, Punakha Dzong, which lies 90 km downstream of Thorthomi lake and at the beginning of major settlements, would witness a peak discharge of  $14\,128\,\mathrm{m}^3\,\mathrm{s}^{-1}$ , approximately 6 h following breach initiation. A potential GLOF from Thorthomi lake would cause extensive agricultural and infrastructural damage to 245 ha of agricultural lands, and, for a maximum breach scenario, 1277 buildings are expected to be inundated. Comparable damage is also expected for two minor flood scenarios, implying that such damage is inevitable for a future Thorthomi GLOF.

A hazard assessment for a GLOF plays a crucial role for understanding and mitigating risks associated with these devastating natural events. Our study quantified the potential danger a GLOF from Thorthomi lake would pose to the downstream settlements and infrastructure. Such assessments will enable policymakers, local communities, and relevant stakeholders to make informed decisions regarding land use planning, disaster preparedness, and early warning systems.

Since glacial environments are dynamic and subject to change due to climate variations, GLOF hazard assessments are not static. Continuous monitoring and regular reassessments of glacial lakes and associated hazards are essential to account for environmental shifts and to ensure the effectiveness of mitigation strategies. Furthermore, a multidisciplinary approach in GLOF hazard assessments is necessary. Collaborations between researchers, policymakers, local communities, and other stakeholders are essential for effective decision-making, disaster preparedness, and the implementation of mitigation measures. To essentially reduce GLOF risk, the development of methods to safely release dammed water to downstream areas is important.

*Data availability.* Our study used open and commercial data (NSB, 2021, 2018; NCHM, 2021). Commercial data may be distributed under licence terms and conditions.

Author contributions. TW: conceptualisation, data curation, method, and writing original draft; RT: conceptualisation, data curation, draft writing, and reviewing and editing.

Competing interests. The contact author has declared that neither of the authors has any competing interests.

*Disclaimer.* Publisher's note: Copernicus Publications remains neutral with regard to jurisdictional claims made in the text, published maps, institutional affiliations, or any other geographical representation in this paper. While Copernicus Publications makes every effort to include appropriate place names, the final responsibility lies with the authors.

Acknowledgements. Tandin Wangchuk acknowledges a Human Resource Development Scholarship from the Japan International Cooperation Agency (JICA). We acknowledge Yuji Toda and Takashi Tashiro, as well as other lab members of the Hydraulic Research Laboratory at Nagoya University. We also express our gratitude to Shigeo Suizu, Tomoyuki Wada, and Toru Koike at Earth System Science Co., Ltd. We sincerely thank members of the National Center for Hydrology and Meteorology for their continued support of our study.

Review statement. This paper was edited by Pascal Haegeli and reviewed by Stefan Ram and Rayees Ahmed.

