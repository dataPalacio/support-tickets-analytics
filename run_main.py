from scripts.main import exec_pipeline

caminho_arquivo = r'C:\git-clones\support-tickets-analytics\data\raw\2025-07-01_raw.csv'  # Ajuste o caminho se necessário
nome_arquivo_saida = r'C:\git-clones\support-tickets-analytics\data\processed\all_gau_processed.csv'  # Ajuste o caminho se necessário

exec_pipeline(caminho_arquivo, nome_arquivo_saida)