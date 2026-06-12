
# **ABSTRACT**

Increasing numbers of people live in flood-prone areas worldwide. With continued development, urban flood will become more frequent, which has caused casualties and property damage. Researchers have been dedicating to urban flood risk assessments in recent years. However, current research is still facing the challenges of multi-modal data fusion and knowledge representation of urban flood events. Therefore, in this paper, we propose an Urban Flood Knowledge Graph (UrbanFloodKG) system that enables KG to support urban flood risk assessment. The system consists of data layer, graph layer, algorithm layer, and application layer, which implements knowledge extraction and storage functions, integrates knowledge representation learning models and graph neural network models to support link prediction and node classification tasks. We conduct model comparison experiments on link prediction and node classification tasks based on urban flood event data from Guangzhou, and demonstrate the effectiveness of the models used. Our experiments prove that the accuracy of risk assessment can reach 91% when using GEN, which provides a a promising research direction for urban flood risk assessment.

# **CCS CONCEPTS**

• **Information systems**  $\rightarrow$  *Clustering and classification.* 

# **KEYWORDS**

urban flood, knowledge graph, link prediction, graph neural network

# **ACM Reference Format:**

Yu Wang, Feng Ye, Binquan Li, Gaoyang Jin, Dong Xu, and Fengsheng Li. 2023. UrbanFloodKG: An Urban Flood Knowledge Graph System for Risk Assessment. In *Proceedings of the 32nd ACM International Conference on* 

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org.

CIKM '23, October 21-25, 2023, Birmingham, United Kingdom

© 2023 Copyright held by the owner/author(s). Publication rights licensed to ACM. ACM ISBN 979-8-4007-0124-5/23/10...\$15.00 https://doi.org/10.1145/3583780.3615105

Information and Knowledge Management (CIKM '23), October 21–25, 2023, Birmingham, United Kingdom. ACM, New York, NY, USA, 11 pages. https://doi.org/10.1145/3583780.3615105

# 1 INTRODUCTION

Increasing numbers of people live in flood-prone areas worldwide. With continued development, urban flood will become more frequent, which has caused casualties and property damage [58]. With the rapid development of machine learning, deep learning methods have been increasingly explored for their potential application in urban flood risk assessment. Existing research has demonstrated that Long Short Term Memory (LSTM) [56], Recurrent Neural Network (RNN) [3] and Convolutional Neural Network (CNN) [30] are commonly used in flood forecasting. However, the structures of the above models are complex and the explainable ability is poor. Therefore, it is worth exploring how to use knowledge related to urban flood events to help human capture the relationships between time and space, overcome the limitations of above models, and further improve the accuracy of risk assessment.

In addition, recent studies emphasize the importance of data fusion in specific applications, such as data fusion [16] is proposed to improve the accuracy of hydraulic simulation of urban flood, and a remote sensing and text bimodal data fusion model based on UFCLI [49] is proposed to improve accuracy of urban flood damage. However, no researchers try to fuse multi-modal data for urban flood risk assessment. Meanwhile, some studies try to extract explicit knowledge from data for performance enhancement and semantic reasoning [6, 54, 55]. But in the field of flood assessment, there are mainly data-driven researches [30, 38], and remains a lack of effective representation of knowledge to aid in flood risk assessment. Considering existing research has not explored how to integrate multi-modal data into knowledge from urban flood to support downstream tasks, we summarize the key challenges for further research on urban flood risk assessment from two aspects:

• Multi-modal Data Fusion. Due to the diverse sources and tools of data collection, the collected data has different structures and forms. On the one hand, urban flood related data is usually stored in different structures, such as tables, texts, and images. On the other hand, there are many relationships between data, such as the similar duration of event A

- and event B. Therefore, how to conduct effective fusion of multi-modal data has not been fully explored.
- Knowledge Representation. Urban flood events involve data from multiple aspects, including flood table data organized by monitoring departments, textual data reported in news broadcasts, on-site image data collected by sensors, etc. For this multi-modal data, how to embed multi-modal data related to urban flood events to downstream task-driven algorithm models is a challenge.

Knowledge graph (KG) [34] is a technology that represents and stores entities and relationships in a graph form and has been successfully applied in fields such as KG-based recommendation systems [13] and KG-based question answering systems [17]. Specifically, KG uses triple facts (head entity, relationship, tail entity) to store and represent knowledge in the real world, where entities can be objects, events, locations, or abstract concepts, and relationships describe their connections [39]. Meanwhile, Liu [23] combines urban computing with KG system, exploring new modes of urban data management and analysis. Therefore, we believe that this provides a reasonable and feasible way for risk assessment of urban flood events.

To unlock the full potential of urban flood data for efficient risk assessment, we present a system called Urban Flood Knowledge Graph (UrbanFloodKG). The system consists of data layer, graph layer, algorithm layer and application layer to meet various needs in urban flood risk assessment research. Finally, we conduct link prediction and node classification experiments by using different models to demonstrate the feasibility of the proposed UrbanFloodKG system.

The main contributions of our work are as follows:

- We propose a system that retrieves urban flood-related data from various data sources, construct a KG of urban flood events, and further integrate various KG representation algorithms and graph neural network models. This system is the first KG-based urban flood risk assessment system, providing a new perspective for assessing urban flood events.
- We present a systematic scheme for UrbanFloodKG construction, which identifies the key elements in urban flood environment as entities, and describes their semantic connections as relations. The proposed construction scheme provides a general framework to fuse the urban flood-related data into the KG, and potentially benefits various downstream tasks.
- We construct a dataset for link prediction and node classification tasks using urban flood-related data collected from Guangzhou over the years. After using different models, we compare their performance and demonstrate the effectiveness and feasibility of our proposed system.

In the following sections, we present the design and implementation of our UrbanFloodKG system. Section 2 introduces the background of KG and the requirements for our system. Section 3 provides an overview of the system architecture and details each layer. In Section 4, we present the application scenarios and compare various models for knowledge representation and graph neural networks. Section 5 discusses related work, and we conclude the paper in Section 6.

# 2 PRELIMINARY & REQUIREMENTS

## 2.1 Preliminary

Here we formally define the KG as follows [11, 23, 57].

Definition 2.1 (Knowledge Graph). A knowledge graph (KG) is represented as a graph structure called  $\mathcal{G} = \{\mathcal{E}, \mathcal{R}, \mathcal{F}\}$ , where  $\mathcal{E}, \mathcal{R}$ , and  $\mathcal{F}$  denote the sets of entities, relations, and facts, respectively. Specifically, the fact set  $\mathcal{F} = (h, r, t) \mid h, t \in \mathcal{E}, r \in \mathcal{R}$  stores the triples in the KG. Each triple  $(h, r, t) \in \mathcal{F}$  represents a directed edge from entity h to entity t with a relation type r.

Definition 2.2 (Knowledge Graph Construction). KG construction is facilitated through the utilization of a procedure denoted as f, which maps a data source to a KG:  $f:D\times f_k(D)\to \mathcal{G}$ . In this context, D represents the set of data sources, and  $f_k(D)$  corresponds to the background knowledge associated with the data target, which can include domain-specific knowledge. It is crucial to highlight that the availability of background knowledge plays a significant role in KG construction. This background knowledge can be provided through pre-designed rules or a language model that generates representations. Without such background knowledge, the process of KG construction is often hindered or unable to proceed.

## 2.2 Requirements

To guide our system design for a comprehensive and reproducible platform, we summarize the requirements as following three as-pects:

- Data and storage compatibility. When integrating data of different types, formats, and sources into the same storage system, the integrity, consistency, and accessibility of the data can be maintained.
- Algorithm universality. Knowledge representation algorithms can be applied universally to downstream subtasks.
- Knowledge maintainability. The system must effectively manage and update urban flood event data to ensure its accuracy and relevance.

Therefore, according to the above definitions and requirements, we build the UrbanFloodKG system, which is introduced in the following.

# 3 THE URBAN FLOOD KG SYSTEM

In this section, we present an overview of our designed Urban-FloodKG system. Subsequently, we delve into the specific details from a layered perspective.

## 3.1 System Overview

The high-level system architecture of the UrbanFloodKG system is shown in Fig. 1. The different layers are described as follows:

- Data. The data layer is responsible for collecting data from multiple sources and cleaning the collected data.
- Graph. This graph layer constructs UrbanFloodKG by defining its schema, extracting entities and relationships from urban data of different structures and forms, and enriching them with additional attributes. By integrating urban flood data in this way, the construct UrbanFloodKG provides a comprehensive and effective platform for urban flood risk

Image /page/2/Figure/2 description: A diagram illustrating the high-level architecture of the UrbanFloodKG system, organized into four distinct layers: Application, Algorithm, Graph, and Data. The bottom layer, Data, involves 'Data Collection & Cleaning' of 'Structured data', 'Semi-structured data', and 'Unstructured data'. The next layer up is Graph, which is divided into 'Knowledge Extraction' (including Schema, Entity, Relation, and Attribute) and 'Knowledge Storage' (using OrientDB). Above that is the Algorithm layer, which has two parts: 'Knowledge Representation' (using 'Translation-based models & GNN-based models') and 'Operation' (including Query, Embedding, Link Prediction, and Node Classification). The top layer is Application, which handles Tasks such as 'Knowledge Reasoning', 'Event Classification', 'Urban Decision-making', and others indicated by an ellipsis.

Figure 1: The high-level architecture of UrbanFloodKG system.

assessment. Next, all constructed triplets are transformed into graph data structures and input into OrientDB [36].

- Algorithm. The algorithm layer utilizes Translation-based models and GNN-based models to transform the triplets in the KG into vector embeddings, while also offering fundamental operations.
- Application. In the application layer, the application scenarios of this system are introduced. This layer provides services for knowledge reasoning, event classification, and urban decision-making tasks.

## 3.2 Data Layer

The data layer provides data collection and data cleaning functions.

*Data Collection.* The data types of urban flood events can be divided into three categories: structured data, semi-structured data, and unstructured data, as shown in Fig. 2.

- **Structured data.** Most structured data are mainly tables, and we extract key information manually.
- Semi-structured data. Most semi-structured data are texts. Named entity recognition [19, 26] and relation extraction tasks are of great help in extracting knowledge from unstructured text. We use the UIE [24] framework to extract

- knowledge from text automatically, extract key attributes as event attribute information.
- Unstructured data. The unstructured data mainly consist of manually collected images of water-logging scenes.

Image /page/2/Picture/14 description: A diagram illustrating three types of information, labeled "Table," "Image," and "Text," arranged horizontally. On the left, under the label "Table," is a black and white icon of a grid with four columns and three rows. In the center, under the label "Image," is a photograph of a flooded urban street with reflections of buildings in the water and a car in the distance. On the right, under the label "Text," is a text box containing the sentence: "The Shinan Avenue experienced urbanflood, lasting for one hour."

Figure 2: Multi-modal data related to urban flood events.

## 3.3 Graph Layer

The graph layer is responsible for the management of KG data. In the knowledge extraction stage, we summarize the following four key aspects: schema definition, entity identification, relation extraction and attribute enrichment.

*Schema Definition.* To ensure entities in the KG have a consistent structure and semantics, thereby enhancing the reliability of the KG, a schema or ontology is used to describe the high-level

structure of the KG. This includes defining the types of entities and relations present within the graph [15]. Fig. 3 illustrates the schema of UrbanFloodKG, wherein the rectangles represent various entity types and the edges depict their relationships within the UrbanFloodKG.

Image /page/3/Figure/3 description: A concept map or entity-relationship diagram showing the relationships between various entities. The entities are represented by light blue rounded rectangles, and the relationships are shown as labeled arrows. The diagram shows that an 'Image' is an 'on-siteImageOf' a 'Waterlogging Area'. The 'Waterlogging Area' is 'locateAt' a 'Region', and a 'Department' is also 'locateAt' a 'Region'. A 'Reason' can 'leadTo' an 'Event', which can 'occurIn' a 'Waterlogging Area'. An 'Event' can 'leadTo' an 'Influence' and is a 'cateOf' a 'Risk-level'. There is a recursive relationship on 'Event' labeled 'samePosition, closeTime'. A 'Leader' can 'resolve' an 'Event', and the 'Leader' 'belongTo' a 'Department'.

Figure 3: The schema of UrbanFloodKG. Each rectangle represents a schema of an entity.

**Entity Identification.** To ensure the standardization and consistency of the content in the KG, it is necessary to establish conventions for its representation. Therefore, the following entities can be identified:

- Event. Event represents each specific urban flood event, which is a key entity in the research of UrbanFloodKG.
- Influence. Influence represents the impact caused by urban flood events.
- Reason. Reason represents the causes of urban flood events summarized by professionals.
- Leader. Leader represents the personnel responsible for handling urban flood events.
- Department. Department represents the department to which personnel responsible for handling urban flood events belong.
- Region. The Region denotes the administrative area of the city to which the urban flood event is attributed.
- Water-logging Area. Water-logging Area represents the specific location where the urban flood events occurred.
- Image. Image stores on-site photographs depicting the urban flood events.
- **Risk-level**. Risk-level represents the the assessment of the risk level of urban flood events conducted by experts during the later stages.

**Relation Extraction.** After analyzing the identified entity types within UrbanFloodKG, we extract representative relations to capture the semantic connections between entities. These relations are categorized as follows:

• **Spatial Relations.** The spatial relationship model characterizes the spatial association between entities. The relationships "locatAt" and "occurIn" simulate the spatial connections between event entities and location entities, as well as region entities, respectively.

- Personal Relations. Personal relationships emphasize individual knowledge. The "belongTo" relationship links the department entity to the leader's workplace, while the "resolve" relationship connects the leader entity to the event entity that they are responsible for handling.
- Causal Relations. Causal relationships aid in comprehending and predicting causal connections among entities. The relationship "leadTo" establishes a link between the event entity and the reason entity or the influence entity, forming a comprehensive chain of events.
- Affiliated Relations. The association relationship signifies
  the linkage between entities. "on-siteImageOf" connects the
  on-site image entity with the water-logging area entity, while
  "cateOf" establishes a connection between the event entity
  and the risk-level entity. "samePosition" and "closeTime" link
  event entities with the same location or close occurrence
  time, effectively capturing the association between entities.

Attribute Enrichment. To increase the amount of information and expressiveness of entities in the KG. By adding more attributes to entities, a more detailed and comprehensive description can be provided, making the KG richer and more useful. Therefore the system further enriches the entities with attribute provided, which are described as follows:

Event Attributes. The event attributes are displayed in Table 1

 Attribute
 Classified Group

 StartTime (ms)
 timestamp

 Depth (m)
 0-0.3,0.3-0.5,0.5-0.8,>0.8

 Duration (h)
 0-1,1-3,3-5,>5

Lanes (number)

Table 1: Event Attributes.

• Influence Attributes. An event's influence is described through relevant text, which can be extracted as feature maps using the Word2Vec[27] model, allowing identification of the important features of the impact text for better understanding of the event's influences.

0-3,3-6,6-9,>9

- Reason Attributes. The cause of an event is also conveyed through text, with its characteristic attribute being the relevant textual description of what triggered the event. This text-based information can also be extracted as feature maps using the Word2Vec model, allowing for a better understanding of the cause of the event.
- Leader Attributes. The leader attribute includes the name and, contact phone number.
- Department Attributes. The department attribute includes the name and location information.
- Region Attributes. The region attribute includes the boundary, area, and number of buildings of the region.
- Water-logging Area Attributes. The attribute of the water-logging area comprises specific location information and area information pertaining to the water-logging area.

- Image Attributes. The on-site image attribute of the event is extracted as feature maps using the ResNet[14] model.
- Risk-level Attributes. The event's risk-level attribute comprises three categories: mild, moderate, and severe.

Knowledge Storage. Currently, there are several popular graph databases available, including Neo4j [47], JanusGraph [29], Arango-DB [53], and TigerGraph [8]. It is worth mentioning that we have discovered that OrientDB [36], as a multi-model database, is also capable of effectively storing graph data. OrientDB is a full-function, NoSQL MMDMS, addressing the big data variety problem with one single, multi-model store and a SQL-based, multi-model query language.

The UrbanFloodKG system uses an object-oriented approach to store triples as node and edge classes. It employs the OrientDB database, which supports graph-based processing, SQL queries, and parallel query execution. OrientDB is not only a graph database but also a multi-model database that can handle both graphs and documents simultaneously. Table 2 shows three types of node and two types of edge in OrientDB and Fig. 4 shows a portion of the KG

Table 2: In OrientDB, there are three categories of node classes - Schema Node, Entity Node and Attribute Node. Additionally, there are two types of edge classes - Schema Edge and Entity Edge. Each node and edge possesses its unique "Name" attribute.

| Class      | Type                    | Name                             |
|------------|-------------------------|----------------------------------|
| Schema     | Schema Node             | Schema name                      |
| Entity     | Entity Node             | SchemaName_Rid                   |
| Attribute  | Attribute Node          | Attribute value                  |
| SchemaEdge | Schema Relation<br>Edge | hasInstance, Relation<br>name    |
| EntityEdge | Entity Relation<br>Edge | Attribute name,<br>Relation name |

## 3.4 Algorithm Layer

*Translation-based models*. The urban flood event information is stored in OrientDB in the form of nodes and edges. It is difficult to directly analyze them, and existing research has proposed KG representation learning [11, 45]. It learns low-dimensional continuous representation vectors (also called embeddings) of entities and relationships while preserving the inherent structure and semantics of the KG.

The process of KG representation learning is described below. Given a knowledge graph  $\mathcal{G}=(\mathcal{E},\mathcal{R},\mathcal{F})$ , which includes embedding vectors  $\mathcal{E}$  and  $\mathcal{R}$  representing entities and relationships, along with a set of triples  $\mathcal{F}$ , the KG representation learning algorithm employs various scoring functions  $\phi$  to calculate scores for entity and relationship embeddings. The goal is to assign higher scores to valid triples compared to invalid ones. By utilizing a predefined loss

function  $\mathcal{L}$ , such as cross-entropy loss or hinge loss [37], the KG representation learning algorithm updates the embedding parameters iteratively until convergence is achieved.

Typical scoring functions utilized for KG representation encompass translation-based models [2]. The system incorporates two translation-based models, namely TransE [2] and HolE [32]. However, to address concerns regarding scalability, two decomposition-based models, namely ComplEx [43] and DisMult [52], are also supported.

Image /page/4/Figure/13 description: A diagram illustrates a neural network architecture for graph processing, flowing from left to right. The process begins with an 'Input' block containing a graph 'G' with four green nodes. This input is fed into a block labeled 'GEN', which contains four variations of the input graph. The output of the 'GEN' block passes through a 'ReLU' activation function. This is followed by a second 'GEN' block and another 'ReLU' function. The next stage is a fully connected layer labeled 'FC', depicted with four input nodes and four output nodes, all interconnected. Finally, the 'Output' block shows the resulting graph where the nodes are colored differently (orange, yellow, and green) and labeled C1, C2, and C3, suggesting a node classification or clustering task.

Figure 5: The GEN Network model for urban flood event classification generates a corresponding classification (C1, C2, C3) for each node.

*GNN-based models*. Some graph neural network models can also be used for knowledge representation, the network structure used in our system is based on the GENeralized Graph Convolution Network (GEN) [21]. In the forward propagation process of the GEN network, the feature vector update equation for each urban flood event node is:

$$\mathbf{x}_{i}' = MLP(\mathbf{x}_{i} + AGG(ReLU(\mathbf{x}_{j} + \mathbf{e}_{ji}) + \epsilon : j \in \mathcal{N}(i)))$$
(1)

The mechanism of information collation and updating in the GEN network is delineated by Equation (1). This procedure involves the renewal of a node's feature vector via a multi-layer perceptron (MLP) and an aggregation function (AGG). In this context,  $\mathbf{x}_i$  signifies the feature vector of node i, while  $\mathbf{x}_j$  is a symbol for the feature vector of node j. Additionally,  $\mathbf{e}_{ji}$  denotes the edge feature vector, encapsulating the attribute information of the edge that connects node j to node i. Besides,  $\epsilon$  is a learnable parameter vector employed to modify the scale and shift of the node feature vector. The model's AGG function makes use of a summation aggregation function.

The structure of the event classification model is shown in Fig. 5. The urban flood event classification model defines two layers of GEN networks and a fully connected layer. The input is a graph G, which includes the feature vectors of each node (node features), the edge indices of adjacent nodes (edge indices), and the feature vectors of each edge (edge attributes). The forward propagation process of the GEN model involves propagating and integrating information on graph-structured data. Nodes update their feature vectors based on information from neighboring nodes, capturing both local and global information within the graph structure.

*Operations*. Typical functions in traditional graph systems [50] are supported by the UrbanFloodKG system, such as Cypher and embedding access. In addition, in order to adapt the system to urban flood risk assessment applications, we have developed three types of functions, which are abstracted as basic operations in Table 3.

Image /page/5/Figure/2 description: A diagram illustrates a knowledge graph with a schema level and an entity level. A legend explains the components: white circles are Schema Nodes, light blue are Entity Nodes, light green are Attribute Nodes, black arrows are Schema Relation Edges, and blue arrows are Entity Relation Edges. The schema level shows nodes for 'Event', 'Department', and 'Leader'. The relationships are: 'Leader' resolves 'Event', and 'Event' belongs to 'Department'. The entity level shows instances: 'Departmnet\_#32:1' is an instance of 'Department' with the name 'Drainage Company'. 'Event\_#30:1' is an instance of 'Event' with a duration of '0-1' and a startTime of '1621900800'. 'Leader\_#31:1' is an instance of 'Leader' with the name 'Zhang' and phone '1391111111'. An entity relation edge connects 'Event\_#30:1' to 'Leader\_#31:1'.

Figure 4: The portion of UrbanFloodKG. Each Entity Node is linked to multiple Attribute Nodes via an Entity Relation Edge, where the edge name corresponds to the attribute name.

Table 3: Operations.

| Operation                               | Return             | Description                                              |
|-----------------------------------------|--------------------|----------------------------------------------------------|
| query(Sql_Command)                      | return result      | Executes Cypher query based on OrientDB on UrbanFloodKG. |
| get_emb(entities, embedding_type,model) | return embedding   | Get the embeddings of entities or relations.             |
| node_cla(feature_Vector,model)          | return level       | Return risk level of event.                              |
| link_pred(src_ent, tar_ent, rel, model) | return probability | Calculates plausibility of an input triple.              |

We use the interfaces provided by ampligraph [7] and PyG [12] to implement the latter three proposed operations.

 query. This operation accepts the Cypher query from the user, which returns the corresponding results on the Urban-FloodKG. For example, users can obtain information about urban flood events that occurred on Shi Nan Road via below query command.

```
MATCH {class:Entity,
WHERE:(name='ShiNanRoad')}.
inE('EntityEdge'){as:m,
WHERE:(name='occurIn')}
RETURN m.out
```

• get\_emb. This operation offers a direct interface for accessing the embeddings of entities or relations in UrbanFloodKG. It particularly provides embeddings for models depending on the input model.

- node\_cla. This operation accomplishes the node classification task within the KG. By supplying the entity's vector feature, the UrbanFloodKG system invokes this operation to perform classification using the embeddings learned by a GNN-based model.
- link\_pred. This operation enables relational link prediction between two entities, src\_ent and tar\_ent, by calculating a score using the input model. And users can obtain the likelihood of a triple fact.

## 3.5 Application Layer

The proposed framework in this paper can be applied to various aspects of urban flood control, which can be summarized as follows:

**Knowledge reasoning**. Based on the KG representation learning model, the possibility of a triplet can be predicted. After training with a large amount of data, users can enter a triplet by themselves,

File Name **Basic Sample Format** Records Event\_ID | StartTime | Duration | Lanes | Depth | Area\_ID | Influence\_ID event.txt 10,000 | RiskLevel 1|1621900800 | 0-3| 1-3 | 0.3-0.5| 4 | 2 | mild Area\_ID | Name 422 waterlogging-area.txt 1|Shinan Avenue Reason\_ID | Name |Event\_ID reason.txt 873 1|large drainage area|1 Influence\_ID | Name influence txt 653 1|Power and communication system interruption Event\_ID | Event\_ID same\_position.txt 2155 1|2 Event ID | Event ID close\_time.txt 1415 1|2Image\_ID | Embedding |Area\_ID image.txt 10000 1 | [0.164,0.135,0.223,...] | 1

Table 4: The files of UrbanFlood Dataset. Each entity has its own attributes and associated ID values with other related entities.

for example (?, leadTo, a certain event), users can input some possible causes of urban flood in the ?, and the model will return a possibility for reasoning the cause of urban flood for a certain event.

*Event classification.* Users can enter various information about urban flood events, such as rainfall, depth, duration, etc. The model predicts the risk level of the event, assigning it a classification grade includes: mild, moderate, or severe. Based on the input information, the model analyzes the event's characteristics, conducts quantitative analysis, calculates the risk score, and maps it to the corresponding risk level.

*Urban decision making*. The model accurately assesses and predicts the risks of urban flood events, aiding city decision-makers in understanding the risk characteristics and impact scope of such events and taking more effective countermeasures. KG-based risk assessment and prediction of urban flood events provides important data and knowledge support for city decision making, contributing to the sustainable development and safe operation of cities.

# 4 EXPERIMENT

In this section, firstly, the construction of the urban flood event dataset is introduced. Then, combined with specific cases, model comparison experiments of link prediction and node classification tasks are carried out to evaluate the effectiveness and applicability of the UrbanFloodKG system we designed.

## 4.1 DataSet Construction & Environment

We gather 10,000 urban flood event data from 2010 to 2018 in Guangzhou and make the dataset. The files included in Table 4 provide details about the dataset. Based on this dataset, we conduct subsequent experiments of link prediction and node classification. The experiments are conducted using PyTorch 2.0.0 on a

host equipped with an AMD Ryzen7 5800 CPU, 32GB RAM, and one NVIDIA GeForce RTX 4080 GPU.

## 4.2 Link Prediction Analysis

In this part, we explore representative applications in the urban flood scenario and summarize the challenges in urban flood research that can be regarded as link prediction problems.

For performance comparison, we adopt the commonly used metrics in the respective task. By conducting performance comparison experiments with various models, we demonstrate the effectiveness of the UrbanFloodKG system.

**Causal Prediction.** The causal prediction use case formulates the traditional causal prediction problem [31] into the link prediction problem on the UrbanFloodKG, which is stated as follows:

Problem 1. UrbanFloodKG-based Reason Prediction Problem. Given the UrbanFloodKG  $\mathcal{G} = \{\mathcal{E}, \mathcal{R}, \mathcal{F}\}$ , a recorded information of urban flood event like reason  $e_r$  lead to the event  $e_e$  can be expressed as  $(e_r, r_{leadTo}, e_e)$  with  $e_r$ , and  $e_e$  as entities and  $r_{leadTo}$  as relation therein.

Hence, the reason prediction problem of potential reasons of an urban flood event  $e_e$ , can be formulated as the link prediction problem of  $(?, r_{leadTo}, e_e)$  in UrbanFloodKG.

The overall framework is depicted in Fig. 6, where the application layer utilizes the link\_pred operation to predict if there exist leadTo links between reason entities and event entities.

To evaluate the proposed framework, we extract a subset of data from our self-constructed UrbanFlood dataset. The dataset is split into train/validation/test sets, following a ratio of 7:1:2.

By using four KG representation learning models: TransE, ComplEx, DistMult, and HolE, we evaluate the effectiveness of our system for reason prediction using the MRR, MR, and Hits@n metrics. Table 5 presents results and illustrates the successful performance of our system in reason prediction.

Image /page/7/Figure/2 description: A flowchart illustrating a data processing pipeline. An initial block labeled "UrbanFlood System" has two arrows pointing to two separate databases, represented by cylinders. The top database is labeled "Reason" and the bottom one is labeled "Event". From the "Reason" database, an arrow labeled "get\_emb" points to a parallelogram labeled "Reason embedding". Similarly, from the "Event" database, an arrow labeled "get\_emb" points to a parallelogram labeled "Event embedding". Both the "Reason embedding" and "Event embedding" blocks have arrows that converge into a single line. This line is labeled "link\_pred" and points to a final rounded rectangle labeled "leadTo".

Figure 6: The illustration of leveraging UrbanFloodKG system for reason prediction problem.

Table 5: The result comparison of reason prediction task.

| Model    | MRR  | MR      | Hits@10 | Hits@3 | Hits@1 |
|----------|------|---------|---------|--------|--------|
| ComplEx  | 0.36 | 1166.96 | 0.69    | 0.54   | 0.16   |
| DistMult | 0.39 | 1010.31 | 0.72    | 0.56   | 0.19   |
| HolE     | 0.49 | 884.47  | 0.85    | 0.71   | 0.27   |
| TransE   | 0.38 | 457.92  | 0.66    | 0.49   | 0.13   |

Problem 2. UrbanFloodKG-based Influence Prediction Problem. Given the UrbanFloodKG  $\mathcal{G} = \{\mathcal{E}, \mathcal{R}, \mathcal{F}\}$ , a recorded information of urban flood event like event  $e_e$  led to the influence  $e_i$ , can be expressed as  $(e_e, r_{leadTo}, e_i)$  with  $e_e$ , and  $e_i$  as entities and  $r_{leadTo}$  as relation therein.

Hence, the influence prediction problem of potential influences caused by an urban flood event  $e_e$ , can be formulated as the link prediction problem of  $(e_e, r_{leadTo}, ?)$  in UrbanFloodKG.

The overall framework is illustrated in Fig. 7. Especially, the application layer calls the operation link\_pred to predict if there exist leadTo links between event entities and influence entities.

Image /page/7/Figure/9 description: A flowchart illustrating a system for predicting relationships. The process starts with an "UrbanFlood System" box, which branches into two parallel paths. The top path leads to a database labeled "Event," which is then processed by a "get\_emb" function to create an "Event embedding." The bottom path leads to a database labeled "Influence," which is also processed by a "get\_emb" function to create an "Influence embedding." Both the "Event embedding" and "Influence embedding" are then combined and fed into a function labeled "link\_pred," which results in a final output labeled "leadTo."

Figure 7: The illustration of leveraging UrbanFloodKG system for influence prediction problem.

To evaluate the proposed framework, we additionally extract a subset of data from our self-constructed UrbanFlood dataset. The dataset is split into train/validation/test sets, following a ratio of 7:1:2. We evaluate the effectiveness of our system for influence prediction by employing four KG representation learning models. Table 6 presents results and illustrates the successful performance of our system in influence prediction.

Table 6: The result comparison of influence prediction task.

| Model    | MRR  | MR     | Hits@10 | Hits@3 | Hits@1 |
|----------|------|--------|---------|--------|--------|
| ComplEx  | 0.55 | 158.83 | 0.67    | 0.60   | 0.49   |
| DistMult | 0.63 | 135.06 | 0.74    | 0.67   | 0.56   |
| HolE     | 0.70 | 165.20 | 0.82    | 0.75   | 0.64   |
| TransE   | 0.43 | 62.15  | 0.57    | 0.47   | 0.35   |

## 4.3 Node Classification Analysis

In this part, we summary the issues about risk assessment in ur-banFlood research that can be considered as node classification problems.

**Risk-level classification.** For the risk assessment of urban flood events, we believe that two hypotheses can be proposed:

- The risk of individual events increases as the number of urban flood events linked to time and location rises. For example, when multiple urban flood events transpire in a particular area within a short period, it suggests that the area possesses inadequate flood prevention measures, thereby escalating the risk of subsequent events.
- The risk increases with the degree of the event node. For instance, when an urban flood event is connected to numerous surrounding urban flood entities, it suggests that the event is located in a high-risk event aggregation area and consequently carries a higher level of risk itself.

In summary, the risk assessment of events should consider both time and spatial elements, not just the events themselves. In our constructed UrbanFlood dataset, the expert evaluation level of the risk of each event, represented by the Risk-level entity, has already been included. Starting from the events' own attributes and considering the related events, we can discover the classification rules between events and effectively assess future urban flood events.

The overall framework is illustrated in Fig. 8. Especially, the application layer calls the operation node\_cla to classify each event node.

Image /page/7/Figure/21 description: A block diagram illustrates a data processing workflow. The process starts with a rectangle labeled "UrbanFlood System" which sends a "query" to a database labeled "Event-related entity". Data from this database and another database labeled "Event" are then processed by a "Feature Engineering" block. The output is a parallelogram labeled "Feature Vector". This vector is then used in a process labeled "node\_cla" to produce the final output, which is a rounded rectangle labeled "Risk-level".

Figure 8: The illustration of leveraging UrbanFloodKG system for Risk-level classification problem.

To evaluate the proposed framework, we sample a subset of data from our self-constructed UrbanFlood dataset. The basic statistics of the dataset are summarized in Table 7. The dataset is split into train/validation/test sets, following a ratio of 7:1:2.

Table 7: Statistics of UrbanFlood dataset for risk-level classification.

| #Nodes | #Edges | #Attrs | Train | Valid | Test |
|--------|--------|--------|-------|-------|------|
| 10,000 | 3570   | 6      | 7000  | 1000  | 2000 |

The experiment compares multiple models and evaluates them using accuracy, precision, recall, and F1-score metrics. The experimental results are shown in Table 8.

Table 8: The result comparison of risk-level classification prediction task.

| Model     | Accuracy | Precision | Recall | F1-score |
|-----------|----------|-----------|--------|----------|
| GATv2 [4] | 0.3564   | 0.5883    | 0.3564 | 0.2669   |
| SG [48]   | 0.3832   | 0.7636    | 0.3832 | 0.2123   |
| AGNN [42] | 0.6741   | 0.6640    | 0.6741 | 0.6558   |
| TAG [10]  | 0.3815   | 0.7640    | 0.3815 | 0.2107   |
| GIN [51]  | 0.3914   | 0.7618    | 0.3914 | 0.2202   |
| GEN       | 0.9136   | 0.9129    | 0.9136 | 0.9126   |

The classification network model based on the GEN model achieves an accuracy of 91%, surpassing other graph neural network models. Additionally, it reveals that by considering the features and properties of urban flood event nodes, it is possible to represent nodes of different urban flood events as vectors for accurate risk assessment.

The classification results are visualized in Fig. 9. After the multidimensional feature vectors of each urban flood event node are reduced by PCA, they are divided into three categories based on the predicted level: mild, moderate, and severe. This approach can effectively assess and predict the risk level of urban flood events.

Image /page/8/Figure/9 description: A scatter plot with an x-axis ranging from -15 to 15 and a y-axis ranging from -10 to approximately 12. The plot displays three categories of data points, indicated by a legend in the top right corner. Blue dots represent 'mild', orange dots represent 'moderate', and green dots represent 'severe'. The green 'severe' points are clustered on the left side of the plot, primarily for x-values less than 0. The orange 'moderate' points form a vertical band in the center of the plot. The blue 'mild' points are clustered on the right side of the plot, primarily for x-values greater than 5.

Figure 9: The Visualization of the Classification Results.

# 5 RELATED WORK

We summarize the related work into two aspects: KG-based systems and flood risk assessment-based systems.

Knowledge graph-based systems. Traditional KG-based systems encompass Freebase [1], DBpedia [20], WordNet [28], Wikidata [44], YAGO [41], and others. These systems primarily concentrate on general or encyclopedic knowledge, which is constructed from vast amounts of unstructured text data and structured semantic network data, such as Wikipedia. For instance, the first three systems gather structured knowledge from user contributions on Wikipedia, WordNet provides formal linguistic knowledge about words, and YAGO integrates factual information extracted from Wikipedia using rule-based and heuristic methods, along with WordNet.

Flood risk assessment-based systems. With the development of flood risk assessment in recent years [9, 33], the latest research has designed systems for terrain data management [5, 18, 40]. Wang [46] leverages multiple information sources to determine the parameters of the flood model. They also investigate the influence of different approaches to handling terrain datasets on the outcomes of flood modeling. Notably, their study emphasizes the significance of capturing the micro-features of cities to improve the accuracy of modeling results. Lyu [25] employs the FAHP-FCA method to incorporate various factors, including regional and subway longitudinal subsidence, in order to assess the flood risk of the Shanghai subway system within a subsidence environment. Rahadianto [35] uses analytical hierarchy process to help the system to assess how much impact and damage that will be hit the risky area and give the recommendation to government and people how to increase the preparedness so it can reduce the damage from flood. Li [22] proposes a hydraulic model and flood calculation program, demonstrating the feasibility of the proposed method and identifying areas with inadequate flood control capacity in the Xiushui River.

# 6 CONCLUSION

In this paper, we propose the UrbanFloodKG system, a KG-based urban flood system. We propose a solution to construct KG from urban flood data with different structures and patterns and implements multi-modal data fusion. Based on the constructed UrbanFloodKG, the system seamlessly combines knowledge representation models and graph neural network models to offer comprehensive relevant operations. Finally, we classify the practical application problems of flood risk assessment into link prediction and node classification tasks and evaluate the effectiveness and feasibility of the models using multiple models, providing a new perspective for flood risk assessment

# 7 ACKNOWLEDGEMENTS

The paper is supported by the Research on Key Technologies for Improving Flood Control Safety System of Nansha District, Guangzhou (823005916); the Jiangsu Province Water Conservancy Science and Technology Project (2022003); the Major Science and Technology Project of the Ministry of Water Resources (SKS-2022139).

# **REFERENCES**

