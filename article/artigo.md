# Previsão de Média de Gols na FIFA World Cup 2026 com Machine Learning

**Disciplina de Machine Learning — AV2 | 2026**

---

## Resumo

Este trabalho propõe um modelo de Machine Learning para prever a média de gols marcados por jogo de cada seleção na Copa do Mundo da FIFA 2026. Utilizando o dataset *International Football Results from 1872 to 2026* (Kaggle), foram construídas features a partir do ciclo preparatório de quatro anos, da forma recente (últimos 15 jogos), do ELO histórico dos adversários e do desempenho em Copas anteriores. Três algoritmos foram avaliados — Regressão Linear, Random Forest e XGBoost — com validação cruzada temporal (walk-forward) e teste estatístico de Wilcoxon. O modelo final, Regressão Linear com 11 features (v6), obteve MAE de 0,446 gols por jogo no conjunto de teste (Copa 2022) e correlação de 0,68 com o valor de mercado dos elencos, dado não utilizado durante o treino. Seis versões de features foram testadas sistematicamente, demonstrando que modelos mais simples generalizam melhor com o tamanho reduzido do dataset (248 amostras). As previsões para 2026 indicam Espanha (2,17 gols/jogo) e Argentina (2,01) como as seleções com maior potencial ofensivo.

---

## 1. Introdução

A Copa do Mundo da FIFA é o maior evento esportivo do planeta, reunindo 48 seleções a partir de 2026. A capacidade de prever o desempenho ofensivo das equipes participantes tem aplicações em análise tática, jornalismo esportivo e estudos acadêmicos sobre modelagem de eventos esportivos.

Modelos preditivos em futebol enfrentam um desafio fundamental: a alta variância inerente ao esporte. Um único jogo pode ser decidido por um erro defensivo ou um momento de brilhantismo individual, tornando qualquer previsão determinística inadequada. A abordagem estatística, ao trabalhar com médias ao longo de múltiplos jogos, mitiga essa variância e permite identificar padrões consistentes de desempenho.

Este trabalho propõe um modelo para prever a **média de gols marcados por jogo** de cada seleção na Copa do Mundo, combinando quatro dimensões de informação: o desempenho no ciclo completo de preparação (quatro anos), a forma recente (últimos 15 jogos), a qualidade dos adversários enfrentados (ELO rating) e o histórico em Copas anteriores. O modelo é treinado com dados de oito Copas (1994–2022) e aplicado para gerar previsões para a Copa 2026.

---

## 2. Metodologia

### 2.1 Dados e Preparação

O dataset principal é o *International Football Results from 1872 to 2026* (Kaggle), contendo 49.287 partidas internacionais. Os arquivos utilizados foram `results.csv` (resultados) e `shootouts.csv` (decisões por pênaltis). Como fonte adicional, valores de mercado dos elencos foram coletados do Transfermarkt para as Copas de 2014 a 2026, utilizados como validação externa.

O período de interesse foi definido a partir de 1990, considerando as Copas de 1994 a 2022 como conjunto de treino e teste. Para cada Copa alvo, o **ciclo preparatório** compreende todos os jogos disputados entre o encerramento da Copa anterior e o início da Copa alvo, excluindo jogos de Copa do Mundo — estes são utilizados exclusivamente para calcular o target.

A variável-alvo é a média de gols marcados por jogo de cada seleção dentro da Copa correspondente. O dataset final contém 248 amostras (seleção × Copa).

### 2.2 Engenharia de Features

Foram desenvolvidas e testadas seis versões de features, descritas na Tabela 1. A versão final (v6) contém 11 features organizadas em quatro grupos:

**Grupo 1 — Desempenho no ciclo (4 anos):**
- `media_gols_marcados_ciclo`: média de gols marcados por jogo no ciclo completo
- `media_gols_sofridos_ciclo`: média de gols sofridos por jogo no ciclo
- `pct_vitorias_ciclo`: percentual de vitórias no ciclo
- `total_jogos_ciclo`: total de jogos disputados no ciclo

**Grupo 2 — Forma recente (últimos 15 jogos):**
- `media_gols_marcados_ult15`: média de gols marcados nos últimos 15 jogos
- `media_gols_sofridos_ult15`: média de gols sofridos nos últimos 15 jogos
- `pct_vitorias_ult15`: percentual de vitórias nos últimos 15 jogos

A janela de 15 jogos representa aproximadamente 1,5 ano de competições, equilibrando estabilidade estatística e recência. Janelas menores (10 jogos) mostraram-se instáveis; janelas maiores (20 jogos) sobrepõem-se ao ciclo completo.

**Grupo 3 — Qualidade dos adversários (ELO):**
- `elo_medio_adv_ciclo`: ELO médio dos adversários enfrentados no ciclo
- `elo_medio_adv_ult15`: ELO médio dos adversários nos últimos 15 jogos

O ELO foi calculado a partir de todos os jogos disponíveis desde 1872, com fator K=40 para jogos competitivos e K=20 para amistosos, seguindo Hvattum & Arntzen (2010). Esta feature corrige o viés de seleções que jogam contra adversários sistematicamente mais fracos em suas eliminatórias regionais.

**Grupo 4 — Histórico em Copas:**
- `media_gols_ultimas2_copas`: média de gols marcados nas duas Copas anteriores (0 se não participou)
- `fase_ultima_copa`: fase atingida na Copa imediatamente anterior (0=não classificou, 1=grupos, 2=oitavas, 3=quartas, 4=semi, 5=vice, 6=campeão)

A função de cálculo de fase foi corrigida para utilizar `shootouts.csv` na determinação do vencedor em jogos decididos por pênaltis, e para distinguir o jogo do 3º lugar da final — erros que classificavam incorretamente Argentina como vice-campeã 2022 e Croácia como campeã.

### 2.3 Modelos

Três algoritmos foram avaliados:

- **Regressão Linear:** baseline interpretável, verifica se relações lineares são suficientes
- **Random Forest:** captura não-linearidades via ensemble de árvores de decisão
- **XGBoost:** gradient boosting, estado da arte para dados tabulares

Todos os modelos foram treinados com `random_state=42` para garantir reprodutibilidade.

### 2.4 Validação

A divisão treino/teste respeita a ordem temporal: as Copas de 1994 a 2018 compõem o conjunto de treino (216 amostras) e a Copa 2022 o conjunto de teste (32 amostras). Esta abordagem evita data leakage temporal.

A validação cruzada utiliza o método **walk-forward**: em cada fold, o modelo é treinado nas Copas anteriores e testado na Copa seguinte, avançando uma Copa por vez (6 folds no total). Este método é o mais adequado para dados com dependência temporal.

A comparação estatística entre modelos utiliza o **teste de Wilcoxon** (não-paramétrico, adequado para amostras pequenas), com nível de significância α = 0,05.

---

## 3. Resultados

### 3.1 Comparação de Versões de Features

A Tabela 1 apresenta o desempenho das seis versões de features testadas com Regressão Linear no conjunto de teste (Copa 2022).

**Tabela 1 — Comparação de versões de features (Regressão Linear)**

| Versão | Features | Amostras | MAE Teste | MAE CV | Δ vs v1 |
|--------|----------|----------|-----------|--------|---------|
| v1 (baseline) | 7 | 216 | 0,480 | 0,430 | — |
| v2 (+ amistosos/comp + ELO ponderado) | 13 | 216 | 0,547 | 0,437 | +14% |
| v3 (+ ponderação dupla ELO × torneio) | 9 | 216 | 0,530 | 0,426 | +10% |
| v4 (+ ELO médio adversários) | 9 | 216 | 0,456 | 0,437 | -5% |
| v5 (v4 + valor de mercado) | 12 | 64 | 0,458 | 0,444 | -5% |
| **v6 (v4 + histórico Copas)** | **11** | **216** | **0,446** | **0,444** | **-7%** |

A v4 introduziu o ELO médio dos adversários, que corrigiu o viés de seleções com ciclos regionais mais fáceis. A v6 adicionou o histórico de Copas anteriores, mantendo as 216 amostras de treino e obtendo o menor MAE no teste.

### 3.2 Comparação de Modelos — Versão Final (v6)

**Tabela 2 — Comparação de modelos com features v6**

| Modelo | MAE Teste | RMSE Teste | MAE CV | Std CV |
|--------|-----------|------------|--------|--------|
| **Regressão Linear** | **0,446** | **0,535** | 0,444 | 0,062 |
| Random Forest | 0,468 | 0,563 | **0,445** | 0,050 |
| XGBoost | 0,530 | 0,627 | 0,504 | 0,056 |

O teste de Wilcoxon indicou que XGBoost é significativamente pior que Regressão Linear (p=0,031). A diferença entre Regressão Linear e Random Forest não é estatisticamente significativa (p=0,156), sendo a Regressão Linear preferida pelo princípio da parcimônia e pelo melhor MAE no teste.

### 3.3 Por que a Regressão Linear supera modelos complexos?

Com 216 amostras de treino, Random Forest e XGBoost sofreram overfitting e aprenderam correlações espúrias. Em particular, aprenderam que ELO alto dos adversários correlaciona negativamente com gols na Copa — um viés identificado na análise da seleção francesa, que possui o maior ELO médio de adversários do dataset (1.264) e foi fortemente penalizada pelos modelos não-lineares. A Regressão Linear, por sua simplicidade, não captura esse tipo de interação espúria.

### 3.4 Coeficientes do Modelo Final

Os coeficientes da Regressão Linear v6, ordenados por magnitude absoluta:

| Feature | Coeficiente |
|---------|-------------|
| `pct_vitorias_ult15` | −0,915 |
| `pct_vitorias_ciclo` | +0,432 |
| `media_gols_marcados_ult15` | +0,399 |
| `media_gols_sofridos_ciclo` | −0,363 |
| `media_gols_ultimas2_copas` | +0,140 |
| `media_gols_sofridos_ult15` | −0,086 |
| `media_gols_marcados_ciclo` | +0,053 |

O coeficiente negativo de `pct_vitorias_ult15` é contra-intuitivo mas explicável: seleções com muitas vitórias recentes frequentemente jogaram contra adversários fracos, o que já é capturado pelo ELO médio dos adversários. O sinal positivo de `media_gols_ultimas2_copas` confirma que o histórico em Copas é um preditor relevante.

### 3.5 Validação Externa — Correlação com Valor de Mercado

A correlação de Pearson entre as previsões do modelo final e o valor de mercado dos elencos (Transfermarkt, 2026) foi de **0,68**. Como o valor de mercado não foi utilizado durante o treino, esta correlação constitui uma validação externa da consistência do modelo: seleções com elencos mais valiosos tendem a ter previsões de gols mais altas.

### 3.6 Previsões para a Copa 2026

**Tabela 3 — Top 20 seleções por média de gols prevista (Copa 2026)**

| Posição | Seleção | Confederação | Previsão | Valor de Mercado |
|---------|---------|--------------|----------|------------------|
| 1 | Espanha | UEFA | 2,17 | €1.150M |
| 2 | Argentina | CONMEBOL | 2,01 | €575M |
| 3 | Netherlands | UEFA | 1,93 | €808M |
| 4 | Colombia | CONMEBOL | 1,92 | €285M |
| 5 | Portugal | UEFA | 1,92 | €841M |
| 6 | Belgium | UEFA | 1,86 | €442M |
| 7 | England | UEFA | 1,84 | €1.300M |
| 8 | France | UEFA | 1,80 | €1.290M |
| 9 | Norway | UEFA | 1,71 | €503M |
| 10 | Brazil | CONMEBOL | 1,71 | €932M |
| 11 | Germany | UEFA | 1,70 | €828M |
| 12 | Croatia | UEFA | 1,68 | €258M |
| 13 | Japan | AFC | 1,62 | €224M |
| 14 | Ecuador | CONMEBOL | 1,60 | €350M |
| 15 | Switzerland | UEFA | 1,59 | €251M |
| 16 | New Zealand | OFC | 1,54 | — |
| 17 | Senegal | CAF | 1,47 | €406M |
| 18 | Austria | UEFA | 1,45 | €232M |
| 19 | Uruguay | CONMEBOL | 1,42 | €419M |
| 20 | Canada | CONCACAF | 1,34 | — |

**Médias previstas por confederação:**

| Confederação | Média prevista |
|--------------|----------------|
| CONMEBOL | 1,65 |
| UEFA | 1,56 |
| OFC | 1,54 |
| CONCACAF | 1,09 |
| AFC | 1,07 |
| CAF | 1,03 |

---

## 4. Discussão

### 4.1 Análise das Previsões

Espanha lidera com 2,17 gols por jogo — justificado pelo ciclo ofensivo mais forte do dataset (2,67 gols/jogo no ciclo, 2,93 nos últimos 15 jogos) combinado com o título da Eurocopa 2024. Argentina em segundo reflete o status de campeã mundial vigente (fase 6 na Copa 2022) e ciclo sólido nas Eliminatórias CONMEBOL.

A CONMEBOL superou a UEFA na média prevista (1,65 vs 1,56), o que é historicamente defensável: as Eliminatórias sul-americanas são amplamente reconhecidas como as mais disputadas do mundo, com ELO médio de adversários superior ao de outras confederações. Seleções sul-americanas "fracas" como Venezuela e Paraguai enfrentaram Argentina, Brasil e Colômbia durante o ciclo — o que eleva suas features mesmo com ciclos modestos.

France em 8º (1,80) é coerente com o ciclo 2022–2026 irregular, apesar da posição de vice-campeã em 2022 e campeã em 2018. O modelo captura corretamente que o potencial histórico não compensa uma forma recente inconsistente.

### 4.2 Limitações do Modelo

A principal limitação identificada é **New Zealand em 16º** (1,54): como único representante da OFC, a seleção joga contra adversários com ELO médio muito baixo durante o ciclo, inflando suas features de gols marcados. Esta distorção é documentada e esperada, dado que o modelo não possui mecanismo para penalizar a qualidade do calendário regional.

**Colombia em 4º** (1,92) pode ser questionada por não ter participado da Copa 2022 (fase=0), mas é sustentada pelo ciclo excepcional nas Eliminatórias CONMEBOL — o maior ELO médio de adversários do dataset (1.328), indicando que jogou contra os times mais fortes.

### 4.3 Evolução das Features

A jornada de v1 a v6 ilustra o trade-off entre riqueza de features e tamanho do dataset. Versões mais complexas (v2, v3) introduziram mais informação mas causaram overfitting com as 216 amostras disponíveis. A v4 identificou a feature mais impactante (ELO dos adversários), e a v6 acrescentou o histórico de Copas sem reduzir as amostras de treino — resultando no melhor MAE no teste.

---

## 5. Limitações e Ameaças à Validade

- **Tamanho do dataset:** 248 amostras (8 Copas × ~31 seleções) é reduzido para aprendizado de modelos complexos, favorecendo algoritmos mais simples como Regressão Linear.
- **Ausência de dados contextuais:** lesões de jogadores-chave, mudanças de treinador e contexto tático não são capturados.
- **Ciclo 2026 incompleto:** os dados disponíveis vão até março/2026 — jogos dos meses finais do ciclo podem estar ausentes.
- **Viés regional:** seleções da OFC e de confederações menores têm ELO médio de adversários artificialmente baixo, inflando suas médias de gols.
- **Novo formato:** a Copa 2026 terá 48 seleções e grupos de 3 equipes — padrão diferente das Copas de treino (32 seleções, grupos de 4), podendo alterar a dinâmica de gols na fase de grupos.
- **Validade externa:** padrões históricos de 1994–2022 podem não se reproduzir integralmente em 2026.
- **Erro esperado:** ~0,45 gols por jogo por seleção, baseado na validação cruzada.

---

## 6. Conclusão

Este trabalho desenvolveu um pipeline completo de Machine Learning para previsão de desempenho ofensivo na Copa do Mundo da FIFA, desde a engenharia de features até a previsão final para 2026. O modelo final — Regressão Linear com 11 features — demonstrou que a simplicidade supera a complexidade quando o dataset é limitado, resultado alinhado com o princípio da parcimônia em modelagem estatística.

A principal contribuição metodológica foi a incorporação do ELO médio dos adversários como feature, que corrigiu o viés de seleções com calendários regionais mais fáceis e elevou a correlação externa com valor de mercado de 0,54 para 0,68. A correção da função de fase (pênaltis e jogo do 3º lugar) garantiu a integridade dos dados históricos de Copas.

A jornada sistemática por seis versões de features produziu resultados científicamente honestos: nem todas as melhorias tentadas funcionaram, e as que não funcionaram são igualmente informativas — revelando os limites do que é possível prever com dados históricos de jogos em um esporte de alta variância.

Para trabalhos futuros, sugere-se: (i) incorporar dados de valor de mercado histórico completo (pré-1994), (ii) explorar features baseadas em redes sociais de passes e métricas táticas avançadas, e (iii) modelar a incerteza das previsões via intervalos de confiança bootstrap.

---

## Referências

1. Hvattum, L. M., & Arntzen, H. (2010). Using ELO ratings for match result prediction in association football. *International Journal of Forecasting*, 26(3), 460–470.
2. Dixon, M. J., & Coles, S. G. (1997). Modelling association football scores and inefficiencies in the football betting market. *Journal of the Royal Statistical Society*, 46(2), 265–280.
3. Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.
4. Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 785–794).
5. Kaggle. (2026). International football results from 1872 to 2026. Disponível em: https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017
6. James, G., Witten, D., Hastie, T., & Tibshirani, R. (2013). *An Introduction to Statistical Learning*. Springer.
7. Transfermarkt. (2026). FIFA World Cup participants and squad values. Disponível em: https://www.transfermarkt.com/world-cup/teilnehmer/pokalwettbewerb/FIWC
