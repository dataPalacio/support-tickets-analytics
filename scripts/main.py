import pandas as pd
import os
import re
import unicodedata

# === Carregamento de Arquivo ===
def import_data(caminho, tipo_arquivo='csv', encoding='utf-8', sep=';', debug=False):
    if not os.path.isfile(caminho):
        print(f"Erro: Arquivo não encontrado: {caminho}")
        return None

    try:
        if tipo_arquivo == 'csv':
            df = pd.read_csv(caminho, sep=sep, encoding=encoding)
        elif tipo_arquivo == 'excel':
            df = pd.read_excel(caminho)
        else:
            print(f"Tipo de arquivo não suportado: {tipo_arquivo}")
            return None

        if debug:
            print(f"Arquivo {caminho} carregado com sucesso!")
            print(f"Forma dos dados: {df.shape}")
            print(f"Colunas: {df.columns.tolist()}")
        return df

    except Exception as e:
        print(f"Erro ao carregar arquivo {caminho}: {e}")
        return None

# === Exclusão de Colunas ===
def excluir_colunas_exceto(df, colunas_manter, inplace=False):
    colunas_excluir = [col for col in df.columns if col not in colunas_manter]
    try:
        return df.drop(columns=colunas_excluir, inplace=inplace)
    except KeyError as e:
        print(f"Erro: Algumas colunas não foram encontradas - {e}")
        return df.copy() if not inplace else None

# === Padronização de Nomes de Colunas ===
def padronizar_col(df):
    mapa_nomes = {
        'ID': 'id',
        'Título': 'titulo',
        'Equipamento Quantidade': 'equipamento_qtd',
        'Data de abertura': 'data_abertura',
        'Requerente - Requerente': 'requerente',
        'Localização': 'localizacao',
        'Atribuído - Grupo técnico': 'p_responsavel',
        'Responsável': 'responsavel'
    }
    return df.rename(columns=mapa_nomes)

# === Estatísticas do DataFrame ===
def rows_cols(df):
    if df is not None:
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

# === Limpeza de Campos ===
def dclean(df):
    if 'requerente' in df:
        df['requerente'] = df['requerente'].astype(str).str.strip().str.upper()
    if 'localizacao' in df:
        df['localizacao'] = df['localizacao'].astype(str).str.strip()
    if 'descricao' in df:
        df['descricao'] = (df['descricao'].astype(str)
                           .str.replace(r'DADOS DO FORMULÁRIO|Informações Obrigatórias', '', regex=True)
                           .str.replace(r'\n+', ' ', regex=True)
                           .str.strip())
    if 'data_abertura' in df:
        df['data_abertura'] = pd.to_datetime(df['data_abertura'], dayfirst=True, errors='coerce').dt.date
    return df

# === Atribuição de Responsável ===
# Definimos os responsáveis e as respectivas localizações em grupos
RESPONSAVEIS_POR_LOCALIZACAO = {
    'Informática': ['LOC_001', 'LOC_008', 'LOC_017', 'LOC_021', 'LOC_023'],
    'gestor_1': ['LOC_004', 'LOC_014', 'LOC_018', 'LOC_036', 'LOC_043'],
    'gestor_2': ['LOC_003', 'LOC_024', 'LOC_029', 'LOC_030', 'LOC_033', 'LOC_034'],
    'gestor_3': ['LOC_002', 'LOC_007', 'LOC_016', 'LOC_019', 'LOC_020', 'LOC_022', 
                 'LOC_035', 'LOC_040', 'LOC_041'],
    'gestor_4': ['LOC_005', 'LOC_009', 'LOC_012', 'LOC_015', 'LOC_026', 'LOC_028',
                 'LOC_032', 'LOC_037', 'LOC_038', 'LOC_039', 'LOC_042'],
    'gestor_5': ['LOC_006', 'LOC_010', 'LOC_011', 'LOC_013', 'LOC_025', 'LOC_027',
                 'LOC_031']
}

# Criamos o dicionário de localização para responsável a partir da estrutura acima
LOCALIZACAO_RESPONSAVEIS = {
    loc: resp
    for resp, locais in RESPONSAVEIS_POR_LOCALIZACAO.items()
    for loc in locais
}

def atribuir_responsavel_por_localizacao(df, coluna_localizacao='Localização', nome_nova_coluna='Responsável'):
  
    if coluna_localizacao not in df.columns:
        raise ValueError(f'Coluna "{coluna_localizacao}" não encontrada no DataFrame.')

    df[nome_nova_coluna] = df[coluna_localizacao].map(LOCALIZACAO_RESPONSAVEIS).fillna("Não definido")

    return df

# === Extração da Quantidade de Monitores Solicitados ===
def extrair_nome(titulo):
    match = re.search(r"Solicitação de equipamento - (.+)", titulo)
    return match.group(1).strip() if match else None

# === Pipeline ===
def exec_pipeline(caminho_arquivo, save_csv=None):
    df = import_data(caminho_arquivo) # importação do arquivo
    if df is None:
        return None
    df = dclean(df) # limpeza dos dados
    df = atribuir_responsavel_por_localizacao(df) # atribuição de responsável por localização
    df = padronizar_col(df) # padronização dos nomes das colunas
    colunas_para_manter = [
        'id', 'titulo', 'data_abertura', 'requerente', 
        'localizacao', 'responsável', 'p_responsavel', 'equipamento_qtd'] # colunas a serem mantidas
    df = excluir_colunas_exceto(df, colunas_para_manter) # exclusão de colunas desnecessárias

    if 'titulo' in df.columns:
        df['equipamento'] = df['titulo'].apply(extrair_nome) # extração do nome do equipamento

    if save_csv:
        df.to_csv(save_csv, index=False, sep=';') # salvamento do DataFrame em CSV
        print(f"Arquivo salvo em: {save_csv}") 

    return df
