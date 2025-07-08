# === Estatísticas do DataFrame ===
def rows_cols(df):
    if df is not None:
        print('----- Estatisticas Descritivas -----')
        print("Linhas:", df.shape[0])
        print("Colunas:", df.shape[1])

# === Análise Exploratória ===
def explorar_df(df):
    if df is not None:
        print('--- Visão Geral ---')
        print('Número de linhas:', df.shape[0])
        print('Número de colunas:', df.shape[1])
        print('\n--- Tipos de Dados ---')
        print(df.dtypes)
        print('\n--- Valores Ausentes por Coluna ---')
        print(df.isnull().sum())

