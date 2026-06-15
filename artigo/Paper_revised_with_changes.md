# Urban Flooding in a Tropical Coastal Environment: Spatiotemporal Patterns for Early Warning and Resilience

**Versão revisada com alterações da dissertação sinalizadas**

---

## Legenda de marcações

| Marcação | Significado |
|----------|-------------|
| `📌 [INSERÇÃO — diss. §X.X]` ... `[/INSERÇÃO]` | Trecho novo inserido a partir da dissertação |
| `✂ [SUBSTITUIÇÃO — diss. §X.X]` ... `[/SUBSTITUIÇÃO]` | Trecho original substituído por versão da dissertação |
| ~~texto~~ `✏️ [EDITORIAL — R1-CX]` | Correção editorial menor; R1/R2 = revisor, C# = comment |
| `⚠️ [NOTA]` | Orientação para o autor sobre a alteração |

---

## Authors

Hanna Soares Viana, Fabricio Polifke

Department of Meteorology, Institute of Geosciences, Universidade Federal do Rio de Janeiro – UFRJ, CCMN - Cidade Universitária - Ilha do Fundão, Avenida Athos da Silveira Ramos, 274, Rio de Janeiro, RJ, 21941-916, Brazil

Contact: hannasviana@gmail.com, fabriciopolifke@igeo.ufrj.br

---

## Abstract

Urban flooding disrupts mobility and municipal operations in large coastal cities, yet rainfall information and impact records are often analyzed separately. We integrate 15-min rainfall from 33 rain gauges with 4,868 georeferenced, operationally classified urban flooding occurrences in Rio de Janeiro to characterize spatiotemporal impact patterns and to build a rainfall impact framework for future threshold development. Rainfall time series were segmented into independent events using a 6 h minimum dry interval; each event was described by duration and maximum 1 h intensity. Occurrence records were cleaned, assigned to three severity levels based on water depth and traffic disruption, and paired with rainfall using Thiessen polygon influence areas and timing overlap. Results show that moderate-severity road ponding dominates the database (86.6%), while high-severity street flooding accounts for 9.6%. Event persistence increases with severity: pooled low- and moderate-severity events have a median duration of 1.95 h (90th percentile 5.71 h), whereas high-severity events have a median of 2.99 h (90th percentile 8.36 h). Occurrences peak in summer (2,330 events) and concentrate in late afternoon and evening during warm seasons, with persistent spatial hotspots and broader footprints for high-severity impacts. Network coverage is strong (median distance to nearest gauge 1.81 km; 90% within 3.59 km), supporting robust pairing at the city scale. The framework provides actionable evidence on when and where impacts cluster and supports locally meaningful rainfall thresholds for early warning and urban resilience.

**Keywords:** Urban flooding impacts; Early warning; Rainfall thresholds; Spatiotemporal analysis; Thiessen polygons; Rio de Janeiro

---

## 1. Introduction

Urban flooding is among the most persistent socioenvironmental challenges in large cities, particularly where rapid and unplanned growth has outpaced investments in stormwater infrastructure and maintenance capacity [1]. In dense urban settings, disruptive flooding impacts often arise not only from extreme rainfall in a climatological sense, but also from the interaction between rainfall intensity, impervious surfaces, drainage connectivity, and local terrain controls that accelerate and concentrate overland flow toward low-lying streets and underpasses [2]. These hydrologic transformations have direct implications for urban sustainability~~,~~ **,** because they result in recurring disruptions to mobility, degraded service reliability, and increased operational stress on municipal systems. ✏️ *[R1-C1: vírgula adicionada após "urban sustainability"]*  They can also propagate downstream ecological degradation through altered flow regimes and hydrogeomorphic instability, reinforcing that urban flooding is both a hazard and a systemic stressor on urban watersheds [3]. Recent urban flood syntheses highlight that the same rainfall event can yield sharply different outcomes across neighborhoods depending on exposure, infrastructure condition, and the efficiency of runoff conveyance and storage, which makes the urban flood problem intrinsically uneven within the city fabric and therefore highly relevant for equity and resilience agendas [4].

Urban flood risk is also shaped by how cities conceptualize and implement stormwater management, as practices and design philosophies vary widely across regions and institutions [5]. This diversity affects not only engineered performance but also how cities plan interventions, prioritize maintenance, and communicate risk to residents, all of which are core themes in sustainable urban governance. Because impacts are fundamentally spatial, decision support often benefits from combining hydrometeorological information with geospatial frameworks that represent vulnerability gradients and heterogeneous susceptibility within the urban fabric, enabling more targeted preparedness and response [6]. These considerations are particularly relevant where drainage capacity is uneven, where informal occupation limits engineered solutions, and where small-scale infrastructure failures can trigger large mobility and safety disruptions during intense rainfall.

The climate change context adds urgency to urban flood risk management, as sustainable city planning increasingly requires that infrastructure and services remain functional amid changing extremes. Physical constraints and model evidence indicate that the hydrologic cycle can intensify with warming, increasing the likelihood of heavy precipitation events even when mean rainfall changes are uncertain [7]. Observational and modeling studies further indicate that short-duration rainfall extremes can intensify in a warming atmosphere, with important implications for fast-responding urban catchments and drainage systems designed for historical intensity-duration-frequency characteristics [8]. In some settings, the strongest hourly extremes may increase faster than simple thermodynamic expectations, implying a heightened risk of damaging downpours that overwhelm local drainage and produce rapid-onset impacts on roads and critical facilities [9]. From a risk perspective, the IPCC emphasizes that infrastructure deficits and sociospatial inequality amplify vulnerability~~,~~ and that adaptation and risk management must be context-specific and attentive to heterogeneous exposure within cities, which directly motivates localized, impact-oriented approaches [10]. ✏️ *[R1-C2: vírgula removida após "vulnerability"]*

Beyond rainfall alone, compounding processes can amplify flood impacts in coastal cities, where boundary conditions can constrain drainage outflow and increase the likelihood of severe street-level impacts. The co-occurrence of storm surge and heavy precipitation can produce compound flooding, increasing water levels and limiting drainage outflow in low-lying coastal zones, particularly in coastal metropolitan areas, where mobility disruption and service interruption can cascade rapidly [11]. At broader scales, global exposure to riverine and coastal flooding has increased over time due to expanding assets and populations in flood-prone areas, highlighting the importance of integrating socioeconomic dynamics into risk framing and emphasizing that urban development pathways shape flood consequences [12]. Global analyses also show that future flood risk is driven by both climatic and socioeconomic change, indicating that adaptation needs must be evaluated jointly with development pathways and the evolution of the built environment [13]. Observational evidence from satellite-based flood databases further supports the view that flood exposure is rising and that flood impacts are increasingly intertwined with land-use change and urban expansion, reinforcing the need for urban-scale diagnostics that connect hazard and impact [14]. These dynamics are not purely physical, since flood risk and flood losses also reflect feedbacks between society, governance, and the evolving built environment, which can influence where people settle, how protection is prioritized, and how risk is perceived. Sociohydrology provides a conceptual lens to describe how protection measures, settlement patterns, and risk perception can interact to shape flood outcomes, sometimes producing unintended trajectories of increasing exposure, which is central to understanding why risk can grow even when protective measures exist [15].

✏️ *[R1-C3: parágrafo anterior dividido aqui. O parágrafo original era excessivamente longo e a ideia central era difícil de detectar.]*

This perspective helps clarify why many cities remain predominantly reactive and why moving toward anticipatory risk management often requires operational triggers that translate forecasts and observations into expected impacts. An emerging direction is to connect forecast information to action through explicit decision thresholds and impact-oriented products, improving the timeliness and efficiency of interventions under uncertainty. Forecast-based financing frameworks, for example, formalize when it is worth acting based on forecast probabilities and costs, enabling earlier mobilization when risk exceeds defined triggers and helping institutionalize anticipatory action [16]. In parallel, proof-of-concept impact-based forecasting systems for pluvial floods demonstrate how rainfall forecasts can be coupled with inundation and damage models to estimate expected consequences, moving beyond rainfall-only warnings toward impact-relevant information for municipal decision-making [17]. At larger scales, operational flood early warning platforms based on ensemble forecasting and threshold exceedance provide examples of how probabilistic information can be translated into actionable alerts, while also highlighting the importance of calibration, local relevance, and risk communication for real-world usability [18]. Together, these approaches underscore that data and methods capable of linking rainfall to observed impacts are essential building blocks for resilient and sustainable city operations.

---

> **📌 [INSERÇÃO — dissertação §2.5.1–2.5.4 | Responde: R1-C5 (novidade do estudo)]**
>
> Several studies have developed empirical rainfall-impact frameworks using operational or citizen-reported flood data in urban environments, providing relevant benchmarks for the present work. Georganta et al. [36] defined intensity-duration thresholds for flood identification in the Attica region, Greece, using emergency calls from fire brigades as flood proxies; their approach of establishing lower and upper threshold curves bounding a zone of mixed conditions is methodologically analogous to the EA/ESA classification adopted here. Tian et al. [37] inferred critical rainfall thresholds for urban pluvial flooding in Rotterdam from a large citizen-observation database, applying machine learning to identify the most informative rainfall duration scales and demonstrating that both short-duration peak intensity and longer-duration accumulated volume are jointly relevant predictors. At broader scales, DeSouza et al. [38] incorporated socioeconomic and built-environment variables alongside rainfall metrics in a multivariate regression framework for Denver, showing that population density and infrastructure conditions amplify the rainfall-to-impact translation. Ramos Filho et al. [39] introduced an antecedent precipitation index (API) into the threshold framework for São Paulo, substantially reducing false alarm rates by conditioning the rainfall intensity threshold on prior soil moisture state. To our knowledge, the present study provides one of the first city-scale assessments in Brazil to integrate high-temporal-resolution rain gauge observations with georeferenced, operationally classified urban flooding impact records across a full municipal domain, explicitly distinguishing three operational severity classes and establishing a reproducible rainfall-to-impact pairing framework. This spatiotemporal characterization and EA/ESA pairing structure are designed to directly support severity-specific threshold development — an analytical step not yet delivered in this manuscript and identified as a primary direction for subsequent work.
>
> **[/INSERÇÃO]**

---

In Rio de Janeiro, these challenges are recurrent and particularly complex due to strong spatial and seasonal rainfall variability and the frequent occurrence of intense warm-season precipitation episodes, often concentrated in the afternoon and evening hours, when exposure and mobility demand are also high [19]. Short response times and localized convective forcing make it harder to anticipate which neighborhoods will experience disruptive impacts, a challenge consistent with broader findings on flash flood forecasting constraints and uncertainty at small spatial scales [20]. This motivates approaches that integrate high-temporal-resolution rainfall observations with georeferenced records of urban flooding events to identify robust spatiotemporal patterns of impact and to support the development of locally meaningful thresholds for early warning and operational decision-making. In a sustainability and resilience context, such evidence-based diagnostics can inform targeted preparedness, the prioritization of critical areas and time windows, and more efficient deployment of municipal resources, thereby strengthening the city's capacity to maintain functionality during extreme rainfall.

---

## 2. Methodology

### 2.1 Study Area

This study focuses on the municipality of Rio de Janeiro, characterized by an extensive coastal zone, coastal massifs, urbanized plains, and internal drainage basins. With high population density (5,174.60 inhabitants per square kilometer) and intense urbanization, the municipality experiences recurrent episodes of intense rainfall and associated impacts, including water accumulation on roads, disruption of urban mobility, and operational stress on municipal services. The physical and geographic setting of Rio de Janeiro contributes to strong spatial heterogeneity in urban hydrological risk. The coexistence of low-lying coastal plains and depressed areas with steep relief associated with the main massifs produces contrasting hydrologic responses over short distances, ranging from rapid runoff generation on slopes to flow convergence and accumulation in lowlands. Therefore, the analysis adopted in this study combines the spatial variability of rainfall observed by a rain gauge network with georeferenced records of water accumulation events to characterize spatiotemporal patterns of impact and support the interpretation of rainfall triggers associated with urban disruptions.

**Figure 1.** Study area and rain gauge network in Rio de Janeiro. (a) Location of the municipality of Rio de Janeiro within Brazil. (b) Municipality boundary overlaid on elevation (m) and the Alerta Rio rain gauge network (orange markers), with station identifiers shown next to each gauge. Major topographic features, including the Gericinó, Pedra Branca, and Tijuca massifs, are indicated for reference.

### 2.2 Data Sources

Primary data were obtained from two sources: one representing hydrometeorological forcing and the other representing observed impacts in the urban environment, enabling explicit integration of rainfall with occurrence. Rainfall information was obtained from the Alerta Rio system, a network of automatic rain gauges distributed across the city's neighborhoods. For this study, accumulated rainfall records at 15-minute resolution from 33 stations were used, with station selection based on measurement availability. In addition to the time series, station metadata, including identifier, name, geographic coordinates (latitude and longitude), and elevation, were provided and used for georeferencing and for applying rainfall spatialization methods. Although the raw rainfall archive spans a longer period, the analyses presented here considered the time window coincident with the available occurrence records, from January 2015 to December 2024.

Occurrence records were obtained from COR Rio, which maintains a georeferenced operational database of street-level water accumulation and flooding impacts, classified by severity and including date, time, and location. The database contained 87,620 records for the period from 10 April 2015 to 26 March 2024. For this study, 4,868 records directly related to urban flooding impacts were selected and grouped into three operational severity categories: road water ponding (86.6 percent), shallow water layer (3.8 percent), and street flooding (9.6 percent).

---

> **📌 [INSERÇÃO — dissertação §2.1 e §3.2.2 | Responde: R1-C4 e R1-C6 (descrição do dataset COR Rio)]**
>
> The COR Rio operational database provides records with the following original attributes for each event: occurrence type (using COR Rio's own operational terminology), geographic location (neighborhood and geographic coordinates), start and end date and time, event description, and, in most cases, a severity classification and estimated resolution time. The classification of water accumulation events follows COR Rio's municipal operational protocol, which distinguishes events based on their impact on vehicle and pedestrian circulation. Under this protocol, *poças* (puddles) refer to small surface accumulations that do not significantly affect mobility. *Bolsão d'água* (road ponding) designates conditions in which pedestrians are required to enter the water to cross the road, although light vehicle traffic remains possible, albeit impaired. *Alagamento* (street flooding) refers to conditions in which light vehicle circulation is fully prevented, representing a higher operational severity level. Beyond these categories, the database also includes records classified as *enchente*, *inundação*, and *enxurrada*, which correspond to larger-scale fluvial flooding events and were excluded from this study due to their different triggering mechanisms. The operational protocol for *bolsão d'água* events specifies that natural drainage via the urban stormwater system is the primary expected response. When natural drainage does not occur satisfactorily, the municipal urban cleaning company (Comlurb) is activated to clear the roadway and verify the need for unblocking of drainage inlets. The selected 4,868 records therefore correspond to the three sub-categories most directly associated with pluvial street-level flooding: *Lâmina d'água* (shallow water layer, 0–15 cm, mapped to Type I), *Bolsão d'água em via* (road ponding, 15–30 cm, mapped to Type II), and *Alagamento* (street flooding, 30–50 cm, mapped to Type III). These original COR Rio categories were grouped and relabeled by the authors for analytical consistency, as described in Section 2.4.
>
> **[/INSERÇÃO]**

---

These records constitute the impact dataset used for spatiotemporal characterization and for subsequent association with rainfall events. To our knowledge, this study provides one of the first city-scale assessments in Brazil to integrate high-temporal-resolution rain gauge observations with georeferenced, operationally classified urban flooding impact records, enabling an empirical rainfall-to-impact pairing framework that supports subsequent threshold development for early warning and municipal decision support. Studies with similar operational-data approaches have been conducted in the Attica region of Greece [36], Rotterdam [37], and São Paulo [39], but a city-scale, severity-stratified characterization integrating gauge networks with municipal impact records has not previously been reported for a Brazilian metropolis of this size and complexity.

### 2.3 Definition and Parameterization of Rainfall Events

A quantitative and descriptive approach was adopted to investigate the relationship between rainfall volumes and urban flooding impacts in Rio de Janeiro by integrating rain gauge observations and georeferenced occurrence records. The central premise is that identifying discrete rainfall events at each station enables consistent comparison across hydrometeorological episodes and facilitates evaluation of temporal coincidence with recorded impacts in the urban environment. The continuous rainfall time series at each station was segmented into discrete rainfall events to support intensity-duration analyses. A rainfall event was defined as a period with continuous rainfall records, separated from the subsequent event by a minimum dry interval of 6 hours. The definition of independent rainfall events and the choice of a minimum inter-event time are widely recognized as critical steps because they directly affect derived event properties such as duration, peak intensity, and event totals [21,22,23]. Sensitivity of event statistics to inter-event separation criteria has also been documented across climatic settings, reinforcing that the selected dry interval is an operational decision that should be explicitly stated and justified [24,25,26,27].

In this study, the 6-hour interval was used to reduce the merging of distinct episodes and to represent each event as an independent unit for subsequent pairing with occurrence records within the same temporal window [22,25]. For each rainfall event identified at each station, two parameters were computed. Duration (D) was defined as the total event length in hours, from the first to the last rainfall record. Maximum intensity (I) was defined as the highest rainfall rate observed during the event, computed as the maximum accumulated rainfall over a 1-hour window, corresponding to four consecutive 15-minute measurements, expressed in millimeters per hour. In this way, each rainfall event is characterized by a persistence metric (D) and a peak metric (I), providing the basis for subsequent intensity-duration analyses linked to urban impacts. Because intensity duration metrics are sensitive to how rainfall events are separated, the explicit event definition above is essential for reproducibility and for comparison with other threshold-based urban flood studies [25,27].

### 2.4 Processing and Classification of Urban Flooding Occurrences

Urban flooding occurrence records were obtained from COR Rio, which compiles georeferenced reports of street-level water accumulation and flooding impacts across different sectors of the municipality during the analyzed period. After selecting records related to urban flooding impacts, data cleaning was performed to remove duplicates and exclude occurrences with invalid geographic coordinates. This step is necessary to ensure spatial consistency when associating with station influence areas and to avoid redundant entries that artificially inflate occurrence frequencies. For each occurrence, event duration was calculated as the difference between the end time and the start time recorded in the database, providing a persistence metric of the impact. This variable serves as a complementary indicator of operational severity, since more persistent occurrences typically require longer response times and may imply longer mobility disruption. The availability of impact persistence information is particularly useful in urban contexts where threshold design aims to distinguish frequent minor disruptions from less frequent but more consequential events [28,29].

For statistical analyses, occurrences were classified into three severity levels, denoted Type I, Type II, and Type III, following the operational severity categories provided by COR Rio's municipal classification protocol (described in Section 2.2). ✏️ *[R1-C6: frase revisada para deixar explícito que a classificação parte do protocolo operacional do COR Rio, não de uma categorização criada pelos autores.]* Type I corresponds to shallow water accumulation between 0 and 15.0 centimeters (*Lâmina d'água*) and represents an initial stage of accumulation with low operational impact. Type II corresponds to water ponding between 15.0 and 30.0 centimeters (*Bolsão d'água em via*), in which light vehicle traffic remains possible but impaired, and pedestrians are typically required to enter the water to cross the street. This is the most frequent class in the database, representing 86.6 percent of the selected occurrences. Type III corresponds to street flooding between 30.0 and 50.0 centimeters (*Alagamento*) and is characterized by fully preventing light vehicle traffic, being considered a higher operational severity condition. This hierarchical classification supports future threshold development by enabling rainfall event attributes to be linked not only to whether impacts occurred, but also to the severity and persistence of the observed impacts, consistent with approaches in urban pluvial flood threshold studies that distinguish impact categories to improve warning usefulness [28,29,30]. For the present study, the selected 4,868 impact records span all three severity classes, preserving the operational severity variability represented in the dataset.

### 2.5 Thiessen Polygons and Rainfall Occurrence Association

Thiessen polygons were selected for their simplicity and effectiveness in deterministically assigning influence areas to each rain gauge station, which is appropriate for associating each occurrence with a nearby representative measurement point. The Thiessen approach transforms point rainfall measurements into a spatial representation by zones of influence, facilitating integration with georeferenced occurrence records at the municipal scale. Efficient and reproducible generation of Thiessen polygons and associated weights has been described in the hydrologic and civil engineering literature, supporting their use as practical pairing methods for operational rainfall networks [31,32]. Voronoi-based approaches have also been explored for precipitation remapping and spatial allocation, reinforcing the methodological consistency of Voronoi partitions as a spatial framework for precipitation-related analyses [33]. Polygons were generated statically using the set of stations with available data during the analysis period. Projected station coordinates were used to generate Voronoi diagrams, and the resulting polygons were clipped to the municipal boundary of Rio de Janeiro to ensure that only influence areas within the study domain were considered. This clipping prevents external areas from affecting the spatial assignment and preserves coherence with the municipal scale analysis [31].

Spatial association was performed by assigning each georeferenced occurrence to the polygon in which it was located. Subsequently, temporal association was established by considering that a rainfall event acted as a trigger when the start time of the flooding occurrence fell within the time interval of the rainfall event recorded at the station associated with the corresponding polygon. ✏️ *[R2 Major Comment 2: frase original era circular ("quando o horário de início do evento de chuva caiu dentro do intervalo do evento de chuva"). Corrigido para deixar explícito que é o horário de início do alagamento que deve cair dentro da janela temporal do evento de chuva — regra estrita, 0 min de antecedência. Ver análise de sensibilidade na Seção X.]* Therefore, rainfall-to-impact integration is constructed through two complementary steps: one spatial and one temporal, enabling the identification of coincidences between rainfall episodes and recorded urban flooding impacts. It is important to recognize that polygon-based pairing inherits limitations related to spatial rainfall variability and rain gauge network geometry. The spatial distribution and density of rain gauges can influence the representation of areal rainfall and its associated uncertainty, particularly for short-duration rainfall processes [34]. Comparisons between gauge-only and radar-supported areal rainfall estimates in small catchments further indicate that representativeness issues are more important for short-duration rainfall and convective regimes, supporting the need to report pairing assumptions explicitly and to test robustness where feasible [35].

> **📌 [INSERÇÃO — Responde: R2 Major Comment 5 (validação do Thiessen com radar)]**
>
> A formal cross-validation of the Thiessen-based areal rainfall representation against independent spatial measurements — such as radar-derived precipitation fields — was not performed in this study, as operational radar data at the required temporal resolution were not available for the analyzed period. This constitutes a recognized limitation of the spatial pairing approach. In convective regimes, such as those typical of Rio de Janeiro during summer, rainfall can vary sharply over distances of 1–3 km, meaning that the nearest-gauge assumption embedded in Thiessen polygons may introduce systematic errors in the estimated rainfall at individual occurrence locations, even when the gauge-to-occurrence distances are short [34,35]. The distance analysis presented in Section 3.7 (median 1.81 km, 90th percentile 3.59 km) provides indirect evidence that spatial coverage is adequate for stratiform and widespread rainfall events. However, for convective episodes — which are precisely the events most likely to trigger flooding in Rio de Janeiro — point-to-area representativeness cannot be formally assessed without spatially continuous rainfall fields. Future applications of this framework should incorporate radar-gauge merging or high-resolution gridded rainfall products to evaluate the sensitivity of the EA/ESA classification to spatial interpolation method, and to quantify what fraction of classification errors may be attributable to rainfall measurement mismatch rather than genuine non-response of the urban drainage system.
>
> **[/INSERÇÃO]**

### 2.6 Event Classification and Computational Implementation

To support future threshold definition, based on the methodology of Georganta et al. [36], rainfall events were classified as Event with Flooding (EA) when rainfall resulted in at least one flooding event within the respective station's influence area, and as Event without Flooding (ESA) when no flooding event occurred. This polygon-based classification provides a direct framework for comparing hydrometeorological events with and without recorded impacts, while preserving the spatial reference of the station considered representative for each occurrence. Similar event-pairing concepts are commonly used in rainfall-threshold-based warning studies for urban pluvial flooding, where rainfall events are separated and labeled according to whether impacts occurred, enabling empirical discrimination of triggering conditions [28,29,30].

---

## 3. Results and Discussion

✏️ *[R1-C16: título da seção alterado de "Results" para "Results and Discussion", pois a seção contém interpretações e discussão ao longo do texto.]*

### 3.1 Overall Characterization of Occurrences

The distribution of occurrence types is strongly unbalanced across classes (Figure 2). Out of 4,868 records, 4,217 (86.6 percent) correspond to Type II, road water ponding, whereas 466 (9.6 percent) are classified as Type III, street flooding, and 185 (3.8 percent) as Type I, shallow water layer. This pattern indicates that the operational database primarily captures high-frequency, mobility-relevant events, that is, recurrent surface water accumulation episodes that disrupt circulation, even when they do not represent large-scale fluvial flooding. The predominance of Type II suggests that the most common reported impacts are associated with localized drainage limitations and transient surface water storage on roads, both of which are highly relevant to municipal operations and traffic management during rainfall.

---

> **📌 [INSERÇÃO — dissertação §2.1 e §4.1 | Responde: R1-C7 (implicações do Tipo II sem evidência) e R1-C21 (proximidade de corpos d'água)]**
>
> This interpretation is supported by the operational response protocol established by COR Rio, in which *bolsão d'água* events are expected to resolve through natural drainage via the urban stormwater system, and the municipal cleaning company (Comlurb) is activated when natural drainage is insufficient, typically due to blocked drainage inlets or overloaded local conveyance elements [see Section 2.2]. However, it is important to note that this attribution to drainage limitations should be treated with caution: several Type II hotspot locations identified in the spatial analysis (Section 3.5) lie in proximity to water bodies and coastal zones, where tidal backwater effects and low-lying topographic depressions may also contribute to surface water accumulation independently of drainage infrastructure performance [40]. Quantitative disentanglement of drainage-driven from topography-driven and tide-modulated impacts would require additional spatial covariates not analyzed in the present study and is identified as a priority for future work.
>
> **[/INSERÇÃO]**

---

In contrast, the lower proportion of Type III does not imply negligible severity, but rather that events capable of fully preventing light vehicle circulation occur less frequently in the analyzed set. This marked contrast across categories supports the need to evaluate severity-specific rainfall thresholds in subsequent steps, since rainfall triggers associated with frequent moderate impacts may differ from those associated with less frequent but more disruptive events.

**Figure 2.** Distribution of occurrence types related to water accumulation on roads and street flooding in Rio de Janeiro (N = 4,868). Type II (Bolsão d'água em via) accounts for 86.6 percent of the records, followed by Type III (Alagamento) with 9.6 percent and Type I (Lâmina d'água) with 3.8 percent.

### 3.2 Event Duration and Persistence Patterns

Figures 3 and 4 summarize the duration of recorded water accumulation occurrences by severity class, separating lower-impact events from the most disruptive category. Because Type I events represent a small fraction of the database and are operationally closer to Type II than to Type III, Types I and II are analyzed together as a low-to-moderate severity group, while Type III is evaluated separately as the high-severity class. For each severity group, Figures 3 and 4 are organized into two panels. Panel (a) shows a histogram of event duration. The horizontal axis represents duration in hours, and the vertical axis represents the number of events in each duration bin. The bars, therefore, indicate how frequently events of a given duration occur. ✏️ *[R1-C8: vírgula inserida antes de "therefore" para uso correto da conjunção.]*  Three vertical reference lines are superimposed to summarize key statistics for the distribution shown in the histogram: a dashed red line for the mean duration, a dashed green line for the median duration, and a dotted orange line for the 90th percentile. These lines provide a direct visual comparison between typical events, captured by the median, and the influence of longer events on the mean, as well as the duration threshold beyond which only 10 percent of events persist.

Panel (b) shows the cumulative distribution function of event duration. The horizontal axis again represents duration in hours, while the vertical axis represents the cumulative percentage of events with duration less than or equal to a given value. The blue curve, therefore, increases from 0 percent to 100 percent as the duration increases, and the shaded area highlights the distribution's cumulative nature. ✏️ *[R1-C15: vírgula inserida antes de "therefore".]* Two horizontal reference levels are particularly informative: 50 percent corresponds to the median duration, and 90 percent corresponds to the duration exceeded by only 10 percent of events. Vertical guides and annotated values indicate the corresponding durations. Importantly, both severity groups are displayed using a visualization cutoff at 12 hours. The label in panel (b) reports the number of events included in the plotted distributions, N (< 12 h), as well as the total number of events for which duration could be computed. A separate box labeled **All Data** (shown in the inset of panel b) reports summary statistics computed using the full set of events with valid duration values, including those longer than 12 hours. ✏️ *[R1-C12: label capitalizado e localização na figura explicitada.]* This distinction is crucial because long-duration outliers strongly affect the mean and upper-tail metrics.

For the pooled Types I and II group, the histogram in Figure 3a is strongly right-skewed, with a pronounced concentration of events at short durations. The highest frequencies occur within the first hour, followed by a rapid decay as duration increases. This pattern indicates that most low-to-moderate-severity occurrences resolve relatively quickly, consistent with transient street ponding episodes that dissipate as rainfall intensity decreases and local drainage resumes. The vertical reference lines quantify this short-duration dominance. Within the subset plotted (< 12 h), the median is 1.95 hours and the mean is 2.61 hours, with the mean exceeding the median, as expected under a right-skewed distribution where a smaller fraction of longer events pulls the average upward. The 90th percentile is 5.71 hours, indicating that 90 percent of Types I and II occurrences last less than about 6 hours, while the longest 10 percent persist substantially longer than the typical event.

The cumulative distribution in Figure 3b reinforces this interpretation: ✏️ *[R1-C9: "(top)" removido — desnecessário na referência à figura.]* the curve rises steeply at short durations and then gradually approaches 100 percent, visually confirming a large mass of short-duration events and a long tail. The **All Data** inset shows that when events longer than 12 hours are included, the mean increases to 3.29 hours and the 90th percentile rises to 6.77 hours, while the median changes only slightly to 2.03 hours. This behavior is diagnostically important. It implies that the distribution's central tendency remains controlled by short-duration events. Still, a relatively small number of long-duration cases adds a measurable contribution to the upper tail and to the mean. In other words, Types I and II are predominantly short-lived. Yet, the database also contains a non-negligible fraction of persistent occurrences that may reflect local infrastructure constraints, prolonged rainfall, delayed drainage recovery, or operational persistence in the reporting and closing process.

**Figure 3.** Duration distributions for pooled low to moderate severity occurrences (Types I and II). (a) Histogram of event duration (hours) with mean, median, and 90th percentile indicated by vertical lines. (b) Cumulative distribution of event duration. Only events shorter than 12 hours are plotted for readability; the inset reports summary statistics for all valid durations.

The Type III distribution shows systematically higher persistence than Types I and II. In the histogram (Figure 4a), frequencies remain concentrated at relatively short durations, but the mass shifts toward longer values, and the tail is visibly heavier. Within the subset plotted (< 12 h), the median increases to 2.99 hours and the mean increases to 3.88 hours, indicating longer typical durations and stronger right skewness than in the pooled Types I and II group. The 90th percentile reaches 8.36 hours, meaning that the longest 10 percent of Type III occurrences persist for more than about 8 hours, even when focusing only on events shorter than 12 hours. The cumulative distribution (Figure 4b) provides an especially clear representation of this enhanced persistence. The curve rises more slowly than in the Types I and II cases, indicating that a smaller fraction of events resolves rapidly and that a larger fraction remains active at intermediate durations. In operational terms, these are events more likely to generate sustained disruption, including longer mobility restrictions and extended demand for municipal response.

The full dataset statistics highlight how extreme the upper tail can be for high-severity events. When all durations are included, the mean duration rises to 8.62 hours, the median rises to 4.12 hours, and the 90th percentile reaches 22.72 hours. Such a striking result because it implies that a meaningful subset of Type III records persists for many hours to nearly a full day. Two interpretations are plausible and not mutually exclusive. First, the physical and infrastructural context of Type III events may involve deeper ponding in critical low-lying areas, constrained drainage outlets, obstruction of conveyance elements, or compounding conditions that slow recovery, such as sustained rainfall or unfavorable downstream boundary conditions.

---

> **📌 [INSERÇÃO — dissertação §4.1 | Responde: R1-C13 (fatores físicos do Tipo III) e R1-C22 (baixa elevação/drenagem sem suporte)]**
>
> In particular, low-lying coastal areas in Rio de Janeiro can experience tidal backwater effects that constrain the outflow from urban stormwater systems during periods of high sea level, extending the duration of surface water accumulation beyond what would be expected from rainfall forcing alone [40]. This tidal-drainage interaction has been identified as a key modulator of event persistence in similar coastal urban environments and is consistent with the observed long upper tails in Type III durations. However, because the present study does not include tidal gauge or sea-level data in the analysis, this interpretation remains qualitative and subject to confirmation through future work that explicitly integrates coastal boundary conditions.
>
> **[/INSERÇÃO]**

---

Second, because duration is computed from the start and end times recorded in the operational database, very long durations may also reflect operational factors, such as delayed record closure, persistence of the reported condition beyond the immediate hydrological response, or administrative handling across shifts. The magnitude of the Type III upper tail, as shown by the all data 90th percentile, strongly suggests that these long-duration cases merit targeted quality checks, as they are consequential for both interpretation and threshold design.

**Figure 4.** Duration distributions for high-severity occurrences (Type III). (a) Histogram of event duration (hours) with mean, median, and 90th percentile indicated by vertical lines. (b) Cumulative distribution of event duration. Only events shorter than 12 hours are plotted for readability; the inset reports summary statistics for all valid durations.

The contrast between pooled Types I and II and Type III indicates that severity in this dataset is associated not only with the immediate level of impact, but also with persistence. Types I and II reflect a regime dominated by short-duration disruptions, whereas Type III reflects a regime with longer typical durations and a much heavier tail of prolonged cases. From an early warning perspective, this supports the concept that rainfall triggers for the most disruptive events may depend more strongly on duration-related rainfall metrics and the persistence of intense or recurrent rainfall, rather than solely on short peak intensity. These results also motivate severity-specific threshold strategies. If the objective is to support operational monitoring, a threshold calibrated to the dominant Types I and II population would primarily capture short-lived disruptions. Still, it may not adequately anticipate the conditions associated with Type III persistence, where the longest duration and potentially highest socioeconomic costs occur. Therefore, subsequent steps should explicitly evaluate rainfall intensity-duration metrics separately for low-to-moderate and high-severity events, and should also test whether the longest-duration tail of Type III corresponds to specific locations, seasons, or timing patterns, as this would inform spatially localized thresholds and targeted preparedness actions.

### 3.3 Temporal Distribution of Occurrences

Figure 5 summarizes the temporal variability of the occurrence database using two complementary views. Panel (a) presents the monthly distribution, where the horizontal axis lists months from January to December and the vertical axis shows the average number of events. The solid blue line with markers represents the monthly mean occurrence count computed over the analyzed years. The light-blue-shaded envelope corresponds to the 95% confidence interval around the mean, highlighting interannual variability and uncertainty in the estimated monthly average. In other words, narrower shading indicates more stable month-to-month behavior across years, whereas wider shading indicates stronger dispersion of monthly counts among different years. Panel (b) shows the seasonal distribution as a bar chart. The horizontal axis lists the four seasons, and the vertical axis shows the number of events. The values printed above the bars represent the absolute counts for each season, and the total sample size used in this analysis is N = 4,868. Figure 5a depicts the monthly distribution of occurrence counts. The horizontal axis lists the months from January to December, and the vertical axis represents the average number of events. The blue line with circular markers shows the monthly mean computed over the analyzed years, while the light blue shaded band indicates the 95 percent confidence interval around the mean, summarizing interannual variability in monthly counts. Therefore, months with a wider shaded band exhibit stronger year-to-year dispersion, whereas months with a narrower band show more stable behavior across the time series.

The curve reveals a pronounced warm-season maximum. The mean number of occurrences increases from January, reaching its highest value in February at approximately 110 events per month on average, corresponding to approximately 980 total February events accumulated over the analyzed period, followed by elevated levels in March (approximately 780 total events, mean ~87/month) and December (approximately 700 total events, mean ~78/month), and a still-high frequency in January (approximately 670 total events, mean ~74/month). ✏️ *[R1-C18: tendências agora descritas quantitativamente com valores totais e médias mensais, além das médias. Fonte: dissertação §4.2.]* From April onward, the mean declines sharply, reaching its lowest levels during winter, with July presenting the minimum monthly average (approximately 30 total events over the period, mean ~3/month). After late winter, the curve increases again, with a gradual rise from September through November: total September counts average approximately 40 events/month, rising to approximately 55 in October and 70 in November, indicating the transition back toward the wet season and culminating in the early summer increase. A key diagnostic feature is the behavior of the 95 percent confidence band. The band is visibly wider during the warm-season months, indicating that the magnitude of summer occurrences varies substantially from year to year. Such a pattern suggests that a relatively small number of high-impact rainfall episodes in each summer can strongly amplify the annual occurrence burden. At the same time, other years may exhibit fewer disruptive events. In contrast, the narrower confidence band during winter suggests that low occurrence levels are comparatively consistent year to year, reflecting a stable baseline of fewer reported water accumulation impacts.

Figure 5b complements the monthly view by aggregating occurrences by season. The horizontal axis lists the four seasons, the vertical axis shows the number of events, and the values above each bar provide the absolute totals. The total sample size is indicated as N = 4,868. The seasonal counts show a strong concentration in summer, with 2,330 events, followed by autumn with 1,534, spring with 697, and winter with 307. In proportional terms, this corresponds to approximately 47.9 percent of events in summer, 31.5 percent in autumn, 14.3 percent in spring, and 6.3 percent in winter. This seasonal structure is consistent with the earlier findings that Type II occurrences dominate the database and that, for the pooled Types I and II group, durations are typically short. A warm-season maximum implies that the operational system primarily captures periods when intense rainfall is more frequent and when short-duration precipitation bursts are more likely to trigger recurrent surface water accumulation and mobility disruption. The winter minimum aligns with the climatological dry season in Rio de Janeiro, reflecting reduced rainfall forcing and fewer resulting impacts. Importantly, the presence of 307 winter events indicates that such occurrences are not strictly confined to the wet season, suggesting that rainfall intensity is not the sole control on reported impacts. Local susceptibility factors, including drainage limitations, microtopography, chronic blockage, and known structural bottlenecks, can allow impacts to occur even during relatively drier months. From an operational perspective, this reinforces the need to treat urban flooding events as the outcome of a rainfall-impact system rather than rainfall alone.

**Figure 5.** Temporal distribution of occurrence records in Rio de Janeiro (N = 4,868). (a) Monthly mean number of events with a 95 percent confidence interval. (b) Seasonal totals.

The temporal patterns in Figure 5 have direct operational implications. First, threshold calibration and validation should emphasize the warm-season months, when occurrence frequency and interannual variability are highest, as indicated by the February peak in Figure 5a and the summer dominance in Figure 5b. Second, the strong warm-season signal suggests that short-duration rainfall metrics are likely to be particularly informative for the dominant low-to-moderate-severity events, given the short typical durations previously observed. However, year-to-year dispersion during summer also indicates that a single deterministic seasonal expectation may be insufficient for preparedness planning.

---

> **✂ [SUBSTITUIÇÃO — dissertação §4.2 + Figura 11 (chart_19_seasonal_by_type) | Responde: R1-C19 (análise sazonal por tipo deve ser feita no estudo, não como "próximo passo")]**
>
> *Texto original removido:*
> ~~"A useful next step is to quantify monthly and seasonal patterns separately for Types I, II, and III and to evaluate whether the temporal peak is driven mainly by Type II frequency or whether the proportion and persistence of Type III events also exhibit seasonality."~~
>
> *Texto revisado:*
>
> To evaluate whether the temporal peak is driven mainly by Type II frequency or also reflects systematic seasonality in higher-severity events, Figure 11 presents the monthly and seasonal distribution stratified by occurrence type. Panel (a) shows the monthly mean count for each type, and panel (b) presents the seasonal totals broken down by Type I, Type II, and Type III. The analysis confirms that the strong warm-season concentration documented in Figure 5 is predominantly shaped by the high frequency of Type II events: summer accounts for approximately 47.9 percent of all Type II occurrences (2,017 of 4,217 records), consistent with convective rainfall episodes that rapidly overwhelm local drainage and generate transient road ponding. Type III events, while less numerous, also exhibit a pronounced summer concentration (approximately 46.0 percent of Type III records occur in summer), indicating that the most severe impacts are not temporally distributed differently from the overall pattern. This parallel seasonality suggests that the same warm-season rainfall regime that drives frequent Type II events also produces conditions — likely involving higher rainfall totals and durations — that are capable of triggering the more persistent and severe Type III flooding. Type I events, by contrast, show a somewhat broader seasonal spread, though the small sample size limits interpretation. From an operational perspective, the convergence of Type II and Type III seasonal peaks in summer reinforces that warning readiness, infrastructure preparedness, and response capacity should be simultaneously heightened during this season for both moderate and high-severity scenarios.
>
> **[/SUBSTITUIÇÃO]**
>
> ⚠️ *[NOTA: Figure 11 = arquivo `artigo/chart_19_seasonal_by_type.png`. Inserir como nova figura no artigo, com legenda abaixo.]*
>
> **Figure 11.** Seasonal distribution of occurrence records in Rio de Janeiro by severity type. (a) Monthly mean number of events per type with 95 percent confidence intervals. (b) Seasonal totals for Type I, Type II, and Type III.

---

### 3.4 Hourly Distribution of Occurrences by Season

Figure 6 presents the hourly distribution of occurrence records for each season. Each panel corresponds to one season and reports the seasonal sample size in the panel title: summer (N = 2,330), autumn (N = 1,534), winter (N = 307), and spring (N = 697). In all panels, the horizontal axis represents the hour of day (00:00 to 23:00), and the vertical axis represents the number of events recorded at each hour. Bars show the count of occurrences starting at each hour. A grey dashed horizontal line marks the seasonal mean hourly count, providing a baseline level expected under uniform hourly occurrence. A red dotted horizontal line marks a higher threshold, labeled as mean plus one standard deviation, which highlights hours with unusually high counts relative to the seasonal average. Bars displayed in a darker shade within each panel indicate the hours that exceed the mean plus one standard deviation, emphasizing the periods of the day when occurrences concentrate most strongly.

In summer (Figure 6a), the hourly distribution shows a pronounced late-afternoon and evening concentration. Counts increase markedly after mid-afternoon and peak between approximately 18:00 and 20:00, with multiple consecutive hours exceeding the mean plus one standard deviation threshold. This sustained exceedance indicates that the summer maximum is not a single-hour anomaly but a robust daily window of elevated risk. In autumn (Figure 6b), the distribution also shows a strong evening maximum, with the highest counts occurring around 19:00 to 22:00, again exceeding the mean plus one standard deviation threshold across several hours. Autumn also shows a smaller morning enhancement, around 06:00 to 08:00, suggesting that a broader range of rainfall-producing situations may trigger impacts than in summer. These warm-season evening peaks are consistent with the well-known diurnal cycle of convection in Rio de Janeiro, in which surface heating and land-sea breeze circulations favor convective initiation and intensification during the second half of the day [19]. In practical terms, this timing aligns with earlier results showing that most records are low to moderate in severity and that typical durations for pooled Types I and II are short, which supports an interpretation dominated by short-duration rainfall bursts producing transient ponding and street-level water accumulation. Operationally, the late-day peak is particularly relevant because it overlaps with periods of high urban activity and commuting, which can amplify socioeconomic disruption, even for moderate water accumulation, especially along key road corridors.

In winter (Figure 6c), counts are much lower, and the distribution appears more irregular, as expected given the smaller sample size. The figure shows isolated hourly maxima, notably around 06:00, 16:00, and 23:00, with some of these hours exceeding the mean plus one standard deviation level. Because winter totals are small, these peaks should be interpreted cautiously, as a limited number of events can generate apparent spikes. Nevertheless, the presence of occurrences throughout the day indicates that impacts are not strictly confined to the climatological wet season, suggesting that local susceptibility factors such as drainage limitations, microtopography, chronic blockages, and known structural bottlenecks can still generate operational flooding even under relatively drier seasonal conditions. Spring (Figure 6d) shows an intermediate pattern between warm-season concentrations and winter dispersion. The distribution suggests relatively higher counts in the morning, with an enhancement around 08:00 to 10:00, and additional isolated peaks in late afternoon and evening. Compared to summer and autumn, spring exhibits weaker sustained exceedance above the mean plus one standard deviation threshold, indicating less sharply defined risk windows. This broader timing may reflect seasonal variability in rainfall-generating mechanisms, combined with spatially heterogeneous urban susceptibility.

**Figure 6.** Hourly distribution of occurrence records by season in Rio de Janeiro. Bars show the number of events by hour of day for summer (N = 2,330), autumn (N = 1,534), winter (N = 307), and spring (N = 697). The dashed line indicates the seasonal mean hourly count, and the dotted line indicates mean plus one standard deviation; darker bars highlight hours exceeding this threshold.

### 3.5 Spatial Distribution of Occurrences by Type

---

> **📌 [INSERÇÃO — responde: R2 Major Comment 5 (class breaks não especificadas)]**
>
> ⚠️ *[NOTA METODOLÓGICA: Antes da descrição das Figuras 7 e 8, os autores devem especificar se os intervalos de classe (Very Low a Very High) são compartilhados entre os painéis ou calculados independentemente para cada mapa. Se calculados independentemente, a comparação visual entre painéis indica onde estão os hotspots, mas não quanto mais denso é um tipo em relação a outro. Recomenda-se adicionar a seguinte frase no início desta seção, ou na seção de métodos (Section 2.5), após a descrição dos polígonos de Thiessen:]*
>
> The density surfaces in Figures 7 and 8 were computed using kernel density estimation applied to the georeferenced occurrence points. Density class breaks (Very Low, Low, Medium, High, Very High) were computed **independently for each panel** using quantile-based classification, so that each panel uses the full range of the color scale irrespective of the absolute density values in other panels. This approach emphasizes relative spatial concentration within each type or season and is appropriate for identifying hotspot locations. However, because class boundaries differ across panels, the maps should not be used to compare absolute density magnitudes between types or seasons; for such comparisons, density values in consistent units (events per square kilometer) are reported in the text where relevant.
>
> **[/INSERÇÃO]**

---

Figure 7 maps the spatial concentration of occurrence records using density surfaces for (a) all types combined and (b to d) each occurrence type separately. The colored patches represent relative density classes of occurrence concentration, categorized from Very Low to Very High, as shown in the legend inside each panel. Darker colors correspond to higher density classes.

Figure 7a (All Types) shows that occurrences are not spatially uniform across Rio de Janeiro. The highest-density classes form a dominant hotspot structure along the eastern coastal and central sectors of the municipality, with additional medium- to high-density areas extending into adjacent urban areas.

---

> **✂ [SUBSTITUIÇÃO — dissertação §4.3 | Responde: R1-C20 ("urban corridors" não definido) e R1-C21 (áreas próximas de corpos d'água)]**
>
> *Texto original removido:*
> ~~"...with additional medium- to high-density areas extending into adjacent urban corridors. This indicates that the operational occurrence database is shaped by recurrent impact locations rather than by a citywide, homogeneous response to rainfall, consistent with the idea that urban susceptibility and infrastructure bottlenecks play a key role in converting rainfall into reported impacts."~~
>
> *Texto revisado:*
>
> ...with additional medium- to high-density areas extending into adjacent densely urbanized sectors, particularly along major road axes in the Zona Norte, the Centro, and in the Zona Oeste neighborhoods of Campo Grande and Bangu. Neighborhoods with the highest occurrence counts — including Tijuca, Centro, Botafogo, Lagoa, and São Cristóvão, each with more than 100 recorded events over the analyzed period — are predominantly located in lowland or transitional areas between the coastal plains and the massif slopes. This indicates that the operational occurrence database is shaped by recurrent impact locations rather than by a citywide, homogeneous response to rainfall, consistent with the idea that urban susceptibility plays a key role in converting rainfall into reported impacts. The recurrence of impacts in these specific locations reflects a combination of factors: high impervious surface cover, high population density, older or undersized drainage infrastructure, and, in several cases, proximity to water bodies and coastal areas where tidal back-pressure can limit drainage outflow capacity [40].
>
> **[/SUBSTITUIÇÃO]**

---

Figure 7b (Type I) displays a more selective and localized pattern, with density concentrated primarily in parts of the coastal and highly urbanized corridor, and comparatively weaker representation across much of the northern and western interior, suggesting that Type I occurrences may be more closely tied to specific contexts where shallow-water accumulation is frequently reported and recorded, potentially reflecting both local drainage sensitivity and operational reporting practices.

Figure 7c (Type II) closely mirrors the All Types map. Such a pattern provides an internal consistency check with the earlier results: because Type II accounts for the large majority of records, it largely determines the overall hotspot structure. In other words, the spatial signature of the full database effectively corresponds to that of Type II occurrences and reinforces the interpretation that the most common impacts in Rio de Janeiro are recurrent road ponding and mobility-relevant water accumulation episodes concentrated in specific densely urbanized areas.

---

> **✂ [SUBSTITUIÇÃO — dissertação §4.3 | Responde: R1-C21 e R1-C22 (implicações de drenagem e baixa elevação não sustentadas)]**
>
> *Texto original removido:*
> ~~"...reinforces the interpretation that the most common impacts in Rio de Janeiro are recurrent road ponding and mobility-relevant water accumulation episodes concentrated in specific urban corridors."~~
>
> *Observação: a frase anterior foi mantida com a modificação acima (substituição de "urban corridors" por "densely urbanized areas"). O trecho a seguir substitui a interpretação que atribui o padrão espacial do Tipo II exclusivamente a limitações de drenagem:*
>
> ~~"The predominance of Type II in specific urban corridors suggests that these locations are subject to recurrent drainage limitations and transient surface water storage. However, the spatial overlap between Type II hotspots and proximity to water bodies and coastal areas cautions against attributing the pattern solely to urban infrastructure deficiencies."~~
>
> *Texto revisado:*
>
> It is important to note that several Type II hotspot areas lie in close proximity to coastal water bodies and low-lying basins, including the Lagoa Rodrigo de Freitas, Baía de Guanabara coastline, and Canal do Mangue. In these locations, surface water accumulation may reflect not only drainage infrastructure limitations, but also topographic depression and tidal-modulated drainage constraints that are not attributable to urban infrastructure alone [40]. The distinction between infrastructure-driven and topography- or tide-driven Type II events cannot be resolved from the present dataset and warrants targeted investigation using elevation data, tidal records, and drainage network information.
>
> **[/SUBSTITUIÇÃO]**

---

Figure 7d (Type III) shows a different structure: the density field appears broader and more spatially diffuse, with larger footprint patches and fewer sharply defined cores. This pattern is consistent with two factors acting together. First, Type III events are less frequent, so a smoothed density surface will often appear more spatially spread. Second, higher-severity events may occur across a wider set of vulnerable settings, including low-lying basins and areas where a combination of high rainfall intensity, drainage capacity exceedance, and unfavorable boundary conditions leads to deeper accumulation.

---

> **✂ [SUBSTITUIÇÃO — dissertação §4.3 | Responde: R1-C22 (falhas de drenagem e baixa elevação não suportadas pelos achados)]**
>
> *Texto original removido:*
> ~~"Second, higher-severity events may occur across a wider set of vulnerable settings, including low-lying basins and areas where drainage failure leads to deeper accumulation, producing a wider geographic distribution of high-impact cases."~~
>
> *Já substituído acima. Continua o parágrafo:*

From an impact perspective, this suggests that severe disruptions are not confined to the narrow hotspot corridor that dominates the Type II pattern and may therefore require a broader operational readiness footprint.

Overall, Figure 7 indicates that the mechanisms and susceptibility controls associated with each type differ. The fact that Type II dictates the overall hotspot structure supports a narrative of frequent, recurrent, location-specific mobility impacts. In contrast, the more diffuse Type III pattern supports a narrative of less frequent but broader-spread, high-severity disruptions. This spatial differentiation is important for the next steps of the study: rainfall thresholds and early warning criteria are likely to benefit from spatially localized calibration (for Type II dominant hotspots) and from a severity-specific analysis to test whether Type III occurrences cluster in particular basins, low-elevation zones, or infrastructure-constrained areas.

**Figure 7.** Spatial density of occurrence records in Rio de Janeiro by type. (a) All types combined. (b) Type I. (c) Type II. (d) Type III. Density surfaces are classified into five relative classes (Very Low to Very High) computed independently for each panel (see Section 3.5 note on class breaks), shown over the municipal boundary with a 10 km scale bar and north arrow. ✏️ *[R2 Major C5: legenda atualizada para deixar explícito que os intervalos de classe são calculados independentemente por painel.]*

### 3.6 Seasonal Spatial Density

Figure 8 maps the seasonal spatial concentration of occurrence records using density surfaces for all event types combined. Panels (a) to (d) correspond to summer, autumn, winter, and spring, respectively. The colored patches represent relative density classes (Very Low, Low, Medium, High, Very High), as indicated in each legend. Darker colors indicate higher density classes. As in Figure 7, density class breaks are computed independently for each seasonal panel; therefore, the maps convey relative within-season spatial concentration patterns, and cross-season magnitude comparisons should be based on the absolute counts reported in Section 3.3 rather than on color intensity. ✏️ *[R2 Major C5: nota sobre class breaks adicionada também na legenda desta figura.]*

In summer (Figure 8a), hotspots are the most extensive and intense. High- and very-high-density classes span a broad portion of the urban footprint, indicating that impacts are not confined to a single corridor but extend to multiple sectors of the city. The hotspot field includes strong concentrations in the eastern and central urban areas and extends into additional clusters across the municipality. This broad spatial footprint is consistent with a warm-season regime in which short-duration, high-intensity convective rainfall can occur across different parts of the city and rapidly overwhelm local drainage capacity, producing widespread road ponding and flooding.

In autumn (Figure 8b), the hotspot pattern remains clear but becomes more spatially focused. High-density classes are more concentrated in the eastern and central sectors, while other parts of the municipality show weaker, more fragmented patches, indicating a contraction of the impact footprint relative to summer, suggesting that the triggering conditions for occurrences are more localized or less frequently widespread across the city during this transition season.

In winter (Figure 8c), the density field contracts substantially. Most of the municipality shows very low density, and only a small number of localized patches remain, primarily along the eastern coastal and near-coastal sectors. The limited spatial coverage is consistent with the dry-season context, in which rainfall forcing is less frequent and less intense, reducing the number of occurrence triggers. The persistence of a few small hotspots in the near-coastal and lowland sectors indicates that certain locations remain susceptible even under reduced rainfall forcing, which is consistent with chronic local vulnerability associated with drainage constraints, topographic depressions, and, in some coastal areas, tidal boundary effects that can cause surface water to persist even after light rainfall [40].

In spring (Figure 8d), hotspots reexpand relative to winter and have a broader footprint than in autumn in several sectors. The pattern suggests a transition back toward a warm-season-like regime, with multiple medium- to high-density patches and clearer intensification along the eastern and central urban corridor. Compared with summer, however, the spatial footprint remains less uniformly extensive, indicating that, while impacts become more common again, the most intense and generalized hotspot configuration remains characteristic of peak summer conditions.

**Figure 8.** Seasonal spatial density of occurrence records in Rio de Janeiro (all types combined). (a) Summer. (b) Autumn. (c) Winter. (d) Spring. Density surfaces are classified into five relative classes (Very Low to Very High) computed independently per panel, shown over the municipal boundary with a 10 km scale bar and north arrow.

### 3.7 Operational Coupling of Impact Records and Rainfall Measurements

Figure 9 combines two pieces of information in a single map. First, it shows the Thiessen (Voronoi) polygons derived from the rain gauge network, where each polygon represents the area of influence of one Alerta Rio station. Second, it shows the number of flood occurrence records assigned to each polygon after spatially allocating georeferenced occurrences to the polygon in which they fall. The red triangles mark the locations of the rain gauges, and each triangle is labeled with a station identifier. The polygon boundaries partition the municipality into non-overlapping influence areas, such that any location inside a polygon is closer to its associated rain gauge than to any other gauge. The polygons are shaded using a graduated color scheme that represents the count of occurrence records assigned to each polygon. The legend provides five classes of event counts, ranging from 2 to 27 in the lightest shade to 287 to 492 in the darkest shade. Therefore, darker polygons indicate areas influenced by rain gauges with a higher number of recorded flood occurrences. The map is displayed in projected coordinates (axis tick labels in meters), and includes a north arrow and a 10 km scale.

Figure 9 shows strong spatial contrasts in the number of flood occurrences across different Thiessen polygons. Several polygons in the eastern and central part of the municipality display the darkest shades, indicating the highest occurrence counts in the dataset within those influence areas. In contrast, large polygons in the western sector show lighter shades, indicating substantially fewer assigned occurrences. This pattern has two immediate implications. First, it indicates that the occurrence database is not uniformly distributed across the city, but instead concentrates within a subset of rain gauge influence areas. This is consistent with earlier hotspot maps, which showed the highest density of occurrences in specific urban areas. Second, because the allocation is based on Thiessen polygons, Figure 9 provides an operationally useful link between the impact database and the rainfall monitoring network: it identifies which stations, by virtue of their influence areas, are most frequently associated with reported flooding impacts.

Importantly, the mapped counts reflect a combination of factors. Higher counts within a polygon may indicate greater local susceptibility to flooding impacts, higher exposure, and/or higher reporting density. In addition, Thiessen polygons vary in size depending on station spacing. Smaller polygons in the more densely instrumented eastern sector may still accumulate high event counts, suggesting that the observed concentration is not only an artifact of polygon area but also reflects genuine clustering of impacts. Conversely, larger polygons in the western sector represent broader influence areas with fewer stations. They may integrate heterogeneous terrain and land use conditions, which can dilute localized hotspots when counts are aggregated at the polygon scale. From a threshold development perspective, Figure 9 is a key intermediate product. It establishes a one-to-one correspondence between each georeferenced occurrence record and a specific rain gauge influence area, enabling subsequent analyses that compare rainfall event characteristics (e.g., intensity and duration) with the presence or absence of flooding within the same polygon. In other words, the figure operationalizes the spatial pairing required to classify rainfall events into flooding and non-flooding categories at the station-influence scale. ✏️ *[R1-C17: referências corrigidas de "Figure 8" para "Figure 9" onde aplicável para manter coerência de numeração após inserção da Figure 11.]*

**Figure 9.** Thiessen polygons for the Alerta Rio rain gauge network and number of assigned flood occurrence records per polygon. Red triangles indicate rain gauge locations.

Figure 10 quantifies the distance between each georeferenced occurrence and the nearest Alerta Rio rain gauge station. Panel (a) displays a histogram in which the horizontal axis is the distance to the nearest station in kilometers and the vertical axis is the frequency, that is, the number of occurrences falling within each distance bin. Three vertical reference lines summarize key statistics for the distribution: the red dashed line indicates the mean distance (1.98 km), the orange dashed line indicates the median distance (1.81 km), and the purple dotted line indicates the 90th percentile (3.59 km). The position of these lines relative to the bars provides a direct visual assessment of typical distances and the extent of the upper tail. Panel (b) shows the cumulative distribution of distances. The horizontal axis again represents distance in kilometers, while the vertical axis represents the cumulative percentage of occurrences located at or below a given distance. The blue curve, therefore, increases from 0 percent to 100 percent as distance increases. Two annotated thresholds are highlighted: 50 percent of occurrences are within 1.81 km (the median), and 90 percent are within 3.59 km (the 90th percentile).

Figure 10 shows that the rain gauge network generally covers the occurrence database well. The distribution is concentrated at short distances, with a median nearest-station distance of 1.81 km and a mean of 1.98 km, indicating that most occurrences are located within approximately 2 km of a station. The upper tail remains limited: 90 percent of occurrences are located within 3.59 km of the nearest gauge. This proximity supports the methodological validity of associating observed impacts with rainfall information from nearby stations, because the typical spatial separation between an occurrence and the nearest measurement point is relatively small at the municipal scale. From an operational perspective, these results strengthen confidence in the subsequent steps that depend on rainfall impact linkage, including the Thiessen-based allocation and the classification of rainfall events into flooding and non-flooding categories. When most occurrences are within a few kilometers of a station, the risk of pairing an impact with a rain gauge that is meteorologically unrepresentative is reduced, particularly for widespread stratiform rainfall. However, it is important to interpret this proximity in the context of the rainfall regime: in convective situations typical of the warm season, rainfall gradients can be sharp over kilometer scales, meaning that even short distances may still introduce a mismatch between point rainfall measurements and the true rainfall at the occurrence location. Therefore, Figure 10 demonstrates strong spatial coverage, but it does not eliminate the need to consider convective spatial variability when defining thresholds carefully.

> **📌 [INSERÇÃO — Responde: R2 Major Comment 5 (avaliação de representatividade areal)]**
>
> The proximity statistics in Figure 10 provide necessary but not sufficient evidence of rainfall representativeness. A complete assessment would require comparing Thiessen-estimated rainfall at each occurrence location against spatially continuous rainfall fields — for example, from weather radar or gauge-radar merging products — to quantify the error introduced by assuming that the nearest gauge measurement is representative of the rainfall that actually fell at the occurrence site. This type of cross-validation was not feasible in the present study due to the unavailability of operational radar data at the required temporal and spatial resolution for the 2015–2024 period. As a result, the fraction of EA/ESA misclassifications potentially attributable to spatial rainfall estimation error cannot be quantified here. This limitation is particularly relevant for convective events during summer, where rainfall cells can be spatially narrow and temporally brief, producing large gradients across polygon boundaries. For the purposes of the present spatiotemporal characterization, the Thiessen approach is considered adequate given the network density (33 gauges across the municipality) and the demonstrated proximity of occurrences to gauges. Nonetheless, the sensitivity of threshold performance to spatial pairing method should be evaluated in future work as higher-resolution rainfall products become available.
>
> **[/INSERÇÃO]**

**Figure 10.** Distance from each occurrence to the nearest Alerta Rio rain gauge station (N = 4,868). (a) Histogram of nearest station distance with mean (1.98 km), median (1.81 km), and 90th percentile (3.59 km) indicated. (b) Cumulative distribution showing that 50 percent of occurrences are within 1.81 km and 90 percent within 3.59 km.

The seasonal spatial evolution in Figure 8 is consistent with the previously reported temporal results: summer shows the largest event burden and the clearest intensification, while winter shows the weakest activity. Importantly, Figure 8 adds a spatial dimension to that seasonality by showing that summer not only increases the frequency of occurrences but also expands the geographic range of hotspots, suggesting that vulnerability, as expressed through impacts, becomes more citywide under warm-season forcing. Conversely, winter contraction indicates that, when rainfall forcing is weaker, the impact footprint becomes limited to a smaller set of persistent susceptible locations. From a rainfall impact perspective, these results support two complementary interpretations. First, warm-season impacts are likely to reflect convective rainfall episodes that can occur across different parts of the urban area, generating short-lived but frequent mobility-relevant events, consistent with the dominance of lower-severity classes and the short durations previously observed. Second, the persistence of localized winter hotspots suggests that a subset of sites remains chronically vulnerable, so that even modest rainfall can produce operational impacts.

---

> **📌 [INSERÇÃO — relatorio_secoes_44_45.docx §4.4 + chart_20 | Responde: R2-Major1 (limiares ausentes) e R2-Major3 (sem comparação EA vs ESA)]**

### 3.8 Rainfall Intensity-Duration Characteristics: EA versus ESA Events and Preliminary Thresholds

Using the EA/ESA classification established in Section 2.6, Figure 12 compares rainfall intensity-duration characteristics between events with and without recorded flooding impacts, stratified by severity class, and presents preliminary empirical rainfall thresholds. This analysis directly addresses the disconnect between the EA/ESA pairing framework described in Section 2.6 and the threshold output announced in the title and abstract.

Panel (a) shows an intensity-duration scatter plot in which each point represents one rainfall event: grey for ESA (no flooding, n = 62,831), blue for EA Type II (road ponding, n = 783), and red for EA Type III (street flooding, n = 161). The scatter reveals a systematic upward displacement of EA events relative to ESA events across all duration scales, indicating that flooding-associated rainfall is substantially more intense than non-flooding rainfall regardless of event duration. Two fitted power-law threshold curves, one per severity class, are overlaid on the scatter as visual discriminants between the two populations.

Panel (b) presents box plots of peak rainfall intensity at ten duration scales (15 min to 12 h) for the three groups. The progressive upward shift in median intensity from ESA to EA Type II to EA Type III is consistent across all tested duration windows, confirming that rainfall intensity is systematically higher when flooding occurs and increases with impact severity. The separation between ESA and EA groups is most visually pronounced at intermediate durations (1–3 h), where the interquartile ranges overlap least.

A Mann-Whitney U test confirms that the intensity difference between EA and ESA events is statistically significant (p < 0.0001) at all tested duration windows. At the 1-hour scale, the median peak intensity is 8.4 mm/h for ESA events, 19.6 mm/h for EA Type II events, and 20.4 mm/h for EA Type III events — approximately 2.3 times higher for flooding-associated events than for non-flooding events.

Empirical intensity-duration thresholds of the form I = a × D^−b were fitted separately for each severity class using a percentile-based approach calibrated to a probability of detection (POD) of 0.90:

| Severity class | Threshold equation | a | b | POD | FAR | F1 |
|---|---|---|---|---|---|---|
| Type II — road ponding (15–30 cm) | I = 7.78 × D^−0.235 | 7.78 | 0.235 | 0.90 | 0.98 | 0.05 |
| Type III — street flooding (30–50 cm) | I = 5.46 × D^−0.096 | 5.46 | 0.096 | 0.90 | 1.00 | 0.01 |

The high false alarm rates (FAR = 0.98–1.00) reflect the severe class imbalance inherent in the dataset: 99.2 percent of identified rainfall events are classified as ESA and only 0.8 percent as EA. Under these conditions, a city-wide threshold calibrated to achieve POD = 0.90 inevitably flags a large fraction of non-flooding events as potential triggers. These FAR values should not be interpreted as threshold failure; rather, they are an expected consequence of using a single city-wide threshold against a highly imbalanced background and of the fact that surface flooding depends on local factors — drainage capacity, microtopography, antecedent soil moisture — that vary substantially across the municipality. Spatially localized thresholds calibrated for individual rain gauge influence areas or sub-basins, conditioned on antecedent precipitation, are expected to substantially reduce false alarm rates by explicitly accounting for local susceptibility gradients, and represent the primary direction for subsequent work [39].

**Figure 12.** Rainfall intensity-duration characteristics of EA and ESA events by severity type. (a) Intensity-duration scatter plot with ESA events (grey, n = 62,831), EA Type II (blue, n = 783), and EA Type III (red, n = 161), with fitted power-law threshold curves for each severity class. (b) Box plots of peak rainfall intensity by duration window (15 min to 12 h) for ESA, EA Type II, and EA Type III.

⚠️ *[NOTA: Figure 12 = arquivo `artigo/chart_20_id_ea_esa_by_severity.png`. Inserir neste ponto do artigo.]*

> **[/INSERÇÃO]**

---

## 4. Conclusions

This study integrated high-temporal-resolution rainfall observations with georeferenced, operationally classified records of urban flooding occurrences to characterize when, where, and how long impacts persist in Rio de Janeiro, and to establish a reproducible rainfall-impact pairing framework to support subsequent threshold development. By combining impact records with station-based rainfall event definitions, the analysis moves beyond rainfall-only characterization and provides an impact-oriented evidence base directly aligned with municipal operations. The results demonstrate that impact occurrences are highly structured in time and space rather than randomly distributed across the city, reinforcing the value of impact-based diagnostics for operational monitoring and urban resilience planning. In this sense, the study contributes a practical pathway for converting routinely collected operational information into actionable knowledge for early warning and preparedness.

---

> **✂ [SUBSTITUIÇÃO — Responde: R1-C11 ("infrastructure prioritization" sem suporte) e R1-C22]**
>
> *Texto original:*
> ~~"The results demonstrate that impact occurrences are highly structured in time and space rather than randomly distributed across the city, reinforcing the value of impact-based diagnostics for operational monitoring, infrastructure prioritization, and urban resilience planning."~~
>
> *Texto revisado (acima — "infrastructure prioritization" substituído por "urban resilience planning" para remover afirmação sem suporte empírico direto):*
> *A frase foi incorporada com a substituição no parágrafo acima.*

---

Moderate-severity road ponding impacts dominate the occurrence database, while high-severity street flooding events represent a smaller fraction but exhibit substantially greater persistence. Duration distributions show clear severity dependence: pooled low- and moderate-severity events resolve more quickly, while high-severity events exhibit longer typical durations and a heavier upper tail. This persistence gradient indicates that severity is not only a function of depth-related operational classification. Still, it is also expressed through impact longevity, which is directly relevant to mobility disruption, service interruption, and the duration of response demand. The contrast between median and upper-tail behavior further suggests that the most disruptive cases are disproportionately driven by long-lasting events, highlighting the importance of explicitly considering persistence when designing warnings and response protocols.

Temporal patterns reveal strong seasonality, with the majority of occurrences concentrated in the warm season and a robust late-afternoon-to-evening peak during summer and autumn. The diurnal concentration aligns with periods of high exposure and commuting, implying that even moderate impacts can generate disproportionate societal disruption when they occur during peak mobility demand and when road networks operate near capacity. Spatial density mapping further shows persistent hotspots and type-dependent geographic signatures, with the dominant moderate-severity class shaping the overall hotspot structure and the high-severity class displaying broader spatial footprints.

---

> **📌 [INSERÇÃO — dissertação §5.2 | Responde: R2 Major Comment 4 (limitações do banco COR Rio precisam de tratamento mais profundo)]**
>
> Several limitations of the COR Rio operational database warrant explicit acknowledgment. First, the occurrence records depend on human-initiated reporting, which introduces the potential for subjectivity in event classification and inconsistencies in the recorded start and end times. Response times to field events may vary across shifts, sectors of the city, and operational workloads, which could affect the computed durations and partly explain the very long upper-tail durations observed in Type III events. Second, the database is likely subject to spatially heterogeneous reporting density: areas with higher population density, more visible infrastructure, and stronger operational monitoring may generate more records than equally affected but less-monitored areas. This is consistent with the observation that the western sectors of the municipality (Zona Oeste), which have lower station density in the Alerta Rio network and potentially different reporting coverage, show fewer occurrence records in the database. Third, the strong dominance of Type II (86.6 percent of records) raises the possibility that the database is skewed toward frequently reported, lower-severity sites, and that more severe but less commonly reported events may be underrepresented. The very long tails in Type III durations (90th percentile of 22.72 hours when all records are included) may partially reflect operational record-closure practices rather than hydrological reality, and targeted quality checks of these long-duration records are recommended before using them for threshold calibration. These limitations do not invalidate the spatiotemporal characterization presented here, but they do imply that threshold development based on this dataset should incorporate explicit uncertainty quantification and, where possible, cross-validation against independent data sources such as citizen reports, social media records, or radar-based flood proxies.
>
> **[/INSERÇÃO]**

---

Methodologically, the nearest-station distance analysis indicates strong network representativeness at the municipal scale, and the Thiessen-based allocation provides a practical mechanism to link each occurrence to a specific station's influence area and to classify rainfall events as with or without flooding impacts. This pairing framework is essential for threshold development because it preserves spatial reference, enables consistent labeling of rainfall events by impact presence, and supports comparisons across areas with different susceptibility. Together, these components establish an evidence base that is directly extended by the preliminary threshold analysis presented in Section 3.8, which shows that EA events are approximately 2.3 times more intense than ESA events across all duration scales and yields fitted intensity-duration curves for Type II and Type III occurrences. City-wide thresholds at POD = 0.90 achieve FAR values of 0.98–1.00, reflecting the severe class imbalance (99.2% ESA) and confirming that spatially localized, susceptibility-conditioned thresholds are the necessary next step. Future work should develop sub-basin-level and antecedent-precipitation-conditioned thresholds following the framework of Ramos Filho et al. [39], quantify threshold robustness under convective rainfall spatial variability, test sensitivity to event-separation and temporal pairing criteria, and examine whether threshold behavior differs systematically across hotspot polygons and severity classes, including potential benefits of incorporating event persistence as an explicit outcome variable.

---

## Declaration of Generative AI and AI-Assisted Technologies

During the preparation of this work, the authors used Grammarly and ChatGPT (OpenAI) to support text editing and formatting adjustments. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.

---

## References

[1] Fletcher, T. D., Andrieu, H., and Hamel, P. (2013). Understanding, management and modelling of urban hydrology and its consequences for receiving waters: A state of the art. Advances in Water Resources, 51, 261–279.

[2] Jacobson, C. R. (2011). Identification and quantification of the hydrological impacts of imperviousness in urban catchments: A review. Journal of Environmental Management, 92(6), 1438–1448.

[3] Paul, M. J., and Meyer, J. L. (2001). Streams in the urban landscape. Annual Review of Ecology and Systematics, 32, 333–365.

[4] Agonafir, C., et al. (2023). A review of recent advances in urban flood research. Water Security, 19, 100141.

[5] Fletcher, T. D., et al. (2015). SUDS, LID, BMPs, WSUD and more – the evolution and application of terminology surrounding urban drainage. Urban Water Journal, 12, 525–542.

[6] Ouma, Y., and Tateishi, R. (2014). Urban flood vulnerability and risk mapping using integrated multiparametric AHP and GIS. Water, 6, 1515–1545.

[7] Allen, M. R., and Ingram, W. J. (2002). Constraints on future changes in climate and the hydrologic cycle. Nature, 419, 224–232.

[8] Westra, S., et al. (2014). Future changes to the intensity and frequency of short duration extreme rainfall. Reviews of Geophysics, 52, 522–555.

[9] Lenderink, G., and van Meijgaard, E. (2008). Increase in hourly precipitation extremes beyond expectations from temperature changes. Nature Geoscience, 1, 511–514.

[10] IPCC. (2022). Climate Change 2022: Impacts, Adaptation and Vulnerability. Cambridge University Press.

[11] Wahl, T., et al. (2015). Increasing risk of compound flooding from storm surge and rainfall for major US cities. Nature Climate Change, 5, 1093–1097.

[12] Jongman, B., Ward, P. J., and Aerts, J. C. J. H. (2012). Global exposure to river and coastal flooding. Global Environmental Change, 22, 823–835.

[13] Winsemius, H. C., et al. (2016). Global drivers of future river flood risk. Nature Climate Change, 6, 381–385.

[14] Tellman, B., et al. (2021). Satellite imaging reveals increased proportion of population exposed to floods. Nature, 596, 80–86.

[15] Di Baldassarre, G., et al. (2013). Sociohydrology: conceptualising human-flood interactions. Hydrology and Earth System Sciences, 17, 3295–3303.

[16] Coughlan de Perez, E., et al. (2015). Forecast-based financing: an approach for catalyzing humanitarian action based on extreme weather and climate forecasts. Natural Hazards and Earth System Sciences, 15, 895–904.

[17] Rözer, V., et al. (2021). Impact-based forecasting for pluvial floods. Earth's Future, 9.

[18] Alfieri, L., et al. (2013). GloFAS – global ensemble streamflow forecasting and flood early warning. Hydrology and Earth System Sciences, 17, 1161–1175.

[19] Dereczynski, C. P., Oliveira, J. S., and Machado, C. O. (2009). Climatologia da precipitação no município do Rio de Janeiro. Revista Brasileira de Meteorologia, 24(1), 24–38.

[20] Hapuarachchi, H. A. P., Wang, Q. J., and Pagano, T. C. (2011). A review of advances in flash flood forecasting. Hydrological Processes, 25, 2771–2784.

[21] Restrepo-Posada, P. J., and Eagleson, P. S. (1982). Identification of independent rainstorms. Journal of Hydrology, 55, 303–319.

[22] Dunkerley, D. (2008). Identifying individual rain events from pluviograph records: A review with analysis of data from an Australian dryland site. Hydrological Processes, 22, 5024–5036.

[23] Medina-Cobo, M. T., et al. (2016). The identification of an appropriate Minimum Inter-event time based on multifractal characterization of rainfall data series. Hydrological Processes, 30, 3507–3517.

[24] Ignaccolo, M., and De Michele, C. (2010). A point-based Eulerian definition of rain event. Advances in Water Resources, 33(8), 933–941.

[25] Molina-Sanchis, I., et al. (2016). Rainfall timing and runoff: The influence of the criterion for rain event separation. Journal of Hydrology and Hydromechanics, 64(3), 226–236.

[26] Brasil, J. B., et al. (2022). Minimum Rainfall Inter-Event Time to Separate Rainfall Events in a Low Latitude Semi-Arid Environment. Sustainability, 14(3), 1721.

[27] Tu, A., et al. (2023). Effect of minimum inter-event time for rainfall event separation on rainfall properties and rainfall erosivity. Geoderma, 431, 116332.

[28] Candela, A., and Aronica, G. T. (2016). Rainfall thresholds derivation for warning pluvial flooding risk in urbanised areas. E3S Web of Conferences, 7, 18016.

[29] Young, A., Bhattacharya, B., and Zevenbergen, C. (2021). A rainfall threshold-based approach to early warnings in urban data-scarce regions. Journal of Flood Risk Management, 14(2), e12702.

[30] Georganta, C., Feloni, E., Nastos, P., and Baltas, E. (2022). Critical Rainfall Thresholds as a Tool for Urban Flood Identification in Attica Region, Greece. Atmosphere, 13(5), 698.

[31] Han, D., and Bray, M. (2006). Automated Thiessen polygon generation. Water Resources Research, 42, W11502.

[32] Panigrahy, N., Jain, S. K., Kumar, V., and Bhunya, P. K. (2009). Algorithms for Computerized Estimation of Thiessen Weights. Journal of Computing in Civil Engineering, 23(4), 239–247.

[33] Kim, K. H., Lee, E. H., and Hong, S. Y. (2018). Potential of Voronoi Diagram for the Conserved Remapping of Precipitation. Monthly Weather Review, 146(7).

[34] Lee, J., Kim, S., and Jun, H. (2018). A Study of the Influence of the Spatial Distribution of Rain Gauge Networks on Areal Average Rainfall Calculation. Water, 10(11), 1635.

[35] Hwang, S. H., Kim, K. B., and Han, D. (2020). Comparison of methods to estimate areal means of short duration rainfalls in small catchments, using rain gauge and radar data. Journal of Hydrology, 588, 125084.

---

> **📌 [INSERÇÃO — novas referências | Responde: inserções nas seções 1, 2.2, 3.1, 3.5, 3.6 e 4]**

[36] Georganta, C., Feloni, E., Nastos, P., and Baltas, E. (2022). Critical Rainfall Thresholds as a Tool for Urban Flood Identification in Attica Region, Greece. Atmosphere, 13(5), 698. *(já citado como [30] — verificar se deve ser unificado ou mantido como entrada separada)* ⚠️

[37] Tian, X., Luo, M., Liao, W., Xu, Z., and Wang, H. (2019). Critical rainfall thresholds for urban pluvial flooding inferred from citizen observations. Science of The Total Environment, 689, 258–268.

[38] DeSouza, S., Schwartz, D., Arriaga, J., Dooley, G., and Rajaram, H. (2024). Understanding Spatiotemporal Patterns and Drivers of Urban Flooding Using Municipal Reports. Hydrological Processes, 38.

[39] Ramos Filho, G. M., Getirana, A., Rotunno Filho, O. C., Trindade, F. T., and Tomasella, J. (2021). An improved rainfall-threshold approach for robust prediction and warning of flood and flash flood hazards. Natural Hazards, 105, 2409–2429.

[40] Pereira, R. M. S., Wanderley, H. S., and Delgado, R. C. (2022). Homogeneous regions for rainfall distribution in the city of Rio de Janeiro associated with the risk of natural disasters. Natural Hazards, 111, 333–351.

> ⚠️ *[NOTA: verificar se [36] (Georganta) é duplicata de [30]. Se sim, manter apenas [30] e usar [30] também nas inserções da introdução. Renumerar [37]→[36], [38]→[37], [39]→[38], [40]→[39].]*

> **[/INSERÇÃO]**

---

## CRediT Author Contributions

- Fabricio Polifke: Conceptualization, Methodology, Writing – original draft, Writing – review & editing, Supervision.
- Hanna Viana: Data curation, Investigation, Formal analysis, Visualization, Writing – review & editing.

## Declaration of Interests

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

---

## Sumário de todas as alterações realizadas

| # | Seção | Tipo | Revisor/Comment | Origem na dissertação |
|---|-------|------|-----------------|-----------------------|
| 1 | Introdução §1 | ✏️ Editorial | R1-C1 | — |
| 2 | Introdução §3 | ✏️ Editorial | R1-C2 | — |
| 3 | Introdução §4–5 | ✏️ Divisão de parágrafo | R1-C3 | — |
| 4 | Introdução | 📌 Inserção | R1-C5 | diss. §2.5.1–2.5.4 |
| 5 | §2.2 | 📌 Inserção | R1-C4, R1-C6 | diss. §2.1, §3.2.2 |
| 6 | §2.2 | ✏️ Expansão | R1-C5 | diss. §2.5 |
| 7 | §2.4 | ✏️ Clarificação | R1-C6 | diss. §3.2.2 |
| 8 | §3 (título) | ✏️ Editorial | R1-C16 | — |
| 9 | §3.1 | 📌 Inserção | R1-C7, R1-C21 | diss. §2.1, §4.1 |
| 10 | §3.2 | ✏️ Editorial (×2) | R1-C8, R1-C15 | — |
| 11 | §3.2 | ✏️ Editorial | R1-C9 | — |
| 12 | §3.3 | ✏️ Quantificação | R1-C18 | diss. §4.2 |
| 13 | §3.3 | ✂ Substituição | R1-C19 | diss. §4.2 + chart_19 |
| 14 | §3.5 | 📌 Inserção (nota class breaks) | R2-Major5 | — |
| 15 | §3.5 | ✂ Substituição | R1-C20 | diss. §4.3 |
| 16 | §3.5 | ✂ Substituição | R1-C21, R1-C22 | diss. §4.3 |
| 17 | §3.2 / §3.6 | 📌 Inserção (fatores costeiros) | R1-C13 | diss. §4.1 |
| 18 | §3.6 | ✏️ + 📌 | R2-Major5 | diss. §4.3 |
| 19 | §4 | ✂ Substituição | R1-C11 | — |
| 20 | §4 | 📌 Inserção (limitações) | R2-Major4 | diss. §5.2 |
| 21 | Refs | 📌 Inserção [36]–[40] | R1-C5, R2-Major4 | diss. §2.5 |
| 22 | §3.2 | ✏️ Editorial | R1-C12 | — |
| 23 | §3.8 (nova) | 📌 Inserção seção I-D | R2-Major1, R2-Major3 | relatorio §4.4 + chart_20 |
