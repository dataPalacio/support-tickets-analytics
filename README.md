# 📊 Projeto Análise de Tickets de Suporte Técnico

Este projeto foi criado para resolver um problema comum enfrentado pelo órgão público: **a dificuldade em extrair informações relevantes e confiáveis a partir dos dados brutos dos tickets de suporte técnico**. Muitas vezes, esses dados vêm em formatos variados, com inconsistências e informações incompletas, o que dificulta análises precisas.

O objetivo principal aqui é implementar um pipeline que faça a limpeza, organização e enriquecimento desses dados, transformando-os em um formato estruturado e de fácil consulta. Isso permite que gestores e analistas possam obter insights valiosos para melhorar a eficiência do suporte, identificar gargalos e priorizar ações corretivas.

---

## 📦 Como clonar o projeto

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

> Copie o link do projeto: https://github.com/dataPalacio/support-tickets-analytics.git

---

## 🧱 Estrutura do Projeto

```
📁 support-tickets-analytics/
├── 📂 data/            # Dados brutos e processados (CSV, Excel, etc.)
│   ├── 📂 raw/         # Dados brutos originais
│   └── 📂 processed/   # Dados processados
├── 📂 scripts/         # Scripts Python (ETL, processamento, etc.)
├── 📂 notebooks/       # Notebooks exploratórios (.ipynb)
├── 📂 dashboards/      # Dashboards Power BI (.pbix) e mockups
├── 📂 reports/         # Relatórios finais e figuras geradas
├── 📂 docs/            # Documentação adicional (PDFs, imagens, manuais)
├── requirements.txt    # Dependências do projeto
├── README.md           # Descrição geral do projeto
└── .gitignore
```

- **`data/`**: arquivos brutos, tratados e externos.
- **`scripts/`**: scripts de processamento, como `main.py`.
- **`notebooks/`**: notebooks exploratórios e análises estatísticas.
- **`dashboards/`**: arquivos .pbix do Power BI e mockups.
- **`reports/`**: relatórios finais e figuras geradas.
- **`docs/`**: documentação complementar, imagens ou relatórios.

---

## 🚀 O que esse código faz?

1. **Carrega os dados** de um arquivo `.csv` ou `.xlsx`.
2. **Padroniza os nomes das colunas** (tira acento, deixa tudo minúsculo).
3. **Limpa os campos** (remove espaços, formata datas, etc).
4. **Atribui responsáveis** com base na localização.
5. **Filtra só o que importa** (colunas relevantes).
6. **Extrai o nome do equipamento** do título da solicitação.
7. **(Opcional)** Salva o resultado em um novo `.csv`.

---

## 🛠️ Como executar


```python
from scripts.main import exec_pipeline

df_final = exec_pipeline("data/arquivo.csv", save_csv="output/saida.csv")
```

Se quiser só ver o resultado sem salvar, é só não passar o `save_csv`.

---

## 🚀 O que o pipeline entrega?

- Carrega e padroniza dados de arquivos `.csv` ou `.xlsx`.
- Limpa campos, formata datas e padroniza nomes de colunas.
- Atribui responsáveis automaticamente com base na localização.
- Filtra apenas as colunas relevantes e extrai o nome do equipamento do título.
- Gera um DataFrame limpo, padronizado e enriquecido, pronto para análise, visualizações, dashboards ou relatórios.
- (Opcional) Salva o resultado em um novo `.csv`.

---


## 📁 Exemplo de colunas esperadas

- `ID`
- `Título`
- `Data de abertura`
- `Requerente - Requerente`
- `Localização`
- `Equipamento Quantidade`
- `Atribuído - Grupo técnico`
- `Status`
- `Data de fechamento`
- `Contato`
- `Feedback`

---


## ✅ Exemplo de resultado

O pipeline gera um DataFrame com as seguintes colunas padronizadas:

- `id`, `titulo`, `data_abertura`, `requerente`, `localizacao`, `g_responsavel`, `status`, `data_fechamento`, `contato`, `feedback`, `equipamento_qtd`, `responsavel`, `equipamento`

**Observações:**
- A coluna `responsavel` é criada automaticamente pelo pipeline, com base na localização (`localizacao`).
- A coluna `equipamento` é extraída do campo `titulo` quando o padrão "Solicitação de equipamento - ..." é encontrado.
- `g_responsavel` corresponde ao grupo técnico original do chamado.
- Colunas não listadas acima são descartadas durante o processamento.

### Exemplo de entrada e saída

**Linha de entrada (CSV):**

```
ID;Título;Equipamento Quantidade;Data de abertura;Requerente - Requerente;Localização;Atribuído - Grupo técnico;Status;Data de fechamento;Contato;Feedback
30128;Solicitação de equipamento - Computador;3;01/07/2025;user_006;LOC_001; Suporte N2;Estoque;22/07/2025;Sistema;
```

**Linha processada (DataFrame):**

| id    | titulo                           | data_abertura | requerente | localizacao | g_responsavel | status  | data_fechamento | contato | feedback | equipamento_qtd | responsavel | equipamento |
|-------|-----------------------------------|---------------|------------|-------------|---------------|---------|-----------------|---------|----------|-----------------|-------------|-------------|
|30128  |Solicitação de equipamento - Computador|2025-07-01    |USER_006    |LOC_001      |Suporte N2     |Estoque  |2025-07-22       |Sistema  |          |3                |Informática  |Computador   |

**Atenção:**
- O pipeline espera que os nomes das colunas no CSV de entrada estejam exatamente como listados em "Exemplo de colunas esperadas" (com acentos e maiúsculas/minúsculas corretos). Internamente, todos os nomes são padronizados para minúsculo e sem acento.

---

## 🔍 O que podemos retirar desse projeto?

- Um **DataFrame limpo e padronizado**, pronto para análise.
- Informações enriquecidas com **responsáveis atribuídos automaticamente**.
- Extração de **nomes de equipamentos** a partir de descrições.
- Dados prontos para **visualizações, dashboards ou relatórios**.

---

## ❓ Quais perguntas de negócio podemos resolver?

- Quais são os **equipamentos mais solicitados**?
- Quais **localizações** geram mais demandas?
- Quem são os **responsáveis mais acionados**?
- Existe sazonalidade nas **datas de abertura** dos chamados?
- Quais **requerentes** mais solicitam equipamentos?
- Há locais com **sobrecarga de solicitações**?

---

## 🛠 Tecnologias Utilizadas
- **Python** (Bibliotecas: pandas, os, re, numpy, unicodedata)
- **VS Code + Data_Wrangler** para análises e visualizações interativas
- **GitHub** para versionamento e compartilhamento do projeto


---

## 🔮 Análises Possíveis a Serem Acrescentadas

- 📊 **Gráficos de tendência** por mês ou trimestre.
- 🗺️ **Mapeamento geográfico** das localizações (se houver coordenadas).
- 📈 **Dashboards interativos** com ferramentas como Power BI ou Plotly.
- ⏱️ **Tempo médio de atendimento** (se houver data de fechamento).
- 🧠 **Classificação automática** de solicitações por tipo.
- 📌 **Clusterização** de localizações com padrões semelhantes.

---
## 📄 Licença

Todos os projetos neste repositório estão sob a Licença MIT.

## Considerações Finais

Desenvolvido com ❤️ por [Gustavo Palacio](https://www.linkedin.com/in/gfpalacio/).

Feito pra facilitar a vida de quem analisa dados de chamados e quer tudo pronto pra usar. Qualquer dúvida ou melhoria, só chamar! 😄

📌 **Autor:** *Gustavo Palacio*  
📅 **Data:** *Julho de 2025*
