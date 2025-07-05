import pandas as pd
import os
import re
import unicodedata

# === Carregamento de Arquivo ===
def import_data(caminho, tipo_arquivo='csv', encoding='utf-8', sep=',', debug=False):
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
        return df.drop(columns=colunas_excluir)
    except KeyError as e:
        print(f"Erro: Algumas colunas não foram encontradas - {e}")
        return df.copy()

# === Padronização de Nomes de Colunas ===
def padronizar_col(df):
    mapa_nomes = {
        "ID": 'id',
        "Título": 'titulo',
        "Equipamento Quantidade": 'equipamento_qtd',
        "Data de abertura": 'data_abertura',
        "Requerente - Requerente": 'requerente',
        "Localização": 'localizacao',
        "Descrição": 'descricao',
        "Atribuído - Responsável": 'p_responsavel',
        "Atribuído - Grupo técnico": 'g_responsavel',
        "Status": 'status',
        "Data de fechamento": 'data_fechamento',
        "Contato": 'contato',
        "Feedback": 'feedback'
    }
    # Remove acentos e padroniza para minúsculo
    df = df.rename(columns=mapa_nomes)
    df.columns = [unicodedata.normalize('NFKD', c).encode('ASCII', 'ignore').decode('utf-8').lower() for c in df.columns]
    return df

# === Limpeza de Campos ===
def dclean(df):
    if 'requerente' in df:
        df['requerente'] = df['requerente'].astype(str).str.strip().str.upper()
    if 'localizacao' in df:
        df['localizacao'] = df['localizacao'].astype(str).str.strip()
    if 'g_responsavel' in df:
        df['g_responsavel'] = df['g_responsavel'].astype(str).str.strip()
    if 'descricao' in df:
        df['descricao'] = (df['descricao'].astype(str)
                           .str.replace(r'DADOS DO FORMULÁRIO|Informações Obrigatórias', '', regex=True)
                           .str.replace(r'\n+', ' ', regex=True)
                           .str.strip())
    if 'data_abertura' in df:
        df['data_abertura'] = (
            df['data_abertura']
            .astype(str)
            .str.strip()
            .replace('', pd.NA)
        )
        # Converte datas válidas, datas inválidas ficam em branco (NaT)
        df['data_abertura'] = pd.to_datetime(df['data_abertura'], errors='coerce').dt.date
    if 'data_fechamento' in df:
        df['data_fechamento'] = (
            df['data_fechamento']
            .astype(str)
            .str.strip()
            .replace('', pd.NA)
        )
        df['data_fechamento'] = pd.to_datetime(df['data_fechamento'], errors='coerce').dt.date
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

def atribuir_responsavel_por_localizacao(df, coluna_localizacao='Localização', nome_nova_coluna='responsavel'):
    """
    Atribui o responsável a cada linha do DataFrame com base na localização.
    Padroniza os nomes das colunas para minúsculo e sem acento.
    """
    coluna_localizacao = unicodedata.normalize('NFKD', coluna_localizacao).encode('ASCII', 'ignore').decode('utf-8').lower()
    nome_nova_coluna = unicodedata.normalize('NFKD', nome_nova_coluna).encode('ASCII', 'ignore').decode('utf-8').lower()
    if coluna_localizacao not in df.columns:
        raise ValueError(f'Coluna "{coluna_localizacao}" não encontrada no DataFrame.')
    df[nome_nova_coluna] = df[coluna_localizacao].map(LOCALIZACAO_RESPONSAVEIS)
    df[nome_nova_coluna] = df[nome_nova_coluna].fillna("Nao definido")
    # Adiciona aviso se houver "Nao definido"
    if (df[nome_nova_coluna] == "Nao definido").any():
        print("Aviso: Existem localizações sem responsável definido no dicionário. Verifique a coluna 'responsavel'.")
    return df

# === Extração da Quantidade de Monitores Solicitados ===
def extrair_nome(titulo):
    """
    Extrai o nome do equipamento do título, se seguir o padrão esperado.
    """
    if not isinstance(titulo, str):
        return None
    match = re.search(r"Solicitação de equipamento - (.+)", titulo)
    return match.group(1).strip() if match else None

# === Pipeline ===
def exec_pipeline(caminho_arquivo, save_csv=None):
    """
    Executa o pipeline principal de processamento dos dados:
    1. Importa o arquivo
    2. Padroniza nomes de colunas
    3. Limpa campos
    4. Atribui responsável por localização
    5. Mantém apenas colunas relevantes
    6. Extrai nome do equipamento
    7. Salva CSV, se solicitado
    """
    df = import_data(caminho_arquivo, sep=';')
    if df is None:
        return None

    df = padronizar_col(df)
    df = dclean(df)

    # Atribuição do responsável deve ocorrer após padronização e limpeza
    df = atribuir_responsavel_por_localizacao(
        df,
        coluna_localizacao='localizacao',
        nome_nova_coluna='responsavel'
    )

    colunas_para_manter = [
        'id',
    'titulo',
    'equipamento_qtd',
    'data_abertura',
    'requerente',
    'localizacao',
    'g_responsavel',
    'status',
    'data_fechamento',
    'contato',
    'feedback'
    ]
    df = excluir_colunas_exceto(df, colunas_para_manter)

    if 'titulo' in df.columns:
        df['equipamento'] = df['titulo'].apply(extrair_nome)

    if save_csv:
        df.to_csv(save_csv, index=False, sep=';')
        print(f"Arquivo salvo em: {save_csv}")

    return df


