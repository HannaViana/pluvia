## 3 MATERIAIS E MÉTODOS

Esta seção descreve a área de estudo, as fontes de dados utilizadas, os procedimentos de pré-processamento e tratamento dos dados, as metodologias empregadas para a estimativa da precipitação média espacial e para a identificação e caracterização de eventos de precipitação, bem como as ferramentas computacionais que apoiaram as análises.

### 3.1 Área de Estudo: Município do Rio de Janeiro

O presente estudo concentra-se no município do Rio de Janeiro, capital do estado homônimo, localizado na região Sudeste do Brasil. A cidade possui uma geografia complexa, caracterizada por uma extensa faixa litorânea, maciços costeiros, planícies e bacias hidrográficas internas, que influenciam significativamente os padrões de precipitação e a suscetibilidade a inundações (Figura [Inserir Número da Figura do Mapa do Rio de Janeiro, e.g., a partir de `City Boundary of Rio de Janeiro`]). Com uma elevada densidade populacional e intensa urbanização, o Rio de Janeiro enfrenta desafios recorrentes relacionados a eventos hidrometeorológicos extremos, justificando a necessidade de estudos aprofundados sobre seus regimes de chuva e os impactos associados.

### 3.2 Bases de Dados Utilizadas

Para a realização deste trabalho, foram utilizadas distintas bases de dados, abrangendo informações pluviométricas, registros de ocorrências de inundação e dados geoespaciais de referência.

#### 3.2.1 Dados Pluviométricos: Sistema Alerta Rio

Os dados de precipitação foram obtidos do Sistema Alerta Rio, mantido pela Fundação Instituto de Geotécnica do Município do Rio de Janeiro (Geo-Rio). Esta base de dados consiste em registros de acumulado de chuva em diferentes intervalos temporais (15 minutos, 1 hora, 4 horas, 24 horas e 96 horas), coletados por uma rede de estações pluviométricas telemétricas distribuídas pelo município. Para este estudo, foram utilizados os dados de acumulado de chuva a cada 15 minutos. A série histórica original dos dados brutos compreende um período extenso, sendo que, para as análises de eventos e correlações com ocorrências, considerou-se o período coincidente com os registros de inundação disponíveis, iniciando-se em janeiro de 2015. As informações cadastrais das estações, como identificador, nome, coordenadas geográficas (latitude e longitude) e cota, também foram disponibilizadas pelo Alerta Rio e utilizadas para georreferenciar os dados e para a aplicação de métodos de espacialização da chuva.

#### 3.2.2 Registros de Ocorrências de Inundação: COR-Rio

Os registros de ocorrências relacionadas a alagamentos e inundações foram fornecidos pelo Centro de Operações Rio (COR-Rio), órgão responsável pelo monitoramento e gerenciamento de eventos na cidade. Esses registros incluem informações como tipo de ocorrência, localização (bairro, coordenadas geográficas), data e hora de início e fim do evento, descrição e, em alguns casos, classificação de gravidade e prazo para solução. Foram selecionados os tipos de ocorrência diretamente relacionados a inundações pluviais, especificamente "Bolsão d'água em via", "Alagamentos e enchentes" e "Lâmina d'água". O período dos dados de ocorrências analisado estende-se de [Inserir Data de Início das Ocorrências, e.g., 2015] a [Inserir Data de Fim das Ocorrências, e.g., 2024], conforme a disponibilidade.

#### 3.2.3 Dados Geoespaciais de Referência

Para contextualização espacial e análises geográficas, foram utilizados dados vetoriais do limite municipal do Rio de Janeiro e dos limites dos bairros. Estes dados, originalmente disponibilizados pelo Instituto Pereira Passos (IPP) – Armazém de Dados, foram processados para gerar um polígono unificado do contorno da cidade e para permitir a agregação espacial de informações.

### 3.3 Pré-processamento e Tratamento dos Dados

As bases de dados brutas foram submetidas a um rigoroso processo de pré-processamento e tratamento para garantir a qualidade e a consistência necessárias para as análises subsequentes.

#### 3.3.1 Validação e Limpeza dos Dados Pluviométricos

Os dados pluviométricos brutos passaram por diversas etapas de tratamento. Inicialmente, colunas irrelevantes foram removidas e a chave primária de cada registro, que continha a identificação da estação e o timestamp, foi utilizada para extrair estas duas informações cruciais. As colunas de data e hora foram convertidas para formatos temporais adequados, e os campos de acumulado de chuva foram convertidos para formato numérico.
Valores ausentes nos acumulados de chuva foram preenchidos com 0.0, partindo-se do pressuposto que a ausência de registro em um intervalo específico indica ausência de precipitação mensurável. A coluna `horario`, quando ausente, foi preenchida com um delta de tempo nulo. Foi realizada uma verificação de consistência entre a data e hora extraídas da chave primária e as colunas de data e horário originais, e quaisquer registros inconsistentes foram descartados. Registros duplicados, baseados na chave primária, também foram removidos. Por fim, os dados foram enriquecidos com as informações de nome, latitude e longitude de cada estação, obtidas da base cadastral, e ordenados cronologicamente por `timestamp`.

#### 3.3.2 Filtragem e Enriquecimento dos Registros de Ocorrências

Os registros de ocorrências também foram pré-processados. As colunas de data e hora de início e fim foram convertidas para o formato datetime. O tipo de evento foi mapeado a partir de um cadastro de identificadores de Pontos de Operação Prioritários (POPs). Foram filtradas apenas as ocorrências relevantes para o estudo de inundações, conforme mencionado na seção 3.2.2. Foram calculadas novas variáveis, como a duração de cada ocorrência (em minutos e segundos) e atributos temporais derivados da data de início, como hora do dia, dia da semana, mês e estação do ano (Verão: Dez-Fev; Outono: Mar-Mai; Inverno: Jun-Ago; Primavera: Set-Nov). Ocorrências com informações essenciais faltantes, como coordenadas geográficas ou data de início, foram removidas.

#### 3.3.3 Transformação de Coordenadas e Preparação dos Dados Geoespaciais

Os dados geoespaciais, incluindo as localizações das estações pluviométricas, os pontos de ocorrências de inundação, e os polígonos dos limites dos bairros e do município, foram inicialmente definidos ou convertidos para o sistema de coordenadas geográficas WGS84 (EPSG:4326). Posteriormente, para a realização de cálculos de área e operações geométricas que exigem um sistema de coordenadas planas, todos os dados geoespaciais foram transformados para o sistema de coordenadas projetadas SIRGAS 2000 / UTM zona 23S (EPSG:31983), adequado para a região do Rio de Janeiro. O limite municipal, que poderia ser composto por múltiplos polígonos (ilhas), foi unificado em uma única geometria representativa da área continental e insular do município através de uma operação de união geométrica.

### 3.4 Estimativa da Precipitação Média Espacial pelo Método dos Polígonos de Thiessen

Para transformar os dados pontuais de precipitação das estações em uma estimativa representativa da chuva média sobre a área do município, foi empregado o método dos Polígonos de Thiessen.

#### 3.4.1 Fundamentação Teórica e Geração dos Polígonos Estáticos

O método dos Polígonos de Thiessen, também conhecido como método de Voronoi, assume que a precipitação em qualquer ponto dentro de um polígono é igual à precipitação medida na estação pluviométrica contida nesse polígono (Thiessen, 1911). Cada polígono é formado por mediatrizes traçadas entre estações adjacentes, delimitando uma área de influência para cada posto pluviométrico.
Neste estudo, os polígonos de Thiessen foram gerados de forma estática, ou seja, utilizando o conjunto de estações pluviométricas ativas e com dados disponíveis durante o período de análise. As coordenadas (projetadas) das estações serviram como base para a geração dos diagramas de Voronoi. Os polígonos resultantes foram então interceptados (recortados) pelo limite do município do Rio de Janeiro, garantindo que apenas as áreas de influência dentro do território municipal fossem consideradas.

#### 3.4.2 Cálculo da Precipitação Areal Média em Intervalos de 15 minutos

Após a geração e o recorte dos polígonos, a área de cada um dentro dos limites municipais foi calculada. O peso de cada polígono ($W_i$) foi determinado como a razão entre a sua área ($A_i$) e a área total do município coberta pelos polígonos ($\sum A_i$).
A precipitação areal média ($P_{areal}$) para cada intervalo de 15 minutos foi então calculada como a média ponderada da precipitação registrada em cada estação ($P_i$) pelo peso de seu respectivo polígono de influência, conforme a Equação 1:

$P_{areal}(t) = \sum_{i=1}^{N} P_i(t) \times W_i$
(Equação 1)

Onde:
-   $P_{areal}(t)$ é a precipitação areal média no instante $t$;
-   $P_i(t)$ é a precipitação registrada na estação $i$ no instante $t$;
-   $W_i$ é o peso do polígono de Thiessen associado à estação $i$;
-   $N$ é o número total de estações pluviométricas consideradas.

Este procedimento resultou em uma série temporal única de precipitação areal média a cada 15 minutos para o município do Rio de Janeiro.

### 3.5 Definição e Caracterização de Eventos de Precipitação

A partir da série temporal de precipitação areal média, foram aplicadas diferentes metodologias para identificar e caracterizar eventos de precipitação significativos.

#### 3.5.1 Regularização da Série Temporal de Precipitação Areal

A série temporal de precipitação areal média, calculada na etapa anterior, foi regularizada para garantir um intervalo de tempo constante de 15 minutos entre os registros. Este passo é crucial para métodos de identificação de eventos que dependem da análise de intervalos consecutivos. Para tanto, a série foi reamostrada para a frequência de 15 minutos, e quaisquer intervalos de tempo que originalmente não possuíam dados (ou que resultaram de falhas no sistema de coleta) foram preenchidos com valor de precipitação zero.

#### 3.5.2 Eventos Baseados na Agregação Diária

Uma abordagem para identificar dias com precipitação significativa consistiu na agregação da série regularizada de precipitação areal de 15 minutos para totais diários. Um "dia chuvoso" foi definido como qualquer dia em que o total de precipitação areal acumulada excedeu um limiar mínimo de 0.01 mm. Esta metodologia permite uma visão climatológica da ocorrência de dias com chuva e a quantificação do volume diário.

#### 3.5.3 Eventos Baseados em Períodos Contínuos de Chuva

Para uma caracterização mais detalhada da estrutura temporal das chuvas, foi implementado um método para identificar "eventos de chuva contínua". Um evento foi definido como um período ininterrupto de precipitação, onde cada intervalo de 15 minutos dentro do evento apresenta precipitação superior a um limiar mínimo (`RAIN_THRESHOLD_FOR_EVENT = 0.01 mm`). A metodologia permitiu a consideração de pequenas interrupções secas (`MIN_DRY_SPELL_DURATION`, definida em 1 hora), de modo que dois blocos de chuva separados por um período seco inferior a este limite fossem agrupados como um único evento. Para cada evento contínuo identificado, foram calculadas as seguintes propriedades: data e hora de início, data e hora de fim, duração total, volume total de precipitação acumulada, e a intensidade máxima de precipitação registrada em um intervalo de 15 minutos durante o evento.

#### 3.5.4 Eventos Baseados na Metodologia Peak Over Threshold (POT)

A metodologia Peak Over Threshold (POT) foi empregada para identificar períodos de precipitação de alta intensidade, que frequentemente estão associados a impactos hidrológicos agudos. Esta abordagem foca em identificar blocos de tempo onde a intensidade da precipitação excede um limiar predefinido (`POT_INTENSITY_THRESHOLD`).
O limiar de intensidade foi estabelecido como o percentil 95 das intensidades de precipitação em 15 minutos, considerando apenas os intervalos em que houve registro de chuva (precipitação > 0.01 mm).
Um evento POT foi caracterizado pela ocorrência de um número mínimo de intervalos consecutivos (`MIN_EXCEEDANCE_INTERVALS = 2`, equivalente a 30 minutos) em que a intensidade da chuva superou o limiar estabelecido. Períodos de excedência próximos no tempo, separados por um intervalo inferior a um limite máximo (`MAX_TIME_BETWEEN_EXCEEDANCES`, definido em 3 horas), foram agrupados para formar um único evento POT. Para cada evento POT, foram determinadas as seguintes características: data e hora de início e fim da fase de excedência, a duração total desta fase, o número de intervalos de 15 minutos que excederam o limiar, o volume total de precipitação durante a fase de excedência, a intensidade máxima de precipitação em 15 minutos registrada durante o evento, e a magnitude total da precipitação acima do limiar (soma das diferenças entre a precipitação e o limiar para todos os intervalos excedentes).

### 3.6 Ferramentas Computacionais

Todas as etapas de processamento, análise de dados e geração de visualizações foram conduzidas utilizando a linguagem de programação Python (versão 3.10 ou superior), em ambiente de desenvolvimento Jupyter Notebook. As principais bibliotecas científicas empregadas incluem: Pandas, para manipulação e análise de dados tabulares e séries temporais; GeoPandas, para manipulação de dados geoespaciais; NumPy, para operações numéricas; SciPy, especificamente `scipy.spatial` para a geração dos diagramas de Voronoi (base para os polígonos de Thiessen); Matplotlib, Seaborn e Plotly, para a criação de gráficos estáticos e interativos; e Cartopy, para a elaboração de mapas geoespaciais detalhados.