# Projeto OCR com Amazon Textract: Extração Inteligente de Documentos

Este repositório reúne implementações práticas, aprendizados e insights sobre a utilização do serviço **Amazon Textract** da AWS, explorando desde a detecção simples de texto até a extração estruturada de pares chave-valor (Key-Value) e formulários em documentos oficiais como CNH e listas.

---

## 📌 O que é o Amazon Textract?

O **Amazon Textract** é um serviço gerenciado de Machine Learning da AWS que vai além do OCR tradicional (Reconhecimento Óptico de Caracteres). Ele compreende a estrutura visual de documentos, permitindo extrair:
- **Texto linear e blocos de texto**: Linhas e palavras individuais.
- **Formulários e Pares Chave-Valor**: Relações entre rótulo e conteúdo (ex.: `Nome: João`, `CPF: 123.456.789-00`).
- **Tabelas**: Linhas, colunas e células estruturadas preservando o formato tabular.
- **Consultas (Queries)**: Extração baseada em perguntas em linguagem natural (ex.: *"Qual o número de registro da CNH?"*).

---

## 💡 Principais Insights e Aprendizados

### 1. `detect_document_text` vs `analyze_document`
- **`detect_document_text`**:
  - Voltado para leitura sequencial rápida de linhas e palavras (`LINE`, `WORD`).
  - Ideal para notas, recibos manuscritos ou listas simples (como visto em `Lista.py`).
  - Menor latência e menor custo de processamento.
- **`analyze_document`**:
  - Opera com análise semântica e suporte a `FeatureTypes=["FORMS", "TABLES", "QUERIES"]`.
  - Constrói o grafo de relacionamentos entre blocos (`Relationships`), permitindo associar uma `KEY` ao seu respectivo `VALUE`.
  - Essencial para documentos cadastrais e cartões de identidade (como a CNH em `main.py`).

### 2. Entendendo a Estrutura de Blocos (`Blocks`)
A resposta do Textract é composta por uma lista de `Blocks`, onde cada bloco possui um identificador único (`Id`) e relações com outros blocos:
- **`KEY_VALUE_SET`**: Representa um campo de formulário, podendo ser do tipo `KEY` ou `VALUE`.
- **`CHILD` relationships**: Apontam para os blocos filhos (`WORD` ou `SELECTION_ELEMENT`) que formam o texto legível.
- **`VALUE` relationships**: Ligam o bloco de chave diretamente ao bloco que contém o valor correspondente.

### 3. Gerenciamento de Cache Local (`response.json`)
- Para evitar chamadas repetitivas e custos adicionais com a API da AWS durante o desenvolvimento de scripts de extração/parsers, adotar um padrão de cache local (`response.json`) é uma prática essencial.
- Permite focar e depurar as funções de tratamento de dados (`get_kv_map`, `get_kv_relationship`) sem depender de conexão de rede constante.

### 4. Gestão de Contas AWS e Ativação de Serviços
- Serviços cognitivos como Textract podem exigir etapas de verificação antifraude e validação de pagamento na conta AWS (`SubscriptionRequiredException`), sendo importante testar a conectividade antecipadamente na região correta (como `us-east-1`).
- As permissões no IAM necessitam de políticas adequadas, como `AmazonTextractFullAccess` ou políticas com privilégios mínimos customizadas (`textract:DetectDocumentText`, `textract:AnalyzeDocument`).

---

## 🚀 Possibilidades e Casos de Uso Reais

| Cenário | Descrição | Recurso Textract Recomendado |
| :--- | :--- | :--- |
| **Onboarding Digital e KYC (Know Your Customer)** | Leitura de CNHs, RGs e comprovantes de endereço para validação cadastral automática em fintechs e bancos. | `AnalyzeDocument` (Forms & Queries) |
| **Automação Financeira e Fiscal** | Extração de notas fiscais, faturas e boletos bancários com identificação de itens, taxas e totais. | `AnalyzeExpense` / `TABLES` |
| **Digitalização de Arquivos Históricos** | Conversão de documentos digitalizados em base de texto pesquisável com preservação de estrutura de parágrafos. | `DetectDocumentText` |
| **Processamento de Contratos** | Extração de cláusulas, datas de vigência e partes envolvidas sem necessidade de templates fixos de OCR. | `AnalyzeDocument` (Queries) |

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12+**
- **AWS SDK para Python (`boto3`)**
- **Amazon Textract API**
- **JSON** para persistência e modelagem dos dados extraídos

