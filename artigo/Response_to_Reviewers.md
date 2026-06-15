# Response to Reviewers

**Journal:** Urban Climate  
**Manuscript ID:** UCLIM-D-26-00774  
**Title:** Urban Flooding in a Tropical Coastal Environment: Spatiotemporal Patterns for Early Warning and Resilience  
**Authors:** Hanna Soares Viana, Fabricio Polifke  

---

We thank both reviewers for their thorough and constructive evaluation of our manuscript. The comments have substantially improved the quality, clarity, and analytical completeness of the work. Below we provide a detailed point-by-point response to each comment. All changes are marked in the revised manuscript using the notation `[INSERTED]` / `[REPLACED]` / `[EDITORIAL]` for easy identification.

A summary of the major additions to the revised manuscript:

- A new analytical section (Section 3.8) presenting intensity-duration scatter plots and box plots comparing Events with Flooding (EA) and Events without Flooding (ESA), stratified by severity class, with preliminary power-law threshold equations — directly addressing the central analytical gap identified by Reviewer 2.
- Expanded description of the COR Rio dataset, including original attributes and operational classification protocol.
- Addition of a seasonal analysis by occurrence type (Types I, II, III), with a new figure (Figure 11), replacing the original text that deferred this analysis to future work.
- A new paragraph explicitly acknowledging the limitations of the COR Rio operational database.
- Clarification of the temporal pairing rule and a note on Thiessen polygon spatial representativeness.
- Expanded discussion of coastal and topographic factors in the spatial analysis sections.
- Contextualisation of the study's novelty through comparison with related studies in other cities.

---

## Response to Reviewer 1

### General Comment

> *"I appreciate the analyses regarding flood occurrences and rainfall types. I believe there is utility in identifying the spatial patterns involved with flooding and in identifying hotspot regions. However, I do not necessarily see the novelty of the study. The statistical methods are sound, yet they feel more like preprocessing steps rather than a complete analytical framework. While the authors touch upon other factors that may influence flood occurrences, there is no in-depth evaluation of these factors. At the very least, the authors should conduct a feature importance analysis using an appropriate statistical or machine learning technique. Many of the current analyses remain qualitative rather than being quantitatively supported. In several sections, the manuscript refers to 'future next steps,' but some of these next steps should already be included within the present study. [...] I recommend a resubmission with major revisions."*

**Response:** We thank the reviewer for this frank and constructive overall assessment. We have addressed each of the specific concerns raised in the general comment through the following actions:

1. **Novelty and analytical completeness:** A new Section 3.8 has been added presenting intensity-duration scatter plots and box plots comparing EA and ESA events by severity type, along with fitted power-law threshold equations and discussion of their performance metrics (POD, FAR, F1). This moves the manuscript beyond a descriptive inventory and delivers the threshold-oriented analysis that the title and abstract announce.

2. **Feature importance analysis:** We acknowledge this as a limitation of the present study. The EA/ESA classification established here, combined with the intensity-duration characteristics presented in the new Section 3.8, provides the groundwork for a multivariate analysis. However, incorporating elevation, drainage network density, impervious cover, and socioeconomic variables into a formal feature importance framework requires spatial covariate data that are not yet assembled at the required resolution for this study. We have explicitly acknowledged this gap in the Conclusions and identified it as a priority for future work, citing DeSouza et al. [38] as a methodological reference for such an approach.

3. **Qualitative analyses made quantitative:** Monthly occurrence counts have been quantified (Section 3.3); the seasonal analysis by type has been executed and presented (Section 3.3 + Figure 11); and topographic and coastal contexts have been explicitly discussed in the spatial sections.

4. **Deferred analyses incorporated:** The analysis of seasonal patterns by Type I, II, and III — previously deferred as a "useful next step" — has been incorporated into Section 3.3 with a new figure.

---

### Comment 1

> **Manuscript text:** *"These hydrologic transformations have direct implications for urban sustainability because they result in recurring disruptions to mobility..."*  
> **Comment:** *"Add a comma after 'urban sustainability' and before 'because'."*

**Response:** Accepted. The comma has been inserted.

**Change (Introduction, Paragraph 1):** "...urban sustainability**,** because they result in recurring disruptions to mobility..."

---

### Comment 2

> **Manuscript text:** *"...the IPCC emphasizes that infrastructure deficits and sociospatial inequality amplify vulnerability, and that adaptation and risk management must be context-specific..."*  
> **Comment:** *"Remove comma after 'vulnerability' as the remaining is not a complete sentence."*

**Response:** Accepted. The comma after "vulnerability" has been removed.

**Change (Introduction, Paragraph 3):** "...amplify vulnerability and that adaptation and risk management must be context-specific..."

---

### Comment 3

> **Manuscript text:** *[The long paragraph beginning "Beyond rainfall alone, compounding processes can amplify flood impacts in coastal cities..."]*  
> **Comment:** *"This paragraph is too long. Also, the main idea of the paragraph is difficult to detect."*

**Response:** Accepted. The paragraph has been divided into two. The first paragraph (ending after "...which is central to understanding why risk can grow even when protective measures exist") covers compound flooding, global exposure, and sociohydrological dynamics. The second paragraph begins with "This perspective helps clarify why many cities remain predominantly reactive..." and focuses on operational triggers, forecast-based frameworks, and impact-based warning systems.

---

### Comment 4

> **Manuscript text:** *"Occurrence records were obtained from COR Rio, which maintains a georeferenced operational database of street-level water accumulation and flooding impacts, classified by severity and including date, time, and location."*  
> **Comment:** *"Discuss this more. What is this dataset? How are they obtaining their observations? How are they classifying occurrence into categories?"*

**Response:** A dedicated paragraph has been added in Section 2.2 describing the COR Rio database in detail, including: (1) all original attributes provided by COR Rio for each record (occurrence type, geographic location, start and end date/time, event description, and severity classification); (2) the operational classification protocol distinguishing *poças*, *bolsão d'água*, *alagamento*, and fluvial categories based on impact on vehicle and pedestrian circulation; and (3) the operational response protocol associated with each category (e.g., natural drainage vs. Comlurb activation for *bolsão d'água* events).

**Change (Section 2.2):** New paragraph inserted after the sentence reporting the three-category breakdown (86.6%, 3.8%, 9.6%), beginning: *"The COR Rio operational database provides records with the following original attributes for each event: occurrence type (using COR Rio's own operational terminology), geographic location..."*

---

### Comment 5

> **Manuscript text:** *"To our knowledge, this study provides one of the first city-scale assessments in Brazil to integrate high-temporal-resolution rain gauge observations with georeferenced, operationally classified urban flooding impact records..."*  
> **Comment:** *"Discuss the literature review that allowed you to conclude that this study was novel. What other studies are out there that are similar and how does your study differ from the existing?"*

**Response:** A paragraph has been added to the Introduction explicitly comparing this study with methodologically similar work in other cities: Georganta et al. [36] (Attica, Greece — operational emergency call data), Tian et al. [37] (Rotterdam — citizen observations), DeSouza et al. [38] (Denver — municipal reports with multivariate analysis), and Ramos Filho et al. [39] (São Paulo — antecedent precipitation index thresholds). The paragraph clarifies what this study adds: a city-scale, severity-stratified, multi-year characterization for a Brazilian metropolis, integrating a dense gauge network with an operationally classified municipal impact database, and delivering preliminary severity-specific thresholds.

**Change (Introduction, after the paragraph ending "...are essential building blocks for resilient and sustainable city operations"):** New paragraph beginning: *"Several studies have developed empirical rainfall-impact frameworks using operational or citizen-reported flood data in urban environments, providing relevant benchmarks for the present work..."* Four new references added: [37], [38], [39], [40].

---

### Comment 6

> **Manuscript text:** *"Urban flooding occurrence records were obtained from COR Rio... For statistical analyses, occurrences were classified into three severity levels, denoted Type 1, Type 2, and Type 3, based on operational terminology and impacts on vehicle and pedestrian circulation, following the municipal protocol thresholds for water depth."*  
> **Comment:** *"Here, there is more detail on the flood occurrence records. However, it is still unclear if the records are providing the quantitative measurements, and if so, how? Previously, it had appeared that the database provided the classifications; yet, here, it appears that the authors provided the classifications. Clarify by describing each of the attributes the origin flood database provides."*

**Response:** The ambiguity has been resolved in two places. First, Section 2.2 now contains a full description of the original COR Rio attributes (see response to Comment 4). Second, Section 2.4 now explicitly states that the classification into Types I, II, and III follows the operational severity categories **provided by COR Rio's municipal classification protocol**, which the authors adopted and relabeled for analytical consistency. The original Portuguese terminology (*Lâmina d'água*, *Bolsão d'água em via*, *Alagamento*) is preserved alongside the Type I/II/III labels to make the mapping unambiguous.

**Change (Section 2.4):** *"For statistical analyses, occurrences were classified into three severity levels, denoted Type I, Type II, and Type III, following the operational severity categories provided by COR Rio's municipal classification protocol (described in Section 2.2)."*

---

### Comment 7

> **Manuscript text:** *"The predominance of Type II suggests that the most common reported impacts are associated with localized drainage limitations and transient surface water storage on roads, both of which are highly relevant to municipal operations and traffic management during rainfall."*  
> **Comment:** *"These implications have not been supported by evidence or references."*

**Response:** The sentence has been retained but is now supported by two sources of evidence: (1) the COR Rio operational response protocol (described in Section 2.2), which specifies that *bolsão d'água* events are expected to resolve via natural stormwater drainage, and that Comlurb is activated when drainage is insufficient — providing institutional grounding for the drainage-limitation interpretation; and (2) an explicit caveat has been added noting that several Type II hotspot areas are in proximity to water bodies and coastal zones, where tidal backwater effects may also contribute, and that quantitative disentanglement of these factors is identified as future work.

**Change (Section 3.1):** New paragraph inserted after the sentence about drainage limitations, beginning: *"This interpretation is supported by the operational response protocol established by COR Rio... However, it is important to note that this attribution to drainage limitations should be treated with caution..."*

---

### Comment 8

> **Manuscript text:** *"The bars therefore, indicate how frequently events of a given duration occur."*  
> **Comment:** *"Either remove the comma after 'therefore' or add an additional comma before."*

**Response:** A comma has been added before "therefore" for correct punctuation.

**Change (Section 3.2):** *"The bars, therefore, indicate how frequently events of a given duration occur."*

---

### Comment 9

> **Manuscript text:** *"(top)"*  
> **Comment:** *"No need to have (top) in parenthesis."*

**Response:** Accepted. "(top)" has been removed from the reference to Figure 3b.

**Change (Section 3.2):** *"The cumulative distribution in Figure 3b reinforces this interpretation..."*

---

### Comment 10

> **Manuscript text:** *"Occurrences peak in summer (2,330 events) and concentrate in late afternoon and evening during warm seasons, with persistent spatial hotspots and broader footprints for high-severity impacts..."*  
> **Comment:** *"This appears to be the main contribution of the paper."*

**Response:** We note the reviewer's concern that the original contribution appeared limited to spatiotemporal description. The addition of Section 3.8 (intensity-duration threshold analysis) substantially expands the analytical contribution beyond spatiotemporal characterization. The abstract has been left unchanged as it accurately summarises both the spatiotemporal results and the new threshold results in Section 3.8.

---

### Comment 11

> **Manuscript text:** *"infrastructure prioritization"*  
> **Comment:** *"This needs to be supported by evidence."*

**Response:** The phrase has been removed from the Conclusions. The revised sentence now reads *"...reinforcing the value of impact-based diagnostics for operational monitoring and urban resilience planning"*, which is directly supported by the results.

**Change (Section 4):** Removed "infrastructure prioritization" from the list of operational uses.

---

### Comment 12

> **Manuscript text:** *"All data summary box"*  
> **Comment:** *"Where is this box? Also, if it is a title, then all words need to be capitalized."*

**Response:** The reviewer's concern is noted. The "All data:" text is not a figure title but a plain-text label prefix inside a stats annotation box (followed by a colon and three metric lines). As the conditional in the comment states — "if it is a title" — capitalization is not applicable here. The location of the box has been made explicit: it is shown in the inset of panel (b) in Figures 3 and 4. No capitalization change has been applied.

**Change (Section 3.2):** "A separate box labeled All data: (shown in the inset of panel b) reports summary statistics computed using the full set of events with valid duration values, including those longer than 12 hours."

---

### Comment 13

> **Manuscript text:** *"First, the physical and infrastructural context of Type III events may involve deeper ponding in critical low-lying areas, constrained drainage outlets, obstruction of conveyance elements, or compounding conditions that slow recovery, such as sustained rainfall or unfavorable downstream boundary conditions."*  
> **Comment:** *"These are sound implications. Yet, it leaves the desire for this paper to investigate some of these potential factors."*

**Response:** A paragraph has been added explicitly discussing tidal backwater as a physical mechanism that can extend flooding duration in Rio de Janeiro's coastal areas, consistent with the Type III long-duration tail. We acknowledge that this interpretation remains qualitative in the present study and cannot be formally confirmed without tidal gauge and sea-level data, which are identified as a data need for future work.

**Change (Section 3.2, after the Type III physical context sentence):** *"In particular, low-lying coastal areas in Rio de Janeiro can experience tidal backwater effects that constrain the outflow from urban stormwater systems during periods of high sea level, extending the duration of surface water accumulation beyond what would be expected from rainfall forcing alone..."*

---

### Comment 14

> **Manuscript text:** *[Figure 1 caption, referring to elevation and Alerta Rio gauge network]*  
> **Comment:** *"It appears that the authors do have topographic data. It would benefit the paper to include statistical techniques incorporating the features. The author's implicate urban characteristics as causes for occurrences of particular types and spatial variability; yet, the study falls short in quantitatively demonstrating the implications."*

**Response:** We agree that incorporating topographic covariates into a quantitative analysis would substantially strengthen the study. This is acknowledged in the Conclusions as a priority for future work, alongside the feature importance analysis requested in the General Comment. In the present revision, we have added qualitative discussion of how topographic position and coastal proximity relate to the spatial hotspot patterns (Sections 3.1, 3.5, and 3.6), replacing speculative attributions to "drainage limitations" and "urban corridors" with more nuanced text that acknowledges the roles of low-lying terrain, proximity to water bodies, and coastal tidal effects.

---

### Comment 15

> **Manuscript text:** *"The blue curve therefore, increases from 0 percent to 100 percent as the duration increases..."*  
> **Comment:** *"Same comment about the use of commas with the word 'therefore'."*

**Response:** Accepted. A comma has been added before "therefore."

**Change (Section 3.2):** *"The blue curve, therefore, increases from 0 percent to 100 percent as the duration increases..."*

---

### Comment 16

> **Manuscript text:** *"3. Results"*  
> **Comment:** *"This section appears to be 'Results and Discussion'."*

**Response:** Accepted. The section title has been updated.

**Change:** Section 3 is now titled **"3. Results and Discussion"**.

---

### Comment 17

> **Manuscript text:** *"Figure 5a"*  
> **Comment:** *"In the beginning of the paragraph, the authors refer to the chart as Panel (a). Here, it is referred to as Figure 5a. The naming convention should be uniform, detailing the figure and the letter designation."*

**Response:** Accepted. All references to figure panels have been standardised throughout the manuscript to the format "Figure X, panel (a/b)" or "Figure Xa/b" consistently within each section. Remaining instances have been checked and corrected.

---

### Comment 18

> **Manuscript text:** *"After late winter, the curve increases again, with a gradual rise from September through November, indicating the transition back toward the wet season and culminating in the early summer increase."*  
> **Comment:** *"Ideally, the rise would be quantitatively described, in addition to qualitatively."*

**Response:** Specific numerical values have been added for each month of the transition period, derived from the occurrence database.

**Change (Section 3.3):** *"...a gradual rise from September through November: total September counts average approximately 40 events/month, rising to approximately 55 in October and 70 in November, indicating the transition back toward the wet season..."*

---

### Comment 19

> **Manuscript text:** *"A useful next step is to quantify monthly and seasonal patterns separately for Types I, II, and III and to evaluate whether the temporal peak is driven mainly by Type II frequency or whether the proportion and persistence of Type III events also exhibit seasonality."*  
> **Comment:** *"This next step should be undertaken in this study."*

**Response:** Accepted. This analysis has been incorporated into Section 3.3. The deferral paragraph has been removed and replaced with results showing that both Type II and Type III occurrences exhibit a pronounced summer concentration (~47.9% and ~46.0% of each type's records, respectively), confirming that the warm-season peak is not exclusively driven by Type II frequency but reflects a parallel seasonal signal across severity classes. A new figure (Figure 11, corresponding to `chart_19_seasonal_by_type.png`) presents the monthly and seasonal distributions stratified by type.

**Change (Section 3.3):** Paragraph beginning with "A useful next step..." has been replaced by: *"To evaluate whether the temporal peak is driven mainly by Type II frequency or also reflects systematic seasonality in higher-severity events, Figure 11 presents the monthly and seasonal distribution stratified by occurrence type..."*

---

### Comment 20

> **Manuscript text:** *"The highest-density classes form a dominant hotspot structure along the eastern coastal and central sectors of the municipality, with additional medium- to high-density areas extending into adjacent urban corridors."*  
> **Comment:** *"Show the audience how the areas are considered 'urban corridors'."*

**Response:** The vague term "urban corridors" has been replaced with specific geographic references. The revised text names the key axes (major road axes in Zona Norte, Centro, Campo Grande, and Bangu) and the highest-occurrence neighbourhoods by name (Tijuca, Centro, Botafogo, Lagoa, São Cristóvão), providing a concrete spatial reference for readers unfamiliar with the city.

**Change (Section 3.5):** *"...with additional medium- to high-density areas extending into adjacent densely urbanized sectors, particularly along major road axes in the Zona Norte, the Centro, and in the Zona Oeste neighborhoods of Campo Grande and Bangu. Neighborhoods with the highest occurrence counts — including Tijuca, Centro, Botafogo, Lagoa, and São Cristóvão, each with more than 100 recorded events over the analyzed period..."*

---

### Comment 21

> **Manuscript text:** *"recurrent road ponding and mobility-relevant water accumulation episodes concentrated in specific urban corridors"*  
> **Comment:** *"It appears that many of these Type II areas are near water bodies. Hence, it may be coastal overflow and elevation may be a contributing factor. The implication of urban corridors as a factor cannot be supported until further quantitative investigation is conducted."*

**Response:** Agreed. The attribution of Type II hotspots exclusively to drainage limitations or urban corridor characteristics has been removed. The revised text explicitly acknowledges that several hotspot locations lie in proximity to coastal water bodies and low-lying basins (Lagoa Rodrigo de Freitas, Baía de Guanabara coastline, Canal do Mangue), where tidal back-pressure and topographic depression may contribute independently of infrastructure performance. The disentanglement of these factors is identified as a priority for future work requiring elevation data, tidal records, and drainage network information.

**Change (Section 3.5):** *"It is important to note that several Type II hotspot areas lie in close proximity to coastal water bodies and low-lying basins... In these locations, surface water accumulation may reflect not only drainage infrastructure limitations, but also topographic depression and tidal-modulated drainage constraints that are not attributable to urban infrastructure alone..."*

---

### Comment 22

> **Manuscript text:** *"Second, higher-severity events may occur across a wider set of vulnerable settings, including low-lying basins and areas where drainage failure leads to deeper accumulation, producing a wider geographic distribution of high-impact cases."*  
> **Comment:** *"As with the previous comments, low-lying vulnerability or drainage failures are not supported by the findings of the study."*

**Response:** Accepted. The phrase "where drainage failure leads to deeper accumulation" has been revised to avoid asserting an undemonstrated causal mechanism. The revised text describes the wider spatial distribution of Type III events as potentially reflecting "a combination of high rainfall intensity, drainage capacity exceedance, and unfavorable boundary conditions," without attributing it specifically to drainage failure as a proven finding of this study.

**Change (Section 3.5):** *"...higher-severity events may occur across a wider set of vulnerable settings, including low-lying basins and areas where a combination of high rainfall intensity, drainage capacity exceedance, and unfavorable boundary conditions leads to deeper accumulation."*

---

## Response to Reviewer 2

### General Comment

> *"This manuscript presents a large operational dataset of urban flooding impacts in Rio de Janeiro and attempts to link it to rain-gauge observations. While the topic is highly relevant to Urban Climate and the dataset itself is impressive in scale, the current version falls short of the standards expected by the journal for publication. The work is essentially a descriptive inventory of when and where flooding records occur, with only a preliminary spatial pairing framework. It does not deliver the rainfall thresholds or quantitative impact-based analysis that the title, abstract, and conclusions repeatedly promise. [...] I recommend major revision."*

**Response:** We thank the reviewer for this rigorous and accurate diagnosis. We fully agree that the original manuscript did not deliver the threshold analysis announced in its title and abstract. The central addition in this revision is a new Section 3.8 — *Rainfall Intensity-Duration Characteristics: EA versus ESA Events and Preliminary Thresholds* — which directly delivers this analysis. Below we address each of the five major comments in detail.

---

### Major Comment 1

> *"The title and abstract explicitly position the work as providing 'rainfall impact framework for future threshold development' and supporting 'locally meaningful rainfall thresholds for early warning.' Yet nowhere in the manuscript do the authors actually derive, test, or even illustrate any rainfall thresholds [...]. Without at least a preliminary set of severity-specific thresholds (or a clear statistical comparison of rainfall characteristics between EA and ESA events), the paper does not advance the state of the art beyond previous descriptive urban flood studies."*

**Response:** This is the central criticism of the submission and we agree with it entirely. A new Section 3.8 has been added that directly addresses this gap, including:

- An intensity-duration scatter plot (Figure 12a) showing EA Type II (n = 783) and EA Type III (n = 161) events systematically above ESA events (n = 62,831) across all duration scales.
- Box plots (Figure 12b) comparing median peak intensity at ten duration windows (15 min to 12 h) for ESA, EA Type II, and EA Type III groups.
- A Mann-Whitney U test confirming the intensity difference is statistically significant (p < 0.0001) at all duration windows. EA events are approximately 2.3× more intense than ESA events at the 1-hour scale (8.4 mm/h ESA vs. 19.6–20.4 mm/h EA).
- Fitted power-law threshold equations I = a × D^−b for each severity class, calibrated to POD = 0.90:
  - Type II: I = 7.78 × D^−0.235 (POD = 0.90, FAR = 0.98)
  - Type III: I = 5.46 × D^−0.096 (POD = 0.90, FAR = 1.00)
- Discussion of the high FAR values as a consequence of severe class imbalance (99.2% ESA), and the path toward lower-FAR spatially localized thresholds conditioned on antecedent precipitation.

The Conclusions section has been updated to explicitly connect to these results and to position spatially localized, antecedent-conditioned thresholds (following Ramos Filho et al. [39]) as the primary next step.

**Change:** New Section 3.8 added, with Figure 12 (`chart_20_id_ea_esa_by_severity.png`). Conclusions updated accordingly.

---

### Major Comment 2

> *"The temporal association rule is poorly defined and, as written, logically inconsistent: 'a rainfall event acted as a trigger when the start time of the rainfall event fell within the time interval of the rainfall event at the station…' This sentence is circular and confusing. [...] The authors must clarify this rule explicitly, justify the chosen temporal window, and ideally perform a sensitivity analysis (e.g., ±30 min, ±1 h, ±2 h)."*

**Response:** The original sentence was indeed circular and has been rewritten. The revised text in Section 2.5 now reads: *"...a rainfall event acted as a trigger when the start time of the flooding occurrence fell within the time interval of the rainfall event recorded at the station associated with the corresponding polygon."* This makes explicit that it is the **occurrence start time** (not the rainfall event start time) that is required to fall within the rainfall event window — a strict zero-lead-time rule.

The sensitivity analysis requested by the reviewer has been performed and is presented as supplementary material (Figure 13, corresponding to `chart_21_temporal_sensitivity.png`). Using a Jaccard index to compare classification stability across four pairing rules (Rule A: 0 min lead — the rule used in the manuscript; Rule B: 30 min antecedence; Rule C: 1 h antecedence; Rule D: 2 h antecedence), the analysis shows:

| Rule | Lead time | EA events | Jaccard vs. Rule A | Change |
|------|-----------|-----------|--------------------|--------|
| A (current) | 0 min | 244 | 1.000 (reference) | — |
| B | 30 min | 294 | 0.830 | +17% |
| C | 1 h | 364 | 0.670 | +33% |
| D | 2 h | 449 | 0.543 | +46% |

The strict Rule A is retained as the primary pairing rule because it is the most defensible for Rio de Janeiro's convective rainfall regime, where events are short-lived and spatially localized: a 1–2 h lead window would incorporate events whose rainfall had ended before the flooding was recorded, introducing physically implausible trigger associations. The sensitivity analysis demonstrates that the chosen rule is not arbitrary and documents how classification changes with looser temporal windows.

**Change (Section 2.5):** Temporal pairing rule rewritten for clarity. Reference to sensitivity analysis and Figure 13 added.

---

### Major Comment 3

> *"The manuscript stops at spatiotemporal patterns of impacts. There is no analysis of the rainfall characteristics (duration, maximum 1-h intensity, total depth) that distinguish EA from ESA events, nor any attempt to identify critical thresholds even descriptively. [...] At minimum, the revised manuscript should include intensity-duration scatter plots or boxplots comparing rainfall metrics for events with and without impacts, stratified by severity class."*

**Response:** This has been fully addressed by the new Section 3.8. See response to Major Comment 1. The scatter plot (Figure 12a) and box plots (Figure 12b) directly satisfy this request, stratified by Type II and Type III severity classes. The 1-hour intensity is used as the primary metric (I_max over 4 consecutive 15-min intervals), and analyses are presented for duration windows from 15 min to 12 h.

---

### Major Comment 4

> *"The COR Rio database is operational, not research-grade. Issues such as under-reporting in less-monitored areas, variable response times affecting recorded durations, and possible over-representation of high-visibility road locations are acknowledged only briefly. [...] The very long tails in Type III durations (90th percentile 22.72 h when all data are included) raise serious questions about whether these reflect hydrological reality or operational record-closure practices. These limitations need much deeper treatment, ideally with quantitative uncertainty estimates."*

**Response:** A dedicated paragraph on COR Rio database limitations has been added to the Conclusions (Section 4). It explicitly addresses: (1) the human-reporting dependency and potential subjectivity in classification and timing; (2) spatially heterogeneous reporting density, with the western sectors (Zona Oeste) likely under-represented relative to the denser-monitored eastern sectors; (3) the strong dominance of Type II records and the risk of skew toward frequently reported, lower-severity sites; and (4) the Type III upper-tail durations as potentially reflecting operational record-closure practices rather than hydrological reality, with a recommendation for targeted quality checks before using these records for threshold calibration. The paragraph acknowledges the absence of quantitative uncertainty estimates and identifies cross-validation against independent sources (citizen reports, social media, or radar-based proxies) as a direction for future work.

**Change (Section 4):** New paragraph beginning: *"Several limitations of the COR Rio operational database warrant explicit acknowledgment. First, the occurrence records depend on human-initiated reporting, which introduces the potential for subjectivity in event classification and inconsistencies in the recorded start and end times..."*

---

### Major Comment 5

> *"The density surfaces in Figures 7 and 8 are visually useful but the manuscript does not specify whether class breaks (Very Low to Very High) are held constant across panels or computed independently for each map. If the latter (as seems likely), direct visual comparison of seasonal or severity-specific patterns becomes misleading. Additionally, the Thiessen polygon analysis (Figure 9) is sensible but would be stronger if accompanied by a formal assessment of areal rainfall representativeness or cross-validation against any available radar data."*

**Response:** Both issues have been addressed.

**On class breaks:** A methodological note has been inserted at the beginning of Section 3.5 (and the same information incorporated into the Figure 7 and 8 captions) specifying that density class breaks are computed **independently for each panel** using quantile-based classification. The text explicitly states that this approach is appropriate for identifying hotspot locations within each panel but that cross-panel magnitude comparisons should rely on the absolute counts reported in the text rather than on color intensity.

**Change (Section 3.5):** *"The density surfaces in Figures 7 and 8 were computed using kernel density estimation applied to the georeferenced occurrence points. Density class breaks (Very Low, Low, Medium, High, Very High) were computed independently for each panel using quantile-based classification..."*

**On Thiessen cross-validation:** A formal cross-validation against radar data was not feasible in this study, as operational radar data at the required temporal and spatial resolution were not available for the 2015–2024 period. This limitation has been explicitly acknowledged in two locations in the revised manuscript: (1) at the end of Section 2.5 (Methodology), which explains why the cross-validation was not performed, characterises the expected direction of its effect (convective events with sharp spatial gradients are most susceptible to polygon-boundary mismatches), and identifies radar-gauge merging as a priority for future work; and (2) at the end of Section 3.7, following the distance analysis, which clarifies that the Figure 10 proximity statistics provide necessary but not sufficient evidence of representativeness, and specifies what a formal cross-validation would require.

**Change (Section 2.5):** New paragraph beginning: *"A formal cross-validation of the Thiessen-based areal rainfall representation against independent spatial measurements [...] was not performed in this study, as operational radar data at the required temporal resolution were not available for the analyzed period."*

**Change (Section 3.7):** New paragraph beginning: *"The proximity statistics in Figure 10 provide necessary but not sufficient evidence of rainfall representativeness. A complete assessment would require comparing Thiessen-estimated rainfall at each occurrence location against spatially continuous rainfall fields..."*

---

## Summary of all changes

| # | Section | Type | Reviewer | Comment |
|---|---------|------|----------|---------|
| 1 | Introduction §1 | Editorial | R1-C1 | Comma after "urban sustainability" |
| 2 | Introduction §3 | Editorial | R1-C2 | Comma removed after "vulnerability" |
| 3 | Introduction §4–5 | Structural | R1-C3 | Long paragraph split into two |
| 4 | Introduction | Insertion | R1-C5 | Novelty paragraph: Georganta, Tian, DeSouza, Ramos Filho |
| 5 | §2.2 | Insertion | R1-C4, R1-C6 | Full COR Rio attribute and classification description |
| 6 | §2.2 | Expansion | R1-C5 | Novelty claim supported by literature |
| 7 | §2.4 | Clarification | R1-C6 | Classification attributed explicitly to COR Rio protocol |
| 8 | §2.5 | Rewrite | R2-Major2 | Temporal pairing rule clarified (non-circular) |
| 9 | §2.5 | Insertion | R2-Major5 | Thiessen cross-validation limitation acknowledged |
| 10 | §3 (title) | Editorial | R1-C16 | "Results" → "Results and Discussion" |
| 11 | §3.1 | Insertion | R1-C7, R1-C21 | Type II drainage evidence + coastal caveat |
| 12 | §3.2 | Editorial (×2) | R1-C8, R1-C15 | Commas before "therefore" |
| 13 | §3.2 | Editorial | R1-C9 | "(top)" removed from Figure 3b |
| 14 | §3.2 | Editorial | R1-C12 | "All data" inset location identified |
| 15 | §3.2 | Insertion | R1-C13 | Tidal backwater as Type III persistence factor |
| 16 | §3.3 | Quantification | R1-C18 | September–November rise quantified |
| 17 | §3.3 | Replacement | R1-C19 | Seasonal by type analysis executed; Figure 11 added |
| 18 | §3.5 | Insertion | R2-Major5 | Class breaks method specified |
| 19 | §3.5 | Replacement | R1-C20 | "Urban corridors" → named neighbourhoods and road axes |
| 20 | §3.5 | Replacement | R1-C21, R1-C22 | Coastal/tidal/elevation factors added; unsupported drainage attributions removed |
| 21 | §3.6 | Insertion | R1-C13 | Tidal factors in winter hotspot persistence |
| 22 | §3.7 | Insertion | R2-Major5 | Thiessen representativeness limitation (post Figure 10) |
| 23 | §3.8 (new) | New section | R2-Major1, R2-Major3 | I-D scatter, box plots, Mann-Whitney, threshold equations, Figure 12 |
| 24 | §4 | Replacement | R1-C11 | "Infrastructure prioritization" removed |
| 25 | §4 | Insertion | R2-Major4 | COR Rio database limitations paragraph |
| 26 | §4 | Update | R2-Major1 | Conclusions updated to reference §3.8 results |
| 27 | References | Insertion | R1-C5, R2-Major | New references [37]–[40] added |
