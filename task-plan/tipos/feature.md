# Tipo: feature

Comportamento novo. Tambem vale para `docs` e `infra` ate existir arquivo proprio.

## Definicao de pronto

- As 5 categorias completas (feliz, erro esperado, repeticao, limite, acesso indevido), do ponto de vista de quem usa:
  - `Quando <ator> <faz acao> <em condicao>, entao <resultado observavel>.`
- Uma frase por comportamento. Toda frase e verificavel no aplicativo real ou na API; evite frase que depende de detalhe interno.
- **Acesso indevido** e obrigatoria quando a feature le ou grava dado com dono (outro cliente, outra entidade, outro local).
- **Repeticao** e obrigatoria quando a feature grava algo (clique duplo, duas requisicoes simultaneas).
- O Contrato fixa o que a tela, a API e o banco expoem: rotas, campos, status, permissoes, logs.

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
