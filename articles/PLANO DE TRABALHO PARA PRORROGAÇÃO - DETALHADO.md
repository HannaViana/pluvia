# PLANO DE TRABALHO PARA PRORROGAÇÃO DE PRAZO (MESTRADO)

**Discente:** Hanna Soares Viana

**Orientador:** Prof. Dr. Fabricio Polifke da Silva

**Título:** A Ocorrência de Alagamentos na Cidade do Rio de Janeiro: Uma Análise Baseada em Dados do COR-Rio e do Alerta Rio

---

## 1. Objetivos da Dissertação

O objetivo central desta pesquisa é investigar a relação empírica entre eventos de precipitação e a ocorrência de alagamentos no município do Rio de Janeiro, a partir da integração dos dados pluviométricos do Sistema Alerta Rio (33 estações, dados de 15 em 15 minutos) com os 4.868 registros georreferenciados de ocorrências do Centro de Operações Rio (COR-Rio), no período de 2015 a 2024.

Busca-se estabelecer limiares de chuva baseados em curvas de Intensidade-Duração (I-D) que possam subsidiar sistemas de alerta precoce e a gestão de riscos hidrológicos urbanos. Após as recomendações da banca de qualificação (22/08/2025), o escopo foi ampliado para incluir:

- **Substituição dos Polígonos de Thiessen por sub-bacias hidrográficas** como unidade de análise espacial, conferindo maior precisão hidrológica na associação chuva–alagamento.
- **Incorporação de variáveis ambientais adicionais**, como a distância das ocorrências à rede hidrográfica e a influência da maré na persistência dos eventos.
- **Desenvolvimento de um modelo de alerta operacional** baseado nos novos limiares e na precipitação antecedente, com validação quantitativa de desempenho.

---

## 2. Resumo do Plano de Trabalho

O plano de trabalho consiste na integração, reprocessamento e análise avançada das bases de dados do Alerta Rio e do COR-Rio para o período de 2015–2024, agora sob a nova ótica das sub-bacias hidrográficas. As tarefas principais são organizadas nos seguintes eixos:

### 2.1 Revisão Bibliográfica Complementar

- Investigar na literatura a fundamentação técnica para o uso de zonas pluviométricas e sub-bacias hidrográficas em substituição aos Polígonos de Thiessen, especialmente em áreas urbanas complexas com topografia heterogênea.
- Aprofundar a revisão sobre o efeito da maré na persistência de alagamentos costeiros, com foco em estudos de cidades tropicais litorâneas.
- Revisar metodologias de limiares I-D que incorporam precipitação antecedente (API), com base em Ramos Filho et al. (2021) e abordagens multivariadas como DeSouza et al. (2024).

### 2.2 Reestruturação da Análise Espacial (Sub-bacias Hidrográficas)

- Obter e processar os dados de sub-bacias hidrográficas do município do Rio de Janeiro.
- Substituir a associação espacial por Polígonos de Thiessen pela associação por sub-bacias, reatribuindo cada ocorrência de alagamento e cada estação pluviométrica à sua respectiva sub-bacia.
- Recalcular as áreas de influência e as associações espaço-temporais entre eventos de chuva e registros de alagamento sob a nova compartimentação.

### 2.3 Análise de Vulnerabilidade e Variáveis Complementares

- **Distância à rede hidrográfica:** Gerar gráficos e análises estatísticas da distância entre cada ocorrência de alagamento e o corpo hídrico mais próximo, segmentando por tipo de evento (Bolsão d'água, Lâmina d'água e Alagamento).
- **Co-ocorrência espacial:** Investigar se há ocorrências de bolsão e alagamento no mesmo local, identificando padrões de escalamento de severidade.
- **Influência da maré:** Analisar a relação entre o nível de maré (dados da DHN/Marinha) e a duração/persistência dos eventos de alagamento, testando a hipótese de que a maré alta atua como fator de represamento.

### 2.4 Análise Multivariada por Sub-bacias

- Construir tabelas cruzadas de quantidade de ocorrências por sub-bacia e por zona pluviométrica.
- Avaliar a distribuição diferenciada de tipos de evento (Bolsão, Lâmina, Alagamento) entre as diferentes unidades hidrológicas.
- Explorar correlações entre características das sub-bacias (área, grau de impermeabilização, altitude média) e a frequência/severidade dos alagamentos.

### 2.5 Modelagem de Limiares I-D por Unidade Hidrológica

- Reconstruir os gráficos de dispersão I-D (escala log-log) para cada sub-bacia, classificando os eventos como EA (com alagamento) e ESA (sem alagamento).
- Ajustar curvas de limiar I = a × D^(-b) para cada unidade, utilizando regressão logística e otimização dos parâmetros α e β.
- Definir múltiplas curvas (limiar inferior, intermediário e superior) para criação de zonas de risco graduais, conforme a abordagem de Georganta et al. (2022).
- Incorporar a precipitação antecedente (API) como variável moduladora do limiar intermediário, conforme a metodologia de Ramos Filho et al. (2021).

### 2.6 Refinamento de Intensidade Pluviométrica

- Desenvolver gráficos de intensidade pluviométrica específicos para o horário de início de cada bolsão d'água, permitindo comparar a intensidade no momento exato da ocorrência com a intensidade máxima do evento.
- Analisar se a intensidade no horário do bolsão é um preditor mais adequado do que a intensidade máxima do evento de chuva.

### 2.7 Modelo de Alerta e Validação

- Criar um protocolo de alerta baseado nos novos limiares I-D por sub-bacia e na precipitação antecedente.
- Validar o modelo utilizando métricas quantitativas: Probabilidade de Detecção (POD), Falso Alarme (FAR), Valor Preditivo Positivo (PPV), F1-score e Coeficiente de Correlação de Matthews (MCC).
- Comparar o desempenho do novo modelo (sub-bacias + API) com os limiares anteriores (Polígonos de Thiessen), quantificando a melhoria obtida.

---

## 3. Cronograma do Plano de Trabalho: Progresso e Dificuldades

### 3.1 Atividades Concluídas

As seguintes etapas foram integralmente realizadas durante o período regulamentar:

| Atividade | Período | Status |
|---|---|---|
| Coleta e organização dos dados do COR-Rio (87.620 registros brutos → 4.868 ocorrências de alagamento filtradas) | 2024 | Concluída |
| Coleta e organização dos dados pluviométricos do Alerta Rio (33 estações, dados de 15 min, 2015–2024) | 2024 | Concluída |
| Limpeza e pré-processamento dos dados (remoção de duplicatas, validação de coordenadas, cálculo de durações) | 2024 | Concluída |
| Caracterização espaço-temporal geral: análise descritiva completa das ocorrências (distribuição por tipo, sazonalidade, padrões horários, distribuição espacial por bairro) | 2024–2025 | Concluída |
| Tipificação das ocorrências em três níveis de severidade: Bolsão d'água (86,6%), Lâmina d'água (3,8%) e Alagamento (9,6%) | 2024–2025 | Concluída |
| Geração dos Polígonos de Thiessen e associação espaço-temporal preliminar | 2025 | Concluída |
| Segmentação de eventos de chuva independentes (intervalo seco mínimo de 6h) e cálculo de pares I-D (intensidade máxima 1h e duração) | 2025 | Concluída |
| Construção de gráficos I-D por estação pluviométrica com classificação EA/ESA (33 estações) | 2025 | Concluída |
| Ajuste preliminar de curvas de limiar I-D por estação via regressão logística | 2025 | Concluída |
| Geração de 14+ gráficos para publicação científica (charts v1), incluindo padrões temporais, distribuição horária, duração por tipo e por estação, categorias de duração | 2025 | Concluída |
| Exame de Qualificação | 22/08/2025 | Aprovada |
| Submissão de artigo científico à revista *Urban Climate* (UCLIM-D-26-00774): "Urban Flooding in a Tropical Coastal Environment: Spatiotemporal Patterns for Early Warning and Resilience" | Jan/2026 | Concluída |

### 3.2 Principais Resultados Obtidos

- **Padrões temporais bem definidos:** Verão concentra 47,9% dos eventos (2.330 ocorrências); pico horário entre 17h–20h, coincidindo com chuvas convectivas.
- **Distribuição de duração:** Mediana de 1,95h para eventos de baixa/média severidade e 2,99h para alta severidade (percentil 90 de 8,36h).
- **Concentração espacial:** Eventos concentrados em corredores urbanos específicos (Tijuca, Centro, Botafogo, São Cristóvão), indicando vulnerabilidade associada à topografia e infraestrutura.
- **Limiares I-D preliminares:** 33 curvas de limiar ajustadas por estação, com recall alto (~1,0) mas precisão baixa, indicando que fatores além da chuva influenciam a ocorrência — reforçando a necessidade da nova abordagem por sub-bacias e incorporação de variáveis adicionais.

### 3.3 Dificuldades e Justificativa da Prorrogação

A prorrogação é necessária devido à **re-elaboração dos métodos de análise** após as recomendações da banca examinadora de qualificação. Especificamente:

1. **Mudança da unidade de análise espacial:** A banca recomendou a substituição dos Polígonos de Thiessen por sub-bacias hidrográficas. Esta mudança, embora conceitualmente superior para a representação dos processos hidrológicos urbanos, exige o descarte e reprocessamento completo de todos os cálculos de associação espacial e correlação chuva-alagamento já realizados. Trata-se de um retrabalho substancial que inclui: obtenção e processamento dos dados de sub-bacias, reatribuição de todas as 4.868 ocorrências e de todos os eventos de chuva às novas unidades, e recálculo completo das curvas I-D.

2. **Ampliação do escopo analítico:** A inclusão de novas variáveis (distância à rede hidrográfica, influência da maré, análise de co-ocorrência) demanda coleta de dados adicionais, desenvolvimento de novos scripts de análise e geração de visualizações inéditas.

3. **Necessidade de revisão bibliográfica adicional:** A mudança metodológica requer um novo ciclo de aprofundamento teórico em hidrologia urbana, especificamente sobre a superioridade técnica das zonas pluviométricas e sub-bacias frente aos métodos tradicionais de interpolação.

4. **Artigo científico em revisão:** O artigo submetido à *Urban Climate* poderá requerer revisões baseadas nos pareceres dos revisores, demandando tempo adicional para ajustes.

---

## 4. Cronograma do que será feito até a data da defesa

O período de prorrogação de 6 meses (janeiro a junho de 2026) será utilizado para consolidar a nova metodologia, finalizar o modelo de alerta e concluir a redação da dissertação. Todas as atividades do plano original que ainda não foram realizadas estão contempladas, com as devidas adaptações metodológicas.

| Atividade | Mês 1 (Jan) | Mês 2 (Fev) | Mês 3 (Mar) | Mês 4 (Abr) | Mês 5 (Mai) | Mês 6 (Jun) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **4.1 Revisão bibliográfica complementar** (sub-bacias vs. Thiessen; efeito da maré; API) | X | X | | | | |
| **4.2 Obtenção e processamento dos dados de sub-bacias hidrográficas** do município do RJ | X | | | | | |
| **4.3 Reatribuição espacial de ocorrências e estações às sub-bacias** (substituição completa dos Polígonos de Thiessen) | | X | X | | | |
| **4.4 Análise de vulnerabilidade:** gráficos de distância à rede hidrográfica por tipo de evento (Bolsão, Lâmina, Alagamento) | | X | X | | | |
| **4.5 Análise de co-ocorrência:** investigar bolsão e alagamento no mesmo local; escalamento de severidade | | X | | | | |
| **4.6 Análise da influência da maré:** correlação maré × duração/persistência dos eventos | | | X | X | | |
| **4.7 Análise multivariada:** tabelas cruzadas sub-bacia × zona pluviométrica; distribuição de tipos por unidade hidrológica | | | X | | | |
| **4.8 Reconstrução dos gráficos I-D por sub-bacia** com classificação EA/ESA | | | X | X | | |
| **4.9 Ajuste de curvas de limiar I-D por sub-bacia** (regressão logística; múltiplas curvas de risco) | | | | X | | |
| **4.10 Incorporação da precipitação antecedente (API)** como moduladora dos limiares | | | | X | X | |
| **4.11 Gráficos de intensidade no horário do bolsão** (intensidade específica vs. intensidade máxima do evento) | | | X | X | | |
| **4.12 Criação do modelo/protocolo de alerta** baseado em limiares I-D por sub-bacia + API | | | | X | X | |
| **4.13 Validação quantitativa do modelo** (POD, FAR, PPV, F1, MCC); comparação com limiares anteriores | | | | | X | |
| **4.14 Redação dos capítulos de Resultados e Discussão** | | | | X | X | |
| **4.15 Redação do capítulo de Conclusão** e integração final do manuscrito | | | | | X | |
| **4.16 Revisão final da dissertação** (formatação, figuras, referências, consistência) | | | | | X | X |
| **4.17 Revisão do artigo *Urban Climate*** (se pareceres recebidos) | | | | X | X | |
| **4.18 Preparação para a defesa** (apresentação, ensaio, revisão final) | | | | | | X |
| **DEFESA DA DISSERTAÇÃO** | | | | | | **Jun/2026** |

---

**Data prevista para a defesa:** Junho de 2026.

---

### Justificativa para o Formulário

**Opção a marcar:** "( ) Devido à re-elaboração dos métodos de análise, excedeu-se ao prazo inicialmente previsto."

**Texto da justificativa:** A prorrogação é necessária e suficiente para concluir a pesquisa com a qualidade científica exigida, atendendo integralmente às recomendações da banca examinadora de qualificação. A mudança da unidade de análise espacial de Polígonos de Thiessen para sub-bacias hidrográficas, somada à incorporação de novas variáveis ambientais (distância à hidrografia, influência da maré e precipitação antecedente), exigiu a revisão completa da metodologia e o reprocessamento de toda a base de dados. Os avanços já obtidos — incluindo a caracterização espaço-temporal completa, a análise I-D preliminar por estação, e a submissão de um artigo científico à revista *Urban Climate* — demonstram a solidez do trabalho e a viabilidade de sua conclusão no prazo solicitado. O produto final — um modelo de alerta baseado em limiares I-D calibrados por sub-bacia hidrográfica — terá aplicabilidade prática direta para a gestão de riscos de alagamento na cidade do Rio de Janeiro.
