# Dicionário de Dados

## Arquivo: results.csv (raw)

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `date` | date | Data da partida |
| `home_team` | string | Seleção mandante |
| `away_team` | string | Seleção visitante |
| `home_score` | int | Gols marcados pelo mandante |
| `away_score` | int | Gols marcados pelo visitante |
| `tournament` | string | Nome do torneio |
| `city` | string | Cidade onde foi disputada |
| `country` | string | País sede |
| `neutral` | bool | Se o jogo foi em campo neutro |

---

## Arquivo: features_por_selecao.csv (processed)

Features calculadas por seleção para cada Copa alvo.

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `selecao` | string | Nome da seleção |
| `copa_alvo` | int | Ano da Copa que se quer prever |
| `media_gols_marcados_ciclo` | float | Média de gols marcados no ciclo (pós-copa anterior até início da copa alvo) |
| `media_gols_sofridos_ciclo` | float | Média de gols sofridos no ciclo |
| `pct_vitorias_ciclo` | float | Percentual de vitórias no ciclo |
| `total_jogos_ciclo` | int | Total de jogos no ciclo |
| `media_gols_marcados_ult15` | float | Média de gols marcados nos últimos 15 jogos do ciclo |
| `media_gols_sofridos_ult15` | float | Média de gols sofridos nos últimos 15 jogos do ciclo |
| `pct_vitorias_ult15` | float | Percentual de vitórias nos últimos 15 jogos |
| `media_gols_copa` | float | **TARGET** — média de gols marcados na Copa alvo |

---

## Regras de Construção das Features

- **Ciclo:** jogos disputados entre o fim da Copa anterior e o início da Copa alvo
- **Copas do Mundo são excluídas** das features — apenas o target usa esses jogos
- **Últimos 15 jogos:** os 15 jogos mais recentes dentro do ciclo
- Torneios considerados: Eliminatórias, Copa América, Eurocopa, Nations League, amistosos oficiais
