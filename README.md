# Previsão de Média de Gols na FIFA World Cup 2026

Projeto de Machine Learning — AV2
Disciplina de Machine Learning | 2026

---

## Objetivo

Prever a **média de gols marcados por jogo** de cada seleção na Copa do Mundo da FIFA 2026, combinando:
- Desempenho no **ciclo da Copa** (jogos entre a Copa anterior e a atual, excluindo Copas do Mundo)
- **Forma recente** (últimos 15 jogos antes da Copa)
- **ELO médio dos adversários** (pondera a qualidade dos times enfrentados)
- **Histórico de Copas anteriores** (fase atingida e média de gols nas 2 últimas Copas)

**Variável-alvo:** média de gols marcados por jogo na Copa do Mundo

---

## Dataset

- **Fonte principal:** [International football results from 1872 to 2026](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017)
- **Arquivos utilizados:** `results.csv`, `shootouts.csv`
- **Fonte adicional:** Valor de mercado dos elencos (Transfermarkt, 2014–2026) — `football_team_values_2010_2026.xlsx`
- **Período de treino:** Copas de 1994 a 2022 (248 amostras)

### Como baixar o dataset

1. Acesse o link do Kaggle (necessário ter conta)
2. Clique em **Download** e extraia o ZIP
3. Coloque os arquivos CSV em `data/raw/`
4. Coloque o arquivo Excel de valor de mercado em `data/raw/`

---

## Instalação

```bash
# Clone o repositório
git clone https://github.com/JoaoGabrielDS/ml-worldcup-goals-prediction
cd ml-worldcup-goals-prediction

# Instale as dependências
pip install -r requirements.txt

# Inicie o Jupyter
jupyter notebook
```

**Python:** 3.11.3

---

## Execução

Execute os notebooks na seguinte ordem:

| Ordem | Notebook | Descrição |
|-------|----------|-----------|
| 1 | `notebooks/01_eda.ipynb` | Análise exploratória dos dados |
| 2 | `notebooks/02_features_v6.ipynb` | Engenharia de features (versão final) |
| 3 | `notebooks/03_modelos_v6.ipynb` | Treino, validação e comparação dos modelos |
| 4 | `notebooks/04_previsao_2026_final.ipynb` | Previsão final para a Copa 2026 |

Os notebooks experimentais (versões v1 a v5) estão em `notebooks/experimentos/` para referência.

---

## Estrutura do Repositório

```
ml-worldcup-goals-prediction/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/                        ← datasets originais (não versionados)
│   └── processed/                  ← features e previsões geradas
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_features_v6.ipynb
│   ├── 03_modelos_v6.ipynb
│   ├── 04_previsao_2026_final.ipynb
│   └── experimentos/               ← versões anteriores (v1–v5)
├── src/
│   └── features/
│       └── elo.py                  ← cálculo de ELO histórico
├── experiments/
│   └── experimentos.md             ← rastreio de todos os experimentos
├── article/
│   ├── artigo.md
│   ├── figures/
│   └── tables/
└── docs/
    ├── decisoes-tecnicas.md
    └── dicionario-de-dados.md
```

---

## Modelo Final

**Algoritmo:** Regressão Linear
**Versão de features:** v6 (11 features)
**Amostras de treino:** 248 (Copas 1994–2022)

### Features utilizadas

| Feature | Descrição |
|---------|-----------|
| `media_gols_marcados_ciclo` | Média de gols marcados no ciclo completo |
| `media_gols_sofridos_ciclo` | Média de gols sofridos no ciclo completo |
| `pct_vitorias_ciclo` | % de vitórias no ciclo |
| `total_jogos_ciclo` | Total de jogos no ciclo |
| `media_gols_marcados_ult15` | Média de gols nos últimos 15 jogos |
| `media_gols_sofridos_ult15` | Média de gols sofridos nos últimos 15 jogos |
| `pct_vitorias_ult15` | % de vitórias nos últimos 15 jogos |
| `elo_medio_adv_ciclo` | ELO médio dos adversários no ciclo |
| `elo_medio_adv_ult15` | ELO médio dos adversários nos últimos 15 jogos |
| `media_gols_ultimas2_copas` | Média de gols nas 2 Copas anteriores |
| `fase_ultima_copa` | Fase atingida na Copa imediatamente anterior |

### Por que Regressão Linear?

Com 216 amostras de treino, modelos complexos (Random Forest, XGBoost) sofreram overfitting e aprenderam correlações espúrias. A Regressão Linear generalizou melhor — resultado consistente com o princípio da parcimônia.

---

## Resultados

| Modelo | MAE Teste (Copa 2022) | MAE CV (walk-forward) |
|--------|----------------------|----------------------|
| Regressão Linear v6 | **0.446** | 0.444 |
| Random Forest v6 | 0.468 | 0.445 |
| XGBoost v6 | 0.530 | 0.504 |

**Validação externa:** correlação de **0.68** entre as previsões e o valor de mercado dos elencos (Transfermarkt) — dado que o modelo nunca viu durante o treino.

---

## Previsão Copa 2026 — Top 10

| Posição | Seleção | Previsão (gols/jogo) |
|---------|---------|----------------------|
| 1 | Espanha | 2.17 |
| 2 | Argentina | 2.01 |
| 3 | Netherlands | 1.93 |
| 4 | Colombia | 1.92 |
| 5 | Portugal | 1.92 |
| 6 | Belgium | 1.86 |
| 7 | England | 1.84 |
| 8 | France | 1.80 |
| 9 | Norway | 1.71 |
| 10 | Brazil | 1.71 |

---

## Limitações

- Jogos com menos de 10 partidas no ciclo são descartados (dados insuficientes)
- Mudanças de treinador e lesões não são capturadas
- O ciclo 2026 disponível vai até março/2026 — jogos finais podem estar ausentes
- New Zealand beneficiada pelo ciclo OFC com adversários fracos (documentado)
- Erro esperado: ~0.45 gols por jogo por seleção

---

## Autores

> Preencha com seu nome e matrícula.
