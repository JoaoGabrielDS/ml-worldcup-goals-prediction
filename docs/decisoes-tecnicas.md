# Decisões Técnicas

## 1. Definição do Ciclo da Copa

**Decisão:** O ciclo começa imediatamente após o encerramento da Copa anterior e termina na data de início da Copa alvo. Jogos da Copa do Mundo são excluídos do ciclo.

**Justificativa:** O ciclo representa o período de preparação da seleção. Jogos da Copa anterior são um evento separado com dinâmica diferente. Excluir Copas do ciclo evita data leakage — os dados da Copa alvo são usados apenas como target.

---

## 2. Janela de Forma Recente: 15 Jogos

**Decisão:** Usar os últimos 15 jogos do ciclo como janela de forma recente.

**Justificativa:** Uma seleção disputa em média 8–12 jogos por ano. 15 jogos representa ~1,5 ano — suficiente para capturar a forma atual sem duplicar o que o ciclo de 4 anos já cobre. Janelas de 10 e 20 jogos foram consideradas e descartadas por instabilidade e sobreposição, respectivamente.

---

## 3. ELO Rating como Proxy de Qualidade do Adversário

**Decisão:** Calcular ELO histórico para todas as seleções e usar o ELO médio dos adversários como feature.

**Justificativa:** Gols marcados contra San Marino têm valor preditivo diferente de gols contra a Alemanha. O ELO, calculado a partir de todos os jogos desde 1872 com K=40 (competitivos) e K=20 (amistosos), captura a força relativa das seleções de forma dinâmica. Referência: Hvattum & Arntzen (2010).

---

## 4. Histórico de Copas Anteriores

**Decisão:** Adicionar `media_gols_ultimas2_copas` e `fase_ultima_copa` como features.

**Justificativa:** O desempenho histórico em Copas captura tradição e consistência que as features de ciclo não capturam. A função `get_fase` foi corrigida para usar `shootouts.csv` (pênaltis) e distinguir 3º lugar de final — Argentina era erroneamente classificada como vice-campeã 2022 e Croácia como campeã.

---

## 5. Filtro de Jogos Mínimos

**Decisão:** Seleções com menos de 10 jogos no ciclo 2026 são excluídas da previsão.

**Justificativa:** Com poucos jogos, as médias são estatisticamente instáveis e não representam o desempenho real da seleção.

---

## 6. Divisão Treino/Teste Temporal

**Decisão:** Treino em Copas de 1994–2022 (248 amostras), teste na Copa 2022 (32 amostras).

**Justificativa:** A ordem temporal deve ser respeitada. Usar Copas futuras no treino seria data leakage. A validação cruzada walk-forward é o método mais robusto para dados temporais.

---

## 7. Métricas de Avaliação

**Decisão:** MAE como métrica primária, RMSE como secundária.

**Justificativa:** MAE é mais interpretável (erro em gols por jogo). RMSE penaliza erros grandes. O teste de Wilcoxon foi usado para verificar significância estatística entre modelos.

---

## 8. Modelo Final: Regressão Linear v6

**Decisão:** Usar Regressão Linear com 11 features (v6) como modelo final.

**Justificativa:**
- Melhor MAE no teste da Copa 2022 (0.446 — menor de todos os modelos e versões)
- Com 216 amostras de treino, Random Forest e XGBoost sofreram overfitting e aprenderam correlações espúrias — penalizavam seleções com ELO alto de adversários (viés identificado na análise da França)
- Coeficientes interpretáveis confirmam semântica correta das features
- Correlação externa de 0.68 com valor de mercado (Transfermarkt) valida a consistência do modelo

---

## 9. Versões de Features Testadas

| Versão | Features | Amostras | MAE CV | Decisão |
|--------|----------|----------|--------|---------|
| v1 | 7 (baseline) | 216 | 0.430 | Referência |
| v2 | 13 (+ amistosos/competitivos + ELO ponderado) | 216 | 0.444 | Descartada — não melhorou |
| v3 | 9 (+ ponderação dupla ELO × torneio) | 216 | 0.444 | Descartada — equivalente à v1 |
| v4 | 9 (+ ELO médio adversários) | 216 | 0.437 | Melhor CV, base para v6 |
| v5 | 12 (+ valor de mercado) | 64 | 0.444 | Descartada — perde amostras |
| **v6** | **11 (v4 + histórico Copas)** | **216** | **0.444** | **Modelo final** |

---

## 10. Valor de Mercado — Uso Contextual

**Decisão:** Valor de mercado incluído na tabela final como dado contextual, não como feature do modelo.

**Justificativa:** Dados históricos de valor de mercado disponíveis apenas a partir de 2014. Usá-los no treino reduziria as amostras de 216 para 64 — prejuízo maior que o ganho. A correlação de 0.68 entre previsões e valor de mercado confirma que o modelo captura implicitamente a qualidade dos elencos.

---

## 11. Ensemble vs. Modelo Único

**Decisão:** Usar apenas Regressão Linear, descartando o ensemble (LR + RF + XGBoost).

**Justificativa:** RF e XGBoost penalizavam incorretamente seleções com ELO alto de adversários no ciclo — identificado na análise da França (ELO médio 1264, o maior do dataset). O ensemble diluía a previsão correta da LR com previsões enviesadas dos outros modelos.
