# Tipo: feature

Comportamento novo. Tambem vale para `docs` e `infra` ate existir arquivo proprio.

## Definicao de pronto

- Criterios de aceite do ponto de vista de quem usa:
  - `Quando <ator> <faz acao> <em condicao>, entao <resultado observavel>.`
- Um criterio por comportamento. Inclua casos de erro e de permissao (ex.: usuario sem acesso).
- Todo criterio deve ser verificavel no aplicativo real ou na API. Evite criterio que depende de detalhe interno.

## Investigacao (passo 3)

1. Encontre o **precedente**: funcionalidade parecida ja existente no projeto. Ela indica padrao de codigo e de teste.
2. Identifique onde a feature encosta: telas, rotas, services, colecoes ou tabelas.
3. Liste os termos novos do dominio que a feature cria.

## Entrevista (passo 5)

Garanta que a fronteira cobre:

- Quem usa e o que muda para essa pessoa.
- Comportamento nos casos de borda (lista vazia, erro de rede, permissao negada, dado invalido).
- Termos do dominio novos ou alterados.
- O que fica **fora da v1**.

Pergunta de forma ou comportamento que so se resolve vendo ("como deve parecer", "como deve se comportar"): registre como pergunta em aberto para o Design resolver com prototipo descartavel. Nao force a decisao no Plan.

## Tamanho

Se a feature tem mais de um comportamento entregavel de forma independente, considere `epico` e divida em fatias verticais.
