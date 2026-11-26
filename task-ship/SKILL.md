---
name: task-ship
description: Estagio 5 (Ship) do fluxo Plan > Design > Build > Verify > Ship. De forma autonoma - confere o estado da branch, integra a base, confere o changelog do projeto (se houver), faz push, abre o PR no padrao do fluxo (sem merge), acompanha o CI quando o projeto tem, marca a task como em revisao e registra licoes do processo. O merge e sempre do usuario.
argument-hint: <caminho da nota da task no vault> (vazio = resolver a task ativa)
disable-model-invocation: true
---

# Task Ship

Voce entrega o trabalho verificado como PR. O fluxo continua **autonomo**. Esta e a unica mensagem que o usuario recebe da execucao: faca o PR e o relatorio final valerem a leitura.

```
Nota (verify concluido) -> 1 Conferir -> 2 Integrar base -> 3 Changelog -> 4 Push -> 5 PR -> 6 CI -> 7 Nota -> 8 Licoes -> Relatorio
                                                            (se houver)                      (se houver)
```

## Principios

- **Nunca faca merge.** Nunca force push. Nunca escreva em branch protegida. Nunca use `--no-verify`. Nunca marque um check como nao obrigatorio.
- **Nada de segredo no diff.** Encontrou: pare (caso 5).
- **O PR e para o usuario ler em um minuto.** Sem preambulo, sem repetir o que o diff ja mostra.
- **Nenhum passo some em silencio:** `skip: <motivo>`.

## Quando parar

Siga "Quando parar", "Limites de tentativas" e "Saida de toda parada" de `../task-comum/regras.md`. Os casos proprios do Ship (5, 6 e 7) estao la.

No Ship, o caso 2 aparece quando o push ou o PR exigiria acao sem volta ou em branch protegida. O caso 5 aparece no passo 1; o caso 6, no passo 2; o caso 7, nos passos 4 e 5. O caso 4 aparece quando a correcao por subagente dos passos 2 ou 6 passa do limite.

**Sem subagente.** Siga "Sem subagente" de `../task-comum/regras.md`: o proprio Ship faz a correcao numa passagem separada.

## Contexto do projeto

Leia da memoria do agente e do `CLAUDE.md`: branch base do PR; idioma das mensagens; se ha changelog para o usuario final; se ha CI; repositorios separados.

## Repositorio sem PR

Se a task e de um repositorio que publica direto (contexto do projeto), o Ship encurta. A branch principal desse repositorio nao conta como protegida **so para a ferramenta de publicacao do projeto**; nunca faca commit ou push nela por outro caminho.

1. **Conferir o estado** (passo 1): so os arquivos listados na Execucao estao alterados; nada de segredo.
2. **Pular** os passos 2, 4, 5 e 6 (`skip: repositorio sem PR`). Conferir o changelog (passo 3) so se o contexto pedir.
3. **Publicar** pela ferramenta do projeto, passando exatamente os arquivos da Execucao **e a nota da task**, com a mensagem de commit do vocabulario do projeto para o estagio `ship`. Siga a saida da ferramenta: erro de validacao, corrija e rode de novo; conflito, caso 6; recusa, caso 7.
4. **Nota** (passo 7): `estagio: ship`; secao `## Entrega` com o commit publicado ("publicada no commit <hash>"), sem PR.
5. **Licoes** (passo 8) igual.
6. **Fechar:** como nao ha merge a esperar, o orquestrador chama o `/task-close <nota>` em seguida. Nao chame voce: encerre com `RESULTADO: ship concluido - publicada no commit <hash>`.

## 0. Conferir a entrada

Toda parada deste passo e o caso 0 de `../task-comum/regras.md`, com a linha de resultado.

- Sem argumento: resolva a task ativa como no Build.
- A nota precisa ter `estagio: verify` concluido, sem bloqueante aberto. Senao, pare: o Verify nao aprovou.
- Excecao: nota `em-revisao` com pedido de mudanca sem resposta no PR aberto (comentario ou revisao; o PR e a fonte; resposta: passo 6). O orquestrador chama o Ship de novo, e ele vai direto a correcao do passo 6.
- A branch atual precisa ser a registrada na Execucao. Se nao for e der para trocar sem perder nada (sem mudanca fora de commit), troque. Senao, pare. Repositorio sem PR: nao ha branch da task; confira a branch principal.
- Crie a lista de tarefas com os passos 1 a 8.

## 1. Conferir o estado

1. Branch atual nao e protegida.
2. `git status` limpo: nada fora dos commits da task.
3. O diff (`git diff <base>...HEAD`) so tem arquivos da task. Arquivo nao relacionado: remova do diff com um commit `chore: remove alteracao fora do escopo` e registre.
4. Todo commit da task tem o rodape `Task: <ID>` ("Conferencia do rodape" de `referencias/commits.md`). Commit local sem rodape: corrija a mensagem antes do push. Commit ja enviado sem rodape: nao reescreva o historico; registre o hash na nota.
5. Procure segredos no diff: `.env`, chave, token, certificado, senha, dado pessoal. Encontrou: caso 5.

## 2. Integrar a base

1. `git fetch` e confira se a branch esta atras da base.
2. Atras: faca merge da base na branch (nao rebase: preserva os commits ja verificados).
3. Conflito **mecanico** (lockfile, import, formatacao, arquivos independentes): resolva. Conflito na **logica** da task: caso 6.
4. Houve merge da base: rode de novo testes, lint e build. Vermelho: "Correcao por subagente" de `../task-comum/regras.md`, com o erro. Limite: tabela do mesmo arquivo; persistindo, caso 4.

## 3. Conferir o changelog (se houver)

So confira: o bullet da etapa do changelog (`/task-design`, passo 6) entrou no diff, ou ha `skip` com motivo. Faltou: "Correcao por subagente" de `../task-comum/regras.md`.

Sem changelog no projeto: `skip: projeto sem changelog`.

## 4. Push

`git push -u origin <branch>`. Task em dois repositorios: push nos dois.

## 5. Abrir o PR

1. **Titulo:** `tipo(escopo): assunto` (`referencias/commits.md`). No merge com squash, o titulo vira a mensagem do commit na base.
2. **Corpo:** `templates/pr.md`, com o conteudo do Verify (resumo do diff, evidencia, Atencao, sugestoes) e do Build (desvios). Ate ~40 linhas. Secao vazia sai, exceto "Atencao", que mostra "Nada." quando vazia.
3. Abra **pronto para revisao** (nao rascunho), para a base do projeto: `gh pr create --base <base> --head <branch> --title "<titulo>" --body-file <arquivo>`. Se a branch ja tem PR aberto (Ship retomado), nao abra outro: atualize o titulo e o corpo dele (`gh pr edit`).
4. Dois repositorios: abra os dois PRs e coloque o link de um no outro.
5. **Nao faca merge.**

## 6. Acompanhar o CI (se houver)

Projeto sem CI: `skip: projeto sem CI`.

1. Espere os checks terminarem (`gh pr checks <pr> --watch`).
2. Verde: siga.
3. Falha **causada pelo diff** ou pedido de mudanca do PR (passo 0): leia o primeiro erro acionavel no log, ou o pedido, e aplique "Correcao por subagente" de `../task-comum/regras.md`, com o erro (inclui o ataque a correcao antes do push). No pedido, rode tambem o passo 1 sobre o commit novo antes do push. Push e espere de novo. No pedido, responda no PR com o commit da correcao: pedido respondido assim esta tratado, e a proxima chamada so trata pedido sem resposta. Pedido que muda o QUE (Contrato, escopo, produto): caso 1. Limite: tabela do mesmo arquivo; depois, caso 4.
4. Falha **nao causada pelo diff** (instabilidade, infraestrutura, falha que ja existe na base): siga a nota "CI vermelho nao causado pelo diff" de `../task-comum/regras.md`. Persistindo, comente no PR com a evidencia.
5. Nunca mude o esperado de um teste para o CI passar.

## 7. Atualizar a nota

- Frontmatter: `status: em-revisao`, `estagio: ship`, `atualizado`, `pr: [<url>, ...]`.
- Secao `## Entrega`: branch, PRs (URL), estado do CI, changelog (se houve). Escreva como fato: "PR #12 aberto para develop".
- Escreva a linha `ship` no "Registro de etapas", no formato do template da spec.
- Sincronize o vault.

## 8. Licoes do processo

Leia o "Registro de etapas", a Execucao e a Verificacao da nota. **Registre so se algo aconteceu.** Nada aconteceu: `skip: sem licoes` (o resultado esperado na maioria das tasks).

Conta como licao:

- correcao por subagente no Verify ou no Ship (por que o Build nao pegou antes?);
- bloqueio ou parada (o que faltou: contexto, permissao, ferramenta?);
- comando, caminho ou convencao que o agente teve que descobrir e nao estava no contexto do projeto;
- revisor que deixou passar algo que o CI ou outro revisor pegou;
- desvio de design recorrente.

Para cada licao, escolha **uma** proposta, nesta ordem de preferencia:

1. **Checagem automatica** (regra de lint, hook, job de CI), se o erro e mecanico. Checagem vale mais que texto.
2. **Contexto do projeto** (comando ou convencao que faltou).
3. **Ajuste na skill do fluxo** (passo, regra ou brief).

Acrescente na nota de licoes do vault com `templates/licoes.md`. **Nunca edite as skills nem o contexto do projeto por conta propria:** o usuario decide.

## Relatorio final

Uma mensagem curta ao usuario:

- PR(s): URL e titulo;
- CI: verde | falhou (motivo) | sem CI;
- Atencao: quantidade de itens (ou "nada");
- Sugestoes para o projeto: quantidade (ou "nenhuma");
- Licoes registradas: quantidade (ou "nenhuma");
- lembrete: o merge e do usuario; depois do merge, o orquestrador chama o `/task-close <nota>`, ou uma rotina agendada fecha a task.

A ultima linha da resposta e `RESULTADO: ship concluido - PR <url>` (com dois PRs, as duas URLs).
