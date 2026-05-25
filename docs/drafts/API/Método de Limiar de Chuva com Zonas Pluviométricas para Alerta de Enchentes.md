# **Método de Limiar de Chuva com Zonas 	Pluviométricas para Alerta de Enchentes**

## **Visão Geral**

Este documento explica, de forma simples e prática, como replicar o método apresentado na tese utilizando zonas pluviométricas baseadas apenas em pluviômetros.

A ideia central do método é identificar:

* qual intensidade de chuva costuma gerar enchente;  
* em quais condições isso acontece;  
* e transformar isso em um sistema de alerta probabilístico.

---

# **1\. Conceito Central**

O método parte da seguinte observação:

* às vezes chove muito e não alaga;  
* às vezes chove menos e ocorre enchente.

Portanto:

não existe um único limiar fixo universal.

A solução proposta é criar:

1. um limiar inferior;  
2. um limiar superior;  
3. uma zona intermediária probabilística;  
4. incorporar a condição antecedente do solo usando API.

---

# **2\. Estrutura Geral do Método**

1\. Coletar eventos de chuva  
2\. Separar eventos com e sem enchente  
3\. Calcular intensidade máxima  
4\. Construir limiares  
5\. Aplicar tolerâncias probabilísticas  
6\. Adicionar API  
7\. Avaliar desempenho

---

# **3\. Dados Necessários**

## **3.1 Dados de Chuva**

Idealmente:

* pluviômetros automáticos;  
* resolução sub-horária;  
* séries de 10 min, 30 min ou 1 h.

Exemplos:

| Duração | Intensidade |
| ----- | ----- |
| 10 min | 32 mm/h |
| 1 h | 18 mm/h |
| 3 h | 9 mm/h |

---

## **3.2 Registro de Enchentes**

Você precisa saber:

| Data | Houve enchente? |
| ----- | ----- |
| 12/01/2020 | Sim |
| 18/01/2020 | Não |

---

# **4\. Construção dos Limiares**

## **4.1 Limiar Inferior**

Abaixo dele:

enchente praticamente nunca ocorre

---

## **4.2 Limiar Superior**

Acima dele:

enchente praticamente sempre ocorre

---

## **4.3 Zona Intermediária**

Entre os dois limiares:

* às vezes ocorre enchente;  
* às vezes não.

Essa é a região probabilística.

---

# **5\. Tolerâncias Probabilísticas**

## **5.1 Limiar Inferior**

Aplicar tolerância de 5%.

Ou seja:

aceitar perder poucos eventos reais

para reduzir falsos alarmes.

---

## **5.2 Limiar Superior**

Usar percentil 99%.

Assim:

acima do limiar a chance de enchente é muito alta

---

# **6\. API — Antecedent Precipitation Index**

## **6.1 Ideia Física**

O solo influencia fortemente o risco.

### **Solo seco**

Absorve água.

Necessita chuva maior para gerar enchente.

---

### **Solo saturado**

Pouca chuva já gera escoamento.

---

## **6.2 Fórmula Geral do API**

APIt=Pt+kPt−1+k2Pt−2+...API\_t \= P\_t \+ kP\_{t-1} \+ k^2P\_{t-2} \+ ...

Onde:

* (P\_t) \= chuva;  
* (k) \= fator de decaimento.

Dias recentes possuem maior peso.

---

## **6.3 Relação API × Intensidade**

O método utiliza uma curva exponencial:

I=aeb(API)+cI \= ae^{b(API)} \+ c

Onde:

* (I) \= intensidade crítica;  
* (API) \= chuva antecedente;  
* (a,b,c) \= parâmetros calibrados.

Quanto maior o API:

menor intensidade necessária para causar enchente

---

# **7\. Avaliação do Modelo**

## **7.1 Matriz de Confusão**

| Resultado | Significado |
| ----- | ----- |
| TP | acertou enchente |
| FP | falso alarme |
| FN | perdeu enchente |
| TN | acertou ausência |

---

## **7.2 Métricas**

### **POD**

POD=TP/(TP+FN)POD \= TP / (TP \+ FN)

Quanto maior, melhor.

---

### **FAR**

FAR=FP/(FP+TN)FAR \= FP / (FP \+ TN)

Quanto menor, melhor.

---

### **HK**

HK=POD−FARHK \= POD \- FAR

Mede qualidade geral.

---

# **8\. Uso de Zonas Pluviométricas**

## **8.1 Por Que Usar Zonas?**

A mesma chuva pode produzir respostas diferentes em áreas distintas.

Exemplo:

* área urbana impermeável;  
* área rural permeável;  
* serra;  
* litoral.

Portanto:

um único limiar para toda a região geralmente funciona mal

---

# **9\. O Que É uma Zona Pluviométrica?**

É uma região onde a chuva possui comportamento semelhante.

Exemplos:

* mesma intensidade;  
* mesma sazonalidade;  
* mesma frequência de extremos;  
* mesmo padrão temporal.

Cada zona terá:

* limiar inferior próprio;  
* limiar superior próprio;  
* curva API própria.

---

# **10\. É Possível Fazer Isso Apenas com Pluviômetros?**

Sim.

Você consegue criar zonas pluviométricas usando somente dados de pluviômetros.

Nesse caso:

você modela o regime espacial da chuva

Mesmo sem:

* radar meteorológico;  
* dados hidrológicos detalhados;  
* sensores de nível.

---

# **11\. Como Construir Zonas Usando Apenas Pluviômetros**

## **11.1 Organizar Estações**

Exemplo:

| Estação | Região |
| ----- | ----- |
| P1 | Serra |
| P2 | Centro |
| P3 | Litoral |
| P4 | Interior |

---

## **11.2 Extrair Variáveis Climáticas**

Para cada estação calcular:

| Variável | Objetivo |
| ----- | ----- |
| média anual | regime climático |
| percentil 95 | extremos |
| intensidade máxima | severidade |
| frequência de eventos | recorrência |
| duração média | persistência |
| sazonalidade | comportamento anual |
| API médio | memória úmida |

---

# **12\. Métodos para Criar as Zonas**

## **12.1 Método Manual**

Separação baseada em conhecimento local.

Exemplo:

| Zona | Característica |
| ----- | ----- |
| Z1 | Serra |
| Z2 | Área urbana |
| Z3 | Baixada |
| Z4 | Litoral |

---

## **12.2 Correlação Entre Séries**

Calcular:

corr(Pi,Pj)corr(P\_i,P\_j)

Se duas estações possuem comportamento parecido:

elas pertencem à mesma zona

---

## **12.3 Clusterização Estatística**

Método mais recomendado.

Criar vetores:

\[média anual, P95, máximos, sazonalidade...\]

Aplicar:

* K-Means;  
* Hierarchical Clustering;  
* Gaussian Mixture.

---

# **13\. Aplicação do Método por Zona**

Para cada zona:

1\. separar eventos  
2\. calcular intensidade  
3\. calcular duração  
4\. calcular API  
5\. ajustar limiares  
6\. avaliar métricas

---

# **14\. Estrutura Operacional**

Quando uma nova chuva ocorre:

## **Etapa 1**

Identificar a zona.

---

## **Etapa 2**

Calcular:

* intensidade;  
* duração;  
* API.

---

## **Etapa 3**

Aplicar os limiares daquela zona.

---

# **15\. Estratégia Simples Muito Utilizada**

## **Nearest Gauge**

Método operacional simples:

1\. localizar o pluviômetro mais próximo  
2\. usar os limiares daquela estação/zona

---

# **16\. Estrutura Computacional Recomendada**

## **Organização dos Modelos**

zonas \= {  
    "Z1": modelo\_z1,  
    "Z2": modelo\_z2,  
    "Z3": modelo\_z3  
}

Cada modelo contém:

* limiar inferior;  
* limiar superior;  
* parâmetros API;  
* métricas.

---

# **17\. Evolução para Modelo Probabilístico**

Em vez de limiares rígidos:

gerar probabilidade de enchente

Exemplo:

| Zona | Probabilidade |
| ----- | ----- |
| Z1 | 15% |
| Z2 | 82% |
| Z3 | 97% |

---

## **Modelo Logístico**

P(Flood)=1/(1+e−(β0+β1I+β2API+β3D))P(Flood)=1/(1+e^{-(\\beta\_0+\\beta\_1I+\\beta\_2API+\\beta\_3D)})

Onde:

* (I) \= intensidade;  
* (API) \= precipitação antecedente;  
* (D) \= duração.

---

# **18\. Pipeline Recomendado**

## **Fase 1 — Simples**

* zonas manuais;  
* limiares básicos.

---

## **Fase 2 — Intermediária**

* clusterização automática;  
* calibração regional.

---

## **Fase 3 — Avançada**

* modelo probabilístico espacial;  
* machine learning;  
* nowcasting hidrológico.

---

# **19\. Ferramentas Recomendadas**

## **Linguagem**

* Python.

---

## **Bibliotecas**

| Biblioteca | Uso |
| ----- | ----- |
| Pandas | manipulação de dados |
| NumPy | cálculos numéricos |
| SciPy | ajuste de curvas |
| Scikit-Learn | clustering/modelos |
| Matplotlib | visualização |

---

# **20\. Conclusão**

O método pode ser adaptado com sucesso usando apenas pluviômetros.

A utilização de zonas pluviométricas melhora significativamente:

* precisão espacial;  
* redução de falsos alarmes;  
* robustez operacional.

A principal vantagem é transformar um limiar único em:

limiares regionais específicos para cada padrão de chuva

Isso torna o sistema muito mais próximo de um modelo operacional moderno de alerta de enchentes.

