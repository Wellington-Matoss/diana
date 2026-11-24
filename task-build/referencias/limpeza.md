# Limpeza do diff

Escopo: o diff da task contra a branch base, incluindo mudancas nao commitadas. Nao mexa em codigo fora do diff. Comentario antigo fora do diff fica como esta.

A limpeza tem duas passagens, nesta ordem: **(a) limpeza geral** e **(b) comentarios e supressoes**. As duas seguem as "Regras" do fim.

## (a) Limpeza geral

- **Defesa fora do normal:** `try/catch`, verificacao de nulo ou validacao em caminho interno que ja recebe dado validado. Validacao fica na fronteira (entrada da API, leitura de arquivo, resposta externa).
- **Cast para contornar tipo** (`as any`, `as unknown as X`) sem validacao antes.
- **Aninhamento** que um retorno antecipado resolve.
- **Codigo morto** criado pela task: funcao, variavel, import ou parametro sem uso.
- **Log de debug** e `console.log` deixados pela task.
- **Padrao diferente do arquivo:** nomes, formatacao ou estrutura que nao seguem o resto do arquivo.

## (b) Comentarios e supressoes

Rode num subagente de contexto limpo (ver passo 5 do `SKILL.md`). Quem escreveu o comentario tende a defende-lo.

Por que: comentario de regra de negocio e o mesmo fato escrito em dois lugares, no codigo e na nota da task, no glossario ou no Contrato. Dois lugares acabam dizendo coisas diferentes. Ninguem mantem o comentario, e o agente que le o codigo acredita nele. O porque fica na nota, no glossario, no Contrato e no titulo do teste. O rodape `Task: <ID>` de cada commit leva do codigo ate a nota.

### Lista fechada do que fica

So fica o comentario que cabe num destes casos:

1. licenca;
2. restricao de dependencia externa que nao controlamos (fornecedor, plataforma, protocolo, firmware), com link quando houver;
3. documentacao de contrato de API publica;
4. link para issue que explica uma restricao que o codigo nao consegue expressar.

Todo o resto sai: narracao, comentario que repete o codigo, regra de negocio, justificativa de contorno, codigo comentado, banner e separador. **Na duvida, sai.**

### Surpresa no nosso proprio codigo

Comentario que explica um comportamento surpreendente do nosso codigo sai. No lugar dele, o codigo deixa a regra obvia: nome, extracao de funcao, tipo, ou teste com o nome da regra.

- So dentro do diff e sem mudar comportamento.
- A reescrita nao cabe na task: registre uma pendencia na nota (candidato a debito). Nunca deixe um comentario no lugar.
- O motivo da regra fica na nota e no Contrato.

### Supressao de lint ou de tipo

Supressao de lint ou de tipo (ex.: `eslint-disable`, `@ts-ignore`, `# noqa`, `# type: ignore`) entra na lista de remocao. Leia a regra suprimida:

- regra puramente de estilo: a supressao fica;
- regra que protege a correcao do codigo: remova a supressao e corrija o codigo;
- a correcao sai do escopo da task: a supressao fica e o caso entra nos candidatos a Atencao.

### "Nao remover", "IMPORTANTE" e similares

A afirmacao nao vale sem conferencia. Confira a restricao: leia o codigo em volta, siga o simbolo citado e leia o historico (commit e nota da task pelo rodape).

- Restricao confirmada: o comentario fica. Entra nos candidatos a Atencao a proposta de transformar a restricao num teste, num tipo ou numa checagem automatica. O dono decide no PR.
- Restricao nao confirmada: o comentario sai.

### Relatorio do subagente

O subagente so remove comentario e supressao e faz a reescrita que deixa a regra obvia. Ele devolve:

- arquivos tocados e quantidade de comentarios removidos;
- reescritas feitas (simbolo e regra);
- pendencias criadas (candidatos a debito);
- supressoes removidas e mantidas, com a regra de cada uma;
- restricoes conferidas: confirmada ou nao, com a prova.

## Regras

- Comportamento nao muda.
- Edicoes pequenas e focadas. A unica reescrita permitida e a que troca um comentario por codigo que deixa a regra obvia.
- Depois de limpar: rode testes, lint e build. **Reverta** a edicao de limpeza que quebrar algo.
