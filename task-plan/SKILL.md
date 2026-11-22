---
name: task-plan
description: Estagio 1 (Plan) do fluxo Plan > Design > Build > Verify > Ship. Transforma uma demanda em spec acordada no vault - investiga os fatos, explica o codigo, entrevista em rodadas, confirma o entendimento (teach-back) e escreve a spec. Roteia por tipo (fix, feature, refatoracao, investigacao) e por tamanho (task, epico, mapa). Nao escreve codigo de producao.
argument-hint: <descricao livre da demanda> | <caminho de nota existente no vault>
disable-model-invocation: true
---

# Task Plan

Voce conduz o **Plan**: entrar em acordo sobre O QUE construir antes de qualquer codigo. A saida e uma **spec no vault** que o `/task-design` usa como entrada.

```
Demanda -> 1 Receber -> 2 Classificar -> 3 Investigar -> 4 Explicar -> 5 Entrevistar -> 6 Teach-back -> 7 Escrever spec -> [8 Dividir] -> 9 Handoff
                                            (fatos)       (como e hoje)  (decisoes)      (o que sera feito)
```

## Principios

- **Os fatos sao seus. As decisoes sao do usuario.** Nunca pergunte ao usuario algo que voce pode descobrir no codigo, no historico ou na documentacao. Nunca decida no lugar dele.
- **Nao avance com pergunta bloqueante aberta.** Duvida nao bloqueante vai para "Perguntas em aberto" ou "Fora do escopo".
- **Nao escreva codigo de producao.** Codigo de investigacao (reproducao de bug, script de medicao) e permitido. Ele fica em pasta descartavel e nao entra no commit, exceto quando o Design decidir reaproveitar.
- **Nenhum passo some em silencio.** Passo que nao se aplica fica na lista como `skip: <motivo>`.
- **Um lugar por fato.** Cada regra ou valor que muda comportamento visivel (limite, unidade, formato, mensagem, quem pode o que) fica por extenso **so no Contrato**. O resto da nota cita o item (`ver C3`). Dois lugares com o mesmo fato acabam com valores diferentes.

## Skills e contexto de apoio

Este arquivo descreve o metodo. Ferramentas e contexto do projeto ficam fora dele:

- **Contexto do projeto** (caminhos do vault, prefixos de ID, pastas, convencoes): leia da memoria do agente e do `CLAUDE.md`. Se faltar, pergunte uma vez e sugira salvar na memoria.
- **Sincronizacao do vault**: use a skill de sincronizacao do vault do projeto antes de ler e depois de escrever notas.
- **Sintaxe das notas**: `obsidian-markdown`.
- **Desenho de fluxo (opcional)**: `excalidraw`.

## 0. Abrir a lista de tarefas

Crie a lista de tarefas com os passos 1 a 9. Depois do passo 2, acrescente os passos do arquivo de tipo e, se houver, do arquivo de tamanho.

## 1. Receber a demanda

- Entrada: descricao livre ou caminho de uma nota existente. Se for nota existente com `status: pausada`, complete essa nota. Nao crie outra.
- Reescreva a demanda em 2-3 linhas: o problema e o resultado esperado, na visao de quem pediu.
- **LGPD:** nao leve para a nota dados pessoais de clientes (nome, CPF, CNPJ, contato). Use termos genericos ("Cliente X").

## 2. Classificar tipo e tamanho

Proponha a classificacao. O usuario confirma na primeira rodada da entrevista (passo 5).

| Tipo         | Quando                                      | Arquivo                 |
| ------------ | ------------------------------------------- | ----------------------- |
| fix          | Comportamento errado que ja existe          | `tipos/fix.md`          |
| feature      | Comportamento novo                          | `tipos/feature.md`      |
| refatoracao  | Estrutura muda, comportamento nao           | `tipos/refatoracao.md`  |
| investigacao | Pergunta a responder, sem mudanca de codigo | `tipos/investigacao.md` |

`docs` e `infra` seguem `tipos/feature.md` ate existir arquivo proprio.

| Tamanho | Quando                                                     | Arquivo             |
| ------- | ---------------------------------------------------------- | ------------------- |
| task    | Cabe em uma sessao. O caminho esta claro.                  | nenhum              |
| epico   | O caminho esta claro, mas nao cabe em uma task             | `tamanhos/epico.md` |
| mapa    | Ha decisoes grandes em aberto. O caminho nao esta visivel. | `tamanhos/mapa.md`  |

Leia o arquivo do tipo e, se houver, o do tamanho. Acrescente os passos deles na lista de tarefas.

## 3. Investigar (fatos)

Use subagentes leves, somente leitura. Nao gaste modelo forte em leitura.

- **Como funciona hoje:** um subagente explora a area e escreve uma explicacao de arquitetura para um engenheiro senior que nao conhece a area (fluxo, componentes, onde cada coisa fica).
- **Por que e assim:** um subagente le o historico (commits e PRs que criaram e alteraram a area). Ele cita o que os autores escreveram, marca o que e inferencia e diz o que o historico nao responde. Pule (`skip: <motivo>`) em area nova ou trivial.
- **Fatos externos** (API de terceiros, biblioteca, norma): pesquise em fonte primaria e salve as conclusoes com citacao na nota da task.
- **Glossario:** leia o glossario do projeto e use os termos dele.
- **Prova com dado real (condicional):** se a task cria ou muda regra, metrica, filtro ou formato sobre dado que ja existe, teste a premissa contra o dado antes da entrevista. Um subagente de contexto limpo roda a consulta **so em leitura** e devolve **so numero agregado** (contagem, minimo, mediana, maximo; com menos de 5 casos, so a contagem). Nunca registro individual nem dado pessoal. Nunca producao, a menos que o contexto do projeto defina uma fonte autorizada. Prova que contradiz a premissa muda a proposta antes de chegar ao usuario. Sem regra sobre dado existente: `nao se aplica - <motivo>`. Sem fonte so leitura disponivel: `prova indisponivel - <motivo>`.
- Execute os passos de investigacao do arquivo de tipo.

## 4. Explicar (como e hoje)

Objetivo: o usuario entender o terreno antes de decidir. No chat, curto. O detalhe vai para a nota.

1. **Resumo em 1 minuto** (ate ~120 palavras, sem `arquivo:linha`, sem codigo):
   - **Problema:** o que doi hoje e por que importa.
   - **Onde encaixa:** o caminho do pedido ou do dado em uma linha (ex.: botao -> service -> rota -> banco).
   - **Por que e assim:** a razao historica, se o passo 3 encontrou.
2. Pergunte: "quer o detalhe de alguma parte?". Aprofunde so o que o usuario pedir.

Regras: diga so o que e verdade; o que nao foi confirmado fica marcado "a validar". Defina cada termo do dominio em uma linha. Use os nomes reais das pecas.

## 5. Entrevistar (decisoes)

Mapeie as decisoes como uma arvore: cada decisao abre as decisoes que dependem dela. Trabalhe em **rodadas**.

- A **fronteira** e o conjunto de decisoes cujos pre-requisitos ja foram decididos. Pergunte a fronteira inteira em uma rodada. Pergunta que depende de outra ainda aberta fica para a rodada seguinte.
- Ordene por importancia. Formato de cada pergunta:

```
**Q1 - <titulo>**: <pergunta, com opcoes quando houver>
-> Recomendo: <resposta recomendada e o motivo em uma linha>
```

- Escreva cada pergunta de forma que "sim" aceite a recomendacao. O usuario pode responder "1 sim, 2 sim, 3 nao: X".
- **A primeira rodada sempre inclui:** classificacao (tipo e tamanho), definicao de pronto e Contrato.
  - **Definicao de pronto:** frases `quando ..., entao ...` nas **5 categorias**, com o ajuste do arquivo de tipo:
    - **feliz:** o caminho normal;
    - **erro esperado:** entrada invalida, recusa de negocio, falta de permissao;
    - **repeticao:** clique duplo, pedido duplicado, duas requisicoes ao mesmo tempo;
    - **limite:** zero, negativo, vazio, vencido, maximo;
    - **acesso indevido:** usuario A lendo ou alterando dado de B.

    Categoria que nao se aplica: `nao se aplica - <motivo>`. Cada frase vira um teste com o mesmo titulo.
  - **Contrato (`C1`, `C2`...):** o que outra parte do sistema, o banco ou o usuario enxerga e fica **fixo**: rota e metodo, formato de entrada e resposta, codigo de status e de erro, campo gravado, permissao por perfil, log ou auditoria gerado, texto de tela que importa. Nao repete as frases. Ate 5 sub-regras por item; mais que isso, quebre em outro item. **Tudo o que nao esta no Contrato e sugestao:** o Design e o Build podem mudar sem perguntar. Mudar o Contrato e mudar o QUE.
- Se uma pergunta precisa de um fato, mande um subagente buscar e continue com as outras perguntas. So as perguntas que dependem desse fato esperam.
- **Termos do dominio:** se o usuario usar termo vago ou em conflito com o glossario, aponte na hora e proponha o termo canonico. Se o codigo contradiz o que o usuario disse, mostre a contradicao.
- **Decisao que e de outra pessoa** (gestor, cliente, outro time): nao decida na sessao. Gere um questionario com `templates/questionario.md`, salve na nota, marque `status: aguardando` e pare. A task continua quando a resposta chegar.
- **Fim da entrevista:** a fronteira esta vazia. Nenhuma decisao ficou presumida em silencio.

## 6. Teach-back (o que sera feito)

Objetivo: o usuario conseguir explicar a task sem IA. Bloqueante, mas leve.

1. **Resumo em 1 minuto do que sera feito:**
   - **Problema** (1-2 frases).
   - **Onde encaixa** (1 linha).
   - **O que muda:** uma linha por peca nova ou alterada.
   - **Caminho descartado:** a alternativa mais simples e por que nao.
2. Faca **2-3 perguntas curtas sobre o porque** (nao decoreba de arquivo), ou aceite que o usuario resuma a task em 2-3 frases.
3. Se o usuario errar ou travar, reexplique so aquele ponto.
4. Nao avance sem confirmacao. "Entendi, pode seguir" conta.

## 7. Escrever a spec

1. Sincronize o vault. Defina o ID (prefixo do projeto + proximo numero livre, olhando tasks pendentes e concluidas).
2. Crie a nota a partir de `templates/spec.md` na pasta de tasks do vault. Antes de salvar, confira o "um lugar por fato": regra ou valor que aparece com valores diferentes em dois lugares e corrigido; fora do Contrato, so `ver Cn`.
3. **Glossario:** acrescente ou corrija os termos resolvidos na entrevista. O glossario tem so termos, sem detalhe de implementacao.
4. **Decisao de arquitetura:** registre na documentacao de arquitetura do vault so quando as tres condicoes forem verdadeiras: (a) dificil de reverter, (b) surpreendente sem contexto, (c) resultado de um trade-off real, e **com o OK do usuario** (decisao nova so nasce com OK). Senao, a decisao fica so na nota da task.
5. **Desenho de fluxo (opcional):** pergunte se o usuario quer. Se sim, use a skill `excalidraw` e salve na pasta de desenhos do projeto.
6. Escreva a linha `plan` no "Registro de etapas", no formato do template.
7. Sincronize o vault (commit e push das notas).

## 8. Dividir (so epico e mapa)

Siga o arquivo de tamanho. Para tamanho `task`: `skip: task unica`.

## 9. Criterio de saida e handoff

Confira antes de encerrar:

- [ ] Definicao de pronto nas 5 categorias (ou `nao se aplica - motivo`) e Contrato aprovados.
- [ ] Prova com dado real feita, ou registrada como `nao se aplica` / `indisponivel` com motivo.
- [ ] Nenhuma pergunta bloqueante aberta.
- [ ] Teach-back confirmado.
- [ ] Spec salva e vault sincronizado.
- [ ] Itens pulados registrados com `skip: <motivo>` na nota.

Mostre: ID, caminho da nota, desenho (se houver), commit do vault.

Proximo passo:

- tipo `investigacao`: nao ha Design. Entregue a resposta e encerre.
- demais tipos: ofereca **`/task-design <nota>`**. So ofereca se o teach-back foi confirmado.
