# Padrao de commit e titulo de PR

Baseado em Conventional Commits. Idioma: o definido no contexto do projeto (padrao: portugues do Brasil).

## Formato

```
tipo(escopo): assunto

<corpo opcional: o porque, em ate 3 linhas>

Task: <ID>
```

- **tipo:** um da tabela abaixo.
- **escopo:** o modulo ou a area do dominio (`alertas`, `auth`, `sensores`). Use os termos do glossario. Omita se a mudanca for transversal.
- **assunto:** verbo no imperativo, minusculo, sem ponto final, ate ~60 caracteres. Diz o que muda no comportamento, nao em qual arquivo. Bom: `dispara alerta no valor igual ao limite`. Ruim: `ajusta alertas.js`.
- **corpo:** so quando o porque nao e obvio. Em commit de correcao de bug, escreva a causa confirmada.
- **rodape:** `Task: <ID>`. Mudanca que quebra compatibilidade: `BREAKING CHANGE: <o que quebra e como migrar>`. `Task: <ID>` fica no ultimo paragrafo, em linhas seguidas com os outros trailers (co-autoria, `BREAKING CHANGE`): o git so le como trailer o ultimo paragrafo (exemplo: o commit `fix` abaixo).

**Conferencia do rodape:** `git log --format='%h %(trailers:key=Task,valueonly)' <base>..HEAD` mostra o ID em todos os commits do intervalo. `grep` nao vale.

## Tipos

| Tipo | Quando |
|---|---|
| `feat` | comportamento novo para o usuario |
| `fix` | correcao de comportamento errado |
| `test` | so testes (ex.: teste de reproducao vermelho antes da correcao) |
| `refactor` | estrutura muda, comportamento nao |
| `perf` | melhora de desempenho medida |
| `docs` | documentacao, changelog |
| `chore` | manutencao sem efeito no comportamento (dependencia, configuracao) |
| `ci` | pipeline de CI |

## Commits por etapa (Build)

Cada etapa do Build gera um commit nesse formato. Exemplo de um fix:

```
test(alertas): reproduz alerta ausente no valor igual ao limite

Task: <ID>
```
```
fix(alertas): dispara alerta no valor igual ao limite

Causa: a comparacao usava ">" em vez de ">=".

Task: <ID>
Co-Authored-By: <nome> <email>
```

## Titulo do PR

O titulo do PR usa o mesmo formato (`tipo(escopo): assunto`) e descreve a task inteira. No merge com squash, ele vira o commit que entra na base.
