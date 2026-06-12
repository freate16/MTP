

# Triggering factors and flooding processes of glacial lake outburst flood at Ranzerio lake

Check for updates

Liye Yang<sup>1,2</sup>, Zhong Lu³ ⊠, Chaoying Zhao⁴ ⊠, Qin Zhang⁴, Xie Hu⁵ & Baohang Wang<sup>6</sup>

The frequency and intensity of glacial lake outburst floods (GLOFs) are increasing with rapid glacier retreat under a warming climate, yet the processes linking triggers and downstream responses remain poorly understood. Here, we investigate the 2013 GLOF at Ranzerio lake in southeastern Tibet using multi-source remote sensing, field observations, and hydrodynamic modeling. A glacier tongue collapse, with an estimated volume of  $3.8 \times 10^6 \, \text{m}^3$ , was identified as the primary trigger of the moraine dam breach. Flood routing simulations with the HEC-RAS 2D model reproduced a peak discharge of  $7930 \pm 18 \, \text{m}^3/\text{s}$  about  $25 \pm 5 \, \text{min}$  after the outburst, capturing flood propagation and geomorphic impacts downstream. The results reveal the multistage process chain of the outburst and highlight the importance of monitoring lake evolution, glacier movement, terrain change, and meteorological conditions for early warning and risk management in glacierized mountain regions.

High Mountain Asia (HMA) is experiencing rapid warming at a rate of 0.32 °C per decade, driving widespread glacier retreat and the expansion of glacial lakes<sup>1</sup>. These changes are contributing to an increased frequency and magnitude of glacial lake outburst floods (GLOFs), which pose significant threats to downstream communities and infrastructure<sup>2–5</sup>. GLOFs can be triggered by both short-term dynamic processes, such as avalanches, landslides, or extreme rainfall, and long-term destabilization mechanisms, including permafrost degradation, dam weakening, and buried ice melt<sup>6,7</sup>.

In the Himalayas, displacement waves from ice or rock avalanches are responsible for nearly half of all moraine-dam failures. Under ongoing climate warming, processes such as the rapid expansion of glacial lakes, accelerated glacier retreat, and growing instability of ice- and permafrost-affected slopes are expected to heighten the likelihood of moraine dam failure, thereby increasing both the frequency and potential magnitude of GLOF hazards<sup>6-8</sup>.

Despite increasing concern among scientists and hazard management authorities about the growing frequency and potential impacts of GLOFs, many events in remote high-altitude regions remain insufficiently documented owing to limited monitoring and poor accessibility<sup>7,9</sup>. These events often involve complex, cascading processes—such as mass movement initiation, wave generation, dam overtopping and erosion, and downstream flooding—whose timing and dynamics depend on the trigger type<sup>4,10</sup>. For example, GLOFs triggered by sudden ice or rock avalanches typically evolve over seconds to minutes, whereas those induced by extreme rainfall may

develop over several hours or days. In this study, we specifically focus on GLOFs triggered by sudden events. By contrast, GLOFs associated with ice-dammed lake drainage can occur over much longer timescales, ranging from days to months, but these are not considered here.

Advancements in remote sensing now allow for the near-continuous monitoring of glacier and lake dynamics, providing valuable information for hazard assessment. Synthetic Aperture Radar (SAR) and optical offset tracking enable the quantification of multi-dimensional glacier motion, offering insights into surge and avalanche precursors<sup>11–14</sup>. Interferometric Synthetic Aperture Radar (InSAR) techniques have been widely applied to detect slope deformation linked to permafrost thaw and ground ice creep<sup>15,16</sup>. Combined with hydrodynamic models such as HEC-RAS, these datasets can help reconstruct flood processes and assess downstream impacts<sup>17–19</sup>. However, the reliability of model outputs is contingent on the quality and resolution of input parameters, highlighting the importance of integrated, multi-source observations.

On 5 July 2013, a GLOF from Ranzerio lake (30.47°N, 93.53°E) in southeastern Tibet caused severe damage to downstream infrastructure and communities. Several studies have investigated this event, with optical imagery, terrain data, and field observations suggesting that a glacier avalanche was the likely trigger<sup>20–22</sup>. However, a comprehensive assessment that combines high-resolution remote sensing and dynamic modeling to fully characterize the flood mechanism, evolution, and post-event glacier response remains lacking. A more comprehensive approach is needed to

<sup>1</sup>College of Civil Engineering, Xiangtan University, Xiangtan, China. <sup>2</sup>Hunan Provincial Key Laboratory of Geomechanics and Engineering Safety, Xiangtan University, Xiangtan, China. <sup>3</sup>Roy M. Huffington Department of Earth Sciences, Southern Methodist University, Dallas, TX, USA. <sup>4</sup>College of Geological Engineering and Geomatics, Chang'an University, Xi'an, China. <sup>5</sup>College of Urban and Environmental Sciences, Peking University, Beijing, China. <sup>6</sup>College of Geography and Oceanography, Minjiang University, Fuzhou, China. ⊠e-mail: zhonglu@mail.smu.edu; cyzhao@chd.edu.cn

capture the interactions between glacier dynamics and dam failure processes. Addressing this gap is critical for improving process-based understanding of GLOF initiation and propagation in paraglacial environments.

This study addresses these knowledge gaps by integrating multi-source satellite remote sensing, high-resolution terrain data, and physically based hydrodynamic modeling to investigate the 2013 Ranzerio GLOF. Specifically, we: (1) quantified temporal changes in glacial lake extent and parent glacier velocity between 2010 and 2021; (2) identified the primary trigger of the lake outburst; (3) reconstructed the flood hydrograph and downstream routing using the HEC-RAS 2D model; and (4) synthesized the GLOF process chain by combining geomorphic, glaciological, and meteorological datasets. This integrated framework enhances understanding of the multistage processes driving GLOFs in paraglacial environments and provides a transferable approach to support hazard assessment and early-warning efforts in High Mountain Asia.

Ranzerio lake is located in Zhongyu Township, Jiali County, south-eastern Tibet, situated above the Nidu Zangpo River (Fig. 1). The study area spans elevations from approximately 4500 m to 6386 m above sea level. It lies within a semi-humid monsoon climate zone, with a mean annual temperature of  $-0.4\,^{\circ}\text{C}$  and approximately 83% of annual precipitation occurring between May and September, largely driven by monsoonal circulation<sup>20</sup>. The region is characterized by a dense distribution of glaciers and glacial lakes. Due to ongoing climate warming, the Qinghai–Tibet Plateau (QTP) has undergone widespread permafrost degradation in recent decades. According to the permafrost distribution map by Zou et al.<sup>23</sup>, the study area is underlain by permafrost (Fig. 1a).

Before the outburst, Ranzerio lake was one of the largest morainedammed glacial lakes in southeastern Tibet, with a surface area of approximately 0.58 km<sup>2</sup>, and measuring about 1.4 km in length and 0.5 km in width<sup>21</sup>. Both the lake and its parent glacier were aligned along a north-south axis. Following the GLOF, two new dammed lakes formed in the Yibu and Luoqiong valleys, with surface areas of approximately 0.13 km<sup>2</sup> and 0.33 km<sup>2</sup>, respectively<sup>20,21</sup>. These lakes were impounded in tributary valleys where GLOF-deposited debris from the main valley blocked the natural drainage pathways, effectively damming the tributary streams. High-resolution satellite imagery reveals substantial geomorphic changes on the valley slopes surrounding Ranzerio lake. Figure 1a shows the spatial coverage of Sentinel-1 SAR data and RapidEye optical imagery used in this study. Figure 1b, c illustrates lake and glacier changes before and after the outburst. In 2010, the glacier and lake areas were 5.28 km<sup>2</sup> and 0.58 km<sup>2</sup>, respectively, and a well-defined drainage channel was visible (Fig. 1b). By 12 September 2013, following the outburst, the glacier area had slightly decreased to 5.13 km<sup>2</sup>, while the lake area had been reduced by 54%, shrinking to 0.25 km2 (Fig. 1c). Inset panels show detailed views of the incised moraine dam and downstream impoundments, as captured by RapidEye imagery and confirmed through field surveys8.

# Results

## Long-term development of the glacier and Ranzerio lake

Long-term changes in Ranzerio lake area and glacier tongue length were quantified from 2010 to 2021. Figure 2 presents the temporal evolution of these features over the study period. Between 2010 and 2012, the lake area expanded modestly from approximately 0.54 km² to 0.58 km². However, following the outburst flood event in July 2013, the lake area decreased sharply to about 0.27 km² by September 2013, indicating a substantial alteration of the glacier-lake system.

Subsequently, the lake area gradually increased, reaching roughly  $0.29\,\mathrm{km^2}$  by 29 October 2021 (Fig. 2b). Concurrently, the glacier tongue exhibited continuous retreat. Prior to the outburst, the tongue length had diminished to 317 m by 2012 and further to 300 m by July 2013. After the event, retreat accelerated, with the glacier tongue length reducing to approximately 128 m by October 2021, corresponding to an average retreat rate of ~22 m/yr (Fig. 2c).

## Triggering factors of Ranzerio lake outburst

Glacier surface velocities were derived using high-resolution RapidEye imagery and the offset tracking method. Annual horizontal glacier velocities from 2010 to 2013 are shown in Fig. 3. In these maps, vector arrows depict flow direction, while color gradients indicate velocity magnitude.

Between 30 October 2010 and 24 October 2011 (Fig. 3a), horizontal glacier velocity was relatively modest. During the subsequent period (24 October 2011 to 5 September 2012; Fig. 3b), a distinct shift in flow pattern occurred. In particular, the glacier tongue on the steep slope exhibited intensified southward motion, with velocities reaching approximately 30 m/yr. From 5 September 2012 to 12 September 2013 (Fig. 3c), the glacier tongue accelerated further, advancing toward the lake at a velocity of ~40 m/yr. Although the observed acceleration of glacier flow could have increased stress at the glacier–lake interface and potentially affected the stability of the proglacial moraine, direct evidence from ice-core stratigraphy or internal deformation measurements is lacking for the 2013 event. Therefore, while glacier velocity may have contributed to moraine destabilization, DEM-derived elevation changes provide the most robust geomorphic evidence for the onset of the GLOF.

RapidEye optical imagery revealed the development of a crevasse between October 2010 and September 2013. In the upper portion of the step icefall, transverse crevasses were consistently observed (Fig. 4), indicating increasing internal glacier stress. Accumulated glacier ice was observed flowing downslope toward the lake basin, cascading over steep sections of the glacier front and partially reaching the lake margin, rather than floating on the lake surface. By September 2012, imagery clearly showed glacier ice resting directly on the lake surface (Fig. 4c). Continued glacier retreat, combined with the progressive enlargement of crevasses, culminated in ice collapse from the tongue into the lake between September 2012 and September 2013. These dynamic instabilities—such as sudden mass movements or ice collapse—are considered triggers for the lake outburst event, potentially generating displacement waves that rapidly increase lake levels and erode the lake dam.

Further, we analyzed terrain changes using high-resolution 5 m TanDEM-X DEMs acquired on 22 April 2013 and 16 September 2013, representing pre- and post-GLOF conditions. Figure 5 illustrates the topographic evolution over this period. Before the outburst, the glacier tongue exhibited steep slopes averaging 39.6° and was characterized by well-developed transverse crevasses (Fig. 5a). Following the GLOF, substantial surface lowering was observed on the glacier tongue and within the lake basin (Fig. 5b). The differential DEM (Fig. 5c) revealed surface elevation losses of up to  $\sim\!50$  m in the steepest portions of the glacier tongue, indicating significant ice collapse. The estimated volume of collapsed glacier ice was approximately  $3.8\times10^6\,\mathrm{m}^3$  based on elevation differences and DEM resolution.

Additionally, the lake surface elevation dropped by approximately 45 m (inset map in Fig. 5c), indicating deep incision of the moraine spillway as a result of rapid drainage. The breach depth was therefore estimated at ~45 m, consistent with previous field assessments<sup>21</sup>. Together, these observations support the hypothesis that an ice collapse from the steep glacier tongue generated displacement waves, which induced a rapid and transient rise in lake level, thereby eroding the moraine dam and ultimately triggering its failure.

## GLOF reconstruction and downstream impact assessment

We reconstructed the 2013 GLOF event at Ranzerio lake to quantify flood depth, flow velocity, and discharge at downstream settlements. Figure 6 illustrates the modeled maximum flow depth and velocity. The hydrograph inset in Fig. 6a shows that the peak discharge at the dam breach ( $\sim$ 7930  $\pm$  18 m³/s) occurred approximately 25  $\pm$  5 min after the breach initiation.

To assess downstream impacts, we analyzed modeled flow parameters at four villages: Rongqingcun (Village 1), Zhaixongcun (Village 2), Bengdacun (Village 3), and Lingngucai (Village 4), located ~26, 28, 35, and 40 km from Ranzerio lake, respectively (Figs. 1 and 7). The modeled flood

Image /page/2/Figure/2 description: A scientific figure composed of three panels, labeled (a), (b), and (c), illustrating changes in a glacial landscape using remote sensing data.

Panel (a) is a regional map centered around Jiali, with coordinates from 93°20'E to 93°40'E and 30°20'N to 30°40'N. It shows a main river with several numbered villages along its banks, and distinguishes between areas of "Seasonally frozen ground" and "Permafrost." The map outlines the coverage areas for "Sentinel-1" (black), "RapidEye" (orange), and the "Study area" (red). A red star marks the "Lake site." An inset map in the top right corner shows the location of the study area on an elevation map of the Tibetan Plateau.

Panel (b) is a satellite image showing a close-up of the study area before a change event. It features a "Glacier" outlined in purple, a "Lake" outlined in blue at the glacier's terminus, and a "Drainage channel" outlined in orange extending from the lake.

Panel (c) is a satellite image of the same area as (b), showing the landscape after the change event. It highlights a newly formed "Dam" (yellow line), a resulting "Flooding area" (reddish-brown outline), and a "New lake" that has formed downstream. Two inset images provide zoomed-in views of the "Dam" and the "New lake."

A comprehensive legend at the bottom defines all the symbols and outlines used across the panels.

Fig. 1 | Spatial coverage of multi-source remote sensing datasets and changes in the glacier and Ranzerio lake (created using ArcGIS 10.4 by the authors).

a Footprints of remote sensing imagery: black rectangle indicates Sentinel-1 SAR

a Footprints of remote sensing imagery: black rectangle indicates Sentinel-1 SAR coverage, orange indicates RapidEye optical imagery, and the red box delineates the study area. Locations of downstream villages are also shown: Rongqingcun (Village

1), Zhaixongcun (Village 2), Bengdacun (Village 3), and Lingngucai (Village 4).  $\bf b$  Pre-GLOF (30 October 2010) and  $\bf c$  post-GLOF (12 September 2013) RapidEye images, illustrating the landscape changes triggered by the 2013 Ranzerio lake GLOF event.

Image /page/3/Figure/2 description: A scientific figure illustrating the changes in Ranzerio lake and its associated glacier tongue from 2010 to 2021, divided into three parts: (a), (b), and (c).

Part (a) displays a series of nine satellite images of the lake. The top row, labeled "Before," shows images from 2010/10/30, 2011/10/24, and 2012/9/5, where the lake is large. The next two rows, labeled "After," show images from 2013/9/12, 2016/12/13, 2017/8/24, 2019/9/26, 2020/8/25, and 2021/10/29. The 2013 image shows a significantly smaller lake with ice debris, corresponding to a major event. Subsequent images show the lake slowly recovering but not reaching its pre-2013 size.

Part (b) is a line graph plotting "Lake area (km²)" against "Year" from 2010 to 2022. The lake area increases from about 0.53 km² in 2010 to a peak of about 0.59 km² in 2012. A sharp drop, labeled "2013 event," occurs in 2013, with the area decreasing to about 0.27 km². After 2013, the lake area shows a slight, gradual increase, reaching about 0.30 km² by 2022.

Part (c) is a line graph plotting "Glacier tongue (m)" against "Year" from 2010 to 2022. The graph shows a consistent decrease in the length of the glacier tongue over the period. It starts at over 600 m in 2010 and drops to approximately 120 m by 2022. A label "2013 event" is placed near the data points for 2012 and 2013, indicating a continued retreat during that time.

Fig. 2 | Time series of Ranzerio lake and the glacier tongue from 2010 to 2021 (created using ArcGIS 10.4 and Origin 2021 by the authors). a Spatiotemporal evolution of the glacier tongue and lake extent. b Temporal changes in lake area. c Temporal changes in glacier tongue length.

hydrographs and flow depths at these sites are shown in Fig. 7 and summarized in Table 1.

Results indicate a progressive attenuation of both peak discharge and maximum flow depth with increasing downstream distance. At village 1, the peak discharge was  $\sim 2623 \pm 7 \text{ m}^3/\text{s}$ , arriving  $89 \pm 7 \text{ min}$ 

after the breach, with a flow depth of  $\sim$ 7.7  $\pm$  0.6 m. At village 2, the peak discharge decreased to  $\sim$ 2485  $\pm$  14 m³/s, occurring at 101  $\pm$  6 min postbreach, with a depth of  $\sim$ 5.5  $\pm$  0.1 m. At village 3, the discharge further declined to  $\sim$ 1056  $\pm$  5 m³/s, reaching the site at 177  $\pm$  7 min, with a depth of  $\sim$ 4.3  $\pm$  0.1 m. At village 4, the peak discharge was  $\sim$ 242  $\pm$  2 m³/s,

Image /page/4/Figure/2 description: A four-panel figure illustrating glacier horizontal velocity from 2010 to 2013. The three main panels, labeled (a), (b), and (c), show 3D topographical maps of a glacier and the adjacent Razerio Lake during different time periods. The glacier's surface is covered with colored vectors indicating the direction and speed of ice flow. The fourth panel provides a legend. Panel (a) covers the period 2010/10/30-2011/10/24. Panel (b) covers 2011/10/24-2012/9/5. Panel (c) covers 2012/9/5-2013/9/12. The legend in the bottom right indicates that a reference red vector represents a velocity of 60 meters per year (m/yr). Below this, a color bar for 'Horizontal Velocity (m/yr)' shows a scale from 0 (blue) to 60 (red), with labeled increments of 10.

Fig. 3 | Glacier horizontal velocities from 2010 to 2013 (created using Origin 2021 by the authors). a 30 October 2010 to 24 October 2011. b 24 October 2011 to 5 September 2012. c 5 September 2012 to 12 September 2013. Vector arrows indicate flow direction, and color shading represents the magnitude of horizontal velocity.

arriving  $332 \pm 9$  min after the event, with a maximum modeled depth of  $\sim 2.2 \pm 0.2$  m.

These results demonstrate the rapid onset and high magnitude of the initial flood wave, followed by progressive attenuation downstream. Such dynamics underscore the need for rapid detection of upstream triggers, such as ice collapse, and for coordinated early warning systems coupled with targeted risk-reduction measures. Practical applications include continuous remote sensing of glacier and lake conditions, real-time hydrological monitoring, and automated alert systems to inform downstream communities and guide emergency response planning.

## Deposition estimation and uncertainty in flood simulation

Due to the absence of direct post-event water depth measurements, the simulated GLOF inundation extent was validated against observations from high-resolution RapidEye imagery. The flood extent was delineated from two 5 m resolution RapidEye scenes acquired on 12 September 2013 (Fig. 8a). Comparison shows that the observed inundation area was 3.67 km², while the simulated extent covered 3.89 km², representing a relative difference of ~6.0%. Likewise, the modeled new lake area (0.339 km²) closely matched field-derived measurements (0.330 km²)<sup>8,20</sup>, with a deviation of only ~2.7%. These small differences fall within the expected uncertainty range and indicate that the hydraulic model is capable of reliably reproducing the spatial extent of flooding.

Owing to the limited spatial coverage of the available DEM datasets, deposition and erosion were analyzed only within the overlapping areas (Fig. 8b). The DEM difference analysis revealed a total sediment deposition of  $48.06 \pm 0.004 \, \text{Mm}^3$  and a total erosion of  $25.54 \pm 0.005 \, \text{Mm}^3$ , resulting in a net volumetric change of  $22.52 \, \text{Mm}^3$  within the analyzed area. It should be noted that these estimates here are limited to the DEM coverage and do not represent the total downstream sediment caused by the flood.

Flow dynamics during GLOF events are often complex, involving transitions from clear-water to sediment-laden or debris flows with possible

non-Newtonian rheologies<sup>5,24</sup>. Due to the absence of detailed sediment data for this event, we adopted a clear-water hydraulic model following established approaches<sup>5,18,25</sup>. While this simplification may underestimate sediment-transport effects, it provides credible estimates of inundation extent, flooding discharge, and timing given the available dataset.

## Glacier movement after the lake outburst

To investigate the post-outburst dynamics of the parent glacier, we derived glacier displacement time series using the PO-MSBAS method applied to Sentinel-1 SAR imagery acquired between 2017 and 2021. Azimuth displacements, representing motion along the satellite flight path, were used to approximate north-south glacier movement, consistent with the glacier's primary orientation <sup>12,26</sup>.

Figure 9 presents the azimuth displacement time series, revealing a persistent southward glacier motion with an average velocity of  $\sim$ 6 m/yr in the accumulation zone. At point G (Fig. 9i), the cumulative LOS displacement reached  $\sim$ 7 m, while the total azimuth displacement over the 4-year period amounted to  $\sim$ 20 m, indicating sustained glacier flow following the outburst event.

# **Discussion**

The 2013 Ranzerio lake outburst can be understood within the broader framework of moraine-dammed GLOF triggering mechanisms<sup>27–31</sup>. Such events are commonly initiated by external disturbances—such as ice or rock collapse, mass movements, or displacement waves—that erode the dam and trigger its failure. Our evidence indicates that the Ranzerio outburst was most likely driven by a sudden ice collapse and the subsequent generation of high-energy displacement waves.

High-resolution glacier velocity mapping revealed sustained acceleration of the glacier tongue, from ~30 m/yr in 2011–2012 to ~40 m/yr in 2012–2013, accompanied by crevasse expansion and downslope extension toward the lake margin. By late 2012, the glacier

Image /page/5/Figure/2 description: A four-panel figure displaying satellite images of a glacier tongue from 2010 to 2013, illustrating changes over time. Each panel is labeled with a letter and a date.

- Panel (a), dated 2010/10/30, shows the glacier with a red flag pointing to a feature labeled "crevasse". A white dashed line indicates the glacier's edge, labeled "Glacier retreat".
- Panel (b), dated 2011/10/24, shows the same area a year later, with the "crevasse" still marked and the glacier's edge having retreated further back.
- Panel (c), dated 2012/9/5, is a false-color image highlighting the "crevasse" with a red flag.
- Panel (d), dated 2013/9/12, shows a significant "break" in the glacier, indicated by red text and four red arrows pointing to the fractures.

All panels are marked with coordinates 30°29' and 93°32' and include a scale bar for 0.05 km. A partial caption at the bottom reads: "glacier crevasse on its tongue from 2010 to 2013 (created using ArcGIS September 2013. Note: The zoomed-in sections may appear less sharp du...".

Fig. 4 | Glacier crevasse on its tongue from 2010 to 2013 (created using ArcGIS 10.4 by the authors). a RapidEye image on 30 October 2010. b RapidEye image on 24 October 2011. c RapidEye image on 5 September 2012. d RapidEye image on 12

September 2013. Note: The zoomed-in sections may appear less sharp due to the original PlanetScope spatial resolution and local magnification used to highlight details.

front was in direct contact with the lake surface. Similar pre-failure acceleration patterns have been observed in other ice-avalanche-induced GLOFs<sup>32-34</sup>, where progressive destabilization often precedes catastrophic collapse. DEM differencing between April and September

2013 revealed surface lowering of up to ~50 m on the steep glacier tongue, corresponding to an estimated ice loss volume of ~3.8  $\times$  10  $^6$  m³. This sudden collapse likely generated displacement waves capable of overtopping the moraine dam  $^{35\text{--}37}$ .

Image /page/6/Figure/2 description: A figure composed of three maps and one line graph, illustrating the topographical changes before and after a Glacial Lake Outburst Flood (GLOF). The maps are located at approximately 93°32' E longitude and between 30°28' and 30°29' N latitude. Map (a), labeled "Pre-GLOF", shows a grayscale topographical view with a "Steep Region" and "Crevasses" indicated. A large, textured area is outlined in blue. Map (b), labeled "Post-GLOF", shows the same region after the event, with the previously blue-outlined area now outlined in pink and appearing smoother. Map (c) displays the "Elevation change (m)" using a color scale. The area of change is highlighted, showing a significant loss of elevation (colored yellow, orange, and red), with a total volume change of 3.8x10^6 m^3 noted. The legend for elevation change ranges from -50 to >50 meters. A "Breach Dam" is indicated at the lower end of the affected area. Below the maps, a line graph plots "Dam breach depth (m)" on the y-axis versus "Distance (km)" on the x-axis. The y-axis ranges from 0 to 45 m, and the x-axis from 0.00 to 0.25 km. The blue line on the graph shows the depth profile of the breach, starting at 0, rising to a peak of approximately 43 meters at a distance of about 0.12 km, and then decreasing sharply.

Fig. 5 | Terrain changes of the glacier tongue and Ranzerio lake before and after the GLOF, derived from TanDEM-X datasets (created using ArcGIS 10.4 and Origin 2021 by the authors). a Pre-GLOF terrain on 22 April 2013. b Post-GLOF terrain on 16 September 2013. c Elevation difference map showing terrain changes

before and after the event, highlighting the ice collapse that occurred from the lower glacier tongue and the incision of the moraine dam. The inset map illustrates the dam breach, with an incision depth of  $\sim\!45$  m.

Meteorological analysis based on ERA5 reanalysis data further highlighted anomalous conditions in early July 2013, as shown in Fig. 10. Mean daily June–July temperatures over 2004–2013 ranged from 4.19–6.54 °C and 6.20–8.52 °C, respectively. Corresponding mean daily precipitation also fluctuated notably, with June averages between ~4.50 mm and 7.28 mm, and July averages between 4.94 mm and 8.48 mm. Cumulative June–July totals varied from ~293.5 mm to 481.2 mm, with the 2013 value (423.6 mm) exceeding the median but remaining below the decadal maximum. Using the 2004–2012 baseline, the 95th percentile thresholds for daily precipitation and temperature were 11.68 mm and 8.83 °C, respectively <sup>38</sup>. Importantly, the days immediately preceding the GLOF outburst included both an extreme high-temperature event (5 July 2013) and an extreme precipitation event (3 July 2013), each surpassing these thresholds. These conditions likely enhanced meltwater input and hydrological loading on the proglacial lake, thereby exacerbating dam instability <sup>29,39,40</sup>.

Integrating the geomorphological, glaciological, and meteorological evidence, we propose a multi-stage process chain, as shown in Fig. 11: (1) long-term glacier retreat and steepening of the ice front above the lake increased susceptibility to collapse; (2) short-term metrological anomalies in early July 2013 accelerated destabilization; (3) a sudden ice collapse generated displacement waves, rapidly elevating lake levels and imposing erosion on the moraine dam; and (4) overtopping and subsequent erosion breached the dam to a depth of ~45 m, releasing the lake volume as a high-magnitude flood that caused downstream geomorphic change and sediment redistribution.

This study provides a comprehensive reconstruction of the 2013 Ranzerio GLOF by integrating geomorphic, glaciological, and meteorological datasets with high-resolution remote sensing and physically based hydrodynamic modeling. Differential DEM analysis revealed pronounced surface lowering of up to  $\sim\!50$  m on the steep glacier tongue, corresponding to an ice-collapse volume of  $\sim\!3.8\times10^6\,\mathrm{m}^3$ . This ice collapse acted as the primary trigger, generating displacement waves that abruptly raised lake levels and imposed extreme erosion on the moraine dam. Hydrodynamic simulations constrained by field-derived breach geometry successfully reproduced the outburst process, estimating a peak discharge of  $7930\pm18\,\mathrm{m}^3/\mathrm{s}$ , a breach depth of  $\sim\!45\,\mathrm{m}$ , and an inundation extent closely matching RapidEye observations (relative difference  $\sim\!6\%$ ). These quantitative results validate the reliability of our reconstruction.

By explicitly linking the multistage process chain—from accelerated glacier flow and tongue destabilization, through ice collapse and displacement wave generation, to moraine-dam breach and downstream flooding—this study identifies specific indicators that can be monitored for early warning. Observables such as ice-front acceleration, sudden ice mass movement, and dam erosion provide actionable signals for hazard detection. Furthermore, the reconstruction of erosion and deposition volumes along the flood path offers quantitative input for hazard mapping and risk assessment, allowing identification of areas most susceptible to inundation and sediment impact.

Beyond the event-specific insights, the integrated methodological framework—combining optical and SAR remote sensing, DEM

Image /page/7/Figure/2 description: A figure with two maps, labeled (a) and (b), and an inset graph, illustrating the characteristics of the Ranzerio lake outburst flooding. 

Map (a) displays the 'Maximum Flow depth (m)' in a river valley. The flood path is colored on a scale from light blue (0-4 m) to dark pink (36-40 m). The map includes latitude and longitude coordinates, with four numbered green circles (1, 2, 3, 4) marking locations along the river downstream from Ranzerio lake.

Map (b) shows the 'Maximum Flow velocity (m/s)' for the same event and location. The flow velocity is represented by a color scale from dark red (0-2 m/s) to dark blue (18-20 m/s).

An inset graph plots 'Discharge (m³/s)' on the y-axis against 'Time (min)' on the x-axis. A red line shows the discharge hydrograph, which peaks sharply. An annotation indicates the peak discharge is 7930 m³/s at 25 minutes. Both maps include a scale bar showing 0, 2, and 4 km.

Fig. 6 | The maximum flowing depth and velocity of Ranzerio lake outburst flooding (created using ArcGIS 10.4 and Origin 2021 by the authors). a The maximum flooding depth. b The maximum flow velocity.

differencing, ERA5-based meteorological reanalysis, and hydraulic modeling—provides a transferable approach for high-mountain regions. This framework supports the development of early warning systems, targeted hazard mapping, and quantitative risk assessment, contributing to climate adaptation planning in other rapidly changing cryospheric environments.

Several limitations in this study should be acknowledged. First, due to the absence of direct post-event field measurements—such as wash limits or downstream water surface elevation profiles—it was not possible to validate modeled water surface profiles against observed data. This constrains our ability to comprehensively evaluate model performance in reproducing

downstream flow dynamics beyond the inundation extent<sup>10</sup>. To partially address this limitation, we compared the modeled inundation area with high-resolution satellite imagery, which provided reliable spatial delineation of the flood extent. Future post-event field campaigns should therefore prioritize the collection of wash limits, water surface elevations, and sediment deposition profiles to enhance model calibration and to better constrain flood dynamics in similar GLOF events.

Second, the sediment erosion and deposition analysis derived from DEM differencing provided only a partial estimate of geomorphic change associated with the 2013 Ranzerio GLOF. However, these estimates capture

Image /page/8/Figure/2 description: A figure containing four line graphs, labeled (a) Village1, (b) Village2, (c) Village3, and (d) Village4. Each graph plots Flow depth (m) on the left y-axis and Discharge (m³/s) on the right y-axis against Time (min) on the x-axis, which ranges from 0 to 1000. The legend indicates that a blue line with a shaded uncertainty band represents Flow depth, and a red line with circle markers represents Discharge. In graph (a) Village1, both flow depth and discharge show a sharp, immediate peak, with flow depth reaching about 8.5 m and discharge reaching about 2700 m³/s, before gradually decreasing. In graph (b) Village2, the pattern is similar, with flow depth peaking around 5.5 m and discharge peaking around 2700 m³/s. In graph (c) Village3, the peaks are lower and occur slightly later, with flow depth reaching about 4.5 m and discharge about 1100 m³/s. In graph (d) Village4, the rise is much more gradual, with flow depth peaking around 2.5 m and discharge around 600 m³/s at approximately 300 minutes.

Fig. 7 | Flooding discharge and depth of Ranzerio lake at four downstream villages (created using ArcGIS 10.4 and Origin 2021 by the authors). a–d Flow depth and discharge at four downstream villages, respectively.

Table 1 | GLOF peak discharges and flow depths at four downstream villages

| Routing location | Time (min) | Maximum discharge (m³/s) | Maximum flow depth(m) |
|------------------|------------|--------------------------|-----------------------|
| Village1         | $89 1 7$  | $2623 1 7$              | $7.7 1 0.6$          |
| Village2         | $101 1 6$ | $2485 1 14$             | $5.5 1 0.1$          |
| Village3         | $177 1 7$ | $1056 1 5$              | $4.3 1 0.1$          |
| Village4         | $332 1 9$ | $242 1 2$               | $2.2 1 0.2$          |

only a fraction of the total sediment budget, as extensive downstream reaches were not covered by the available DEMs. A more complete understanding of GLOF sediment budgets and flow dynamics therefore, requires extending DEM differencing to wider downstream areas. Moreover, coupling such geomorphic analyses with detailed sedimentological investigations of flood deposits will be essential for constraining flow rheology, sediment transport mechanisms, and depositional patterns<sup>2,41</sup>. This integration will provide critical insights into the physical processes governing GLOFs and improve the predictive capability of hazard assessments in high-mountain environments.

Finally, while this study focused on the triggering mechanisms and flooding processes of the 2013 Ranzerio GLOF, future research should also examine hillslope dynamics surrounding proglacial lake basins. The valley slopes around Ranzerio lake are underlain by permafrost, and ongoing regional permafrost degradation driven by climatic warming may exacerbate slope instability and surface deformation<sup>5</sup>. Remote sensing techniques, particularly InSAR, offer effective means to monitor

and quantify such ground movements in remote, data-scarce high-mountain environments <sup>18,42,43</sup>. Characterizing the temporal and spatial evolution of hillslope deformation could improve assessments of potential hazards threatening moraine dam stability or triggering future outburst floods. Integrating hillslope monitoring with hydrological and glaciological datasets, therefore, represents a promising approach for enhancing early warning systems and advancing comprehensive hazard evaluations in glacierized regions under climate change.

# **Methods**

To investigate the 2013 Ranzerio lake GLOF event, we developed an integrated processing workflow combining multi-source satellite remote sensing data with physically based hydrodynamic modeling. The datasets used are summarized in Table 2.

Four high-resolution RapidEye optical images (5 m spatial resolution) acquired between 2010 and 2013 were used to delineate lake boundaries and estimate horizontal glacier surface velocities prior to the outburst. An additional five RapidEye images (2016–2021) were analyzed to track postevent changes in glacier extent and lake area. Sentinel-1 SAR imagery (2017–2021) was further used to monitor glacier motion after the event. To quantify terrain changes and evaluate potential triggering mechanisms, we employed two TanDEM-X digital elevation models (5 m resolution) acquired on 22 April and 16 September 2013. Elevation differencing between the two DEMs enabled the identification of pre- and post-GLOF surface changes.

Meteorological forcing was characterized using daily precipitation and temperature data from the ERA5 reanalysis<sup>44</sup>. Specifically, we used the post-processed daily statistics from 1940 to the present, available from the

Image /page/9/Figure/2 description: A multi-panel figure comparing flooded areas and downstream elevation changes in a mountainous, snow-covered region. The figure is composed of four main panels labeled (a), (a1), (a2), and (b).

Panel (a) is an overview map showing a river valley. A legend indicates three types of areas: "Lake area" (light purple), "Mapped inundation area" (magenta dashed line), and "Simulated inundation area" (blue dashed line). The mapped and simulated areas follow the path of a flood down the valley. The map includes latitude and longitude coordinates and a 1 km scale bar.

Panel (a1) is a zoomed-in view of the upper part of the flood path, showing the "Maximum Flow depth (m)". A color scale indicates depths from 0-4 m (light blue) to 24-28 m (dark purple).

Panel (a2) is a zoomed-in view of the lower part of the flood path, also showing the maximum flow depth. A specific area is highlighted with a dashed box and labeled "0.339 km²". A further magnified view of this area shows a lake-like feature labeled "0.330 km²".

Panel (b) shows the "Elevation change (m)" along the same flood path. A color scale ranges from red (-50 to -40 m) to blue (90 to 100 m), representing erosion and deposition, respectively. The upper reaches of the path are shown in red, orange, and yellow, while the lower, wider area is shown in green and blue.

Fig. 8 | Comparison of flooded areas and downstream elevation changes (created using ArcGIS 10.4 by the authors). a Flood inundation area between simulated and mapped results. b Elevation changes occur at the downstream due to limited DEM coverage.

Copernicus Climate Data Store (https://cds.climate.copernicus.eu/datasets/derived-era5-single-levels-daily-statistics). This globally consistent dataset assimilates a wide range of observations into a state-of-the-art atmospheric model, providing ~0.25° (~28 km) spatial resolution and daily temporal resolution. For this study, daily total precipitation and air temperature from June to July 2004–2013 were extracted for the study area to characterize meteorological conditions leading up to the GLOF.

In the absence of pre-event SAR acquisitions, glacier surface velocities for 2010–2013 were estimated using optical image correlation applied to the RapidEye dataset. Ice collapse volume was quantified from TanDEM-X elevation changes and subsequently used to inform the GLOF process reconstruction. The outburst flood was simulated using the HEC-RAS 2D hydrodynamic model, incorporating breach parameters derived from DEM differencing and previous field studies. HEC-RAS was selected for its proven capability in dam-break and flood routing simulations, as well as its ability to represent unsteady flow dynamics in complex terrain 5.18,19.

## Lake mapping using optical imagery

To map the temporal evolution of the Ranzerio lake and minimize classification uncertainties, we employed high-resolution RapidEye multispectral imagery from 2010 to 2021. To ensure that seasonal

hydrological fluctuations did not confound interannual changes in lake area, imagery was deliberately selected from the same season each year. This seasonal consistency is a widely recognized strategy in glacial lake monitoring, as it reduces the influence of transient factors such as snowmelt or seasonal ice cover, thereby improving the comparability of multi-year measurements 45,46.

Lake boundaries were delineated using a semi-automated approach based on the Normalized Difference Water Index (NDWI). For images acquired under conditions of low solar illumination or partial snow/ice cover, manual editing was conducted to correct misclassified pixels, guided by careful visual inspection. The final lake polygons were further cross-checked against historical optical imagery and existing glacier lake inventories for the Tibetan Plateau 16,47 to ensure both spatial accuracy and temporal consistency. This integrated approach provided a robust time series of glacial lake outlines, suitable for quantifying area changes across the study period.

## Glacier velocity using optical and SAR images

To quantify glacier surface displacement before and after the 2013 Ranzerio lake outburst, we applied offset tracking techniques to both optical and SAR datasets. Annual glacier velocities from 2010 to 2013

Image /page/10/Figure/2 description: A figure composed of nine panels, labeled (a) through (i), illustrating glacier displacement from 2017 to 2020. Panels (a) through (h) are a time series of 3D topographic maps showing the cumulative displacement of a glacier near Razerio Lake. The dates for the maps are: (a) 2017/03/21, (b) 2018/07/02, (c) 2018/12/29, (d) 2019/07/09, (e) 2019/12/24, (f) 2020/04/22, (g) 2020/07/15, and (h) 2020/10/31. A color scale at the bottom indicates cumulative displacement in meters (m), ranging from -15 (purple) to +15 (red), with 0 being green. Over time, the glacier area on the maps changes from green to blue and purple, indicating increasing negative displacement. Panel (i) is a scatter plot titled 'Glacier displacement (m)' versus 'Year'. The y-axis ranges from -20 to 0 m, and the x-axis ranges from 2017 to 2021. The plot shows two data series: AZI (red dots) and LOS (blue dots). Both series show a downward trend over time. The AZI displacement starts near 0 in 2017 and decreases to approximately -15 m by late 2020. The LOS displacement also starts near 0 in 2017 and decreases to about -7 m by late 2020.

Fig. 9 | Glacier displacement time series from 2017 to 2020 (created using ArcGIS 10.4 and Origin 2021 by the authors). a-h Displacement on 21 March 2017, 2 July 2018, 29 December 2018, 9 July 2019, 24 December 2019, 22 April 2020, 15 July 2020,

31 October 2020, respectively. The colors represent the cumulative displacement. i The two-dimensional displacement time series on point G.

Image /page/10/Figure/5 description: Fig. 10 | Daily temperature, daily precipitation, and cumulative precipitation at Ranzerio site between June and July from 2004 to 2014 (created using Python 3.12 by the authors). Daily temperature is shown in blue solid lines, daily precipitation is shown in gray bars, and cumulative precipitation is shown in gray dashed lines.

Image /page/10/Figure/6 description: A multi-axis graph plots meteorological data from January 1, 2004, to January 1, 2014. The x-axis represents the date. The primary y-axis on the left, labeled 'Daily Precipitation (mm)', ranges from 0 to 25. The secondary y-axis on the right has two scales: 'Temperature (°C)' from -5 to 15, and 'Cumulative Precipitation (mm)' from 0 to over 5000. The graph displays four data series as indicated by the legend: a red dashed line for 'Event: 2013-07-5', gray bars for 'Daily Precipitation (mm)', a solid blue line for 'Temperature (°C)', and a dashed black line for 'Cumulative Precipitation (mm)'. The daily precipitation is shown as dense vertical bars, exhibiting an annual pattern. The temperature follows a cyclical annual pattern, peaking in the middle of each year. The cumulative precipitation shows a sawtooth pattern, resetting to zero at the beginning of each year and increasing throughout the year. A specific event on July 5, 2013, is marked with a vertical red dashed line, corresponding to a high daily precipitation event shown as a red bar.

were derived using four high-resolution (5 m) ortho-rectified RapidEye images. Displacements were estimated using the phase correlation-based image matching algorithm implemented in the COSI-Corr software package, a robust method for large-scale glacier motion analysis<sup>48–51</sup>.

The image pairs were processed by computing phase differences in the Fourier domain to detect sub-pixel offsets. Matching window sizes ranging from 32 to 256 pixels and a step size of 2 pixels were tested to optimize correlation quality. A signal-to-noise ratio (SNR) threshold of 0.9 was used to filter out low-confidence matches. Displacement fields in the east–west

and north–south directions were produced, followed by noise suppression using gross error removal, non-local means filtering, and polynomial surface fitting (deramping). Horizontal surface velocities were obtained by combining the displacement components and normalizing by the acquisition interval. Given the 5 m pixel resolution, the expected measurement precision was approximately 0.25–0.5 m<sup>48</sup>.

For the post-outburst period (2017–2021), glacier motion was estimated using Sentinel-1 SAR data processed with the GAMMA software. Pixel Offset tracking was performed using a matching window of  $128 \times 128$  pixels in range and azimuth directions, and a search step of  $4 \times 1$  pixels. A normalized cross-correlation threshold of 0.3 was applied to exclude unreliable offset vectors<sup>12</sup>. The offset time series were then integrated using the Multi-dimensional Small Baseline Subset (MSBAS) method  $^{11,12}$ . Then, we used the Pixel Offset tracking MSBAS (PO-MSBAS) method to retrieve glacier displacement time series in both azimuth and line-of-sight (LOS) directions by singular value decomposition (SVD).

## Terrain change using TanDEM-X data

To assess terrain changes associated with the Ranzerio lake outburst, we employed two TanDEM-X digital elevation models (DEMs) with a spatial resolution of 5 m, acquired on 22 April 2013 and 16 September 2013. DEM differencing is a widely used approach for quantifying surface elevation changes over time<sup>52,53</sup>. However, accurate estimation of elevation change requires prior co-registration of the DEMs to eliminate horizontal and vertical misalignments that can introduce systematic biases.

We adopted the gradient-based co-registration method proposed by Ye et al.<sup>54</sup>. In this approach, pixel-wise oriented gradients were extracted from the reference DEM (April 2013) and compared to the target DEM (September 2013) using the fast Fourier transform (FFT) to compute a similarity metric in the frequency domain. Control points (CPs) were identified through this similarity analysis, and a transformation was applied to align the target DEM to the reference. The co-registered DEMs were then differenced to produce an elevation change map.

Image /page/11/Picture/7 description: A diagram illustrates the process of a glacial lake outburst flood. On the left, a large piece of ice, labeled "Ice collapse ~3.8x10^6 m^3", is shown breaking off from a "Glacier" and falling into a "Lake" below. The impact creates "Displacement waves" in the lake. These waves travel across the lake and wash over a natural dam, an event labeled "Dam overtopping". The water that spills over the dam flows down the other side, resulting in "Flooding". A sun is depicted in the upper right corner of the diagram.

**Fig. 11** | Schematic diagrams showing the likely mechanisms of the disaster chains of the GLOF event for Ranzerio lake (created using Python 3.12 by the authors).

The elevation difference dataset was used to detect geomorphic changes in the glacier and surrounding slopes, supporting the analysis of surface deformation patterns. GLOF triggering zones were delineated where elevation loss exceeded 5 m and local slope gradients were steeper than 30°, following established approaches<sup>10,55</sup>. These elevation changes also served as input for assessing the dam breach parameters, supporting downstream hydrodynamic modeling of the outburst event. Moreover, to evaluate geomorphic changes caused by the 2013 Ranzerio GLOF, we performed DEM differencing between pre- and post-event high-resolution DEMs within their common overlapping spatial extent<sup>41</sup>. We calculated sediment volumes by multiplying pixel area by elevation change values and summing over deposition and erosion zones separately. Due to the limited spatial coverage of DEM data, these volume estimates represent only a partial sediment budget of the GLOF pathway and do not capture all downstream effects.

## **GLOF simulation using HEC-RAS model**

The hydrodynamic simulation of the 2013 Ranzerio lake outburst was performed using HEC-RAS, a widely used two-dimensional hydraulic modeling software developed by the U.S. Army Corps of Engineers. The 2D flow module in HEC-RAS solves the shallow water equations, which are commonly applied for simulating unsteady surface water flows<sup>17–19</sup>. Key model inputs include digital elevation data, lake volume before the outburst, dam breach parameters, Manning's roughness coefficients, and upstream/downstream boundary conditions.

To ensure accurate representation of pre-flood topography, we employed 5 m resolution TanDEM-X data acquired on 22 April 2013, reflecting terrain conditions prior to the outburst event. The pre-event lake area and volume were derived from high-resolution RapidEye imagery and previously published field observations<sup>21,22</sup>. Before the outburst, the lake covered approximately 0.58 km² with an estimated volume of  $\sim 11.7 \times 10^6$  m³ by Peng et al. <sup>22</sup>. To estimate dam breach parameters, we applied Froehlich's empirical equations <sup>56</sup>, which are widely used in outburst flood modeling due to their relatively low uncertainty. The equation provides estimates of dam failure time ( $T_f$  in hours) and peak discharge ( $Q_p$  in  $m^3/s$ ):

$$\begin{cases}
T_f = 0.00254(V_w)^{0.53}(h_b)^{-0.9} \\
Q_p = 0.607(V_w)^{0.295}(h_w)^{1.24}
\end{cases}$$
(1)

where  $h_b$  is the dam breach depth (in m),  $V_w$  is the lake volume above  $h_b$  (in m³),  $h_w$  is the depth of water above the breach dam (in m).

The released flood volume was calculated by comparing the lake volume before and after the outburst event. Post-outburst lake depths were obtained from bathymetric measurements collected by an uncrewed automated sampling and monitoring vessel<sup>8</sup>. Lake volume after the GLOF was calculated by summing the product of lake depth and pixel area across the lake extent, as expressed in Eq. (2):

$$V = D_i \times R_i^2 \tag{2}$$

where  $D_i$  represents the depth for each individual pixel,  $R_i$  represents the corresponded pixel size of 5 m.

Table 2 | Summary of multi-source data used in the study

| Data             | RapidEye                                                                                                   | TanDEM-X                         | Sentinel-1       | Precipitation                                         | Temperature |
|------------------|------------------------------------------------------------------------------------------------------------|----------------------------------|------------------|-------------------------------------------------------|-------------|
| Used bands       | Red/Green/Blue/Near infrared                                                                               | X                                | C                | -                                                     | -           |
| Pixel spacing    | 5 m                                                                                                        | 5 m                              | 2.3 m × 14.0 m   | 0.25°                                                 | 0.25°       |
| Numbers          | 9                                                                                                          | 2                                | 115              | -                                                     | -           |
| Acquisition date | 2010/10/30;2011/10/24; 2012/09/05;2013/09/12; 2016/12/<br>13;2017/08/24; 2019/09/26;2020/08/25; 2021/10/29 | 2013/04/22; 2013/09/16           | 2017–2021        | 2004–2013                                             |             |
| Purpose          | Glacier velocity before the lake outburst; Area changes before and after the lake outburst                 | Elevation changes; GLOF modeling | Glacier velocity | Meteorological factors analysis for the lake outburst |             |

Fig. 12 | Lake depth of Ranzerio lake after the outburst event (created using ArcGIS 10.4 and Origin 2021 by the authors). a The distribution of lake depth. b The lake depth along the profile.

Image /page/12/Figure/3 description: The image consists of two parts, labeled (a) and (b), illustrating the bathymetry of a lake.

Part (a) is a bathymetric map of the lake. The map uses a color scale to represent lake depth, ranging from blue for 0 meters to red for 40 meters. Blue contour lines are drawn at 5-meter intervals. A dashed black line labeled "Profile" runs longitudinally through the lake. The map includes coordinates 30°28'30" and 93°32", a north arrow, and a scale bar indicating 0.2 km.

Part (b) is a line graph showing the depth profile along the dashed line from part (a). The x-axis represents "Distance (km)" from approximately 1.2 to 0, and the y-axis represents "Depth (m)" from 0 to 40, with depth increasing downwards. The blue line shows that the lake depth starts at 0 m, increases sharply, fluctuates in the deepest section between approximately 28 m and 35 m, and then gradually becomes shallower, reaching a depth of about 5 m at a distance of 1.2 km.

Figure 12 shows the spatial distribution of lake depth after the outburst and depth variations along a selected profile. The maximum lake depth reached approximately 36 m, with depths exceeding 20 m mainly occurring between 0.05 km and 0.15 km along the profile. Using this approach, the post-outburst lake volume was estimated at  $\sim\!3.8\times10^6$  m³. By subtracting this from the pre-outburst volume, the total released flood volume was calculated to be approximately 7.9  $\times$  10  $^6$  m³. We did not explicitly include the additional water volume potentially contributed by mass movements in the simulation because reliable knowledge of collapse dynamics is limited. Moreover, it is difficult to assess how well the lake model can represent the complex interaction between the collapse and the lake  $^{77,58}$ . As a result, our estimates of flood volume and peak discharge should be regarded as conservative values.

In the GLOF simulations, Manning's roughness coefficients were assigned according to land cover and vegetation types, with typical values ranging from 0.025 to 0.033 and an average value of 0.03<sup>5,17</sup>. Accordingly, a roughness coefficient of 0.03 was applied to the unvegetated downstream channel. The model employed the full momentum equations to simulate two-dimensional, unsteady flow, using a time step of 1 s and a total simulation duration of 24 h. Upstream boundary conditions were derived from the estimated dam breach hydrographs, while downstream boundary conditions were specified as a normal water depth gradient of 0.01 m/m<sup>17,19</sup>. Thus, the 2013 Ranzerio lake outburst GLOF was reconstructed using observed breach parameters and released lake volume to ensure realistic simulation results. Additionally, uncertainties in the simulation parameters, lake bathymetry, model parameters, and flow transitions inevitably propagate into flood outputs<sup>5</sup>. Given the challenges in directly constraining

these parameters, we assessed the uncertainty in the hydraulic reconstruction by quantifying the spatial variability of modeled peak discharge and flow depth. Specifically, we calculated the standard deviations of these variables across neighboring grid cells surrounding downstream villages<sup>59</sup>. This approach yields a representative range of discharge and depth, reflecting the robustness and sensitivity of the hydraulic reconstruction. Furthermore, the simulated inundation extent was compared against flood mapping derived from RapidEye imagery to evaluate model uncertainty.
