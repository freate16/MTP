

## **ABSTRACT**

Glacial Lake Outburst Flood (GLOF) has become a crucial aspect as the increase in the meltdown of glaciers results in the breach of unstable debris dams. Hence, it is essential to understand the nature of the glacial lakes for proper planning and development of the region in the long term. In this paper, a deep learning network is developed for GLOF hazard and risk assessment. The Shepard Convolutional Neural Network Fused Deep Maxout Network (ShCNNFDMN) is developed by fusing the Shepard Convolutional Neural Networks (ShCNN) and the Deep Maxout Network (DMN) based on regression analysis. Here, various data and feature attributes, like geometric properties, location properties, lake-based properties, and global properties are determined from the glacial lake data. Afterthat, hazard assessment is carried out based on these parameters by the ShCNNFDMN. Then, risk assessment is performed based on the hazard levels and the feature attributes. The ShCNNFDMN is analyzed based on metrics, such as Hazard modelling error, Risk prediction error, Mean Average Error (MAE), and R-Squared are found to produce values of 0.462, 0.423, 0.358, and 0.288, respectively. The proposed method is useful in applications, like infrastructure planning, taking preventive and mitigative actions in downstream areas of glacier lakes.

### **ARTICLE HISTORY**

Received 30 October 2023 Accepted 10 June 2024

## **KEYWORDS**

GLOF; risk assessment; hazard assessment; Shepard Convolutional Neural Networks; Deep Maxout Network

## 1. Introduction

Global warming and increased human activities have caused major changes in the drylands, and terrestrial water resources all over the world (Zhang et al. 2023). The high voluminous melting glacier water runoff, and accumulates in front of receding glaciers or depressions over sagging and thinning glacier surfaces creating moraine-dammed lakes (Sattar et al. 2021). Generally, glacier shrinking results in the expansion and creation of a huge number of glacial lakes on/in front of the glaciers (Wang et al. 2018). A huge volume of water is released because of certain failures in the moraine or sudden emptying of these lakes due to the overflow of dams, where the destructive events caused by released water sediment are termed Glacial Lake Outburst Floods (GLOF) (Liu et al. 2020; Worni, Huggel, and Stoffel 2013). The GLOF is characterised by its potential for erosion and high transport (Breien et al. 2008) and it can be effectively converted into debris

flows of about 1.5 tm<sup>-3</sup> densities. It is also due to dynamic slope movements of the glaciers over the lakes, namely slopes (Wang and Goh 2021), landslides, rock falls, or icefalls (Awal et al. 2010; Emmer and Vilímek 2013). The incidence of GLOF has been high, especially in the Himalayan area, and has posed a tremendous risk to the local inhabitants (Li et al. 2018). Further, the quantity of water flow in the river affects various activities, such as the allocation of water for hydropower projects, irrigation systems, ecosystems, etc. (Ali et al. 2020).

An in-targeted framework based on the adaption of climate change as well as glacier hazard management is performed from the lessons of the devastating GLOF events (Wang et al. 2018). Over the past decades, the GLOF hazard has increased the risk level due to the significant growth of the existing glacial lakes (Sattar, Goswami, and Kulkarni 2019). The impact of GLOF is transboundary, where the floods destroy most of the downstream infrastructure and kill hundreds of people

thus causing huge damage (Khanal et al. 2015; Liu et al. 2020). Based on a regional scale, the GLOF hazard evaluation is often divided into three parts. The first stage involves gathering the fundamental data about glacial lakes, including their size, position, and surrounding terrain. In the second stage, glacial lakes that are potentially dangerous are identified using the variables that have been chosen. Finally, by using model simulation, field investigation, and high-resolution remote sensing images the study of dangerous glacial lakes is performed (Huggel et al. 2004; McKillop and Clague 2007; Osti, Egashira, and Adikari 2013; Wang et al. 2018). The implementation of different GLOF-related hazard remediations is carried out to develop a significant hazard management system (Sattar, Goswami, and Kulkarni 2019). The GLOF hazard assessment models are developed by considering the glacial lake outburst debris flow scenario (Worni et al. 2012) after earthquakes and small glacial lakes in the areas, which are familiar for landslides and collapses along the channels (Liu et al. 2020). Numerous approaches have been proposed in the past for performing GLOF risk assessment and these techniques vary from each other depending on the subjectivity, input data, choice of examined characteristics, quantity, structure, and so on (Washakh et al. 2019).

In general, because of the potentially hazardous conditions in high mountains, the assessment of glacier hazards cannot be based solely on historical records and past events. Hence, it is necessary to implement various modelling approaches for the determination of present and future GLOF risks and hazards (Allen et al. 2016; Frey et al. 2018; Schaub et al. 2013; Schneider et al. 2014). Generally speaking, identifying exposure, vulnerability, and convergence of hazards are the fundamental elements utilised in risk assessment and management. The subset of machine learning techniques based on representation learning and artificial neural networks is known as deep learning (Wang et al. 2023). Images are processed using a convolutional neural network (Wu et al. 2023). for object detection and classification. The relative GLOF risk towards the downstream region is caused by the cumulative and peak discharge of the hazard components. This leads to overtopping, potential GLOF triggers, damming moraine conditions, and drainable volume functions of the lake. It is also helpful for the determination of hazards based on the vulnerability and exposure of elements downstream of the lake (Emmer 2018; Frey et al. 2018). Moreover, for responsive disaster preparedness and mitigation implementing detailed models and assessments are essential to address extreme-magnitude scenarios (Sattar et al. 2021).

### 1.1. Motivation

In the Himalayan region, glacial lakes have emerged and expanded quickly as a result of glacier recession brought on by climate change. The region is now more vulnerable to Glacial Lake Outburst Floods (GLOFs) as a result of the increased melting. The infrastructure and way of life in the nearby low-lying communities could suffer if potentially hazardous glacier lakes collapsed catastrophically. GLOF has become a crucial aspect in the economic and social stability of the downstream areas as the increase in the meltdown of glaciers results in the breach of unstable debris dams. Hence, it is essential to understand the nature of the glacial lakes for proper planning and development of the region in the long term. Also, the prevailing works carried out with a focus on GLOF risk assessment with their merits and problems confronted that motivated the development of the ShCNNFDMN.

The major intention of this research is to implement a GLOF risk assessment model using the proposed ShCNNFDMN. Here, the GLOF risk assessment is carried out by considering the various properties of the glacial lake. Initially, properties, like geometric, location, lake-based, and global properties are excerpted from the input data. Thereafter, these features are applied to the ShCNNFDMN for assessing the hazard and risk. Here, the ShCNNFDMN is modelled by fusing the ShCNN with the DMN based on regression modelling. At first, the hazard assessment is carried out by the ShCNNFDMN based on the extracted features, and thereafter, the ShCNNFDMN carries out the risk assessment using the features as well as the hazard levels.

The key contribution of this work is as follows:

• Proposed ShCNNFDMN for risk/hazard assessment: In this work, GLOF risk and hazard assessment is carried out by using the ShCNNFDMN, which is formulated by combining ShCNN with DMN, based on regression modelling to improve the efficiency of assessment. Here, fusion is accomplished by applying the concept of Fractional Calculus (FC) to produce a regression model.

The remaining part of the work is arranged as given: section 2 depicts the related works, section 3 portrays the ShCNNFDMN proposed in this work for GLOF risk assessment. The experimental results are shown in Section 4, and Section 5 concludes the study with recommendations for enhancements.

## 2. Literature review

Sattar et al. (2021) proposed a physical hydrodynamic model for modelling the lake outburst and hazard

assessment of the glacial lakes. This method was developed for assessing the GLOF risks across the Barun-Arun river valley in Nepal. Here, the hydraulic flow of the river at six downriver encampments was analyzed, and the possible impact at every location was estimated by evaluating two low-level, two moderate-level, two high-level, and two extreme-level magnitudes were investigated for the current lake size and using this, the future dimension of the lake was modelled. Liu et al. (2020) developed a GLOF hazard assessment model for analyzing the risk of GLOF in Bhote Koshi Basin (BKB). This model assessed the GLOF hazard levels by regarding the situation that the numerous landslides caused by earthquakes evolved into debris in the outburst flood thereby enlarging the volume and discharge of the debris flow. This approach was effective in comprehending the data required for GLOF hazard analysis. However, the method was not appropriate for very high-hazard glacial lakes. Saifullah et al. (2020) devised a Remote sensing technique for GLOF risk assessment along the China-Pakistan Economic Corridor (CPEC). This research was aimed at investigating the formation and impacts of barrier lakes, supra-glacial, and end moraine based onsitu and remote sensing approaches in the Hunza River basin along CPEC considering the peak discharges and volume of the lakes. Emmer and Vilímek (2013) studied the Lake and breach hazard assessment model for assessing the risks of GLOF of moraine-dammed lakes. In this work, various methods for assessing the lake and breach hazards were outlined and the approaches were applied for assessing the hazard levels of the moraine-dammed lakes in Cordillera Blanca (Peru).

Wang et al. (2018) introduced a Hydrologic Engineering Center-River Analysis System (HEC-RAS) for carrying out the integrated hazard assessment of the Cirenmaco glacial lake. This method combined various approaches, like 2D hydraulic modelling, bathymetric survey, and remote sensing for assessing the hazards presented by the Cirenmaco glacial lake. The results produced by the approach were shown to be highly effective in mitigating the risks, but specific care was needed when examining the outcomes of the model because of the complicated nature of GLOFs. Sattar, Goswami, and Kulkarni (2019) developed a two-dimensional hydrodynamic modelling approach for assessing the GLOF hazards of South LhonakLake. Here, a realistic bathymetric framework was constructed for depicting the various GLOF scenarios, and the hazard probability was assessed by utilising one and two-dimensional hydrodynamic modelling techniques. This method made it easier to build structures in the middle of the flow channel and may help manage the risk that extreme flow occurrences bring to areas downstream. Unfortunately, the approach did not provide in-

situ measurements of the geomorphic characteristics over the flow channel or an analysis of engineering properties. Frey et al. (2018) proposed a Scenario-based multisource GLOF hazard mapping technique for assessing the risks of multisource GLOFs. Here, the cascaded mass movement of debris was simulated by utilising a chain of interrelating numerical models. Later, vulnerability evaluations for breach formation and rock-ice avalanches were employed for defining the events of related probability and varying magnitude. However, it failed to enhance the hazard mapping in urban areas that includes a detailed computation of the impacts of urban infrastructure on the flow behaviour of GLOFs. Li et al. (2018) used an Unmanned Surface Vessel (USV) and remote sensing to assess the hazards of GLOF in the Jialong Co glacial lake. Geomorphological analysis, volume assessment, and area dynamics were used for estimating the hazard potential of Jialong Co. The evolution of the Jialong Co in the last years was analyzed using Sentinel 2 satellite and Landsat series image data. Then, the volume, and underwater topography of the lake were detected utilising USVs for bathymetric measurements. Later, the hazard potential was determined by combining the geomorphic conditions, volume data, and area dynamics obtained from in-situ measurements. This plan assisted in determining the volume and underwater topography of the lake, but it did not improve accuracy or carry out longterm geographic monitoring of the moraine dam. Ahmed et al. (2022). uses a combination of remote sensing, GIS, and dam break modelling to evaluate the GLOF danger of Gangabal Lake, which is situated in the Upper Jhelum basin of the Kashmir Himalaya. Glab-Top-2, multitemporal satellite data, and the Cosi - Corr model were also used to evaluate the parameters of the Harmukh glacier, which feeds Gangabal Lake. Wangchuk and Tsubaki (2024) studied the possible effects of a GLOF coming from one of Bhutan's biggest and fastest-growing glacial lakes, Thorthomi, which is a glacial lake in the Phochhu River Basin. The findings here highlight the critical necessity to comprehend and get ready for the possible aftermath of a GLOF from Thorthomi Lake in order to lessen the effects on downstream ecosystems, economies, and societies.

## 3. Proposed ShCNNFDMN-based glof modelling for hazard assessment and risk management

In the current era, the dramatic rise in temperature worldwide due to global warming has resulted in an increase in the number of glacier lakes as well as the dimension of the existing ones. These phenomena have led to a potential risk of GLOF that can wreak havoc on man-made infrastructure and the natural environment. Hence, it is necessary to assess the risk of GLOF to avoid and mitigate any undue casualties. This paper proposes a hybrid ShCNNFDMN-based GLOF risk assessment technique, which is implemented as follows. Gathering information from the dataset is the primary step in the risk assessment process. After that, a number of features, including geometric, locationbased, lake-based, and global properties, are ascertained by applying the input data to the data and feature attribute extraction phase. The location properties that are taken into consideration are indicated by the latitude, longitude, and altitude, with the geometric property being the shape of the lake. Additionally, global characteristics like the Global Terrestrial Network for Glaciers (GTN-G) region and the Universal Transverse Mercator (UTM) grid zone, as well as lake-based parameters like lake area, perimeter, water volume, type, and uncertainty, are also extracted from the input data. Following the mining of the data and feature properties, the suggested hybrid deep learning method ShCNNFDMN is used to assess the hazards. The ShCNN (Ren et al. 2015) and DMN (Sun, Su, and Wang 2018) are combined to create the suggested ShCNNFDMN. The GLOF hazard is evaluated in this instance and assigned to one of the following five categories: Very High (VH), High (H), Medium (M), Low (L), and Very Low (VL). Lastly, the suggested ShCNNFDMN is used to execute the risk assessment based on the data, feature properties, and hazard levels. The GLOF risk is also divided into five categories, which include VH, H, M, L, and VL. The suggested ShCNNFDMN's structural view for the GLOF risk assessment is displayed in Figure 1.

### 3.1. Data acquisition

The initial step in GLOF assessment is to aggregate the data from the GLOF inventory dataset (https://zenodo. org/record/4477945#.ZGXf7nZBxPZ), which can be formulated as.

$$C = \{C_1, C_2, \dots, C_i, \dots, C_c\}$$
 (1)

where,  $C_i$  refers to the *i*th record contained in the dataset  $C_i$ which is considered for GLOF risk prediction, and c specifies the total number of records contained in the dataset.

### 3.2. Feature attributes

Once the data  $C_i$  is retrieved, it is subjected to the extraction of various feature attributes, such as geometric properties, location properties, lake-based properties, and global

properties are determined from the input data. The main intention of this task is to identify the key features of the lake, thereby enabling efficient hazard and risk assessment.

#### 3.2.1. Geometric properties

The geometric property of the glacial lake is considered an important aspect as it determines the stability of the lake. Here, the shape of the lake is taken into account and is found from the input lake image. At first, the boundary values of the lake are computed and then the image is split up into multiple grids. The grids that are contained inside the boundary of the lake are assigned a value of "1", and those falling outside the boundary are allocated a value of "0". Thus, a shape feature matrix comprising of the binary value is obtained from the input lake image, and the shape index matrix thus generated is represented as N.

#### 3.2.2. Location properties

Location is another significant feature that influences the severity of calamities caused by GLOF. The glacial lakes are generally located in uninhabited and remote mountain valleys, however, wide-ranging GLOFs can cause significant damage to properties as well as multiple casualties downstream up to tens of kilometres. Here, various location attributes, such as longitude, latitude, and altitude are computed from the input data, as the location of the glacial lake can be accurately found using these attributes.

- (i) *Longitude*: Longitude is a reference with respect to the prime meridian and it refers to the angular distance (decimal degree) to the west or east of the prime meridian. The longitude feature is represented as  $J_1$ .
- (ii) Latitude: Latitude gives the location of any place with respect to the equator, and is given as a measure of angular distance (decimal degree) to the south or north of the equator. Most of the glaciers are located in higher-latitude regions, such as the Arctic and Antarctic. But the low-latitude regions with high mountain ranges, like the Himalayas and Andes also contain glaciers. The latitude of the glacial lake measured is indicated as  $J_2$ .
- (iii) Altitude: This attribute refers to the elevation of the glacier lake above sea level and is measured in metres/feet. Glacial lakes are more commonly found in high-altitude regions, and their numbers have increased with the retreat of glaciers. Let  $J_3$  designate the altitude feature.

#### 3.2.3. Lake-based properties

The devastating power of GLOF depends on the characteristics of the glacial lake and hence, these parameters

Image /page/5/Figure/3 description: A flowchart titled 'Figure 1. Structural view of the proposed ShCNNFDM N for GLOF risk assessment.' The diagram illustrates a process for risk assessment. At the top, under 'Data and feature attributes', four categories of properties are listed with their corresponding data points: 'Geometric properties' lead to 'Shape of the lake'; 'Location properties' lead to 'Latitude, longitude, and altitude'; 'Lake-based properties' lead to 'Lake area, perimeter, water volume, lake type, and uncertainty'; and 'Global properties' lead to 'UTM grid zone and GTN-G region'. An arrow points down from 'Data and feature attributes' to two parallel processes: 'Risk assessment' on the left and 'Hazard assessment' on the right. The 'Hazard assessment' box contains a 'Proposed ShCNNFDM N' model, which is composed of 'Shepard Convolutional Neural Networks (ShCNN)' and 'Deep Maxout Network (DMN)'. The output of this assessment is a 'Hazard class'. The 'Risk assessment' box also contains a 'Proposed ShCNNFDM N' model, which receives inputs from 'ShCNN' and 'DMN'. This risk assessment process also takes the 'Hazard class' as an input. The final output from the 'Risk assessment' box is the 'Risk class'.

Figure 1. Structural view of the proposed ShCNNFDMN for GLOF risk assessment.

have to be considered while evaluating the risk assessment. The lake-based properties, such as lake area, perimeter, water volume, lake type, and uncertainty (Zheng et al. 2021) are considered here.

- (i) Lake area: Lake area indicates the surface area of the lake and is obtained by multiplying the length and width of the lake and is expressed as  $J_4$ . Lake area is measured in square metres and is measured based on the UTM.
- (ii) *Perimeter*: The total length of the shoreline line of the lake gives the perimeter value and is indicated
- (iii) Water volume: The volume of the lake is measured by finding the product of the surface area of the

- lake, and is expressed in cubic metres. The water volume feature of the glacial lake is characterised as  $J_6$ . The destructive potential of GLOF depends on the volume of water contained in the lake.
- (iv) Lake type: The impact of GLOF depends on the type of the glacial lakes, which can be either Ice (I), Moraine (M), or others (O). Moraine-dammed glacial lakes are found to be a more prominent cause of GLOF than other glacial lakes. The laketype feature is symbolised as  $J_7$ .
- (v) Uncertainty: This parameter deals with the uncertainty of the measurements of the glacial topology obtained using remote sensing techniques, and is considered so that the values can be analyzed as per their relevance. Uncertainty of the lake area is

jan

expressed as,

$$J_8 = J_6/A \times A^2/2 \times 0.6872 \tag{2}$$

where A refers to the image's spatial resolution, I<sub>6</sub> designates the perimeter, and  $J_8$  represents the uncertainty feature.

#### 3.2.4. Global properties

In addition to the above features, the global properties, such as the UTM grid zone, and GTN-G region of the glacial lake are considered to improve the risk assessment efficiency.

- (i) UTM grid zone: This refers to the UTM zone in which the glacial lake is present. The UTM coordinate system partitions the globe into 60 zones, and in all zones, the coordinates are measured in northings and eastings in metres, and each zone has a width of 6° longitude. The UTM grid zone is designated as  $J_9$ .
- (ii) *GTN-G region*: The GTN-G region in which the glacial lake is located is termed the GTN-G region feature, and is characterised by  $J_{10}$ . These regions are essential in analyzing the variations in glaciers and other attributes in a region. Once the various features are excerpted from the database, they are combined to obtain a feature vector as given below,

$$J = \{J_1, J_2, \dots, J_{10}\}$$
 (3)

where,  $J_1$  is the latitude,  $J_2$  specifies the longitude,  $J_3$ symbolises the altitude,  $J_4$  refers to the lake area,  $J_5$ characterises the perimeter of the lake, J<sub>6</sub> denotes the water volume,  $J_7$  represents the lake type,  $J_8$  is the uncertainty feature,  $J_9$  exemplifies the UTM grid zone, and  $J_{10}$  terms the GTN-G region. The feature vector is generated J and the shape index matrix N is applied to the proposed ShCNNFDMN for hazard assessment.

### 3.3. Hazard assessment

A hazard assessment is carried out to find the probability that the water will be released from a glacial lake. This process is carried out by identifying the potentially hazardous lake first and then assessing the probability of water release based on the hazard index of the lake from the features extracted J. Here, hazard assessment is carried out by using the proposed ShCNNFDMN, which is created by combining the ShCNN (Ren et al. 2015) with DMN (Sun, Su, and Wang 2018) based on regression analysis. A statistical

method for determining the relationships between variables in a given set of data is regression analysis. It can evaluate the statistical significance of the association, or the probability that the correlation is the product of chance, as well as show how strong the relationship is. One of the two main purposes of regression analysis is to either predict the value of the dependent variable for those for whom some information about the explanatory factors is available, or to assess the effect of an explanatory variable on the dependent variable. The ShCNNFDMN is fed with the shape index matrix N and a feature is generated J for assessing the GLOF hazard. The ShCNNFDMN comprises three parts, such as the ShCNN model, the DMN model, and the ShCNNFDMN layer. Initially, the shape index matrix N is subjected to the ShCNN model, which classifies the hazard into either of the five categories, such as VH, H, M, L, and VL. Thereafter, the output of the ShCNN is forwarded to the ShCNNFDMN layer, which fuses the output of the ShCNN with the feature vector *J* based on regression modelling, which is applied to determining the relationship between the two inputs, thereby enhancing the effectiveness of hazard assessment. Later, the fused output generated by the ShCNNFDMN layer is subjected to the DMN model for hazard assessments along with the shape index matrix N. Here, regression modelling is accomplished by applying the concept of Fractional Calculus (FC) (Bhaladhare and Jinwala 2014). Figure 2 demonstrates the architectural view of the proposed ShCNNFDMN for hazard assessment, and the various processes undertaken are expounded on in the ensuing subsections.

#### 3.3.1. ShCNNmodel

Initially, the hazard assessment is accomplished by using the ShCNN (Ren et al. 2015) by applying the shape index matrix N. The ShCNN is a type of CNN that is developed by incorporating the Shepard technique for altering the basic CNN to attain Translation Variant Interpolation (TVI). The key advantage of using the ShCNN is its low computational cost and its ability in realising end-to-end TVI operations for intermittently spaced data. The network attains superior results by adding a smaller number of feature maps and optimisation of the TVI process. The Shepard structure computes the weights of the familiar pixels based on the spatial distance between them and the target pixels differently, and its convolution form is formulated

$$H_1 k = \begin{cases} (Z*N)_k / (Z*L)_k & \text{if } L_k = 0\\ N_k & \text{if } L_k = 1 \end{cases}$$
 (4)

Image /page/7/Figure/3 description: An architectural diagram illustrating the proposed ShCNNFDMN model for hazard assessment. The diagram shows a multi-stream process. In the top stream, a 'Shape index matrix N' is fed into an 'ShCNN model', which is represented by a linear sequence of seven blocks, producing 'Output H1'. In the middle stream, a 'Feature vector J' is input to the 'ShCNNFDMN layer'. This layer, which also receives 'Output H1', contains two components: 'Regression Modeling' and 'Fusion'. The output of this layer is 'Output H2'. In the bottom stream, the 'Shape index matrix N' is also input into a 'DMN model'. This model is depicted as a more complex structure with three rows of interconnected blocks. The final output of the entire system, originating from the DMN model, is the 'Risk level R'.

Figure 2. Architectural view of the proposed ShCNNFDMN for hazard assessment.

wherein, N represents the shape index matrix to the ShCNN, k signifies the image coordinate,  $H_{1k}$  refers to the output, \* implies the convolution function, L characterises the binary operator, which has a value  $L_k=0$  in case the pixel values are not known, and Z refers to the kernel function that has a weight inversely proportional to the separation among the pixel under consideration and  $Z_k=1$ .

The characterisation of the convolutional kernel is the major factor that affects the interpolation result in the Shepard framework, and so a Shepard interpolation layer is employed to allow a kernel design that has good flexibility and is data-driven.

##### Shepard interpolation layer:

The expression given below describes the Shepard interpolation layer's feed-forward pass,

$$G_{j}^{d}(G^{d-1}, L^{d}) = \alpha \left( \sum_{l} \frac{Z_{jl}^{d} * G_{l}^{d-1}}{Z_{jl}^{d} * L_{l}^{d}} + p^{d} \right), \quad d = 1, 2, 3, \dots \tag{5}$$

Here, d represents the index of layer,  $G^{d-1}$  indicates the input of the present layer, whose mask is characterised as  $L^d$ , the term j in  $G_j^{d-1}$  and  $G_j^d$  denotes the feature map index in the (d-1) th and dth layer, respectively,  $Z_{il}$  signifies the trainable parameters and convolution of

[Icon of a ship in a circle]

 $Z_{il}$  is performed with the mask of the present layer  $L^d$  in the denominator and activations of the final layer in the numerator.  $G^{d-1}$  can signify the feature maps of the convolution or pooling layers of the CNN, and this can also be considered as the preceding Shepard interpolation layer. The term  $\alpha$  is used to impose non-linearity in the network and *p* symbolises bias.

Figure 3 explicates the structure of the ShCNN, where it is applied with the shape index matrix N. The various inputs, such as feature maps/images, and masks representing the position where interpolation must happen are fed as input to the Shepard interpolation layer. Any complex interpolation operator can be constructed by applying the interpolation layer in a repeated manner with several non-linear layers. The mask refers to the binary map which has a value "0" for missing areas and "1" for familiar areas, and the same kernel is used with the mask as well as the image. The insignificant values of the preceding convolved mask  $Z^d*L^d$  are zeroed and a threshold is applied to generate the mask of the (d+1)th layer. Shepard interpolation layer with multiple stages is required to learn the sophisticated manner of propagation in processes where relatively bigger missing regions, like inpainting, occur. The output generated by the ShCNN is represented as  $H_1$ .

#### 3.3.2. ShCNNFDMN layer

Once the output of the ShCNNH<sub>1</sub> is obtained, it is fed to the ShCNNFDMN layer together with the location properties, lake-based properties, and global properties of the lake. One of the main advantage of ShCNNFDMN layer is simple and robust. The location properties are given by  $P_1 = \{J_1, J_2, J_3\}$  which include the latitude  $J_1$ , longitude  $J_2$ , and altitude  $J_3$ . Further, the lake-based properties are given by  $P_2 = \{J_4, J_5, J_6, J_7, J_8\}$  that comprise the lake area  $J_4$ , perimeter  $J_5$ , water volume  $J_6$ , lake type  $J_7$ , and uncertainty  $J_8$ . The global properties of the lake  $P_3 = \{J_9, J_{10}\}$  incorporate the UTM grid zone  $J_9$  and GTN-G region  $J_{10}$ . Here, the features are fused with the classified output of the ShCNN by using the concept of regression modelling. The relationship between the features and the classified output can be determined by using regression modelling, which is carried out here by utilising FC (Bhaladhare and Jinwala 2014), which is a subdivision of applied mathematics that solves the integral and derivative equations by using the Laplace transform. Here, the problem is first solved by converting it into the Laplace domain and later, the actual solution is determined by applying inverse transform. Here, the features excerpted as considered to be taken at various time intervals, and the

weighted features are combined with the classified output of the ShCNN. This process is formulated as follows,

At the interval t, the output of the ShCNNFDMN layer is expressed as,

$$g = \sum_{q=1}^{n_1} P_{1q} \omega_q \tag{6}$$

Here,  $P_1$  refers to the location properties of the lake comprising latitude, longitude, and altitude,  $n_1$  refers to the number of location properties, and  $\omega$  refers to the weight coefficients.

When the time interval t-1 is considered, then the output of the ShCNNFDMN layer is obtained by considering the lake-based properties, and this is mathematically modelled as,

$$g_1 = \sum_{q=1}^{n_2} P_{2q} \omega_q \tag{7}$$

where,  $P_2$  symbolises the lake-based properties and  $n_2$ represents the number of lake-based properties. Further, the output of the ShCNNFDMN layer at time instance t-2 is formulated based on the global properties of the glacial lake, and is modelled as,

$$g_2 = \sum_{q=1}^{n_3} P_{3q} \omega_q \tag{8}$$

Here,  $P_3$  represents the global properties of the lake, such as the UTM grid zone, and GTN-G region, and  $n_3$  characterises the number of global properties.

Moreover, the output of the ShCNNFDMN at  $(t-3)^{th}$  intervals is considered to be the classified layer of the  $ShCNNH_1$ , and these are combined by using FC. Applying the concept of FC (Bhaladhare and Jinwala 2014),

$$\begin{aligned} y(t+1) &= u \cdot y(t) + \frac{1}{2}u \cdot y(t-1) \\ &\qquad + \frac{1}{6}(1-u)y(t-2) \\ &\qquad + \frac{1}{24}u(1-u)(2-u) \cdot y(t-3) \end{aligned}\tag{9}$$

Substituting the respective values ShCNNFDMN layer, the equation depicted above can be written as,

$$H_2 = u \cdot g + \frac{1}{2}u \cdot g_1 + \frac{1}{6}(1 - u)g_2 + \frac{1}{24}u(1 - u)(2 - u) \cdot H_1$$
 (10)

Shape index matrix N

Image /page/9/Figure/4 description: A diagram illustrating the architecture of a neural network. The data flows from left to right through a series of layers. The sequence of layers and the dimensions of the data after each layer are as follows: two light blue 'Conv layers' resulting in dimensions of 1x26x32 and 1x26x64 respectively; a light yellow 'Leaky ReLU layer' with an output of 1x26x64; a light blue 'Maxpooling layer' resulting in 1x13x64; an olive green 'Flatten layer' with an output of 1x832; and two light yellow 'Dense layers' with outputs of 1x32 and 1x5. The final output of the network is labeled 'Output H₁'.

Figure 3. Structure of the ShCNN.

Applying the values of g,  $g_1$ , and  $g_2$  from equations (6-8),

$$\begin{aligned}H_{2} ={}& u \cdot \sum_{q=1}^{n_{1}} P_{1q} \omega_{q} + \frac{1}{2} u \cdot \sum_{q=1}^{n_{2}} P_{2q} \omega_{q} \\ & + \frac{1}{6} (1 - u) \sum_{q=1}^{n_{3}} P_{3q} \omega_{q} \\ & + \frac{1}{24} u (1 - u) (2 - u) \cdot H_{1}\end{aligned}\qquad (11)$$

Here,  $H_1$  characterises the output of the ShCNN and is found using equation (4),  $H_2$  which signifies the output generated by the ShCNNFDMN layer, and u symbolises a constant that signifies the derivative order in FC.

#### 3.3.3. DMN model

The DMN is applied with the shape index matrix N, and the output  $H_2$  produced by the ShCNNFDMN layer for performing hazard assessment. The output produced by the ShCNN is also a hazard assessment level, and the output produced by the ShCNN is combined with the features and given to the DMN, thereby boosting the efficiency of hazard assessment. The ShCNN and DMN perform classification at various stages, and thus in the DMN, more refined features are used along with the shape-indexed matrix, which minimises the classification cost as well. Here, the DMN (Sun, Su, and Wang 2018) is mainly applied for hazard assessment due to its ability to produce superior outcomes in resource-constrained scenarios. DMN predict more consistently and accurately. The DMN is applied with an inputS;  $(S = \{N, H_2\})$  created by considering the shape indexed matrix N and the output of the

ShCNNFDMN layer  $H_2$ , and the various processes taking place in the DMN are explicated as given below,

$$b_{x,y}^{1} = \max_{y \in [1,v_1]} S^T V_{\dots xy} + w_{xy}$$
 (12)

$$b_{x,y}^{2}T = \max_{y \in [1,v_{2}]} b_{x,y}^{1}TV_{...xy} + w_{xy}$$
 (13)

$$b_{x,y}^{e}T = \max_{v \in [1,v_e]} b_{x,y}^{e-1}TV_{...xy} + w_{xy}$$
 (14)

$$b_{x,y}^{f}T = \max_{y \in [1,y_f]} b_{x,y}^{f-1}TV_{\dots xy} + w_{xy}$$
 (15)

$$R_{x} = \max_{y \in [1, y_{f}]} b_{x, y}^{f} \tag{16}$$

Here, x refers to the total count of layers in DMN,  $A_x$  refers to the hazard assessed by the DMN,  $v_e$  designates the overall count of units in the  $e^{th}$  layer,  $w_{xy}$  characterises the bias,  $V_{xy}$  symbolises the weight, and  $b_{x,y}^e$  designates the output produced by the eth layer. As depicted in the above equation, a max-pooling function is used by the DMN, and the maximal value of the output generated in each layer is fed to the consecutive layers. When v > 2 the DMN can estimate any conventional nonlinear activation functions. The architectural view of the DMN is depicted in Figure 4 and the output produced is indicated as R.

### 3.4. Risk management using the proposed ShCNNFDMN

After the hazard level *R* is identified by the ShCNNFDMN, risk assessment is carried out based on the hazard levels *R* 

Image /page/10/Figure/1 description: The number 106 is shown in black text against a white background.

Image /page/10/Figure/2 description: A diagram illustrating the architecture of a convolutional neural network. The model processes an input labeled 'S = {N, H₂}' through a series of layers to output a 'Risk level R'. The architecture is laid out in three rows. The first row consists of an Input layer (64x64x3), a Convolution layer (62x62x64), a Lamda layer (62x62x32), a Batch Normalization layer (62x62x32), and a Max pooling layer (31x31x32). The second row continues with a Convolution layer (29x29x128), a Lamda layer (29x29x64), a Batch Normalization layer (29x29x64), a Max pooling layer (14x14x64), a Dropout layer (14x14x64), and another Convolution layer (12x12x256). The third row includes a Lamda layer (12x12x64), a Batch Normalization layer (12x12x64), a Dropout layer (6x6x64), a Flatten layer (1x2304), and a Dense layer (1x1) which produces the final output. A legend at the bottom clarifies the layer types corresponding to different colors: Input layer, Lamda, Max pooling layer, Flatten, Convolution layer, Batch Normalization layer, Dropout layer, and Dense.

Figure 4. Architectural view of the DMN.

and various feature attributes N, and J. Risk assessment is extremely essential as it gives a clear picture of the aftereffects of a GLOF, thereby helping in taking effective risk reduction strategies. Glacial lakes that are assessed to be under HVH hazard levels pose a greater risk to the communities residing downstream (Zheng et al. 2021). Here, risk assessment is performed using the ShCNN based on the risk index, which can be obtained considering the exposure index and the hazard index. The exposure index refers to the potency of GLOF causing devastation to the infrastructures as well as life and hazard index terms the combined magnitude and likelihood of the GLOF. The ShCNNFDMN is already elucidated in section 3.3., and combines the ShCNN (Ren et al. 2015) and the DMN (Sun, Su, and Wang 2018) using regression analysis.

## 4. Results and Discussion

The results obtained during the experimentation of the ShCNNFDMN for GLOF risk assessment are detailed in this section. Further, the experimental set-up, evaluation measures, dataset, and analysis of the approach are also demonstrated.

### 4.1. Experimental set-up

The ShCNNFDMN for GLOF risk assessment proposed in this work is implemented on a system with the Python language using the glacial lake inventories dataset (https://zenodo.org/record/4477945#. ZGXf7nZBxPZ). Table 1 shows the experimental parameters of the proposed method.

**Table 1.** Experimental parameters of the proposed method.

| Methods          | Physical<br>hydrodynamic<br>model | GLOF Hazard<br>assessment | Lake and breach<br>Hazard assessment | HEC-RAS | Two-dimensional<br>hydrodynamic model | Scenario-based<br>multi-source GLOF | Proposed<br>ShCNNFDMN |
|------------------|-----------------------------------|---------------------------|--------------------------------------|---------|---------------------------------------|-------------------------------------|-----------------------|
| Epochs           | 20                                | 20                        | 25                                   | 20      | 20                                    | 20                                  | 30                    |
| Batch size       | 32                                | 32                        | 32                                   | 32      | 32                                    | 32                                  | 64                    |
| Learning<br>rate | 0.001                             | 0.001                     | 0.001                                | 0.001   | 0.001                                 | 0.001                               | 0.001                 |

The bold values represent the best performance.

Image /page/11/Figure/3 description: A geographical map showing the distribution of glacial lakes over a Digital Elevation Model (DEM) of a mountainous region. The map is bounded by coordinates from 70°0'0"E to 100°0'0"E longitude and from 20°0'0"N to 40°0'0"N latitude. A compass rose is present in the upper right corner. The legend indicates that the blue areas represent 'Glacial Lakes'. The DEM values, shown in grayscale, range from a 'Low' of 232 to a 'High' of 8233. The map includes a scale bar marked up to 1,240 Kilometers and a textual scale of '1 cm = 210 km'.

Figure 5. Glacial Lake Dataset.

### 4.2. Dataset description

The data used for the experimentation of the ShCNNFDMN is acquired from the glacial lake inventories dataset and has been mapped in Figure 5 (https://zenodo.org/record/4477945#.ZGXf7nZBxPZ). This dataset comprises the data of the glacial lakes present in the Third Pole region. The data encompassed are acquired over a period of 15 years from 1990 to 2015, Further, the data is modelled for considering future conditions for 2050 and 2100 on the Third Pole under an ice-free scenario, Representative Concentration Pathway (RCP) 8.5, RCP 4.5, and RCP 2.6. It contains various data regarding the glacial lake shape, location, uncertainty, lake water volume, hazard value, risk value, exposure value, etc.

### 4.3. Evaluation measures

Two parameters, such as Hazard modelling error, and Risk prediction error are considered to evaluate the supremacy of the ShCNNFDMN.

(i) *Hazard modelling error*: The hazard modelling error is measured by finding the deviation of the predicted hazard value by the ShCNNFDMN from the expected values.

$$HME = \frac{\sum_{i=1}^{n} |y_i - x_i|}{n}.$$
 (17)

where, HME refers to the Hazard Modelling Error,

 $y_i$  refers to the prediction, $x_i$  refers to the true value, and n designates the total number of data.

(ii) *Risk prediction error:* The risk prediction error is also found similar to the hazard modelling error by determining the difference between the predicted risk value from the anticipated risk value.

$$RPE = \frac{\sum_{i=1}^{n} |y_i - x_i|}{n}.$$
 (18)

where, *RPE* refers to the Risk Prediction Error.

(iii) *Mean Average Error (MAE):* The MAE, is a statistical measure of inaccuracies between paired observations that represent the same occurrence.

$$MAE = \frac{\sum_{i=1}^{n} |y_i - x_i|}{n}.$$
 (19)

where, MAE refers to the Mean Average Error.

(iv) *R-Squared:* The percentage of a dependent variable's variance that can be accounted for by an independent variable is expressed statistically as R-squared.

$$R^2 = 1 - \frac{RSS}{TSS}. (20)$$

where, RSS refers to the sum of squares of residuals, and TSS refers to the total sum of squares.

### 4.4. Performance analysis

The performance of the ShCNNFDMN is examined by considering the values of Hazard modelling error, and Risk

prediction error determined when different k-fold values and training data percentages are used for various iterations.

#### 4.4.1. Based on k-fold

Figure 6 demonstrates the performance assessment of the ShCNNFDMN while varying the k-fold values. In Figure 6 (a), the analysis of the ShCNNFDMN based on hazard modelling error is exhibited. With a k-fold of 9, the value of hazard prediction error measured by the ShCNNFDMN is 0.558, 0.526, 0.518, 0.505, and 0.487, corresponding to 20, 40, 60, 80, and 100 iterations. Likewise, the assessment of the ShCNNFDMN in terms of risk prediction error is illustrated in Figure 6(b). The ShCNNFDMN is observed to have attained a risk prediction error of 0.495 for 20 iterations, 0.507 for 40 iterations, 0.497 for 60 iterations, 0.484 for 80 iterations, and 0.428 for 100 iterations with k-fold of 9. In Figure 6(c), the analysis of the ShCNNFDMN based on MAE is showed. With a k-fold of 9, the value of MAE measured by the ShCNNFDMN is 0.450, 0.414, 0.410, 0.395, and 0.370,

corresponding to 20, 40, 60, 80, and 100 iterations. Figure 6 (d) explicates the assessment of the ShCNNFDMN on the basis of R-Squared. For k-fold of 9, the ShCNNFDMN recorded R-Squared of 0.346 for 20 iterations, 0.331 for 40 iterations, 0.324 for 60 iterations, 0.312 for 80 iterations, and 0.292 for 100 iterations.

#### 4.4.2. Considering training data

The evaluation of the ShCNNFDMN considers the hazard modelling error and risk prediction error while taking into account various training data percentages. Figure 7(a) explicates the assessment of the ShCNNFDMN on the basis of hazard modelling error. For 90% of training data, the ShCNNFDMN recorded hazard modelling error of 0.644 for 20 iterations, 0.582 for 40 iterations, 0.561 for 60 iterations, 0.540 for 80 iterations, and 0.484 for 100 iterations. Further, the assessment of the ShCNNFDMN concerning the risk prediction error is exhibited in Figure 7(b). The risk prediction error measured by the ShCNNFDMN

Image /page/12/Figure/9 description: The image displays four line graphs, labeled (a), (b), (c), and (d), showing the performance assessment of a model named ShCNNFDM. Each graph plots a different performance metric against 'K-Fold' on the x-axis, which ranges from 5 to 9. Each graph includes five lines representing the model run with a different number of iterations: 20 (blue with 'x' markers), 40 (pink with '\*' markers), 60 (green with right-pointing triangle markers), 80 (teal with left-pointing triangle markers), and 100 (red with circle markers).

(a) The top-left graph shows 'Hazard modelling error' on the y-axis, from 0.50 to 0.70. For all lines, the error generally decreases as K-Fold increases. The error is lowest for the model with 100 iterations (red line, from ~0.53 to ~0.48) and highest for the model with 20 iterations (blue line, from ~0.71 to ~0.56).

(b) The top-right graph shows 'Risk prediction error' on the y-axis, from 0.45 to 0.70. Similar to the first graph, the error decreases as K-Fold increases and as the number of iterations increases. The 100-iteration model has the lowest error (red line, from ~0.54 to ~0.43), while the 20-iteration model has the highest (blue line, from ~0.72 to ~0.51).

(c) The bottom-left graph shows 'MAE' (Mean Absolute Error) on the y-axis, from 0.38 to 0.52. The MAE decreases as K-Fold increases and as the number of iterations increases. The 100-iteration model performs best with the lowest MAE (red line, from ~0.45 to ~0.37), and the 20-iteration model performs worst with the highest MAE (blue line, from ~0.52 to ~0.45).

(d) The bottom-right graph shows 'R-squared' on the y-axis, from 0.30 to 0.44. In this graph, the R-squared value decreases as K-Fold increases for all models. Contrary to the error metrics, a higher R-squared value is better, and the model with fewer iterations performs better. The 20-iteration model has the highest R-squared (blue line, from ~0.44 to ~0.34), while the 100-iteration model has the lowest (red line, from ~0.36 to ~0.29).

Figure 6. Performance assessment of the ShCNNFDMN based on (a) Hazard modelling error, (b) Risk prediction error, (c) MAE, and (d) R-Squared.

Image /page/13/Figure/3 description: The image contains four line graphs, labeled (a), (b), (c), and (d), which show the performance assessment of a model called ShCNNFDMN. Each graph plots a different performance metric against the percentage of training data, which ranges from 50% to 90% on the x-axis. All graphs compare five versions of the model based on the number of iterations: 20, 40, 60, 80, and 100.

(a) The first graph plots 'Hazard modelling error' on the y-axis from 0.50 to 0.75. For all lines, the error decreases as the training data increases. The error is lowest for 100 iterations (red line, from ~0.56 to ~0.48) and highest for 20 iterations (blue line, from ~0.75 to ~0.64).

(b) The second graph plots 'Risk prediction error' on the y-axis from 0.45 to 0.75. The trend is similar to the first graph, with the error decreasing with more training data and more iterations. The 100-iteration line drops from ~0.57 to ~0.44, while the 20-iteration line drops from ~0.74 to ~0.62.

(c) The third graph plots 'MAE' (Mean Absolute Error) on the y-axis from 0.375 to 0.525. Again, the error decreases as training data and the number of iterations increase. The 100-iteration line goes from ~0.43 to ~0.36, and the 20-iteration line goes from ~0.53 to ~0.42.

(d) The fourth graph plots 'R-squared' on the y-axis from 0.30 to 0.42. In this case, the R-squared value decreases as the training data percentage increases. The model with 20 iterations has the highest R-squared values (from ~0.425 to ~0.335), while the model with 100 iterations has the lowest (from ~0.39 to ~0.295).

The caption below reads: 'Figure 7. Performance assessment of the ShCNNFDMN based on (a) Hazard modelling error, (b) Risk prediction error, (c) MAE, and (d) R-squared.'

Figure 7. Performance assessment of the ShCNNFDMN based on (a) Hazard modelling error, (b) Risk prediction error, (c) MAE, and (d) R-Squared based on training data.

with 20, 40, 60, 80, and 100 iterations is 0.620, 0.569, 0.524, 0.463, and 0.436, respectively, for 90% of training data. In Figure 7(c), the analysis of the ShCNNFDMN based on MAE is exhibited. With 90% of training data, the value of MAE measured by the ShCNNFDMN is 0.423, 0.422, 0.417, 0.387, and 0.364, corresponding to 20, 40, 60, 80, and 100 iterations. Likewise, the assessment of the ShCNNFDMN in terms of R-Squared is illustrated in Figure 7(d). The ShCNNFDMN is observed to have attained a R-Squared of 0.338 for 20 iterations, 0.318 for 40 iterations, 0.318 for 60 iterations, 0.311 for 80 iterations, and 0.296 for 100 iterations with 90% of training data.

### 4.5. Comparative techniques

The efficiency of the ShCNNFDMN is investigated by comparing the proposed technique with other prevailing

GLOF risk assessment methods, such as the Physical hydrodynamic model (Sattar et al. 2021), GLOF Hazard assessment (Liu et al. 2020), Lake and breach Hazard assessment (Emmer and Vilímek 2013), HEC-RAS (Wang et al. 2018), Two-dimensional hydrodynamic model, and Scenario-based multi-source GLOF.

### 4.6. Comparative analyis

The analysis of the ShCNNFDMN is carried out to examine its superiority in performing GLOF risk/hazard assessment by taking into consideration different values of training data and k-fold.

#### 4.6.1. Using K-fold

The examination of the ShCNNFDMN based on k-fold is with respect to hazard modelling error and risk prediction error is displayed in Figure 8. The hazard

Image /page/14/Figure/1 description: Two line graphs, labeled (a) and (b), compare the performance of seven different models. Both graphs plot an error metric on the y-axis against 'K-Fold' on the x-axis, which ranges from 5 to 9. Graph (a) shows 'Hazard modelling error' on the y-axis, ranging from 0.50 to 0.75. Graph (b) shows 'Risk prediction error' on the y-axis, ranging from 0.45 to 0.75. The seven models compared are: 'Physical hydrodynamic model' (blue), 'GLOF Hazard assessment' (pink), 'Lake and breach Hazard assessment' (green), 'HEC-RAS' (cyan), 'Two-dimensional hydrodynamic model' (red), 'Scenario-based multi-source GLOF' (yellow), and 'Proposed ShCNNFDMN' (dark gray). In both graphs, the 'Proposed ShCNNFDMN' model consistently has the lowest error across all K-Fold values. In graph (a), its error decreases from approximately 0.52 at K-Fold 5 to 0.47 at K-Fold 9. In graph (b), its error decreases from approximately 0.56 at K-Fold 5 to 0.43 at K-Fold 9. The other models generally show higher and more variable error rates.

Image /page/14/Figure/2 description: A line graph, labeled (c), plots the Mean Absolute Error (MAE) on the y-axis against the K-Fold value on the x-axis. The x-axis ranges from 5 to 9, while the y-axis ranges from 0.375 to 0.525. The graph compares the performance of seven different models, each represented by a colored line with unique markers. The legend identifies six of the models: 'GLOF Hazard assessment' (dark blue line with 'x' markers), 'Lake and breach Hazard assessment' (pink line with star markers), 'HEC-RAS' (cyan line with triangle markers), 'Two-dimensional hydrodynamic model' (red line with circle markers), 'Scenario-based multi-source GLOF' (yellow line with diamond markers), and 'Proposed ShCNNFDMN' (gray line with pentagon markers). A seventh line, green with circular markers, is also present but not identified in the legend. The 'Proposed ShCNNFDMN' model consistently shows the lowest MAE across all K-Fold values, decreasing from approximately 0.445 at K-Fold 5 to 0.362 at K-Fold 9. Most other models also show a general downward trend in MAE as the K-Fold value increases.

Image /page/14/Figure/3 description: A line graph, labeled (d), showing the relationship between R-squared values and K-Fold for seven different models. The x-axis is labeled 'K-Fold' and ranges from 5 to 9. The y-axis is labeled 'R-squared' and ranges from 0.30 to 0.44. The graph displays seven lines, each representing a different model, and all lines show a downward trend, indicating that the R-squared value decreases as the K-Fold value increases. The models and their approximate data points are as follows: 'Physical hydrodynamic model' (blue line with x markers) starts at approximately R-squared=0.445 at K-Fold=5 and ends at 0.348 at K-Fold=9. 'GLOF Hazard assessment' (pink line with star markers) starts at 0.443 and ends at 0.345. 'Lake and breach Hazard assessment' (green line with circle markers) starts at 0.435 and ends at 0.33. 'HEC-RAS' (cyan line with triangle markers) starts at 0.42 and ends at 0.33. 'Two-dimensional hydrodynamic model' (red line with circle markers) starts at 0.422 and ends at 0.325. 'Scenario-based multi-source GLOF' (yellow line with diamond markers) starts at 0.412 and ends at 0.312. 'Proposed ShCNNFDMN' (gray line with pentagon markers) consistently has the lowest R-squared values, starting at 0.398 and ending at 0.30.

Figure 8. Comparative assessment of the ShCNNFDMN based on (a) Hazard modelling error, (b) Risk prediction error, (c) MAE, and (d) R-Squared considering k-fold.

modelling error-based assessment of the ShCNNFDMN is demonstrated in Figure 8(a). The ShCNNFDMN is found to have produced a hazard modelling error of 0.483with k-fold of 8, while the prevailing risk assessment approaches, such as the Physical hydrodynamic model, GLOF Hazard assessment, Lake and breach assessment, HEC-RAS, Two-dimensional hydrodynamic model, and Scenario-based multi-source GLOF, measured hazard modelling error of 0.620, 0.594, 0.619, 0.612, 0.583, and 0.516, correspondingly. In Figure 8(b), the investigation of the ShCNNFDMN with respect to risk prediction error is presented, For a k-fold value of 8, the risk prediction error recorded by the Physical hydrodynamic model is 0.639, GLOF Hazard assessment is 0.554, Lake and breach Hazard assessment is 0.526, HEC-RAS is 0.544, Two-dimensional hydrodynamic model is 0.527, Scenario-based multi-source GLOF is 0.496, and ShCNNFDMN is 0.454. The MAE-based assessment ShCNNFDMN is demonstrated in Figure 8(c). The ShCNNFDMN is found to have produced a MAE of 0.379 with k-fold of 8, while the prevailing risk assessment approaches, such as the Physical hydrodynamic model, GLOF Hazard assessment, Lake and breach Hazard assessment, HEC-RAS, Two-dimensional hydrodynamic model, and Scenario-based multi-source GLOF, measured hazard modelling error of 0.470, 0.450, 0.448, 0.425, 0.416, and 0.415, correspondingly. In Figure 8(d), the investigation of the ShCNNFDMN with respect to R-Squared is presented, For a k-fold value of 8, the R-Squared recorded by the Physical hydrodynamic model is 0.366, GLOF Hazard assessment is 0.356, Lake and breach Hazard assessment is 0.355, HEC-RAS is 0.350, Two-dimensional hydrodynamic model is 0.344, Scenario-based multi-source GLOF is 0.330, and ShCNNFDMN is 0.313.

#### 4.6.2. Based on training data

Figure 9 represents the analysis of the ShCNNFDMN for GLOF risk/hazard assessment considering different percentages of training data. The ShCNNFDMN is examined for its efficacy on the basis of hazard

Image /page/15/Figure/3 description: A set of four line graphs, labeled (a), (b), (c), and (d), comparing the performance of seven different models against varying amounts of training data. The x-axis for all graphs is 'Training data (%)', ranging from 50 to 90. The seven models compared are: 'Physical hydrodynamic model', 'GLOF Hazard assessment', 'Lake and breach Hazard assessment', 'HEC-RAS', 'Two-dimensional hydrodynamic model', 'Scenario-based multi-source GLOF', and 'Proposed ShCNNFDMN'.

Graph (a) plots 'Hazard modelling error' on the y-axis (from 0.45 to 0.75). Generally, the error for all models decreases as training data increases. The 'Proposed ShCNNFDMN' model consistently has the lowest error, decreasing from approximately 0.54 to 0.48. The 'Physical hydrodynamic model' starts with the highest error at about 0.74.

Graph (b) plots 'Risk prediction error' on the y-axis (from 0.45 to 0.75). The error trends downwards for most models with more training data. The 'Proposed ShCNNFDMN' model again shows the best performance with the lowest error, dropping from about 0.57 to 0.42.

Graph (c) plots 'MAE' (Mean Absolute Error) on the y-axis (from 0.350 to 0.550). All models show a decrease in MAE as training data increases. The 'Proposed ShCNNFDMN' model has the lowest MAE, decreasing from around 0.435 to 0.36. The 'Physical hydrodynamic model' has the highest MAE across the range.

Graph (d) plots 'R-squared' on the y-axis (from 0.30 to 0.44). In this graph, the R-squared values for all models generally decrease as the percentage of training data increases. The 'Physical hydrodynamic model' has the highest R-squared values, while the 'Proposed ShCNNFDMN' has the lowest.

Figure 9. Comparative assessment of the ShCNNFDMN based on (a) Hazard modelling error, (b) Risk prediction error, (c) MAE, and (d) R-Squared based on training data.

modelling error and this is portrayed in Figure 9(a). For training data of 80%, the hazard modelling error produced by the Physical hydrodynamic model, GLOF Hazard assessment, Lake and breach Hazard assessment, HEC-RAS, Two-dimensional hydrodynamic model, Scenario-based multi-source GLOF, and ShCNNFDMN is 0.601, 0.613, 0.627, 0.669, 0.592, 0.542, and 0.484, respectively. Likewise, Figure 9(b) illustrates the examination of the ShCNNFDMN on the basis of risk prediction error. The risk prediction error measured by ShCNNFDMNis 0.463, for 80% of training data, whereas the other techniques produced risk prediction error of 0.563 for the Physical hydrodynamic model, 0.553 for GLOF Hazard assessment, 0.517 for Lake and breach Hazard assessment, 0.541 for HEC-RAS, 0.516 for Two-dimensional hydrodynamic model, 0.495 for Scenario-based multi-source GLOF. The ShCNNFDMN is examined for its efficacy on the basis of MAE and this is portrayed in Figure 9(c). For training data of 80%, the MAE produced by the Physical hydrodynamic model, GLOF Hazard assessment, Lake and breach Hazard assessment, HEC-RAS, Two-dimensional hydrodynamic model, Scenario-based multisource GLOF, and ShCNNFDMN is 0.473, 0.452, 0.446, 0.443, 0.440, 0.423, and 0.380, respectively. The R-Squared-based assessment of the ShCNNFDMN is demonstrated in Figure 9(d). The ShCNNFDMN is found to have produced a R-Squared of 0.307 with training data 80%, while the prevailing risk assessment approaches, such as the Physical hydrodynamic model, GLOF Hazard assessment, Lake and breach Hazard assessment, HEC-RAS, Two-dimensional hydrodynamic model, and Scenario-based multi-source GLOF, measured hazard modelling error of 0.370, 0.350, 0.349, 0.339, 0.320, and 0.318, correspondingly.

### 4.7. Comparative discussion

The GLOF risk/hazard assessment technique proposed in this work using ShCNNFDMN is examined for its

Table 2. Comparative discussion of the ShCNNFDMN.

| Variations       | Metrics                      | Physical<br>hydrodynamic<br>model | GLOF Hazard<br>assessment | Lake and breach<br>Hazard<br>assessment | HEC-<br>RAS | Two-dimensional<br>hydrodynamic<br>model | Scenario-based<br>multi-source<br>GLOF | Proposed<br>ShCNNFDMM |
|------------------|------------------------------|-----------------------------------|---------------------------|-----------------------------------------|-------------|------------------------------------------|----------------------------------------|-----------------------|
| K-fold           | Hazard<br>modelling<br>error | 0.613                             | 0.634                     | 0.603                                   | 0.563       | 0.557                                    | 0.507                                  | 0.473                 |
|                  | Risk<br>prediction<br>error  | 0.554                             | 0.604                     | 0.551                                   | 0.517       | 0.483                                    | 0.467                                  | 0.427                 |
|                  | MAE                          | 0.450                             | 0.442                     | 0.437                                   | 0.436       | 0.415                                    | 0.398                                  | 0.363                 |
|                  | R-squared                    | 0.348                             | 0.343                     | 0.330                                   | 0.328       | 0.325                                    | 0.313                                  | 0.297                 |
| Training<br>data | Hazard<br>modelling<br>error | 0.565                             | 0.601                     | 0.578                                   | 0.638       | 0.573                                    | 0.527                                  | <b>0.462</b>          |
|                  | Risk<br>prediction<br>error  | 0.592                             | 0.545                     | 0.592                                   | 0.466       | 0.453                                    | 0.435                                  | <b>0.423</b>          |
|                  | MAE                          | 0.439                             | 0.427                     | 0.416                                   | 0.390       | 0.382                                    | 0.371                                  | <b>0.358</b>          |
|                  | R-squared                    | 0.353                             | 0.340                     | 0.328                                   | 0.313       | 0.305                                    | 0.303                                  | <b>0.288</b>          |

efficiency considering hazard modelling error and risk prediction error with respect to other related works and this is explicated in Table 2. The values of hazard modelling error, risk prediction error, MAE, and Rsquared portrayed are recorded when k-fold value of 9 and training data of 90% are considered. The superior values of 0.462, 0.423, 0.358, and 0.288 are obtained by the ShCNNFDMN assessment based on hazard modelling error, risk prediction error, MAE, and R-Squared for 90% training data. The usage of multistage classifier developed with ShCNN and DMN based on regression analysis effectively modelled the hazard and risk values, thus minimising the risk prediction error.

##### Below are some of the factors that contribute to the proposed approach's superior performance:

The proposed ShCNNFDMN is formulated by combining the ShCNN and DMN. The key advantage of using the ShCNN is its low computational cost and its ability in realising end-to-end TVI operations for intermittently spaced data. The network attains superior results by adding a smaller number of feature maps and optimisation of the TVI process. DMN perform classification at various stages, and thus in the DMN, more refined features are used along with the shapeindexed matrix, which minimises the classification cost. Here, the DMN is mainly applied for hazard assessment due to its ability to produce superior outcomes in resource-constrained scenarios. DMN predict

Table 3. ANOVA test for the proposed method.

|             | Sum of squares | Degrees of<br>freedom | Mean squares | F    | P value   |
|-------------|----------------|-----------------------|--------------|------|-----------|
| Factor<br>1 | 14.35          | 3                     | 7.845        | 18.2 | 7.823e-05 |
| Error       | 6.15           | 15                    | 0.571254     | -    | -         |
| Total       | 19             | 17                    | -            | -    | -         |

more consistently and accurately. Thus, the proposed method ShCNNFDMN produce better performance.

### 4.8. Analysis of ANOVA Test

The ANOVA test analysis is shown in Table 3. It's known as the statistical approach. It is the procedure for breaking down the data variables into distinct parts in order to conduct further tests. To get information about the independent and dependent variables, the data are grouped using ANOVA. The F test is the another name for the ANOVA test. The ANOVA formula is written as follows:

$$F = \frac{MST}{MSE}$$

Where, F = ANOVA coefficient, MST = Mean sum of squares due to treatment, MSE = Mean sum of squares due to error.

## 5. Conclusion

This paper uses a unique deep-learning network called ShCNNFDMN to propose a fresh framework for assessing GLOF risks and hazards. In this case, evaluation is done based on a number of glacial lake attributes, including geometric, geographical, lake-based, and global attributes. First, the features are taken from the input data and evaluated by the ShCNNFDMN. Regression analysis is performed using the FC idea, and the resulting ShCNNFDMN is the result of the fusion of ShCNN and DMN. Initially, the ShCNN is trained with the geometric feature of the lake that was retrieved in the form of a shape-indexed matrix for classification. The final output and features are combined using the ShCNNFDMN layer, and for fine risk assessment, the DMN and shape-indexed matrix are applied. Superior values of 0.462, 0.423, 0.358, and 0.288 are noted in the ShCNNFDMN assessment based on hazard modelling error, risk prediction error, MAE, and R-Squared. The proposed method helps to prevent major hazards and risks. The proposed method is useful in various applications, like proper infrastructure planning, and taking preventive and mitigative actions in downstream areas of glacier lakes. The limitation of the proposed method is that it does not consider more evalution metrics to evaluate the model's performance. In future work, parameters, like the geomorphic parameters of the river channel, such as slope, and moraine can be considered to improve the risk assessment efficiency. Also, some more evaluation metrics will be considered to evaluate the model's performance.

## Disclosure statement

No potential conflict of interest was reported by the author(s).

## **Funding**

This work was supported by The International Talent Program of the Chinese Academy of Sciences [grant number 2021PC0045].

