UNIVERSIDADE FEDERAL DO RIO DE JANEIRO
INSTITUTO DE GEOCIÊNCIAS
PROGRAMA DE PÓS-GRADUAÇÃO EM METEOROLOGIA




 A OCORRÊNCIA DE ALAGAMENTOS NA CIDADE DO RIO DE JANEIRO: UMA ANÁLISE BASEADA EM DADOS DO COR-RIO E DO ALERTARIO




HANNA SOARES VIANA



Exame de Qualificação de Mestrado apresentada ao Programa de Pós-graduação em Meteorologia do Instituto de Geociências do Centro de Ciências Matemáticas e da Natureza da Universidade Federal do Rio de Janeiro (PPGM IGEO-CCMN-UFRJ), como parte dos requisitos necessários à obtenção do título de Mestre em Meteorologia. 

Orientador: Prof. Dr. Fabricio Polifke da Silva 






                                                      RIO DE JANEIRO
22 de Agosto de 2025
 A OCORRÊNCIA DE ALAGAMENTOS NA CIDADE DO RIO DE JANEIRO: UMA ANÁLISE BASEADA EM DADOS DO COR-RIO E DO ALERTA RIO
HANNA SOARES VIANA

Qualificação submetida ao corpo docente do Programa de Pós-Graduação em Meteorologia do Instituto de Geociências do Centro de Ciências Matemáticas e da Natureza da Universidade Federal do Rio de Janeiro (PPGM-IGEO/CCMN/UFRJ) como parte dos requisitos necessários para a obtenção do grau de Mestre em Ciências (Área: Meteorologia)

Examinada por:

____________________________________
D.Sc. Fabricio Polifke da Silva (PPGM-IGEO-UFRJ)

____________________________________
D.Sc. Lino Augusto Sander de Carvalho (PPGM-IGEO-UFRJ)
 
____________________________________
D. Sc. Daniel Andres Rodriguez  (COPPE-UFRJ)








RESUMO

Alagamentos urbanos representam um desafio crescente para a cidade do Rio de Janeiro, exacerbados pela expansão urbana e pela intensificação de eventos meteorológicos extremos. A gestão de riscos, muitas vezes reativa, carece de ferramentas preditivas calibradas para a complexa realidade do município. Este trabalho analisou a relação empírica entre eventos de precipitação e a ocorrência de alagamentos, com o propósito de estabelecer limiares de chuva para subsidiar sistemas de alerta precoce. Para isso, foram integradas e analisadas duas bases de dados operacionais para o período de 2015 a 2024: os registros de precipitação do Sistema Alerta Rio e as ocorrências georreferenciadas de alagamentos do Centro de Operações Rio (COR-Rio). A metodologia envolveu a caracterização descritiva, a análise da distribuição espaço-temporal dos eventos e o desenvolvimento de limiares de Intensidade-Duração (I-D) com incorporação do Índice de Precipitação Antecedente (API) por sub-bacia hidrográfica. Os resultados da análise dos dados de ocorrências revelam padrões bem definidos: a maioria dos eventos (86,6%) é classificada como "Bolsão d'água", com duração predominantemente inferior a duas horas. Temporalmente, as ocorrências concentram-se no verão (47,9%) e no final da tarde, com pico entre 18h e 20h, coincidindo com o regime de chuvas convectivas da cidade. Espacialmente, os alagamentos não são aleatórios, concentrando-se em corredores urbanos e bairros específicos como Tijuca, Centro e Botafogo. A precipitação foi agregada ao nível de sub-bacia por ponderação de área (interseção dos Polígonos de Thiessen com as sub-bacias hidrográficas), e o API foi calculado com coeficiente de decaimento K = 0,85 para janelas de 1 a 10 dias antecedentes. Para 41 das 55 sub-bacias identificadas no município, foram ajustados limiares com curva exponencial intermediária I = a·e^(b·API) + c, avaliados em 10 escalas temporais (15 minutos a 24 horas). Os valores de Probabilidade de Detecção (POD) variaram de 0,14 a 1,0 e a Taxa de Alarmes Falsos (FAR) entre 0,004 e 0,52, com a maioria das sub-bacias apresentando melhor desempenho com janelas de 1 a 3 dias antecedentes. A otimização do coeficiente de decaimento K — testado nos valores 0,60; 0,70; 0,75; 0,80; 0,85; 0,90 e 0,95 — revelou que K = 0,60 é o ótimo para 34% das sub-bacias, indicando drenagem rápida e memória hidrológica curta em bacias altamente urbanizadas, enquanto valores elevados (0,90–0,95) predominam em sub-bacias com corpos d'água internos. 10 sub-bacias apresentaram melhora expressiva de desempenho em relação ao K fixo em 0,85, com destaque para o Canal do Mangue (+0,083) e Arroio Fundo/Rio Grande (+0,070). Complementarmente, a separação sazonal dos limiares — aplicada individualmente para as quatro estações meteorológicas (verão DJF, outono MAM, inverno JJA e primavera SON) — reduziu a Taxa de Alarmes Falsos média de 0,757 para 0,658 no inverno (−10 pontos percentuais), estação em que 75% das sub-bacias apresentaram K ótimo de 0,60 e janela antecedente média de apenas 1,7 dias, evidenciando a rápida drenagem do sistema no período seco. Os limiares de verão foram superiores aos anuais em 77% dos casos, refletindo a maior tolerância do sistema saturado nesta estação. Os resultados demonstram que a incorporação do API com K otimizado e a diferenciação sazonal refinam os limiares de alerta ao considerar tanto a intensidade do evento quanto o estado de saturação prévia e a sazonalidade do regime hidrológico, contribuindo para a melhoria da resiliência urbana frente a eventos extremos de chuva.
Palavras-chave: Alagamentos Urbanos; Limiar de Precipitação; Precipitação Antecedente; Análise Espaço-Temporal; Sub-bacia Hidrográfica; Rio de Janeiro; Dados Operacionais.








ABSTRACT

Urban flooding represents a growing challenge for the city of Rio de Janeiro, exacerbated by urban expansion and the intensification of extreme weather events. Risk management, often reactive, lacks predictive tools calibrated for the municipality's complex reality. This study analyzed the empirical relationship between precipitation events and flooding occurrences, aiming to establish rainfall thresholds to support early warning systems. For this purpose, two operational datasets from 2015 to 2024 were integrated and analyzed: precipitation records from the Alerta Rio System and georeferenced flooding occurrences from the Rio Operations Center (COR-Rio). The methodology involved descriptive characterization, spatiotemporal analysis of the events, and the development of Intensity-Duration (I-D) thresholds incorporating the Antecedent Precipitation Index (API) at the hydrological sub-basin scale. Results from the analysis of the occurrence data reveal well-defined patterns: the majority of events (86.6%) are classified as 'Bolsão d'água' (ponding), with a duration predominantly under two hours. Temporally, occurrences are concentrated in the summer (47.9%) and late afternoon, peaking between 6 PM and 8 PM, coinciding with the city's convective rainfall regime. Spatially, the flooding events are not random but are concentrated in specific urban corridors and neighborhoods such as Tijuca, Centro, and Botafogo. Precipitation was aggregated at the sub-basin level using area-weighted Thiessen polygon intersections, and the API was computed with a decay coefficient K = 0.85 for antecedent windows of 1 to 10 days. For 41 of the 55 sub-basins identified in the municipality, thresholds were fitted using an intermediate exponential curve I = a·e^(b·API) + c, evaluated across 10 time steps (15 minutes to 24 hours). The Probability of Detection (POD) ranged from 0.14 to 1.0 and the False Alarm Ratio (FAR) from 0.004 to 0.52, with most sub-basins performing best with 1 to 3 antecedent days. The optimization of the decay coefficient K — tested across values K ∈ {0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95} — revealed that K = 0.60 is optimal for 34% of sub-basins, reflecting fast drainage and short hydrological memory in highly impervious urban catchments, while high values (0.90–0.95) dominate in sub-basins with internal water bodies. Ten sub-basins showed meaningful performance gains over the fixed K = 0.85 baseline, with the largest improvements recorded for Canal do Mangue (+0.083) and Arroio Fundo/Rio Grande (+0.070). Further, seasonal threshold separation — fitting independent parameters for each meteorological season (Summer DJF, Autumn MAM, Winter JJA, Spring SON) — reduced the mean False Alarm Ratio from 0.757 to 0.658 in winter (−10 percentage points), the season in which 75% of sub-basins favour K = 0.60 and an average antecedent window of only 1.7 days, reflecting rapid drainage during the dry period. Summer thresholds exceeded annual thresholds in 77% of cases, consistent with greater system tolerance under the wet-season saturation regime. The results demonstrate that incorporating the API with sub-basin-optimized K and seasonal differentiation refines alert thresholds by jointly accounting for event intensity, prior hydrological saturation state, and intra-annual variability, contributing to enhanced urban resilience against extreme rainfall events.
Keywords: Urban Flooding; Rainfall Threshold; Antecedent Precipitation; Spatiotemporal Analysis; Hydrological Sub-basin; Rio de Janeiro; Operational Data.






LISTA DE FIGURAS

Figura 1 – Esquematização da Metodologia ................................................................................. ……………………………...31
Figura 2 – Método do Polígono de Thiessen aplicado na cidade do Rio de Janeiro ................ …………………………………………………………………….35
Figura 3 – Distribuição Percentual dos Tipos de Eventos ............................................................................................................................38
Figura 4 – Distribuição de duração de eventos ............................................................................................................................39
Figura 5 – Gráficos Sazonais da distribuição de Alagamentos ................................................. ……………………………………………………..40
Figura 6 – Gráfico Mensal da distribuição de Alagamentos ..................................................... …………………………………………………..41
Figura 7 – Gráfico da distribuição horária dos eventos de alagamentos ............................................................................................................................42
Figura 8 – Mapa de pontos de acúmulos d'água ............................................................................................................................43
Figura 9 – Mapa de Bairros com Ocorrências de Alagamento ............................................................................................................................44
Figura 10 – Zonas de alerta API por sub-bacia com K otimizado (curva exponencial I = a·e^(b·API) + c) ............................................................................................................................XX
Figura 11 – Limiares de Intensidade-Duração por sub-bacia com K otimizado (brutos e com tolerância) ............................................................................................................................XX
Figura 12 – Resumo sazonal dos limiares API: métricas de desempenho, limiares inferiores e distribuição do K ótimo por estação ............................................................................................................................XX
Figura 13 – Limiares de Intensidade-Duração sazonais por sub-bacia (quatro painéis: verão, outono, inverno e primavera) ............................................................................................................................XX
Figura 14 – Zonas de alerta API sazonais por sub-bacia (grade 10 passos de tempo × 4 estações) ............................................................................................................................XX


LISTA DE TABELAS

Tabela 1. Categoria de acúmulos de água em via. Fonte: COR-Rio ……………...........................................................................................................17

Tabela 2. Etapas metodológicas de limiar…………………………………………………………………………………….37

Tabela 3. Sub-bacias com melhor desempenho após otimização de K………………………………………………….XX
Tabela 4. Desempenho médio dos limiares inferiores por estação (POD, FAR e Score)…………………………….XX











SUMÁRIO

1 INTRODUÇÃO
1.1 Contextualização do Problema
1.2 Justificativa
1.3 Hipóteses e Questões de Pesquisa
1.4 Objetivos
1.4.1 Objetivo Geral
1.4.2 Objetivos Específicos
1.5 Estrutura do Trabalho
2 FUNDAMENTAÇÃO TEÓRICA
      2.1. Precipitação e sua Medição
2.1.1 Bolsões d’água: Definições, Classificações e Implicações
2.3 Regime Pluviométrico e Padrões Sazonais no Rio de Janeiro
2.4 Técnicas de Interpolação Espacial de Precipitação
2.5 Metodologias de Limiares de Precipitação                                                                     2.5.1 A Relação Intensidade-Duração de Caine (1980)                                   2.5.2 Adaptação da Abordagem I-D para Inundações Urbanas com Dados Operacionais                                                                                                           2.5.3  Análises Multivariadas para Áreas Urbanas                                                       2.5.4 Limiar com a Precipitação Antecedente                                                           2.5.5 Incerteza para limiares de chuva 
3 MATERIAIS E MÉTODOS
3.1 Área de Estudo: Município do Rio de Janeiro
3.2 Base de Dados
3.2.1 Dados Pluviométricos (Sistema Alerta Rio)
3.2.2 Registros de Ocorrência de Bolsões d’água (COR-Rio)
3.3 Tratamento, Organização e Pré-processamento dos Dados
3.4 Aplicação do Método de Thiessen
3.5 Aplicação dos Limiares
3.6 Agregação Espacial por Sub-bacia Hidrográfica
3.7 Cálculo do Índice de Precipitação Antecedente (API)
3.8 Ajuste de Limiares API por Sub-bacia
3.9 Separação Sazonal dos Limiares
3.10 Ferramentas Computacionais Utilizadas
4  RESULTADO E DISCUSSÃO
4.1 Distribuição Espacial e Temporal das Chuvas
4.2 Ocorrências de Bolsões d’água e sua Localização
4.3 Análise de Correlação entre Precipitação e Bolsões
4.3.1 Estabelecimento de Limiares de Alerta
4.3.2 Sazonalidade das Ocorrências
4.3.3 Limitações da Pesquisa
4.4 Análise API por Sub-bacia Hidrográfica
4.4.1 Cobertura Espacial e Pesos de Agregação
4.4.2 Desempenho dos Limiares API
4.4.3 Análise Sazonal dos Limiares
     PASSOS FUTUROS
     CRONOGRAMA
REFERÊNCIAS

1 INTRODUÇÃO

1.1 Contextualização do Problema

Os alagamentos urbanos representam desafios socioambientais enfrentados por grandes centros urbanos, particularmente aqueles caracterizados por um crescimento desordenado e infraestrutura deficiente. Diversos fatores contribuem para o risco de inundações. Chuvas muito fortes, problemas na infraestrutura (como esgoto sobrecarregado ou bueiros entupidos), e características do terreno (inclinação, altura, e a presença de prédios ou áreas impermeáveis). A localização se torna um fator importante: áreas costeiras, por exemplo, são mais vulneráveis, pois a água do mar pode transbordar durante as chuvas, piorando a situação com o aumento do nível do mar e tempestades (Agonafir et al., 2023)
Relatórios do Painel Intergovernamental sobre Mudanças Climáticas (IPCC) apontam que a expansão urbana, especialmente o crescimento desordenado, aumenta a vulnerabilidade das populações e da infraestrutura a eventos meteorológicos extremos, cujas frequência e intensidade tendem a se acentuar no cenário das mudanças climáticas (IPCC, 2022). 
O contexto brasileiro exemplifica a tendência global. Com mais de 87% de sua população vivendo em áreas urbanas, segundo o censo demográfico de 2022 (IBGE, 2023), os grandes centros urbanos do país estão suscetíveis à vulnerabilidade meteorológica, devido à escassez de infraestrutura adequada ao crescimento populacional. 
Na cidade do Rio de Janeiro, como na maioria dos grandes pólos urbanos, tais eventos são recorrentes e provocam impactos severos em diversas esferas, incluindo perdas materiais, interrupção da mobilidade urbana, comprometimento da saúde pública e, em situações mais graves, fatalidades. A vulnerabilidade da cidade é produto de uma combinação de fatores: a alta impermeabilização do solo, a ocupação de áreas de risco e uma topografia que favorece a rápida concentração do escoamento superficial. Chuvas intensas nas encostas dos maciços geram fluxos que convergem para as planícies costeiras, onde se localiza a maior parte da malha urbana.
A gestão de riscos opera, em grande parte, de forma reativa aos eventos. A ausência de limiares de precipitação calibrados para as diferentes realidades topográficas e urbanísticas do município limita a capacidade de emissão de alertas preventivos com antecedência e especificidade geográfica adequadas. A sobrecarga da infraestrutura de escoamento, em função de volumes pluviométricos excessivos, demanda abordagens analíticas que integrem dados meteorológicos, como os dados de estações pluviométricas do Alerta Rio, e dados de alagamento, como os registros de ocorrências de alagamento do Centro de Operações do Rio (COR). Tal integração permite a identificação de padrões e a definição de limiares de alerta, promovendo uma maior proteção da população e o embasamento das ações dos órgãos de defesa civil.
Atualmente, a falta de limiares de precipitação localizados e específicos dificulta a emissão de alertas prévios, o que compromete a capacidade de resposta das autoridades e da população. A aplicação do método de interpolação espacial para a rede de pluviômetros, correlacionando dados de chuva com a localização de alagamentos, oferece uma abordagem empírica para suprir essa deficiência. Essa metodologia permite mapear áreas de maior suscetibilidade e identificar padrões espaço-temporais entre a precipitação e a formação dos bolsões d'água e alagamentos. Ao desenvolver um limiar de intensidade-duração baseado em evidências locais, esta pesquisa contribuirá diretamente para a melhora da resiliência urbana frente a eventos extremos de chuva. Os resultados poderão ser incorporados em sistemas de alerta precoce, otimizando a alocação de recursos, a mobilização de equipes de emergência e a comunicação com a população, minimizando, assim, os prejuízos socioeconômicos e ambientais causados pelos alagamentos.


1.4 Objetivos

1.4.1 Objetivo Geral

Investigar a relação entre os eventos de precipitação e a ocorrência de alagamentos no município do Rio de Janeiro, a partir da integração de dados do Alerta Rio e do Centro de Operações da Prefeitura do Rio de Janeiro (COR-Rio), com o propósito de estabelecer relações empíricas utilizando limiares de chuva que possam subsidiar sistemas de alerta precoce e a gestão de riscos hidrológicos.

1.4.2 Objetivos Específicos

Caracterizar a espacialização dos bolsões na cidade do Rio de Janeiro, identificando as áreas mais recorrentes e suas características geográficas e urbanísticas.
Analisar a distribuição espacial e temporal dos bolsões em correlação com os padrões de chuva, utilizando técnicas de interpolação espacial para estimar a precipitação em locais não monitorados.
Estabelecer limiares de intensidade-duração da precipitação que servem como gatilho para a ocorrência dos alagamentos, considerando as particularidades das diferentes regiões da cidade, definindo curvas críticas para cada área de influência dos pluviômetros.
Avaliar a influência da precipitação antecedente na duração dos bolsões d'água, para quantificar a relação entre a saturação do sistema e o tempo de permanência dos alagamentos.



2 FUNDAMENTAÇÃO TEÓRICA

2.1  Precipitação, sua Medição e Classificação de Acúmulos d'Água

Geralmente, alagamentos são desencadeados por eventos de chuva extremos em áreas com problemas de drenagem, como ocorre em vias urbanas. Para mitigar esses impactos, com métodos de controle não estruturais, cidades e regiões metropolitanas globalmente empregam dados de sensores para emitir alertas e implementar ações preventivas. Entre os equipamentos mais comuns está o pluviômetro, um sensor que fornece informações pontuais, específicas e factuais sobre a chuva. Esses sensores, em geral, são instalados em conjunto, formando uma rede para monitoramento (SIMOYAMA,2023)
Entretanto, para monitorar através de câmeras e gerenciar os impactos na cidade do Rio de Janeiro, o COR-Rio adota uma terminologia específica para classificar os diferentes tipos de acúmulo de água nas vias urbanas, com base nos impactos sobre a circulação de pedestres e veículos.
A categoria "bolsão d'água" refere-se a situações em que o pedestre é obrigado a entrar na água para atravessar a via, embora o tráfego de veículos leves seja possível, ainda que dificultado. Já a categoria “alagamento” é caracterizada por impedir completamente o trânsito de veículos leves, sendo, portanto, um evento de maior severidade.
Além dessas categorias, o COR-Rio classifica também as poças, definidas como pequenos acúmulos de água resultantes de imperfeições na pista, que não comprometem significativamente a mobilidade. Em contrapartida, as categorias “enchente”, “inundação” e “enxurrada” referem-se a acúmulos de grande porte, com maior potencial de impacto urbano.
O protocolo operacional vigente diante da ocorrência de bolsões d'água prevê a drenagem natural do volume acumulado por meio dos sistemas de escoamento pluvial. Quando esse processo não ocorre de forma satisfatória, a Companhia Municipal de Limpeza Urbana (Comlurb) é acionada para realizar a limpeza da via e verificar a necessidade de desobstrução dos ralos pluviais.

Tabela 1. Categoria de acúmulos de água em vias. Fonte: COR-Rio



2.3 Regime Pluviométrico e Padrões Sazonais no Rio de Janeiro

A compreensão da relação entre chuva e alagamentos no Rio de Janeiro exige, primeiramente, o conhecimento do regime pluviométrico local. A cidade apresenta uma forte variação sazonal. O trimestre de novembro a janeiro concentra os maiores volumes de chuva, devido à intensificação da atuação de sistemas convectivos associados ao aquecimento superficial e à circulação marítima mais vigorosa (DERECZYNSKI et al., 2009). Em contrapartida, o período de inverno, compreendido entre junho e agosto, apresenta os menores totais pluviométricos, resultado da menor frequência de sistemas frontais e convectivos.
Particularmente, o mês de setembro destaca-se por um pico de precipitação na região do Sumaré, revelando um padrão pluviométrico em escala local. Essa anomalia pode estar relacionada à topografia específica da região e às condições atmosféricas locais.
A distribuição da precipitação ao longo do dia varia conforme a estação do ano. Durante a primavera e o verão, as chuvas ocorrem majoritariamente no período da tarde e da noite, devido ao aquecimento diurno da superfície e à intensificação da brisa marítima (DERECZYNSKI et al., 2009). Já no outono e inverno, a precipitação apresenta uma distribuição mais uniforme ao longo do dia, com predominância de eventos associados à passagem de frentes frias.

2.4 Técnicas de Interpolação Espacial de Precipitação

As redes de pluviômetros são uma referência valiosa para validar dados de precipitação. No entanto, sua limitação reside na capacidade de fornecer medições apenas em locais específicos, não conseguindo representar a distribuição espacial da precipitação em áreas maiores, como uma cidade ou uma bacia hidrográfica. Por outro lado, imagens de radar e satélite oferecem dados espacialmente contínuos, mas carecem de continuidade temporal. Para suprir essa lacuna, a interpolação espacial pode ser usada para estimar a precipitação em pontos desconhecidos a partir dos dados coletados pelos pluviômetros dentro de uma área (SIMOYAMA, 2023). Assim, para estudos que necessitam do volume de chuva para áreas vizinhas de pluviômetros, como em eventos de inundações, alagamentos e vazão de bacia hidrográfica, a análise de interpolação espacial pode ser utilizada.
Múltiplos estudos, que comparam diferentes métodos de interpolação espacial, afirmam que a escolha do método depende do objetivo do estudo, a variabilidade climatológica da região, a escala do tempo, resolução espacial desejada e o contexto territorial da região, como a densidade das redes de pluviômetros, a topografia, área rural ou urbana etc (BORGES et al. 2016).
Os métodos de interpolação podem ser classificados em duas grandes categorias: determinísticos e geoestatísticos. Os métodos determinísticos utilizam funções matemáticas para criar superfícies a partir dos pontos medidos, com base em critérios de semelhança ou grau de suavização. Já os métodos geoestatísticos, fundamentados na teoria das variáveis regionalizadas, incorporam a autocorrelação espacial dos dados para realizar as estimativas. A seguir, são descritos três dos métodos mais consolidados na literatura, em ordem crescente de complexidade: Polígonos de Thiessen, Ponderação pelo Inverso da Distância (IDW) e Krigagem.
O método dos Polígonos de Thiessen, também conhecido como método do polígono de vizinhança mais próxima, é um dos interpoladores mais simples e diretos. Seu princípio baseia-se na definição de áreas de influência para cada estação pluviométrica. Para qualquer ponto dentro de um polígono, o valor de precipitação estimado é simplesmente o valor medido na estação contida nesse mesmo polígono (THIESSEN, 1911). Sua principal vantagem reside na simplicidade conceitual e na baixa exigência computacional, sendo facilmente implementado. No entanto, sua maior limitação é a geração de uma superfície descontínua, com transições abruptas e artificiais nas bordas dos polígonos, o que não representa a variabilidade gradual da precipitação na natureza.
A Ponderação pelo Inverso da Distância (IDW), é um método determinístico que opera sob a premissa da Primeira Lei da Geografia de Tobler: "tudo está relacionado com tudo, mas coisas próximas estão mais relacionadas do que coisas distantes". O valor estimado para um ponto não medido é calculado como uma média ponderada dos valores das estações vizinhas, onde o peso atribuído a cada estação é inversamente proporcional a uma potência de sua distância até o ponto de interesse (SHEPARD, 1968). A principal vantagem do IDW é sua natureza intuitiva e a capacidade de gerar uma superfície contínua e mais suave que a dos Polígonos de Thiessen. Contudo, o método apresenta limitações significativas. A escolha do expoente da distância é subjetiva e pode alterar drasticamente o resultado. Ademais, o IDW tende a produzir o chamado "efeito olho de boi" (bull's-eye effect) ao redor das estações, e é incapaz de estimar valores superiores ao máximo ou inferiores ao mínimo observado na amostra de dados, o que pode subestimar picos de precipitação.
Finalmente, a Krigagem representa a abordagem geoestatística mais robusta para a interpolação espacial. Diferentemente dos métodos determinísticos, seu princípio não se baseia apenas na distância, mas na estrutura de autocorrelação espacial dos dados, quantificada por meio do semivariograma. O semivariograma modela o grau de dependência espacial entre as amostras e é utilizado para calcular os pesos ótimos que resultam na melhor estimativa linear não enviesada (ISAAKS; SRIVASTAVA, 1989). A principal vantagem da Krigagem é sua fundamentação estatística, que não apenas fornece uma estimativa, mas também uma medida da incerteza associada a essa estimativa (a variância da krigagem). Além disso, variações como a Krigagem Universal podem incorporar tendências (como o efeito da altitude), e a Co-krigagem pode utilizar variáveis secundárias correlacionadas para melhorar a estimativa (Abo-Monasar & Al-Zahrani, 2014). Suas desvantagens, no entanto, residem na sua complexidade teórica e operacional. O método exige um número razoável de dados para a construção de um semivariograma confiável, e a modelagem do mesmo envolve um grau de subjetividade. 

2.5. Metodologias de Limiares de Precipitação

Limiares de precipitação podem ser utilizados como uma estratégia para criação de sistemas de alertas para desastres hidrológicos urbanos. Podendo correlacionar a relação entre a chuva e ocorrências de alagamentos. Ajudando a tomada de decisão de cidades, mobilizações de emergência e regras operacionais. Dada a sua importância, a literatura científica sobre o tema é extensa e abrange diversas abordagens metodológicas.
A escolha por uma abordagem empírica para a definição de limiares de precipitação, deve ser fundamentada não apenas em seus parâmetros, mas também em uma compreensão clara de suas alternativas. A literatura científica classifica as metodologias de definição de limiares em um espectro que vai do puramente estatístico ao fisicamente baseado. Demonstrar conhecimento sobre esse espectro é crucial para validar a escolha metodológica como uma decisão informada e adequada ao problema e aos dados disponíveis.
O artigo de Montesarchio et al. (2015), oferece uma análise comparativa direta e detalhada que serve como um guia para essa contextualização. O estudo se propôs a comparar explicitamente o desempenho de três famílias de métodos para a definição de limiares de inundação, aplicando-as a três bacias hidrográficas na Itália. As abordagens analisadas foram:
Método Empírico: Baseado na análise de dados históricos de chuva e inundações para traçar uma curva de lei de potência (similar à de Caine) que separa eventos com e sem desastres. Sua principal vantagem é a simplicidade e a baixa exigência de dados.
Método Hidrológico: Utiliza um modelo hidrológico calibrado (no caso, o HEC-HMS) para determinar, por meio de simulações inversas, qual a quantidade e o padrão de chuva necessários para gerar uma vazão crítica (de inundação) em um ponto específico da bacia. Sua vantagem é a representação mais realista dos processos físicos.
Método Probabilístico: Emprega a teoria da decisão Bayesiana e a teoria da entropia para definir um limiar que minimiza um "risco" ou "custo" esperado, considerando as probabilidades de acertos, alarmes falsos e falhas. Sua vantagem é a quantificação explícita da incerteza.
Os resultados da comparação mostraram que cada método possui um balanço distinto entre precisão e complexidade. O método probabilístico (entropia de risco) apresentou o melhor desempenho geral, com a maior taxa de sucesso e a menor taxa de alarmes falsos. Contudo, é o mais complexo de implementar. O método hidrológico também teve um bom desempenho, mas depende criticamente da disponibilidade de dados para calibração. O método empírico, embora o mais simples, mostrou-se eficaz, especialmente quando a disponibilidade de dados é limitada. A principal conclusão do artigo é que não existe um método universalmente "melhor"; a escolha depende do objetivo, do contexto e, fundamentalmente, da qualidade e quantidade dos dados disponíveis.
Complementando essa visão, a revisão sistemática de Henao Salgado & Zambrano Nájera (2022), reforça e atualiza essa classificação. Analisando 19 estudos de caso recentes, as autoras categorizam os métodos em quatro tipos: empírico, hidrológico/hidrodinâmico, probabilístico e composto (que combina elementos dos outros). A revisão confirma que, embora os modelos hidrodinâmicos sejam considerados mais robustos por sua base física, os métodos empíricos continuam sendo essenciais e amplamente utilizados, especialmente como uma primeira aproximação, em contextos urbanos complexos ou em cenários com dados limitados.
A abordagem empírica é a mais direta, operacionalmente viável e cientificamente validada para atingir os objetivos propostos. A utilização de uma método de alerta de inundação baseada em limiares de precipitação de um rede de pluviômetros geram uma vantagem operacional. Nesse contexto, a precipitação é o principal gatilho para alagamentos urbanos. Eles se baseiam na comparação direta da chuva observada com valores de referência pré-definidos, gerando uma resposta binária, limiar excedido ou não. Essa simplicidade permite que tomadores de decisão atuem rapidamente, sem a necessidade de formação técnica aprofundada em modelagem hidrológica (Montesarchio et al., 2015). No entanto, a eficácia de um sistema de alerta depende da capacidade de traduzir esses dados pontuais em ações práticas.

2.5.1 A Relação Intensidade-Duração de Caine (1980)

O ponto de partida para a análise de limiares empíricos de precipitação é o trabalho de Nel Caine, publicado em 1980, intitulado "The Rainfall Intensity: Duration Control of Shallow Landslides and Debris Flows". O problema que Caine se propôs a resolver foi a ausência de um critério quantitativo e generalizável para definir a "chuva crítica" capaz de deflagrar deslizamentos de terra superficiais e fluxos de detritos. Ele partiu da premissa de que o gatilho para esses eventos não era simplesmente a chuva total acumulada, nem uma intensidade instantânea máxima, mas sim uma combinação funcional de intensidade e duração.
O resultado principal do estudo foi a definição de uma curva-limite que separa, no gráfico I-D, as condições de chuva que resultaram em deslizamentos daquelas que, presumivelmente, não o fariam. Essa fronteira foi expressa pela equação de lei de potência:

I = α *D- β   

Onde (I) é a intensidade da chuva (mm/h), (D) é a duração (h), e (α) e (β) são parâmetros empíricos que definem a posição e a inclinação da curva que separa os eventos que deflagraram desastres daqueles que não o fizeram.

2.5.2 Adaptação da Abordagem I-D para Inundações Urbanas com Dados Operacionais

A estrutura conceitual de Caine (1980), embora fundamental, foi desenvolvida para um contexto de deslizamentos. A sua aplicação em sistemas de alerta para inundações urbanas exigiu adaptações, principalmente no que diz respeito à fonte de dados utilizada para validar a ocorrência dos desastres. Estudos mais recentes passaram a utilizar dados operacionais de alta frequência, gerados por agências municipais e serviços de emergência, para calibrar limiares locais e específicos, tornando-os mais representativos da realidade urbana.
Um exemplo dessa abordagem é o trabalho de Georganta et al. (2022), que definiu limiares de precipitação para a identificação de inundações na região da Ática, na Grécia. O problema central do estudo era atualizar e refinar os limiares existentes, utilizando um período de dados mais longo (2005-2017) e uma metodologia mais robusta. A principal contribuição metodológica foi o uso de dados do Corpo de Bombeiros Helênico como um proxy para a ocorrência de inundações. Os autores estabeleceram um critério estatístico para definir um "dia de inundação": um dia era classificado como tal se o número de chamadas de emergência relacionadas a inundações em uma determinada sub-bacia excedesse um valor limiar (calculado como o percentil 95 do número de chamadas diárias, resultando em aproximadamente 6 chamadas/dia). Com essa classificação, cada evento de chuva, identificado a partir de uma rede de 17 pluviômetros, pôde ser rotulado como "indutor de inundação" ou "não indutor de inundação". Ao plotar todos os eventos em um gráfico I-D, os autores definiram duas curvas de limiar, em vez de apenas uma. A curva inferior separava os eventos que certamente não causariam inundações, enquanto a curva superior identificava as condições de chuva acima das quais as inundações eram altamente prováveis. O espaço entre as duas curvas foi definido como uma zona de "condições mistas", onde a ocorrência de inundações é incerta e depende de outros fatores locais. 
Na mesma linha de pesquisa é apresentada por Tian et al. (2019), que inferiram limiares de precipitação para inundações pluviais urbanas a partir de observações de cidadãos em Roterdã. O desafio era extrair um sinal claro de um banco de dados massivo (70.000 relatos de inundações por cidadãos ao longo de 10 anos), que, por sua natureza, contém mais ruído e incerteza do que dados oficiais. Para isso, os autores correlacionaram os dias com alto número de relatos (>20 relatos/dia) com dados de radar de alta resolução espacial e temporal. Em vez de um ajuste visual de curvas, a metodologia empregou modelos de aprendizado de máquina (árvores de decisão) para identificar objetivamente quais características da chuva melhor separavam os dias com e sem inundação. Os modelos foram treinados usando as intensidades de pico de chuva em nove escalas temporais diferentes, de 5 minutos a 24 horas. O resultado mais significativo foi que os modelos de árvore de decisão, de forma consistente, selecionaram uma combinação de intensidades de chuva de curta duração (como 5 minutos) e de longa duração (como 24 horas) como os preditores mais importantes. Essa descoberta fornece uma prova quantitativa de que tanto o pico de intensidade (o "impacto" imediato da chuva) quanto o volume acumulado (a "saturação" do sistema) são cruciais para o gatilho de inundações urbanas. 

2.5.3  Análises Multivariadas para Áreas Urbanas

Apesar da ampla aplicação dos limiares baseados em chuva, a abordagem carrega uma premissa implícita: a de que a precipitação é o único fator determinante para a ocorrência de alagamentos. No entanto, o ambiente urbano é um sistema complexo onde a vulnerabilidade a inundações é modulada por uma interação de fatores meteorológicos, de infraestrutura e sociais. O trabalho de DeSouza et al. (2024), aborda essa questão de forma crítica e detalhada, para a necessidade de análises multivariadas.
O estudo, realizado na cidade de Denver, Colorado, partiu de uma causa: uma análise inicial para estabelecer um limiar de precipitação de variável única, similar às abordagens clássicas, apresentou um desempenho muito baixo. Utilizando o Coeficiente de Correlação de Matthews (MCC) como métrica de desempenho, os autores descobriram que nenhum limiar de intensidade ou duração da chuva conseguia distinguir de forma confiável entre tempestades que geraram relatos de inundação e aquelas que não o fizeram. O melhor desempenho obtido foi próximo ao de uma previsão aleatória, indicando que, para Denver, a chuva por si só era um preditor insuficiente.
Diante dessa limitação, a metodologia avançou para uma abordagem multivariada, utilizando um modelo de regressão logística. O objetivo era modelar a probabilidade de uma tempestade resultar em um relato de inundação, considerando um conjunto diversificado de variáveis preditoras. Essas variáveis foram agrupadas em três categorias: (I) Características da Tempestade: Intensidade máxima de precipitação em 5 minutos, profundidade total e duração da tempestade, (II) Características do Ambiente Construído: Densidade da tubulação de águas pluviais e porcentagem de área impermeável, (III) Características Sociais: Densidade populacional e renda média do setor censitário.
Os resultados da regressão logística representam a principal contribuição do artigo. A análise identificou que a intensidade máxima de precipitação em 5 minutos é o preditor mais forte, confirmando a importância do pico de intensidade como gatilho. No entanto, a densidade populacional emergiu como o segundo preditor mais forte, com um coeficiente de magnitude quase tão grande quanto o da intensidade da chuva. Outras variáveis significativas, em ordem de importância, foram a profundidade da tempestade, a duração, a renda média e a densidade da tubulação.
As variações nos limiares que serão encontradas entre as diferentes áreas de influência dos pluviômetros poderão ser explicadas não apenas por diferenças na chuva ou na topografia, mas também por fatores socioeconômicos e de infraestrutura. O trabalho de DeSousa et al. (2024) justifica a necessidade de desenvolver limiares locais e específicos, pois prova que a vulnerabilidade a alagamentos é uma função de características que variam espacialmente pela cidade.

2.5.4 Limiar com a Precipitação Antecedente

Uma limitação da abordagem de Intensidade-Duração (I-D) é que ela analisa cada evento de chuva como um episódio isolado, desconsiderando as condições de umidade pré-existentes no sistema hidrológico. Intuitivamente, um solo já saturado por chuvas recentes ou um sistema de drenagem urbana que ainda não escoou completamente um evento anterior atingirá sua capacidade crítica com um volume de chuva subsequente menor. Para incorporar essa "memória" do sistema e refinar fisicamente os modelos empíricos é a inclusão da Precipitação Antecedente (API).
O estudo de Ramos Filho et al. (2021), apresenta uma aplicação conceito. O problema que os autores buscaram resolver foi a alta incerteza e o número significativo de alarmes falsos que ocorrem na "zona de condições mistas",  a área entre os limiares superior e inferior nos gráficos I-D, onde a ocorrência de inundações é ambígua.
A metodologia proposta vai além de simplesmente adicionar a API como uma terceira variável em um gráfico 3D. O estudo introduz um "limiar intermediário" dinâmico, cuja posição depende das condições antecedentes. Esse limiar é definido por uma curva exponencial que relaciona a intensidade de pico da chuva (I) com o valor da API, geralmente na forma:

I = a ⋅ e(b ⋅ API)+ c

Onde (a), (b) e (c) são constantes ajustadas empiricamente. Essa abordagem permite que o limiar que separa as condições de inundação e não inundação se mova: para uma API baixa (sistema seco), uma intensidade de chuva maior é necessária para cruzar o limiar; para uma API alta (sistema úmido), uma intensidade de chuva muito menor já é suficiente para deflagrar um alerta. A análise foi aplicada a um banco de dados de inundações e chuvas no estado de São Paulo, testando a correlação para diferentes janelas de tempo de intensidade de pico (de 10 minutos a 24 horas) e diferentes períodos de cálculo da API (de 1 a 10 dias).
Os resultados demonstraram a eficácia da abordagem. A inclusão da API e da curva exponencial intermediária melhorou significativamente o desempenho preditivo dos limiares. Para inundações, a melhor correlação foi encontrada entre a intensidade de pico de 8 horas e a API de 8 dias, resultando em uma Probabilidade de Detecção (POD) de 81% e um Valor Preditivo Positivo (PPV) de 82%. Esses valores representam um aumento médio de 14% na POD em comparação com os limiares que não consideram a API. Além disso, a metodologia conseguiu excluir corretamente 63% das não ocorrências da zona de incerteza, reduzindo drasticamente o potencial de alarmes falsos.
.A análise de Ramos Filho et al. (2021) justifica por que a inclusão da API é uma validação necessária para aumentar a precisão dos limiares de alerta. A abordagem de definir curvas I-D que variam em função da API é um refinamento que pode explicar por que, em ambientes urbanos, chuvas de intensidade aparentemente moderada por vezes causam grandes alagamentos, elas podem estar ocorrendo sobre um sistema já saturado por eventos de chuva anteriores.

2.5.5 Incerteza para limiares de chuva 

A qualidade de qualquer limiar de precipitação, independentemente do método estatístico utilizado para derivá-lo, é criticamente dependente da qualidade e da representatividade dos dados de chuva que o alimentam. A literatura recente tem se aprofundado nas nuances relacionadas às fontes de dados (pluviômetros, satélites, radar) e à escala espacial da análise, destacando como essas escolhas metodológicas impactam diretamente o resultado final.
O estudo de Kampf et al. (2018), embora realizado em um contexto climático distinto (regiões áridas do Arizona), oferece conclusões de relevância sobre a escala espacial da medição de chuva. O problema central investigado foi como a escolha da fonte de dados de chuva, um único pluviômetro mais próximo versus a média de uma rede de pluviômetros ou dados de radar que afeta os limiares de precipitação para a geração de escoamento. A metodologia consistiu em comparar os limiares calculados usando diferentes fontes de dados para bacias hidrográficas de tamanhos variados.
O resultado mais importante do estudo foi a demonstração quantitativa de que o uso de um único pluviômetro é adequado apenas para bacias hidrográficas muito pequenas (geralmente <1 km²). Para áreas maiores, o uso de um único ponto de medição tende a superestimar significativamente o limiar necessário para gerar escoamento. Isso ocorre porque tempestades, especialmente as convectivas, são espacialmente heterogêneas, e um único pluviômetro pode não capturar a chuva que caiu em outras partes da bacia. A conclusão dos autores é que, para bacias maiores, é essencial utilizar uma média da rede de pluviômetros ou dados de radar para obter uma estimativa espacialmente representativa da chuva. 
Aprofundando a questão das fontes de dados, o trabalho de Rossi et al. (2017), foca na comparação entre limiares derivados de pluviômetros e de satélites, além de propor métodos para quantificar a incerteza. O estudo foi motivado pela crescente disponibilidade de estimativas de chuva por satélite e pela necessidade de avaliar sua utilidade para a previsão de desastres. A metodologia envolveu a definição de limiares para deslizamentos na região da Úmbria, Itália, usando três métodos estatísticos distintos (Mínimos Quadrados, Regressão Quantílica e Mínimos Quadrados Não Lineares) e duas fontes de dados: uma rede de 60 pluviômetros e estimativas do satélite TRMM.
Os resultados mostraram consistentemente que os limiares derivados de dados de satélite eram mais baixos do que os derivados de pluviômetros. Essa diferença é explicada pela tendência conhecida dos satélites de subestimarem a intensidade de chuvas fortes e localizadas. O estudo também concluiu que o método de Mínimos Quadrados Não Lineares (NLS) foi o mais robusto para ajustar as curvas de limiar aos dados. A principal contribuição deste artigo para a presente dissertação é o enriquecimento da discussão sobre as limitações e incertezas dos dados. Embora este trabalho utilize uma rede de pluviômetros, a análise de Rossi et al. (2017) destaca que mesmo essa fonte de dados não é perfeita e que a densidade da rede é um fator crítico. 
























3 MATERIAIS E MÉTODOS

Esta seção detalha os materiais e métodos empregados para a análise de eventos de chuva e alagamentos urbanos no município do Rio de Janeiro. Descreve-se a área de estudo, as bases de dados utilizadas, as ferramentas computacionais, os procedimentos de tratamento e pré-processamento dos dados, a técnica de análise espacial para a rede de pluviômetros aplicada aos registros de inundação e os respectivos limiares de alagamentos (Figura 3).



                           Figura 1. Esquematização da Metodologia



3.1 Área de Estudo: Município do Rio de Janeiro
O presente estudo tem como foco a cidade do Rio de Janeiro, localizada na região Sudeste do Brasil. A cidade possui uma geografia caracterizada por uma extensa faixa litorânea, maciços costeiros, planícies e bacias hidrográficas internas, que influenciam os padrões de precipitação e a suscetibilidade a inundações. Com uma alta densidade populacional  5.174,60 hab/km² e urbanização intensa, particularmente em vias públicas, o Rio de Janeiro enfrenta eventos recorrentes de chuvas extremas.

3.2 Base de Dados

Este estudo adota uma abordagem quantitativa e descritiva para investigar a relação entre os volumes de precipitação e a ocorrência de alagamentos na cidade do Rio de Janeiro. Para isso, foram utilizados dados primários provenientes de duas fontes principais: o COR-Rio e o sistema Alerta Rio.
Os dados de alagamentos foram obtidos junto ao COR-Rio, que mantém um banco de informações georreferenciadas com registros de eventos de acúmulo de água, classificados segundo sua severidade (poças, bolsões, alagamentos e enchentes) e com indicação de data, hora e localização. Esses dados compreendem registros de eventos ocorridos em diferentes regiões do município ao longo do período de análise.
Em paralelo, foram coletados os dados pluviométricos disponibilizados pelo sistema Alerta Rio, composto por uma rede de pluviômetros automáticos distribuídos em pelos bairros da cidade. Esses instrumentos fornecem medições contínuas e de alta resolução temporal da precipitação acumulada, permitindo a identificação de períodos de chuvas intensas.



3.2.1 Dados Pluviométricos (Sistema Alerta Rio)
Os dados de precipitação foram obtidos do Sistema Alerta Rio, mantido pela Fundação Instituto de Geotécnica do Município do Rio de Janeiro (Geo-Rio). Esta base de dados consiste em registros de acumulado de chuva em diferentes intervalos temporais, coletados por uma rede de estações pluviométricas distribuídas pelo município. Para este estudo, foram utilizados dados de precipitação acumulada a cada 15 minutos, provenientes de 33 estações pluviométricas. A seleção das estações baseou-se na disponibilidade de medições. As informações cadastrais das estações, como identificador, nome, coordenadas geográficas (latitude e longitude) e cota, também foram disponibilizadas pelo Alerta Rio e utilizadas para georreferenciar os dados e durante a aplicação de métodos de espacialização da chuva. A série histórica original dos dados brutos compreende um período extenso, sendo que, para as análises de eventos de chuva e correlações com ocorrências de alagamento, considerou-se o período coincidente com os registros de alagamentos disponíveis, iniciando-se em janeiro de 2015 até dezembro de 2024.
A série temporal contínua foi segmentada em eventos de chuva discretos para permitir a análise de Intensidade-Duração. Um evento de chuva foi definido como um período com registros de precipitação contínuos, separado do evento seguinte por um período seco de, no mínimo, 6 horas. Para cada evento de chuva identificado em cada estação, foram calculados dois parâmetros fundamentais:
Duração (D): O tempo total, em horas, desde o primeiro até o último registro de chuva do evento.
Intensidade Máxima (I): A maior taxa de precipitação registrada durante o evento, calculada como o maior acumulado de chuva em um intervalo de 1 hora (quatro medições consecutivas de 15 minutos), expressa em mm/h.

3.2.2 Registros de Ocorrência de Bolsões d’água (COR-Rio)
Os registros de ocorrências relacionadas a alagamentos e inundações foram fornecidos pelo Centro de Operações Rio (COR-Rio), órgão responsável pelo monitoramento e gerenciamento de eventos na cidade. Esses registros incluem informações como tipo de ocorrência, localização (bairro, coordenadas geográficas), data e hora de início e fim do evento, descrição e, em alguns casos, classificação de gravidade e prazo para solução. A base de dados de ocorrências, fornecida pelo COR-Rio, continha um total de 87620 registros para o período analisado, que estende-se de 10/04/2015 a 26/03/2024. Foram selecionados os 4868 registros com tipo de ocorrência relacionado a alagamento urbano, especificamente "Bolsão d'água em via" (86,6%), seguidas por "Lâmina d'água" (3,8%) e "Alagamento" (9,6%), que foram reunidos em apenas um grupo para análise.
A limpeza de dados realizada removeu registros duplicados (mesmo local e horário de início) e ocorrências que não possuíam coordenadas geográficas válidas. Para cada ocorrência, a duração do alagamento foi calculada como a diferença entre o horário de fim e o horário de início do registro, fornecendo uma métrica da persistência do evento.

3.4 Aplicação do Método de Thiessen

O método dos Polígonos de Thiessen foi escolhido devido à sua simplicidade e eficácia em atribuir uma área de influência a cada ponto de medição de forma determinística. Essa abordagem é adequada para a finalidade deste estudo, que busca associar cada ocorrência de alagamento ao pluviômetro mais próximo e representativo.
Neste estudo, os polígonos de Thiessen foram gerados de forma estática, ou seja, utilizando o conjunto de estações pluviométricas ativas e com dados precipitação disponíveis durante o período de análise. As coordenadas (projetadas) das estações serviram como base para a geração dos diagramas de Voronoi. Os polígonos resultantes foram então formatados dentro do limite municipal do Rio de Janeiro, garantindo que apenas as áreas de influência dentro da cidade fossem consideradas.


Figura 2. Método do Polígono de Thiessen aplicado na cidade do Rio de Janeiro 

3.5. Associação Espaço-Temporal dos Dados

Após o tratamento individual, as bases de dados de chuva e de alagamentos foram associadas para estabelecer uma relação de causa e efeito. O processo de associação foi realizado em duas etapas:
Associação Espacial: Cada registro de alagamento georreferenciado foi associado ao Polígono de Thiessen em que estava contido. Dessa forma, cada alagamento foi vinculado a um único pluviômetro de influência.
Associação Temporal: Um evento de chuva foi considerado o gatilho para um alagamento se o horário de início do alagamento ocorreu durante o período do evento de chuva. Este procedimento resultou em um banco de dados unificado, onde cada evento de alagamento foi pareado com as características (Intensidade e Duração) do evento de chuva que o provocou.


3.6 Aplicação dos Limiares

Para cada pluviômetro, os limiares de alerta foram estabelecidos empiricamente a partir da análise de gráficos de Intensidade-Duração (I-D) baseado na metodologia de Georganta et al. (2022). O procedimento foi o seguinte:

Construção do Gráfico de Dispersão: Para cada estação, todos os eventos de chuva identificados foram plotados em um gráfico com eixos em escala logarítmica, representando a Intensidade Máxima (I, em mm/h) no eixo vertical e a Duração (D, em horas) no eixo horizontal.
Classificação dos Eventos: Cada ponto no gráfico foi classificado em uma de duas categorias, com base na associação espaço-temporal descrita na seção 3.5:
Evento com Alagamento (EA): Pontos representando chuvas que resultaram em, pelo menos, um registro de alagamento no seu respectivo polígono.
Evento sem Alagamento (ESA): Pontos representando chuvas que não geraram registros de alagamento.
Definição da Curva de Limiar: Uma curva de limiar, seguindo o modelo de lei de potência I = a ⋅ D⁻ᵇ, foi ajustada visualmente no gráfico para separar a região com alta densidade de EAs (acima da curva) da região dominada por ESAs (abaixo da curva). Os parâmetros a e b foram definidos para cada estação, buscando maximizar a taxa de detecção de alagamentos (EAs acima da curva) e minimizar a taxa de alarmes falsos (ESAs acima da curva).





Tabela 2. Quadro de etapas metodológicas de limiar

Etapa 1: Preparação e Associação
Etapa 2: Análise e Classificação
Etapa 3: Modelagem e Resultado
1. Dados de Entrada: Rede de Pluviômetros (Alerta Rio)
 Pontos de Alagamento (COR-Rio)
3. Análise da Chuva: Para cada evento de chuva, calcular pares de (Intensidade Máx, Duração).
5. Construção do Gráfico I-D: Plotar todos os eventos de chuva em um gráfico log-log.
2. Associação Espacial:  Gerar Polígonos de Thiessen.  Atribuir cada ponto de alagamento ao seu pluviômetro mais próximo.
4. Classificação dos Eventos: Com Alagamento (EA): Chuva que coincidiu com ≥ 1 ocorrência no seu polígono. Sem Alagamento (ESA): Chuva que não teve ocorrências no polígono.
6. Definição do Limiar: Ajustar curvas (I = a ⋅ D⁻ᵇ) para separar as zonas de eventos EA e ESA, gerando os limiares críticos de alerta para cada pluviômetro do Rio de Janeiro.




3.6 Agregação Espacial por Sub-bacia Hidrográfica

Para superar a limitação de associar cada ocorrência de alagamento a um único pluviômetro, a precipitação foi agregada ao nível de sub-bacia hidrográfica. Os pesos de influência de cada estação foram calculados pela interseção geométrica entre os Polígonos de Thiessen e os polígonos das sub-bacias do município, de modo que o peso de cada estação i para uma dada sub-bacia é proporcional à fração da área da sub-bacia coberta por seu respectivo polígono:

P_sb = Σ(w_i × P_i)

onde P_sb é a precipitação representativa da sub-bacia, P_i é a precipitação medida na estação i e w_i é o peso correspondente, com Σw_i = 1. Esse procedimento resultou em 149 pares estação–sub-bacia distribuídos entre as 55 sub-bacias identificadas no município, com sub-bacias de cobertura múltipla recebendo contribuições ponderadas de duas ou mais estações.

Para cada sub-bacia e dia com precipitação diária total superior a 10 mm, foram calculadas as intensidades de pico para 10 durações distintas: 15 minutos, 30 minutos, 1, 2, 3, 6, 8, 10, 12 e 24 horas. As ocorrências de alagamento foram associadas às sub-bacias por junção espacial, e cada dia foi classificado como Evento com Alagamento (EA), quando havia pelo menos um registro de bolsão na sub-bacia, ou Evento Sem Alagamento (ESA) em caso contrário. Sub-bacias com cobertura insuficiente de dados pluviométricos ou histórico de alagamentos insuficiente (número de registros EA < 1) foram excluídas da etapa de ajuste.


3.7 Cálculo do Índice de Precipitação Antecedente (API)

Seguindo a metodologia proposta por Ramos Filho et al. (2021), calculou-se o Índice de Precipitação Antecedente (API) para cada sub-bacia, com o objetivo de incorporar a "memória" do sistema hidrológico ao processo de definição dos limiares. O API quantifica o nível de saturação prévia do sistema, ponderando as chuvas dos dias anteriores por um coeficiente de decaimento exponencial. Para um dado dia t, o API com janela de n dias é definido como:

API_n(t) = Σ_{i=1}^{n} K^i × P(t−i)

onde P(t−i) é o total de precipitação da sub-bacia no dia t−i e K é o coeficiente de decaimento (K = 0,85). O valor de K = 0,85 pondera progressivamente a influência das chuvas mais antigas, atribuindo maior relevância aos dias mais recentes. Foram calculados valores de API para janelas de 1 a 10 dias antecedentes, permitindo identificar, para cada sub-bacia e duração, a janela temporal que maximiza o desempenho preditivo.


3.8 Ajuste de Limiares API por Sub-bacia

Para cada combinação de sub-bacia, duração e janela antecedente, ajustou-se uma curva exponencial intermediária seguindo a abordagem de Ramos Filho et al. (2021):

I = a · e^(b · API) + c

onde I é a intensidade de pico da chuva (mm/h) e os parâmetros a, b e c foram determinados por busca em grade (grid search). Foram definidos dois limiares fixos de intensidade — um superior e um inferior — calculados, respectivamente, como o máximo das intensidades ESA (limiar superior bruto) e o mínimo das intensidades EA (limiar inferior bruto), com versões alternativas usando o percentil 99 e o percentil 5 para incorporar tolerância estatística. A curva exponencial intermediária delimita quatro zonas de alerta:

(i) Zona vermelha: acima do limiar superior — alta probabilidade de alagamento;
(ii) Zona laranja: entre a curva exponencial e o limiar superior — probabilidade elevada;
(iii) Zona amarela: entre o limiar inferior e a curva — probabilidade moderada;
(iv) Zona azul: abaixo do limiar inferior — baixa probabilidade de alagamento.

O desempenho de cada combinação foi avaliado por três métricas clássicas de verificação de previsão binária:

- POD (Probability of Detection): TP / (TP + FN) — fração dos eventos de alagamento corretamente detectados;
- FAR (False Alarm Ratio): FP / (FP + TN) — fração de alarmes disparados sem ocorrência real;
- PPV (Positive Predictive Value): TP / (TP + FP) — precisão dos alarmes emitidos.

A seleção dos parâmetros ótimos para cada sub-bacia e duração foi realizada maximizando a função score = POD × PPV × (1 − FAR), que penaliza simultaneamente alarmes falsos e detecções perdidas.

Uma extensão metodológica em relação à abordagem original de Ramos Filho et al. (2021) diz respeito ao coeficiente de decaimento K. Enquanto estudos anteriores adotam K fixo em 0,85, este trabalho incorpora K como parâmetro de busca, avaliando os valores K ∈ {0,60; 0,70; 0,75; 0,80; 0,85; 0,90; 0,95}. A motivação é que sub-bacias com drenagem mais rápida ou menor capacidade de retenção do solo podem responder melhor a valores baixos de K — que atribuem pouca memória aos dias mais distantes — enquanto sub-bacias com corpos d'água internos ou solo mais permeável podem se beneficiar de valores elevados de K, que prolongam a influência das chuvas antecedentes. O K ótimo é determinado conjuntamente com a janela antecedente (n_dias) e os parâmetros da curva exponencial (a, b, c), ampliando o espaço de busca para 7 × 10 = 70 combinações K × n_dias por sub-bacia e duração.


3.9 Separação Sazonal dos Limiares

A abordagem descrita na seção 3.8 ajusta um único conjunto de parâmetros para cada combinação sub-bacia × duração utilizando todos os eventos do período 2015–2024. Essa configuração ignora a variabilidade intra-anual do regime hidrológico: no verão, o solo pode estar previamente saturado por chuvas convectivas frequentes, reduzindo a intensidade necessária para gerar alagamento; no inverno, a baixa frequência de precipitação mantém o sistema mais drenado, de modo que limiares mais altos são esperados para as mesmas escalas temporais.

Para incorporar esse efeito, aplicou-se o mesmo procedimento de ajuste separadamente para cada uma das quatro estações meteorológicas do hemisfério Sul:

- Verão (DJF): dezembro, janeiro e fevereiro;
- Outono (MAM): março, abril e maio;
- Inverno (JJA): junho, julho e agosto;
- Primavera (SON): setembro, outubro e novembro.

Cada evento do banco de dados foi atribuído à sua respectiva estação com base no mês da data de ocorrência. Para cada combinação sub-bacia × estação × duração, repetiu-se integralmente a busca em grade de K ∈ {0,60; 0,70; 0,75; 0,80; 0,85; 0,90; 0,95} e janelas antecedentes de 1 a 10 dias, com os mesmos critérios de métricas e score. Foram mantidos requisitos mínimos de amostra — pelo menos 3 eventos EA e 3 eventos ESA por estação — abaixo dos quais o ajuste não é realizado e o limiar anual serve como alternativa operacional. Os resultados sazonais são avaliados pelas mesmas métricas (POD, FAR, PPV e Score) e comparados aos valores anuais para quantificar o ganho introduzido pela separação estacional.


3.10 Ferramentas Computacionais Utilizadas
Todas as etapas de processamento, análise de dados e geração de visualizações foram conduzidas utilizando a linguagem de programação Python (versão 3.10). As principais bibliotecas empregadas incluem: Pandas, para manipulação e análise de dados tabulares e séries temporais; GeoPandas, para manipulação de dados geoespaciais; NumPy, para operações numéricas; SciPy, especificamente scipy.spatial para a geração dos diagramas de Voronoi (base para os polígonos de Thiessen); Matplotlib e Seaborn, para a criação de gráficos; e Cartopy, para a elaboração de mapas.

4 RESULTADO E DISCUSSÃO
                                                                                          
Este capítulo apresenta os resultados obtidos a partir da análise descritiva e espaço-temporal dos dados de alagamentos fornecidos pelo COR-Rio para o período de 2015 a 2024. Seu objetivo é caracterizar a natureza, a frequência e a distribuição desses eventos no município do Rio de Janeiro.

4.1 Caracterização Geral das Ocorrências de Alagamento

A análise da tipologia dos eventos (Figura 3) revela que a grande maioria dos registros, correspondendo a 86,6%, é classificada como "Bolsão d'água em via". Eventos de maior severidade, classificados como "Alagamento”, representam uma parcela significativamente menor, com 9,6%. Essa distribuição indica que o problema mais recorrente monitorado pelo COR-Rio são os acúmulos de água de menor escala, que impactam diretamente a mobilidade urbana, mas não necessariamente caracterizam inundações de grande escala.


          Figura 3. Distribuição Percentual dos Tipos de Eventos 

A distribuição da duração dos eventos (Figura 4) demonstra que a maioria dos alagamentos é de curta a média permanência. O intervalo de 1 a 2 horas concentra o maior número de ocorrências (1.219 eventos). Aproximadamente 47% de todos os registros (2.205 ocorrências) são solucionados em até 2 horas. Reforçando o que foi visto na revisão bibliográfica, os melhores resultados para prever alagamentos em áreas urbanas são limiares de intensidade-duração e durações de 10 a 60 minutos são o melhor intervalo de tempo para limiares derivados para inundações pluviais e inundações repentinas. Com esse valor da duração do bolsão é um trunfo para ter limiares mais específicos de cada pluviômetro.
Contudo, observa-se uma cauda longa na distribuição, com 622 eventos (cerca de 13% do total) persistindo por mais de 6 horas. A existência de eventos de longa duração (mais de 6 horas), sugere que a capacidade de escoamento é comprometida por fatores adicionais além da intensidade da chuva. Isso reforça uma das hipóteses deste trabalho: a de que a saturação do solo por chuvas antecedentes e, em áreas costeiras, o efeito de represamento da maré alta, são os principais moduladores da duração dos bolsões e alagamentos. Um sistema já saturado ou com sua saída bloqueada pela maré não consegue drenar eficientemente, transformando um evento de chuva pontual em um alagamento persistente.

Figura 4. Distribuição de duração de eventos 
4.2 Distribuição Temporal das Ocorrências

A análise sazonal na Figura 5 (esquerda) destaca as variações sazonais das ocorrências de inundação, evidenciando uma clara concentração de ocorrências nos meses mais quentes. O verão se destaca como a estação com a maior frequência, somando aproximadamente 2.500 eventos, o que corresponde a 47,9% do total de registros no período analisado. O outono segue como a segunda estação com maior incidência, respondendo por 31,5% dos casos. Em contraste, o inverno apresenta o menor número de alagamentos, um padrão consistente com o período de estiagem na cidade. A existência de registros durante a estação seca, embora em menor número, indica que os alagamentos não são eventos exclusivos dos períodos de chuva mais intensa.

Figura 5. Gráficos Sazonais da distribuição de Alagamentos

A distribuição mensal das ocorrências, apresentada na Figura 6, evidencia um padrão sazonal bem definido, conforme visto anteriormente na Figura 5. O pico de eventos concentra-se nos meses de verão, com fevereiro registrando o maior número de ocorrências (aproximadamente 980), seguido por março (cerca de 780) e janeiro (cerca de 670). Dezembro também se destaca como um mês de alta frequência (cerca de 700). A partir de abril, observa-se uma redução acentuada no número de eventos, que atinge os valores mais baixos durante o inverno, com julho apresentando a menor incidência. A frequência volta a aumentar progressivamente a partir de setembro, indicando a transição para o período mais chuvoso.
Este padrão sazonal está em forte concordância com o regime pluviométrico da cidade do Rio de Janeiro. O verão é caracterizado pela maior atividade de sistemas convectivos, frequentemente associados ao aquecimento da superfície e à influência de sistemas meteorológicos de grande escala, como a Zona de Convergência do Atlântico Sul (ZCAS). As chuvas de verão são tipicamente de alta intensidade e curta duração, o que sobrecarrega rapidamente a capacidade dos sistemas de drenagem urbana e explica a maior frequência de alagamentos. Em contrapartida, o inverno é a estação mais seca, o que justifica a baixa incidência de eventos registrada.

Figura 6. Gráfico da distribuição Mensal de Alagamentos

A distribuição horária dos eventos (Figura 7) revela um padrão diurno bem definido. O número de ocorrências começa a aumentar a partir das 15h, atingindo um pico entre 18h e 20h. Este período concentra a maior parte dos alagamentos registrados, indicando uma associação com eventos de chuva que se desenvolvem ou se intensificam no final da tarde e início da noite. 
O pico de ocorrências no verão e no final da tarde, conforme observado nos resultados, está em concordância com o regime pluviométrico da cidade, descrito por Dereczynski et al. (2009). Este padrão é característico da atuação de sistemas meteorológicos como a Zona de Convergência do Atlântico Sul (ZCAS) e, principalmente, de tempestades convectivas de verão. Tais tempestades, formadas pelo aquecimento da superfície e pela circulação de brisa marítima, produzem chuvas de alta intensidade e curta duração, sobrecarregando rapidamente a capacidade de escoamento do sistema de drenagem.

Figura 7. Gráfico da distribuição horária dos eventos de alagamentos



4.3 Distribuição Espacial das Ocorrências

A distribuição espacial dos pontos de alagamento (Figura 8) mostra que os eventos não ocorrem de forma aleatória, mas se concentram em corredores urbanos específicos. Observa-se uma alta densidade de ocorrências ao longo de eixos viários importantes da Zona Norte, no Centro da cidade, e em áreas densamente povoadas da Zona Oeste, como Campo Grande e Bangu.


Figura 8. Mapa de pontos de acúmulos dágua 

A agregação dos dados por bairro (Figura 9) quantifica essa concentração e identifica os principais bairros afetados por alagamento. Bairros como Tijuca, Lagoa, Centro, Botafogo e São Cristóvão destacam-se com mais de 100 eventos registrados no período. Em contraste, bairros da orla da Zona Norte e da Zone Oeste, embora também afetados, apresentam uma frequência menor. A concentração dos alagamentos em bairros da Zona Sul e em áreas centrais não pode ser atribuída unicamente à precipitação. Essas regiões historicamente combinam uma topografia de baixada, alta densidade de ocupação, elevado índice de impermeabilização do solo e uma infraestrutura de drenagem mais antiga e, por vezes, subdimensionada. Essa combinação de fatores de vulnerabilidade torna a área suscetível a alagamentos mesmo durante eventos de chuva de intensidade moderada, o que explica por que são as áreas mais recorrentes.


Figura 9. Mapa de Bairros com Ocorrências de Alagamento

4.4 Análise API por Sub-bacia Hidrográfica

A extensão da análise para o nível de sub-bacia hidrográfica, com incorporação do Índice de Precipitação Antecedente (API), representa o refinamento central desta pesquisa em relação à abordagem I-D clássica por estação pluviométrica. A abordagem permite que o limiar que separa condições de alagamento e não alagamento se mova dinamicamente em função do estado de saturação prévia do sistema: para uma API baixa (sistema seco), uma intensidade de chuva maior é necessária para cruzar o limiar; para uma API elevada (sistema úmido), uma intensidade moderada já pode ser suficiente para deflagrar um alerta.

4.4.1 Cobertura Espacial e Pesos de Agregação

A partir da interseção entre os Polígonos de Thiessen e os polígonos das 55 sub-bacias identificadas no município, foram calculados os pesos de influência de cada estação pluviométrica, resultando em 149 pares estação–sub-bacia. Exemplificando, a Micro Bacia do Galeão (ID 9) é atendida por duas estações: a Estação 18 contribui com 80,5% do peso e a Estação 21 com 19,5%, refletindo as áreas de cobertura relativas dos respectivos Polígonos de Thiessen sobre a sub-bacia. Sub-bacias localizadas em áreas insulares ou de orla com histórico insuficiente de eventos de alagamento — como a Ilha de Paquetá (ID 2) e sub-bacias das praias da Baía — não apresentaram dados suficientes para o ajuste dos parâmetros.

Ao todo, 21.799 pares dia–sub-bacia foram processados com precipitação diária total superior a 10 mm ao longo do período de análise (2015–2024), dos quais uma parcela foi classificada como EA (dia com pelo menos um registro de alagamento na sub-bacia) e o restante como ESA. O balanço EA/ESA varia consideravelmente entre as sub-bacias, refletindo as diferentes densidades de cobertura da rede de monitoramento e as características de uso do solo de cada região.

4.4.2 Desempenho dos Limiares API

Para as 38 sub-bacias com dados suficientes, foram ajustados parâmetros para 10 escalas temporais. Com K fixo em 0,85, os valores de POD variaram de 0,14 a 1,0, a FAR entre 0,004 e 0,52, e o PPV entre 0,015 e 0,83. O número ótimo de dias antecedentes variou de 1 a 10 dias, com a maioria das sub-bacias apresentando melhor desempenho com janelas de 1 a 5 dias, indicando que o estado de umidade de curto prazo é o principal modulador da suscetibilidade a alagamentos, em consonância com Ramos Filho et al. (2021).

A inclusão de K como parâmetro de busca — com o API recalculado corretamente a partir da série diária composta completa, incluindo dias com precipitação inferior a 10 mm — revelou que nenhum valor único é adequado para todas as sub-bacias. K = 0,60 foi o ótimo para 13 das 38 sub-bacias (34%), refletindo drenagem rápida e memória hidrológica curta, característica de bacias urbanas altamente impermeabilizadas. Valores elevados de K (0,90–0,95) foram ótimos para 9 sub-bacias (24%), incluindo Botafogo, Galeão e Sub-bacia Secundária do Rio da Prata do Mendanha, onde corpos d'água internos ou maior capacidade de retenção prolongam a influência das chuvas anteriores. K = 0,85 — adotado de forma uniforme por Ramos Filho et al. (2021) — mostrou-se ótimo para apenas 7 sub-bacias (18%), evidenciando que sua adoção universal introduz viés sistemático no ajuste dos limiares.

10 sub-bacias apresentaram ganho de score superior a 0,005 em relação ao K fixo em 0,85. As melhorias mais expressivas ocorreram no Canal do Mangue (+0,083), Sub-bacia do Arroio Fundo/Rio Grande (+0,070) e Lagoa Rodrigo de Freitas (+0,026). A Micro Bacia do Centro manteve a liderança em score absoluto (0,334; K = 0,80; duração de 6h; 10 dias antecedentes), seguida pelo Canal do Mangue (0,248; K = 0,60) e pela Sub-bacia dos Rios Acari/Pavuna/Meriti (0,236; K = 0,85). A Tabela 3 apresenta os resultados das sub-bacias com melhor desempenho.

Os limiares ajustados com K otimizado e as zonas de alerta correspondentes estão representados nas Figuras 10 e 11. A Figura 10 exibe, para cada sub-bacia, as quatro zonas de alerta delimitadas pela curva exponencial intermediária I = a·e^(b·API) + c, com os pontos classificados como EA (círculos vermelhos) e ESA (quadrados cinzas) sobrepostos ao gráfico de dispersão intensidade × API. A Figura 11 apresenta os limiares de Intensidade-Duração (I-D) por sub-bacia, comparando os limiares brutos e os limiares com tolerância estatística, evidenciando a variabilidade das condições críticas entre as diferentes regiões da cidade.


Tabela 3. Sub-bacias com melhor desempenho após otimização de K (ordenadas por score)

| Sub-bacia | Duração | Dias API | K ótimo | POD | FAR | PPV | Score |
|---|---|---|---|---|---|---|---|
| Micro bacia do Centro | 6h | 10 | 0,80 | 0,657 | 0,170 | 0,613 | 0,334 |
| Sub bacia do Canal do Mangue | 24h | 2 | 0,60 | 0,583 | 0,174 | 0,515 | 0,248 |
| Sub bacia dos Rios Acari/Pavuna/Meriti | 1h | 5 | 0,85 | 0,528 | 0,174 | 0,541 | 0,236 |
| Restinga da Barra | 24h | 1 | 0,70 | 0,522 | 0,199 | 0,514 | 0,215 |
| Sub bacia da Lagoa Rodrigo de Freitas | 24h | 1 | 0,60 | 0,573 | 0,201 | 0,425 | 0,195 |
| Sub bacia do Arroio Fundo/Rio Grande | 8h | 4 | 0,75 | 0,518 | 0,123 | 0,419 | 0,190 |
| Sub bacia do Canal do Cunha | 10h | 10 | 0,85 | 0,506 | 0,195 | 0,464 | 0,189 |
| Micro bacia de Copacabana | 3h | 3 | 0,85 | 0,574 | 0,118 | 0,330 | 0,167 |
| Sub bacia de Botafogo | 12h | 10 | 0,95 | 0,559 | 0,154 | 0,349 | 0,165 |
| Micro bacia da Urca | 30min | 1 | 0,80 | 0,375 | 0,013 | 0,375 | 0,139 |
| Sub bacia do Rio Carioca | 30min | 1 | 0,60 | 0,294 | 0,025 | 0,476 | 0,137 |


4.4.3 Análise Sazonal dos Limiares

A separação sazonal dos limiares foi realizada para as 51 sub-bacias com dados disponíveis, gerando 2.040 combinações sub-bacia × estação × duração, das quais 1.000 (49%) apresentaram eventos suficientes para o ajuste. A distribuição de eventos EA pelos dados ilustra a forte assimetria sazonal: o verão concentra 802 eventos EA (47%), o outono 521 (31%), a primavera 279 (16%) e o inverno apenas 104 (6%), padrão consistente com o regime pluviométrico do município descrito na seção 2.3.

O desempenho médio dos limiares por estação, apresentado na Tabela 4 e visualizado na Figura 12, evidencia que o inverno produz os maiores ganhos em especificidade. A FAR média caiu de 0,757 (valor anual de referência) para 0,658 no inverno (−10 pontos percentuais), e 43% dos casos apresentaram FAR inferior a 0,60, em contraste com apenas 11% no ajuste anual. Esse resultado confirma a hipótese de que limiares únicos anuais superestimam os alarmes na estação seca, pois qualquer chuva intensa em solo pouco saturado pode ultrapassar o limiar sem necessariamente causar alagamento. O Score médio do inverno (0,034) superou todas as demais estações, a despeito do menor POD (0,812), indicando que a maior precisão (PPV e menor FAR) compensa a redução de sensibilidade.

Tabela 4. Desempenho médio dos limiares inferiores por estação (média sobre sub-bacias e durações)

| Estação | n ajustados | POD | FAR | PPV | Score | FAR < 0,60 |
|---------|------------|-----|-----|-----|-------|-----------|
| Verão (DJF) | 350 | 0,880 | 0,748 | 0,137 | 0,030 | 17% |
| Outono (MAM) | 300 | 0,863 | 0,763 | 0,146 | 0,030 | 20% |
| Inverno (JJA) | 130 | 0,812 | 0,658 | 0,122 | 0,034 | 43% |
| Primavera (SON) | 220 | 0,822 | 0,745 | 0,099 | 0,021 | 18% |
| **Anual (ref.)** | **390** | **0,895** | **0,757** | — | — | **11%** |

Os limiares sazonais refletem as condições físicas esperadas. Os limiares de verão são superiores aos anuais em 77% dos pares sub-bacia × duração: em termos práticos, é preciso mais chuva para disparar um alerta no verão porque o sistema já opera próximo da sua capacidade, e eventos de alta intensidade são mais frequentes e nem sempre resultam em alagamento. Já o limiar de inverno ficou abaixo do anual em apenas 45% dos casos — o algoritmo se ajusta ao intervalo real de intensidades da estação, que já são menores, estabelecendo limiares absolutos compatíveis com a menor pluviosidade típica do período.

A distribuição do K ótimo por estação, apresentada na Figura 12c, revela um padrão hidrológico relevante. No inverno, 75% dos casos apresentam K = 0,60 e a janela antecedente modal é de 1 dia (média de 1,7 dias), indicando que a precipitação do dia imediatamente anterior é praticamente o único preditor relevante — o sistema drena tão rapidamente que a memória de dias mais distantes é negligenciável. No verão e outono, a distribuição de K é mais heterogênea (K ≥ 0,85 em 30–37% dos casos) e a janela antecedente média alcança 3,9 e 4,3 dias, respectivamente, sugerindo que a saturação acumulada ao longo de vários dias tem influência sobre o limiar crítico nessas estações.

As maiores reduções de FAR no inverno em relação ao valor anual ocorreram no Canal do Cunha (−0,458; de 0,857 para 0,399), na Micro Bacia do Centro (−0,430; de 0,789 para 0,359) e na Sub-bacia dos Rios Acari/Pavuna/Meriti (−0,360; de 0,911 para 0,550). Estas sub-bacias têm em comum altos volumes de eventos ESA no verão que inflam a FAR anual, mas no inverno apresentam poucas ocorrências sem alagamento acima do limiar, o que melhora substancialmente a precisão dos alertas.

A principal limitação da abordagem sazonal é a cobertura reduzida no inverno: 38 das 51 sub-bacias não possuem o mínimo de 3 eventos EA nessa estação, inviabilizando o ajuste. Para essas sub-bacias, recomenda-se adotar o limiar anual como alternativa operacional. As Figuras 13 e 14 apresentam, respectivamente, os limiares I-D sazonais e as zonas de alerta por sub-bacia, com painéis individuais para cada estação, evidenciando a variação dos parâmetros ajustados e a ausência de limiares nas estações com dados insuficientes.


5.2 Limitações da Pesquisa

É importante reconhecer as limitações inerentes ao estudo. Primeiramente, os dados de ocorrência do COR-Rio, embora valiosos, dependem de registros humanos, o que pode introduzir subjetividade na classificação dos eventos e possíveis inconsistências nos horários de início e fim. Em segundo lugar, a rede de pluviômetros do Alerta Rio, apesar de densa, apresenta menor cobertura em partes da Zona Oeste, o que pode impactar a precisão da associação chuva-alagamento nesta região.

5.3 Passos Futuros

Os resultados obtidos nas análises de caracterização espaço-temporal, limiares API por sub-bacia com K otimizado e separação sazonal estabelecem uma base técnica sólida para os próximos desenvolvimentos. Os próximos passos concentram-se em quatro frentes complementares.

A primeira frente é a validação independente dos limiares ajustados — tanto anuais quanto sazonais. Os parâmetros foram estimados sobre o conjunto completo de dados disponíveis (2015–2024); uma validação cruzada temporal — utilizando, por exemplo, os anos mais recentes (2022–2024) como conjunto de teste e o período anterior como treino — permitirá avaliar a estabilidade dos limiares e sua capacidade de generalização para eventos não observados no período de calibração. A validação sazonal apresenta desafio adicional, pois o número reduzido de eventos EA no inverno pode tornar os parâmetros ajustados mais sensíveis ao conjunto de treinamento.

A segunda frente é a análise de sensibilidade e interpretação física dos parâmetros sazonais. A distribuição bimodal do K ótimo (concentração em 0,60 e 0,90–0,95) e a variação da janela antecedente entre estações (média de 1,7 dias no inverno versus 3,9 dias no verão) devem ser relacionadas às características morfológicas, de uso do solo, de cobertura vegetal e de infraestrutura de drenagem de cada sub-bacia. Essa análise permitirá identificar quais atributos físicos explicam por que certas regiões retêm memória hidrológica prolongada ao longo do ano, enquanto outras apresentam resposta quase instantânea independentemente da estação.

A terceira frente é a ampliação da cobertura no inverno. Das 51 sub-bacias analisadas, 38 não possuem eventos EA suficientes para ajuste do limiar de inverno. Estratégias para contornar essa limitação incluem o agrupamento de sub-bacias morfologicamente semelhantes para o ajuste regional, a extensão do período de dados ou a incorporação de registros de outras fontes operacionais.

A quarta frente é a integração operacional. Os limiares sazonais ajustados serão avaliados quanto à viabilidade de incorporação ao sistema de alertas do COR-Rio, considerando a necessidade de seleção automática da estação vigente, a disponibilidade de dados de precipitação em tempo real para o cálculo da API e os requisitos de antecedência mínima para a emissão de alertas preventivos.


















5.4 Cronograma


Etapas
Set
Out
Nov
Dez
Jan
Fev
Mar
1. Associação de Dados (Chuva x Alagamento)














2. Construção dos Gráficos I-D (por pluviômetro)














3. Ajuste das Curvas de Limiar (I-D)














4.Submissão do artigo com análises preliminares














5. Validação e Avaliação de Desempenho














6. Redação dos Capítulos














7. Redação Final e Formatação














8. Preparação para a Defesa (Apresentação e Revisão Final)














9. Submissão artigo com resultado final
































REFERÊNCIAS

AGONAFIR, C. et al. A review of recent advances in urban flood research. Water Security, v. 19, p. 100141, 2023.

ALFIERI, L.; THIELEN, J. A European precipitation index for extreme rain-storm and flash flood early warning. Meteorological Applications, v. 22, n. 1, p. 3-13, 2015.

BORGES, P. A.; FRANKE, J.; da ANUNCIAÇÃO, Y. M. T. et al. Comparação de métodos de interpolação espacial para a estimativa da distribuição da precipitação no Distrito Federal, Brasil. Theoretical and Applied Climatology, v. 123, p. 335–348, 2016.

CAINE, N. The Rainfall Intensity: Duration Control of Shallow Landslides and Debris Flows. Geografiska Annaler: Series A, Physical Geography, v. 62, n. 1/2, p. 23-27, 1980.

COELHO NETTO, A. L. A interface florestal-urbana e os desastres naturais relacionados à água no Maciço da Tijuca: desafios ao planejamento urbano numa perspectiva sócio-ambiental. Revista do Departamento de Geografia, v. 16, p. 46-60, 2005.

DERECZYNSKI, C. P.; SILVA, J. O.; MACHADO, C. O. Climatologia da precipitação no município do Rio de Janeiro. Revista Brasileira de Meteorologia, v. 24, n. 1, p. 24-38, 2009.

DESOUZA, S. et al. Understanding Spatiotemporal Patterns and Drivers of Urban Flooding Using Municipal Reports. Hydrological Processes, 2024. (Nota: Este artigo foi citado como referência, mas os detalhes completos de publicação como volume e página podem ser de um pré-print ou de uma versão aceita, a serem confirmados na publicação final).

GEORGANTA, C. et al. Critical Rainfall Thresholds as a Tool for Urban Flood Identification in Attica Region, Greece. Atmosphere, v. 13, n. 5, p. 698, 2022.

HENAO SALGADO, M. J.; ZAMBRANO NÁJERA, J. Assessing Flood Early Warning Systems for Flash Floods. Frontiers in Climate, v. 4, p. 787042, 2022.

ISAAKS, E. H.; SRIVASTAVA, R. M. An Introduction to Applied Geostatistics. New York: Oxford University Press, 1989.

KAMPF, S. K. et al. Rainfall Thresholds for Flow Generation in Desert Ephemeral Streams. Water Resources Research, v. 54, n. 12, p. 9935-9950, 2018.

MONTESARCHIO, V. et al. Comparison of methodologies for flood rainfall thresholds estimation. Natural Hazards, v. 75, n. 1, p. 909-934, 2015.

PAPAGIANNAKI, K. et al. Flash flood occurrence and relation to the rainfall hazard in a highly urbanized area. Natural Hazards and Earth System Sciences, v. 15, n. 8, p. 1859-1871, 2015.

PEREIRA, R. M. S.; WANDERLEY, H. S.; DELGADO, R. C. Homogeneous regions for rainfall distribution in the city of Rio de Janeiro associated with the risk of natural disasters. Natural Hazards, v. 111, p. 333-351, 2022.

PUTRI QATRINNADA, W. F. et al. A literature review: rainfall thresholds as flash flood monitoring for an early warning system. Water Practice & Technology, v. 19, n. 11, p. 4486, 2024.

QIAN, K. et al. Urban pluvial flooding prediction by machine learning approaches – a case study of Shenzhen city, China. Advances in Water Resources, v. 145, p. 103719, 2020.

RAMOS FILHO, G. M. et al. An improved rainfall-threshold approach for robust prediction and warning of flood and flash flood hazards. Natural Hazards, v. 105, p. 2409–2429, 2021.

RAMOS FILHO, G. M. Performance of rainfall threshold for flood identification from ground- and satellite-based (sub)daily data. 2021. 99 f. Tese (Doutorado em Engenharia Civil e Ambiental) – Centro de Tecnologia, Universidade Federal da Paraíba, João Pessoa, 2021.

ROSSI, M. et al. Statistical approaches for the definition of landslide rainfall thresholds and their uncertainty using rain gauge and satellite data. Geomorphology, v. 285, p. 16-27, 2017.

SHEPARD, D. A two-dimensional interpolation function for irregularly-spaced data. In: ACM '68: PROCEEDINGS OF THE 1968 23RD ACM NATIONAL CONFERENCE, New York, 1968. Anais... New York: Association for Computing Machinery, 1968. p. 517-524.

SIMOYAMA, F. O. Location models to optimize flood monitoring networks. 2023. Dissertação (Mestrado) – Instituto Nacional de Pesquisas Espaciais, São José dos Campos, 2023.

THIESSEN, A. H. Precipitation averages for large areas. Monthly Weather Review, v. 39, n. 7, p. 1082-1084, 1911.
TIAN, X. et al. Critical rainfall thresholds for urban pluvial flooding inferred from citizen observations. Science of The Total Environment, v. 689, p. 258-268, 2019.


