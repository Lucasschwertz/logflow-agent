# Exemplos de uso

## Log com erro

Comando:

```powershell
python -m src.main ".\examples\sample_pipeline_error.log"
```

Entrada resumida:

```text
WARNING Deprecated dependency detected: old-package==1.2.0
ERROR Migration failed: relation users already exists
ERROR Pipeline failed with exit code 1
```

Saída esperada em alto nível:

- JSON final com `status` igual a `finished`.
- `severity` igual a `alta`, porque há dois erros.
- Relatório gravado em `outputs/logflow-report.md`.
- Recomendação para revisar migração e idempotência.

## Log de sucesso

Crie um arquivo local de exemplo, como `examples/local_success.log`, com o
conteúdo abaixo:

```text
2026-07-08T20:10:01Z INFO Starting pipeline job deploy-production
2026-07-08T20:10:04Z INFO Running tests
2026-07-08T20:10:10Z INFO Pipeline finished successfully
```

Comando:

```powershell
python -m src.main ".\examples\local_success.log"
```

Saída esperada em alto nível:

- JSON final com `status` igual a `finished`.
- `severity` igual a `informativa`.
- Relatório sem erros ou avisos relevantes.
- Recomendação indicando que nenhuma ação corretiva é necessária no momento.

## Arquivo inexistente

Comando:

```powershell
python -m src.main ".\examples\arquivo_inexistente.log"
```

Saída esperada em alto nível:

- JSON com `status` igual a `validation_failed`.
- `validation_errors` contendo a mensagem `Arquivo não encontrado`.
- Nenhuma análise de severidade.
- Nenhum relatório novo de análise gerado para esse arquivo.

## Relatório Markdown

Quando a execução é válida, o arquivo `outputs/logflow-report.md` contém:

- arquivo analisado;
- status final da execução;
- severidade;
- resumo;
- erros detectados;
- avisos detectados;
- recomendação;
- observação de segurança sobre mascaramento de dados sensíveis.
