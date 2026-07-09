# Registro de prompts e uso de IA

Este documento registra como a IA foi usada no planejamento, implementação,
testes, CI e documentação do mini-projeto LogFlow Agent.

## Contexto principal

Prompt usado como direção do projeto:

```text
Criar um mini-projeto Python 3.12 com LangGraph que analise logs de pipeline,
identifique erros e avisos, classifique severidade e gere um relatório Markdown.
Manter o escopo simples, local, testável e sem dependências externas além das
necessárias ao grafo, testes e lint.
```

Saída esperada:

- estrutura de projeto Python;
- grafo LangGraph com nós pequenos;
- validação de entrada;
- ferramentas locais para arquivo e análise de log;
- testes automatizados;
- CI com lint e testes;
- documentação obrigatória.

## Planejamento

Prompt usado:

```text
Planeje um agente LangGraph para triagem de logs de CI/CD. O agente deve receber
um arquivo .log ou .txt, validar a entrada, mascarar dados sensíveis simples,
extrair erros e avisos, classificar severidade e gerar um relatório Markdown.
```

Refinamento aplicado:

- separar validação, leitura, preparação, análise e relatório em nós distintos;
- manter o estado compartilhado tipado com `TypedDict`;
- usar conexões condicionais apenas onde existem falhas de validação.

## Implementação

Prompt usado:

```text
Implemente o fluxo com LangGraph sem alterar o contrato público da CLI. Evite
chamadas externas e mantenha a análise determinística por palavras-chave.
```

Saída esperada:

- `src/agent/graph.py` com o grafo;
- `src/agent/nodes.py` com os nós;
- `src/tools/log_tools.py` com heurísticas de análise;
- `src/tools/file_tools.py` com leitura e escrita UTF-8;
- `src/security/validators.py` com validações simples.

## Testes

Prompt usado:

```text
Crie testes pequenos para validação de caminho, conteúdo vazio, mascaramento de
segredos, extração de erros e avisos, severidade e recomendações.
```

Refinamentos após erros:

- validar arquivo inexistente antes de extensão e tamanho;
- cobrir arquivos vazios;
- garantir que valores de `token`, `password` e `api_key` sejam mascarados;
- adicionar teste de consistência para o status exibido no relatório Markdown.

## CI

Prompt usado:

```text
Configure um workflow simples de GitHub Actions para Python 3.12 que instale
requirements.txt, execute ruff check . e pytest em push e pull request.
```

Saída esperada:

- workflow em `.github/workflows/ci.yml`;
- execução de lint antes dos testes;
- compatibilidade com branches `main`, `develop` e `feature/**`.

## Documentação

Prompt usado:

```text
Preencha a documentação do mini-projeto com README, arquitetura, exemplos,
prompts e slides curtos. Explique o problema, objetivo, fluxo LangGraph,
ferramentas, instalação, execução, testes, decisões, limitações e segurança.
```

Saída esperada:

- `README.md` permitindo instalação, execução e entendimento do projeto;
- `docs/architecture.md` com Mermaid e descrição dos nós;
- `docs/examples.md` com cenários de erro, sucesso e arquivo inexistente;
- `docs/prompts.md` com evidência de uso de IA;
- `slides/mini-projeto-logflow-agent.md` com até dois slides.

## Observação

Os prompts acima registram o uso de IA como apoio ao desenvolvimento. O agente
em tempo de execução não envia logs para serviços externos; ele usa regras locais
e determinísticas.
