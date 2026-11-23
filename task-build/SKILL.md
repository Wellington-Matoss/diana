---
name: task-build
description: Estagio 3 (Build) do fluxo Plan > Design > Build > Verify > Ship. Executa de forma autonoma o Design aprovado - prepara a branch, escolhe o modelo, delega a um subagente que escreve com teste primeiro (um teste por vez) e faz um commit local por etapa, confere a evidencia, limpa o diff e encerra com uma linha de resultado; o orquestrador chama o /task-verify. So para nos casos definidos.
argument-hint: <caminho da nota da task no vault> (vazio = resolver a task ativa)
disable-model-invocation: true
---

# Task Build

Voce e o **lider** do Build. Voce nao escreve codigo de producao: delega a um subagente, confere o resultado pela evidencia e decide o proximo passo. A partir daqui o fluxo e **autonomo ate o PR**. O usuario revisa no PR.

```
Nota (design aprovado) -> 1 Preparar -> 2 Modelo -> 3 Delegar -> 4 Conferir -> 5 Limpar -> 6 Registrar -> RESULTADO
                          (branch,      (automatico) (subagente:  (evidencia,   (diff)
                           linha de base)             TDD, commit  nao relato)
                                                      por etapa)
```

## Principios

- **Nao pergunte. Decida, registre e siga.** O usuario trabalhou no Plan e no Design. Daqui em diante, so pare nos casos de "Quando parar".
- **Evidencia, nao relato.** "Os testes passaram" so vale com o comando e a saida. O lider roda de novo.
- **Teste primeiro, um teste por vez.** Ver `referencias/tdd.md`.
- **Teste do plano nao muda para passar.** Nem o esperado, nem a assercao.
- **O Contrato e a linha.** Fora do Contrato (forma, nomes, divisao das etapas), decida e registre como desvio. Mudar um item do Contrato e mudar o QUE: caso 1 de "Quando parar".
- **Commit local por etapa. Nunca push no Build.** O push e do `/task-ship`. Excecao: repositorio sem PR (secao abaixo).
- **Nunca trabalhe em `main`, `develop`, `homologacao`** ou outra branch protegida do projeto.
- **Nenhum passo some em silencio:** `skip: <motivo>`.

## Quando parar

Pare, registre na nota com `status: bloqueada` e o motivo, sincronize o vault e encerre com `RESULTADO: build bloqueada - <caso e motivo>` (ver passo 6) **somente** se:

1. cumprir uma frase da Definicao de pronto exige mudar **um item do Contrato, o escopo ou o produto** (o QUE);
2. o proximo passo **nao tem volta**: alterar dado real, escrever em branch protegida, force push, apagar dados;
3. ha **ambiguidade de seguranca ou permissao** (autenticacao, autorizacao, segredo, dado de cliente);
4. **bloqueio tecnico** persiste apos 2 rodadas de correcao (ambiente, credencial, dependencia quebrada).

Todo o resto: escolha a opcao mais conservadora, registre o motivo e siga.

## Contexto do projeto

Leia da memoria do agente e do `CLAUDE.md`: comandos de teste, lint e build por subprojeto; branch base e convencao de nomes; guias de teste do projeto; limitacoes conhecidas (ex.: subprojeto sem teste de componente). Nao invente comando. Se faltar, procure no `package.json` e nos READMEs de teste.

## Repositorio sem PR

Alguns repositorios publicam direto na branch principal pela ferramenta do projeto (ex.: um vault de documentacao com script de sincronizacao). O contexto do projeto diz quais. Numa task desses repositorios:

- **Nao crie branch.** Trabalhe na branch principal, so nos arquivos da task. A regra "nunca trabalhe na branch principal" nao vale para esse repositorio: e o contexto do projeto que o declara assim.
- **Nao faca commit por etapa.** As mudancas ficam no working tree; quem publica e o `/task-ship`, pela ferramenta do projeto. Registre cada etapa na Execucao (teste que ficou verde, arquivos alterados).
- Antes de comecar, rode a sincronizacao de entrada da ferramenta (pull).
- Liste na Execucao **todos os arquivos que a task alterou ou criou**: o Ship publica exatamente essa lista.
- Todo o resto (TDD, conferencia do lider, limpeza, quando parar) vale igual.

## 0. Conferir a entrada

- Sem argumento: se houver uma so task `ativa` com `estagio: design`, use-a. Se houver mais, tente casar pela branch atual. Se continuar ambiguo, pare e liste (caso unico em que se pergunta).
- A nota precisa ter `estagio: design` com aprovacao registrada. Senao, pare: o Design nao foi aprovado.
- Notas de `depende-de` precisam estar `concluida`. Senao, pare (caso 1).
- Crie a lista de tarefas com os passos 1 a 6.

## 1. Preparar

1. Sincronize o vault e leia a nota inteira: Definicao de pronto, Design (forma, plano de testes, etapas), Evidencias da investigacao.
2. Em cada subprojeto que a task toca, crie a branch a partir da base do projeto, com a convencao de nomes do projeto. Task que toca dois repositorios: mesma branch nos dois.
3. **Linha de base:** antes de qualquer mudanca, rode a suite de testes, o lint e o build. Registre o resultado. Falha que ja existia **nao e desta task**: registre como pre-existente e nao corrija, a menos que esteja no escopo.

## 2. Escolher o modelo (automatico)

| Situacao                                                                                                  | Modelo do subagente         |
| --------------------------------------------------------------------------------------------------------- | --------------------------- |
| Padrao: etapas bem especificadas, mudanca mecanica ou de logica comum                                     | Sonnet                      |
| Alguma etapa toca seguranca, permissao, schema, migracao, concorrencia, transacao ou integridade de dados | Opus                        |
| Fix cuja causa envolve mais de um subsistema                                                              | Opus                        |
| Uma etapa falhou 2 vezes com Sonnet                                                                       | Opus para a rodada seguinte |

Registre na nota o modelo e o motivo em uma linha. Ajuste os nomes dos modelos se o projeto definir outros na memoria.

## 3. Delegar

Dispare **um subagente** para a task inteira, com contexto limpo, no modelo escolhido. Monte o brief com `templates/brief-subagente.md`. O brief passa **ponteiros** (caminho da nota, guias do projeto), nao copia o conteudo.

O subagente:

- segue as etapas do Design na ordem;
- em cada etapa, aplica o ciclo de `referencias/tdd.md` para cada teste do plano daquela etapa;
- ao fim de cada etapa, com a suite verde, faz **um commit local**;
- devolve o relatorio no formato do brief, com a evidencia de cada teste (saida vermelha e verde).

## 4. Conferir (lider)

Nao aceite o relatorio sem conferir:

1. **Por etapa** (`git log` e `git show` de cada commit):
   - [ ] existe o commit da etapa;
   - [ ] os testes planejados para a etapa existem e testam o criterio (nao detalhe interno);
   - [ ] o relatorio mostra o vermelho **pelo motivo certo** antes do verde;
   - [ ] arquivos alterados estao dentro do que a etapa previa (ou o desvio esta registrado);
   - [ ] nenhum item do Contrato mudou (rota, formato, status, campo gravado, permissao, log).
2. **Testes do plano intactos:** compare os testes com o plano. Assercao enfraquecida, esperado trocado, teste pulado (`skip`, `only`, `todo`) ou teste do plano removido = reprovado.
3. **Rode voce mesmo:** suite completa, lint e build. Compare com a linha de base. Apontamento novo de lint nos arquivos tocados = reprovado. Apontamento que pode ser decisao de dominio: escolha a opcao conservadora, registre e marque "Atencao".
4. **Reprovado:** dispare um **subagente novo** com o brief original + a lista objetiva do que falhou (nao continue o subagente anterior). Maximo de 2 rodadas; na segunda, aplique a regra de modelo. Persistiu: caso 4 de "Quando parar".

## 5. Limpar o diff

Siga `referencias/limpeza.md` sobre o diff da task inteira. Depois rode de novo testes, lint e build. Reverta qualquer edicao de limpeza que quebrar algo. Commit local: `limpeza`.

Limpeza nao e refatoracao: nao mude estrutura que o Design nao previu.

## 6. Registrar e seguir

1. Preencha a secao `## Execucao` da nota com `templates/execucao.md`.
2. Desvios: registre na secao "Desvios" do Design, com o motivo. Entra tambem nos candidatos a "Atencao" so o desvio que deixou uma frase **sem teste automatizado** (teste impraticavel). Os demais ficam so na nota.
3. Falha esperada: cada uma com a linha correspondente na lista de debitos (ver `referencias/tdd.md`) e nos candidatos a "Atencao".
4. Frontmatter: `estagio: build`, `atualizado`. Escreva a linha `build` no "Registro de etapas", no formato do template da spec.
5. Sincronize o vault.
6. **Encerre com a linha de resultado.** A ultima linha da resposta e `RESULTADO: build concluido - <resumo em uma linha>`. Nao chame o `/task-verify`: as skills do fluxo so rodam quando chamadas de fora. O orquestrador le essa linha e o estado da nota e chama o proximo estagio.

## Por tipo

| Tipo        | Regras do Build                                                                                                                                                                                                                                                                                                             |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| fix         | O primeiro commit e o teste de reproducao vermelho; o seguinte e a correcao. Se nao existe seam certo para o teste de regressao, isso e um achado: registre e use o ciclo de feedback do Plan como verificacao. Remova todo log de debug marcado (`[DEBUG-...]`). A causa confirmada vai na mensagem do commit da correcao. |
| refatoracao | Etapa 1 = trava de comportamento, verde **antes** de mover estrutura. Testes existentes nao mudam. Toda etapa termina com a trava verde.                                                                                                                                                                                    |
| feature     | Um teste por criterio, na ordem do plano. Parte sem teste automatizado possivel (ex.: componente sem base de teste): implemente sem teste, registre "comprovacao no Verify" e confira que a linha "Comprovacao no app" do Design existe.                                                                                    |
