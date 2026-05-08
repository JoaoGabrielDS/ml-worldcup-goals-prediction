# Previsão de Média de Gols na FIFA World Cup

Projeto de Machine Learning — AV2  
Disciplina de Machine Learning | 2026

---

## Objetivo

Prever a **média de gols marcados** por cada seleção na Copa do Mundo da FIFA, com base em:
- Desempenho no **ciclo da Copa** (jogos entre a Copa anterior e a atual)
- **Forma recente** (últimos 15 jogos antes da Copa)

**Variável-alvo:** média de gols marcados por jogo na Copa do Mundo

---

## Dataset

- **Fonte:** [International football results from 1872 to 2026](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017)
- **Arquivos utilizados:** `results.csv`, `goalscorers.csv`
- **Período relevante:** 1990–2022 (Copas de 1994 a 2022)

### Como baixar o dataset

1. Acesse o link acima (necessário ter conta no Kaggle)
2. Clique em **Download** e extraia o ZIP
3. Coloque os arquivos CSV em `data/raw/`

---

## Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd projeto-ml-av2

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Inicie o Jupyter
jupyter notebook
```

---

## Execução

Execute os notebooks na seguinte ordem:

| Ordem | Notebook | Descrição |
|-------|----------|-----------|
| 1 | `notebooks/01_eda.ipynb` | Análise exploratória dos dados |
| 2 | `notebooks/02_features.ipynb` | Engenharia de features |
| 3 | `notebooks/03_modelos.ipynb` | Treino e avaliação dos modelos |
| 4 | `notebooks/04_previsao_2026.ipynb` | Previsão final para a Copa 2026 |

---

## Estrutura do Repositório

```
projeto-ml-av2/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/              ← dataset original (não versionado)
│   └── processed/        ← features e targets gerados
├── notebooks/            ← análise e modelagem
├── src/
│   ├── data/             ← limpeza e filtragem
│   ├── features/         ← cálculo de features
│   ├── models/           ← treino dos modelos
│   ├── evaluation/       ← métricas e comparação
│   └── visualization/    ← gráficos
├── experiments/          ← rastreio de hiperparâmetros e resultados
├── article/              ← artigo técnico-científico
└── docs/                 ← decisões técnicas e dicionário de dados
```

---

## Modelos Treinados

| Modelo | Tipo |
|--------|------|
| Regressão Linear | Baseline |
| Random Forest Regressor | Ensemble |
| XGBoost Regressor | Gradient Boosting |

**Métrica primária:** MAE (Mean Absolute Error) e RMSE

---

## Resultados

> A ser preenchido após a modelagem.

---

## Limitações

- Jogos amistosos e competitivos têm naturezas diferentes
- Seleções com poucos jogos no ciclo têm features menos confiáveis
- Mudanças de treinador/geração de jogadores não são capturadas diretamente

---

## Autores

> Preencha com seu nome e matrícula.
