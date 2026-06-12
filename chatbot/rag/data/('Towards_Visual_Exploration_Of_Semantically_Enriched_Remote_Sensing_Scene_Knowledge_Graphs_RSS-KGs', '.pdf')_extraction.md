
## **ABSTRACT**

There has been an increase in the adoption of Linked Data and subsequently representing data in the form of knowledge graphs across a wide spectrum of domains. There has also been significant interest in the remote sensing community to publish Earth Observation data in the form of Linked Data. As the geospatial Linked Data cloud on the internet grows, there arises a need for efficient methods of exploratory analysis of such information-rich geospatial knowledge graphs. Knowledge graph representation of remote sensing scenes has proved to add significant value for effective mining of implicit information in addition to seamless integration with other data sources. This work is geared towards visual exploration of semantically enriched Remote Sensing Scene Knowledge Graphs (RSS-KGs). In this paper, we propose and implement an interactive web-based interface to visually explore and interact with RSS-KGs using Cesium. The proposed interface seeks to visualize the knowledge graph in the form of nodes and edges, mapped over the remote sensing scene consisting of different land use land cover regions and their inferred characteristics in addition to their spatial relationships with one another. It is envisaged that visualization in the form of nodes and edges would aid in visually validating the spatial relations in the knowledge graph, thus enhancing the understanding of the geospatial knowledge graph from the end user perspective. We demonstrate the efficacy of the interface through the visual exploration of an enriched geospatial knowledge graph of a remote sensing scene captured during an urban flood event.

*Index Terms*— visualization, exploration, knowledge graphs, remote sensing scenes, earth observation, linked data

## 1. INTRODUCTION

Recently there has been a huge interest in publishing Linked Data on the web, backed by different governance initiatives [1]. The advantages of Linked Data in terms of seamless accessibility, interoperability and integration have been well understood by the research community. This has led to an increase in the size of the Linked Data cloud available on the web. The geospatial research community too has noticed and acknowledged the benefits of Linked Data and publishing

Image /page/0/Figure/9 description: A flowchart titled 'Figure 1. Multi-level Semantic Enrichment of Remote Sensing Scene' illustrates a four-tiered process for enriching data. The layers, from bottom to top, are Data Mediation Layer, Spatial Knowledge Enrichment, Contextual Knowledge Enrichment, and Scene Knowledge Aggregation.

1. \*\*Data Mediation Layer\*\*: This foundational layer produces a 'Linked Data Representation of Remote Sensing Scene Knowledge'. An example 'RSS-LD' shows entities like 'Vehicle "V1"' and 'Road "R1"'.

2. \*\*Spatial Knowledge Enrichment\*\*: This layer takes 'Spatial SWRL Rules' and a 'Remote Sensing Scene Ontology (RSSO)' as input. A 'Deductive Reasoner' processes them to create an 'Enriched Remote Sensing Scene Knowledge Graph (RSS-KG)' with 'Spatial', 'Directional', and 'Topological' components. An example 'RSS-KG' shows vehicles intersecting with a road ('geo:sfIntersects' -> 'Road "R1"').

3. \*\*Contextual Knowledge Enrichment\*\*: This layer uses 'Contextual SWRL Rules' and a 'Flood Scene Ontology (FSO)'. A 'Deductive Reasoner' enriches the knowledge graph, which now has 'Contextual' and 'Spatial' layers. The example 'RSS-KG' shows vehicles being 'On' an 'Unaffected Road "UR1"'.

4. \*\*Scene Knowledge Aggregation\*\*: The top layer starts with 'Spatio-Contextual Triple Aggregation'. A 'Deductive Reasoner' produces the final 'Enriched Remote Sensing Scene Knowledge Graph (RSS-KG)' with 'Aggregated', 'Contextual', and 'Spatial' layers. The example 'RSS-KG' shows an aggregated concept: 'Traffic Congestion "TC1"' is 'On' an 'Unaffected Road "UR1"'.

Figure 1. Multi-level Semantic Enrichment of Remote Sensing Scene Knowledge Graphs (RSS-KGs) as proposed by Sem-RSSU Framework [2]

Geospatial Linked Data is largely being encouraged. With the adoption of Geospatial Linked Data, there is an increasing interest in leveraging such EO Linked Data through knowledge graph representation for mining the otherwise implicit knowledge. In addition to improving spatio-contextual inferencing over semantically enriched geospatial knowledge graphs there is a need for effective visual exploration of such information-rich sources.

This works builds over the Semantics driven Remote Sensing Scene Understanding (Sem-RSSU) Framework [2]. The Sem-RSSU framework advocates the transformation of remote sensing scenes as knowledge graphs. It facilitates this by proposing the Remote Sensing Scene Ontology (RSSO) – a core ontology for a generic remote sensing scene, formalizing the concepts and relations among regions in a scene. It also proposes the Flood Scene Ontology (FSO), formalizing the concepts and relations that transpire during an urban flood event. It introduces and demonstrates a holistic pipeline to translate remote sensing scenes to semantically enriched Remote Sensing Scene Knowledge Graphs (RSS-KGs). Figure 1 depicts the multilevel Semantic Enrichment Layer of the Sem-RSSU framework for hierarchical spatial, contextual and aggregate enrichment of RSS-KGs.

This work is geared towards developing an intuitive interface for effective visual exploration of such information rich Remote Sensing Scene Knowledge Graphs. There have been some prominent research studies on visualization of geospatial linked data. Map4RDF [3] was developed as a faceted browser for visualization of RDF datasets with

Image /page/1/Figure/0 description: A screenshot of a web application titled "Visual Exploration of Semantically Enriched Remote Sensing Scene Knowledge Graphs (RSS-KGs)". The application is displayed in a web browser, with the URL visible as www.geosysiot.in/tools/rssKG-Explorer/. The interface is split into two main parts. On the left is a dark control panel with white text and toggle switches. This panel includes options like "RSS-Knowledge Graph in 3D," information about the data source, ontologies, and details of the remote sensing scene: "(Raster - WV02 [FCC]) | Srinagar, India | Sept. 17, 2014)". It also credits the developers from IIT Bombay. On the right is the main visualization area, which shows an aerial view of a city. A large portion of this view is overlaid with a false-color composite image, where vegetation appears bright red and water or flooded areas appear in shades of cyan, surrounding buildings. A major road runs diagonally through the scene.

Figure 2. Visualization of the Remote Sensing Scene of an Urban Flood Event in False Color Composite captured by WorldView 2, overlayed on Cesium's base map imagery

support for visual exploration of GeoSPARQL endpoints. The LGD Browser [4] was another prominent tool for faceted browsing of structured information in OSM visualized on a slippy map. Sextant [5] has been a powerful visualization and editing tool for exploring time-evolving geospatial linked data. Another research study [6] aimed to visualize geospatial ontologies by exploiting the visualization capabilities of Cesium – a webGL based JavaScript library to render the globe in 3D on the web browser.

Although these research studies have developed powerful visualization tools for exploring geospatial linked data, none of them focus on the inherent granular graph nature of linked data consisting of nodes and edges. Nodes and edges are fundamental building blocks of a knowledge graph. This work proposes to enable intuitive visual exploration of nodes and edges of remote sensing scene knowledge graphs in addition to a region-based visualization through an interactive web-based interface. Thus, this work aims to enable users to develop a comprehensive understanding of a Remote Sensing Scene Knowledge Graph (RSS-KG) through the web-based interface that has been developed as part of this research.

## 2. METHODOLOGY

This work advocates the use of Cesium<sup>1</sup> – a WebGL based JavaScript library for rendering the globe in 3D in the web browser. The geospatial visualization capabilities of Cesium

have been studied and understood. Thus, it has been found to be an apt candidate for visualizing and enabling interactive exploration of Remote Sensing Scene Knowledge Graphs (RSS-KGs).

### 2.1 JSON-LD

JSON-LD stands for JavaScript Object Notation for Linked Data. JSON-LD is a data serialization format for Linked Data. It has been conceptualized to leverage the benefits of the interoperable JSON based data serialization to the world of Linked Data and Semantic Web. The serialization in JSON-LD is similar to JSON in terms of storing data in form of key-value pairs. It must be noted that each triple has an "@id" key associated with it pointing to the URI of the resource that it represents. Due to its ease of consumption by web-based systems, JSON-LD forms an apt choice for knowledge graph representation and visualization with Cesium. The proposed web-based interface visualizes the "Regions" in the Remote Sensing Scene as Nodes and the Spatial Relations - "Externally Connected" of the Region Connection Calculus (RCC8) as Edges. Thus, the spatial interaction of the regions among themselves has been effectively visualized. Consequently, this leads to the visual validation of inferred spatial relations in the knowledge graph, thus improving the understanding of the knowledge graph from an end user perspective.

<sup>1</sup> https://cesium.com/cesiumjs/

Image /page/2/Figure/0 description: A screenshot of a web application titled "Visual Exploration of Semantically Enriched Remote Sensing Scene Knowledge Graphs (RSS-KGs)" running in a browser. The main view is a 3D visualization of a remote sensing scene of an urban area, overlaid with a complex network graph consisting of numerous blue circular nodes and yellow connecting lines (edges). On the left is a control panel with options for the visualization, including toggles for "RSS-Knowledge Graph in 3D (Nodes and Edges)" and "RSS-Knowledge Graph (Regions-Polygons)". This panel also provides details about the data: Data Source is "RSS-KG [JSON-LD]", Ontologies are "RSSO | FSO", the Remote Sensing Scene is from "Srinagar, India | Sept. 17, 2014", and the graph was generated by the "Sem-RSSU Framework". On the right, a panel titled "Selected Node" displays detailed information for a specific node, ID "http://www.geosysiot.in/semrssu/data#R6". The type of this node is identified as "ApplicationSchema#FloodWater". Its geographic coordinates are listed, including Centroid X: 74.77952999546662 and Centroid Y: 34.086458934296296. The panel also lists other externally connected nodes. The caption below the image reads: "Figure 2. Visualization of the Nodes and Edges in the Remote Sensing Scene Knowledge Graph (RSS-KG) in 3D for a RS Scene of an Urban Flood Event."

Figure 3. Visualization of the Nodes and Edges in the Remote Sensing Scene Knowledge Graph (RSS-KG) in 3D for a RS Scene of an Urban Flood Event, with an Edge representing the "Externally Connected (EC)" Relation of the RCC8

The interface has been developed using HTML5, CSS3 and JavaScript. The Remote Sensing Scene Knowledge Graph (RSS-KG) in the JSON-LD form has been hosted on the server for consumption by the developed interface for visual exploration.

## 3. EXPERIMENTAL RESULTS

### 3.1. Dataset

The Remote Sensing Scene Knowledge Graph (RSS-KG) generated by the Sem-RSSU framework for the remote sensing scene of an urban flood event in Srinagar, India during September 2014, has been considered for this study. The snippet in Figure 4 depicts the RSS-KG in the JSON-LD format. The instance of "Region" class with "id" as "R0" has been depicted. The knowledge graph has been semantically enriched by inferring implicit concepts and relations using the Sem-RSSU framework. In that regard, "ResidentialBuilding", the inferred classes of "FloodedResidentialBuilding" "AccessibleResidentialBuilding" defined in the RSSO and FSO have been derived. The snippet also depicts the inferred spatial relation - "Externally Connected" of RCC8 between instances of "Region" classes. In addition to the LULC Classes and the Spatial Relations, the RSS-KG also constitutes the geometry-related data such as Centroid, Extent and Polygon Geometry represented in the Well-Known Text (WKT) representation.

```
[ {
    "@id": "http://www.geosysiot.in/semrssu/data#RO",
    "@type": [
    "http://www.geosysiot.in/rsso/ApplicationSchema#Region",
    "http://www.geosysiot.in/rsso/ApplicationSchema#ResidentialBuilding",
    "http://www.geosysiot.in/fso/ApplicationSchema#ResidentialBuilding",
    "http://www.geosysiot.in/fso/ApplicationSchema#FloodedResidentialBuilding"],
    "http://www.geosysiot.in/fso/ApplicationSchema#hasInferredLULC":
    [ {
        "@value": "floodedBuilding"
      }, {
        "@value": "accessibleResidentialBuilding"
      }),
      "http://www.geosysiot.in/rsso/ApplicationSchema#hasURX": [ {
        "@type": "http://www.w3.org/2001/XMLSchema#double",
        "@value": "74.780932527"
      }),
      "http://www.geosysiot.in/rsso/ApplicationSchema#hasURY": [ {
        "@type": "http://www.w3.org/2001/XMLSchema#double",
        "@type": "http://www.w3.org/2001/XMLSchema#double",
        "@type": "http://www.so.org/2001/XMLSchema#double",
        "@type": "http://www.so.org/2001/XMLSchema#double",
        "@type": "http://www.geosysiot.in/rsso/ApplicationSchema#hasURY": [ {
        "@type": "http://www.so.org/2001/XMLSchema#double",
        "@type": "http://www.geosysiot.in/rsso/ApplicationSchema#hasURY": [ {
        "@type": "http://www.geosysiot.in/semrssu/data#R4"
      }, ...
} "http://www.opengis.net/ont/geosparql#rcc8ec": [ {
        "@id": "http://www.geosysiot.in/semrssu/data#R4"
      }, ...
} "####################################
```

Figure 4. Snippet of the RSS-KG for a Remote Sensing Scene of an Urban Flood Event

Table 1. Time taken for visualizing Remote Sensing Scene Knowledge Graph (RSS-KG) for Nodes and Edges and Region Geometries

| Remote Sensing Scene<br>Knowledge Graph (RSS-KG)<br>Visualization | Number of<br>Entities     | Time<br>(seconds) |
|-------------------------------------------------------------------|---------------------------|-------------------|
| Nodes and Edges                                                   | Nodes: 554<br>Edges: 2153 | 5.78              |
| Region Geometries                                                 | Regions: 554              | 1.02              |

5785

Image /page/3/Figure/0 description: A screenshot of a web application titled "Visual Exploration of Semantically Enriched Remote Sensing Scene Knowledge Graphs (RSS-KGs)". The main view displays a satellite image of a town, overlaid with a color-coded map showing regions in red, green, black, and brown, with a grey road running through the center. On the left is a control panel with various toggles and settings, including "RSS-Knowledge Graph in 3D" and "RSS-Knowledge Graph (Regions-Polygons)". It specifies the data source as "Remote Sensing Scene (Raster - WV02 [FCC] | Srinagar, India | Sept. 17, 2014)". On the right, a panel displays detailed information for a selected region, which is a road. The details include its ID, Type, Centroid coordinates (X: 74.7800655700565, Y: 34.08730995206955), corner coordinates, and a list of externally connected regions.

Figure 5. Visualization of Regions as Polygon Geometries in a Remote Sensing Scene Knowledge Graph (RSS-KG) for a RS Scene of an Urban Flood Event

### 3.2. Discussion

Figure 2, figure 3 and figure 5 depict screenshots of the developed visual exploration interface. Figure 3 depicts the knowledge graph visualization in the form of nodes and edges. The nodes and edges can be interacted with through mouse clicks to be presented with more information about the clicked entities. Similarly, the figure 5 depicts the visualization of polygon geometries of the "Region" instances in the knowledge graph. The "Region" instances are visualized in a color in accordance with the Land Use Land Cover Class (LULC) they belong to. These "Region" instances can also be interacted with individually to be presented with inferred concepts and relations from the RSS-KG. Table 1 depicts the time taken for visual rendering of the knowledge graph by the web browser. It was observed that the node-edge visualization took significantly more time as compared to region-geometry visualization for rendering, due to the overhead of visualizing the huge number of edges, in addition to nodes.

## 4. CONCLUSION

This research proposed an intuitive interface using Cesium, for effective visual exploration of Remote Sensing Scene Knowledge Graphs (RSS-KGs) generated by the Sem-RSSU framework. The knowledge graphs comprehensively represent the different Land Use Land Cover regions contained in remote sensing scenes along with inferred spatio-contextual concepts and relations. Thus, this research aimed to enhance the comprehensive understanding of a remote sensing scene from an end user

perspective. The visual exploration interface developed as a part of this research has been hosted on the web (http://www.geosysiot.in/tools/rssKG-Explorer/).

Future work on this interface would involve enabling support for user uploaded geospatial knowledge graphs in addition to support for remote GeoSPARQL endpoints.
