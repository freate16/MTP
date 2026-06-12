
## **ABSTRACT**

We employ multi-modal data (i.e., unstructured text, gazetteers, and imagery) for location-centric demand/request matching in the context of disaster relief. After classifying the *Need* expressed in a tweet (the WHAT), we leverage OpenStreetMap to geolocate that *Need* on a computationally accessible map of the local terrain (the WHERE) populated with location features such as hospitals and housing. Further, our novel use of flood mapping based on satellite images of the affected area supports the elimination of candidate resources that are not accessible by road transportation. The resulting map-based visualization combines disaster-related tweets, imagery and pre-existing knowledge-base resources (gazetteers) to reduce decision-making latency and enhance resiliency by assisting individual decision-makers and first responders for relief effort coordination.

## CCS CONCEPTS

• **Information systems** → *Decision support systems*;

## **KEYWORDS**

disaster relief, location-centric processing, flood mapping, need matching

## **ACM Reference Format:**

Shruti Kar<sup>1\*</sup>, Hussein S. Al-Olimat<sup>1\*</sup>, Krishnaprasad Thirunarayan<sup>1</sup>, Valerie L. Shalin<sup>1</sup>, Amit Sheth<sup>1</sup>, Srinivasan Parthasarathy<sup>2</sup>. 2018. D-record: Disaster Response and Relief Coordination Pipeline. In *Proceedings of SIGSPATIAL Workshop (ARIC 2018)*, Jennifer B. Sartor, Theo D'Hondt, and Wolfgang De Meuter (Eds.). ACM, New York, NY, USA, Article 4, 4 pages. https://doi.org/10.475/123\_4

## 1 INTRODUCTION

Recent catastrophic events, e.g., resulting from floods and hurricanes, combined with increased urbanization and interdependent infrastructure reveal an increasing vulnerability to natural and human-made hazards. A resilience framework must accommodate both precise information for action and for various levels of analysis, posing substantial challenges [4]. These include characterizing hazards with an integrated ontology across voluminous, multi-modal

Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the full citation on the first page. Copyrights for third-party components of this work must be honored. For all other uses, contact the owner/author(s).

ARIC 2018, Nov. 2018, Seattle, Washington
© 2018 Copyright held by the owner/author(s).
ACM ISBN 123-4567-24-567/08/06.
https://doi.org/10.475/123\_4

data sources, facilitating rescue/response actions, and assessing the effects of pre- and post-disaster actions on individual needs.

The dire real-time need for integrated, coherent multi-modal data from different sources has motivated substantial research [8]. Social media is a significant source of such data. Twitter users, for example, post short texts as updates. These messages (a.k.a. tweets) reveal *Needs* and requires matching with possible available help. These messages can provide critical information to first responders and individual decision-makers to contribute effectively to relief efforts [18]. Tweets authored about crisis events may contain crucial but unstructured location-centric information (such as incident reports) even when explicit geo-tagging is absent. The ability to extract specific location information from this unstructured terminology and the other attached information is critical for timely assistance by the first responders.

Crowdsourced data (such as OpenStreetMap) that covers the geographical area of a disaster event can assist in the extraction of location content from tweets. To achieve this, we developed D-record: **D**isaster **re**sponse and **re**lief **coord**ination, a pipeline that utilizes multi-modal data (i.e., unstructured text, gazetteers, and satellite imagery). D-record allows first responders to visualize and match location-centric *Needs* and options for available help while taking into account transportation constraints and available options in the local area of a disaster.<sup>1</sup>

## 2 RELATED WORK

The following related work informs the D-record pipeline and clarifies its contributions

Disaster-Centric Ontologies. Lightweight lexicons or vocabularies like the Management of Crisis Vocabulary (MOAC)<sup>2</sup>, CrisisNLP<sup>3</sup>, and CrisisLex [21] provide the different concepts for disaster management but lack the granularity required for describing response and miss crucial spatial and thematic details. Other efforts like UNOCHA's Humanitarian eXchange Language (HXL)<sup>4</sup> improve information sharing during disasters but lacks specific crisis-related concepts. The Social Media and Emergency Management (SMEM) ontology [13] combines emergency domain knowledge with social media information for Incident Classification. However, SMEM focuses on major coarse-grained categories of disasters such as meteorology or biology. As stated above, state-of-the-art techniques in event representation for disaster response is critically limited with respect to the usability and dissemination of recommended action and response (intentional intervention) required for relief

<sup>\*</sup>Authors contributed equally.

<sup>&</sup>lt;sup>1</sup>The source code of the pipeline is available at https://github.com/shrutikar/d-record.

<sup>&</sup>lt;sup>2</sup>http://observedchange.com/moac/ns/

<sup>3</sup>http://crisisnlp.qcri.org/

<sup>4</sup>http://hxlstandard.org/

efforts coordination. Given the above limitations, D-record uses a location-centric ontology to assist in matching relevant needs with available help to support a disaster response use-case as discussed in Section 3.

**Need Classification.** For extracting the type of *Needs* (e.g, food, shelter, or medical) from text data, state-of-the-art Need classification techniques such as [16] focus on the identification of information type. However, these techniques do not provide a comprehensive solution for matching classification output. [5] merely summarizes disaster information at a certain geographical level without providing any actionable decisions for response and relief. Instead, they provide summaries of topics to decision makers. Our previous classification technique [3] uses an ontology and location detection to enhance situational awareness through recognizing the interdependencies between disaster events, which helps in the early identification of Needs. Inspired by these techniques, D-record employs a coarser Need classifier to make its classifications compatible with the affordances of locations (e.g., a shelter can support a variety of Needs such as food and water whereas a hospital can provide medical and rescue support *Needs*). In other words, we resort to coarser needs (as opposed to fine-grained needs) for effective matching because available help centers satisfy multiple needs.

**Matching.** Our previous technique on Seekers and Suppliers matching [18] uses hand-crafted rules to match the *Need* requested with a possible provider, e.g., matching someone offering shelter with someone requesting shelter. Other approaches to *Need* matching such as [6] uses structured input from users and utilizes moderators in the loop to match those *Needs* with organizations presently available to help. The *Need*-capacity matching technique by [17] quantifies the degree of impact of a disaster and prioritizes the matching accordingly. Finally, [14] provides both online and offline solutions for requesting, providing and coordinating resources.

Limitations of the above work include: (a) the inadequate assumption that all routes are available for matching by assuming the full accessibility of roads during a disaster [19], and (b) the matching problem being solved for a different level of granularity than for the required individual level of *Needs*.

**Flood Mapping.** Some logistical matching methods assume the full accessibility of routes. Hu et al. [7], for example, provides an algorithm for optimal path selection in a logistics supply-chain management system. In contrast, [15] provides a portal for UN staff to upload spatial data including satellite images and crowdsourced data that can identify blocked routes. We use our customized state-of-the-art human-guided flood mapping technique [11] to prune the flooded routes to reflect the situation on the ground relevant for better-informed transportation.

**Data Visualization.** The majority of the visualization techniques in the literature place geo-tagged tweets on a map [12] or display users' structured input such as in [20]. However, these techniques fail for social media-based systems where geo-tagged tweets are relatively infrequent, and the information is buried inside unstructured texts. [10] showed the effectiveness of layered visualization systems, where each layer can contain a different source of information. In D-Record, each layer can include a different *Need* class or OpenStreetMap location features. To visualize the kinds of

Image /page/2/Figure/8 description: A diagram illustrating a system for disaster relief coordination and response, which processes data from multiple sources to create a layered map for matching seekers and providers. The process is shown in three main parts. The first part details the data sources on the left: 'Classify and Geoparse Tweets' using Twitter and LNEx; 'Satellite Image for Flood Mapping' using satellite imagery to identify flooded locations; and 'OpenStreetMap and Crowd-sourced Location Features'. The outputs from these sources are processed to 'Prune Flooded Locations' and are then combined into a stack of map layers shown in the center. The layers, from top to bottom, are: Flood Areas, Twitter Medical/Rescue Needs, CS Medical/Rescue Available, OSM Medical/Rescue Available, Twitter Shelter/Food/Supplies Needs, CS Shelter/Food/Supplies Available, OSM Shelter/Food/Supplies Available, and a base layer from MapBox. Each layer is associated with a specific icon. The final part, at the bottom, is labeled 'Disaster Relief Coordination and Response' and contains a box for 'Map Directions & Seekers/Providers Matching', illustrated with icons of a person, a map, and another person, signifying the matching of those in need with those providing aid.

Figure 1: D-record map layers and pipeline functions

*Needs* effectively they are bound to their spatial footprints extracted using our tool LNEx [2].

## 3 METHOD

The following section describes the different data sources, the functionality of the pipeline, and the map layers we employ that support the visualization of information. Figure 1 contains a summary of map layers and their purpose.

**Data Sources.** D-Record utilizes three data sources: Twitter, OpenStreetMap, and Satellite Images. Twitter data consists of two groups. The first group contains a set of two targeted streams from two disaster events, namely, the Chennai Flood in 2015 and Houston Flood in 2016 [2]. The second group of crisis tweets is from CrisisNLP [9] and CrisisLexT26[16] datasets labeled for their information type (e.g., affected individuals, donations, and volunteering). The first group drives the pipeline. The second is used to train a binary classifier to recognize the expression of *Need* in tweets and expand the concepts in the underlying ontology (see Section 3). Crowd-sourced data from volunteers (contributed as Excel sheets) contain information about shelters and help requests/offers (e.g., Chennai Flood - List of Corporation and Relief Centres<sup>5</sup>).

The OpenStreetMap gazetteer provides location names and metadata (such as geo-coordinates) that produce the affordances of each location with respect to the needed help (e.g., a hospital can provide rescue and medical support) allowing for matching a help offer with a *Need* request from tweets. The Output of our flood mapping tool [11], which uses satellite images, determines the flooded geo-points and overlays this information on top of the map.

**Location-Centric Ontological Modeling.** Determining spatially and temporally specific instances for coordinating resources *Needs* benefit from a domain-specific location-centric event ontology for social media data. Event location is key to both aggregation and analysis of related event instances. Therefore, we created an event ontology that uses information from past disaster and risk reports<sup>6</sup> to enrich existing disaster event vocabularies.

The D-Record ontology<sup>7</sup> represents the temporal distinction between the response and relief phases of a disaster. The class "Concepts" includes two kinds of concepts: *Needs* and Availability. The class OSMFeatures covers the affordances of various location types (i.e., OSM map features<sup>8</sup>) in relation to the *Need* classes.

<sup>&</sup>lt;sup>5</sup>https://rebrand.ly/reliefspreadsheet

<sup>6</sup> such as by https://www.acaps.org/

<sup>&</sup>lt;sup>7</sup>The ontology can be found at https://github.com/shrutikar/d-record.

<sup>&</sup>lt;sup>8</sup>http://wiki.openstreetmap.org/wiki/Map\_Features

Image /page/3/Figure/2 description: A flowchart detailing a data processing pipeline for disaster response and scenario dissemination. The process begins on the left with a 'Data' section, which includes three sources: 'Stream and Crowd Sourced Data' (with icons for Twitter and Excel sheets), 'Pre-Disaster Data' (with the OpenStreetMap logo), and 'Satellite Imagery' (with the NOAA logo). The data flows through a series of processing steps. Stream and crowd-sourced data undergo 'Semantic Filtering' and then 'Information Retrieval/Extraction'. This extraction process, also fed by pre-disaster data, branches into 'Geoparsing' (using LNEx), 'Seekers / Providers need classification', and 'OSM location classification with map feature types'. The 'Seekers / Providers' data is further processed by 'Event Ontology & Situational Data' using 'Lexicon NLP'. Satellite imagery is used for 'Flood Mapping'. The processed data streams converge: 'Geoparsing' and 'Event Ontology' data become 'Typed geolocated data', while 'OSM location classification' and 'Flood Mapping' data are used to 'Prune/Filter Locations'. Both of these outputs are then stored via 'Caching in ElasticSearch'. From the cache, 'map layers' are created using 'mapbox'. These layers are used for 'Seekers / Providers Matching'. This matching process leads to 'Provide turn-by-turn directions with contact information', which is also informed by 'Prune non-available routes' from the flood mapping. There is a feedback loop from providing directions back to the matching process. The final step is 'Scenario Dissemination', illustrated by a map with colored risk zones and a route between points X and A.

Figure 2: D-record system architecture

| <b><i>Need</i> Class</b>              | <b>CrisisNLP and CrisisLexT26 Classes</b>                                                     |
|---------------------------------------|-----------------------------------------------------------------------------------------------|
| Shelter/Food/<br>Supplies <i>Need</i> | donation_needs_or_offers_or_volunteering_services,<br>displaced_people_and_evacuation         |
| Medical/Rescue<br>Help <i>Need</i>    | missing_trapped_or_found_people, deaths_reports, in-<br>jured_or_dead_people, affected_people |

Table 1: Our mapping of CrisisNLP and CrisisLexT26 classes

The set of keywords for a "Needs" concept was expanded using topic modeling learned from the labeled data for the two classes: Shelter/Food/Supplies and Medical/Rescue Help. The relevance probability of each word to the Need class/topic functioned as a feature while training our Need classifier as shown in Section 3. Finally, the sub-classes of the Needs concept are mapped to the OSMFeatures sub-classes representing the options for available help at each location type (i.e., the affordances). For example, hospital maps to the Medical/Rescue Help class and pharmacy maps to the Shelter/Food/Supplies Need class.

**Text Classification.** To leverage the existing labeled data from CrisisNLP and CrisisLexT26, we combined the overlapping classes to form the two *Need* classes (see Table 1). We used tweets from these datasets to train an SVM-based classifier which allows Drecord to categorize any given crisis related text into one of the two classes: Shelter/Food/Supplies *Need* or Medical/Rescue Help *Need*. The *Need* class Shelter/Food/Supplies includes donations, volunteer services, and *Needs* for food, water, shelter, or clothes. The *Need* class Medical/Rescue Help comprises affected people, death reports, injured or dead people, missing or trapped people, and other medical and rescue-related information. The classified streaming text appears on the map for matching.

The classifier had to capture tweet semantics. A simple Bag-of-Words model lacks context. Instead, feature engineering [22] vectorizes the text sentences to capture their semantics adequately. Before featurizing, the text was preprocessed by stemming, case folding and removing "noisy" lexical elements (such as URLs, non-ASCII characters, mentions, punctuations, dataset-specific stopwords, and hashtags). Finally, we designed an SVM classifier with lexicon-based features, TF-IDF vectors, and gensim's word2vec embeddings<sup>9</sup>.

Using the relevance probabilities from topic modeling described earlier, we form lexicon-based two-tuple feature vectors (i.e., Shelter/Food/Supplies and Medical/Rescue Help). Each element in the vector represents the word frequency multiplied by its relevance score. This vector was concatenated with the other features from TF-IDF and gensim's word2vec embeddings, which captures the semantics of a word by looking at the context where it was mentioned. To address the class imbalance, SMOTE oversampled the minority class synthetically.

**System Architecture.** D-record uses three major forms of data (see Figure 2): Streaming and Crowdsourced, pre-disaster, and satellite imagery data. The knowledge extracted from text streams (filtered using hashtags of the disaster event) and crowdsourced excel sheets provides situational awareness and the various kinds of help available at each location. The pre-disaster information available from OpenStreetMap (sliced using a bounding box of the disaster event) represented the available help confirmed or pruned using satellite images. The output from our flood mapping method [11] helped prune out routes that were unavailable during the matching process for the location seeking help.

Our tool LNEx extracts and attaches each location to their latlong information which locates tweet information on the map, following *Need* classification. Since OpenStreetMap provides the metadata for locations (including names, types, and geo-coordinates), the flood map information is used to prune out the locations that are flooded and not accessible for help. D-record caches all of this information in Elasticsearch. The *Need* information and location of a tweet indicate where the help is needed while OSM location features identify available help. We create the map layers on top of MapBox<sup>10</sup>. The system then matches a *Need* in the ontology with the locations that can fulfill that *Need*. D-record ultimately prunes all routes containing a flooded section according to the flood map.

## 4 RESULTS

SVM with the SMOTE (to partially overcome class imbalance) and the Gradient Boosting Algorithm performed the best and achieved a 0.8 F-Score in the *Need* classification task. We tested it using the leave-one-out technique (i.e., testing on one dataset and training using the rest). D-record extracted locations from tweets to support plotting these tweets on the map. The experiments used our Chennai and Houston datasets, containing 169,838 and 415,057 tweets, respectively. From these tweets, LNEx extracted 85,564 locations from the Chennai dataset and 241,684 locations from Houston dataset. As for the number of OpenStreetMap location features, 1,103 and 2,826 locations were retrieved for the affected areas of Chennai and Houston, respectively. Other crowdsource data received from the excel sheets were relatively few, around 41 locations.

## 5 DEMONSTRATION

Figure 3 shows D-record where users can choose the time range to filter the data using ⓐ, the dataset using ⓑ, and select the map layers using ⓒ. To match a *Need*, the user clicks on the orange icons as in ① which shows a textbox with the tweet text and the extracted location. Users can click on a "Match Need" button to get the closest and non-flooded nearby location which can provide help for the given *Need*, as in ②. Users obtain the matched location information by hovering the mouse over the green icons as in ③. The tool will provide the full information of the matched location and the contact number if available with the turn-by-turn directions obtained using MapBox directions API<sup>11</sup> as shown in ④.

<sup>9</sup>https://radimrehurek.com/gensim/

<sup>10</sup> https://www.mapbox.com/

<sup>11</sup>https://www.mapbox.com/help/define-directions-api/

Image /page/4/Figure/2 description: A screenshot of a disaster management user interface called "HazardsSEES". The interface is split into a left sidebar and a main map view. The left sidebar has a logo, a time range selector set to "12-01-2015 1:30 PM - 01-30-2016 2:00 PM", a location selector with "Chennai" selected, and a legend for map icons such as "Flooded Areas", "Medical/Rescue Help Available", and "Shelter/Food/Supplies Needed". The main map area displays a map of Chennai with purple patches indicating flooded areas. On the map, there is a pop-up window showing a message: "@Uber\_Chennai - Need help in rescuing a group of girls from Perumalagaram Salai Chennai! #ChennaiMicro #ChennaiFloods" with a "Match Need" button. A blue line indicates a route on the map. Another pop-up identifies the "ACS Medical College And Hospital". In the bottom right, a box shows "Matched Location Info" for the hospital, including its address and turn-by-turn directions.

Figure 3: Example screenshot of the D-record tool.

## 6 CONCLUSIONS AND FUTURE WORK

A domain-specific location-centric event ontology is crucial for situation awareness and disaster response. We demonstrated our D-record pipeline for *Need*-offer matching and discussed the functionality of the system and the multi-modal data used to fire its engine. The pipeline can be used to match coarse-grained *Needs* with possible suppliers meaningfully using location information available on the map. In the future, a finer-grained classifier can be designed to do more flexible or specific matching. Additionally, we plan to develop a custom entity extractor building on our prior work [1], to extract emerging entities during the onset of a disaster for more advanced spatiotemporal reasoning. We also plan to use weather data and background knowledge to mark flood-prone areas to help in preparedness in addition to response. To empower first and local responders, we intend to bring this pipeline for broader use by the disaster response community and port it to smartphones.

## **ACKNOWLEDGMENTS**

We would like to thank our collaborators Jiongqian (Albert) Liang, Jiayong Liang (Jay), Desheng Liu, and Nikhita Vedula from the Ohio State University for providing the flood mapping data.

This research was supported by the NSF award EAR-1520870 "Hazards SEES: Social and Physical Sensing Enabled Decision Support for Disaster Management and Response". All views are those of the authors and do not necessarily reflect the views of the sponsor.


