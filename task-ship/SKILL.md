---
name: task-ship
description: Estagio 5 (Ship) do fluxo Plan > Design > Build > Verify > Ship. De forma autonoma - confere o estado da branch, integra a base, atualiza o changelog do projeto (se houver), faz push, abre o PR no padrao do fluxo (sem merge), acompanha o CI quando o projeto tem, marca a task como em revisao e registra licoes do processo. O merge e sempre do usuario.
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
- **Nada de segredo no diff.** Encontrou: pare.
- **O PR e para o usuario ler em um minuto.** Sem preambulo, sem repetir o que o diff ja mostra.
- **Nenhum passo some em silencio:** `skip: <motivo>`.

## Quando parar

Pare, registre `status: bloqueada` com o motivo e informe o usuario **somente** se:

1. o diff contem segredo, credencial, `.env` ou dado de cliente;
2. o push ou o PR exigiria acao sem volta ou em branch protegida, ou a autenticacao do `git`/`gh` nao esta disponivel;
3. a integracao da base gera conflito na logica da task (nao mecanico);
4. o CI falha pelo diff apos 3 rodadas de correcao.

## Contexto do projeto

Leia da memoria do agente e do `CLAUDE.md`: branch base do PR; idioma das mensagens; se ha changelog para o usuario final, onde fica, formato e regras de curadoria; se ha CI; repositorios separados.

## 0. Conferir a entrada

- Sem argumento: resolva a task ativa como no Build.
- A nota precisa ter `estagio: verify` concluido, sem bloqueante aberto. Senao, pare: o Verify nao aprovou.
- Crie a lista de tarefas com os passos 1 a 8.

## 1. Conferir o estado

1. Branch atual nao e protegida.
2. `git status` limpo: nada fora dos commits da task.
3. O diff (`git diff <base>...HEAD`) so tem arquivos da task. Arquivo nao relacionado: remova do diff com um commit `chore: remove alteracao fora do escopo` e registre.
4. Procure segredos no diff: `.env`, chave, token, certificado, senha, dado pessoal. Encontrou: caso 1.

## 2. Integrar a base

1. `git fetch` e confira se a branch esta atras da base.
2. Atras: faca merge da base na branch (nao rebase: preserva os commits ja verificados).
3. Conflito **mecanico** (lockfile, import, formatacao, arquivos independentes): resolva. Conflito na **logica** da task: caso 3.
4. Houve merge da base: rode de novo testes, lint e build. Vermelho: volte ao Build com o erro (uma rodada); persistindo, caso 3.

## 3. Changelog do projeto (se houver)

Se o contexto do projeto define um changelog para o usuario final:

- Uma linha, em linguagem do usuario final: o que ele percebe de diferente. Nada de detalhe tecnico.
- Use o formato, as secoes e as regras de curadoria do projeto (ex.: o que entra so no changelog interno).
- Commit: `docs(changelog): <assunto>`.

Sem changelog no projeto: `skip: projeto sem changelog`.

## 4. Push

`git push -u origin <branch>`. Task em dois repositorios: push nos dois.

## 5. Abrir o PR

1. **Titulo:** `tipo(escopo): assunto` (`referencias/commits.md`). No merge com squash, o titulo vira a mensagem do commit na base.
2. **Corpo:** `templates/pr.md`, com o conteudo do Verify (resumo do diff, evidencia, Atencao, sugestoes) e do Build (desvios). Ate ~40 linhas. Secao vazia sai, exceto "Atencao", que mostra "Nada." quando vazia.
3. Abra **pronto para revisao** (nao rascunho), para a base do projeto: `gh pr create --base <base> --head <branch> --title "<titulo>" --body-file <arquivo>`.
4. Dois repositorios: abra os dois PRs e coloque o link de um no outro.
5. **Nao faca merge.**

## 6. Acompanhar o CI (se houver)

Projeto sem CI: `skip: projeto sem CI`.

1. Espere os checks terminarem (`gh pr checks <pr> --watch`).
2. Verde: siga.
3. Falha **causada pelo diff**: leia o primeiro erro acionavel no log, dispare um subagente do Build com o erro, commit, push, espere de novo. Maximo 3 rodadas; depois, caso 4.
4. Falha **nao causada pelo diff** (instabilidade, infraestrutura, falha que ja existe na base): rode de novo uma vez. Persistindo: comente no PR com a evidencia e acrescente em "Atencao".
5. Nunca mude o esperado de um teste para o CI passar.

## 7. Atualizar a nota

- Frontmatter: `status: em-revisao`, `estagio: ship`, `atualizado`, `pr: [<url>, ...]`.
- Secao `## Entrega`: branch, PRs (URL), estado do CI, changelog (se houve). Escreva como fato: "PR #12 aberto para develop".
- "Registro de etapas": `ship: concluido em <data>. Skips: <lista>`.
- Sincronize o vault.

## 8. Licoes do processo

Leia o "Registro de etapas", a Execucao e a Verificacao da nota. **Registre so se algo aconteceu.** Nada aconteceu: `skip: sem licoes` (o resultado esperado na maioria das tasks).

Conta como licao:

- rodada de volta ao Build (por que o Build nao pegou antes?);
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
- lembrete: o merge e do usuario; depois do merge, `/task-close` (ou a rotina agendada) fecha a task.
