# Slide 1 - LogFlow Agent

## Problema

Logs de pipeline acumulam mensagens de sucesso, avisos, erros e possíveis dados
sensíveis. A triagem manual é lenta e pode atrasar a identificação da causa mais
provável de uma falha.

## Proposta do agente

O LogFlow Agent analisa um arquivo `.log` ou `.txt`, identifica erros e avisos,
classifica a severidade e gera uma recomendação objetiva.

## Entrada e saída

- Entrada: caminho de um arquivo de log local.
- Saída no terminal: JSON com status, severidade, resumo e recomendação.
- Saída em arquivo: `outputs/logflow-report.md`.

---

# Slide 2 - Fluxo, segurança e validação

## Fluxo LangGraph

`validate_input` -> `read_log` -> `prepare_context` -> `analyze_log` ->
`generate_report` -> `final_response`

## Ferramenta integrada

Leitura do log e escrita do relatório Markdown com ferramentas locais em UTF-8.

## Segurança

- Aceita apenas `.log` e `.txt`.
- Limita tamanho de entrada.
- Mascara padrões simples de `token`, `password`, `api_key` e `secret`.

## Testes e documentação

- Testes com `pytest`.
- Lint com `ruff check .`.
- CI no GitHub Actions.
- Documentação em README, arquitetura, exemplos, prompts e slides.
