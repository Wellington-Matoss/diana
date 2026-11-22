# Tipo: investigacao

Uma pergunta a responder. Somente leitura. Nao muda codigo.

## Definicao de pronto

- A pergunta esta respondida com fontes (`arquivo:linha`, commit, PR, documentacao).
- O que e inferencia esta marcado como inferencia.
- O que nao foi possivel responder esta listado.
- Se a pergunta e uma escolha entre alternativas: recomendacao com tabela de trade-offs.

## Fluxo

- Passo 3: investigue com subagentes. Para "por que e assim", use o historico.
- Passo 4: a explicacao e a propria entrega.
- Passo 5: entreviste so para delimitar a pergunta (escopo, profundidade, para que serve a resposta).
- Passo 6: `skip: investigacao, o teach-back e a explicacao do passo 4`. Se o usuario quiser, faca o teach-back.
- Passo 7: salve a resposta na nota de task com o formato abaixo. Status: `concluida`.

## Formato da resposta

- Visao geral
- Conceitos-chave
- Como funciona
- Onde cada coisa fica
- Armadilhas
- (se for decisao) Alternativas e trade-offs, com recomendacao

## Se a investigacao levar a uma mudanca

Nao implemente. Encerre a investigacao e abra uma nova task com `/task-plan`, com o tipo certo (fix, feature ou refatoracao) e link para esta nota.
