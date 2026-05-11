"""
Cálculo de ELO Rating histórico e Peso por Torneio.

Módulo responsável por:
1. Calcular o ELO histórico de cada seleção após cada partida
2. Calcular o peso de prestígio de cada torneio baseado no
   ELO médio histórico dos seus participantes

Referência: Hvattum & Arntzen (2010) — Using ELO ratings for match
result prediction in association football.
"""

import pandas as pd
import numpy as np


def calcular_elo_historico(df: pd.DataFrame,
                           elo_inicial: int = 1000,
                           k_competitivo: int = 40,
                           k_amistoso: int = 20) -> pd.DataFrame:
    """
    Calcula o ELO de cada seleção após cada partida.

    Parâmetros:
    -----------
    df : DataFrame com colunas date, home_team, away_team,
         home_score, away_score, tournament
    elo_inicial : ELO de partida para seleções sem histórico
    k_competitivo : fator K para jogos competitivos
    k_amistoso : fator K para amistosos

    Retorna:
    --------
    DataFrame original com colunas extras:
        elo_home_antes, elo_away_antes
        elo_home_depois, elo_away_depois
    """
    df = df.sort_values('date').reset_index(drop=True)
    elo = {}
    registros = []

    for _, row in df.iterrows():
        home = row['home_team']
        away = row['away_team']

        elo_h = elo.get(home, elo_inicial)
        elo_a = elo.get(away, elo_inicial)

        prob_home = 1 / (1 + 10 ** ((elo_a - elo_h) / 400))

        if row['home_score'] > row['away_score']:
            resultado = 1.0
        elif row['home_score'] == row['away_score']:
            resultado = 0.5
        else:
            resultado = 0.0

        k = k_amistoso if row['tournament'] == 'Friendly' else k_competitivo
        delta = k * (resultado - prob_home)

        novo_elo_h = elo_h + delta
        novo_elo_a = elo_a - delta

        registros.append({
            'elo_home_antes':  elo_h,
            'elo_away_antes':  elo_a,
            'elo_home_depois': novo_elo_h,
            'elo_away_depois': novo_elo_a,
        })

        elo[home] = novo_elo_h
        elo[away] = novo_elo_a

    df_elo = pd.DataFrame(registros)
    return pd.concat([df.reset_index(drop=True), df_elo], axis=1)


def calcular_peso_torneio(df_com_elo: pd.DataFrame,
                          peso_min: float = 0.5,
                          peso_max: float = 1.0) -> pd.Series:
    """
    Calcula o peso de prestígio de cada torneio baseado no
    ELO médio histórico dos seus participantes.

    Torneios com seleções mais fortes em média recebem peso maior.
    O peso é normalizado entre peso_min e peso_max.

    Parâmetros:
    -----------
    df_com_elo : DataFrame com colunas tournament, elo_home_antes, elo_away_antes
    peso_min : peso mínimo (torneios mais fracos)
    peso_max : peso máximo (torneios mais fortes)

    Retorna:
    --------
    Series com índice = nome do torneio, valor = peso normalizado
    """
    elo_home = df_com_elo[['tournament', 'elo_home_antes']].rename(
        columns={'elo_home_antes': 'elo'}
    )
    elo_away = df_com_elo[['tournament', 'elo_away_antes']].rename(
        columns={'elo_away_antes': 'elo'}
    )
    elo_todos = pd.concat([elo_home, elo_away])

    elo_medio = elo_todos.groupby('tournament')['elo'].mean()

    elo_min = elo_medio.min()
    elo_max = elo_medio.max()

    pesos = (elo_medio - elo_min) / (elo_max - elo_min) * (peso_max - peso_min) + peso_min

    return pesos


if __name__ == '__main__':
    df = pd.read_csv('data/raw/results.csv', parse_dates=['date'])
    df_com_elo = calcular_elo_historico(df)
    df_com_elo.to_csv('data/processed/results_com_elo.csv', index=False)

    pesos = calcular_peso_torneio(df_com_elo)
    pesos_df = pesos.reset_index()
    pesos_df.columns = ['tournament', 'peso']
    pesos_df = pesos_df.sort_values('peso', ascending=False)
    pesos_df.to_csv('data/processed/pesos_torneios.csv', index=False)

    print(f'ELO calculado para {df_com_elo.shape[0]} jogos.')
    print('\nTop 20 torneios por peso:')
    print(pesos_df.head(20).to_string(index=False))
