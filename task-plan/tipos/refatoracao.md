# Tipo: refatoracao

A estrutura muda. O comportamento nao muda. Diferente de feature (acrescenta comportamento) e de fix (corrige comportamento).

## Definicao de pronto

- **Comportamento igual:** a trava de comportamento passa antes e depois da mudanca.
- **Leitura mais facil:** um ganho concreto e verificavel. Exemplos: menos camadas entre a chamada e a regra; menos ramificacoes; wrapper de um so chamador removido; tipo que impede estado invalido. "Codigo mais limpo" nao serve.
- Formato dos criterios:
  - `Quando <entrada ou acao>, entao <mesma saida de hoje>.`
  - `<ganho de leitura mensuravel>.`

## Investigacao (passo 3)

1. **Mapeie o contrato:** o que os chamadores observam hoje (entradas, saidas, erros, efeitos colaterais).
2. **Mapeie a cobertura:** quais testes ja cobrem esse contrato. Type check e lint nao contam como trava.
3. Se a cobertura nao for suficiente, registre: "a trava de comportamento e a primeira etapa do Build". O Design define a trava (teste de caracterizacao, snapshot ou comparacao antigo x novo).
4. **Nomeie a estrutura que falta** (ex.: maquina de estados no lugar de booleanos espalhados, tabela no lugar de if/else). A forma alvo e decidida no Design.
5. Liste codigo morto e wrappers que podem sair antes da mudanca (remover antes de acrescentar).

## Regras de escopo

- Bug encontrado durante a refatoracao: vira task `fix` separada. Nao corrija dentro da refatoracao.
- Comportamento novo: vira task `feature` separada.
- Escreva os dois casos em "Fora do escopo" com link para a nova nota.
- Refatoracao ampla (renomear ou trocar tipo usado no projeto inteiro): tamanho `epico`, com a sequencia expandir -> migrar em lotes -> contrair (ver `tamanhos/epico.md`).
