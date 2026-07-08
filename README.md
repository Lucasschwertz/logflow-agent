# LogFlow Agent

LogFlow Agent é um mini-projeto em Python 3.12 com LangGraph para analisar logs
de execução de pipelines e gerar um relatório Markdown com severidade, resumo,
linhas relevantes e recomendação de ação.

## Problema

Logs de CI/CD e automações costumam misturar mensagens informativas, avisos,
erros e possíveis dados sensíveis. Isso dificulta uma primeira triagem rápida
quando uma execução falha ou termina com alertas.

## Objetivo do agente

O agente recebe um arquivo `.log` ou `.txt`, valida a entrada, lê o conteúdo,
mascara padrões simples de segredo, identifica linhas de erro e aviso, classifica
a severidade e grava um relatório em `outputs/logflow-report.md`.

## Tecnologias

- Python 3.12
- LangGraph
- pytest
- Ruff
- GitHub Actions para lint e testes

## Fluxo LangGraph

O grafo executa os seguintes nós:

1. `validate_input`: valida caminho, existência, extensão e tamanho do arquivo.
2. `read_log`: lê o arquivo e valida se o conteúdo não está vazio.
3. `prepare_context`: mascara valores sensíveis por padrões simples.
4. `analyze_log`: extrai erros, avisos, severidade, resumo e recomendação.
5. `generate_report`: grava o relatório Markdown.
6. `final_response`: finaliza a execução com status `finished`.

Quando a validação da entrada ou do conteúdo falha, o fluxo segue para
`error_response` e não gera relatório de análise.

## Ferramenta utilizada

A ferramenta integrada principal é a leitura e escrita de arquivos em
`src/tools/file_tools.py`. Ela lê o log informado e grava o relatório Markdown no
caminho de saída. A análise usa funções locais em `src/tools/log_tools.py`.

## Instalação

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Execução

```powershell
python -m src.main ".\examples\sample_pipeline_error.log"
```

Para escolher outro caminho de saída:

```powershell
python -m src.main ".\examples\sample_pipeline_error.log" --output ".\outputs\logflow-report.md"
```

## Exemplos de entrada e saída

Entrada com erro:

```text
2026-07-08T20:10:15Z ERROR Migration failed: relation users already exists
2026-07-08T20:10:15Z ERROR Pipeline failed with exit code 1
```

Saída JSON em alto nível:

```json
{
  "status": "finished",
  "severity": "alta",
  "report_path": "outputs/logflow-report.md",
  "validation_errors": []
}
```

Saída Markdown em alto nível:

```markdown
# Relatório LogFlow Agent

## Status

finished

## Severidade

alta
```

## Testes e lint

```powershell
pytest
ruff check .
```

O pipeline de CI executa os mesmos comandos em Python 3.12.

## Decisões tomadas

- Usar LangGraph para deixar o fluxo explícito e fácil de revisar.
- Manter a análise heurística e local, sem dependência de chamada externa.
- Aceitar apenas arquivos `.log` e `.txt`.
- Limitar arquivos de entrada a 512 KB.
- Gerar um relatório Markdown simples para facilitar leitura e versionamento
  seletivo, sem versionar saídas geradas.

## Limitações

- A classificação é baseada em palavras-chave, não em interpretação semântica
  profunda.
- A sanitização cobre apenas padrões simples como `token=`, `password=`,
  `api_key=` e `secret=`.
- O agente não corrige automaticamente o pipeline; ele recomenda próximos passos.
- Logs muito grandes não são aceitos pelo validador atual.

## Cuidados de segurança

- Não informe arquivos com segredos reais quando não for necessário.
- O relatório mascara apenas padrões simples; revise manualmente antes de
  compartilhar saídas.
- Não versione arquivos gerados em `outputs/`, exceto `outputs/.gitkeep`.
- Use variáveis de ambiente para credenciais em projetos reais.
