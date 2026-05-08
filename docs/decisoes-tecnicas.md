# Decisões Técnicas

## 1. Definição do Ciclo da Copa

**Decisão:** O ciclo começa imediatamente após o encerramento da Copa anterior e termina na data de início da Copa alvo.

**Justificativa:** O ciclo representa o período de preparação da seleção para aquela Copa específica. Jogos da Copa do Mundo anterior não fazem parte desse ciclo — são um evento separado com dinâmica diferente (pressão, seleção de jogadores, fases eliminatórias).

---

## 2. Janela de Forma Recente: 15 Jogos

**Decisão:** Usar os últimos 15 jogos do ciclo como janela de forma recente.

**Justificativa:** Uma seleção disputa em média 8–12 jogos por ano. 15 jogos representa aproximadamente 1,5 ano — suficiente para capturar a forma atual sem duplicar o que o ciclo de 4 anos já cobre. Janelas menores (10 jogos) são instáveis demais; janelas maiores (20 jogos) sobrepõem muito com o ciclo.

---

## 3. Exclusão de Jogos da Copa do Mundo das Features

**Decisão:** Jogos de Copa do Mundo são usados **apenas para calcular o target**, nunca como features.

**Justificativa:** Evitar data leakage. As features devem representar apenas o que se sabia antes da Copa começar.

---

## 4. Divisão Treino/Teste Temporal

**Decisão:** Treino em Copas de 1994–2018, teste na Copa de 2022.

**Justificativa:** A ordem temporal deve ser respeitada. Usar Copas futuras no treino seria data leakage. A validação temporal (walk-forward) é o método mais robusto para dados com dependência temporal.

---

## 5. Métricas de Avaliação

**Decisão:** MAE como métrica primária, RMSE como secundária.

**Justificativa:** O problema é de regressão. MAE é mais interpretável (erro em gols por jogo). RMSE penaliza erros grandes, útil para identificar previsões muito distantes.

---

## 6. Modelos Escolhidos

| Modelo | Justificativa |
|--------|--------------|
| Regressão Linear | Baseline interpretável; verifica se relação linear já é suficiente |
| Random Forest | Captura não-linearidades; robusto a outliers |
| XGBoost | Estado da arte para dados tabulares estruturados |

**Trade-off:** Regressão Linear é mais interpretável; XGBoost tende a ter melhor desempenho mas é caixa-preta. Usamos SHAP values para interpretar o XGBoost.
