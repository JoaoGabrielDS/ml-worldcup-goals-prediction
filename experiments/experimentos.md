# Rastreio de Experimentos

## Comparação de Versões de Features

| Versão | Features | Amostras Treino | MAE Teste (2022) | MAE CV | Wilcoxon vs v1 | Decisão |
|--------|----------|-----------------|------------------|--------|----------------|---------|
| v1 | 7 (baseline) | 216 | LR: 0.480 / RF: 0.451 / XGB: 0.560 | LR: 0.430 | — | Referência |
| v2 | 13 (+ amistosos/comp + ELO ponderado) | 216 | LR: 0.547 / RF: 0.582 / XGB: 0.579 | LR: 0.437 | p>0.05 | Descartada |
| v3 | 9 (+ ponderação dupla ELO × torneio) | 216 | LR: 0.530 / RF: 0.566 / XGB: 0.550 | LR: 0.426 | p>0.05 | Descartada |
| v4 | 9 (v1 + ELO médio adversários) | 216 | LR: 0.456 / RF: 0.461 / XGB: 0.519 | LR: 0.437 | p>0.05 | Base para v6 |
| v5 híbrido | 12 (v4 + valor de mercado) | 64 | LR: 0.458 / RF: 0.481 / XGB: 0.477 | LR: 0.444 | p>0.05 | Descartada — perde amostras |
| **v6** | **11 (v4 + histórico Copas)** | **216** | **LR: 0.446** / RF: 0.468 / XGB: 0.530 | **LR: 0.444** | p>0.05 | **Modelo final** |

---

## Experimentos Detalhados — Modelo Final (v6)

| Data | Modelo | Hiperparâmetros | MAE Teste | RMSE Teste | MAE CV | Std CV | Observações |
|------|--------|-----------------|-----------|------------|--------|--------|-------------|
| 2026-05-11 | Regressão Linear v6 | default | 0.4460 | 0.5346 | 0.4443 | 0.0619 | **Modelo final** — melhor MAE teste |
| 2026-05-11 | Random Forest v6 | n_estimators=100, random_state=42 | 0.4677 | 0.5631 | 0.4451 | 0.0500 | Wilcoxon p=0.156 vs v4 |
| 2026-05-11 | XGBoost v6 | n_estimators=100, random_state=42 | 0.5303 | 0.6271 | 0.5038 | 0.0557 | Pior dos três |

---

## Histórico Completo de Experimentos

| Data | Versão | Modelo | MAE Teste | MAE CV | Observações |
|------|--------|--------|-----------|--------|-------------|
| 2026-05-09 | v1 | Regressão Linear | 0.480 | 0.430 | Baseline |
| 2026-05-09 | v1 | Random Forest | 0.451 | 0.445 | Melhor MAE teste v1 |
| 2026-05-09 | v1 | XGBoost | 0.560 | 0.528 | Dataset pequeno — pior desempenho |
| 2026-05-10 | v2 | Regressão Linear | 0.547 | 0.437 | 6 features novas — overfitting |
| 2026-05-10 | v2 | Random Forest | 0.582 | 0.444 | Pior que v1 |
| 2026-05-10 | v3 | Regressão Linear | 0.530 | 0.426 | Ponderação torneio × ELO |
| 2026-05-10 | v4 | Regressão Linear | 0.456 | 0.437 | ELO médio adversários |
| 2026-05-10 | v4 | Random Forest | 0.461 | 0.452 | Wilcoxon p=0.44 vs v1 |
| 2026-05-10 | v5 | XGBoost | 0.477 | 0.494 | Melhorou com valor de mercado |
| 2026-05-11 | v6 | Regressão Linear | 0.446 | 0.444 | Menor MAE teste — modelo final |
| 2026-05-11 | v6 | Random Forest | 0.468 | 0.445 | Wilcoxon p=0.156 |

---

## Validação Cruzada Temporal (Walk-Forward) — Modelo Final

Folds: Copas [1994] → teste 1998, [1994,1998] → teste 2002, ... [1994–2018] → teste 2022

| Modelo | MAE Médio | Desvio-Padrão |
|--------|-----------|---------------|
| Regressão Linear v6 | 0.4443 | 0.0619 |
| Random Forest v6 | 0.4451 | 0.0500 |
| XGBoost v6 | 0.5038 | 0.0557 |

---

## Teste de Wilcoxon — Modelo Final (v6)

| Comparação | p-value | Significativo? |
|------------|---------|----------------|
| LR v4 vs RF v4 | 0.5625 | Não |
| LR v4 vs XGB v4 | 0.0312 | Sim (p<0.05) |
| RF v4 vs XGB v4 | 0.0312 | Sim (p<0.05) |
| RF v4 vs RF v6 | 0.1562 | Não |
| LR v4 vs LR v6 | 0.4375 | Não |

**Conclusão:** XGBoost é significativamente pior que LR e RF. Entre LR e RF, a diferença não é estatisticamente significativa — LR escolhida pelo princípio da parcimônia e melhor MAE no teste.

---

## Validação Externa — Correlação com Valor de Mercado

| Versão | Correlação Previsão × Valor de Mercado |
|--------|----------------------------------------|
| v4 (ensemble) | 0.54 |
| v6 (LR only) | **0.68** |

A correlação de 0.68 com o valor de mercado do Transfermarkt — dado nunca visto pelo modelo durante o treino — confirma a consistência das previsões.
