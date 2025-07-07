from scripts.main import exec_pipeline

caminho_arquivo = r'data\raw\2025-07-01_raw.csv'  # Ajuste o caminho se necessário
nome_arquivo_saida = r'data\processed\2025-07-01_processed.csv'  # Ajuste o caminho se necessário

exec_pipeline(caminho_arquivo, nome_arquivo_saida)