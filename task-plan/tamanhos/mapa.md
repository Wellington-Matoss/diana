# Tamanho: mapa

Trabalho grande e nebuloso: o caminho ate o resultado ainda nao esta visivel. O mapa **planeja, nao executa**. Cada item do mapa e uma **decisao**, nao uma parte da implementacao. Quando o caminho fica claro, o mapa termina e vira um ou mais epicos.

## Nota de mapa

Crie uma nota com `tamanho: mapa` e estas secoes:

```markdown
## Destino
<como e o fim deste mapa: uma spec, uma decisao travada ou uma mudanca. 1-2 linhas.>

## Notas
<dominio, skills a consultar, preferencias desta frente>

## Decisoes ate agora
- [[<nota da decisao>]]: <resumo de uma linha da resposta>

## Ainda nao especificado
<o que esta no escopo, mas ainda nao da para formular como pergunta precisa>

## Fora do escopo
- [[<nota>]]: <resumo e por que esta fora>
```

O mapa e um **indice**. A decisao fica na nota dela. O mapa so resume e faz link.

## Notas de decisao

Cada decisao e uma nota com `tipo: decisao`, `pai: [[<mapa>]]`, `depende-de` e `modo`:

| Modo | Quem conduz | Uso |
|---|---|---|
| pesquisa | agente sozinho | Buscar um fato externo de que a decisao depende |
| prototipo | com o usuario | Algo concreto e descartavel para reagir ("como deve parecer") |
| entrevista | com o usuario | Conversa em rodadas (passo 5 do SKILL.md). Caso padrao. |
| tarefa | agente ou usuario | Trabalho manual que desbloqueia uma decisao (criar conta de teste, liberar acesso) |

Corpo da nota: `## Pergunta` (a decisao que ela resolve). A resposta entra so quando for resolvida, em `## Resposta`.

**Decisao ou "Ainda nao especificado"?** Se voce consegue formular a pergunta com precisao agora, e uma nota de decisao, mesmo que ainda dependa de outra. Se nao consegue, fica em "Ainda nao especificado".

## Modo 1: montar o mapa

1. **Nomeie o destino** com uma entrevista (passo 5). O destino define o escopo.
2. **Mapeie a fronteira** com uma entrevista em largura: cubra o espaco todo, sem aprofundar um tema. Se nao aparecer nenhuma incerteza grande, nao precisa de mapa: mude para `epico` ou `task`.
3. Crie a nota de mapa e as notas de decisao que ja podem ser formuladas, com as dependencias.
4. Dispare as decisoes de modo `pesquisa` em subagentes, em paralelo.
5. Pare. Montar o mapa e o trabalho de uma sessao.

## Modo 2: andar no mapa

1. Leia a nota de mapa (nao todas as notas de decisao).
2. Escolha a decisao: a que o usuario indicar, ou a primeira livre (todas as dependencias resolvidas).
3. Resolva conforme o `modo` da nota.
4. Escreva a resposta na nota da decisao, mude para `concluida` e acrescente uma linha em "Decisoes ate agora".
5. Crie as novas decisoes que a resposta tornou claras. Remova de "Ainda nao especificado" o que virou nota. Se a resposta mostra que algo esta alem do destino, mova para "Fora do escopo".

**Uma decisao por sessao**, exceto as de modo `pesquisa`.

## Fim do mapa

O mapa termina quando "Ainda nao especificado" esta vazio e nao ha decisao aberta. Proximo passo: `/task-plan` em modo `epico` usando a nota de mapa como entrada.
