# Rastreio de Experimentos

| Data | Modelo | Hiperparâmetros | MAE Treino | MAE Teste | RMSE Treino | RMSE Teste | Observações |
|------|--------|-----------------|------------|-----------|-------------|------------|-------------|
| 2026-05-09 | Regressão Linear | default | - | 0.4800 | - | 0.5651 | Baseline — conservador, evita extremos |
| 2026-05-09 | Random Forest | n_estimators=100, random_state=42 | - | 0.4512 | - | 0.5789 | Melhor MAE, mas RMSE maior que Linear |
| 2026-05-09 | XGBoost | n_estimators=100, random_state=42 | - | 0.5603 | - | 0.6874 | Pior dos três — dataset pequeno demais |