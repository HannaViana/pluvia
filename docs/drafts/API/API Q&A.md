tem como fazer isso usando zonas pluviometricas?

Sim — e na prática isso costuma ser uma abordagem MUITO melhor do que usar um limiar único para toda a região.

O que você faria é transformar o método da tese em um sistema:

limiar por zona pluviométrica

em vez de:

um limiar para toda a bacia/cidade/estado

Isso resolve um dos maiores problemas desses modelos:

a chuva “significa” coisas diferentes em lugares diferentes.

Intuição física

Imagine uma cidade com:

morro  
baixada  
área urbana densa  
área rural  
litoral

A mesma chuva:

50 mm/h

pode:

não causar nada numa área permeável;  
causar inundação grave numa área impermeabilizada.

Então faz muito sentido dividir em zonas homogêneas.

O que é uma zona pluviométrica nesse contexto

Você agrupa áreas que têm comportamento parecido de chuva.

Pode ser baseado em:

climatologia;  
relevo;  
altitude;  
regime convectivo/orográfico;  
radar;  
clusters estatísticos.

Cada zona terá:

seu próprio limiar inferior;  
seu próprio limiar superior;  
sua própria curva API × intensidade.  
Estrutura geral

O sistema fica assim:

Zona A → limiares A  
Zona B → limiares B  
Zona C → limiares C  
Como adaptar o método  
PASSO 1 — Dividir a área em zonas

Existem 4 maneiras principais.

Opção 1 — Manual (mais simples)

Você define baseado em conhecimento hidrológico.

Exemplo:

Zona    Característica  
Z1    Serra  
Z2    Área urbana  
Z3    Baixada  
Z4    Litoral

Boa para protótipo.

Opção 2 — Isoietas / climatologia

Usa médias históricas de precipitação.

Você agrupa regiões com:

sazonalidade semelhante;  
intensidade semelhante;  
frequência semelhante.  
Opção 3 — Clusterização estatística

Essa é a mais elegante.

Você cria vetores com:

média anual;  
percentis extremos;  
intensidade máxima;  
duração típica;  
sazonalidade;  
API médio;  
altitude.

Depois aplica:

K-Means;  
Hierarchical Clustering;  
Gaussian Mixture.

Resultado:

zonas hidrometeorologicamente homogêneas  
Opção 4 — Radar meteorológico

Você pode usar:

CAPPI;  
frequência convectiva;  
assinaturas espaciais.

Muito usado operacionalmente.

Depois da divisão

Você executa o MESMO método da tese dentro de cada zona.

Ou seja:

Para cada zona:  
1\. Separar eventos  
chuvas \+ enchentes daquela zona  
2\. Calcular  
intensidade;  
duração;  
API.  
3\. Ajustar limiares  
inferior;  
superior.  
4\. Ajustar curva API

I  
z  
    ​

\=a  
z  
    ​

e  
b  
z  
    ​

API  
\+c  
z  
    ​

Agora cada zona tem:

a  
z  
    ​

b  
z  
    ​

c  
z  
    ​

próprios.

Resultado operacional

Quando chega chuva nova:

Etapa 1

Detecta em qual zona está chovendo.

Etapa 2

Calcula:

intensidade;  
duração;  
API.  
Etapa 3

Usa os limiares DAQUELA ZONA.

Exemplo intuitivo  
Zona urbana impermeável

Pode gerar enchente com:

20 mm/h  
Zona rural permeável

Talvez precise:

50 mm/h

Um limiar único destruiria a precisão.

O ganho estatístico costuma ser enorme

Porque você reduz:

heterogeneidade;  
variância interna;  
falsos alarmes.

Normalmente melhora:

POD;  
HK;  
FAR.  
O que eu recomendo fortemente

Em vez de:

intensidade × duração

eu faria:

intensidade × duração × zona

Ou até:

intensidade × duração × API × zona  
Melhor ainda: usar zonas hidrológicas \+ pluviométricas

Você pode combinar:

Informação    Influência  
Chuva    gatilho  
Uso do solo    resposta  
Declividade    escoamento  
Drenagem    inundação  
Impermeabilização    pico rápido

Isso gera zonas MUITO mais robustas.

Estrutura computacional recomendada

Você teria algo assim:

zonas \= {  
    "Z1": modelo\_z1,  
    "Z2": modelo\_z2,  
    "Z3": modelo\_z3  
}

Cada modelo contém:

limiar inferior;  
limiar superior;  
curva API;  
métricas.  
Uma melhoria MUITO poderosa

Em vez de limites “duros”, você pode gerar:

probabilidade de enchente

Exemplo:

Zona    Probabilidade  
Z1    15%  
Z2    82%  
Z3    97%

Isso é operacionalmente MUITO superior.

Como isso é feito

Você transforma o limiar em:

regressão logística;  
random forest;  
XGBoost.

Exemplo:

P(Flood)=  
1+e  
−(β  
0  
    ​

\+β  
1  
    ​

I+β  
2  
    ​

API+β  
3  
    ​

D)  
1  
    ​

Onde:

I \= intensidade;  
API \= chuva antecedente;  
D \= duração.  
Isso vira um sistema moderno de nowcasting hidrológico

Muito parecido com:

CEMADEN;  
JMA;  
sistemas europeus;  
flash flood guidance.  
O que eu faria no seu lugar  
Fase 1 — simples

Criar:

zonas manuais

e aplicar exatamente o método da tese.

Fase 2 — intermediária

Trocar por:

clusterização automática  
Fase 3 — avançada

Migrar de:

limiar

para:

modelo probabilístico espacial  
Resumindo

Sim, o método funciona MUITO bem com zonas pluviométricas — e provavelmente fica melhor do que o modelo original — porque você reduz a heterogeneidade espacial e cria limiares específicos para cada regime de chuva e resposta hidrológica.