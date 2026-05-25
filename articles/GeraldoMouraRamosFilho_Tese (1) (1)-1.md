Federal University of Paraíba - UFPB

Technology Center

POSTGRADUATE PROGRAM IN CIVIL AND ENVIRONMENTAL

ENGINEERING

- PhD THESIS –
# PERFORMANCE OF RAINFALL THRESHOLD FOR FLOOD

# IDENTIFICATION FROM GROUND- AND SATELLITE-BASED

# (SUB)DAILY DATA

By

# Geraldo Moura Ramos Filho

# PhD thesis defended at Federal University of Paraíba for attaining the degree

# in Doctor of Civil and Environmental Engineering with emphasis on Water

# Resources

João Pessoa – Paraíba October 2021

Federal University of Paraíba - UFPB

Technology Center

POSTGRADUATE PROGRAM IN CIVIL AND ENVIRONMENTAL

ENGINEERING

- PhD THESIS –
# PERFORMANCE OF RAINFALL THRESHOLD FOR FLOOD

# IDENTIFICATION FROM GROUND- AND SATELLITE-BASED

# (SUB)DAILY DATA

PhD Thesis submitted to the Postgraduate Program in Civil and

Environmental Engineering at the Federal University of Paraíba, as part of

requisites for attaining the title of Doctor.

# Geraldo Moura Ramos Filho

# Advisor: Prof. Dr. Cristiano das Neves Almeida

# Co-advisor: Prof. Dr. Victor Hugo Rabelo Coelho

João Pessoa – Paraíba October 2021

# 2

```
Catalogação na publicação
Seção de Catalogação e Classificação
R175p Ramos Filho, Geraldo Moura.
Performance of rainfall threshold for flood
identification from ground- and satellite-based
(sub)daily data / Geraldo Moura Ramos Filho. - João
Pessoa, 2021.
99 f. : il.
Orientação: Cristiano das Neves Almeida.
Coorientação: Victor Hugo Rabelo Coelho.
Tese (Doutorado) - UFPB/CT.
1. Desastres naturais. 2. Inundação. 3. Enxurrada. 4.
Precipitações extremas. 5. Limiares de precipitação. I.
Almeida, Cristiano das Neves. II. Coelho, Victor Hugo
Rabelo. III. Título.
UFPB/BC CDU 504.4(043)
Elaborado por ANNA REGINA DA SILVA RIBEIRO - CRB-15/024
```

To my dear mother, Elizabete, and my dear father, Geraldo, who always supported me

and believed in my potential. And to those who are part of my life.

I dedicate!

# 4

ACKNOWLEDGEMENTS

I reserve this space to thank everyone who helped directly or indirectly in this new

personal and professional achievement. It would not have been possible without the support

of many people who are part of my life. Firstly, I thank God for all the opportunities given

and experiences that certainly contributed to my personal and professional growth.

My fiancée, Mariângela Cardoso Bezerra, for all the love, understanding, and support

received, even in moments of my absence, which were necessary to seek the knowledge

necessary to complete this work.

My parents, Geraldo Moura Ramos and Elizabete de Amorim Correia, for the

affection and devotion, for the moral principles that made me what I am today, and above

all, for the certainty that I have by my side people who truly love me. To my brothers, Larissa

Correia Moura Ramos and Thiago Correia Moura Ramos, for all the affection,

encouragement, attention, and moments of distraction.

My advisor, Professor Dr. Cristiano das Neves Almeida, and co-advisor, Professor

Dr. Victor Hugo Rabelo Coelho, for the guidance, teaching, support, and encouragement

received during these years, which were so fundamental to achieve this dream, also

fundamental for my professional growth.

Members of the examining board, Prof. Dr Adriano Rolim da Paz, Prof. Dr Gerald

Souza da Silva, Prof. Dr Javier Tomasella and Prof. Dr Yunqing Xuan for their availability

in accepting to attend at the PhD board, whose thoughtful suggestions contributed

undoubtedly to improve the quality of the PhD thesis.

My research colleagues, Emerson da Silva Freitas, André Nóbrega Gadêlha, Marcela

Antunes Meira, Filipe Carvalho Lemos and Abner Silva Lins for their friendship and

collaborations in the PhD activities and paper publications.

Finally, I acknowledge CAPES foundation for the scholarship (Finance Code 001

and grant number: 88882.440978/2019-01) that allows the accomplishment of this thesis.

# 5

ABSTRACT

Great effort has been made over the last few decades to develop and improve methods for

monitoring hydrological disasters. Among them, rainfall thresholds, defined as the minimum

rainfall conditions that are likely to trigger hydrological disasters, are the most popular tool

used to study the relationship between rainfall and hydrological disaster occurrences,

highlighted due to their straightforward approach for application in different regions. Some

factors make it difficult to determine rainfall thresholds, such as the quality of rainfall and

disasters data, and the large distances between the rain gauges and the disaster. To overcome

these limitations, the use of satellite-based precipitation products is a way out to characterize

rainfall events that trigger disasters. Accordingly, this thesis aims to present an improved

method of using a threshold of peak rainfall intensity for robust floods evaluation and

warnings by applying probabilistic-based methods and taking into consideration the

antecedent conditions. Moreover, this study assesses the quality of satellite-based

precipitation products to create rainfall thresholds for floods monitoring. São Paulo State

was selected as the study area because is a typical hot spot frequented by landslides and

floods. In addition, São Paulo is the richest state in Brazil, with the largest number of floods,

flash floods, and sub-daily rainfall data made available by public agencies. Results show that

the use of tolerance levels and the delineating of an intermediate threshold by incorporating

an exponential curve that relates rainfall intensity and Antecedent Precipitation Index (API)

helped reduce significantly many uncertainties in the hydrological disasters monitoring.

Moreover, the use of satellite-based products showed to be less accurate compared to rain

gauges to characterize extreme rainfall events and delineating the thresholds, tending to

underestimate the ground-based precipitation mainly for sub-daily scales. Although

underestimating the ground-based data, the satellite-based products can be applied as an

alternative source to develop warning systems, especially in areas with a lower density of

rain gauges. Overall, the results found in this study showed to be helpful for decision-making

by the implementation of flood monitoring and early warning systems, and, consequently to

contribute to the development of more robust and/or complex flood models able to minimize

the hydrological impacts, whether using ground-based or satellite-based data.

**KEYWORDS:** Natural disasters, Extreme precipitation, Rainfall threshold, Floods, Flash

floods.

# 6

RESUMO

Grande esforço está sendo realizado durantes as últimas décadas para desenvolvimento de

métodos de monitoramento de desastres hidrológicos. Dentre eles, os limiares de

precipitação, definidos como a condição mínima de precipitação que são susceptíveis a

deflagração desastres hidrológicos, são a ferramenta mais popular usada para estudar a

relação entre precipitação e desastres hidrológicos, destacando-se devido à sua abordagem

simples. Alguns fatores dificultam a determinação dos limiares de chuva, como a qualidade

dos dados de chuva e desastres, e as grandes distâncias entre as estações pluviométricas e os

desastres. Para superar essas limitações, o uso de produtos de precipitação por satélite é uma

saída para caracterizar os eventos de chuva que desencadeiam desastres. Consequentemente,

esta tese tem como objetivo apresentar um método melhorado para a delimitação de limiares

de picos de intensidade de chuva para avaliação e alerta dos desastres, através da aplicação

de métodos baseados em probabilística e levando em consideração as condições

antecedentes ao desastre. Além disso, avaliar a qualidade dos produtos de precipitação

baseados em satélite para criar limites de precipitação para o monitoramento de desastres

hidrológicos. O Estado de São Paulo foi escolhido por ser uma região típica para ocorrências

de deslizamentos e inundações. Além disso, São Paulo é o estado mais rico do Brasil, com

o maior número de registros de inundações e enxurradas, bem como dados pluviométricos

subdiários disponibilizados por órgãos públicos. Os resultados mostram que o uso de níveis

de tolerância e o delineamento de um limiar intermediário pela incorporação de uma curva

exponencial que relaciona a intensidade da chuva e o Índice de Precipitação Antecedente

(API) ajudou a reduzir significativamente muitas incertezas no monitoramento de desastres

hidrológicos. Além disso, a avaliação dos produtos baseados em satélite mostrou que eles

apresentam menor acurácia em relação aos pluviômetros, tendendo a subestimar as medidas

observadas in-situ, principalmente, para escalas subdiárias. No entanto, eles podem ser

aplicados como fonte alternativa para o desenvolvimento de sistemas de alerta,

principalmente, em áreas com menor densidade de pluviômetros. De forma geral, conclui-

se que os resultados encontrados devem ser úteis na tomada de decisão, na implementação

de sistemas de monitoramento e alerta precoce de inundações, e na contribuição para o

desenvolvimento de modelos mais robustos e/ou complexos para minimizar os impactos,

seja utilizando dados in-situ ou baseados em satélite.

**PALAVRAS-CHAVES:** Desastres naturais, Precipitações extremas, Limiares deprecipitação, inundação, enxurrada.

# 7

TABLE OF CONTENTS

ACKNOWLEDGEMENTS ABSTRACT

RESUMO LIST OF FIGURES

LIST OF TABLES

1 INTRODUCTION ..................................................................................................... 15

1.1 HYPOTHESES ........................................................................................................ 17

1.2 MAIN AIMS ........................................................................................................... 17

1.3 SPECIFIC AIMS ...................................................................................................... 18

1.4 THESIS STRUCTURE .............................................................................................. 18

2 LITERATURE REVIEW ......................................................................................... 19

2.1 NATURAL DISASTERS ........................................................................................... 19

2.1.1 Definition......................................................................................................... 19 2.1.2 Increasing recurrence and databases development ........................................ 20

2.1.3 Disaster Classification .................................................................................... 21**2.2 EXTREME PRECIPITATION EVENTS ........................................................................ 23**

2.2.1 Ground-based measurements .......................................................................... 24 2.2.2 Satellite-based precipitation products............................................................. 25

2.3 RAINFALL THRESHOLD METHODOLOGIES ............................................................. 27

3 STUDY AREA CHARACTERISTICS ................................................................... 31

4 IMPROVED RAINFALL-THRESHOLD APPROACH....................................... 34

4.1 CONTEXTUALIZATION .......................................................................................... 34

4.2 MATERIALS AND METHODS................................................................................... 35

4.2.1 Selection of events ........................................................................................... 36_4.2.1.1 Rainfall data............................................................................................. 36_

4.2.1.2 Flood and flash flood data ....................................................................... 37 4.2.1.3 Characterisation of rainfall events........................................................... 38

4.2.2 Improvements of the rainfall threshold ........................................................... 39**4.2.2.1 Definition of the rainfall peak intensity-duration threshold .................... 39**

4.2.2.2 Application of tolerance levels ................................................................ 39 4.2.2.3 Delineating the intermediate threshold.................................................... 40

4.2.3 Evaluation procedures..................................................................................... 40 4.2.4 Link to the colour-class warning level systems ............................................... 41

4.3 RESULTS AND DISCUSSION.................................................................................... 42

4.3.1 Characterisation of the flood and flash flood occurrences ............................. 42 4.3.2 Rainfall peak intensity-duration threshold...................................................... 42

4.3.3 Tolerance levels............................................................................................... 45 4.3.4 Intermediate threshold..................................................................................... 47

# 8

5 CHARACTERIZATION OF EXTREME EVENTS AND DELINEATION OF RAINFALL THRESHOLDS BY SATELLITE-BASED PRECIPITATION

PRODUCTS ....................................................................................................................... 51

5.1 MATERIALS AND METHODS................................................................................... 52

5.1.1 Satellite-based rainfall products ..................................................................... 52 5.1.2 Flood dataset ................................................................................................... 54

5.1.3 Observed rainfall dataset ................................................................................ 54 5.1.4 Rainfall events and threshold definition.......................................................... 55

**5.1.5 Comparison and evaluation procedures ......................................................... 55**5.2 RESULTS AND DISCUSSION.................................................................................... 57

5.2.1 Characterisation of rainfall events that triggers floods .................................. 57 5.2.2 Overall analysis of the uncorrected dataset .................................................... 59

5.2.3 Overall analysis of the corrected dataset ........................................................ 60 5.2.4 Rainfall thresholds........................................................................................... 60

5.2.4.1 Evaluation for different tolerance levels ................................................. 60 5.2.4.2 Determination of rainfall thresholds........................................................ 62

6 CONCLUSIONS AND RECOMMENDATIONS .................................................. 65

REFERENCES .................................................................................................................. 68

APPENDIXES A................................................................................................................ 81

APPENDIXES B................................................................................................................ 94

# 9

LIST OF FIGURES

Figure 1 – Examples of recurrent natural disasters in Brazil (Courtesy: UNIFESP and UNA- SUS 2016) ................................................................................................................... 22

Figure 2 – Flowchart for the precipitation products. (Courtesy: Sun et al. 2018)............... 27 Figure 3 – Concept of rainfall thresholds (a) clearly distinguished (b) not clearly

distinguished (Courtesy: modified from Berti et al. 2012).......................................... 28 Figure 4 – Long-term (1950–1990) mean monthly rainfall for the coastal and plateau zones

obtained from the meteorological stations used by Alvares et al. (2013). .................. 31 Figure 5 – (a) Map of Brazil showing the São Paulo State. (b) Rain gauges and Köppen’s

classification map for São Paulo State according to Alvares et al. (2013). (c) Elevation of the São Paulo State and location of the 347 flood occurrences. (d) Demographic

density of São Paulo and location of the 71 flash flood occurrences. (e) Long-term (1950-1990) mean annual rainfall obtained from the meteorological stations used by

Alvares et al. (2013). (f) Landsat-based land use and land cover map for 2017 provided by the MapBiomas Project (Souza et al. 2020). .......................................................... 32

Figure 6 – Hydrological disaster in São Paulo (Courtesy: CEPED 2013) .......................... 33 Figure 7 – Methodological chart, showing (a) the raw and selected flood and flash flood

occurrences; (b) the rainfall intensity threshold approach; (c) the tolerance levels adopted to improve the rainfall intensity threshold; and (d) the improved threshold

relating rainfall peak intensity and antecedent precipitation index (API). .................. 36 Figure 8 – Rainfall intensities peak versus rainfall duration applying the approach without

the tolerance levels for (a) floods and (b) flash floods. Improved application of the methodology using the tolerance levels (99th percentile and 5%) for (c) floods and (d)

flash floods. The graphs use logarithmic scale............................................................ 43 Figure 9 – Peak rainfall intensity versus Antecedent Precipitation Index (API) graphs for

each time-step and delimitation of the exponential curves for warning level systems applied for floods......................................................................................................... 48

Figure 10 – Peak rainfall intensity versus Antecedent Precipitation Index (API) graphs for each time-step and delimitation of the exponential curves for warning level systems

applied for flash floods. ............................................................................................... 49 Figure 11. Daily precipitation classification that leads flood occurrences in São Paulo State

..................................................................................................................................... 57 Figure 12. Graph showing the (a) KGE, (b) CC, (c) BIAS, and (d) VAR scores for the 14

satellite-based rainfall, considering only extreme precipitation events for time steps ranging from 3 hours to 10 days. The red lines represent the perfect values. ............. 59

Figure 13. Heatmap of the mean values of (a) POD, (b) FAR, and (c) HK using different no- exceedance probability. ............................................................................................... 61

Figure 14. Accumulated precipitation versus duration applying the tolerance levels of 5, 10, 20, 30, 40, and 50% for the (a) rain gauges, (b) CHIRP V2.0, (c) CHIRPS V2.0, (d)

IMERG-E V06, (e) IMERG-L V06, (f) IMERG-F V06, (g) CMORPH-CRT V01, (h) MERRA-2, (i) MSWEP V2.2, (j) PERSIANN, (k) PERSIANN-CCS, (l) PERSIANN-

CDR V1R1, (m) PDIR-Now, (n) SM2RAIN-ASCAT V1.2, and (o) GPM+SM2RAIN. ..................................................................................................................................... 63

Figure 15. BIAS values for the estimated rainfall thresholds, using rain gauge as a reference, for tolerance levels of (a) 5, (b) 10, (c) 20, (d) 30, (e) 40, and (f) 50%. The red lines

represent the perfect values. ........................................................................................ 64

# 10

Figure 16 – Scatter plots of rainfall observed values (rain gauges) vs estimated values (CHIRP V2.0) that lead to floods at different timescales............................................ 82

Figure 17 - Scatter plots of rainfall observed values (rain gauges) vs estimated values (CHIRPS V2.0) that lead to floods at different timescales. ........................................ 82

Figure 18 – Scatter plots of rainfall observed values (rain gauges) vs estimated values (CMORPH-CRT V1.0) that lead to floods at different timescales. ............................ 83

Figure 19 - Scatter plots of rainfall observed values (rain gauges) vs estimated values (IMERGHHE V06) that lead to floods at different timescales. .................................. 84

Figure 20 – Scatter plots of rainfall observed values (rain gauges) vs estimated values (IMERGHLL V06) that lead to floods at different timescales.................................... 85

Figure 21 – Scatter plots of rainfall observed values (rain gauges) vs estimated values (IMERGHH V06) that lead to floods at different timescales...................................... 86

Figure 22 – Scatter plots of rainfall observed values (rain gauges) vs estimated values (MERRA-2) that lead to floods at different timescales............................................... 87

Figure 23 – Scatter plots of rainfall observed values (rain gauges) vs estimated values (MSWEP V2.2) that lead to floods at different timescales. ........................................ 88

Figure 24 – Scatter plots of rainfall observed values (rain gauges) vs estimated values (PDIR- Now) that lead to floods at different timescales. ......................................................... 89

Figure 25 – Scatter plots of rainfall observed values (rain gauges) vs estimated values (PERSIANN) that lead to floods at different timescales............................................. 90

Figure 26 – Scatter plots of rainfall observed values (rain gauges) vs estimated values (PERSIANN-CCS) that lead to floods at different timescales. ................................... 91

Figure 27 – Scatter plots of rainfall observed values (rain gauges) vs estimated values (PERSIANN-CDR V1R1) that lead to floods at different timescales......................... 92

Figure 28 – Scatter plots of rainfall observed values (rain gauges) vs estimated values (SM2RAIN-ASCAT V1.2) that lead to floods at different timescales. ...................... 92

Figure 29 – Scatter plots of rainfall observed values (rain gauges) vs estimated values (GPM+SM2RAIN) that lead to floods at different timescales.................................... 93

# 11

LIST OF TABLES

Table 1 – Hydrological disasters classification (Source: EM-DAT)................................... 23 Table 2 – Summary of relevant studies on precipitation thresholds ................................... 29

Table 3 – Summary of evaluation metrics for the flood and flash flood thresholds, considering the approach without the use of tolerance levels. .................................... 45

Table 4 – Summary of evaluation metrics for the floods and flash floods thresholds considering the tolerance levels (99th percentile and 5%) and the intermediate

thresholds..................................................................................................................... 46 Table 5 – Summary of evaluation metrics for flood and flash flood occurrences applying

the improved thresholds that use rainfall intensities and Antecedent Precipitation Index (API). ................................................................................................................. 50

Table 6. Summary of 14 precipitation estimates products evaluated in this study, similar to as presented by Beck et al. (2019)............................................................................... 53

Table 7 – Summary of Mean Relative Absolute Error (MRAE) for estimated precipitation products, considering different timescales .................................................................. 95

Table 8 – Summary of Root Mean Square Error (RMSE) for estimated precipitation products, considering different timescales. ................................................................. 96

Table 9 – Summary of Correlation Coefficient (CC) for estimated precipitation products, considering different timescales. ................................................................................. 97

Table 10 – Summary of BIAS for estimated precipitation products, considering different timescales. ................................................................................................................... 98

Table 11 – Summary of Variability (VAR) for estimated precipitation products, considering different timescales. ................................................................................. 99

Table 12 – Summary of KGE for estimated precipitation products, considering different timescales. ................................................................................................................. 100

# 12

LIST OF ABBREVIATIONS AND SYMBOLS

| a, b, c | – Constants values |
| --- | --- |
| API | – Antecedent Precipitation Index |
| BIAS | – Ratio of estimated and observed means |
| CC | – Pearson’s correlation coefficient |
| CEMADEN | – Brazilian National Centre for Monitoring Early Warning of Natural Disasters |
| CENAD | – National Center for Risk and Disaster Management |
| CEPED | – Center for Studies and Research on Disasters |

| CHIRP V2.0 | – Climate Hazards group InfraRed Precipitation V2.0 |
| --- | --- |
| CMORPH-CRT CHIRPS V2.0 | – Climate Hazards group InfraRed Precipitation with Stations V2.0 |

CPC MORPHing technique bias corrected V1.0 V1.0 –

| COBRADE | – Brazilian Coding of Disasters |
| --- | --- |
| CODAR | – Coding of Disasters, Threats, and Risks |
| CPC-Global | – Climate Prediction Center - Global |
| CRED | – Center for Research on the Epidemiology of Disasters |
| CRU TS v4 | – Climatic Research Unit gridded Time Series version 4 |
| DesInventar | – Disaster effects Inventory system |
| EM-DAT | – Emergency events Database |

| FAR | – False Alarm Ratio |
| --- | --- |
| FN | – False Negative |
| FP | – False Positive |
| G1 | – Group of events that represents intensities that likely lead to flood occurrences |
| G2 | – Group of events that represents intensities that may lead to flood occurrences |
| G3 | – Group of events that represents intensities that may not lead to flood occurrences |
| G4 | – Group of events that represents intensities that not likely lead to flood occurrences |

| GHCN-M v2 | – Global Historical Climatology Network Monthly version 2 |
| --- | --- |
| GPCC-daily | – Global Precipitation Climatology Center - daily Integration of IMERG-E with SM2RAIN-based rainfall estimates derived from satellite |
| GPM+SM2RAIN | – Soil Moisture products |

| HK | – Hanssen-Kuiper skill score |
| --- | --- |
| i | – number of antecedent days |
| I | – Intensity (mm.h-1) |
| IBGE | – Brazilian Institute of Geography and Statistics |

| IMERG-E V06 | – Integrated Multi-satellitE Retrievals for GPM early run V06 |
| --- | --- |
| IMERG-F V06 | – Integrated Multi-satellitE Retrievals for GPM final run V06 |
| IMERG-L V06 | – Integrated Multi-satellitE Retrievals for GPM late run V06 INTElligent use of climate models for adaptation to Non-Stationary hydrological |
| INTENSE project | – Extremes. |

| IPMET | – Meteorological Research Institute |
| --- | --- |
| K | – Decay rate |
| KGE | – Kling-Gupta Efficiency |
| MASA | – Metropolitan Area of Santo André |

# 13

| MASP | – Metropolitan Area of São Paulo |
| --- | --- |
| MAU | – Metropolitan Area of Ubatuba |
| MERRA-2 | – Modern-Era Retrospective Analysis for Research and Applications 2 |

MSWEP V2.2 – Multi-Source Weighted-Ensemble Precipitation V2.2

| NRCS | – Natural Resources Conservation Service |
| --- | --- |
| PDIR-Now | – Precipitation Dynamic Infrared Rain Rate near real-time (PDIR-Now) Precipitation Estimation from Remotely Sensed Information using Artificial Neural |
| PERSIANN | – Networks |

| PERSIANN-CCS | – Precipitation Estimation from Remotely Sensed Information using Artificial Neural Networks Cloud Classification System |
| --- | --- |
| PERSIANN-CDR V1R1 | – Precipitation Estimation from Remotely Sensed Information using Artificial Neural Networks Climate Data |

| PNGR | – National Planning for Risk Management |
| --- | --- |
| POD | – Probability of Detection |
| PPV | – Positive Predictive Value |
| Pt | – Rainfall for the day t (mm) |
| S2ID – | – Integrated Disaster Information System |
| SIDEC | – Integrated Civil Defense System The Integrated Storm Monitoring, Forecasting and Alerting System for the Brazilian |
| SIMPAT | – South - Southeast Regions |

SM2RAIN- Precipitation Estimation from the application of the SM2Rain algorithm to the ASCAT ASCAT V1.2 – soil moisture data

| TN | – True Negative |
| --- | --- |
| TP | – True Positive |
| TRMM | – Tropical Rainfall Measuring Mission |
| UDEL | – University of Delaware |
| UNDRR | – United Nations Office for Disaster Risk Reduction United States Agency for International Development’s Office of Foreign Disaster |

USAID/OFDA – Assistance

| VAR | – Ratio of the estimated and observed coefficients of variation |
| --- | --- |
| WHO | – World Health Organization |
| WMO | – World Meteorological Organization |

# 14

1 INTRODUCTION

Many natural disasters events occur every year in almost all countries, causing

thousands of deaths, considerable structural damages, and significative economic losses

worldwide (Hallegatte et al. 2013; Sampson et al. 2015; Dinis et al. 2021). According to the

United Nations Office for Disaster Risk Reduction (UNDRR), the number of natural

disasters grew 1.75 times between 2000 and 2019 compared to the previous twenty years

(i.e., from 1980 to 1999). Among the natural disasters, floods are the most common type of

disaster, accounting for 44% of all occurrences considered in the UNDRR report, showing a

growth of 2.3 times and accounting for more than 1.65 billion people affected, 104,614

deaths, and 651 billion dollars of economic loss. This growing number of flood events over

the years is mainly due to extreme weather conditions, high urbanization rate, and inadequate

response to disasters (Špitalar et al. 2014; Tsakiris 2014; Du et al. 2015).

Brazil has continental dimensions with distinct regional characteristics. Therefore,

the pattern of natural disasters varies from region to region, whether in terms of the type of

disaster and time of year in which they occur. However, drought and floods are the most

common phenomena that occur in all regions, causing the larger number of impacts

(UNIFESP and UNA-SUS 2016). Specifically, the São Paulo State is a typical hot spot for

disasters occurrences due to the region's natural characteristics associated with a high level

of urbanization (Tominaga et al. 2015). Thus, it is essential to understand the causes,

mechanisms involved, and dynamics of the processes that are happening with new shapes

and sizes during each passing year, to seek safer and more economically viable alternatives

for planning strategies and scenarios for disaster risk management (Ramos 2017).

During the last few decades, great efforts have been made for monitoring

hydrological disasters (Getirana et al. 2020; Young et al. 2021). Complex computer models

such as hydrodynamic models have been a new challenge for many researchers and

authorities to build warning systems (Azari et al. 2008; González-Cao et al. 2019; Li et al.

2019). Such methods aim to reduce the damages and deaths caused by floods (Froidevaux

et al. 2015; Jang 2015; Rijswick 2015). While such practice remains as the mainstream

approach, there are situations where empirical methods still prevail. This is because, in many

places, it is impossible to carry out detailed modelling of the related physical process (e.g.

landslides, floods, flash floods) either due to data availability or being too challenging to

model (Behrangi et al. 2011; Blenkinsop et al. 2018; Peres et al. 2018). Among the empirical

methods, the rainfall-threshold method is one of the most widely used for monitoring

15

hydrological disasters (Huang et al. 2015), where the thresholds are determined by the

properties derived from rainfall events such as intensity, duration, and antecedent

precipitation (Glade et al. 2000; Aleotti 2004; Berti et al. 2012; Papagiannaki et al. 2015;

Scheevel et al. 2017; Brunetti et al. 2018; Mirus et al. 2018). However, when compared with

the applications in predicting landslides, the number of studies using rainfall thresholds for

flood and flash floods warning systems remains low and the area has been poorly explored

(Diakakis 2012; Papagiannaki et al. 2015; Santos and Fragoso 2016).

As mentioned before, the data availability is still a big challenge to overcome all over

the globe. In Brazil, regarding flood records, official information is still scarce or not unified

in a single database. To get around this problem, it is necessary to survey occurrences from

various sources of information. However, some problems can be observed, such as the

existence of duplicate records, the difficulty in identifying the type of natural disaster that

actually occurred, the lack of accuracy of the day and location of occurrence, or the coverage

of the affected area (Carvalho 2018). Similarly to the occurrences, the use of accurate and

spatially well-distributed sub-daily rainfall data is recognized by the scientific community

as an essential source of information to create robust prediction and warning hydrological

disaster systems (Dunkerley 2019; Shrestha et al. 2019; Chikoore et al. 2021). However,

obtaining the sub-daily rainfall variability over large areas by in-situ data is still a hard task

because such records sparsely cover the global landmass (Hegerl et al. 2015; Lewis et al.

2019). The number of in-situ sub-daily rainfall records is even lower for the key tropical

regions, probably due to the higher implementation costs of rain gauges able to measure sub-

daily events, compared with those that measure on a daily timescale (Kidd et al. 2017; Freitas

et al. 2020).

The use of cutting-edge satellite-borne remote sensing technology has played a key

role over the recent decades in providing sub-daily rainfall data (Tan et al. 2014; Levizzani

et al. 2018; Sungmin and Kirstetter 2018). Currently, a plethora of promising recently

released and revised gridded satellite-based products providing valuable distributed

information of sub-daily rainfall data are available to be used for many applications (Yuan

et al. 2019; Llauca et al. 2021). The characteristics of these rainfall products differ in terms

of spatial and temporal resolutions (from 0.04º to 2.5º and from 30 minutes to monthly,

respectively), spatial coverage (from continental to fully global), latency (from 15 minutes

to several years), among others (Beck et al. 2017b). Despite that, only a few studies have

assessed the performance of these products in landslide monitoring (Brunetti et al. 2021),

even less for flood monitoring.

16

This thesis was based on the development of two studies: 1) to address some

problems found in existing rainfall threshold methodologies and 2) to evaluate alternatives

for the development of tools useful for warning systems applying different satellite-based

precipitation products. Firstly, this thesis seeks to propose the improvement of a

methodology proposed by Diakakis (2012) for delimitation of rainfall thresholds for flood

and flash flood through the reduction of uncertainties and, consequently, minimization of

observed false alarms. For this first step of the study, two precipitation thresholds were

determined, called upper and lower threshold, in which tolerance limits were applied for

each one of them to allow a better adjustment in the warning level settings. In addition, a

methodology for delineating an intermediate threshold through the evaluation of different

interactions between intensity peaks and API (Antecedent Precipitation Index) was

presented, taking into consideration different evaluation metrics. Based on this first study, a

considerable amount of flood occurrences in São Paulo State could not be used because of

the poor data quality of some rain gauges and/or the lack of rain gauge coverage. Therefore,

the second study of this thesis was to evaluate different satellite-based precipitation in

characterizing extreme events and delineating rainfall thresholds for flood hazards. Then, 14

satellite-based precipitation products were assessed for different time steps to characterize

the rainfall events that trigger floods by applying different metrics for evaluating their

performances.

1.1 Hypotheses

The following two hypotheses were addressed in this study:

1. The reduction of uncertainties using rainfall threshold methodologies for floods
and flash floods can be achieved by determining tolerance limits, delimiting an intermediate

threshold, and performing different interactions between intensity peaks rainfall and the

Antecedent Precipitation Index (API);

2. Satellite-based precipitation products can be used to spatially define rainfall
thresholds for different time steps based on an existing methodology to develop warning

system for floods.

1.2 Main aims

17

This thesis aims to develop methodologies for analyzing the relationship between the

extreme precipitation events and (flash)floods occurrence applying ground- and satellite-

based (sub)daily data, to establish a correlation between these variables, define rainfall

thresholds with the potential to trigger floods, and assess their performance.

1.3 Specific aims

The specific aims of this thesis are:

**** To propose a rainfall threshold estimation approach to improve floods and flash

floods hazards monitoring by applying tolerance limits, setting an intermediate

threshold, and evaluating performance considering different evaluation metrics to

reduce uncertainties and minimize observed false alarms;

**** To assess the quality of the current available satellite-based precipitation products to

identify extreme rainfall events and delineate rainfall thresholds for floods.

**** To perform quality analysis of rainfall data for CEMADEN rainfall gauges and the

satellite-based products;

**** To survey hydrological disasters from different sources of information, as well as to

characterize the rainfall events that triggered them, developing therefore a database

for the state of São Paulo between 2015 and 2019;

1.4 Thesis Structure

The thesis was divided into six major items in the following order: 1) Introduction,

presenting a contextualization and justification that motivated the development of this thesis;

2) Literature review, covering conceptual and basic topics essential to better understand the
study; 3) Study area, presenting the characteristics of the studied area and justifying its

selection; 4) Improved rainfall-threshold approach, showing the proposed methodology for

delimitation of rainfall thresholds; 5) Characterization of extreme rainfall events by satellite-

based products, assessing different satellite-based products to difine rainfall thresholds; and

6) Conclusions and recommendations, highlighting the main results found and proposing
further studies.

18

2 LITERATURE REVIEW

The literature review was subdivided into three major items, addressing all subjects

of the methodology in the following order: 1) natural disasters, covering basic concepts; 2)

extreme rainfall events, definition, precipitation measurement methods; and 3) rainfall

threshold methodologies.

2.1 Natural Disasters

2.1.1 Definition

According to the World Health Organization (WHO 1971), a natural disaster is an

act of nature of such magnitude as to create a catastrophic situation in which day-to-day

patterns of life are suddenly disrupted, and, as a result, they need basic assistance and

protection against unfavorable environmental factors and conditions. The Center for

Research on the Epidemiology of Disasters (CRED) adds that it is a situation or event

overwhelming the local capacity to deal with the situation using its own resources; an

unforeseen and often sudden event that causes great damage, destruction and human

suffering (Wallemacq and House 2018).

In Brazil, the Normative Instruction nº 1 was published in August 2012 by the Nation

Integration Ministry, which establishes procedures and criteria for the decree and recognition

of an Emergency Situation or State of Public Calamity by the Municipalities, States, and the

Federal District. This document in its first article presents the definition of disaster as the

result of adverse events, natural or man-made in a vulnerable scenario, causing serious

disturbance to the functioning of a community or society involving extensive human,

material, economic or environmental loss and damage, which exceeds the local capacity to

deal with the problem using its own resources (Brasil 2012).

Overall, disasters cause intense changes in society and combine different factors such

as threats and vulnerabilities, which expose certain populations to the risk of these

phenomena occur. Disaster occurs when risks are poorly managed and the population is not

prepared to face extreme or unexpected phenomena (Furtado et al. 2014).

19

2.1.2 Increasing recurrence and databases development

The number of natural disasters has been increasing in recent decades. Several

authors justify this increase as a consequence of the intense urbanization process associated

with a disorderly growth of regions unsuitable for occupation, due to its unfavorable

geological and geomorphological characteristics (Barbería et al. 2014; Papagiannaki et al.

2015). Moreover, anthropic action, such as deforestation, changes in drainage, garbage

disposal, and others, mostly without the implementation of adequate infrastructure, increase

the dangers and instabilities (Srinivas and Nakagawa 2008; Dhyani and Dhyani 2016).

Therefore, when there is an agglomeration of buildings in improper areas, landslides and

floods, for example, assume catastrophic proportions causing great economic and social

losses (Tominaga et al. 2015).

The development of a natural disasters database is essential to analyze its

characteristics, as it aims to assist in the decision-making for disaster preparedness and

provide an objective basis for vulnerability assessment and set priorities (Battistini et al.

2017; Segoni et al. 2021). In 1988, CRED launched a worldwide disaster database called

Emergency events Database (EM-DAT) with assistance from the United States Agency for

International Development's Office of Foreign Disaster Assistance (USAID/OFDA). The

data is compiled from a variety of sources, including non-governmental organizations,

insurance companies, research institutes, and news agencies. For a disaster to be added to

the database, at least one of the following criteria must be met: 10 or more people killed; 100

or more people affected; declaration of a state of emergency; or requesting international

assistance (Guha-sapir et al. 2016).

In Brazil, in 2012, the system called Integrated Disaster Information System (S2ID)

was developed by the National Planning for Risk Management (PNGR) project in technical

cooperation between the Center for Studies and Research on Disasters from Federal

University of Santa Catarina (CEPED/ UFSC) and the Ministry of National Integration,

through the National Secretariat of Civil Defense. The purpose of the S2ID system is to

streamline the procedures to recognize requesting of Emergency Situation or State of Public

Calamity and the transfer of federal resources to States or Municipalities affected by

disasters (Gimenez 2017). However, some problems can be pointed that significantly

compromise the stages of characterization and diagnosis of areas susceptible to natural

disasters. Normally, these problems are related to the existence of several discrepancies and

incompleteness in the data and recorded information (Carvalho 2018).

20

The Meteorological Research Institute (IPMET) makes available natural disaster

records from São Paulo and Parana State through the Integrated System for Monitoring,

Forecasting and Warning of Storms for the South-Southeast Regions of Brazil (SIMPAT),

which compiles the information obtained from different sources, for example, Civil Defense

and news. However, this information does not undergo any prior analysis, therefore it is

necessary to properly verify the occurrences. The Civil Defense information can be

consulted through the Integrated Civil Defense System – SIDEC, which is a geo-referenced

management platform that facilitates decision-making.

In the near future, the National Center for Monitoring and Alerting of Natural

Disasters (CEMADEN) will make available a standardized database, which will provide

historical records of the occurrence of disaster related to geo-hydrological risks in at least

958 municipalities. The system is under development and soon this database will be released

on the CEMADEN Interactive Map. The objective of CEMADEN is also to integrate this

database with the international platform in South America called “DesInventar” (Disaster

Effects Inventory System). The “DesInventar” platform is a database of natural disasters

conceived in the 1990s by researchers at La Red (Network for Social Studies in Disaster

Prevention in Latin America) to bring together several databases within one single platform,

serving as data acquisition and query system for disasters of any magnitude. Almost all Latin

American countries take part in DesIventar database, except for Brazil.

2.1.3 Disaster Classification

The Brazilian Coding of Disasters (COBRADE) was established through the

Normative Instruction No. 1 to replace the Coding of Disasters, Threats, and Risks

(CODAR). The new coding was created from the international classification used by

Emergency events Database (EM-DAT). According to the National Center for Risk and

Disaster Management (CENAD 2014), an important reason to standardize the classification

of disasters is the need to record these phenomena in the historical context of the country.

Coding allows the formation of a database, which can be used for a contextualized analysis

of the occurrence of disasters worldwide or in the national territory, enabling the planning

of preventive and preparatory measures to deal with these adverse events. Moreover, the

adoption of the EM-DAT classification is important due to the need to adapt the Brazilian

classification to the standards established worldwide, and to effectively include Brazil in the

expansion of this important international database. Another advantage verified to use EM-

21

DAT classification for the construction of COBRADE was the need to simplify the

classification of disasters contained in CODAR.

The international and national classifications of disasters are divided into two

categories: natural or technological. About natural disasters, the international classification

recognizes six groups, in contrast to the national classification that recognizes only five,

which differs as to the extraterrestrial group. In addition, some adaptations were made to the

national classification to better adapt to the Brazilian reality. Among the remaining five

groups, EM-DAT defined them as follows:

__ **Geophysical**: A hazard originating from solid earth. This term is used

interchangeably with the term geological hazard (Figure 1a).

**** _Meteorological:_ A hazard caused by short-lived, micro- to meso-scale extreme

weather and atmospheric conditions that last from minutes to days.

__ **Hydrological**: A hazard caused by the occurrence, movement, and distribution of

surface and subsurface freshwater and saltwater (Figure 1b e Figure 1c).

**** _Climatological_: A hazard caused by long-lived, meso- to macro-scale atmospheric

processes ranging from intra-seasonal to multi-decadal climate variability. (Figure

1d, Figure 1e e Figure 1f).

**** _Biological_: A hazard caused by the exposure to living organisms and their toxic

substances (e.g. venom, mold) or vector-borne diseases that they may carry.

**Figure 1 –** Examples of recurrent natural disasters in Brazil (Courtesy: UNIFESP and UNA-SUS2016)

22

Hydrological disasters, Table 1, have among their causes the action of natural

processes that imply excess water in the affected system, usually associated with extremes

of floods and/or urban drainage problems (Tingsanchali 2012; Atta-ur-Rahman et al. 2016).

The last two decades (1998–2017) represent the largest number of records caused by

hydrological disasters in history, mainly, induced by floods (accounting for 43.4% of all-

natural disasters) (Wallemacq and House 2018).

**Table 1 –** Hydrological disasters classification (Source: EM-DAT)

_Disaster main_ Disaster Description_type_ Sub-type

| Coastal flood | Overflow of water Higher-than normal levels along the coast and in lakes or reservoirs |
| --- | --- |
| Riverine flood | A general term for the overflow of water from a stream channel onto normally dry land in the floodplain |

**Flood** Rapid inland floods due to intense rainfall. A flash flood describes suddenFlash flood flooding with short duration. In sloped terrain the water flows rapidly with

a high destruction potential. The accumulation of floating ice restricting or blocking a river’s flow and

Ice jam flood drainage. Ice jams tend to develop near river bends and obstructions (e.g. bridges).

**Landslide** Avalanche A large mass of loosened earth material, snow, or ice that slides, flows orfalls rapidly down a mountainside under the force of gravity

Rogue wave An unusual single crest of an ocean wave far out at sea that is much higher and/or steeper than other waves in the prevailing swell system

**Wave Action** A standing wave of water in a large semi- or fully-enclosed body of waterSeiche (lakes or bays) created by strong winds and/or a large barometric pressure

gradient.

2.2 Extreme precipitation events

Rainfall is an intermittent phenomenon with an irregular spatiotemporal distribution

that can cause many natural disasters (Dunkerley 2008). It is the natural agent that triggers

situations of flood and flash flood, which are the real threats to the socio-economic system

(Miguez et al. 2018).

The World Meteorological Organization (WMO) defines extreme precipitation as

significant accumulated precipitation that often leads to multiple disasters (e.g., floods, mass

movements, flash floods, etc.). However, extreme precipitation varies seasonally and from

region to region, so it is not possible to use a single definition of an extreme precipitation

event that is suitable for all regions. Thus, it is desirable to quantify multiple time scales of

extreme precipitation events for different places. Generally, an extreme precipitation event

is recognized when it relates to one of the following contexts: (1) when it exceeds a certain

23

threshold that has a certain associated impact, i.e., a fixed threshold, or (2) an event of

precipitation is considered extreme due to its rarity, that is, a threshold based on the

percentile (WMO 2015).

Therefore, the use of accurate and spatially well-distributed sub-daily rainfall data is

an essential source of information to create a reliable warning system that provides useful

knowledge for decision-making (Dunkerley 2019; Shrestha et al. 2019; Chikoore et al.

2021). The rainfall characteristics analyzed in most studies are the total precipitation,

duration, intensity, and temporal and spatial distribution.

2.2.1 Ground-based measurements

Rainfall over the ground can be measured using rain gauges and radars. The first is

the most traditional way to provide accurate rainfall data, measuring precipitation directly at

the Earth’s surface (Kidd 2001). However, obtaining sub-daily rainfall variability over large

areas is still a hard task because such records sparsely cover the global landmass (Hegerl et

al. 2015; Lewis et al. 2019). The number of in-situ sub-daily rainfall records is even lower

for the tropical regions, probably due to the higher implementation costs of rain gauges able

to measure sub-daily events, compared with those that measure on a daily timescale (Kidd

et al. 2017; Freitas et al. 2020). Consequently, the use of empirical methods that consider

properties derived from rainfall events cannot be properly applied in such low-density or

inexistent gauge areas.

Thus, new projects emerged aiming to create a reliable precipitation database. The

INTENSE project (INTElligent use of climate models for adaptation to non-Stationary

hydrological Extremes) is the first major international effort to focus on global extreme sub-

daily rainfall, allowing substantial advances in the quantification of observed historical

changes. However, the INTENSE project identified after a data collection initiative that

countries from Africa and Latin America have the lowest availability of sub-daily rainfall

data (Blenkinsop et al. 2018). In Brazil, CEMADEN created a sub-daily monitoring network

containing approximately 3,400 automatic rain gauges nationwide. This network was created

to support the prediction and development of warning systems of disasters related to

precipitation, such as floods and landslides. Thus, most rain gauges are located in cities and

the rainfall recording time is 10 minutes under rain and 60 minutes when there is no rain.

Moreover, rain gauges provide only-single point measurements and have a far from

ideal spatial distribution around the world, hence they poorly represent the spatial variability

24

of precipitation, which varies from a few meters to several kilometers, making the sampling

requirements for measuring its spatial distribution extremely stringent. In contrast, radars are

an alternative to rain gauges and provide real-time measurement with high temporal and

spatial resolution, but their coverage is limited only over land and is also affected by the lack

of accessibility because of their high cost (Varma 2018).

The radar system emits a beam of energy at the microwave energy that is

backscattered from particles in the atmosphere, which can then be converted into a measure

of rainfall intensity (Kidd and Huffman 2011). However, the accuracy of radar

measurements is in general insufficient, particularly in the case of extreme rainfall

magnitudes (Marra and Morin 2015). This is due to the fact that radar rainfall intensity is

derived indirectly from measured radar reflectivity instead of being a direct measurement

(Ochoa-Rodriguez et al. 2019). As a result, both radar reflectivity measurements and the

reflectivity-intensity conversion process are subject to multiple sources of errors (Villarini

and Krajewski 2010).

2.2.2 Satellite-based precipitation products

According to Varma (2018), due to the difficulties and limitations of ground

measurements, satellite-based precipitation products become the most convenient way to

estimate precipitation over large areas. Nowadays, with the advance of the number of

satellite sensors and imaging technology, a great number of promising recently released and

revised satellite-based products providing valuable distributed information of sub-daily

rainfall data are available to be used for many applications (Yuan et al. 2019; Llauca et al.

2021).

The sensors onboard satellites can be classified into three categories:

Visible/InfraRed sensors, passive Microwave, and active Microwave sensors (Michaelides

et al., 2009; Prigent, 2010). Corresponding methods used to derive precipitation have been

developed, including the Visible/InfraRed-based methods, active and passive Microwave

techniques, and merged Visible/InfraRed and Microwave approaches (Kidd & Levizzani,

2011). According to Sun et al. (2018) and Varma (2018):

**** The Visible/Infrared methods share common characteristics as they provide

information only on the top of the cloud, hence rain droplets inside the clouds are not

directly sensed. So, the precipitation estimate is indirect thought the principle that

25

cold and bright clouds are related to convection; cold cloud tops suggest greater

vertical development in the cloud and therefore more rain. They provide wide

coverage over tropical regions with high spatial and temporal resolution (e.g.,

PERSIANN, PERSIANN CCS).

**** Passive microwave techniques are a more direct method of measuring precipitation

than the Visible/Infrared techniques because they can penetrate clouds and sense

precipitation-sized particles. The most critical disadvantage of passive microwave

precipitation estimation is that they have low spatiotemporal coverage (e.g., IMERG-

products).

**** The use of active microwave observations from satellites for precipitation began with

the launch of the first spaceborne precipitation radar in the TRMM mission in 1997,

which made it possible to capture the three-dimensional structure of rain. The active

microwave techniques offer the most direct of all satellite estimation methods,

despite this, it has been limited mainly to TRMM.

As mentioned before, rain gauges provide accurate measurements of precipitation at

single points but are sparsely distributed over the globe, as well as can be affected by

sampling errors (Habib et al. 2001; Kidd et al. 2017). On the other hand, satellite

observations have homogeneous spatial coverage, however random errors and biases can be

detected, e.g., deficiencies in the algorithms (Chen et al. 2021; Shen et al. 2021). Therefore,

merge different sources of information to overcome these errors and biases combining the

individual advantages of the different methods are currently aim at various studies. (Figure

2). For example, combining gauge and satellite data, such as PERSIANN-CDR V1R1,

CMORPH-CRT V1.0.

Moreover, reanalysis datasets are also available and are mostly used in the study of

weather and climate. Reanalysis generates large variety of atmospheric, sea-state, and land

surface parameters across a uniform grid with spatial homogeneity over long time periods

through data assimilation, a process that relies on both observations and model-based

forecasts to estimate conditions (Dee et al. 2014; Sun et al. 2018). Nowadays, more complex

models, multiple observed datasets for multiple variables, and different data assimilation

techniques are essential factors that improve their quality (Parker 2016), e.g., ERA-Interim,

CHIRPS V2.0, MERRA-2, MSWEP V2.2.

26

**Figure 2 –** Flowchart for the precipitation products. (Courtesy: Sun et al. 2018)

2.3 Rainfall threshold methodologies

Great efforts have been made during the last few decades to develop and improve

methods for a better flood prediction aiming to reduce the damages and deaths caused by

floods (Froidevaux et al. 2015; Jang 2015; Rijswick 2015; Getirana et al. 2020; Young et al.

2021). However, it has been gradually applied more for landslide warning purposes than for

flooding (Diakakis 2012; Papagiannaki et al. 2015; Santos and Fragoso 2016).

Among the existing methods for the development of warning systems, they can be

grouped into three main categories: (i) methods that combine soil mechanics and hydrology;

(ii) exclusively hydrological methods (methods based on the tank model); and (iii) empirical

methods (CEMADEN 2018). Among them, the empirical methods still prevail as an

alternative approaches to build hydrological disasters warning systems, since other methods

require a set of detailed input data or challenging complex models with high computation

costs (Yang et al. 2016).

The rainfall threshold approaches are a widely empirical method used for

hydrological disasters monitoring (e.g., floods, flash floods, debris flows and landslides)

(Glade et al. 2000; Aleotti 2004; Berti et al. 2012; Santos and Fragoso 2016; Scheevel et al.

27

2017; Mirus et al. 2018). This method aims to delimit a clear line between rainfall events

that might or might not lead to disasters (Figure 3a), i.e., the rainfall threshold defines a safe

zone and an unsafe zone to the triggering of disasters. However, in many cases, this

distinction is not so trivial as other factors can contribute to disaster occurrences.

Consequently, an area of uncertainty arises (Figure 3b), in which there is a mixture of records

of rainfall events that trigger and did not trigger a disaster. The improvement of the currently

available methodologies (i.e., by reducing such uncertainties) is exactly the first main aim

of this thesis.

**Figure 3 –** Concept of rainfall thresholds (a) clearly distinguished (b) not clearly distinguished(Courtesy: modified from Berti et al. 2012)

In general, it is observed in the literature different approaches to characterize the

rainfall events used to determine rainfall thresholds: (i) using precipitation for a specific

rainfall event, for example, through the relationship between the intensity/accumulated

rainfall and the duration of the event (Cannon et al. 2008; Diakakis 2012; Segoni et al. 2014;

Papagiannaki et al. 2015; Rossi et al. 2017; Brunetti et al. 2018; Peres et al. 2018); (ii)

considering the antecedent conditions, for example, through the relationship between the

intensity/accumulated rainfall and the rainfall that preceded the event (Zêzere et al. 2010;

Bai et al. 2014; Huang et al. 2015; Santos and Fragoso 2016; Pan et al. 2018); (iii) among

others. Table 2 presents some studies developed for the delimitation of precipitation

thresholds to different regions of the world.

28

**Table 2 –** Summary of relevant studies on precipitation thresholds

Study Natural Area Temporal Threshold Disaster Resolution Approach

Diakakis 2012 Flood Marathons – Greece Sub-hourly Intensity vs Duration

Segoni et al. 2014 Landslide Tuscany – Italy Hourly Intensity vs Duration

Huang et al. 2015 Landslide Huangshan – China Hourly Intensity vs Antecedent rainfall

| Papagiannaki et al. 2015 | Flood Flash | Attica - Greece | Sub-hourly | Intensity vs Duration |
| --- | --- | --- | --- | --- |
| Santos and Fragoso 2016 | Flood | Corgo basin – Portugal | Daily | Accumulated rainfall vs |

Antecedent rainfall Rossi et al. 2017 Landslide Umbria – Italy Hourly Accumulated

rainfall vs Duration Peruccacci et al. 2017 Landslide Italy Hourly Accumulated

rainfall vs Duration Brunetti et al. 2018 Landslide Italy Multi Hourly Accumulated

rainfall vs Duration Muntohar et al. 2021 Landslide Indonesia Daily Accumulated

rainfall vs Duration

For flood studies, Diakakis (2012) examined the peak rainfall intensities, total storm

accumulation, average intensity, and antecedent moisture conditions of the 52 most

important storm records in Greece that triggered flood, and showed that only peak rainfall

intensity presented a significant correlation with flood triggering, and defined a rainfall

threshold above which flooding becomes highly probable. This methodology was applied

later for flash floods in this same area by Papagiannaki et al. (2015). The authors observed

that most of the flash floods occurrences area associated with maximum accumulated rainfall

of more than 20 mm in 24 h and 3 mm in 10 min, however the number of occurrences

increases significantly above the levels of 60 mm in 24 h and 10 mm in 10 min.

For landslides studies, Peruccacci et al. (2017) build a catalogue of 2309 rainfall

events with landslides in Italy between 1996 and 2014. It was defined national and 26

regional thresholds for environmental subdivisions based on topography, lithology, land use,

land cover, and others. The results showed differences between some of the thresholds,

highlighting, that more rainfall is needed to trigger landslides where the mean annual

precipitation is high than where it is low.

In one of the first studies evaluating the satellite data to determine rainfall thresholds,

Rossi et al. (2017) determined rainfall thresholds in the Umbria region in central Italy. The

authors observed that the rainfall thresholds obtained from satellite data are lower than those

29

obtained from rain gauge measurements, which converges with the literature, where satellite

rainfall data underestimate the rainfall registered by rain gauges.

Brunetti et al. (2018) evaluated the capability of different rainfall products to forecast

the spatial-temporal occurrence of rainfall-induced landslides using rainfall thresholds.

Results showed that satellites products underestimated rainfall with respect to ground

observations. However, by adjusting the rainfall thresholds, satellite products are able to

identify landslide occurrence, even though with less accuracy than ground-based rainfall

observations.

Muntohar et al. (2021) developed a landslide early warning system based on the

satellite-based TRMM in Indonesia. The threshold performance was evaluated by seven

statistics indices. The results showed a good accuracy rate, even though it still has a fairly

error rate that should be further investigated. Thus, it can be implemented in a landslide early

warning system by the government authority.

30

3 STUDY AREA CHARACTERISTICS

This study was carried out in São Paulo State, located in the Brazilian Southeast

region with an area of 248,200 km2 between 19°55'58''S-25°00'53''S and 50°32'15''W-

47°55'36''W (Figure 5). The state is highly urbanised with approximately 45.5 M inhabitants,

reaching a level of urbanisation of 95% (IBGE 2018). The study area is divided into two

zones with different physical characteristics: 1) the coastal zone which has an altitude lower

than 300 m and 2) the plateau zone which comprises most of the area of the state with

elevation ranging from 300 to 900 m. This topographical characteristic is an important

natural factor in explaining the climate of the state of São Paulo (Setzer 1946). The coastal

zone is dominated by the humid tropical climate with a mean annual temperature above 22

°C and average annual rainfall above 2,000 mm. Meanwhile, the plateau zone is mainly

characterised by the humid subtropical climate with an annual average temperature of 20 °C

and average annual rainfall equal to 1,400 mm year-1 (Alvares et al. 2013). The rainfall in

both regions of the state is more concentrated during the austral summer, i.e., between

October and March. Generally, April and September are the driest months in São Paulo State

(Figure 4). Approximately 70% of the study area is composed of Devonian-Cretaceous

deposits of the Paraná and Bauru basins, while the remaining 30% mainly corresponds to a

crystalline basement with rocks older than the Neoproterozoic Era (Garcia et al. 2018). Other

sedimentary deposits (e.g., intercontinental, and coastal Cenozoic basins) also compose the

geology of the São Paulo State but at a small proportion.

**Figure 4 –** Long-term (1950–1990) mean monthly rainfall for the coastal and plateau zonesobtained from the meteorological stations used by Alvares et al. (2013).

31

**Figure 5 –** (a) Map of Brazil showing the São Paulo State. (b) Rain gauges and Köppen’sclassification map for São Paulo State according to Alvares et al. (2013). (c) Elevation of the São

Paulo State and location of the 347 flood occurrences. (d) Demographic density of São Paulo and location of the 71 flash flood occurrences. (e) Long-term (1950-1990) mean annual rainfall

obtained from the meteorological stations used by Alvares et al. (2013). (f) Landsat-based land use and land cover map for 2017 provided by the MapBiomas Project (Souza et al. 2020).

32

São Paulo State is a typical hotspot frequented by landslides and floods arising from

prolonged or intense rainfall events (Figure 6). The occurrences of these disasters are due to

the natural characteristics of the region associated with the high level of urbanisation

(Tominaga et al. 2015). From 2000 to 2015, there have been more than 10,800 natural

disasters recorded, causing 534 deaths and affecting approximately 971,500 people and

128,500 buildings. Out of all natural disasters recorded in São Paulo, more than 50% were

caused by sudden and violent changes in the distribution or movement patterns of water

(Brollo and Ferreira 2016). Moreover, São Paulo is the richest state in Brazil, with the largest

number of floods and flash floods records as well as sub-daily rainfall data made available

by public agencies.

| Flash Flood in Rio da Prata – Jaguariúna | Flood in Capivarí – SP |
| --- | --- |
| Flood in Franco da Rocha – SP | Landslide in Diadema – SP |

**Figure 6 –** Hydrological disaster in São Paulo (Courtesy: CEPED 2013)

33

4 IMPROVED RAINFALL-THRESHOLD APPROACH

4.1 Contextualization

Among the empirical methods, the rainfall-threshold method is one of the most

widely used for predicting and warning some of the hydrological disasters (Huang et al.

2015), where the thresholds are determined by the properties derived from rainfall events

such as intensity, duration, and antecedent precipitation (e.g., Glade et al. 2000; Aleotti 2004;

Berti et al. 2012; Papagiannaki et al. 2015; Scheevel et al. 2017; Brunetti et al. 2018; Mirus

et al. 2018). In the area of flood warning, Diakakis (2012) used rainfall intensity-duration

parameters to determine the thresholds after adapting the methodologies proposed by

Cannon et al. (2008) and Guzzetti et al. (2008) for landslides. In his study, two thresholds

(upper and lower) are defined but large uncertainties still exist, mainly manifested by the

considerable number of occurrences and non-occurrences of flooding concentrated in the

region between the two thresholds, which often causes many false alarms. Consequently,

many warning systems are frequently neglected by the community due to the large

uncertainties (Abon et al. 2012). Thus, reducing such uncertainties is crucial to minimise the

costs and improve the decision-making processes (Villarini et al. 2010).

The uncertainties of the rainfall thresholds are inevitable as rainfall is not the only

factor that triggers flooding and flash flooding events (Papagiannaki et al. 2015). The

shortcomings of the intensity-duration thresholds are frequently mentioned in the literature,

although this type of method remains as the mostly widespread in the world (Zhao et al.

2019). For instance, choosing rainfall events with short durations to build the threshold

would exclude the important antecedent wetness information, whereas selecting rainfall

events with long durations can mitigate this but it would also flatten the peak intensity that

otherwise can be the real trigger of floods (Bogaard and Greco 2018). Other methods attempt

to overcome this by using information of antecedent rainfall (e.g., Chleborad et al. 2008; Lee

and Park 2016; Scheevel et al. 2017) or Antecedent Precipitation Index (API) (e.g., Glade et

al. 2000; Mirus et al. 2018; Suribabu and Sujatha 2019; Zhao et al. 2019). The use of API,

in contrast with the use of the antecedent rainfall, allows for the consideration of the loss of

the rainfall over the past days (Suribabu and Sujatha 2019). In addition, some other studies

also provided a quantitative assessment of the rainfall threshold approaches for landslides

occurrences by applying probability-based methods (Berti et al. 2012). These probability-

based methods allow the definition of multiple rainfall thresholds based on different

34

exceedance probability levels, which makes possible the establishment of various warning

levels (Brunetti et al. 2010; Huang et al. 2015).

Still, when compared with the applications in predicting landslides, the number of

studies using rainfall thresholds for flood and flash floods warning systems remain low and

the area has been poorly explored. It is also clear that reducing the uncertainties in such

applications is crucial for the effective issuance of flood warnings. The present chapter of

the thesis aims to create a rainfall threshold estimation approach for the robust prediction

and warning of floods and flash floods hazards, as previously presented in the section 1.2 of

this document. The flood and flash flood warning system proposed in this first study intends

to reduce the uncertainties and minimise false alarms observed in the region between the

upper and lower thresholds by introducing an intermediate threshold derived by assessing

the different interactions between the rainfall peak intensity and API, considering different

evaluation metrics. Moreover, the novel inclusion of two tolerance levels in the upper and

lower regions of the threshold intends to enable a more fine-tuned flood warning level

setting.

4.2 Materials and methods

This study used a series of steps to create a robust rainfall threshold able to reduce

the uncertainties of events triggering floods occurrences, as shown in Figure 7. Overall, the

implementation of the proposed rainfall threshold approach includes: a) the selection of

events, b) the application of rainfall intensity-duration parameters to define thresholds, c)

the adoption of tolerance levels to improve the rainfall intensity threshold, and d) the

implementation of an intermediate threshold relating rainfall peak intensity and API to better

separate the flood and flash flood occurrences from the non-occurrences. These

methodological steps are described in detail in the next items of this section.

35

**Figure 7** – Methodological chart, showing (a) the raw and selected flood and flash floodoccurrences; (b) the rainfall intensity threshold approach; (c) the tolerance levels adopted to

improve the rainfall intensity threshold; and (d) the improved threshold relating rainfall peak intensity and antecedent precipitation index (API).

4.2.1 Selection of events

4.2.1.1 Rainfall data

Rainfall data over the period of 1 January 2015 - 31 December 2017 were collected

from the 732 rain gauges distributed throughout the São Paulo State. The rain gauges belong

to the Brazilian National Centre for Monitoring Early Warning of Natural Disasters

(CEMADEN, acronym in Portuguese), a national-wide network established by the Brazilian

Government supporting the natural disasters risk management (Bacelar et al. 2020). The

ground-based rainfall observation network of CEMADEN is equipped with tipping bucket

gauges with a 10-min temporal resolution when it rains and 60-min temporal resolution over

no-rain periods. These rainfall data were screened before use in this study. The quality-

control procedure is as follows: first, a computational routine was created to select only rain

gauges with less than 30-days of missing data along each of the three civil years considered

in this study; then, all rain gauges meeting this first requirement were visually inspected

using two standard methods, including: 1) a comparison of monthly and sub-daily rainfall

data of the five nearest stations was carried out to verify large discrepancies between them;

36

and 2) an analysis of the range of values and changes over subsequent measurements of each

rain gauge to identify constant or null rainfall records that probably indicate gauge clogging.

This resulted in the final 590 gauges that were selected for the whole study period (Figure

5b). These data were then used to define the rainfall events and to calculate their respective

thresholds. It is worth noting that not all 590 gauges were used for every year because of the

quality-check procedures adopted in this study; instead: 1) 216 rain gauges with high-quality

data in 2015, 2) 315 rain gauges with high-quality data in 2016, and 3) 355 rain gauges with

high-quality data in 2017.

Most rain gauges used to calculate the rainfall thresholds are located within the

metropolitan regions of the São Paulo State, including: 1) the Metropolitan Area of São

Paulo (MASP), with an estimated density of 7,689 inhabitants/km2 and covered by 42 rain

gauges, 2) the Metropolitan Area of Ubatuba (MAU), with an estimated density of 121

inhabitants/km2 and covered by 18 rain gauges, and 3) the Metropolitan Area of Santo André

(MASA), with an estimated density of 3,919 inhabitants/km2 and covered by 17 rain gauges.

4.2.1.2 Flood and flash flood data

Detailed information of flood and flash flood occurrences are fundamental for the

analysis of their relationship with rainfall events. In this study, flood occurrences were

considered as the overflow of water from a stream channel onto normally dry land in the

floodplain, whereas flash flood occurrences were regarded as a rapid inland flood due to

intense rainfall or a sudden flooding with short duration (Guha-Sapir et al. 2015). The

inventory of these occurrences, which comprise the same period of the rainfall data, was

obtained from three main sources: 1) The Integrated Storm Monitoring, Forecasting and

Alerting System for the Brazilian South-Southeast Regions (SIMPAT, acronym in

Portuguese), 2) The Civil Defence of the state of São Paulo, and 3) press news. The data

provided by the press news were also used to confirm and differentiate the type of occurrence

(floods or flash floods) by analysing some available information such as pictures, rainfall

duration, and location. In order to choose the most appropriate rain gauges, only those flood

and flash occurrences that could be georeferenced (e.g., via address and coordinates) and

dated were selected. This was followed by the application of two more criteria to further

filter out the events/occurrences that: 1) come with daily rainfall less than 10 mm near to the

flood and flash flood events, or 2) have the nearest rain gauge located more than 20 km from

the occurrence. Although choosing only occurrences distant less than 20 km from the rain

37

gauges as a criterion, almost 72% of the flood and flash flood events were located within 10

km from the stations.

4.2.1.3 Characterisation of rainfall events

In parallel with the selection of the flood and flash flood occurrences, rain gauges were

chosen to define the rainfall events that better characterise the disasters. In this study, the

relationship between rainfall peak intensities and the antecedent wetness conditions was

assessed for the events that might or might not lead to the floods and flash floods. This

assessment was performed to avoid two potential issues: 1) the inadvertent exclusion of

important antecedent wetness information for rainfall events with short duration, and 2) the

flatness of peak intensity for rainfall events with long duration. The procedure is as follows:

first, the rainfall peak intensity for all rain gauges was calculated for each day considering

ten time-steps (10 min, 30 min, 1 h, 2 h, 3 h, 6 h, 8 h, 10 h, 12 h, and 24 h). Thereafter, the

API was tested for different time-steps (1 to 10 days) to estimate the antecedent wetness

conditions for the day before the rainfall event (Kohler and Linsley 1951), as in eq. 1:

ି௜

API = ෍ 𝑃 ି௧ ௧ 𝑘 (1)

௧ୀିଵ

where _𝑖_ is the number of antecedent days considered in the study, _𝑃௧_ is the rainfall for the

day _𝑡_ (mm), and _𝑘_ is a decay rate that ranges from 0.80 to 0.98 according to Viessman and

Lewis (1996). The values of API chosen in this study are within the ranging established by

some well-recognised methods such as the Natural Resources Conservation Service (NRCS)

method that uses 5 days of antecedent moisture condition (NRCS 1972). Some other studies

also suggest values of API ranging from 2 to 6 days to characterise flooding (e.g., Tramblay

et al. 2012; Froidevaux et al. 2015).

The selection of the rainfall events that better characterise the flood and flash

occurrences followed largely the methodology proposed by Rossi et al. (2017), i.e., only

those rainfall events with gauges having observed the most critical rainfall for the days of

occurrences and situated within 20 km distance from the location where the floods or flash

floods occur were selected; whereas the other rainfall events were treated as non-

occurrences.

38

4.2.2 Improvements of the rainfall threshold

4.2.2.1 Definition of the rainfall peak intensity-duration threshold

The most representative peak of rainfall intensity was obtained by plotting peak

rainfall intensities of various time intervals against their respective durations. The objective

of this first step is to distinguish two clear thresholds (lower and upper) that divide the graph

into three parts and four distinct groups: 1) the upper part (Group 1), which corresponds with

the peak intensities that always lead to flooding or flash flooding occurrences; 2) the middle

part, which contains peak intensities that may (Group 2) or may not (Group 3) lead to

flooding or flash flooding events; and 3) the lower part (Group 4), which includes peak

intensity values that do not lead to flooding or flash flooding. Accordingly, an analysis of

the graph based on the following four criteria was also performed in this study to define the

time interval of the peak rainfall intensity that better represents the flood and flash flood

occurrences: 1) a higher number of occurrences above the upper threshold, 2) a higher

number of non-occurrences below the lower threshold, 3) lower amplitude between the upper

and lower thresholds, and 4) values of the metrics presented in section 4.2.3.

4.2.2.2 Application of tolerance levels

Some studies complemented the rainfall threshold method with probabilities of

occurrence to reduce the uncertainties of false alarms for hydrological disasters (e.g., Berti

et al. 2012; Huang et al. 2015; Wu et al. 2015; Santos and Fragoso 2016; Brigandì et al.

2017). Aiming to reduce the uncertainties in the middle part of the graph but without losing

the characteristics of Group 1 and Group 4, two levels of tolerance (sometimes mentioned

as exceedance probability) were used in this study to minimise the amplitude between the

upper and lower thresholds, e.g.: 1) a new lower threshold defined as the 5% of the

occurrences above the lower threshold where the value 5% has also been adopted for

landslide studies (Peruccacci et al. 2009, 2012, 2017; Brunetti et al. 2010; Rossi et al. 2017);

and 2) a new upper threshold defined as the 99th percentile of non-occurrences above the

lower threshold. The first tolerance level leaves 5% of the empirical data points below the

lower threshold, while the second tolerance level was adopted to leave a minimum number

of the non-occurrences above the upper threshold.

39

4.2.2.3 Delineating the intermediate threshold

Afterwards, the API was used to analyse the occurrences and non-occurrences of the

middle part of the graph after considering the two tolerance levels. The upper and lower parts

of the graph were excluded from this further analysis because it is presumed that they are

already well-represented by the intensity peaks. Some studies show generally a negative

relationship between the antecedent conditions and a critical event rainfall, indicating that

with increasingly wet conditions, less rainfall is required to trigger an occurrence (Bai et al.

2014). In this study, the middle part was outlined following the study carried out by Collins

et al. (2007) for landslides, which relates rainfall intensity and API by an exponential

equation to better identify occurrences and non-occurrences of events at this part of the

graph, as follows:

𝐼 = 𝑎 𝑒௕ ୅୔୍ + 𝑐 (2)

where _𝐼_ is the peak intensity (mm h⁻¹), and _𝑎_, _𝑏_, and _𝑐_ are constants to be determined. The

constant values were obtained by 50,000 iterations, combining: 1) 50 values of ‘_𝑎_’ ranging

from the minimum rainfall intensity to three times the maximum rainfall intensity of the

occurrences; 2) 20 values of ‘_𝑏_’ varying between -0.01 and -1; and 3) 50 values of ‘_𝑐_’ ranging

from the minimum rainfall intensity to the mean rainfall intensity of the occurrences. The

best-fitted constants and the reference day for the API calculation were selected based on

the optimal values of the metrics presented in section 4.2.3.

4.2.3 Evaluation procedures

The performance of the upper, intermediate and lower thresholds to identify true or

false alarms was evaluated using a binary classifier of the rainfall conditions that do or do

not lead to flood and flash flood occurrences (Segoni et al. 2014; Turkington et al. 2014;

Zhao et al. 2019). A contingency matrix consisting of four components was used for each

threshold, including: 1) true positive (TP), when the threshold is exceeded and the

hydrological disaster occurs; 2) false negative (FN), when the threshold is not exceeded and

the hydrological disaster occurs; 3) false positive (FP), when the threshold is exceeded and

the hydrological disaster does not occur; and 4) true negative (TN), when the threshold is

not exceeded and the hydrological disaster does not occur. Three metrics were then applied

40

using the contingency matrix to assess the skill score of the flood and flash flood thresholds:

1) probability of detection (POD), which measures the fraction of events that are correctly
predicted; 2) false alarm ratio (FAR), which exhibits the fraction of events incorrectly

predicted; and 3) positive predictive value (PPV), which shows the probability of events

correctly predicted:

| POD = TP + FN TP | (3) |
| --- | --- |
| FAR = FP + TN FP | (4) |
| PPV = TP + FP TP | (5) |

The values of these metrics range from 0% to 100%. The optimal score for POD and

PPV is close to 100%, while the perfect value for FAR is close to 0%.

4.2.4 Link to the colour-class warning level systems

In Brazil, national and regional disaster management agencies such as CEMADEN

usually use colour-class systems to indicate different levels of risk (e.g., moderate, high, and

very high). These systems generally employ classes varying from cold to warm colours to

show conditions that could lead to increased risk. Similar risk information, using this colour-

class system designed from multiple rainfall thresholds to link threat levels to the emergency,

is also used by many disaster management agencies worldwide and scientific studies (e.g.,

Brunetti et al. 2010; Huang et al. 2015; Jang 2015). Based on this information, the definition

of four thresholds using the methodology proposed in this study makes it possible for the

implementation of probabilistic schemes for warning level systems predicting flood and

flash flood occurrences, defined as follows:

1. Blue alert: rainfall events below the lower threshold that represent a low
probability of occurrences when the rainfall conditions are maintained.

2. Yellow alert: rainfall events between the lower and the intermediate thresholds
that represent a moderated probability of occurrences when the rainfall conditions

are maintained.

41

3. Orange alert: rainfall events between the intermediate and the upper threshold that
represent a high probability of occurrences when the rainfall conditions are

maintained.

4. Red alert: rainfall events above the upper threshold that represent an extremely
high probability of occurrences when the rainfall conditions are maintained.

4.3 Results and discussion

4.3.1 Characterisation of the flood and flash flood occurrences

Figure 5c & Figure 5d show the spatial distribution of the 347 and 71 occurrences of

flood and flash floods, respectively, in the state of São Paulo between 1 January 2015 and

31 December 2017. Represented by separated points in the map, these occurrences were

obtained from the three main sources of data described in section 4.2.1.2. The main source

of occurrences was acquired from the SIMPAT dataset, with 284 (82% of the total) floods

and 58 (82% of the total) flash floods. The spatial distribution of information, collected from

the different data sources, shows that a large number of floods (59%) and flash floods (55%)

were concentrated in areas with population density higher than 500 inhabitants/km2, which

includes only 59 of the 645 municipalities of São Paulo State. The largest number of floods

were identified in MASP (45), Bauru (12), and Sorocaba (9). On the other hand, the number

of observed flash floods was higher in Bauru (8), São Paulo (6), and Campinas (5). The 240

floods and 47 flash floods occurrences considered in this study were mostly triggered during

the rainy season (January – March), which represents 69% and 66% of the total, respectively.

According to SIMPAT, the number of socio-economic impacts caused by the floods and

flash floods in São Paulo State during the studied period amount to more than 4,310

displacements, 26 injuries, and 17 deaths.

4.3.2 Rainfall peak intensity-duration threshold

The results of the rainfall thresholds for floods and flash floods, without the use of

tolerance levels, are shown in Figure 8a & Figure 8b. The thresholds of the upper part of the

graph for floods range from 171.6 to 4.2 mm h-1 for the rainfall durations of 10 min and 24

h, respectively. The thresholds of the lower part of the graph for floods range from 4.7 to 1.1

mm h-1 for the same durations, respectively. As far as flash floods are concerned (Figure 8b),

42

the thresholds of the upper part of the graph presented similar values when compared to

floods (between 170.4 and 4.3 mm h-1). Conversely, the lower part exhibited values of

intensity peaks six times higher (25.2 mm h-1) for shorter time-steps.

**Figure 8 –** Rainfall intensities peak versus rainfall duration applying the approach without thetolerance levels for (a) floods and (b) flash floods. Improved application of the methodology using

the tolerance levels (99th percentile and 5%) for (c) floods and (d) flash floods. The graphs use logarithmic scale.

It is noticeable that the peak rainfall intensity for longer durations (24 h) presents a

better relationship with the eventual flood events, where the upper and lower lines of the

threshold tend to be closer. Consequently, the largest number of flood occurrences and non-

occurrences was registered above (below) the upper (lower) thresholds, respectively. Thus,

43

a reduced quantity of events in the middle part of the graph, containing both occurrences and

non-occurrences, was also observed. This finding differs from the study carried out by

Diakakis (2012) in Greece, which found a better relationship for shorter peak intensity

duration due to the upper and lower thresholds being much closer in 10 or 30 min durations

than in 24 hours. On the other hand, the amplitude of the middle part of the graph (the

distance between the two thresholds) was similar for all time-steps when flash floods were

considered. However, the largest number of occurrences/non-occurrences above (below) the

upper (lower) thresholds was noticed for the time-steps of 1 and 2 h. Papagiannaki et al.

(2015) also observed a better separation between flash floods occurrences and non-

occurrences in Greece for shorter peak intensity durations, however only when the analysis

is performed on a more local scale.

Table 3 shows the evaluation metrics for predicting floods and flash floods using the

two thresholds but without adding of the tolerance levels. It is noticeable that the upper

threshold is a precise approach for predicting flood and flash flood occurrences, presenting

FAR and PPV values equal to 0% and 100% for all time steps, respectively. However, the

upper threshold is only applicable to a very limited number of occurrences, since the POD

for this threshold presented low values for floods (from 1 to 17%) and flash floods (from 3

to 15%) for all time steps. The lower threshold exhibits high and low values of FAR (from

15 to 93%) and PPV (from 9 to 19%) for floods, respectively. For flash floods, reduced

values of FAR (from 12 to 19%) and PPV (from 4 to 7%) are found for the lower threshold

when compared to those observed for floods. These results show that the application of the

rainfall peak intensity-duration threshold presents a high number of non-occurrences above

the lower threshold, albeit displaying POD values equal to 100% for both type of floods.

This behavior suggests that the approach can detect most occurrences only above the lower

threshold, but with a considered level of false alarms regardless of the time-step adopted.

Similar performance has also been observed in the application of rainfall intensity-duration

thresholds for floods and landslides worldwide (e.g., Santos and Fragoso 2016; Brunetti et

al. 2018; Zhao et al. 2019). For both upper and lower thresholds, the rainfall peak intensity-

duration threshold without the use of tolerance levels presented better results for time steps

equal to 1 and 24 h for flash floods and floods, respectively.

44

**Table 3 –** Summary of evaluation metrics for the flood and flash flood thresholds, considering theapproach without the use of tolerance levels.

Metrics Peak Intensities (h)

1/6 1/2 1 2 3 6 8 10 12 24

_POD_ 1% 7% 4% 7% 8% 12% 12% 13% 14% 17%_Upper_

_FAR_ 0% 0% 0% 0% 0% 0% 0% 0% 0% 0%_threshold_

_Flood PPV_ 100% 100% 100% 100% 100% 100% 100% 100% 100% 100%

**POD** 100% 100% 100% 100% 100% 100% 100% 100% 100% 100%**Lower**

_FAR_ 93% 83% 72% 48% 41% 24% 26% 20% 20% 15%_threshold_

**PPV** 4% 4% 5% 7% 8% 13% 12% 15% 15% 19%

_POD_ 3% 3% 14% 15% 11% 10% 7% 7% 8% 13%_Upper_

_FAR_ 0% 0% 0% 0% 0% 0% 0% 0% 0% 0%_threshold_

**PPV** 100% 100% 100% 100% 100% 100% 100% 100% 100% 100%

**POD** 100% 100% 100% 100% 100% 100% 100% 100% 100% 100%**Lower**

_Flash Flood FAR_ 19% 13% 13% 15% 17% 12% 13% 13% 13% 13%_threshold_

_PPV_ 4% 7% 6% 6% 5% 7% 7% 7% 6% 7%

4.3.3 Tolerance levels

Figure 8c & Figure 8d show the rainfall thresholds for floods and flash floods after

introducing the tolerance levels of 99th percentile for the non-occurrences below the upper

and 5% of the occurrences above the lower thresholds. The two tolerance levels were defined

to seek to reduce the uncertainties of the middle part of the graph. The application of the

tolerance level of 99th percentile corresponded to a mean inclusion of 11 and 6 non-

occurrence events of floods and flash floods above the upper threshold, respectively.

However, it also brings in an increase of 14% of the number of floods and flash floods

occurrences above the upper threshold. For the tolerance level at 5% percentile, the number

of occurrences included below the lower threshold was 17 and 4 for floods and flash floods,

respectively. However, it was also observed a considerable reduction in the number of non-

occurrences of floods (63%) and flash floods (53%) in the middle part of the graph.

Similarly, the study carried out by Brunetti et al. (2018) also presented a significant reduction

(68%) in the number of non-occurrences for landslides above the threshold after the use of

the same tolerance level. However, it is worth highlighting that, in our study, without these

tolerance levels, the inclusion of occurrences/non-occurrences in the lower/upper threshold

was zero.

It is observed that there is a noticeable decline of the amplitudes between the lower

and upper thresholds when floods are considered using the tolerance levels, mainly for the

45

time-steps ranging from 10 min to 2 h (Figure 8c). This reduction of the amplitude between

the two thresholds predominantly occurred because of the significant rising of the lower

threshold. This leads to the fact that approximately half of the non-occurrences above the

lower threshold are excluded and in the meantime the number of flood occurrences above

upper thresholds are included, respectively. As far as flash floods are concerned, the largest

variations of the lower threshold using the tolerance levels mainly occur between the time-

steps 1 and 3 h, excluding more than half of the non-occurrences above the originally defined

lower threshold (Figure 8b & Figure 8d). Conversely, the upper threshold for flash floods

remained practically unchanged. Table 4 shows the assertiveness of the rainfall thresholds

for floods and flash floods after the use of the two tolerance levels. The results reveal a

considerable improvement of POD for the upper threshold applying the tolerance level of

99th percentile for the non-occurrences, ranging now from 8 to 31% for floods and from 4 to

32% for flash floods. These outcomes obtained for POD correspond to an improvement of

14% for floods and flash flood compared to those acquired by the application of this

methodology without the use of the proposed tolerance levels, while the FAR values

remained negligible for all time-steps.

Table 4 – Summary of evaluation metrics for the floods and flash floods thresholds considering the tolerance levels (99th percentile and 5%) and the intermediate thresholds.

Metrics Peak Intensities (h)

1/6 1/2 1 2 3 6 8 10 12 24

_Upper POD_ 8% 13% 20% 24% 27% 27% 31% 31% 29% 31%

_threshold FAR_ 0% 0% 0% 0% 0% 0% 0% 0% 0% 0%

th

_Flood(99 ) PPV_ 82% 87% 91% 92% 93% 93% 94% 94% 94% 94%

_Lower POD_ 95% 95% 95% 96% 95% 95% 95% 95% 95% 95%

_threshold FAR_ 31% 18% 14% 12% 9% 8% 7% 6% 5% 6%

| (5%) | PPV 10% 16% 19% 22% 26% 29% 32% 35% 38% 34% |
| --- | --- |
| Upper | POD 4% 15% 27% 32% 30% 23% 25% 24% 25% 28% |

_threshold FAR_ 0% 0% 0% 0% 0% 0% 0% 0% 0% 0%

| (99 th ) | PPV 38% 69% 79% 82% 81% 76% 78% 77% 78% 80% |
| --- | --- |
| Lower | POD 96% 97% 96% 96% 96% 97% 96% 96% 96% 96% |

Flash FloodThreshold FAR **15% 8% 5% 4% 4% 6% 6% 6% 6% 7%**

_(5%) PPV_ 5% 10% 15% 18% 16% 13% 13% 13% 12% 11%

Overall, the PPV values after the use of the tolerance level of 1% for the upper

threshold presented a slight decreasing about 9% for floods and 26% flash floods, presenting

46

now variations above 80% and 70% for almost all intensity peaks, respectively. This fact

represents a slight loss in the predictive capacity of the threshold using the tolerance level,

however, a higher number of occurrences can be found. Thus, the upper threshold with the

application of the tolerance level of 1% remains a robust approach for predicting the

occurrences. Like the methodology without the application of the tolerance levels, the

optimal scores of the metrics for floods and flash floods were observed for longer (8 h) and

shorter (2 h) time-steps, respectively.

The lower threshold applying the tolerance level of 5% for the flood occurrences

resulted in an increase of 16% of the PPV (now ranging from 10 to 38%) and a reduction of

32% of the FAR (now ranging from 5 to 31%), when compared to the approaches without

the tolerance level (Table 4). Similar increases can be observed for flash floods, with

improvements of 6 and 7% for PPV and FAR rates after adopting this tolerance level,

respectively. The better performance of PPV and FAR noticed for floods applying the

tolerance level for the lower threshold mainly occurred because: 1) the lower values of

rainfall peak intensities observed for its outbreak, and 2) the higher number of flood records

included in the lower threshold (17 floods against 4 flash floods). The values of POD equal

to ~95% for both floods and flash floods also indicate that almost all occurrences remain

represented for all time-steps after the use of the tolerance level for the lower threshold.

4.3.4 Intermediate threshold

This section analyses the use of an exponential equation relating rainfall intensity

and API for improving the separation between occurrences and non-occurrences of the

intermediate threshold, which represents the main contribution of this study. Figure 9 &

Figure 10 show the results of the application of this methodology for floods and flash floods,

respectively. It is noticeable that for floods the curves were more influenced by the API for

shorter time-steps, especially for those equal to 10 min, 1 h, and 3 h. Accordingly, the curves

for floods remained barely influenced by the API for time-steps equal to 2 and 8 h. For flash

floods, the curves presented good sensitivity for almost all time-steps, except for 1 h. In

general, the intensities for floods and flash floods tended to be constant and not dependent

to API for durations higher than 1 h.

47

**Figure 9 –** Peak rainfall intensity versus Antecedent Precipitation Index (API) graphs for eachtime-step and delimitation of the exponential curves for warning level systems applied for floods.

48

**Figure 10 –** Peak rainfall intensity versus Antecedent Precipitation Index (API) graphs for eachtime-step and delimitation of the exponential curves for warning level systems applied for flash

floods.

49

Overall, the curves generated by the exponential equations well-characterise the

intermediate threshold, where the occurrences and non-occurrences can be obtained

correlating rainfall intensity and API. The proposed methodology better includes the

occurrences and excludes the non-occurrences for rainfall events with higher and lower

values of API, respectively. Moreover, adoption of the exponential curves can help regions

with a moderate probability of occurrences (yellow alert) based on limit values of API,

regardless of the rainfall intensity (e.g., peak intensities of 1 to 8 hours for flash floods in

Figure 10). Also, the exponential curves can determine a region capable of triggering

occurrences with low values of API and intensity (e.g., peak intensity of 2 hours for flood in

Figure 9).

The application of this approach for floods and flash floods, using an exponential

equation for better separating the occurrences from the non-occurrences, presented

considerably improved results for almost all analysed metrics and nearly all time-steps

considered (Table 5). The most representative result for floods was observed for longer time-

steps, especially for 8 h. Specifically for this time step of 8 h, the POD, FAR and PPV metrics

presented values equal to 81%, 1% and 82%, respectively. Meanwhile, the time steps ranging

from 1 h to 12 h presented similar results for flash floods, highlighting the time steps equal

to 2 (POD = 79%, FAR = 1%, and PPV = 43%) and 6 h (POD = 79%, FAR = 1%, and PPV

= 44%) which presented the best metrics. Indeed, the use of methodologies considering the

API to delineate thresholds has proven to be an outstanding instrument for flood and flash

flood hazard predictions and warning systems.

Table 5 – Summary of evaluation metrics for flood and flash flood occurrences applying the improved thresholds that use rainfall intensities and Antecedent Precipitation Index (API).

Intensities (h) Floods Intensities (h) Flash Floods X Metrics X Metrics

| API (day) 1/6 x 1 | POD 77% FAR 6% PPV 30% | API (day) 1/6 x 7 | POD 85% FAR 3% PPV 21% |
| --- | --- | --- | --- |
| 1/2 x 1 1 x 1 | 78% 75% 4% 3% 41% 48% | 1/2 x 3 1 x 6 | 82% 79% 1% 1% 33% 40% |
| 2 x 6 3 x 7 | 83% 82% 3% 2% 51% 57% | 2 x 6 3 x 7 | 79% 80% 1% 1% 43% 39% |
| 6 x N/A 8 x 8 | 83% 81% 2% 1% 61% 82% | 8 x 7 6 x 7 | 79% 79% 1% 1% 44% 41% |
| 12 x 9 10 x 9 | 80% 79% 1% 1% 66% 66% | 12 x 8 10 x 7 | 80% 82% 1% 1% 39% 39% |
| 24 x 9 | 78% 1% 66% | 24 x 7 | 85% 1% 37% |

50

5 CHARACTERIZATION OF EXTREME EVENTS AND DELINEATION OF

RAINFALL THRESHOLDS BY SATELLITE-BASED PRECIPITATION

PRODUCTS

During the last decades, several studies have assessed the accuracy of one or a set of

satellite-based rainfall data at various spatial and temporal scales, most of which using

independent gauge or radar observations (Tan and Duan 2017; Gadelha et al. 2018; Wang et

al. 2018; Beck et al. 2019a). Some of these studies evaluated the performance of the satellite-

based rainfall products regionally or globally for hydrological applications, such as water

resources management (Ranghetti et al. 2018; Sheffield et al. 2018), groundwater storage

and depletion (Vasco et al. 2019; Singh and Saravanan 2020), hazard monitoring (Pandey

and Srivastava 2019; Parker et al. 2021), and stream flow modelling (Su et al. 2019; Kha et

al. 2020). However, applications of satellite-based rainfall data for hydrological disasters

warning purposes through the use of empirical methods have been scarce, mainly, because:

1) the bias in near real-time rainfall estimates, 2) the latency of products, and 3) insufficient
spatial and temporal resolutions (AghaKouchak et al. 2015; Brocca et al. 2017). Based on a

literature review, we identified that only a few studies evaluated the capability of the satellite

gridded rainfall datasets in detect landslide events with the use of empirical rainfall

thresholds (e.g., Nanda Pratama et al. 2017; Brunetti et al. 2018, 2021; Monsieurs et al. 2019;

Chikalamo et al. 2020; He et al. 2020), with no similar analysis for flood events, especially

over large areas. A study carried out by Brunetti et al. (2018), for instance, showed that the

four analysed precipitation satellite-based products were able to identify landslides

occurrences in Italy by adjusting the rainfall thresholds, but with less accuracy than ground-

based rainfall observations. More recently, a study performed by Brunetti et al. (2021) in

India, also using empirical rainfall thresholds derived from the analysis of historical

landslide events, found that the two analysed satellite-based rainfall products outperformed

the ground observations thanks to their better spatial and temporal resolutions.

Clearly, satellite-based data are an important data source for improving the spatial

representativeness of rainfall-threshold approaches and, consequently, providing tools to

create more robust warning systems for flood occurrences, especially in many parts of the

world with low-density sub-daily rain gauge networks. Therefore, we commissioned this

study to addresses the following scientific questions: (a) How do the currently available

rainfall satellite-based products perform for flood events detection? (b) Which satellite-

based product performs better in defining empirical rainfall-threshold methods for floods?

51

The main aims of this study are: (i) to assess the quality of satellite-based

precipitation products for identifying extreme rainfall events able to produce flood events,

and (ii) to evaluate the use of satellite-based precipitation products to create rainfall

thresholds for flood hazards. To achieve the proposed objectives, we used detailed

information on flood occurrences available for the São Paulo State in Brazil for a period of

five years (2015-2019). In addition, we used ground-based sub-daily rainfall dataset obtained

from a network of around 730 rain gauges and 14 satellite-based precipitation products with

different temporal and spatial resolutions. This study is intended then to provide a valuable

tool for flood warning systems using satellite-based rainfall products in tropical regions.

5.1 Materials and methods

5.1.1 Satellite-based rainfall products

The performance of the 14 (sub-) daily satellite-based rainfall products were

evaluated in this study based on a point-to-cell analysis comparison between these estimated

datasets and the rain gauges. Table 6 provides an objective-focused tabular information of

all estimated rainfall datasets considered in this evaluation. All analysed products are global

or quasi-global, with data available to cover the entire study period, except the

GPM+SM2RAIN that provides rainfall data only until 2018. The spatial resolution of the

evaluated rainfall products ranges from 0.04º to 0.5º, while the temporal resolution varies

between 30-min and daily. Among the 14 rainfall products, eight of them are fully based on

satellite data (hereafter referred to as the uncorrected products, which includes CHIRP V2.0,

IMERG E, IMERG-L, PDIR-Now, PERSIANN, PERSIANN-CCS, SM2RAIN-ASCAT

V1.2, and GPM+SM2RAIN) and six products combine gauge and satellite data (hereafter

corrected products, which includes CMORPH-CRT V1.0, IMERG F, PERSIANN-CDR

V1R1, CHIRPS V2.0, MERRA-2, and MSWEP V2.2). Some of them also use (re)analysis

data to generate the products (e.g., CHIRP V2.0, CHIRPS V2.0, MERRA-2, and MSWEP

V2.2). A rainfall depth threshold of 0.1 mm day-¹ was established to define rain/no-rain and

to exclude daily events deemed insignificant, following Li and Liu (2020).

52

**Table 6.** Summary of 14 precipitation estimates products evaluated in this study, similar to as presented by Beck et al. (2019).

Spatial Temporal Temporal Name Description Spatial resolution Reference Coverage Resolution Coverage

Climate Hazards group InfraRed

CHIRP V2.0 Precipitation (CHIRP) V2.0 0.05º 50º/S Daily 1981- present Funk et al. 2015

Climate Hazards group InfraRed CHIRPS V2.0 Precipitation with Stations (CHIRPS) 0.05º 50º N/S Daily 1981- present Funk et al. 2015

V2.0

CPC MORPHing technique (CMORPH) Joyce et al. 2004; CMORPH-CRT V1.0 bias corrected (CRT) V1.0 0.07º 60º N/S 30 min 1998-2019 Xie et al. 2017

Precipitation Estimation from Remotely Sensed Information using Artificial Neural

PDIR-Now Networks - Dynamic Infrared Rain Rate 0.04º 60º N/S Hourly 2000- present Nguyen et al. 2020 near real-time (PDIR-Now)

Integrated Multi-satellitE Retrievals for

IMERG-E V06 GPM (IMERG) early run V06 0.1º 60º N/S 30 min 2000- present Huffman et al. 2019

Integrated Multi-satellitE Retrievals for

IMERG-L V06 GPM (IMERG) late run V06 0.1º 60º N/S 30 min 2000- present Huffman et al. 2019

Integrated Multi-satellitE Retrievals for

IMERG-F V06 GPM (IMERG) final run V06 0.1º 60º N/S 30 min 2000- present Huffman et al. 2019

Modern-Era Retrospective Analysis for

| MERRA-2 | Research and Applications 2 | ~0.5º | Global | Hourly | 1980- present | Gelaro et al. 2017 |
| --- | --- | --- | --- | --- | --- | --- |
| MSWEP V2.2 | Multi-Source Weighted-Ensemble Precipitation (MSWEP) V2.2 | 0.1º | Global | 3-hourly | 1979- present | Beck et al. 2017a, 2019b |

Precipitation Estimation from Remotely Sorooshian et al. PERSIANN Sensed Information using Artificial Neural 0.25º 60º N/S Hourly 2000- present

Networks (PERSIANN) 2000 Precipitation Estimation from Remotely

Sensed Information using Artificial Neural

PERSIANN-CCS Networks (PERSIANN) Cloud 0.04º 60º N/S Hourly 2003-Present Hong et al. 2004 Classification System (CCS)

Precipitation Estimation from Remotely PERSIANN-CDR Sensed Information using Artificial Neural

0.25º 60º N/S Daily Ashouri et al. 2015 1983- present

V1R1 Networks (PERSIANN) Climate Data Record (CDR) V1R1

| SM2RAIN-ASCAT V1.2 | application of the SM2Rain algorithm to Precipitation Estimation from the the ASCAT soil moisture data | 12.5km | Global | Daily | 2007-2019 | Brocca et al. 2019 |
| --- | --- | --- | --- | --- | --- | --- |
| GPM+SM2RAIN | based rainfall estimates derived from three Integration of IMERG-E with SM2RAIN- | 0.25º | 60º N/S | Daily | 2007-2018 | Massari et al. 2020 |

different satellite Soil Moisture products

53

5.1.2 Flood dataset

Detailed and accurate information of floods that occurred between January 2015 to

December 2019 in the São Paulo State was obtained from the following four sources: (1)

The Integrated Storm Monitoring, Forecasting and Alerting System for the Brazilian South-

Southeast Regions (SIMPAT); (2) the Brazilian National Centre for Monitoring Early

Warning of Natural Disasters (CEMADEN); (3) The Civil Defence of São Paulo State; and

(4) press news. The survey encloses detailed information of the disaster classification,

location (address or coordinate), day of occurrence, besides, when possible, the number of

deaths and affected people, and references in the press. Only georeferenced occurrences

(e.g., via address and coordinates) confirmed in at least two of the above-mentioned sources

of data were selected for this study. Moreover, the occurrences with (1) daily rainfall less

than 10 mm registered near to the flood events or (2) the nearest rain gauge located more

than 20 km from the flood events were excluded for further analyses. We identified 762

occurrences of floods in the São Paulo State during the studied period. After the restrictions

mentioned above, a total of 551 occurrences of floods were used for the further analyses.

The mean distance between the occurrences and the nearest rain gauge was ~7 km. Most of

the 211 flood events were excluded for the analyses because the lack of rain gauges distant

less than 20 km from the occurrences. This exclusion is a consequence of the uneven

distribution of rain gauges over the region, which are more concentrated in larger cites.

5.1.3 Observed rainfall dataset

This study began by considering ground-based sub-daily rainfall data from 730

automated rain gauges operated by CEMADEN over the period between January 2015 and

December 2019. CEMADEN has a national-wide ground-based rainfall network consisting

of tipping bucket gauges with a 10-min temporal resolution when it rains and 60-min over

no-rain periods. The observed rainfall data used in this study underwent the same quality

control measure as that used by Freitas et al. (2020) to detect possible rain gauge

inconsistencies and selecting only high-quality data. Therefore, only those rain gauges with

less than 30 days of missing data along each civil year were considered in this study.

Moreover, the gauges that met this criterion were visually inspected as follows: 1) comparing

the monthly and sub-daily rainfall data with the five nearest stations to verify large

discrepancies between them; and 2) analysing the range of values and changes over

subsequent measurements of each rain gauge to identify constant or null rainfall records that

54

probably indicate gauge clogging. After the quality control procedure adopted in this study,

a total of 583 gauges were selected to define the rainfall events and calculate its respective

rainfall thresholds.

5.1.4 Rainfall events and threshold definition

The delineation of the thresholds was based on an empirical model that evaluates the

amounts of precipitation that may or may not lead to flooding events through the analyses

of the exceedance or not of a certain threshold. Six aggregation periods (3 h, 6 h, 12 h, 1 d,

3 d, and 10 d) were considered to determine the accumulated precipitation. For the sub-daily

aggregations, we considered the maximum moving sum of the accumulated precipitation.

The daily precipitation was classified according CEMADEN in light rain (< 10 mm),

moderate rain (≥ 10 mm and < 30 mm), heavy rain (≥ 30 mm and < 70 mm), and severe (≥

70 mm).

The rainfall thresholds were determined for the observed data and each satellite-

based rainfall product separately by applying the adapted empirical methodology used by

Diakakis (2012) and Papagiannaki et al. (2015). Specifically, in this study we used the

accumulated rainfall-duration thresholds for detecting the occurrence of floods, i.e., by

plotting the cumulated rainfall of various time intervals against their respective durations.

An analysis of the graph based on the following three criteria was performed to define the

time interval of the cumulated rainfall that better represents the flood events: (1) the higher

number of occurrences above the threshold, (2) the higher amount of non-occurrence below

the threshold, and (3) the values of the metrics presented in the next section of this

manuscript. Multiple rainfall-duration thresholds were defined from the application of 5%,

10%, 20%, 30%, 40%, and 50% non-exceedance probability aiming to reduce the

uncertainties of false alarms.

5.1.5 Comparison and evaluation procedures

The first evaluation step was to apply the Kling-Gupta Efficiency (KGE) scores to

assess the performance of the satellite-based rainfall products in characterising the rainfall

events that trigger are able to floods. KGE is an objective performance metric combining

correlation (CC, represented by the Pearson’s correlation coefficient), BIAS (represented by

55

the ratio of estimated and observed means), and variability (VAR, represented by the ratio

of the estimated and observed coefficients of variation):

KGE = 1 − ඥ(𝐶𝐶 − 1)ଶ + (𝐵𝐼𝐴𝑆 − 1)ଶ + (𝑉𝐴𝑅 − 1)ଶ (6)

μୣ

BIAS = (7) μ୭

∑୬ (O ୧ୀଵ ୧ − Oഥ) (E୧ − Eഥ) CC = (8)

ට∑୬୧ୀଵ(O୧ − Oഥ)ଶ . ඥ∑୬୧ୀଵ(E୧ − Eഥ)ଶ

CVୣ σୣ ⁄μୣ VAR = = (9)

CV୭ σ୭⁄μ୭

where O is the value observed by the rain gauges, Ō is the mean observed values, E

is the value estimated by satellite-based products, Ē is the mean estimated values, _𝜇_ is the

distribution mean and _𝜎_ is the standard deviation. The subscripts e and o correspond the

estimated and observed data, respectively. KGE values range from -∞ to 1, with desirable

values close to 1.

A second evaluation step was to verify the performance of the rainfall threshold

determined by each rainfall products to identify true or false alarms using a binary classifier

of the rainfall conditions that do or do not lead to floods occurrences. The same contingency

matrix applied in the section 4.2.3, consisting of four components, was used for each

threshold, including: 1) true positive (TP), when the threshold is exceeded and the flood

occurs; 2) false negative (FN), when the threshold is not exceeded and the flood occurs; 3)

false positive (FP), when the threshold is exceeded and the flood does not occur; and 4) true

negative (TN), when the threshold is not exceeded and the flood does not occur. The

following three metrics were then applied using the above-mentioned contingency matrix to

assess the skill score of the floods thresholds: 1) probability of detection (POD), which

measures the fraction of events that are correctly predicted by the satellite-based products;

2) false alarm ratio (FAR), which exhibits the fraction of events incorrectly detected by the
satellite-based products; and 3) Hanssen-Kuiper (HK) skill score, which measures the

applicability/quality to identify the usability and accuracy of the threshold:

TP POD = (10) TP + FN

56

| FAR = FP + TN FP | (11) |
| --- | --- |
| HK = POD − FAR | (12) |

The values of these three metrics range from 0% to 100%. The perfect values for

POD and HK are close to 100%, while the desirable values for FAR are close to 0%.

5.2 Results and discussion

5.2.1 Characterisation of rainfall events that triggers floods

Figure 11 presents the classifications of the daily rainfall considering the values

registered by the rain gauges and the analysed products only for the days where floods events

were registered. The results show that the ground-based data presented only heavy (45%)

and severe (55%) rain records during the analysed period. Conversely, all satellite-based

rainfall products presented light rain and moderate rain records ranging from 19% (CHIRPS

V2.0) to 53% (SM2RAIN-ASCAT V1.2) and from 36% (MERRA-2) to 62%

(GPM+SM2RAIN). This indicates an underestimation of the daily accumulated precipitation

by all analysed products. Among the dataset able to detect daily heavy and severe rains when

flood occurrences were registered, the following products stand out: 1) PDIR-Now,

represented by 31% of heavy rain and 6% of severe rain; 2) CMORPH-CRT V1.0,

characterised by 32% of heavy rain and 5% of severe rain; 3) PERSIANN-CCS, which

presented 26% of heavy rain and 6% of severe rain; and 4) IMERG-F, showing 25% of heavy

rain and 5% of severe rain.

**Figure 11.** Daily precipitation classification that leads flood occurrences in São Paulo State

57

Satellite-based underestimations of these extreme precipitation events, when

compared with the rain gauge observations, were also reported by others researchers

previously for a variety of products (e.g., Mayor et al. 2017; Solakian et al. 2020; Xuan et

al. 2020). Thus, it is important to analyse the performance of multiple precipitation products

over the region of interest instead of relying on randomly chosen products (Masugana et al.,

2019), because the performance of these products in capturing the spatiotemporal variability

of extremes rainfall depends on season, regions, time period, and inexistence or scarcity of

rain gauges to bias-correct products (Chen et al., 2020).

Figure 12 presents the mean KGE scores of the 14 satellite-based rainfall products

considering the six accumulated rainfall periods. The results of the KGE show that all

products presented negative mean scores for time steps ranging from 3 h to 1 day (-0.64 to -

0.41, on average). The best and worst performances of the mean KGE scores for the sub-

daily dataset, considering these first four aggregation periods (from 3 h to 1 day), were

identified to be IMERG-F (i.e., -0,38) and MERRA-2 (i.e., -1.28) products, respectively.

When only the daily datasets are considered, the best and worst performances of the daily

mean KGE scores were observed as the GPM+SM2RAIN (i.e., -0.08) and PERSIANN-CDR

V1R1 (i.e., -0.44) products, respectively. Overall, it is noticeable an improvement in the

KGE values when longer rainfall accumulation times are considered. Null to positive mean

KGE scores were observed for the time steps of 3 and 10 days (-0.02 to 0.18, on average).

Variability was the main responsible for the poor performance for time steps varying

between 3 hours and 1 day (2.12 to 1.87, on average), but the bias (0.25 – 0.27, on average)

and CC (0.08 to 0.19, on average) also presented their worst results for such time steps. For

longer time steps (3 days and 10 days), the variability presented results closer to ideal (1.45

- 1.18, on average), while the bias (0.39 – 0.57, on average) and CC (0.34 – 0.35, on average)
remained furthest from the desirable values for all products.

Overall, the best values of the analysed metrics were found for all products when the

rainfall was accumulated over 10 days. Two gauge-based uncorrected products (PDIR-Now

and GPM+SM2RAIN) presented the highest values of KGE (i.e., 0.36) for the time step

equal to 10 days. However, PDIR-Now presented the highest bias (i.e., 076), indicating that

this product better represents the total precipitation compared to GPM+SM2RAIN (bias =

0.54). On the other hand, the data from GPM+SM2RAIN better linearly correlates with the

observed data (CC = 0.55) when compared to the PDIR-Now product. The performance of

these two above-mentioned uncorrected products was followed by the following corrected

58

products: CHIRPS V2.0 (KGE = 0.34), MSWEP V2.2 (KGE = 0.28), and IMERG-F (KGE

= 0.27).

**Figure 12.** Graph showing the (a) KGE, (b) CC, (c) BIAS, and (d) VAR scores for the 14 satellite-based rainfall, considering only extreme precipitation events for time steps ranging from 3 hours to

10 days. The red lines represent the perfect values.

5.2.2 Overall analysis of the uncorrected dataset

Among the eight uncorrected satellite products (i.e., PERSIANN, PERSIANN-CCS,

PDIR-Now, SM2RAIN-ASCAT, GPM+SM2RAIN, IMERG-E, IMERG-L, and CHIRP

V2.0), the GPM+SM2RAIN product performed better for extreme precipitations when

considering the daily time step onwards, with mean KGE value of 0.15, followed by PDIR-

Now and CHIRP V2.0, with KGE values equal to 0.03 for both. PDIR-Now is a product,

intended to replace the PERSIANN-CCS datasets, which considers the errors and

uncertainties resulting from the use infrared images (Nguyen et al. 2020). Nevertheless,

PERSIANN-CCS performed slightly better than PDIR-Now for sub-daily time steps,

reversing the position for daily time steps onward. The PERSIANN product presented the

lowest values of KGE among the uncorrected analysed products, ranging from -0.60 (3

hours) to 0.04 (10 days). All sub-daily uncorrected products presented extremely low values

of KGE for time steps below 1 day, with means ranging from -0.76 (PERSIANN) to -0.45

(PERSIANN-CCS). Overall, the GPM+SM2RAIN product performed noticeably better than

SM2RAIN-ASCAT V1.2 (mean KGE = -0.11), i.e., the other product that also uses satellite-

based soil moisture data. The two microwave-based datasets (IMERG-E and IMERG-L)

59

showed similar results for all analysed time steps, with mean KGE values equal to -0.05

when considering daily onward time steps, i.e., slight worse than that observed for CHIRP

V2.0 (KGE = 0.03).

5.2.3 Overall analysis of the corrected dataset

The products corrected by ground observations use daily, pentadal (5-day), decadal

(10-day), and/or monthly precipitation data in their algorithms. Among the gauged corrected

products, CHIRPS V2.0 presented the higher values of KGE for extreme precipitations,

varying for daily time step onwards between -0.28 (1-day) and 0.34 (10-days). The

performance of this product was followed by MSWEP V2.2 and IMERG-F, with KGE

values ranging from -0.65 (3-hours) to 0.28 (10-days) and from -0.45 (3-hours) to 0.27 (10-

days), respectively. The CMORPH-CRT V1.0 product presented similar performance than

those observed for MSWEP V2.2 and IMERG-F, with KGE values varying between -0.47

(3-hours) and 0.26 (10-days). MERRA-2 and CMORPH-CRT V1.0 exhibited the lowest

values of KGE among the products corrected by ground observations, with overall

performances even worse than all those observed for the uncorrected products. The

performance of these products may be affected by some factors in rain gauges, such as

miscellaneous technical errors, different reporting times, different quality control

procedures, network density, among others (Derin and Yilmaz 2014; Sun et al. 2018; Beck

et al. 2019a; Shen et al. 2021).

5.2.4 Rainfall thresholds

5.2.4.1 Evaluation for different tolerance levels

Figure 13 shows the heatmaps with the main values of POD, FAR, and HK for the

six considered tolerance levels. The values of POD are set by the adopted tolerance levels,

with values varying between 0.95 and 0.50 for the no-exceedances probabilities of 5 and

50% for all satellite-based and the observed data, respectively (Figure 13a). On the other

hand, the FAR values presented reductions as the tolerance levels increased, with the worst

performance observed for CHIRPS V2.0, PERSIANN and PERSIANN-CDR V1R1

(FAR≈0.75) adopting a tolerance level of 5% tolerance (Figure 13b). The rainfall products

CMORPH-CRT V1.0, IMERG-F, and GPM+SM2RAIN exhibited the lower values of FAR

(0.11) when a tolerance level of 50% was considered, i.e., like the observed data but with a

60

tolerance level of 5% only (FAR = 0.13). The product that performed better overall in the

number of false alarms (IMERG-F) showed values varying between 0.50 (5%) and 0.11

(50%), i.e., much higher than those observed for the rain gauges, which ranged from 0.13 to

0.02, respectively.

**Figure 13.** Heatmap of the mean values of (a) POD, (b) FAR, and (c) HK using different no-exceedance probability.

Overall, all analysed products showed similar patterns in of HK, with an increase in

the values until a certain peak value, mostly between the application of tolerance levels of

10% and 30%, before a decline in the values of this metric for higher tolerance levels. The

difference is that the CHIRPS V2.0, PERSIANN, PERSIAN-CCS, and PERSIAN-CDR

V1R1 products exhibited peak values of HK for tolerance levels varying between 30% and

40%. The HK values indicate a better performance for the observed data utilising a tolerance

level of 5% (HK = 0.83), followed by the CHIRP V2.0 and IMERG-F products, which

presented HK values equal to 0.51 and 0.52, respectively, for tolerance levels of 20%.

Although presenting the highest values of HK, these two mentioned products still exhibited

a considerable rate of false alarms, around 28%. CHIRPS V2.0 and PERSIANN-CDR V1R1

also had the worst performance for this metric, as expected, with highest HK values equal to

0.29 and 0.36 for a tolerance level of 30%, respectively. The study carried by Brunetti et al.

(2018), which analysed 4 satellite products for delimitation of landslide thresholds in Italy,

showed that the SM2RAIN-ASCAT V1.2 product presented the highest values of HK equals

61

to 0.42 for exceedance limits between 20-25%, while the PERSIANN product performed

worse, with HK value equals to 0.31 for a tolerance level of 25%. Jia et al (2019) also

analysed 4 rainfall products for landslide thresholds on a global scale, including CMORPH,

which better performed among the evaluated, presenting a HK value equals to 0.43 for a

tolerance level of 22%. The same global scale study identified that PERSIANN presented

the lowest values of HK among the analysed products, with the best result (HK = 0.14) found

for a tolerance level equals to 9%.

5.2.4.2 Determination of rainfall thresholds

Figure 14 presents the six precipitation thresholds obtained from the tolerance limits

of 5, 10, 20, 30, 40, and 50% for the observed data and all analysed precipitation products.

It is possible to observe a considerable underestimation of the thresholds delineated by the

satellite-based products compared to those elaborated by the observed data, with larger

differences noticed for shorter time steps (3h–1d), which were smoothed for longer

considered periods (3–10 days). For instance, the CHIRPS V2.0, GPM+SM2RAIN, and

PDIR products presented, respectively, values for 10-days accumulated rainfalls equal to

54.6, 53.0, and 67.0 mm considering a tolerance level of 20%, which correspond,

respectively, to biases of 0.6, 0.58, and 0.72 (Figure 15) when compared to the thresholds

using the observed data (i.e., 91,8 mm). This behaviour was expected as it is difficult for the

satellite-based rainfall products to capture the precipitation peaks, resulting in values with

more spaced in time compared to those identified for the observed dataset. The worst

performances of the satellite-based products for longer time steps (i.e., daily onwards) were

verified for 3 days accumulated rainfall considering tolerance levels of 5%, with PERSIANN

(2.71 mm) and MSWEP V2.2 (3.73 mm) presenting the largest differences to the observed

data (42.6 mm), i.e., biases of 0.06 and 0.09, respectively. For shorter time-steps ranging

from 3h to 1d, the worst results were found for tolerance levels of 5%, where almost all

products presented bias values equal to or lower than below 0.1. An exception, considering

a tolerance level of 5%, was observed for the CHIRPS products, with bias value equals to

0.17 for accumulated rainfall of 1 day (6.41 mm, i.e., still much lower than the 37 mm

obtained with the observed data). The best results found for shorter time-steps were verified

for 1-day accumulated rainfall considering tolerance levels of 50% tolerance level. For this

combination of accumulated rainfall and tolerance level, for instance, the products

CMORPH-CRT V1.0, IMERG-F V06, and PDIR presented values equal to 22.75, 20.17,

62

and 20.0 mm, while the observed data, for the same time-step and no-exceedance probability,

exhibited a value of 73.5 mm. Overall, it is noticed in Figure 15 that the time steps presented

greater relevance in the improvement of the bias values compared to the tolerance limits.

**Figure 14.** Accumulated precipitation versus duration applying the tolerance levels of 5, 10, 20, 30,40, and 50% for the (a) rain gauges, (b) CHIRP V2.0, (c) CHIRPS V2.0, (d) IMERG-E V06, (e)

IMERG-L V06, (f) IMERG-F V06, (g) CMORPH-CRT V01, (h) MERRA-2, (i) MSWEP V2.2, (j) PERSIANN, (k) PERSIANN-CCS, (l) PERSIANN-CDR V1R1, (m) PDIR-Now, (n) SM2RAIN-

ASCAT V1.2, and (o) GPM+SM2RAIN.

63

**Figure 15.** BIAS values for the estimated rainfall thresholds, using rain gauge as a reference, fortolerance levels of (a) 5, (b) 10, (c) 20, (d) 30, (e) 40, and (f) 50%. The red lines represent the perfect

values.

64

6 CONCLUSIONS AND RECOMMENDATIONS

This thesis seeks to improve disaster monitoring and prediction, developing

techniques and methods that will increase the effectiveness of warnings systems. The

proposed methodology presented an evaluation of extreme precipitation events for the state

of São Paulo, becoming a methodological contribution to monitor the occurrence of (flash)

floods.

The first part of this thesis improved an existing peak rainfall intensity threshold

method capable of better separating the occurrences from the non-occurrences of floods and

flash floods. The improvement of this new approach included the use of two tolerance levels

and the delineation of an intermediate threshold represented by an exponential curve relating

rainfall intensity and API. The application of the tolerance levels proposed in this study

presented noticeable improvements for the rainfall peak intensity thresholds, with substantial

reduction of false alarms after the application of a tolerance level of 5% for the lower

threshold. Meanwhile, the number of occurrences above the upper threshold increased by

two times after the use of a tolerance level of the 99th percentile, improving the effectiveness

of the issuance of warnings. The delineation of the intermediate threshold also presented

improvements for almost all time-steps considered in this study, although the scores of the

metrics showed a slightly worse performance for flash floods when compared to floods. This

better performance noted for floods probably occurred because the higher amount of data

available for this type of event when compared to those observed for flash floods.

Additionally, the use of a denser rain gauge network, with stations closer to the flash flood

occurrences than those used in this study, could be more effective in capturing this type of

event.

It must be mentioned that a considerable amount of flood and flash flood information

in São Paulo State could not be used in the first study because of the poor data quality of

some rain gauges and/or the lack of rain gauge coverage at all. Thus, (sub)daily rainfall data

from 14 different satellite-based products were evaluated to characterise rainfall events that

trigger floods. The applicability of a methodology for determining precipitation thresholds

using the satellite-based products was then also evaluated. The two main findings of the

second study are summarised as follows:

(1) Overall, all analysed products tend to large underestimate the extreme rainfall

events (i.e., when and where flood events were registered) observed by the rain gauges,

mainly for sub-daily scales. This underestimation primarily occurred due to the difficulty of

65

the estimated products to capture precipitation peaks, as their values are more distributed

over time with longer durations. The point-to-pixel analysis used in this study tended to

contribute more to the underestimation of the observed peak intensity due to the

representation of a spatial average of precipitation at the pixel scale. The best results

evaluating the extreme rainfall events were expected for products corrected by ground-based

rainfall stations, but they were found for the PDIR-Now and GPM+SM2RAIN products

considering 10-days accumulated precipitation, followed by the corrected CHIRPS V2.0,

MSWEP V2.2, and GPM IMERG-F, although the results (i.e., KGE values ranging from

0.36 to 0.27) indicate that all products are far from ideal (KGE=1).

(2) Large underestimations were also identified for the rainfall thresholds delineated

by the satellite-based products. Despite the large underestimations, the delineation of rainfall

thresholds using satellite-based products is possible but with lower precipitation values and

a greater probability of false alarm occurrences. The observed rainfall data, considering

tolerance limits of 5%, presented mean HK and bias values for daily rainfall data ~60 and

65%, respectively, higher than the two products that better delineated the rainfall thresholds

(e.g., CHIRP V2.0 and IMERG-F) but considering tolerance levels of 20%.

Based on our findings, the rainfall satellite-based products dataset, even less accurate

than the ground-based observations, can be applied, when multi-daily accumulated data are

considered, as an alternative source of data for determining precipitation thresholds in some

regions that presents low-density of rain gauges. PDIR-Now showed to be an interesting

source of data to characterise flood events since this product provides near-real-time

information, followed by the SM2RAIN products, which correct the satellite rainfall data

without the use of ground-based information. For regions with a high-density of rain gauges

with sub-daily data available, the use of ground-based data will still provide a much better

source of information to characterise events that trigger floods.

The results found for this thesis can help in decision-making to consider new rain

gauges networks expanding the existing ones, especially in areas susceptible to floods, and

also in the development, and implementation of flood monitoring and warning systems.

However, some limitations and recommendations for further work can be pointed out:

(1) The information inconsistency brings great limitations for carrying out more precise

analyzes, so it is primordial the development of methods for analyzing the quality of

information and the creation of an inventory of occurrences of floods properly characterized

with the rainfall that triggered them. Concomitantly, it is recommended proper dissemination

of this information through the development of systems that allows the community to access

66

the information in real-time, also including forecast rainfall, locations susceptible to

flooding, and access to alerts issued by Civil Defense.

(2) The basic limitation is that rainfall thresholds inevitably just represent a simplification

of the relationship between rainfall and flood occurrence, because there is more than one

causative factor, such as urbanization rate, topography, land use, among others, that it can

be accounted for uncertainties in the proposed method. Therefore, improvements of the

rainfall thresholds methodology to reduce even more the uncertainties can be done by 1)

analyzing more rainfall properties correlated with other variables (e.g., soil moisture); 2)

using different approaches to characterize rainfall events (e.g., Minimum Inter-event Time);

and 3) further analyzing the APIs (e.g., longer antecedent periods).

(3) A more local threshold can vary substantially and can have very different rainfall

threshold. Therefore, the replication of the methodology subdividing the study area into

several zones to be analyzed independently, to set up a specific threshold for each of them.

As a consequence, a mosaic of several local rainfall thresholds is set up in place of a single

regional threshold.

(4) Rain gauges provide only-single point measurements and have a far from ideal spatial

distribution around the world, hence they poorly represent the spatial variability of

precipitation, which has great relevance for floods events. As an alternative solution, it

should be replicated the methodology with radar data, with the aim of a better representation

of the areal rain, giving new insight to the study with more detailed observations of rainfall

variations in a region.

(4) The use of new approaches (e.g., merging of products or improving the products

algorithms) must be explored for the satellite-based products by using, for instance, machine

learning techniques, to enable better identification and characterisation of extreme rainfall

events over areas with low availability of in-situ sub-daily data and, consequently, improve

the delineation of thresholds for monitoring flood hazards.

67

REFERENCES

Abon CC, David CPC, Tabios GQ (2012) Community-based monitoring for flood early

warning system: An example in central Bicol River basin, Philippines. Disaster Prev

Manag 21:85–96. [https://doi.org/10.1108/09653561211202728](https://doi.org/10.1108/09653561211202728)

AghaKouchak A, Farahmand A, Melton FS, et al (2015) Remote sensing of drought:

Progress, challenges and opportunities. Rev Geophys 53:452–480.

[https://doi.org/10.1002/2014RG000456](https://doi.org/10.1002/2014RG000456)

Aleotti P (2004) A warning system for rainfall-induced shallow failures. Eng Geol 73:247–

265. [https://doi.org/10.1016/j.enggeo.2004.01.007](https://doi.org/10.1016/j.enggeo.2004.01.007)
Alvares CA, Stape JL, Sentelhas PC, et al (2013) Köppen’s climate classification map for

Brazil. Meteorol Zeitschrift 22:711–728. [https://doi.org/10.1127/0941-](https://doi.org/10.1127/0941-)

2948/2013/0507

Ashouri H, Hsu KL, Sorooshian S, et al (2015) PERSIANN-CDR: Daily precipitation

climate data record from multisatellite observations for hydrological and climate

studies. Bull Am Meteorol Soc 96:69–83. [https://doi.org/10.1175/BAMS-D-13-](https://doi.org/10.1175/BAMS-D-13-)

00068.1

Atta-ur-Rahman, Parvin GA, Shaw R, Surjan A (2016) Cities, Vulnerability, and Climate

Change. Urban Disasters Resil Asia 35–47. [https://doi.org/10.1016/B978-0-12-](https://doi.org/10.1016/B978-0-12-)

802169-9.00003-3

Azari H, Matkan AA, Shakiba A, Pourali H (2008) Flood early warning with integration of

hydrologic and hydraulic models, RS and GIS. (Case study: Madarsoo Basin, Iran).

29th Asian Conf Remote Sens 2008, ACRS 2008 3:1679–1685

Bacelar LCSD, Maciel A, Angelis CF, Tomasella J (2020) Limiares de chuva deflagradores

de inundações bruscas : metodologia , aplicação e avaliação em ambiente operacional.

Rev DAE 68:71–86

Bai S, Wang J, Thiebes B, et al (2014) Analysis of the relationship of landslide occurrence

with rainfall: A case study of Wudu County, China. Arab J Geosci 7:1277–1285.

[https://doi.org/10.1007/s12517-013-0939-9](https://doi.org/10.1007/s12517-013-0939-9)

Barbería L, Amaro J, Aran M, Llasat MC (2014) The role of different factors related to social

impact of heavy rain events: Considerations about the intensity thresholds in densely

populated areas. Nat Hazards Earth Syst Sci 14:1843–1852.

[https://doi.org/10.5194/nhess-14-1843-2014](https://doi.org/10.5194/nhess-14-1843-2014)

Battistini A, Rosi A, Segoni S, et al (2017) Validation of landslide hazard models using a

68

semantic engine on online news. Appl Geogr 82:59–65.

[https://doi.org/10.1016/j.apgeog.2017.03.003](https://doi.org/10.1016/j.apgeog.2017.03.003)

Beck HE, Pan M, Roy T, et al (2019a) Daily evaluation of 26 precipitation datasets using

Stage-IV gauge-radar data for the CONUS. Hydrol Earth Syst Sci 23:207–224.

[https://doi.org/10.5194/hess-23-207-2019](https://doi.org/10.5194/hess-23-207-2019)

Beck HE, Van Dijk AIJM, Levizzani V, et al (2017a) MSWEP: 3-hourly 0.25° global

gridded precipitation (1979-2015) by merging gauge, satellite, and reanalysis data.

Hydrol Earth Syst Sci 21:589–615. [https://doi.org/10.5194/hess-21-589-2017](https://doi.org/10.5194/hess-21-589-2017)

Beck HE, Vergopolan N, Pan M, et al (2017b) Global-scale evaluation of 22 precipitation

datasets using gauge observations and hydrological modeling. Adv Glob Chang Res

69:625–653. [https://doi.org/10.1007/978-3-030-35798-6_9](https://doi.org/10.1007/978-3-030-35798-6_9)

Beck HE, Wood EF, Pan M, et al (2019b) MSWep v2 Global 3-hourly 0.1° precipitation:

Methodology and quantitative assessment. Bull Am Meteorol Soc 100:473–500.

[https://doi.org/10.1175/BAMS-D-17-0138.1](https://doi.org/10.1175/BAMS-D-17-0138.1)

Behrangi A, Khakbaz B, Jaw TC, et al (2011) Hydrologic evaluation of satellite precipitation

products over a mid-size basin. J Hydrol 397:225–237.

[https://doi.org/10.1016/j.jhydrol.2010.11.043](https://doi.org/10.1016/j.jhydrol.2010.11.043)

Berti M, Martina MLV, Franceschini S, et al (2012) Probabilistic rainfall thresholds for

landslide occurrence using a Bayesian approach. J Geophys Res Earth Surf 117:1–20.

[https://doi.org/10.1029/2012JF002367](https://doi.org/10.1029/2012JF002367)

Blenkinsop S, Fowler HJ, Barbero R, et al (2018) The INTENSE project: using observations

and models to understand the past, present and future of sub-daily rainfall extremes.

Adv Sci Res 15:117–126. [https://doi.org/10.5194/asr-15-117-2018](https://doi.org/10.5194/asr-15-117-2018)

Bogaard T, Greco R (2018) Invited perspectives: Hydrological perspectives on precipitation

intensity-duration thresholds for landslide initiation: Proposing hydro-meteorological

thresholds. Nat Hazards Earth Syst Sci 18:31–39. [https://doi.org/10.5194/nhess-18-31-](https://doi.org/10.5194/nhess-18-31-)

2018

Brasil (2012) INSTRUÇÃO NORMATIVA No 1. 9

Brazilian National Centre for Monitoring Early Warning of Natural Disasters (CEMADEN).

(2018) Manual Técnico para Elaboração, Transmissão e Uso de Alertas de Risco de

Movimentos de Massa. CEMADEN, São José dos Campos, Brazil

Brigandì G, Tito Aronica G, Bonaccorso B, et al (2017) Flood and landslide warning based

on rainfall thresholds and soil moisture indexes: The HEWS (Hydrohazards Early

Warning System) for Sicily. Adv Geosci 44:78–88. [https://doi.org/10.5194/adgeo-44-](https://doi.org/10.5194/adgeo-44-)

69

79-2017

Brocca L, Filippucci P, Hahn S, et al (2019) SM2RAIN-ASCAT (2007-2018): Global daily

satellite rainfall data from ASCAT soil moisture observations. Earth Syst Sci Data

11:1583–1601. [https://doi.org/10.5194/essd-11-1583-2019](https://doi.org/10.5194/essd-11-1583-2019)

Brocca L, Massari C, Tarpanelli A, et al (2017) A Review of the Applications of ASCAT

Soil Moisture Products A Review of the Applications of ASCAT Soil Moisture

Products. IEEE J Sel Top Appl Earth Obs Remote Sens 10:2285–2306

Brollo MJ, Ferreira CJ (2016) Gestão de risco de desastres devido a fenômenos

geodinâmicos no estado de São Paulo: Cenário 2000-2015. Instituto Geológico, São

Paulo, Brazil

Brunetti MT, Melillo M, Gariano SL, et al (2021) Satellite rainfall products outperform

ground observations for landslide prediction in India. Hydrol Earth Syst Sci 25:3267–

3279. [https://doi.org/10.5194/hess-25-3267-2021](https://doi.org/10.5194/hess-25-3267-2021)
Brunetti MT, Melillo M, Peruccacci S, et al (2018) How far are we from the use of satellite

rainfall products in landslide forecasting? Remote Sens Environ 210:65–75.

[https://doi.org/10.1016/j.rse.2018.03.016](https://doi.org/10.1016/j.rse.2018.03.016)

Brunetti MT, Peruccacci S, Rossi M, et al (2010) Rainfall thresholds for the possible

occurrence of landslides in Italy. Nat Hazards Earth Syst Sci 10:447–458.

[https://doi.org/10.5194/nhess-10-447-2010](https://doi.org/10.5194/nhess-10-447-2010)

Cannon SH, Gartner JE, Wilson RC, et al (2008) Storm rainfall conditions for floods and

debris flows from recently burned areas in southwestern Colorado and southern

California. Geomorphology 96:250–269.

[https://doi.org/10.1016/j.geomorph.2007.03.019](https://doi.org/10.1016/j.geomorph.2007.03.019)

Carvalho ICDH (2018) Análise de recorrências de eventos de desastres naturais com base

no sistema integrado de informações sobre desastres (S2ID) e séries históricas de

precipitação no Brasil: uma contribuição metodológica. Universidade de Brasília

CENAD (2014) Anuário Brasileiro de Desastres Naturais 2012. Cent Nac Gerenciamento

Riscos e Desastr 1–84

CEPED - Centro Universitário de Estudos e Pesquisas sobre Desastres (2013) Atlas

brasileiro de desastres naturais 1991 a 2012: volume São Paulo, 2nd edn. CEPED

UFSC, Florianópolis, Brazil

Chen H, Yong B, Kirstetter PE, et al (2021) Global component analysis of errors in three

satellite-only global precipitation estimates. Hydrol Earth Syst Sci 25:3087–3104.

[https://doi.org/10.5194/hess-25-3087-2021](https://doi.org/10.5194/hess-25-3087-2021)

70

Chikalamo EE, Mavrouli OC, Ettema J, et al (2020) Satellite-derived rainfall thresholds for

landslide early warning in Bogowonto Catchment, Central Java, Indonesia. Int J Appl

Earth Obs Geoinf 89:102093. [https://doi.org/10.1016/j.jag.2020.102093](https://doi.org/10.1016/j.jag.2020.102093)

Chikoore H, Bopape M-JM, Ndarana T, et al (2021) Synoptic structure of a sub-daily

extreme precipitation and flood event in Thohoyandou, north-eastern South Africa.

Weather Clim Extrem 33:100327. [https://doi.org/10.1016/j.wace.2021.100327](https://doi.org/10.1016/j.wace.2021.100327)

Chleborad AF, Baum RL, Godt JW, Powers PS (2008) A prototype system for forecasting

landslides in the Seattle, Washington, area. GSA Rev Eng Geol 20:103–120.

[https://doi.org/10.1130/2008.4020(06](https://doi.org/10.1130/2008.4020(06))

Collins BD, Kayen R, Sitar N (2007) Process-based empirical prediction of landslides in

weakly lithified coastal cliffs, San Francisco, California, USA. Landslides Clim Chang

Challenges Solut - Proc Int Conf Landslides Clim Chang 175–184.

[https://doi.org/10.1201/noe0415443180.ch22](https://doi.org/10.1201/noe0415443180.ch22)

Dee DP, Balmaseda M, Balsamo G, et al (2014) Toward a consistent reanalysis of the climate

system. Bull Am Meteorol Soc 95:1235–1248. [https://doi.org/10.1175/BAMS-D-13-](https://doi.org/10.1175/BAMS-D-13-)

00043.1

Derin Y, Yilmaz KK (2014) Evaluation of Multiple Satellite-Based Precipitation Products

over Complex Topography. J Hydrometeorol 15:1498–1516.

[https://doi.org/10.1175/JHM-D-13-0191.1](https://doi.org/10.1175/JHM-D-13-0191.1)

Dhyani S, Dhyani D (2016) Strategies for reducing deforestation and disaster risk: Lessons

from Garhwal Himalaya, India. Adv Nat Technol Hazards Res 42:507–528.

[https://doi.org/10.1007/978-3-319-43633-3_22](https://doi.org/10.1007/978-3-319-43633-3_22)

Diakakis M (2012) Rainfall thresholds for flood triggering. The case of Marathonas in

Greece. Nat Hazards 60:789–800. [https://doi.org/10.1007/s11069-011-9904-7](https://doi.org/10.1007/s11069-011-9904-7)

Dinis PA, Huvi J, Cabral Pinto M, Carvalho J (2021) Disastrous Flash Floods Triggered by

Moderate to Minor Rainfall Events. Recent Cases in Coastal Benguela (Angola).

Hydrology 8:73. [https://doi.org/10.3390/hydrology8020073](https://doi.org/10.3390/hydrology8020073)

Du S, Shi P, Van Rompaey A, Wen J (2015) Quantifying the impact of impervious surface

location on flood peak discharge in urban areas. Nat Hazards 76:1457–1471.

[https://doi.org/10.1007/s11069-014-1463-2](https://doi.org/10.1007/s11069-014-1463-2)

Dunkerley D (2019) Sub-daily rainfall intensity extremes: Evaluating suitable indices at

Australian arid and wet tropical observing sites. Water (Switzerland) 11:.

[https://doi.org/10.3390/w11122616](https://doi.org/10.3390/w11122616)

Dunkerley D (2008) Identifying individual rain events from pluviograph records: a review

71

with analysis of data from an Australian dryland site. Hydrol Process 22:5024–5036.

[https://doi.org/10.1002/hyp](https://doi.org/10.1002/hyp)

Freitas E da S, Coelho VHR, Xuan Y, et al (2020) The performance of the IMERG satellite-

based product in identifying sub-daily rainfall events and their properties. J Hydrol

589:125128. [https://doi.org/10.1016/j.jhydrol.2020.125128](https://doi.org/10.1016/j.jhydrol.2020.125128)

Froidevaux P, Schwanbeck J, Weingartner R, et al (2015) Flood triggering in Switzerland:

The role of daily to monthly preceding precipitation. Hydrol Earth Syst Sci 19:3903–

3924. [https://doi.org/10.5194/hess-19-3903-2015](https://doi.org/10.5194/hess-19-3903-2015)
Funk C, Peterson P, Landsfeld M, et al (2015) The climate hazards infrared precipitation

with stations - A new environmental record for monitoring extremes. Sci Data 2:1–21.

[https://doi.org/10.1038/sdata.2015.66](https://doi.org/10.1038/sdata.2015.66)

Furtado J, Oliveira M de, Dantas MC, et al (2014) Capacitação Básica em Proteção e Defesa

Civil. 157

Gadelha AN, Coelho VHR, Xavier AC, et al (2018) Grid box-level evaluation of IMERG

over Brazil at various space and time scales. Atmos Res #pagerange#.

[https://doi.org/10.1016/J.ATMOSRES.2018.12.001](https://doi.org/10.1016/J.ATMOSRES.2018.12.001)

Garcia M da GM, Brilha J, de Lima FF, et al (2018) The Inventory of Geological Heritage

of the State of São Paulo, Brazil: Methodological Basis, Results and Perspectives.

Geoheritage 10:239–258. [https://doi.org/10.1007/s12371-016-0215-y](https://doi.org/10.1007/s12371-016-0215-y)

Gelaro R, McCarty W, Suárez MJ, et al (2017) The modern-era retrospective analysis for

research and applications, version 2 (MERRA-2). J Clim 30:5419–5454.

[https://doi.org/10.1175/JCLI-D-16-0758.1](https://doi.org/10.1175/JCLI-D-16-0758.1)

Getirana A, Kirschbaum D, Mandarino F, et al (2020) Potential of GPM IMERG

precipitation estimates to monitor natural disaster triggers in urban areas: The case of

Rio de Janeiro, Brazil. Remote Sens 12:1–20. [https://doi.org/10.3390/rs12244095](https://doi.org/10.3390/rs12244095)

Gimenez DFS (2017) ANÁLISE DA PRECIPITAÇÃO PLUVIAL E OCORRÊNCIAS DE

DESASTRES NATURAIS NO ESTADO DE SÃO PAULO (1976 – 2012).

Universidade Estadual de Campinas

Glade T, Crozier M, Smith P (2000) Applying probability determination to refine landslide-

triggering rainfall thresholds using an empirical “Antecedent Daily Rainfall Model.”

Pure Appl Geophys 157:1059–1079. [https://doi.org/10.1007/s000240050017](https://doi.org/10.1007/s000240050017)

González-Cao J, García-Feal O, Fernández-Nóvoa D, et al (2019) Towards an automatic

early warning system of flood hazards based on precipitation forecast: the case of the

Miño River (NW Spain). Nat Hazards Earth Syst Sci 19:2583–2595.

72

[https://doi.org/10.5194/nhess-19-2583-2019](https://doi.org/10.5194/nhess-19-2583-2019)

Guha-Sapir D, Hoyois P, Below R (2015) Annual Disaster Statistical Review 2015 The

numbers and trends Centre for Research on the Epidemiology of Disasters (CRED)

Guha-sapir D, Hoyois P, Wallemacq P, Below R (2016) Annual disaster statistical review

2016: The numbers and trends. Rev Lit arts Am 1–50.

[https://doi.org/10.1093/rof/rfs003](https://doi.org/10.1093/rof/rfs003)

Guzzetti F, Peruccacci S, Rossi M, Stark CP (2008) The rainfall intensity – duration control

of shallow landslides and debris flows : an update. Landslides 5:3–17.

[https://doi.org/10.1007/s10346-007-0112-1](https://doi.org/10.1007/s10346-007-0112-1)

Habib E, Krajewski WF, Kruger A (2001) Sampling Errors of Tipping-Bucket Rain Gauge

Measurements. J Hydrol Eng 6:159–166. [https://doi.org/10.1061/(asce](https://doi.org/10.1061/(asce))1084-

0699(2001)6:2(159)

Hallegatte S, Green C, Nicholls RJ, Corfee-Morlot J (2013) Future flood losses in major

coastal cities. Nat Clim Chang 3:802–806. [https://doi.org/10.1038/nclimate1979](https://doi.org/10.1038/nclimate1979)

He S, Wang J, Liu S (2020) Rainfall event-duration thresholds for landslide occurrences in

China. Water (Switzerland) 12:. [https://doi.org/10.3390/w12020494](https://doi.org/10.3390/w12020494)

Hegerl GC, Black E, Allan RP, et al (2015) Challenges in quantifying changes in the global

water cycle. Bull Am Meteorol Soc 96:1097–1115. [https://doi.org/10.1175/BAMS-D-](https://doi.org/10.1175/BAMS-D-)

13-00212.1

Hong Y, Hsu KL, Sorooshian S, Gao X (2004) Precipitation estimation from remotely

sensed imagery using an artificial neural network cloud classification system. J Appl

Meteorol 43:1834–1852. [https://doi.org/10.1175/jam2173.1](https://doi.org/10.1175/jam2173.1)

Huang J, Ju NP, Liao YJ, Liu DD (2015) Determination of rainfall thresholds for shallow

landslides by a probabilistic and empirical method. Nat Hazards Earth Syst Sci

15:2715–2723. [https://doi.org/10.5194/nhess-15-2715-2015](https://doi.org/10.5194/nhess-15-2715-2015)

Huffman GJ, Bolvin DT, Braithwaite D, et al (2019) Algorithm Theoretical Basis Document

(ATBD) Version 06 NASA Global Precipitation Measurement (GPM) Integrated

Multi-satellitE Retrievals for GPM (IMERG). Natl Aeronaut Sp Adm 1–34

IBGE - Instituto Brasileiro de Geografia e Estatística (2021) (IBGE).

[https://cidades.ibge.gov.br/brasil/sp/.](https://cidades.ibge.gov.br/brasil/sp/.) Accessed 16 Jul 2019

Jang JH (2015) An advanced method to apply multiple rainfall thresholds for urban flood

warnings. Water (Switzerland) 7:6056–6078. [https://doi.org/10.3390/w7116056](https://doi.org/10.3390/w7116056)

Joyce RJ, Janowiak JE, Arkin PA, Xie P (2004) CMORPH: A method that produces global

precipitation estimates from passive microwave and infrared data at high spatial and

73

temporal resolution. J Hydrometeorol 5:487–503. [https://doi.org/10.1175/1525-](https://doi.org/10.1175/1525-)

7541(2004)005<0487:CAMTPG>2.0.CO;2

Kha DD, Nhu NY, Long VV, Van DTH (2020) Utility of GSMap precipitation and point

scale in gauge measurements for stream flow modelling - A case study in lam river

basin, Vietnam. J Ecol Eng 21:39–45. [https://doi.org/10.12911/22998993/116350](https://doi.org/10.12911/22998993/116350)

Kidd C (2001) Satellite rainfall climatology: A review. Int J Climatol 21:1041–1066.

[https://doi.org/10.1002/joc.635](https://doi.org/10.1002/joc.635)

Kidd C, Becker A, Huffman GJ, et al (2017) So, how much of the Earth’s surface is covered

by rain gauges? Bull Am Meteorol Soc 98:69–78. [https://doi.org/10.1175/BAMS-D-](https://doi.org/10.1175/BAMS-D-)

14-00283.1

Kidd C, Huffman G (2011) Global precipitation measurement. Meteorol Appl 18:334–353.

[https://doi.org/10.1002/met.284](https://doi.org/10.1002/met.284)

Kohler MA, Linsley RK (1951) Predicting the Runoff From Sorm Rainfall. US Weather Bur

Res Pap 34

Lee JH, Park HJ (2016) Assessment of shallow landslide susceptibility using the transient

infiltration flow model and GIS-based probabilistic approach. Landslides 13:885–903.

[https://doi.org/10.1007/s10346-015-0646-6](https://doi.org/10.1007/s10346-015-0646-6)

Levizzani V, Kidd C, Aonashi K, et al (2018) The activities of the international precipitation

working group. Q J R Meteorol Soc 144:3–15. [https://doi.org/10.1002/qj.3214](https://doi.org/10.1002/qj.3214)

Lewis E, Fowler H, Alexander L, et al (2019) GSDR: A global sub-daily rainfall dataset. J

Clim 32:4715–4729. [https://doi.org/10.1175/JCLI-D-18-0143.1](https://doi.org/10.1175/JCLI-D-18-0143.1)

Li Z, Liu H (2020) Temporal and spatial variations of precipitation change from southeast

to northwest china during the period 1961-2017. Water (Switzerland) 12:.

[https://doi.org/10.3390/W12092622](https://doi.org/10.3390/W12092622)

Li Z, Zhang H, Singh VP, et al (2019) A simple early warning system for flash floods in an

ungauged catchment and application in the Loess Plateau, China. Water (Switzerland)

11:. [https://doi.org/10.3390/w11030426](https://doi.org/10.3390/w11030426)

Llauca H, Lavado‐casimiro W, León K, et al (2021) Assessing near real‐time satellite

precipitation products for flood simulations at sub‐daily scales in a sparsely gauged

watershed in Peruvian andes. Remote Sens 13:1–18.

[https://doi.org/10.3390/rs13040826](https://doi.org/10.3390/rs13040826)

Marra F, Morin E (2015) Use of radar QPE for the derivation of Intensity-Duration-

Frequency curves in a range of climatic regimes

Massari C, Brocca L, Pellarin T, et al (2020) A daily 25km short-latency rainfall product for

74

data-scarce regions based on the integration of the Global Precipitation Measurement

mission rainfall and multiple-satellite soil moisture products. Hydrol Earth Syst Sci

24:2687–2710. [https://doi.org/10.5194/hess-24-2687-2020](https://doi.org/10.5194/hess-24-2687-2020)

Mayor YG, Tereshchenko I, Fonseca-Hernández M, et al (2017) Evaluation of error in

IMERG precipitation estimates under different topographic conditions and temporal

scales over Mexico. Remote Sens 9:1–18. [https://doi.org/10.3390/rs9050503](https://doi.org/10.3390/rs9050503)

Miguez MG, Gregório LT Di, Veról AP (2018) Gestão de riscos e desastres hidrológicos,

1st edn. Elsevier, Rio de Janeiro

Mirus BB, Becker RE, Baum RL, Smith JB (2018) Integrating real-time subsurface

hydrologic monitoring with empirical rainfall thresholds to improve landslide early

warning. Landslides 15:1909–1919. [https://doi.org/10.1007/s10346-018-0995-z](https://doi.org/10.1007/s10346-018-0995-z)

Monsieurs E, Dewitte O, Demoulin A (2019) A susceptibility-based rainfall threshold

approach for landslide occurrence. Nat Hazards Earth Syst Sci 19:775–789.

[https://doi.org/10.5194/nhess-19-775-2019](https://doi.org/10.5194/nhess-19-775-2019)

Muntohar AS, Mavrouli O, Jetten VG, et al (2021) Development of Landslide Early Warning

System Based on the Satellite-Derived Rainfall Threshold in Indonesia. 227–235.

[https://doi.org/10.1007/978-3-030-60311-3_26](https://doi.org/10.1007/978-3-030-60311-3_26)

Nanda Pratama G, Suwarman R, Dewa Gede Agung Junnaedhi I, et al (2017) Comparison

landslide-triggering rainfall threshold using satellite data: TRMM and GPM in South

Bandung area. IOP Conf Ser Earth Environ Sci 71:0–9. [https://doi.org/10.1088/1755-](https://doi.org/10.1088/1755-)

1315/71/1/012003

Natural Resources Conservation Service (NRCS) (1972) National engineering handbook. In:

Development. US Government Printing Office, Washington, DC

Nguyen P, Shearer EJ, Ombadi M, et al (2020) PERSIANN dynamic infrared-rain rate model

(PDIR) for high-resolution, real-time satellite precipitation estimation. Bull Am

Meteorol Soc 101:E286–E302. [https://doi.org/10.1175/BAMS-D-19-0118.1](https://doi.org/10.1175/BAMS-D-19-0118.1)

Ochoa-Rodriguez S, Wang LP, Willems P, Onof C (2019) A Review of Radar-Rain Gauge

Data Merging Methods and Their Potential for Urban Hydrological Applications. Water

Resour Res 55:6356–6391. [https://doi.org/10.1029/2018WR023332](https://doi.org/10.1029/2018WR023332)

Pan HL, Jiang YJ, Wang J, Ou GQ (2018) Rainfall threshold calculation for debris flow

early warning in areas with scarcity of data. Nat Hazards Earth Syst Sci 18:1395–1409.

[https://doi.org/10.5194/nhess-18-1395-2018](https://doi.org/10.5194/nhess-18-1395-2018)

Pandey V, Srivastava PK (2019) Integration of microwave and optical/infrared derived

datasets for a drought hazard inventory in a sub-tropical region of India. Remote Sens

75

11:. [https://doi.org/10.3390/rs11040439](https://doi.org/10.3390/rs11040439)

Papagiannaki K, Lagouvardos K, Kotroni V, Bezes A (2015) Flash flood occurrence and

relation to the rainfall hazard in a highly urbanized area. Nat Hazards Earth Syst Sci

15:1859–1871. [https://doi.org/10.5194/nhess-15-1859-2015](https://doi.org/10.5194/nhess-15-1859-2015)

Parker AL, Castellazzi P, Fuhrmann T, et al (2021) Article applications of satellite radar

imagery for hazard monitoring: Insights from Australia. Remote Sens 13:1–25.

[https://doi.org/10.3390/rs13081422](https://doi.org/10.3390/rs13081422)

Parker WS (2016) Reanalyses and observations: What’s the Difference? Bull Am Meteorol

Soc 97:1565–1572. [https://doi.org/10.1175/BAMS-D-14-00226.1](https://doi.org/10.1175/BAMS-D-14-00226.1)

Peres DJ, Cancelliere A, Greco R, Bogaard TA (2018) Influence of uncertain identification

of triggering rainfall on the assessment of landslide early warning thresholds. Nat

Hazards Earth Syst Sci 18:633–646. [https://doi.org/10.5194/nhess-18-633-2018](https://doi.org/10.5194/nhess-18-633-2018)

Peruccacci S, Brunetti MT, Gariano SL, et al (2017) Rainfall thresholds for possible

landslide occurrence in Italy. Geomorphology 290:39–57.

[https://doi.org/10.1016/j.geomorph.2017.03.031](https://doi.org/10.1016/j.geomorph.2017.03.031)

Peruccacci S, Brunetti MT, Luciani S, et al (2012) Lithological and seasonal control on

rainfall thresholds for the possible initiation of landslides in central Italy.

Geomorphology 139–140:79–90. [https://doi.org/10.1016/j.geomorph.2011.10.005](https://doi.org/10.1016/j.geomorph.2011.10.005)

Peruccacci S, Brunetti MT, Rossi M, Guzzetti F (2009) Rainfall thresholds for the initiation

of landslides in Italy. Assembly 11:2729

Ramos VM (2017) Mapeamento de áreas susceptíveis à ocorrência de escorregamentos no

Brasil e suas relações com aspectos socioeconômicos. Universidade de Brasília

Ranghetti L, Cardarelli E, Boschetti M, et al (2018) Assessment of water management

changes in the Italian rice paddies from 2000 to 2016 using satellite data: A contribution

to agro-ecological studies. Remote Sens 10:80–90. [https://doi.org/10.3390/rs10030416](https://doi.org/10.3390/rs10030416)

Rijswick V (2015) Flood risk management in the netherlands. Delta 1–11

Rossi M, Luciani S, Valigi D, et al (2017) Statistical approaches for the definition of

landslide rainfall thresholds and their uncertainty using rain gauge and satellite data.

Geomorphology 285:16–27. [https://doi.org/10.1016/j.geomorph.2017.02.001](https://doi.org/10.1016/j.geomorph.2017.02.001)

Sampson CC, Smith AM, Bates PB, et al (2015) A high-resolution global flood hazard

model. Water Resour Res 51:7358–7381. [https://doi.org/10.1002/2015WR016954](https://doi.org/10.1002/2015WR016954)

Santos M, Fragoso M (2016) Precipitation thresholds for triggering floods in the Corgo

basin, Portugal. Water (Switzerland) 8:. [https://doi.org/10.3390/w8090376](https://doi.org/10.3390/w8090376)

Scheevel CR, Baum RL, Mirus BB, Smith JB (2017) Precipitation thresholds for landslide

76

occurrence near Seattle, Mukilteo, and Everett, Washington: U.S. Geological Survey

Open-File Report 2017–1039

Segoni S, Gariano SL, Rosi A (2021) Preface to the special issue “rainfall thresholds and

other approaches for landslide prediction and early warning.” Water (Switzerland)

13:1–5. [https://doi.org/10.3390/w13030323](https://doi.org/10.3390/w13030323)

Segoni S, Rosi A, Rossi G, et al (2014) Analysing the relationship between rainfalls and

landslides to define a mosaic of triggering thresholds for regional-scale warning

systems. Nat Hazards Earth Syst Sci 14:2637–2648. [https://doi.org/10.5194/nhess-14-](https://doi.org/10.5194/nhess-14-)

2637-2014

Setzer J (1946) Revista Brasileira de Geografia Física. Rev Bras Geogr 08:3–26

Sheffield J, Wood EF, Pan M, et al (2018) Satellite Remote Sensing for Water Resources

Management: Potential for Supporting Sustainable Development in Data-Poor Regions.

Water Resour Res 54:9724–9758. [https://doi.org/10.1029/2017WR022437](https://doi.org/10.1029/2017WR022437)

Shen Z, Yong B, Gourley JJ, Qi W (2021) Real-time bias adjustment for satellite-based

precipitation estimates over Mainland China. J Hydrol 596:126133.

[https://doi.org/10.1016/j.jhydrol.2021.126133](https://doi.org/10.1016/j.jhydrol.2021.126133)

Shrestha PK, Shrestha S, Ninsawat S (2019) How significant is sub-daily variability of

rainfall for hydrological modelling of floods? A satellite based approach to sub-daily

downscaling of gauged rainfall. Meteorol Appl 26:288–299.

[https://doi.org/10.1002/met.1762](https://doi.org/10.1002/met.1762)

Singh L, Saravanan S (2020) Satellite-derived GRACE groundwater storage variation in

complex aquifer system in India. Sustain Water Resour Manag 6:.

[https://doi.org/10.1007/s40899-020-00399-3](https://doi.org/10.1007/s40899-020-00399-3)

Solakian J, Maggioni V, Godrej AN (2020) On the Performance of Satellite-Based

Precipitation Products in Simulating Streamflow and Water Quality During

Hydrometeorological Extremes. Front Environ Sci 8:1–20.

[https://doi.org/10.3389/fenvs.2020.585451](https://doi.org/10.3389/fenvs.2020.585451)

Sorooshian S, Hsu KL, Gao X, et al (2000) Evaluation of PERSIANN system satellite-based

estimates of tropical rainfall. Bull Am Meteorol Soc 81:2035–2046.

[https://doi.org/10.1175/1520-0477(2000](https://doi.org/10.1175/1520-0477(2000))081<2035:EOPSSE>2.3.CO;2

Souza CM, Shimbo JZ, Rosa MR, et al (2020) Reconstructing three decades of land use and

land cover changes in brazilian biomes with landsat archive and earth engine. Remote

Sens 12:. [https://doi.org/10.3390/RS12172735](https://doi.org/10.3390/RS12172735)

Špitalar M, Gourley JJ, Lutoff C, et al (2014) Analysis of flash flood parameters and human

77

impacts in the US from 2006 to 2012. J Hydrol 519:863–870.

[https://doi.org/10.1016/j.jhydrol.2014.07.004](https://doi.org/10.1016/j.jhydrol.2014.07.004)

Srinivas H, Nakagawa Y (2008) Environmental implications for disaster preparedness:

Lessons Learnt from the Indian Ocean Tsunami. J Environ Manage 89:4–13.

[https://doi.org/10.1016/j.jenvman.2007.01.054](https://doi.org/10.1016/j.jenvman.2007.01.054)

Su J, Lü H, Zhu Y, et al (2019) Evaluating the hydrological utility of latest IMERG products

over the Upper Huaihe River Basin, China. Atmos Res 225:17–29.

[https://doi.org/10.1016/j.atmosres.2019.03.025](https://doi.org/10.1016/j.atmosres.2019.03.025)

Sun Q, Miao C, Duan Q, et al (2018) A Review of Global Precipitation Data Sets: Data

Sources, Estimation, and Intercomparisons. Rev Geophys 56:79–107.

[https://doi.org/10.1002/2017RG000574](https://doi.org/10.1002/2017RG000574)

Sungmin O, Kirstetter PE (2018) Evaluation of diurnal variation of GPM IMERG-derived

summer precipitation over the contiguous US using MRMS data. Q J R Meteorol Soc

144:270–281. [https://doi.org/10.1002/qj.3218](https://doi.org/10.1002/qj.3218)

Suribabu CR, Sujatha ER (2019) Evaluation of moisture level using precipitation indices as

a landslide triggering factor-a study of Coonoor Hill Station. Climate 7:.

[https://doi.org/10.3390/cli7090111](https://doi.org/10.3390/cli7090111)

Tan ML, Duan Z (2017) Assessment of GPM and TRMM precipitation products over

Singapore. Remote Sens 9:1–16. [https://doi.org/10.3390/rs9070720](https://doi.org/10.3390/rs9070720)

Tan ML, Latif AB, Pohl C, Duan Z (2014) Streamflow modelling by remote sensing: A

contribution to digital Earth. IOP Conf Ser Earth Environ Sci 18:0–6.

[https://doi.org/10.1088/1755-1315/18/1/012060](https://doi.org/10.1088/1755-1315/18/1/012060)

Tingsanchali T (2012) Urban flood disaster management. Procedia Eng 32:25–37.

[https://doi.org/10.1016/j.proeng.2012.01.1233](https://doi.org/10.1016/j.proeng.2012.01.1233)

Tominaga LK, Santoro J, Amaral R do. (2015) Desastres naturais: conhecer para prevenir,

3rd edn. Instituto Geológico, São Paulo, Brazil

Tramblay Y, Bouaicha R, Brocca L, et al (2012) Estimation of antecedent wetness conditions

for flood modelling in northern Morocco. Hydrol Earth Syst Sci 16:4375–4386.

[https://doi.org/10.5194/hess-16-4375-2012](https://doi.org/10.5194/hess-16-4375-2012)

Tsakiris G (2014) Flood risk assessment: Concepts, modelling, applications. Nat Hazards

Earth Syst Sci 14:1361–1369. [https://doi.org/10.5194/nhess-14-1361-2014](https://doi.org/10.5194/nhess-14-1361-2014)

Turkington T, Ettema J, Van Westen CJ, Breinl K (2014) Empirical atmospheric thresholds

for debris flows and flash floods in the southern French Alps. Nat Hazards Earth Syst

Sci 14:1517–1530. [https://doi.org/10.5194/nhess-14-1517-2014](https://doi.org/10.5194/nhess-14-1517-2014)

78

UNIFESP, UNA-SUS (2016) Gestão Local de Desastres Naturais para a Atenção Básica.

122

Varma AK (2018) Measurement of Precipitation from Satellite Radiometers (Visible,

Infrared, and Microwave): Physical Basis, Methods, and Limitations. Elsevier Inc.

Vasco DW, Farr TG, Jeanne P, et al (2019) Satellite-based monitoring of groundwater

depletion in California’s Central Valley. Sci Rep 9:1–14.

[https://doi.org/10.1038/s41598-019-52371-7](https://doi.org/10.1038/s41598-019-52371-7)

Viessman W, Lewis GL (1996) Introduction to Hydrology, 4th edn. Harper Collins, New

York

Villarini G, Krajewski WF (2010) Review of the different sources of uncertainty in single

polarization radar-based estimates of rainfall. Surv Geophys 31:107–129.

[https://doi.org/10.1007/s10712-009-9079-x](https://doi.org/10.1007/s10712-009-9079-x)

Villarini G, Krajewski WF, Ntelekos AA, et al (2010) Towards probabilistic forecasting of

flash floods: The combined effects of uncertainty in radar-rainfall and flash flood

guidance. J Hydrol 394:275–284. [https://doi.org/10.1016/j.jhydrol.2010.02.014](https://doi.org/10.1016/j.jhydrol.2010.02.014)

Wallemacq P, House R (2018) Economic losses, poverty and disasters 1998–2017. UNDRR

and CRED, Geneva and Brussels, Switzerland

Wang C, Tang G, Han Z, et al (2018) Global intercomparison and regional evaluation of

GPM IMERG Version-03, Version-04 and its latest Version-05 precipitation products:

Similarity, difference and improvements. J Hydrol 564:342–356.

[https://doi.org/10.1016/j.jhydrol.2018.06.064](https://doi.org/10.1016/j.jhydrol.2018.06.064)

WHO (1971) Guide To Sanitation in Natural Disasters

WMO (2015) Guidelines on the Defintion and Monitoring of Extreme Weather and Climate

Events. Wmo 62

Wu SJ, Hsu CT, Lien HC, Chang CH (2015) Modeling the effect of uncertainties in rainfall

characteristics on flash flood warning based on rainfall thresholds. Nat Hazards

75:1677–1711. [https://doi.org/10.1007/s11069-014-1390-2](https://doi.org/10.1007/s11069-014-1390-2)

Xie P, Joyce R, Wu S, et al (2017) Reprocessed, bias-corrected CMORPH global high-

resolution precipitation estimates from 1998. J Hydrometeorol 18:1617–1641.

[https://doi.org/10.1175/JHM-D-16-0168.1](https://doi.org/10.1175/JHM-D-16-0168.1)

Xuan D, Hu Q, Wang Y, et al (2020) Precipitation characteristic analysis of the Zhoushan

Archipelago: From the view of MSWEP and rainfall merging. Water (Switzerland) 12:.

[https://doi.org/10.3390/w12030829](https://doi.org/10.3390/w12030829)

Yang TH, Hwang G Do, Tsai CC, Ho JY (2016) Using rainfall thresholds and ensemble

79

precipitation forecasts to issue and improve urban inundation alerts. Hydrol Earth Syst

Sci 20:4731–4745. [https://doi.org/10.5194/hess-20-4731-2016](https://doi.org/10.5194/hess-20-4731-2016)

Young A, Bhattacharya B, Zevenbergen C (2021) A rainfall threshold-based approach to

early warnings in urban data-scarce regions: A case study of pluvial flooding in

Alexandria, Egypt. J Flood Risk Manag 14:1–16. [https://doi.org/10.1111/jfr3.12702](https://doi.org/10.1111/jfr3.12702)

Yuan F, Zhang L, Soe KMW, et al (2019) Applications of TRMM- and GPM-era multiple-

satellite precipitation products for flood simulations at sub-daily scales in a sparsely

gauged watershed in Myanmar. Remote Sens 11:. [https://doi.org/10.3390/rs11020140](https://doi.org/10.3390/rs11020140)

Zêzere JL, Oliveira SC, Trigo RM, et al (2010) Rainfall-triggered landslides in the Lisbon

region over 2006 and relationships with the North Atlantic Oscillation. Nat Hazards

Earth Syst Sci 8:483–499. [https://doi.org/10.5194/nhess-8-483-2008](https://doi.org/10.5194/nhess-8-483-2008)

Zhao B, Dai Q, Han D, et al (2019) Antecedent wetness and rainfall information in landslide

threshold definition. Hydrol Earth Syst Sci Discuss 1–26. [https://doi.org/10.5194/hess-](https://doi.org/10.5194/hess-)

2019-150

80

APPENDIXES A

81

**Figure 16 –** Scatter plots of rainfall observed values (rain gauges) vs estimated values (CHIRPV2.0) that lead to floods at different timescales.

**Figure 17 -** Scatter plots of rainfall observed values (rain gauges) vs estimated values (CHIRPSV2.0) that lead to floods at different timescales**.**

82

**Figure 18 –** Scatter plots of rainfall observed values (rain gauges) vs estimated values (CMORPH-CRT V1.0) that lead to floods at different timescales.

83

**Figure 19 -** Scatter plots of rainfall observed values (rain gauges) vs estimated values(IMERGHHE V06) that lead to floods at different timescales.

84

**Figure 20 –** Scatter plots of rainfall observed values (rain gauges) vs estimated values(IMERGHLL V06) that lead to floods at different timescales**.**

85

**Figure 21 –** Scatter plots of rainfall observed values (rain gauges) vs estimated values (IMERGHHV06) that lead to floods at different timescales.

86

**Figure 22 –** Scatter plots of rainfall observed values (rain gauges) vs estimated values (MERRA-2)that lead to floods at different timescales**.**

87

**Figure 23 –** Scatter plots of rainfall observed values (rain gauges) vs estimated values (MSWEPV2.2) that lead to floods at different timescales.

88

**Figure 24 –** Scatter plots of rainfall observed values (rain gauges) vs estimated values (PDIR-Now)that lead to floods at different timescales.

89

**Figure 25 –** Scatter plots of rainfall observed values (rain gauges) vs estimated values(PERSIANN) that lead to floods at different timescales.

90

**Figure 26 –** Scatter plots of rainfall observed values (rain gauges) vs estimated values(PERSIANN-CCS) that lead to floods at different timescales.

91

**Figure 27 –** Scatter plots of rainfall observed values (rain gauges) vs estimated values(PERSIANN-CDR V1R1) that lead to floods at different timescales.

**Figure 28** – Scatter plots of rainfall observed values (rain gauges) vs estimated values (SM2RAIN-ASCAT V1.2) that lead to floods at different timescales.

92

**Figure 29 –** Scatter plots of rainfall observed values (rain gauges) vs estimated values(GPM+SM2RAIN) that lead to floods at different timescales.

93

APPENDIXES B

94

**Table 7 –** Summary of Mean Relative Absolute Error (MRAE) for estimated precipitation products, considering different timescales

**PRODUCTS / TIME** 1h 3h 6h 8h 10h 12h 1d 3d 5d 7d 9d 10d

| CHIRP V2.0 | - | - | - | - | - | - | 79.76% 64.98% 54.73% 47.40% 41.36% 38.70% |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CHIRPS V2.0 | - | - | - | - | - | - | 67.16% 56.59% 47.13% 41.62% 36.42% 33.73% |

**CMORPH-CRT V1.0** 72.77% 63.17% 60.18% 59.77% 59.76% 59.88% 60.43% 51.47% 44.05% 40.94% 38.49% 37.66%

| PDIR-NOW | 72.92% 66.50% 64.18% 64.09% 64.19% 63.67% 60.63% 44.30% 33.12% 25.83% 19.50% 16.78% |
| --- | --- |
| IMERGHEE V06 | 77.30% 70.50% 68.50% 68.25% 68.36% 68.32% 67.52% 57.64% 50.17% 46.20% 43.22% 42.31% |
| IMERGHHL V06 | 78.03% 69.05% 66.13% 65.88% 65.79% 65.88% 65.41% 55.52% 48.21% 44.48% 41.73% 40.76% |
| IMERGHH V06 | 78.05% 68.82% 65.68% 65.34% 65.23% 65.26% 64.51% 53.94% 46.41% 42.55% 39.45% 38.19% |
| MERRA-2 | 88.65% 81.64% 77.76% 76.13% 74.64% 73.48% 69.25% 48.00% 35.58% 27.12% 21.42% 18.85% |

**MSWEP V2.2** - 71.38% 66.77% - - 66.59% 66.17% 58.70% 51.41% 48.11% 45.40% 43.89%

| PERSIANN | 84.17% 75.96% 73.05% 72.78% 72.79% 72.92% 72.10% 63.37% 55.82% 51.80% 47.90% 46.53% |
| --- | --- |
| PERSIANN CCS | 73.88% 68.36% 66.21% 65.92% 65.79% 65.54% 63.73% 50.85% 41.40% 36.06% 31.31% 29.68% |

| PERSIANN-CDR V1R1 | - | - | - | - | - | - | 74.87% 59.24% 47.64% 41.83% 37.86% 36.77% |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SM2RAIN-ASCAT V 1.2 | - | - | - | - | - | - | 84.84% 72.13% 63.75% 56.30% 50.49% 48.08% |

**GPM+SM2RAIN** - - - - - - 73.99% 60.42% 52.17% 47.08% 42.86% 41.25%

95

**Table 8 –** Summary of Root Mean Square Error (RMSE) for estimated precipitation products, considering different timescales**.**

**PRODUCTS / TIME** 1h 3h 6h 8h 10h 12h 1d 3d 5d 7d 9d 10d

| CHIRP V2.0 | - | - | - | - | - | - | 74.44 | 88.10 | 89.93 | 90.93 | 93.53 | 96.12 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHIRPS V2.0 | - | - | - | - | - | - | 65.76 | 78.88 | 81.52 | 82.56 | 85.84 | 88.34 |

**CMORPH-CRT V1.0** 38.58 49.27 55.31 57.72 58.99 60.23 67.00 80.92 84.22 85.87 90.72 94.76

| PDIR-NOW | 38.55 | 48.55 | 53.55 | 55.65 | 56.82 | 58.05 | 63.62 | 69.60 | 70.14 | 70.71 | 73.77 | 76.39 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMERGHEE V06 | 40.39 | 52.00 | 58.01 | 60.27 | 61.61 | 62.94 | 69.11 | 84.51 | 87.96 | 90.92 | 95.92 | 100.03 |
| IMERGHHL V06 | 40.68 | 51.77 | 57.22 | 59.41 | 60.56 | 61.86 | 68.02 | 83.11 | 86.65 | 89.48 | 94.69 | 98.95 |
| IMERGHH V06 | 40.49 | 51.23 | 56.52 | 58.59 | 59.70 | 60.99 | 67.04 | 80.49 | 83.00 | 85.47 | 90.67 | 94.70 |
| MERRA-2 | 44.54 | 58.35 | 64.94 | 67.24 | 68.51 | 69.78 | 75.51 | 94.92 | 102.01 | 107.28 | 110.56 | 113.84 |
| MSWEP V2.2 | - | 54.10 | 59.46 | - | - | 63.77 | 69.23 | 82.72 | 84.96 | 87.75 | 94.06 | 97.07 |
| PERSIANN | 43.99 | 54.70 | 59.72 | 61.55 | 62.56 | 63.31 | 69.43 | 83.77 | 88.70 | 91.90 | 98.47 | 102.43 |
| PERSIANN CCS | 39.16 | 50.67 | 56.75 | 59.06 | 60.31 | 61.60 | 67.63 | 81.95 | 84.87 | 86.43 | 91.56 | 95.16 |

| PERSIANN-CDR V1R1 | - | - | - | - | - | - | 75.31 | 93.05 | 99.13 | 103.34 | 107.73 | 111.46 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SM2RAIN-ASCAT V 1.2 | - | - | - | - | - | - | 79.64 | 97.27 | 100.57 | 102.29 | 108.28 | 112.07 |

**GPM+SM2RAIN** - - - - - - 68.88 79.05 81.37 83.74 87.66 90.39

96

**Table 9 –** Summary of Correlation Coefficient (CC) for estimated precipitation products, considering different timescales.

PRODUCTS / TIME 1h 3h 6h 8h 10h 12h 1d 3d 5d 7d 9d 10d

| CHIRP V2.0 | - | - | - | - | - | - | 0.34 | 0.47 | 0.47 | 0.45 | 0.43 | 0.42 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHIRPS V2.0 | - | - | - | - | - | - | 0.32 | 0.51 | 0.50 | 0.49 | 0.48 | 0.47 |

**CMORPH-CRT V1.0** 0.25 0.18 0.14 0.13 0.14 0.16 0.15 0.34 0.38 0.41 0.42 0.41

**PDIR-Now** 0.14 0.14 0.20 0.21 0.23 0.22 0.19 0.41 0.45 0.45 0.43 0.43

| IMERGHEE V06 | 0.15 | 0.15 | 0.16 | 0.17 | 0.19 | 0.20 | 0.21 | 0.36 | 0.40 | 0.41 | 0.40 | 0.40 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMERGHHL V06 | 0.14 | 0.13 | 0.16 | 0.17 | 0.19 | 0.21 | 0.22 | 0.36 | 0.39 | 0.41 | 0.40 | 0.39 |
| IMERGHH V06 | 0.14 | 0.15 | 0.17 | 0.19 | 0.21 | 0.23 | 0.24 | 0.40 | 0.45 | 0.47 | 0.45 | 0.43 |

| MERRA-2 | -0.06 | -0.07 | -0.06 | -0.06 | -0.07 | -0.07 | -0.05 | -0.04 | -0.03 | -0.03 | -0.02 | -0.01 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MSWEP V2.2 | - | -0.04 | 0.00 | - | - | 0.10 | 0.18 | 0.45 | 0.51 | 0.54 | 0.51 | 0.52 |
| PERSIANN | -0.06 | 0.02 | 0.09 | 0.13 | 0.15 | 0.18 | 0.17 | 0.34 | 0.41 | 0.44 | 0.37 | 0.35 |

**PERSIANN CCS** 0.13 0.10 0.11 0.11 0.13 0.12 0.11 0.28 0.34 0.35 0.30 0.29

| PERSIANN-CDR V1R1 | - | - | - | - | - | - | 0.02 | 0.06 | 0.04 | 0.03 | 0.02 | 0.03 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SM2RAIN-ASCAT V 1.2 | - | - | - | - | - | - | 0.17 | 0.29 | 0.37 | 0.36 | 0.27 | 0.25 |

**GPM+SM2RAIN** - - - - - - 0.34 0.52 0.58 0.59 0.55 0.55

97

**Table 10 –** Summary of BIAS for estimated precipitation products, considering different timescales.

**PRODUCTS / TIME** 1h 3h 6h 8h 10h 12h 1d 3d 5d 7d 9d 10d

| CHIRP V2.0 | - | - | - | - | - | - | 0.19 | 0.32 | 0.41 | 0.47 | 0.53 | 0.55 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHIRPS V2.0 | - | - | - | - | - | - | 0.30 | 0.40 | 0.49 | 0.54 | 0.58 | 0.60 |

**CMORPH-CRT V1.0** 0.22 0.31 0.35 0.35 0.36 0.36 0.35 0.44 0.50 0.54 0.57 0.58

| PDIR-NOW | 0.22 | 0.29 | 0.32 | 0.33 | 0.33 | 0.33 | 0.36 | 0.51 | 0.61 | 0.68 | 0.74 | 0.76 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMERGHEE V06 | 0.18 | 0.25 | 0.28 | 0.28 | 0.28 | 0.28 | 0.29 | 0.39 | 0.45 | 0.49 | 0.52 | 0.52 |
| IMERGHHL V06 | 0.17 | 0.26 | 0.30 | 0.30 | 0.31 | 0.31 | 0.31 | 0.41 | 0.47 | 0.51 | 0.53 | 0.54 |
| IMERGHH V06 | 0.18 | 0.26 | 0.30 | 0.31 | 0.31 | 0.31 | 0.32 | 0.43 | 0.50 | 0.54 | 0.56 | 0.57 |
| MERRA-2 | 0.08 | 0.14 | 0.18 | 0.19 | 0.21 | 0.21 | 0.25 | 0.41 | 0.51 | 0.59 | 0.64 | 0.66 |
| MSWEP V2.2 | - | 0.23 | 0.28 | - | - | 0.29 | 0.30 | 0.39 | 0.46 | 0.49 | 0.51 | 0.52 |
| PERSIANN | 0.12 | 0.20 | 0.24 | 0.25 | 0.25 | 0.25 | 0.26 | 0.35 | 0.42 | 0.46 | 0.49 | 0.50 |
| PERSIANN CCS | 0.22 | 0.27 | 0.29 | 0.30 | 0.30 | 0.30 | 0.32 | 0.43 | 0.52 | 0.57 | 0.61 | 0.62 |

| PERSIANN-CDR V1R1 | - | - | - | - | - | - | 0.21 | 0.33 | 0.42 | 0.47 | 0.51 | 0.52 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SM2RAIN-ASCAT V 1.2 | - | - | - | - | - | - | 0.13 | 0.25 | 0.33 | 0.39 | 0.44 | 0.46 |

**GPM+SM2RAIN** - - - - - - 0.24 0.37 0.45 0.49 0.53 0.54

98

**Table 11 –** Summary of Variability (VAR) for estimated precipitation products, considering different timescales**.**

**PRODUCTS / TIME** 1h 3h 6h 8h 10h 12h 1d 3d 5d 7d 9d 10d

| CHIRP V2.0 | - | - | - | - | - | - | 1.78 | 1.19 | 1.12 | 1.07 | 0.99 | 0.97 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHIRPS V2.0 | - | - | - | - | - | - | 1.83 | 1.24 | 1.15 | 1.15 | 1.08 | 1.03 |

**CMORPH-CRT V1.0** 1.87 2.01 2.08 2.09 2.09 2.08 1.91 1.37 1.29 1.25 1.21 1.17

| PDIR-NOW | 1.80 | 2.02 | 2.15 | 2.14 | 2.11 | 2.08 | 1.96 | 1.39 | 1.31 | 1.28 | 1.20 | 1.14 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMERGHEE V06 | 1.96 | 1.99 | 2.04 | 2.07 | 2.07 | 2.05 | 1.87 | 1.46 | 1.33 | 1.25 | 1.16 | 1.11 |
| IMERGHHL V06 | 2.03 | 2.06 | 2.08 | 2.10 | 2.11 | 2.09 | 1.92 | 1.48 | 1.34 | 1.26 | 1.17 | 1.12 |
| IMERGHH V06 | 1.88 | 1.91 | 1.92 | 1.93 | 1.94 | 1.94 | 1.80 | 1.40 | 1.33 | 1.30 | 1.21 | 1.16 |
| MERRA-2 | 3.01 | 3.11 | 3.04 | 2.92 | 2.86 | 2.80 | 2.47 | 1.85 | 1.74 | 1.73 | 1.58 | 1.50 |
| MSWEP V2.2 | - | 2.03 | 2.10 | - | - | 2.08 | 1.93 | 1.58 | 1.48 | 1.41 | 1.30 | 1.23 |
| PERSIANN | 1.81 | 2.13 | 2.35 | 2.37 | 2.41 | 2.40 | 2.29 | 1.85 | 1.73 | 1.62 | 1.52 | 1.50 |
| PERSIANN CCS | 1.81 | 1.81 | 1.94 | 1.95 | 1.97 | 1.95 | 1.89 | 1.51 | 1.50 | 1.42 | 1.33 | 1.28 |

| PERSIANN-CDR V1R1 | - | - | - | - | - | - | 1.70 | 1.39 | 1.41 | 1.38 | 1.25 | 1.18 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SM2RAIN-ASCAT V 1.2 | - | - | - | - | - | - | 1.49 | 1.39 | 1.39 | 1.33 | 1.20 | 1.14 |

**GPM+SM2RAIN** - - - - - - 1.40 1.17 1.15 1.11 1.03 0.99

99

**Table 12 –** Summary of KGE for estimated precipitation products, considering different timescales.

**PRODUCTS / TIME** 1h 3h 6h 8h 10h 12h 1d 3d 5d 7d 9d 10d

| CHIRP V2.0 | - | - | - | - | - | - | -0.30 | 0.11 | 0.20 | 0.23 | 0.26 | 0.27 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHIRPS V2.0 | - | - | - | - | - | - | -0.28 | 0.19 | 0.27 | 0.30 | 0.33 | 0.34 |

**CMORPH-CRT V1.0** -0.39 -0.47 -0.53 -0.53 -0.53 -0.51 -0.41 0.06 0.15 0.22 0.24 0.26

| PDIR-NOW | -0.40 | -0.51 | -0.56 | -0.54 | -0.51 | -0.49 | -0.41 | 0.14 | 0.26 | 0.31 | 0.34 | 0.36 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IMERGHEE V06 | -0.52 | -0.50 | -0.52 | -0.53 | -0.52 | -0.50 | -0.37 | 0.00 | 0.12 | 0.18 | 0.22 | 0.22 |
| IMERGHHL V06 | -0.58 | -0.56 | -0.54 | -0.55 | -0.54 | -0.52 | -0.39 | 0.00 | 0.13 | 0.19 | 0.22 | 0.23 |
| IMERGHH V06 | -0.48 | -0.45 | -0.42 | -0.41 | -0.41 | -0.39 | -0.30 | 0.08 | 0.18 | 0.23 | 0.26 | 0.27 |
| MERRA-2 | -1.45 | -1.52 | -1.44 | -1.34 | -1.29 | -1.24 | -0.95 | -0.47 | -0.36 | -0.33 | -0.22 | -0.18 |
| MSWEP V2.2 | - | -0.65 | -0.65 | - | - | -0.57 | -0.42 | 0.00 | 0.13 | 0.20 | 0.25 | 0.28 |
| PERSIANN | -0.60 | -0.70 | -0.80 | -0.79 | -0.81 | -0.79 | -0.70 | -0.25 | -0.11 | 0.00 | 0.04 | 0.04 |
| PERSIANN CCS | -0.42 | -0.41 | -0.48 | -0.48 | -0.48 | -0.47 | -0.43 | -0.05 | 0.04 | 0.12 | 0.14 | 0.15 |

| PERSIANN-CDR V1R1 | - | - | - | - | - | - | -0.44 | -0.22 | -0.19 | -0.17 | -0.12 | -0.09 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SM2RAIN-ASCAT V 1.2 | - | - | - | - | - | - | -0.29 | -0.10 | 0.00 | 0.06 | 0.06 | 0.06 |

**GPM+SM2RAIN** - - - - - - -0.08 0.19 0.29 0.34 0.35 0.36

100
