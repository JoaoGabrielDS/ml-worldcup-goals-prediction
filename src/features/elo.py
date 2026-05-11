"""
Cálculo de ELO Rating histórico para todas as seleções.

O ELO é um sistema de pontuação dinâmico que reflete a força relativa
de cada seleção no momento de cada partida. É atualizado após cada jogo
com base no resultado e na força do adversário.

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
    k_competitivo : fator K para jogos competitivos (mais peso)
    k_amistoso : fator K para amistosos (menos peso)

    Retorna:
    --------
    DataFrame original com colunas extras:
        elo_home_antes, elo_away_antes (ELO antes do jogo)
        elo_home_depois, elo_away_depois (ELO após o jogo)
    """
    df = df.sort_values('date').reset_index(drop=True)

    elo = {}  # dicionário: seleção → ELO atual

    registros = []

    for _, row in df.iterrows():
        home = row['home_team']
        away = row['away_team']

        # ELO atual (ou inicial se seleção nunca jogou)
        elo_h = elo.get(home, elo_inicial)
        elo_a = elo.get(away, elo_inicial)

        # Probabilidade esperada de vitória do mandante
        prob_home = 1 / (1 + 10 ** ((elo_a - elo_h) / 400))

        # Resultado real (do ponto de vista do mandante)
        if row['home_score'] > row['away_score']:
            resultado = 1.0   # vitória
        elif row['home_score'] == row['away_score']:
            resultado = 0.5   # empate
        else:
            resultado = 0.0   # derrota

        # Fator K — jogos competitivos têm mais peso
        k = k_amistoso if row['tournament'] == 'Friendly' else k_competitivo

        # Atualização do ELO
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


if __name__ == '__main__':
    df = pd.read_csv('data/raw/results.csv', parse_dates=['date'])
    df_com_elo = calcular_elo_historico(df)
    df_com_elo.to_csv('data/processed/results_com_elo.csv', index=False)
    print(f'ELO calculado para {df_com_elo.shape[0]} jogos.')
    print(df_com_elo[['date', 'home_team', 'away_team',
                       'elo_home_antes', 'elo_away_antes']].tail(10))
