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

Siga "Quando parar", "Limites de tentativas" e "Saida de toda parada" de `../task-comum/regras.md`. O Build nao tem caso proprio.

No Build, o caso 1 aparece na conferencia do passo 4 (item do Contrato que mudou) e no relatorio do subagente.

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

Toda parada deste passo e o caso 0 de `../task-comum/regras.md`, com a linha de resultado.

- Sem argumento: se houver uma so task `ativa` com `estagio: design`, use-a. Se houver mais, tente casar pela branch atual. Se continuar ambiguo, pare e liste as notas candidatas na linha de resultado. Nao pergunte: nesta sessao ninguem responde.
- A nota precisa ter `estagio: design` com aprovacao registrada, ou `estagio: build` com `status: ativa` (retomada, ver "Reentrada" de `../task-comum/regras.md`). Senao, pare: o Design nao foi aprovado.
- Notas de `depende-de` precisam estar `concluida`. Senao, pare.
- Crie a lista de tarefas com os passos 1 a 6.

## 1. Preparar

1. Sincronize o vault e leia a nota inteira: Definicao de pronto, Design (forma, plano de testes, etapas), Evidencias da investigacao.
2. **Branch.** O workspace e do orquestrador; a branch e do Build. Em cada subprojeto que a task toca, crie a branch a partir da base do projeto, com a convencao de nomes do projeto. Se o workspace ja esta numa branch com o nome da convencao para esta task, use-a. Nunca trabalhe na branch base. Task que toca dois repositorios: mesma branch nos dois.
3. **Linha de base:** antes de qualquer mudanca, rode a suite de testes, o lint e o build. Registre o resultado. Falha que ja existia **nao e desta task**: registre como pre-existente e nao corrija, a menos que esteja no escopo.
4. **Retomada** (a Execucao ja registra branch e etapas): use a branch da Execucao, nao crie outra. Mantenha a linha de base registrada. Etapa com commit e conferida na Execucao, e sem mudanca no Design, nao e refeita: o subagente comeca pela primeira etapa que falta.

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
- ao fim de cada etapa, com a suite verde, faz **um commit local** (excecao: fix, ver "Por tipo");
- devolve o relatorio no formato do brief, com a evidencia de cada teste (saida vermelha e verde).

**Sem subagente.** Siga "Sem subagente" de `../task-comum/regras.md`. No Build, o lider executa as etapas com o mesmo ciclo de `referencias/tdd.md` e o mesmo relatorio do brief. O passo 4 continua igual.

## 4. Conferir (lider)

Nao aceite o relatorio sem conferir:

1. **Por etapa** (`git log` e `git show` de cada commit):
   - [ ] existe o commit da etapa;
   - [ ] o commit tem o rodape `Task: <ID>`, como manda o `commits.md` do Ship. Esse rodape e o caminho do codigo ate o porque (blame -> commit -> ID -> nota), agora que o porque nao fica no comentario. Commit sem rodape: corrija antes do push (no Build os commits ainda sao locais);
   - [ ] os testes planejados para a etapa existem e testam o criterio (nao detalhe interno);
   - [ ] o relatorio mostra o vermelho **pelo motivo certo** antes do verde;
   - [ ] arquivos alterados estao dentro do que a etapa previa (ou o desvio esta registrado);
   - [ ] nenhum item do Contrato mudou (rota, formato, status, campo gravado, permissao, log);
   - [ ] se a etapa le dado ja gravado, a Definicao de pronto tem frase para dado fora do padrao (categoria limite do Plan). Senao, o codigo nao decide o comportamento e o caso vai aos candidatos a Atencao: "dado gravado fora do padrao sem frase na Definicao de pronto".
2. **Testes do plano intactos:** compare os testes com o plano. Assercao enfraquecida, esperado trocado, teste pulado (`skip`, `only`, `todo`) ou teste do plano removido = reprovado. No fix, nenhum teste do plano termina como falha esperada: a marca do commit de reproducao sai no commit da correcao.
3. **Rode voce mesmo:** suite completa, lint e build. Compare com a linha de base. Apontamento novo de lint nos arquivos tocados = reprovado. Apontamento que pode ser decisao de dominio: escolha a opcao conservadora, registre e marque "Atencao".
4. **Reprovado:** dispare um **subagente novo** com o brief original + a lista objetiva do que falhou (nao continue o subagente anterior). Limite de rodadas: tabela de `../task-comum/regras.md`. Na segunda, aplique a regra de modelo. Persistiu: caso 4.

## 5. Limpar o diff

Siga `referencias/limpeza.md` sobre o diff da task inteira, em duas passagens:

1. **(a) Limpeza geral:** o lider ou um subagente aplica a secao "(a) Limpeza geral".
2. **(b) Comentarios e supressoes:** dispare um **subagente de contexto limpo** com a secao "(b) Comentarios e supressoes" e o escopo do diff. Quem escreveu tende a defender o proprio comentario. Sem subagente: vale "Sem subagente" de `../task-comum/regras.md`, numa passagem separada que rele o diff do zero.
3. **Conferir (lider):** leia o relatorio e o diff da passagem (b). Rejeite edicao que muda comportamento ou que sai do diff da task. Rode de novo testes, lint e build. Reverta qualquer edicao de limpeza que quebrar algo.
4. **Commit local** no padrao do `commits.md` do Ship: `refactor(<escopo>): limpa o diff da task`, com o rodape `Task: <ID>`.

Limpeza nao e refatoracao: nao mude estrutura que o Design nao previu. Unica excecao: a reescrita pequena, dentro do diff, que troca um comentario por codigo que deixa a regra obvia (ver `referencias/limpeza.md`).

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
| fix         | O primeiro commit e o teste de reproducao, **vermelho de proposito**: e a prova, no historico, de que o teste pega o bug. E a unica excecao a regra de commit com a suite verde. Se o projeto tem hook de pre-commit que roda os testes, marque o teste como falha esperada (`test.fails`, `xfail`) nesse commit, sem linha nos debitos (a marca e temporaria). O commit seguinte e a correcao, com a suite verde e o teste ja sem a marca. Se nao existe seam certo para o teste de regressao, isso e um achado: registre e use o ciclo de feedback do Plan como verificacao. Remova todo log de debug marcado (`[DEBUG-...]`). A causa confirmada vai na mensagem do commit da correcao. |
| refatoracao | Etapa 1 = trava de comportamento, verde **antes** de mover estrutura. Testes existentes nao mudam. Toda etapa termina com a trava verde.                                                                                                                                                                                    |
| feature     | Um teste por criterio, na ordem do plano. Parte sem teste automatizado possivel (ex.: componente sem base de teste): implemente sem teste, registre "comprovacao no Verify" e confira que a linha "Comprovacao no app" do Design existe.                                                                                    |
