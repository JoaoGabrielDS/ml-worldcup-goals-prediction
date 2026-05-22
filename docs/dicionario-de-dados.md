# Dicionário de Dados

## Arquivo: results.csv (raw)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `date` | date | Data da partida |
| `home_team` | string | Seleção mandante |
| `away_team` | string | Seleção visitante |
| `home_score` | float | Gols marcados pelo mandante |
| `away_score` | float | Gols marcados pelo visitante |
| `tournament` | string | Nome do torneio |
| `city` | string | Cidade onde foi disputada |
| `country` | string | País sede |
| `neutral` | bool | Se o jogo foi em campo neutro |

---

## Arquivo: shootouts.csv (raw)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `date` | date | Data da partida |
| `home_team` | string | Seleção mandante |
| `away_team` | string | Seleção visitante |
| `winner` | string | Seleção vencedora nos pênaltis |
| `first_shooter` | string | Seleção que cobrou primeiro |

Utilizado para determinar o vencedor real em jogos empatados no tempo normal — corrige o cálculo de `fase_ultima_copa` para Argentina (campeã 2022 via pênaltis) e Japan (oitavas 2022 via pênaltis).

---

## Arquivo: football_team_values_2010_2026.xlsx (raw)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `copa` | int | Ano da Copa do Mundo |
| `selecao` | string | Nome da seleção (padrão Transfermarkt) |
| `valor_mercado` | float | Valor de mercado total do elenco (€ milhões) |

Fonte: Transfermarkt. Disponível para as Copas de 2014, 2018, 2022 e previsão 2026. Utilizado como dado contextual na tabela final de previsões — não entra no modelo de treino.

---

## Arquivo: results_com_elo.csv (processed)

Dataset original `results.csv` com 4 colunas adicionais de ELO calculadas pelo script `src/features/elo.py`.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| *(todas as colunas de results.csv)* | — | — |
| `elo_home_antes` | float | ELO do mandante antes do jogo |
| `elo_away_antes` | float | ELO do visitante antes do jogo |
| `elo_home_depois` | float | ELO do mandante após o jogo |
| `elo_away_depois` | float | ELO do visitante após o jogo |

**Parâmetros do ELO:**
- ELO inicial: 1000 (seleções sem histórico)
- Fator K competitivo: 40
- Fator K amistoso: 20

---

## Arquivo: features_completo_v6.csv (processed)

Dataset principal de treino — uma linha por seleção × Copa.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `selecao` | string | Nome da seleção |
| `copa_alvo` | int | Ano da Copa que se quer prever |
| `media_gols_marcados_ciclo` | float | Média de gols marcados por jogo no ciclo completo |
| `media_gols_sofridos_ciclo` | float | Média de gols sofridos por jogo no ciclo completo |
| `pct_vitorias_ciclo` | float | Percentual de vitórias no ciclo (0 a 1) |
| `total_jogos_ciclo` | int | Total de jogos disputados no ciclo |
| `media_gols_marcados_ult15` | float | Média de gols marcados nos últimos 15 jogos do ciclo |
| `media_gols_sofridos_ult15` | float | Média de gols sofridos nos últimos 15 jogos do ciclo |
| `pct_vitorias_ult15` | float | Percentual de vitórias nos últimos 15 jogos (0 a 1) |
| `elo_medio_adv_ciclo` | float | ELO médio dos adversários enfrentados no ciclo |
| `elo_medio_adv_ult15` | float | ELO médio dos adversários nos últimos 15 jogos |
| `media_gols_ultimas2_copas` | float | Média de gols marcados nas 2 Copas anteriores (0 se não participou) |
| `fase_ultima_copa` | int | Fase atingida na Copa anterior (ver codificação abaixo) |
| `media_gols_copa` | float | **TARGET** — média de gols marcados na Copa alvo |

**Codificação de `fase_ultima_copa`:**

| Valor | Significado |
|-------|-------------|
| 0 | Não se classificou para a Copa anterior |
| 1 | Eliminado na fase de grupos |
| 2 | Eliminado nas oitavas de final |
| 3 | Eliminado nas quartas de final |
| 4 | Eliminado na semifinal (inclui 3º lugar) |
| 5 | Vice-campeão (finalista derrotado) |
| 6 | Campeão |

---

## Arquivo: previsao_2026_final.csv (processed)

Previsões finais para a Copa 2026 com todas as seleções classificadas.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `selecao` | string | Nome da seleção |
| `confederacao` | string | Confederação (CONMEBOL, UEFA, CAF, AFC, CONCACAF, OFC) |
| `total_jogos_ciclo` | int | Total de jogos no ciclo 2026 |
| `media_gols_marcados_ciclo` | float | Média de gols marcados no ciclo 2026 |
| `media_gols_marcados_ult15` | float | Média de gols marcados nos últimos 15 jogos do ciclo |
| `elo_medio_adv_ciclo` | float | ELO médio dos adversários no ciclo 2026 |
| `fase_ultima_copa` | int | Fase atingida na Copa 2022 |
| `media_gols_ultimas2_copas` | float | Média de gols nas Copas 2018 e 2022 |
| `valor_mercado_milhoes` | float | Valor de mercado do elenco em € milhões (Transfermarkt, 2026) |
| `previsao` | float | Média de gols prevista por jogo na Copa 2026 |

---

## Regras de Construção das Features

- **Ciclo:** jogos entre o fim da Copa anterior e o início da Copa alvo, excluindo jogos de Copa do Mundo
- **Últimos 15 jogos:** os 15 jogos mais recentes dentro do ciclo (`.tail(15)` após ordenação por data)
- **ELO:** calculado para todos os jogos desde 1872 — quanto mais histórico processado, mais preciso o ELO no período de interesse
- **Fase da Copa anterior:** calculada via `shootouts.csv` para jogos decididos nos pênaltis; jogo do 3º lugar classificado como fase 4 (semifinal), não como final
- **Filtro mínimo:** seleções com menos de 10 jogos no ciclo são excluídas da previsão 2026
