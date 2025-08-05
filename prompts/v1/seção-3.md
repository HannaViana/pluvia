## 3 MATERIAIS E MÉTODOS

Esta seção detalha os materiais e métodos empregados para a análise de eventos de chuva e suas consequentes inundações urbanas no município do Rio de Janeiro. Descreve-se a área de estudo, as bases de dados utilizadas, as ferramentas computacionais, os procedimentos de tratamento e pré-processamento dos dados, a metodologia para estimativa da precipitação média espacial e as diferentes abordagens para identificação e caracterização de eventos de chuva, bem como as técnicas de análise espacial aplicadas aos registros de inundação.

### 3.1 Área de Estudo: Município do Rio de Janeiro

O município do Rio de Janeiro, capital do estado homônimo, localiza-se na Região Sudeste do Brasil, entre as latitudes 22°45'S e 23°05'S e longitudes 43°05'O e 43°48'O. Caracteriza-se por uma topografia complexa, com maciços costeiros, planícies e extensas áreas urbanizadas, e um clima tropical atlântico (Aw segundo a classificação de Köppen-Geiger), com verões quentes e úmidos e invernos amenos e relativamente secos. A precipitação média anual varia consideravelmente ao longo do município, influenciada pelo relevo e pela proximidade com o oceano, sendo comum a ocorrência de eventos chuvosos intensos, especialmente durante o verão, que frequentemente resultam em inundações urbanas. A área de estudo compreende todo o limite municipal do Rio de Janeiro, conforme visualizado na Figura X (referenciar a imagem `output_7_1.png` ou similar que mostre o limite da cidade). A delimitação precisa do município foi obtida a partir da união dos polígonos de seus bairros, conforme detalhado na subseção 3.6.

### 3.2 Bases de Dados

Para a realização deste estudo, foram utilizadas duas bases de dados principais: dados pluviométricos provenientes do Sistema Alerta Rio e registros de ocorrências de inundações urbanas do Centro de Operações Rio (COR-Rio).

#### 3.2.1 Dados Pluviométricos (Sistema Alerta Rio)

Os dados de precipitação foram obtidos junto ao Sistema Alerta Rio, mantido pela Fundação Instituto de Geotécnica do Município do Rio de Janeiro (Geo-Rio). Esta base de dados consiste em registros de precipitação acumulada em diferentes intervalos temporais (15 minutos, 1 hora, 4 horas, 24 horas e 96 horas), coletados por uma rede de estações pluviométricas telemétricas distribuídas pelo município. Para este estudo, foram utilizados os dados de `acumulado_chuva_15_min` como base para as análises de maior resolução temporal. O período de dados brutos abrangido inicialmente pode ser extenso, mas foi posteriormente filtrado para alinhar-se com o período dos registros de ocorrências e a disponibilidade de dados consistentes das estações, resultando em um período de análise efetivo que será detalhado na seção de pré-processamento (subseção 3.4). O conjunto de dados original incluía informações como identificador da estação, data, horário e os diversos acumulados de chuva. [O usuário pode inserir aqui uma referência à estrutura dos dados brutos, como um exemplo do `df.head()` do notebook `Data Cleaning for AlertaRio Table` antes da limpeza].

#### 3.2.2 Registros de Ocorrência de Inundações Urbanas (COR-Rio)

Os registros de ocorrências de inundações urbanas foram fornecidos pelo Centro de Operações Rio (COR-Rio), órgão responsável pelo monitoramento e gerenciamento de eventos na cidade. Estes registros contêm informações detalhadas sobre cada ocorrência, tais como: tipo de evento (e.g., "Bolsão d'água em via", "Alagamentos e enchentes", "Lâmina d'água"), localização geográfica precisa (latitude e longitude), bairro, data e hora de início e fim do evento, descrição textual, e, em alguns casos, classificação de gravidade e status. O período de dados considerado para as ocorrências foi de [Inserir o período dos dados de ocorrências utilizados]. Foram selecionados para análise os tipos de ocorrência diretamente relacionados a inundações pluviais, conforme detalhado na subseção 3.5.

### 3.3 Ferramentas Computacionais Utilizadas

Todas as etapas de processamento, análise e visualização de dados foram conduzidas utilizando a linguagem de programação Python (versão 3.10 ou similar). As principais bibliotecas empregadas incluem: Pandas, para manipulação e análise de dados tabulares; GeoPandas, para manipulação de dados geoespaciais; NumPy, para operações numéricas eficientes; SciPy, especificamente para a geração de diagramas de Voronoi (para os polígonos de Thiessen) e estimativa de densidade por kernel (KDE); Shapely, para operações geométricas; e Matplotlib, Seaborn e Plotly, para a criação de gráficos e mapas estáticos e interativos.

### 3.4 Tratamento e Pré-processamento de Dados Pluviométricos

Os dados brutos de precipitação do Sistema Alerta Rio passaram por um rigoroso processo de tratamento e pré-processamento para garantir sua qualidade e adequação para as análises subsequentes. As etapas realizadas, conforme detalhado no notebook `Data Cleaning for AlertaRio Table`, incluíram:

1.  **Remoção de Colunas Desnecessárias**: Colunas como `Unnamed: 0`, que são artefatos da leitura de arquivos CSV, foram removidas.
2.  **Extração e Conversão de Data/Hora**: A coluna `primary_key`, que continha o identificador da estação e a data/hora completa do registro, foi desmembrada para extrair `id_estacao_extracted` e `datetime_extracted`. A `datetime_extracted` foi convertida para o formato datetime do Pandas.
3.  **Conversão de Tipos de Dados**: As colunas `data_particao` e `horario` foram convertidas para os tipos `datetime` e `timedelta`, respectivamente. Colunas numéricas, como os acumulados de chuva e identificadores de estação, foram convertidas para tipos numéricos apropriados.
4.  **Tratamento de Valores Ausentes**: Foi verificada a incidência de valores ausentes. Por exemplo, a análise inicial mostrou os seguintes percentuais de dados faltantes para as colunas de acumulado de chuva: `acumulado_chuva_15_min` (0.38%), `acumulado_chuva_1_h` (0.39%), `acumulado_chuva_4_h` (0.43%), `acumulado_chuva_24_h` (0.49%), e `acumulado_chuva_96_h` (0.62%) [Referenciar a Tabela "Percentual missing in each row" do notebook]. Valores ausentes nas colunas de acumulado de chuva foram preenchidos com 0.0, assumindo que a ausência de registro indicava ausência de chuva mensurável. A coluna `horario` teve seus valores ausentes preenchidos com `pd.to_timedelta(0.0)`.
5.  **Validação de Consistência**: Foi realizada uma verificação para assegurar que os identificadores de estação e as informações de data/hora extraídas da `primary_key` eram consistentes com as colunas `id_estacao`, `data_particao` e `horario`. [Mencionar o resultado, e.g., "Não foram encontradas inconsistências significativas" ou, se houve, como foram tratadas, como a remoção das linhas inconsistentes, se aplicável].
6.  **Remoção de Duplicatas**: Registros duplicados baseados na `primary_key` foram identificados (e.g., 33 duplicatas encontradas) e removidos, mantendo-se apenas a primeira ocorrência.
7.  **Ordenação Temporal**: Os dados foram ordenados cronologicamente pela coluna `timestamp` (anteriormente `datetime_extracted`).
8.  **Filtragem de Estações e Período**: Após a limpeza inicial, os dados pluviométricos foram filtrados para incluir apenas estações com informações de localização válidas e para o período temporal relevante ao estudo das ocorrências de inundação (e.g., a partir de 2015, conforme definido no notebook `Rainfall Analysis in Rio de Janeiro...`).

Ao final deste processo, obteve-se um conjunto de dados pluviométricos limpo e organizado, pronto para as etapas subsequentes de análise. [O usuário pode inserir aqui uma referência à estrutura dos dados limpos, como um exemplo do `df.head()` final do notebook `Data Cleaning for AlertaRio Table`].

### 3.5 Tratamento e Pré-processamento de Dados de Inundações Urbanas

Os dados de ocorrências de inundações urbanas do COR-Rio também foram submetidos a um processo de tratamento e enriquecimento, conforme implementado nos notebooks de análise exploratória, espacial e temporal:

1.  **Conversão de Tipos de Dados Temporais**: As colunas `data_inicio` e `data_fim`, que indicam o início e o término de cada ocorrência, foram convertidas para o formato datetime do Pandas.
2.  **Cálculo da Duração do Evento**: Uma nova coluna, `duration_minutes`, foi calculada a partir da diferença entre `data_fim` e `data_inicio`, fornecendo a duração de cada evento de inundação em minutos.
3.  **Engenharia de Features Temporais**: Para facilitar análises temporais, foram derivadas novas colunas a partir de `data_inicio`, incluindo: hora de início (`hour_start`), dia da semana (`day_of_week`), mês (`month` e `month_num`), ano (`year`), dia do mês (`day_of_month`), data (`date`), e estação do ano (`season` - Verão, Outono, Inverno, Primavera, com base em definições meteorológicas para o Hemisfério Sul).
4.  **Mapeamento do Tipo de Ocorrência**: A coluna `id_pop` foi utilizada para mapear o título ou descrição do tipo de ocorrência (e.g., "Bolsão d'água em via") a partir de uma tabela de referência (`pops.csv`), criando a coluna `tipo`.
5.  **Filtragem de Ocorrências Relevantes**: O conjunto de dados foi filtrado para incluir apenas os tipos de ocorrências de interesse para o estudo de inundações pluviais: "Bolsão d'água em via", "Alagamentos e enchentes", e "Lâmina d'água".
6.  **Tratamento de Valores Ausentes**: Valores ausentes em colunas como `prazo_num` foram tratados (e.g., preenchidos com 0 para fins de visualização, conforme demonstrado no notebook). Registros sem informações essenciais de latitude, longitude ou `data_inicio` foram removidos.

Este pré-processamento resultou em um conjunto de dados de inundações urbanas estruturado e enriquecido, facilitando as análises descritivas e geoespaciais. [O usuário pode inserir aqui uma referência à estrutura dos dados de ocorrências após o pré-processamento, como um `display(ocorrencias.head())` do notebook `Preliminary Exploratory Analysis of Flood Events` após as transformações].

### 3.6 Processamento de Dados Geoespaciais para Delimitação da Área de Estudo

A delimitação precisa da área de estudo, o município do Rio de Janeiro, foi realizada a partir de dados vetoriais dos limites dos bairros. O arquivo `bairro.csv`, contendo informações de cada bairro, incluindo uma coluna `geometry_wkt` com as geometrias dos polígonos em formato Well-Known Text (WKT) [Referenciar a Tabela "Original Neighborhood DataFrame (first 5 rows)" do notebook `Creating Rio de Janeiro City Boundary`], foi o ponto de partida.

As geometrias WKT foram convertidas em objetos geométricos da biblioteca Shapely e, subsequentemente, foi criado um GeoDataFrame utilizando a biblioteca GeoPandas, atribuindo-se o sistema de referência de coordenadas (CRS) geográfico WGS84 (EPSG:4326). A Figura Y [Referenciar a imagem `output_5_5.png` - Mapa dos Bairros] ilustra a distribuição espacial dos bairros.

Para obter o limite municipal unificado, foi aplicada uma operação de dissolução (`dissolve`) a todos os polígonos dos bairros. Esta operação agrega todas as geometrias em um único multipolígono que representa a fronteira externa do município do Rio de Janeiro, conforme mostrado na Figura Z [Referenciar a imagem `output_7_1.png` - Limite da Cidade].

Finalmente, todas as camadas de dados geoespaciais utilizadas neste estudo (limite municipal, localizações das estações pluviométricas e registros de ocorrências de inundação) foram transformadas para o sistema de coordenadas projetadas SIRGAS 2000 / UTM zone 23S (EPSG:31983). Esta projeção é adequada para a região do Rio de Janeiro e permite cálculos precisos de área e distância, essenciais para a metodologia dos polígonos de Thiessen e outras análises espaciais.

### 3.7 Estimativa da Precipitação Média Espacial pelo Método dos Polígonos de Thiessen

Para estimar a precipitação média sobre a área do município do Rio de Janeiro (precipitação areal), foi empregado o método dos Polígonos de Thiessen, também conhecido como método de Voronoi. Este método atribui a cada ponto em uma área a precipitação observada na estação pluviométrica mais próxima, criando polígonos de influência ao redor de cada estação.

O processo metodológico consistiu nas seguintes etapas:

1.  **Geração dos Polígonos de Voronoi**: Utilizando as coordenadas geográficas das estações pluviométricas ativas e em operação durante o período de estudo [Referenciar a Figura "City Boundary and Active Station Locations (Geographic CRS)", que é a `output_11_3.png` do notebook de Thiessen, mostrando as estações sobre o limite da cidade], foram gerados os polígonos de Voronoi. Cada polígono delimita a área ao redor de uma estação que lhe é mais próxima do que a qualquer outra estação.
2.  **Recorte dos Polígonos**: Os polígonos de Voronoi gerados, que inicialmente podem se estender para além dos limites municipais, foram recortados (clipados) utilizando o polígono do limite municipal do Rio de Janeiro (obtido na subseção 3.6).
3.  **Cálculo das Áreas e Pesos**: Para cada polígono de Thiessen resultante ($i$) dentro dos limites municipais, sua área ($A_i$) foi calculada (em m², dado o uso de um CRS projetado). O peso ($w_i$) de cada polígono foi então determinado como a razão entre sua área e a área total do município coberta pelo conjunto de todos os polígonos de Thiessen, conforme a Equação \ref{eq:thiessen_weight}:
    ```latex
    w_i = \frac{A_i}{\sum_{j=1}^{N} A_j}
    ```
    \label{eq:thiessen_weight}
    onde $N$ é o número total de estações (e, consequentemente, polígonos) consideradas. A Figura W [Referenciar a imagem `output_25_0.png` - Static Thiessen Polygons for Rainfall Stations in Rio de Janeiro] apresenta a configuração final dos polígonos de Thiessen, suas respectivas estações e os limites da cidade.
4.  **Cálculo da Precipitação Média Espacial**: A precipitação média espacial ($P_{areal}$) para cada intervalo de tempo de 15 minutos ($t$) foi calculada como a média ponderada da precipitação registrada em cada estação ($P_i(t)$) pelo peso de seu respectivo polígono ($w_i$), de acordo com a Equação \ref{eq:areal_rainfall}:
    ```latex
    P_{areal}(t) = \sum_{i=1}^{N} P_i(t) \cdot w_i
    ```
    \label{eq:areal_rainfall}
    Esta abordagem assume que a precipitação em qualquer ponto dentro de um polígono de Thiessen é igual à precipitação observada na estação correspondente.

### 3.8 Metodologias para Identificação e Caracterização de Eventos de Chuva

A partir da série temporal de precipitação média espacial de 15 minutos, foram aplicadas três metodologias distintas para identificar e caracterizar eventos de chuva significativos. Primeiramente, a série temporal foi regularizada para garantir intervalos consistentes de 15 minutos, preenchendo-se quaisquer falhas temporais com valores de precipitação nulos, assegurando a continuidade necessária para as análises subsequentes.

#### 3.8.1 Agregação Diária da Precipitação

A abordagem mais fundamental consistiu na agregação da precipitação média espacial de 15 minutos para obter totais diários. Um "dia chuvoso" foi definido como qualquer dia em que o total de precipitação acumulada entre 00:00 e 23:45 (hora local) excedesse um limiar mínimo (e.g., 0.01 mm), para distinguir de dias completamente secos ou com traços de chuva insignificantes. Esta metodologia permite a identificação dos dias com os maiores volumes totais de precipitação.

#### 3.8.2 Identificação de Períodos Contínuos de Chuva

Para uma caracterização mais detalhada da dinâmica dos eventos chuvosos, foi implementado um algoritmo para identificar "períodos contínuos de chuva". Este método, encapsulado na função `identify_rain_events` (conforme notebook `Rainfall Analysis in Rio de Janeiro...`), define um evento de chuva como uma sequência de intervalos de 15 minutos nos quais a precipitação excede um limiar mínimo (`RAIN_THRESHOLD_FOR_EVENT`, estabelecido em 0.01 mm/15min). Dois eventos de chuva consecutivos são considerados distintos se separados por um período seco (precipitação abaixo do limiar) com duração superior a um valor pré-definido (`MIN_DRY_SPELL_DURATION`, configurado para 1 hora neste estudo). Para cada evento contínuo identificado, foram calculadas as seguintes métricas:
*   **Horário de início e fim** do evento.
*   **Duração total** do evento.
*   **Volume total de precipitação** acumulado durante o evento.
*   **Intensidade de pico em 15 minutos**, correspondendo ao maior valor de precipitação em um intervalo de 15 minutos durante o evento.
*   **Intensidade média horária** do evento (volume total dividido pela duração em horas).

#### 3.8.3 Análise de Picos Acima de um Limiar (Peak Over Threshold - POT)

A análise de Picos Acima de um Limiar (POT) foi utilizada para focar especificamente nos períodos de precipitação mais intensa, que são frequentemente associados a impactos hidrológicos agudos como inundações rápidas. O limiar de intensidade (`POT_INTENSITY_THRESHOLD`) para esta análise foi definido estatisticamente como o percentil 95 das intensidades de precipitação registradas em todos os intervalos de 15 minutos considerados chuvosos (i.e., com precipitação > 0.01 mm), resultando em um valor de [e.g., 1.28 mm/15min, conforme `POT_INTENSITY_THRESHOLD` definido no notebook].

O algoritmo para identificação de eventos POT, implementado na função `identify_pot_events`, considerou os seguintes critérios:
1.  Um evento POT é iniciado quando a intensidade da precipitação em 15 minutos excede o `POT_INTENSITY_THRESHOLD` por um número mínimo de intervalos consecutivos (`MIN_EXCEEDANCE_INTERVALS`, definido como 2 intervalos, ou 30 minutos).
2.  Blocos de excedência separados por um período de tempo inferior a um máximo especificado (`MAX_TIME_BETWEEN_EXCEEDANCES`, definido como 3 horas) são agrupados para formar um único evento POT.

Para cada evento POT identificado, foram caracterizadas as seguintes propriedades:
*   **Horário de início e fim** da fase de excedência.
*   **Duração da fase de excedência**.
*   **Número de intervalos de 15 minutos** em que o limiar foi excedido.
*   **Volume total de precipitação** acumulado durante a fase de excedência.
*   **Intensidade de pico em 15 minutos** observada durante a fase de excedência.
*   **Magnitude acumulada acima do limiar**, calculada como a soma das diferenças entre a precipitação observada e o limiar para todos os intervalos em que este foi superado.

### 3.9 Análise Espacial da Distribuição de Eventos de Inundação

Para compreender a distribuição espacial das inundações urbanas, foram aplicadas diversas técnicas de análise e visualização geoespacial aos registros de ocorrências:

1.  **Mapas de Dispersão (Scatter Maps)**: Geração de mapas plotando a localização geográfica (latitude e longitude) de cada ocorrência de inundação, permitindo uma visualização direta da sua distribuição sobre a área de estudo. Diferentes tipos de inundação foram codificados por cores ou marcadores distintos.
2.  **Estimativa de Densidade por Kernel (KDE)**: Aplicação da técnica de KDE para identificar áreas de alta concentração (hotspots) de ocorrências de inundação. Esta técnica suaviza a distribuição de pontos, gerando uma superfície contínua de densidade.
3.  **Mapas Coropléticos**: Criação de mapas temáticos onde os bairros do Rio de Janeiro são coloridos de acordo com a frequência (contagem) de eventos de inundação registrados em cada um, permitindo identificar as regiões administrativas mais afetadas.
4.  **Mapas de Bolhas (Bubble Maps)**: Visualização das ocorrências de inundação onde o tamanho de cada ponto (bolha) no mapa é proporcional a uma métrica do evento, como sua duração, permitindo analisar espacialmente a severidade ou persistência das inundações.

Estas análises espaciais visam identificar padrões geográficos na ocorrência de inundações, como a concentração em determinadas áreas ou a relação com características urbanas e topográficas (embora a análise desta última relação não seja o foco principal deste método, os mapas fornecem a base para tal).