# Previsão de Média de Gols na FIFA World Cup com Machine Learning

**Disciplina de Machine Learning — AV2 | 2026**

---

## Resumo

> A preencher após resultados. Breve descrição do problema, metodologia, principais resultados e conclusão. (150–250 palavras)

---

## 1. Introdução

A Copa do Mundo da FIFA é o maior evento esportivo do planeta, disputado a cada quatro anos. A capacidade de prever o desempenho ofensivo das seleções participantes tem aplicações em análise tática, jornalismo esportivo e mercado de apostas. Este trabalho propõe um modelo de Machine Learning para prever a **média de gols marcados por jogo** de cada seleção na Copa do Mundo, combinando dois horizontes temporais: o desempenho no ciclo completo da Copa (quatro anos) e a forma recente (últimos 15 jogos antes do torneio).

O dataset utilizado é o *International Football Results from 1872 to 2026*, disponível no Kaggle, contendo registros de partidas internacionais ao longo de mais de 150 anos.

---

## 2. Metodologia

### 2.1 Dados e Preparação

> Descrever origem, filtragem e criação das features.

### 2.2 Engenharia de Features

> Descrever o ciclo da Copa, a janela de 15 jogos e demais features.

### 2.3 Modelos

> Regressão Linear (baseline), Random Forest, XGBoost.

### 2.4 Validação

> Divisão temporal: treino 1994–2018, teste 2022, previsão 2026.

---

## 3. Resultados

> Tabela comparativa de modelos com MAE e RMSE.

---

## 4. Discussão

> Análise dos erros, importância de features, comparação com baseline.

---

## 5. Limitações e Ameaças à Validade

- **Amistosos vs. competitivos:** amistosos tendem a ter mais gols e podem distorcer as médias.
- **Seleções com poucos jogos:** features menos confiáveis para times com ciclos curtos.
- **Mudanças de geração:** o modelo não captura trocas de treinador ou renovação do elenco.
- **Overfitting:** risco de ajuste excessivo dado o número limitado de Copas disponíveis.
- **Validade externa:** os padrões históricos podem não se reproduzir em Copas futuras com novos formatos.

---

## 6. Conclusão

> A preencher após resultados.

---

## Referências

1. Hvattum, L. M., & Arntzen, H. (2010). Using ELO ratings for match result prediction in association football. *International Journal of Forecasting*, 26(3), 460–470.
2. Dixon, M. J., & Coles, S. G. (1997). Modelling association football scores and inefficiencies in the football betting market. *Journal of the Royal Statistical Society*, 46(2), 265–280.
3. Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.
4. Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *KDD '16*.
5. Kaggle. (2024). International football results from 1872 to 2026. Disponível em: https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017
