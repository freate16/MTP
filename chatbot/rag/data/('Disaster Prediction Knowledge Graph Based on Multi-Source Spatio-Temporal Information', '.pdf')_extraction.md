

Abstract: Natural disasters have frequently occurred and caused great harm. Although the remote sensing technology can effectively provide disaster data, it still needs to consider the relevant information from multiple aspects for disaster analysis. It is hard to build an analysis model that can integrate the remote sensing and the large-scale relevant information, particularly at the sematic level. This paper proposes a disaster prediction knowledge graph for disaster prediction by integrating remote sensing information, relevant geographic information, with the expert knowledge in the field of disaster analysis. This paper constructs the conceptual layer and instance layer of the knowledge graph by building a common semantic ontology of disasters and a unified spatio-temporal framework benchmark. Moreover, this paper represents the disaster prediction model in the forms of knowledge of disaster prediction. This paper demonstrates experiments and cases studies regarding the forest fire and geological landslide risk. These investigations show that the proposed method is beneficial to multi-source spatio-temporal information integration and disaster prediction.

**Keywords:** disaster prediction knowledge graph; spatio-temporal; disaster dynamic prediction; multi-source data fusion; forest fire risk prediction; geological landslide risk prediction

Image /page/0/Picture/14 description: A graphic on a white background features a yellow circular icon with a white checkmark inside. To the right of the icon, the text 'check for updates' is displayed in a dark sans-serif font. The words 'check for' are on the top line, and the word 'updates' is on the bottom line in a bolded font.

Citation: Ge, X.; Yang, Y.; Chen, J.; Li, W.; Huang, Z.; Zhang, W.; Peng, L. Disaster Prediction Knowledge Graph Based on Multi-Source Spatio-Temporal Information. *Remote Sens.* 2022, 14, 1214. https://doi.org/10.3390/rs14051214

Academic Editors: Hideomi Gokon, Yudai Honma and Shunichi Koshimura

Received: 31 January 2022 Accepted: 26 February 2022 Published: 1 March 2022

**Publisher's Note:** MDPI stays neutral with regard to jurisdictional claims in published maps and institutional affiliations.

Image /page/0/Picture/19 description: A Creative Commons Attribution (CC BY) license icon. The icon is a rectangle divided into two horizontal sections. The top section is grey and contains two white circles with black outlines. The left circle has the letters 'CC' in black, and the right circle has a black stick figure icon. The bottom section is black with the letters 'BY' in white.

Copyright: © 2022 by the authors. Licensee MDPI, Basel, Switzerland. This article is an open access article distributed under the terms and conditions of the Creative Commons Attribution (CC BY) license (https://creativecommons.org/licenses/by/4.0/).

# 1. Introduction

Disaster is a general term for events that can have a destructive impact on humans and the environments on which they depend. Although natural disasters are inevitable, it must take efforts to greatly reduce losses. However, due to the wide distribution of natural disasters, time, location, and scale of natural disasters have great uncertainty. It greatly increases the difficulty to resist natural disasters. Therefore, the critical issue is the prediction of disasters with multi-source data of disaster scenarios for formulating emergency plans.

Remote sensing technology can obtain a large amount of strongly dynamic information in large observation ranges with high speed in real-time [1]. It can identify the fine features of ground objects, and extract information such as buildings, roads, and cultivated land by combining remote sensing technology and artificial intelligence technology. It plays an important role in the fields of disaster monitoring, early warning, and emergency decision-making. The critical problem is the fusion of different data types, different data structures, and different types of expert knowledge when the remote sensing information extraction for the multi-scale, multi-temporal, multi-type, multi-precision remote sensing

Remote Sens. 2022, 14, 1214 2 of 21

extraction information, other geographic information, and other spatio-temporal data in disaster scenes. There are studies for addressing the problem of spatio-temporal disaster information fusion, including knowledge representation of spatio-temporal disaster data, attribute analysis based on data spatio-temporal relations, and spatio-temporal dynamic geographic information of and expert knowledge.

In the real-world disaster scene, there exists large-scale multi-source heterogeneous data. There are complex associations between the data, as well as between the data and the disaster knowledge. It can effectively represent and model the data as well as the in-between relations using a knowledge graph. This is an artificial intelligence technology proposed by Google in 2012. Knowledge graph is a data modeling method that represents knowledge as concept, entity, and semantic relations with each other in the form of a graph [2]. Knowledge graphs can connect multi-source spatio-temporal disaster data and expert knowledge by a graph in order to support the analysis of the multi-source heterogeneous data under dynamic and static situations in natural disaster scenarios.

The spatio-temporal knowledge graph is a knowledge graph that can realize the semantic association of spatio-temporal data, which is the basis of disaster prediction. Sun et al. proposed a spatio-temporal knowledge graph ontology model which can manage and query spatio-temporal data in specific fields by adding spatio-temporal attribute information to entities [3]. Geographic information is a type of spatio-temporal data with spatial and temporal characteristics. Therefore, the construction technology of a geographic knowledge graph is very meaningful for this study. Zhang et al. proposed a method for constructing a geographic knowledge graph that takes the spatio-temporal characteristics into account. They studied the formal representation of geographic knowledge and laid a foundation for the acquisition, fusion, reasoning, and application of the spatio-temporal data [4]. Based on ontology, Liu et al. proposed a fast retrieval method that takes the semantic knowledge of geospatial data into account for reducing users' dependence on data storage methods and database grammar rules [5]. Jiang et al. proposed the construction process of a geographic knowledge graph, which helps to realize the knowledge of geographic information by reviewing the geographic knowledge graph [6].

At present, there exists research work regarding the construction of ontology and knowledge graph for specific disasters. Qiu et al. constructed model ontology and data ontology for flood management based on the four phases of disaster management [7]. Xu et al. constructed a conceptual model for earthquake disasters based on geo-ontology and relevant rules of earthquake emergency decision-making [8]. Scheuer et al. constructed flood risk assessment ontology by integrating SWEET ontology and MONITOR ontology [9]. Tao et al. summarized the knowledge graph construction process and key methods for the integrated comprehensive disaster reduction, and took the Jiuzhaigou earthquake as an example to demonstrate the knowledge graph construction process and construction results for Jiuzhaigou earthquake disaster reduction [10]. However, the above studies only focused on the knowledge representation and ontology construction for a single disaster type when building a knowledge model without considering the unified knowledge graph for different disaster types.

Furthermore, the existing knowledge graph models usually do not focus on strategies and rules based on common semantics so that it is hard to provide specific disaster-handling strategies in disaster emergency scenarios for supporting decision-making. The disaster prediction knowledge graph developed by Qiu et al. [7] visualizes the disaster situation. It can more autonomously determine the environmental models and disaster-related data used in different disaster phases using the semantic constraints defined in the ontology [11]. Li et al. constructed a knowledge graph for flow disasters with the personalized visualization of different scenes for multilevel users [12]. Xie et al. combined the complex semantic relationship between earthquake prevention and control entities by extracting various earthquake disaster information, and established a semantic network by constructing a knowledge graph of earthquake disaster prevention and mitigation as the core [13]. Du et al. proposed a top-down and bottom-up method for constructing a

Remote Sens. 2022, 14, 1214 3 of 21

natural disaster emergency knowledge graph [14]. They realized the transformation from multi-source data to interconnected knowledge by taking the flood disaster emergency knowledge graph as an example for experimental verification. At present, the most related research on the disaster knowledge graph respectively works on the perspectives of disaster ontology, disaster knowledge, and disaster events, particularly paying attention to construction methods. In applications, there are only domain knowledge-driven analyses. This rarely integrates dynamic disaster data and model methods deeply for the analysis based on the fused multi-feature fusion. It leads to the problem that the emergency plan cannot be flexibly adapted to the actual situations.

Affected by the attribute characteristics of surface elements, the development of disasters will show certain patterns when the disasters spatially migrate and change over time. This study selects forest fires and geological landslides as typical research objects. This paper proposes the Disaster Prediction Knowledge Graph (DPKG) that facilitates multi-source spatio-temporal data management and knowledge association. The proposed method supports semantic association of spatio-temporal data, efficient query, and quantitative analysis in order to implement information analysis with multiple types of disasters. The proposed method can be used for intelligent deduction of disaster situation and intelligent identification of disaster risk. This paper demonstrates experiments for verifying the benefits of the proposed method with respect to forest fire prediction and geological landslide risk prediction.

The main contributions of this paper are as follows: (1) This paper proposes a disaster prediction method which realizes dynamic data-driven disaster prediction based on the DPKG. (2) This paper proposes a fusion method for the dynamically changing spatio-temporal data and knowledge model. The proposed method is beneficial to improve the ability of natural disaster monitoring, early warning, and emergency response. It can provide a quantitative reference for disaster prediction and play a practical role to a certain extent.

# 2. Materials and Methods

## 2.1. DPKG Architecture

This section describes the theoretical way for mapping disaster prediction scenarios to knowledge graphs, mainly including the hierarchical semantic model of disaster prediction, and the mapping relationship between disaster prediction scenarios and DPKG architecture.

### 2.1.1. Hierarchical Semantic Model of Disaster Prediction Scenarios

The occurrence of disasters is related to a variety of factors. It facilities disaster prediction and decision-making by the analysis of disaster-inducing factors and their interrelationships.

The affect factors of occurrence of natural disasters are composed of common factors and characteristic factors. The common factors are closely related to different types of disasters. The characteristic factors are closely related to the occurrence of a certain natural disaster and weakly related to other types of natural disasters. This study establishes a hierarchical semantic model of disaster prediction considering the affect factors, which provided a theoretical basis for the construction of a conceptual layer for forest fire risk prediction and geological landslide risk prediction, as shown in Figure 1. Aiming at the prediction of forest fires and geological landslides, this paper extracts the common factors and characteristic factors of disaster occurrence by considering remote sensing information (vegetation, farmland, roads, buildings, and water bodies), terrain, meteorology, and human factors closely related to the occurrence of disasters.

Remote Sens. 2022, 14, 1214 4 of 21

Image /page/3/Figure/1 description: A flowchart illustrating the factors used for Forest Fire Risk Prediction and Geological Landslide Risk Prediction. The chart is divided into three color-coded sections. On the left, in a pink section, are "Common factors in disasters," which include Terrain (Slope, Aspect, Height), Meteorological (Wind speed, Wind direction, Precipitation, Temperature, Humidity), and Ground cover (Arable land, Woodland, Water, ......). These common factors feed into a central box labeled "Disaster Occurrence Characteristics." From this central box, the chart branches into two specific disaster types. The top right, in a blue section, details factors for "Forest Fire Risk Prediction," specifically the "Combustibles factor," which includes Vegetation types, Vegetation Coverage, Species, and Tree age. The bottom right, in a green section, details factors for "Geological Landslide Risk Prediction," specifically "Geological factors," which include Stratigraphic lithology, Fault structure, Surface roughness, Surface relief, Plane curvature, and Section curvature. Brackets indicate that the common factors combined with the combustibles factor lead to Forest Fire Risk Prediction, and the common factors combined with geological factors lead to Geological Landslide Risk Prediction.

**Figure 1.** A hierarchical semantic model for disaster prediction scenarios regarding forest fires and geological landslides.

### 2.1.2. Mapping between Disaster Prediction Scenarios and DPKG Architecture

For modeling disaster prediction using a knowledge graph, it is necessary to represent the disaster prediction scenario as the hierarchical semantic model. It maps the data with spatio-temporal characteristics in the disaster prediction scenario into the DPKG according to the structure of the semantic model. The disaster analysis model can be transformed into knowledge. The DPKG also needs to integrate the transformed disaster analysis model and expert knowledge for disaster prediction.

In addition, the architecture design of the DPKG for disaster prediction needs to consider the fusion of multi-source heterogeneous spatio-temporal data including remote sensing extraction information, terrain, meteorology, vegetation, and human factors, as well as the fusion of spatio-temporal data with disaster analysis models and expert knowledge for linkage analysis. This study designs an architecture of DPKG for disaster prediction, as shown in Figure 2, in order to support the modeling of disaster prediction and the collaborative analysis with fused data.

Image /page/3/Figure/6 description: A flowchart diagram illustrating the 'DPKG architecture'. The architecture is divided into several components within nested boxes. The main section is split into two parts: 'Set of rules (TBox)' and 'Set of facts (ATox)'. The 'Set of rules (TBox)' contains a 'Conceptual layer' (with 'Space ontology', 'Time ontology', and 'Common semantic ontology of disaster prediction') and 'Inference rules' (with 'First-order logical reasoning rules', 'Production inference rules', and 'Spatio-temporal semantic reasoning rules'). The 'Set of facts (ATox)' shows a flow where 'Unstructured data', 'Semi-structured data', 'Structured data', and 'Disaster prediction reasoning criterion' feed into a 'Knowledge extraction' process, which results in a 'Set of facts (ABox)'. An arrow points from this main section to two modules at the bottom: 'Disaster fusion data spatio-temporal semantic query module' and 'Disaster prediction rule reasoning module'.

Figure 2. DPKG architecture.

Remote Sens. 2022, 14, 1214 5 of 21

The DPKG for disaster prediction consists of two parts, namely the rule set (TBox) and the fact set (ABox). The TBox consists of the conceptual layer and the inference rules. The conceptual layer is the common semantic basis for describing the hierarchical relationship of various factors in disaster prediction scenarios. The inference rules are the common logic basis for multi-source spatio-temporal data that supports semantic reasoning. The ABox constitutes the instance layer of the knowledge graph, which contains the time, space, status, and other attribute information of various types of ground objects related to disaster emergency extracted from multi-source heterogeneous data. The ABox and the TBox constitute the reasoning basis of the DPKG. Through the rapid retrieval of spatio-temporal data in disaster areas, multi-source spatio-temporal data analysis can be realized. The architecture diagram will be described in detail later.

## 2.2. Construction of Disaster Prediction Knowledge Graph

This section introduces the knowledge representation language, the design of the conceptual layer and instance layer, and the knowledge representation of the disaster prediction model.

### 2.2.1. Knowledge Representation Language

Knowledge graph representation refers to the use of computer symbols to scientifically mark the objectively existing knowledge for facilitating the semantic reasoning [15].

OWL (Web Ontology Language) is a semantic description standard including three sub-languages: OWL-Lite, OWL-DL, and OWL-Full. At present, OWL is the most standardized, rigorous, and expressive language for a knowledge graph. The commonly used knowledge representation form is RDF (Resource description framework) triples. Each piece of knowledge can be represented as the following triple format: (subject, predicate, object), such as (vegetation, yes, combustible). This study chooses OWL as the knowledge representation language.

### 2.2.2. Design of Conceptual Layer

The conceptual layer of the DPKG is a logical structure for multi-source spatiotemporal data. It contains semantic concepts and their interrelationships. Based on the semantic associations between different concepts, such as the subordinate relationship, attribute subject-object relationship, a tree-like hierarchical concept triple interconnection network is constructed for ensuring the consistence of the intrinsic semantic concepts of multi-source spatio-temporal data. The conceptual layer of disaster prediction DPKG is composed of time ontology, space ontology, and disaster prediction common semantic ontology.

#### 1. Common Semantic Ontology of Disaster Prediction

The dynamic prediction of forest fires and geological landslide disasters needs the semantic reasoning and collaborative computing of multi-source spatio-temporal data.

For this goal, this paper proposes a tree-like taxonomy of multi-source concepts of geographic entity associated with multi-source spatio-temporal data. According to the taxonomy, concepts of geographic entity are divided into five fields. This paper defines the domain attribute predicates related to the concepts of each geographic entity.

The concepts of geographic entity constitute a common semantic ontology for the prediction of forest fire and geological landslide disaster.

The storage model of common semantic ontology is hierarchical and expandable. It builds the foundation for the predicate logic reasoning based on the common hierarchical semantic relationship of disaster prediction, as shown in Figure 3.

Remote Sens. 2022, 14, 1214 6 of 21

Image /page/5/Figure/1 description: A black and white flowchart titled 'Conceptual Framework of Disaster Prediction KG'. The main concept branches into three categories: 'Time object', 'Space object', and 'Role object'. 'Time object' further divides into 'Effective time' and 'Time granularity'. 'Space object' divides into 'Geographic description' and 'Features'. 'Role object' divides into 'Mechanism' and 'Post'. The 'Features' category from 'Space object' is connected to a lower level of five boxes: 'Ground cover', 'Meteorological', 'Topography', 'Geology and lithology', and 'Historical disaster'.

Figure 3. Common semantic ontology of disaster prediction.

#### 2. Time Ontology

Time ontology provides a specification of unified time semantic representation in order to ensure that the time information of entities is comparable and computable. This paper leverages the Semantic Web Rule Language (SWRL) time ontology proposed by Stanford University for representing the common time concepts of the DPKG [16]. The logical structure of the SWRL time ontology is shown in Figure 4.

Image /page/5/Figure/5 description: A diagram illustrating a data model or ontology for time-related concepts. It shows several colored rectangular boxes connected by labeled arrows. A pink box labeled "ExtendProposition" connects to a central blue box "ValidTime" via two arrows: a solid one labeled "hasValidTime" and a dotted one labeled "hasPredictTime". The "ValidTime" box connects to a yellow box "Granularity" with an arrow labeled "hasGranularity". Below "ValidTime", a light green box "ValidInstant" and a yellow box "ValidPeriod" are shown as subclasses, indicated by arrows labeled "SubClassOf" pointing to "ValidTime". At the bottom, a large red box is labeled "xsd::DateTime". "ValidInstant" has an arrow labeled "hasTime" pointing to "xsd::DateTime". "ValidPeriod" has two arrows pointing to "xsd::DateTime", one labeled "hasStartTime" and the other "hasFinishTime".

Figure 4. SWRL temporal ontology.

#### Space Ontology

The expression of spatial ontology applies A Geographic Query Language for RDF Data (GeoSPARQL) [17] that is a geographic semantic query specification proposed by OGC (Open Geospatial Consortium) [18]. The geographic semantic query mainly includes the following three common contents.

#### OWL Ontology Vocabulary

It represents all feature entities as subclasses of Spatial Objects. All geometric objects can be subdivided into points, linestrings, and polygons. Geometric objects are represented using features and geometric objects (Geometry) and their defined relationships, as shown in Figure 5.

Image /page/5/Figure/11 description: A class diagram illustrates the relationships between different spatial object types, prefixed with 'ogc:'. At the top is the superclass 'ogc:SpatialObject'. Two classes, 'ogc:Feature' and 'ogc:Geometry', inherit from 'ogc:SpatialObject'. There is a directed association from 'ogc:Feature' to 'ogc:Geometry' labeled 'ogc:hasGeometry'. Three other classes, 'ogc:Point', 'ogc:LineString', and 'ogc:Polygon', all have arrows pointing to the 'ogc:Geometry' class. The 'ogc:Geometry' class is detailed in a larger box with two sections: 'Metadata' and 'Serialization'. Under 'Metadata', the properties are listed as: 'ogc:dimension : xsd:int', 'ogc:coordinateDimension : xsd:int', 'ogc:spatialDimension : xsd:int', 'ogc:isEmpty : xsd:boolean', 'ogc:isSimple : xsd:boolean', and 'ogc:is3D : xsd:boolean'. Under 'Serialization', the properties are 'ogc:asWKT' and 'ogc:WKTLiteral'.

Figure 5. GeoSPARQL part of the ontology table.

Remote Sens. 2022, 14, 1214 7 of 21

#### Geometry extension expression

The GeoSPARQL specification follows the OGC standard for the expression format of point, line, and surface. For example, the coordinate information of a surface data will be recorded in the attribute of *ogc:asWKT*, where *WKT* stands for Well Known Text, which is the ASCII code representation method of spatial objects.

#### Topology extension query

GeoSPARQL specifies eight query relationships for all spatial objects, as shown in Table 1. In addition, it provides many commonly used distance query functions (*geof:distance*), buffer query functions (*geof:buffer*), and convex Package constructor (*geof:convexHull*), to enhance spatial query.

Table 1. GeoSPARQL spatial topological relationship.

| geof:sfEquals  | geof:sfDisjoint | geof:sfIntersects | geof:sfTouches  |
|----------------|-----------------|-------------------|-----------------|
| geof:sfCrosses | geof:sfWithin   | geof:sfContains   | geof:sfOverlaps |

### 2.2.3. Construction of Disaster Prediction Inference Rules

#### Construction of First-Order Logical Inference rules

First-order logic (FOL) is a formal system used in mathematics, philosophy, linguistics, and computer science. Specifically, hierarchical relationships and object attribute relationships can be described as first-order predicate logic, as shown in Figure 6. The common ontology, time ontology, and space ontology of disaster prediction are formally modeled with OWL language. The hierarchical relationship and attribute relationship implies a series of first-order logical reasoning.

```
1
```

Figure 6. Hierarchical relationship and object attribute relationship.

#### 2. Construction of Production Inference rule

Due to the limitation of the knowledge representation of first-order logic, this paper applies SWRL (Semantic Web Rule Language). It extends the set of OWL axioms to include Horn-like rules. In this study, SWRL is used to further enhance the expression of rules for DPKG. A rule has the form, where both antecedent and subsequent are conjunctions of atoms written. Using this syntax, a rule asserting that the combination of the tree species' properties and the tree species' forest fire risk-level properties implies the tree's forest fire risk-level properties, as shown in Figure 7.

```
\langle species(?x,?y) \land forestFireRiskLevel(?y,?z) \Rightarrow forestFireRiskLevel(?x,?z) \rangle
```

**Figure 7.** SWRL inference rule example.

#### 3. Construction of Spatio-Temporal Semantic Inference Rule

Although SWRL can support basic quantitative calculations, it cannot support quantitative analysis of space and time including spatio-temporal semantics. This study leverages the construction method of production inference rules to build the spatio-temporal semantic inference rules. The spatio-temporal semantic inference rule *RuleObject* is a set of rules for the automatic execution of reasoning programs by the DPKG. Each rule is composed

Remote Sens. 2022, 14, 1214 8 of 21

of an event object TriggerObject and an action object ActionObject, which are expressed as RuleObject = (Tr, Ac), where Tr represents the event contained in the RuleObject, Ac represents the action object ActionObject contained in the RuleObject, and R is the reasoning result. The event TriggerObject in this article is defined as a triple that is represented as TriggerObject = (O, T, S), where O represents the geographic entity set contained in the event object, T and S respectively represent the intersection of the geographic entity set in the time dimension and the space dimension. A spatio-temporal co-occurrence scene with a set of geographic entities can be described as an event object that is a definition of the applicable conditions of an inference rule.

The event (or action) object concept is further subdivided into independent events (or actions) and event (or action) combinations, which together form the concept of knowledge inference rules. The logical structure is shown in Figure 8.

Image /page/7/Figure/3 description: A hierarchical diagram illustrating the structure of a 'RuleObject'. The 'RuleObject' is at the top and branches into two main components: 'TriggerObject' on the left and 'ActionObject' on the right. The 'TriggerObject' branch is further subdivided. It points to 'IndependentTrigger' and 'TriggerCombination'. 'IndependentTrigger' then points to 'NormalTrigger' and 'AbnormalTrigger'. 'TriggerCombination' points to 'AndTrigger Combination' and 'OrTrigger Combination'. The 'ActionObject' branch is similarly subdivided. It points to 'IndependentAction' and 'ActionCombination'. 'ActionCombination' then points to 'AndAction Combination' and 'OrAction Combination'. There are also arrows pointing upwards, indicating relationships back to parent objects. For instance, on the right side, arrows point from 'IndependentAction' and 'ActionCombination' back to 'ActionObject', and from 'AndAction Combination' and 'OrAction Combination' back to 'ActionCombination'. A similar pattern of upward-pointing arrows exists on the 'TriggerObject' side of the diagram.

Figure 8. Schematic diagram of the conceptual hierarchy of knowledge inference rules.

### 2.2.4. Design of Instance Layer

#### Knowledge Extraction from Unstructured Data

The dynamic disaster prediction of forest fires and geological landslides requires high spatio-temporal resolution of land cover data. This paper uses Gaofen-2 satellite remote sensing images with the resolution of 0.8 m as the data source. The spatial distribution of disaster-bearing bodies such as buildings and roads is extracted by deep learning methods. The spatial distribution of surface vegetation is obtained by NDVI numerical calculation method [1,19]. It converts the spatial information into triples according to the specification of spatio-temporal and professional attribute representation defined by the concept layer. The triples are stored in the graph database *GraphDB*.

#### 2. Knowledge Extraction from Semi-Structured Data

The terrain data for dynamic disaster prediction of forest fires and geological landslide is the raster geographic data with GeoTIFF format. It converts all types of raster data into vector data of surface elements. It converts geological and lithological data including stratigraphic age, fault, and lithology distribution data into vector geographic information with SHP format. For all types of vector geographic information, it converts the spatial information and feature attributes into triple that are stored in *GraphDB*.

#### 3. Knowledge Extraction from Structured Data

The meteorological data for the dynamic disaster prediction of forest fires and geological landslide is multi-field structured data, which has a direct mapping relationship with the spatio-temporal and professional attributes. Since the vast majority of meteorological data is normal non-hazardous data, this paper only converts the spatial information element attributes of potential disaster-causing meteorological indicators into a triple, so as to avoid the low reasoning speed caused by a large amount of irrelevant data to the reasoning. The triple is stored in *GraphDB*.

Remote Sens. 2022, 14, 1214 9 of 21

#### 4. Knowledge Extraction from Disaster Prediction Reasoning Criterion

This paper introduces the knowledge extraction method by taking the geological landslide prediction model as an example. It is hard to build a general prediction model for a geological landslide because a single model with idiosyncratic conditions cannot deal with the rich types of geological landslide prediction models and the involved data. This paper defines the inference rules for the geological landslide disaster prediction according to the geological landslide risk probability calculation using machine learning and the effective precipitation models. Based on the general law of geological landslide risk analysis [20], this paper selects the H-index shown in Formula (1) as the metric for the quantitative evaluation of the geological landslide risk:

$$H = P_{(T)} \times P_{(S)} \times P_{(I)}, \tag{1}$$

where H is the risk probability of geological landslide disasters within a specific time and space range;  $P_{(T)}$  is the time probability, i.e., the probability of geological landslide disasters occurring within a specific time range;  $P_{(s)}$  is spatial probability, i.e., the probability of geological landslide disasters occurring within a specific spatial range;  $P_{(I)}$  is the intensity probability, i.e., the intensity of possible geological landslide disasters.

This paper introduces a time probability model based on dynamic precipitation data. The model is mainly composed of two parts. One is the effective precipitation; another is the fitting relationship between the effective precipitation and the frequency of geological landslides. The effective precipitation R in the region considers the respective precipitation contributions of the previous days to the cumulative precipitation that causes the geological landslide. The later the time, the greater the contribution rate to the geological landslide.

$$R = R_0 + \alpha_1 R_1 + \ldots + \alpha_n R_n, \tag{2}$$

where  $R_0$  is the daily precipitation;  $\alpha$  is the contribution rate; n is the number of precipitation days, and  $R_n$  is the precipitation on the n-th day before. A linear fitting relationship between the effective precipitation and the frequency of geological landslides is defined for the time probability of geological landslides associated with dynamic precipitation data.

The geological landslide strength is considered as a parameter representing the destructive force of the geological landslide. It includes the volume of the geological landslide, and the sliding velocity. At present, there is no unified set of indicators to describe them. In this paper, the geological landslide volume parameter is used to obtain the geological landslide strength, and the formula is as follows:

$$m_L = log V_{L}, \tag{3}$$

where  $V_L$  is the volume of a single geological landslide with the unit of m<sup>3</sup>; which is calculated based on DEM, and  $m_L$  represents the strength of a single geological landslide. By calculating the strength of each geological landslide in the study area by the above formula, it can obtain the statistics of geological landslide strength according to the frequency.

There are many common factors that lead to forest fires and geological landslides. Certain triggering factors can be monitored when forest fires and geological landslides occur. The development of the two types of disasters will develop and spread within a certain time and space range. Affected by the attribute characteristics of surface elements, both disasters will show certain change patterns when they dynamically migrate and change in space over time. Therefore, this paper extends the geological landslide risk calculation formula to forest fires by considering the above-mentioned commonalities of the two disasters. It builds the unified prediction model for forest fire according to Formula (1). Based on Analytic Hierarchy Process, it builds the forest fire-driven comprehensive index for forest fire risk prediction model.

Remote Sens. 2022, 14, 1214 10 of 21

## 2.3. Query and Reasoning of Disaster Prediction DPKG

### 2.3.1. Spatio-Temporal Semantic Query for Disaster Fusion Data

When a specific attribute of the external dynamic data satisfies the numerical conditions defined by the rule, it is regarded as an abnormal event candidate. Its time range and space range are treated as the basic condition of semantic query. It queries with SPARQL Protocol and RDF Query Language (SPARQL) [21] statements for a geographic entity that has an intersection with the abnormal event candidate and satisfies the reasoning conditions. When querying the spatio-temporal relationship in the graph database, it can quickly locate the affected area of the abnormal event candidate because the graph database is good at efficient depth-first query, as shown in Figure 9. It plays an important role in the emergency field with high response speed requirements.

#### Disaster prediction reasoning flow chart

Image /page/9/Figure/5 description: A flowchart illustrating a process for handling dynamic data to identify and query abnormal events. The process begins at a 'Start' node and proceeds to 'Real-time input of dynamic data (such as meteorological data)'. Next, a decision is made in an oval labeled 'Judging the dynamics Whether the data attribute satisfies the condition'. If the condition is not met ('No'), the process goes directly to the 'End' node. If the condition is met ('Yes'), the flow continues to 'Generate abnormal events to be judged based on the spatiotemporal scope of external dynamic data'. This is followed by 'Based on the abnormal events to be determined and the geographic location affected by the abnormal events Entity Type Generate Query Statement'. The next step is 'With the help of efficient in-depth retrieval of graph database, the area affected by abnormal events can be quickly locked'. This leads to the final process step, 'Query to get the affected geographic entities within the scope of the abnormal event', which then connects to the 'End' node.

Figure 9. Disaster prediction query flow chart.

With the help of the spatio-temporal semantic query of the disaster fusion data, it can quickly find geographic entities located within the temporal and spatial scope of the AbnormalTrigger based on the temporal-spatial intersection relationship in order to filter the buildings and roads affected by the AbnormalTrigger, as shown in Figure 10.

Image /page/9/Figure/8 description: A conceptual diagram on a 2D coordinate system. The horizontal axis is labeled "spatial dimension" and the vertical axis is labeled "time dimension". The diagram features two large, overlapping ovals. The oval on the left is light green and is associated with the green text "Spatio-temporal distribution of buildings and roads", with a green arrow pointing up from the oval to the text. The oval on the right is light orange and is associated with the orange text "Spatial and temporal distribution of AbnormalTrigger", with an orange arrow pointing up from the oval to the text. The overlapping area of the two ovals is colored reddish-pink. A pink arrow points from this intersection to the text below, which reads "Buildings and roads affected by AbnormalTrigger" in pink.

**Figure 10.** Schematic diagram of the spatio-temporal intersection of anomalous events and geographic entities.

In order to ensure the efficiency of spatial information query in disaster emergency scenarios, this paper builds multi-scale geocoding indexes for multi-source geographic entities in GeoSPARQL. It significantly improves the depth-first query speed of random geospatial information in comparison with the frequent joint query of multiple tables in the relational database.

Remote Sens. 2022, 14, 1214 11 of 21

### 2.3.2. Disaster Prediction Rule Reasoning

#### 1. First-order logical reasoning

As defined in the Common Semantic Ontology of Disaster Prediction, surface combustibles include Woodland, Farmland, Building, and Grassland, and Coniferous Forest belongs to Woodland. Based on first-order logical reasoning, it concludes that Coniferous Forest belongs to Surface Combustibles. With the prefix of *hazard*, the above process can be formally defined as shown in Figure 11. Based on these expressions, *(hazard : Coniferous Forest rdf : subClassOf hazard : Surface Combustibles)* can be inferred.

```
1
```

Figure 11. First-order logical reasoning process.

#### 2. Production reasoning

This paper takes SWRL rule reasoning as an example. The feasible reasoning on the DPKG includes reasoning of geographic entity from one attribute to other attributes; reasoning from one geographic entity and its attributes to geographic entities and their attributes.

For example, given the forest fire risk entity and its attribute, i.e., the comprehensive forest fire-driven index *fireDangerValue*, the goal is to build an inference rule for the forest fire risk-level prediction. For this task, the domain analysis rule "when fireDangerValue > 3.8, fireDangerLevel is level 3" is formalized as shown as line 1 in Figure 12.

```
1
```

Figure 12. Production reasoning process.

One more example, knowing the value of aspect entity and aspect attribute, the goal is to construct an inference rule to infer the upslope aspect value. For this task, the domain analysis rule "When aspect is  $<180^{\circ}$ , upAspect = aspect +  $180^{\circ}$ " is formalized as shown as line 2 in Figure 12.

The prediction can be carried out using the SWRL reasoning engine with the inference rules.

#### 3. Spatio-temporal semantic reasoning

This paper builds an automatic real-time monitoring mechanism for emergency information for disaster prediction. It extracts the dynamic information related to the occurrence and development of disasters, i.e., attributes such as space, time, and status of target objects, from structured, semi-structured, and unstructured data sources. It encapsulates the extracted information into real-time event message objects with GeoJSON format. The update of dynamic data will trigger the automatic judgment by the DPKG as shown in Figure 13. The results drive the chained reasoning workflow defined by the disaster prediction inference rules.

Remote Sens. 2022, 14, 1214 12 of 21

#### **Calculation process**

Image /page/11/Figure/2 description: A flowchart titled 'Calculation process' illustrates a system for predicting geological and forest fire risks. The process begins with two inputs: 'Weather forecast data for the next 7 days (updated at 8:00 and 20:00 daily)' and 'Weather monitoring data (lag about 10-20 minutes, updated every 5 minutes)'. Both are fed as 'input' into a process called 'Instance layer dynamic update'. The output of this stage is then used as 'input' for the central calculation step, 'The triplet disaster prediction model starts the calculation'. This model also utilizes 'Spatio-temporal knowledge graph data'. The model produces two 'output' streams: 'Prediction results of geological landslide risk in the next 7 days' and 'Forecast results of forest fire risk in the next 7 days'. The flowchart also includes two dashed lines indicating dependencies. The top line states, 'Forecast days depend on the availability of weather forecast data', connecting the forecast data to the final predictions. The bottom line states, 'Actual real-time performance depends on the lag of meteorological monitoring data', connecting the monitoring data to the final predictions.

Figure 13. Workflow of disaster dynamic prediction.

This paper designs a chain-type automatic reasoning method based on the reasoning criterion. The method divides the calculation logic of the geological landslide prediction model into a series of antecedents and consequences. The antecedents are execution conditions that contain a series of geographic entities. When there exists an intersection of the geographic entities and the conditions set in the antecedent are met, the subsequent associated with the antecedent, i.e., the action object, will be triggered.

It establishes the automatic flow logic between independent criteria such as time probability, space probability, intensity probability, vulnerability of hazard-affected body, and value amount by defining for RuleObject. In this way, it can analyze the relations between time information and space information, which is not feasible using the production reasoning with SWRL.

# 3. Results

This section demonstrates experiments and cases studies of the forest fire and geological landslide risk based on DPKG. These investigations show that the proposed method is beneficial to multi-source spatio-temporal information integration and disaster predictions.

## 3.1. Case Study: Forest Fire Risk Prediction

In this case study, Yanyuan County, in the Liangshan Yi Autonomous Prefecture of China's Sichuan Province, was selected to carry out a dynamic prediction experiment of forest fire disasters. Yanyuan County is located between  $100^{\circ}42'09''-102^{\circ}03'44''$  east longitude and  $27^{\circ}06'31-28^{\circ}16'31''$  north latitude, with a total area of 8398.6 square kilometers. There are rich vegetation and many miscellaneous irrigation and thatch grass in the area. The forest fire disasters are easily caused by the inducing factors such as low rainfall. Therefore, Yanyuan County strongly needs to forecast the situation in advance.

In this case, multi-source heterogeneous data related to forest fire risk prediction are collected, such as vegetation data, terrain data, meteorological data, and land cover data. In order to fully represent the spatio-temporal features of the above data in the DPKG knowledge graph, this paper uses Protégé to construct a time ontology and a space ontology. The concepts related to forest fire prediction form the conceptual layer of DPKG. For the above-mentioned multi-source heterogeneous data, we built a diversified knowledge extraction method for transferring the data into triples according to the semantics of the conceptual layer.

The triples form an instance layer of the DPKG of disaster prediction. An example of the extraction process of the slope in the terrain data is shown in Figure 14.

Remote Sens. 2022, 14, 1214 13 of 21

Image /page/12/Figure/1 description: A diagram illustrates a data processing workflow for geographic information. The flow starts with a TIFF file, a raster image of a geographical area. An arrow labeled 'Raster to Vector' points to a Shapefile, which is a colored vector map of the same area. From the Shapefile, an arrow labeled 'Vector to GeoJSON' points to a code snippet of a GeoJSON file. The GeoJSON code shows a 'FeatureCollection' with properties for a 'Slope'. An arrow labeled 'GeoJSON to Triple' points from the GeoJSON to a knowledge graph representation. This graph has a central node 'SlopeEntity' connected to four other nodes via labeled edges: 'hasSlope' points to '21', 'hasTileCode' points to 'z20\_x322\_y786', 'hasTime' points to '2021-10-27 01:17', and 'hasCenterLonLat' points to '102.98438°E, 26.502315°N'.

Figure 14. Knowledge extraction process using slope as an example.

Forest fire risk prediction needs the theoretical support because the above spatiotemporal data is only a prerequisite for forest fire risk prediction. In this case, the AHP (Analytic Hierarchy Process) is used to evaluate forest fire risk indicators. This paper builds an indicator system for four types of forest fire risk factors: meteorology, terrain, vegetation, and man-made. The weights are shown in Figure 15.

Image /page/12/Figure/4 description: A flowchart diagram illustrating the 'Comprehensive Index of Forest Fire Drivers'. This main index branches into four primary factors, each with a numerical weight. The 'Vegetation factor' has a weight of 0.24 and is subdivided into 'Vegetation Types' (0.18) and 'Canopy' (0.06). The 'Meteorological factor' has the highest weight of 0.40 and is broken down into four sub-factors: 'Wind speed' (0.10), 'Precipitation' (0.10), 'Temperature' (0.10), and 'Humidity' (0.10). The 'Terrain factor' has a weight of 0.21 and includes 'Slope' (0.10), 'Aspect' (0.06), and 'Height' (0.05). Finally, the 'Human factor' has a weight of 0.15 and is represented by a single sub-factor, 'Festival' (0.15).

Figure 15. Forest fire risk factor indicator system.

The comprehensive indicator of forest fire driving factors is defined as Formula (4):

$$CIFFD = \sum v_i \times w_i \ i \in [1, 10], \tag{4}$$

where *CIFFD* represents a composite index of forest fire drivers;  $v_i$  indicates the level corresponding to the original value of the factor, and  $w_i$  indicates the weight corresponding to the factor. The larger the CIFFD, the greater the risk of forest fires.

In this case, 10 factors in four categories of terrain, vegetation, meteorology, and human factors in the experimental area are used as the query input for the DPKG instance layer. The definition in Formula (4) is transformed into spatio-temporal semantic reasoning rules. The reference output is a comprehensive index of forest fire driving factors.

Define spatio-temporal semantic inference rule 1: If the update of meteorological data is detected, it divides the spatial range of the meteorological data update into several rectangular areas. The rectangular areas automatically triggers the query of 10 factors of

Remote Sens. 2022, 14, 1214 14 of 21

terrain, vegetation, meteorology, and human factors in the rectangular areas for obtaining the original value of the factor.

Define spatio-temporal semantic inference rule 2: It obtains the corresponding level value based on the original value of the factor. Based on Formula (4), the comprehensive index of forest fire driving factors is obtained.

Define spatio-temporal semantic inference rule 3: Based on the natural discontinuity method, the calculated comprehensive index of forest fire driving factors is divided into 7 intervals for representing different degrees from low to high. The forest fire risk warning information of the experimental area is obtained, as shown in Figure 16.

Image /page/13/Figure/4 description: A flowchart diagram titled "Semantic inference of forest fire disaster". The diagram is divided into three vertical sections by dashed lines, labeled "Rule one", "Rule two", and "Rule three".

In "Rule one", the process starts with "Meteorological data update", which leads to "Divide rectangular area". An arrow points from this to a box labeled "Query regional forest fire-related factors".

An arrow from "Rule one" points to "Rule two". In this section, there are two icons: a square with a diagonal line and a circle inside, and a stacked triangle. Below them, the text reads "Gets the corresponding level value". This leads to a box labeled "Forest fire driver composite index".

An arrow from "Rule two" points to "Rule three". In this final section, there is a bar chart with bars of increasing height, labeled "Forest fire driving factor composite index divided into intervals". The process concludes in a box labeled "Get rank".

Figure 16. Forest fire risk factor index system.

The antecedent rules in the above spatio-temporal semantic inference rules can trigger the subsequent rules when satisfying the conditions. Therefore, the dynamic changes of meteorological data can automatically trigger the forest fire risk calculation. It realizes the automatic completion of the chain reasoning of the whole process of DPKG without manual effort.

In this case, the actual meteorological record data of Yanyuan County Meteorological Observatory on 3 January 2022 is used as the query input of the instance layer of the DPKG. The output is calculated based on the reasoning of the DPKG.

For the forest fire risk index of the whole county of Yanyuan, the larger the index value, the higher the forest fire risk. The experimental results are shown in Figure 17.

Image /page/13/Figure/9 description: A map displaying the Forest Fire Risk Index for an irregularly shaped geographical area. The map uses a color scale to represent different levels of risk. A legend on the left side details the index values corresponding to each color: dark green for 0.85-2.90, medium green for 2.91-3.60, light green for 3.61-4.00, yellow for 4.01-4.10, light orange for 4.11-4.20, orange for 4.21-4.60, and red for 4.61-5.29. Scattered across the map are several purple dots, which the legend identifies as 'January 3, 2022 06:35 fire point'. In the bottom right corner, there is a scale bar marked in miles, with increments shown at 0, 3, 6, 12, 18, and 24 miles.

**Figure 17.** Map of landslide hazards in Yanyuan County based on multi-Graded Cascade Random Forest.

Remote Sens. 2022, 14, 1214 15 of 21

NASA's Fire Information for Resource Management System shows the actual fire point in Yanyuan County at 6:35 on 3 January 2022, as shown in Figure 17. The results show that the proposed method successfully hits the fire point of the forest fire species within the time and space range of the predicted forest fire risk index greater than 4.21.

The case uses the traditional spatial analysis tool ArcGIS as a baseline method to calculate the forest fire risk in Yanyuan County for the comparative experiments. It is necessary to load and query Yanyuan County data from 14 types of raster datasets. Steps such as uniform coordinate system, uniform pixel size, grid cropping, and stitching are performed on each raster data, and then the prediction calculation can be performed. There are many steps in the baseline operation, and the whole process takes more than 190 min. When using the grid calculator, the performance is low because it needs complex numerical computations in multiple steps.

In addition, the boundaries of various data are not completely coincident, which will lead to missing or abnormal results of the boundary area analysis, and wrong predictions. Although it is possible to forcibly align the pixel positions by means of translation, it will cause errors by an operation that lacks a realistic basis, and changes the spatial distribution of the original data. In addition, it has a low prediction efficiency when using the traditional spatial analysis tools because they cannot process other target regions in parallel.

## 3.2. Case Study: Geological Landslide Risk Prediction

In another case study, Xiji County in Guyuan City of China's Ningxia Hui Autonomous Region is selected to carry out an experiment regarding the dynamic prediction of geological landslide hazards. Xiji County locates between  $105^{\circ}20'-106^{\circ}04'$  east longitude and  $35^{\circ}35'-36^{\circ}14'$  north latitude, which has a total area of 3130 square kilometers. In this area, the loess landslide disaster caused by the Haiyuan earthquake is particularly serious because of the special geological environmental conditions. It has formed 765 geological landslides [22]. It is very dangerous that new geological landslide disasters are easily generated by the inducing factors, e.g., rainfall. Therefore, it is urgent to take an effective method to predict disaster in advance.

In this case, the basic geological data, basic geographic data, hydrological data, human activities, and land is collected for the prediction and calculation of geological landslide risk. In order to fully represent the spatio-temporal features of the above data in the knowledge graph, this paper uses Protégé [23] to construct a time ontology and a space ontology, and concepts related to geological landslide prediction form the conceptual layer of spatial-temporal knowledge graph for disaster prediction. For the above-mentioned multi-source heterogeneous data, a diversified knowledge extraction method is adopted to convert the data into triples according to the semantics of the conceptual layer. It forms the instance layer of the DPKG for disaster prediction using the triples.

The above spatio-temporal data is only a prerequisite for geological landslide risk prediction. It needs the theoretical support of the geological landslide risk prediction. The landslide risk assessment is defined as Formula (2). Geological landslide risk prediction involves time, spatial, and intensity probability. In this case, there are 13 factors belonging to four categories of topography, geology, lithology, meteorology and hydrology, land cover, and human activities in the experimental area. The information of the factors is queried from the knowledge graph. It takes the DEM factors in the topographic data as the query input of the instance layer of the knowledge graph. The linear fitting model between historical landslides and DEM data is transformed into spatio-temporal semantic reasoning rules, as shown in Figure 18. In this way, the spatial probability of landslide disasters in the experimental area can be calculated.

Remote Sens. 2022, 14, 1214 16 of 21

Image /page/15/Figure/1 description: A flowchart illustrating a model for calculating Geological Landslide Risk Probability. At the top, a computer monitor icon is labeled "Geological Landslide Risk Probability," which points to a formula: H = P(T) × P(S) × P(I). The flowchart has two main input branches. The first branch combines three inputs: "The local precipitation data for the past 10 days is an empirical function of the independent variable," "Deep Random Forest Model," and "Linear fit model between historical landslides and DEM data." These are processed through a step called "Knowledge Representation" to generate "Spatiotemporal Semantic Reasoning Rules." The second branch combines three other inputs: "Precipitation rate," "Topography, Geology and lithology, Meteorology and hydrology, Land cover and human activities," and "DEM." These are processed through a step called "Instantiate" to create a "Disaster prediction spatiotemporal knowledge graph instance layer." This instance layer provides "Data Support" to the "Spatiotemporal Semantic Reasoning Rules." Finally, the "Spatiotemporal Semantic Reasoning Rules" are used to derive the three probabilities P(T), P(S), and P(I) for the final risk calculation.

Figure 18. Geological landslide risk prediction calculation formula.

The time probability is a dynamic element. In this case, the time probability is defined as the empirical function with the independent variable of the local precipitation data in the past 10 days, as shown in Formula (3). It transforms Formula (3) into spatio-temporal semantic inference rules, and the time probability of landslide disaster occurrence in the experimental area.

Define spatio-temporal semantic inference rule 1: If the time probability satisfies specific conditions, it is defined as a dangerous time probability.

Define spatio-temporal semantic reasoning rule 2: For a new dangerous time probability, the calculation of the spatial probability and the intensity probability will be automatically triggered. The spatial distribution of the geological landslide risk value in the test area will be calculated according to Formula (1).

Define spatio-temporal semantic inference rule 3: Based on the natural discontinuity method, the geological landslide risk probability value calculated by the previous rule is divided into 10 intervals in ascending order, representing different degrees, every two intervals are combined into a grade for a total of five grades, as shown in Figure 19.

Image /page/15/Figure/7 description: A flowchart diagram titled "Semantic reasoning of landslide disaster" is divided into three sections labeled "Rule one," "Rule two," and "Rule three." In "Rule one," two inputs, "Day time probability" and "Nearest time interval time probability," feed into a box labeled "Time probability of dangerous geological landslide." An arrow from this box leads to "Rule two." In "Rule two," the process is described as "Geographic grid computing," represented by an icon of a map with a grid overlay. This process results in the "Spatial distribution of geological landslide risk values." An arrow from this result leads to "Rule three." In "Rule three," the "Natural discontinuity method" is applied to the risk values. The outcome is visualized as five vertical bars of increasing height, representing different risk levels labeled below as "VL, L, M, H, VH," which likely stand for Very Low, Low, Medium, High, and Very High.

**Figure 19.** Space-time semantic reasoning logic with criteria (VL: very low, L: low, M: moderate, H: high, VH: very high).

The antecedent rules in the above spatio-temporal semantic inference rules can trigger the subsequent rules when the conditions are satisfied. Therefore, the dynamic change of precipitation data can automatically trigger the geological landslide risk calculation for

Remote Sens. 2022, 14, 1214 17 of 21

realizing the automatic completion of the whole process of DPKG chain reasoning without manual effort.

In this case, the actual precipitation record data of Xiji County Meteorological Observatory on 18 September 2018 is used as the query input of the instance layer of the DPKG. Based on the reasoning of spatial-temporal knowledge graph, the geological landslide time probability was daily calculated for the whole county of Xiji from 8 to 28 September 2018. From 18 to 19 September 2018, the geological landslide time probability in the county met the above geological landslide risk time probability conditions for the two consecutive days. The experimental results are shown in Figure 20. Due to the setting of reasoning rule 2, the calculation of geological landslide risk will be triggered automatically. The calculation results of geological landslide risk probability on 18 September 2018 are shown in Figure 21.

The graph of the time probability of landslide

Image /page/16/Figure/4 description: A bar chart titled 'The graph of the time probability of landslide'. The vertical axis is labeled '%0' and ranges from 0 to 20 in increments of 2. The horizontal axis displays dates from 9/8 to 9/28. The chart consists of blue vertical bars for each day, showing the time probability. There are notable peaks in probability on 9/15, with a value of approximately 17.8, and on 9/19, with a value of approximately 18.5. Another smaller peak occurs on 9/18 with a value of about 16. For most other days, the probability fluctuates between approximately 6 and 10. A dashed blue line is overlaid on the chart, starting at a value of about 14, dipping to around 13, and then leveling off at approximately 12.5 for the remainder of the dates.

Bar: The graph of the time probability of landslide in Xiji County from September 8 to 28, 2018

Broken line: The graph of dangerous time probability of landslide in Xiji Countyfrom September 8 to 28,2018

**Figure 20.** The graph of the time probability of landslide. The bar is the graph of the time probability of landslide in Xiji County from 8–28 September 2018. The broken line is the graph of dangerous time probability of landslide in Xiji County from 8–28 September 2018.

Image /page/16/Figure/8 description: A map displaying the geological landslide risk probability for a specific region. The map is color-coded, with a legend indicating the probability levels. A north arrow is in the top left corner. The legend, titled 'Geological Landslide Risk Probability', shows a scale from low risk (dark green) to high risk (red). The probability ranges are as follows: 0-0.024 (dark green), 0.025-0.078 (green), 0.079-0.149 (light green), 0.15-0.231 (yellow-green), 0.232-0.329 (yellow), 0.33-0.439 (light orange), 0.44-0.553 (orange), 0.554-0.675 (dark orange), 0.676-0.812 (orange-red), and 0.813-1 (red). The map is predominantly green, with patches of yellow, orange, and red indicating higher-risk areas. A single yellow dot on the map is labeled 'September 18, 2018 Landslide section'. A scale bar at the bottom right is marked in meters, with intervals at 0, 6250, 12500, and 25000.

Figure 21. Map of landslide hazards in Xiji County based on multi-Graded Cascade Random Forest.

Remote Sens. 2022, 14, 1214 18 of 21

In this case, since the distribution data of buildings and roads in Xiji County is included in the DPKG, it further filtered the buildings and roads in the high-risk areas of geological landslides on 18 September 2018, as shown in Figure 22. From Internet news, we learned that a landslide occurred on National Highway 309 on 18 September 2018, which caused road blockage. The actual geological landslide section is located in the dangerous road area that has been correctly predicted by our method, as shown in Figure 22. Experiments show that it successfully hit the geological landslide event within the time and space range of the warning.

Image /page/17/Figure/2 description: A diagram illustrating the identification and data representation of geological hazards. On the left is a map of a region with a legend indicating different features: grey for Road, pink for Building, red for Risk road, orange for Risk Building, and purple for the September 18, 2018 Landslide section. The map includes a north arrow and a scale bar from 0 to 24000 meters. A small section of the map is magnified and shown in the center as a satellite image of a winding road in a mountainous area. This image has colored overlays corresponding to the legend. To the right, two entity relationship diagrams show how these features are structured as data. An arrow from the purple landslide section points to a 'Landslide Entity' diagram with the following attributes: 'hasCenterLonLat' is '102.98438°E, 26.502315°N', 'hasTime' is '2018-09-18', and 'hasTileCode' is 'z20\_x321\_y765'. An arrow from the red road section points to a 'RiskRoad Entity' diagram with attributes: 'hasCenterLonLat' is '102.98438°E, 26.502315°N', 'hasTime' is '2018-09-18', and 'hasTileCode' is 'z20\_x321\_y766'.

**Figure 22.** Road distribution map of Xiji County included in the landslide disaster warning area on 18 September 2018.

Prediction was carried out in Xiji Country respectively for the area of 3130.00 km<sup>2</sup>, the area of 1509.54 km<sup>2</sup>, and the area of 800.88 km<sup>2</sup>. The experimental results are shown in Figure 23. With the increase of the experimental range, the time of experimental calculation also increases. The performance is basically in a satisfied performance range. Therefore, our method is applicable for large-scale disaster prediction.

Image /page/17/Figure/5 description: A horizontal bar chart with three bars. The vertical axis has three labels: 3130.00, 1509.54, and 800.88. The horizontal axis is labeled in minutes (min) and ranges from 0.00 to 10.00, with major gridlines at intervals of 2.00. The top bar, corresponding to 3130.00, extends to a value of 7.81. The middle bar, for 1509.54, has a value of 3.09. The bottom bar, for 800.88, has a value of 2.70. The bars are blue, with the top and bottom bars having a gradient from light to dark blue.

Figure 23. Comparison of forecast time for different areas in Xiji Country.

# 4. Discussion

Compared with the traditional prediction methods, the disaster prediction method based on the DPKG has the advantages of more accurate spatial overlay analysis, high degree of automation, and fast calculation speed, as shown in Table 2. However, it cannot be ignored that the proposed method in this paper still has certain limitations: (1) Before forecasting the target area, the data required for disaster prediction needs to be preprocessed and stored in advance, and data storage requires a certain amount of time. The larger the area, the more data dimensions required for prediction, and the longer the time. (2) The data used in this case is not accurate enough. For example, the spatial resolution of terrain

Remote Sens. 2022, 14, 1214 19 of 21

data is 30 m, and the spatial resolution of surface coverage data for disaster prediction is 10 m. The accuracy still needs to be improved. If higher-resolution data is obtained, and more detailed tree species, tree age, and other data can be involved in disaster prediction, the accuracy of disaster prediction can be further improved. (3) The comparison with traditional disaster forecasting methods is not sufficient in the experiment that only considers the most well-known tool ArcGIS.



# 5. Conclusions

Compared with plain text data and structured databases, DPKG has the advantages of richer semantic representation, more accurate data content, and better query performance. The knowledge graph provides a new means for the organization, management, fusion, and analysis of multi-source heterogeneous data in complex disaster environments. It facilitates prediction, prevention, and mitigation of the natural disasters. This paper proposes the DPKG that integrates multi-source remote sensing information in disaster scenes with other multi-source heterogeneous information. It considers not only dynamic data describing spatio-temporal facts but also domain analysis models. Based on the analysis of disaster influencing factors, this paper proposes a common disaster prediction method based on the DPKG for the dynamic data-driven disaster prediction. This paper introduces new ideas by taking forest fires and geological landslides as examples. The proposed method can serve the research and application of disaster emergency response with the strong help of artificial intelligence technology.

- (1) From the perspective of cross-domain knowledge integration, knowledge graph integrates remote sensing knowledge and expert knowledge through semantic technology. It effectively connects multi-source heterogeneous data (GIS, meteorology, terrain, ground sensors, etc.) with expert knowledge in the field of disasters;
- (2) The DPKG contains dynamically updated spatio-temporal facts that reflect changes in the real world. Through knowledge graph query, the query performance in disaster emergency scenarios can be improved, and dynamic data updates can automatically drive prediction;
- (3) It provides efficient data storage and management methods for practitioners in the fields of remote sensing and geo-information, which helps to improve the efficiency

Remote Sens. 2022, 14, 1214 20 of 21

of spatio-temporal data query. It reduces the manual effort by using reasoning of the knowledge graph.

The DPKG proposed in this paper aims at the integration of remote sensing information, geographic information, and the correlation between dynamic data and static knowledge in complex disaster environments. It lays the foundation for future in-depth research, particularly for knowledge extraction and knowledge discovery for disaster prediction. In future work, indexing and query performance need to be further verified in the case of more types and larger amounts of data. The depth of knowledge reasoning needs to be further improved. In future research, we will enhance the DPKG by leveraging graph neural networks and deep learning models, so as to integrate a large number of spatio-temporal facts, and realize disaster emergency decision-making, historical data verification, and new model construction; it needs to build a knowledge service system for natural disaster monitoring and prediction as well as the emergency decision-making. In addition, this article basically focuses on verifying the availability and usability of our model through case studies. We will compare with more traditional prediction methods in the future

**Author Contributions:** Conceptualization, X.G. and Y.Y.; methodology, X.G. and W.L.; validation, X.G., W.L. and W.Z.; resources, W.L.; data curation, X.G. and W.L.; writing—original draft preparation, X.G. and J.C.; writing—review and editing, X.G., Y.Y., L.P. and Z.H.; funding acquisition, L.P. All authors have read and agreed to the published version of the manuscript.

**Funding:** This work was supported by the Beijing Municipal Science and Technology Project (Z191100001419002), and Ningxia Key R&D Program (2020BFG02013).

**Institutional Review Board Statement:** Not applicable.

Informed Consent Statement: Not applicable.

Data Availability Statement: Data sharing not applicable.

Conflicts of Interest: The authors declare no conflict of interest.

# References

