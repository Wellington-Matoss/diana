---
name: task-close
description: Fecha tasks cujo PR ja foi mergeado - atualiza a documentacao de arquitetura para o estado atual, trata decisoes superadas, debitos e pendencias residuais, marca a task como concluida e arquiva a nota. Sem argumento, varre todas as tasks em revisao (serve para rotina agendada).
argument-hint: <caminho da nota> (vazio = varrer todas as tasks em-revisao)
disable-model-invocation: true
---

# Task Close

Roda **depois do merge**. A documentacao passa a descrever o codigo que esta na base, entao so faz sentido com o PR mergeado. Autonomo: aplica as mudancas no vault (reversiveis pelo git) e relata o que fez.

## Quando parar

Siga "Quando parar", "Saida de toda parada" e "Reentrada" de `../task-comum/regras.md`, inclusive o paragrafo do Close. No Close, o caso 7 aparece no passo 1 (consulta do PR sem autenticacao) e o caso 8, no passo 6. PR ainda aberto nao e parada.

## Contexto do projeto

Memoria do agente e `CLAUDE.md`: onde ficam as notas de arquitetura, as decisoes, a lista de debitos tecnicos e a pasta de tasks concluidas; regras e verificacao automatica do vault (se houver).

## 0. Escolher as tasks

- Com argumento: so aquela nota. Ela precisa estar `em-revisao` (ou vir do Ship de um repositorio sem PR). Senao, caso 0.
- Sem argumento: todas as notas com `status: em-revisao`.
- Task de repositorio sem PR (chamada pelo orquestrador logo apos o Ship publicar): pule o passo 1 e feche direto; no Resultado, "publicada no commit <hash>" no lugar do PR.
- Sincronize o vault.

## 1. Conferir o PR

Para cada task, consulte cada PR da nota (`gh pr view <url> --json state,mergedAt,baseRefName`):

| Estado                  | Acao                                                                          |
| ----------------------- | ----------------------------------------------------------------------------- |
| todos mergeados         | fechar (passos 2 a 6)                                                         |
| algum aberto            | pular: ainda em revisao (nao e parada)                                        |
| algum fechado sem merge | `status: pausada`, registrar "PR #n fechado sem merge em <data>" e nao fechar |

## 2. Atualizar a documentacao de arquitetura

- So as notas de arquitetura que a task afetou.
- Descreva **como o sistema e hoje**, nao o historico ("na task X adicionamos..." fica na nota da task).
- Acrescente o que e novo (modulo, rota, modelo, convencao) e corrija o que ficou desatualizado. Nao reescreva a nota inteira.
- Mapas ou indices que o projeto usa como gabarito de revisao (ex.: pontos de log ou auditoria): atualize se a task mexeu neles.

## 3. Decisoes

- Decisao de arquitetura nova ja foi registrada no Plan ou no Design (criterio das tres condicoes), com o usuario presente. Se a task gerou uma decisao que nao foi registrada, **nao crie a nota de decisao**: decisao nova so nasce com OK do usuario. Liste no relatorio como **proposta** (titulo, contexto em uma linha, por que cumpre as tres condicoes).
- Decisao antiga que a task mudou: acrescente logo abaixo do titulo dela um aviso `> [!info] Ampliada/Superada em parte por [[<task>]]`, com o que continua valendo. Superada por inteiro: tambem `status: substituida`. Nao reescreva o corpo.

## 4. Debitos e pendencias

- **Debito resolvido pela task:** apague a linha da lista de debitos (em todas as secoes em que aparece). Nao risque, nao marque "resolvido". O registro fica na nota da task.
- **Pendencia residual** (item de "Atencao" nao resolvido, roteiro manual pendente, sugestao para o projeto aceita no PR): cada uma vira **linha na lista de debitos**, com link para a task e natureza (pendente | a validar | aceito). Se ja existe task ou item no roadmap para ela, so faca referencia.
- Siga as regras de formato da lista de debitos do projeto (ex.: contagem no titulo da secao).

## 5. Fechar a nota

- Frontmatter: `status: concluida`, `concluida_em: <data>`, `atualizado`.
- Escreva a linha `close` no "Registro de etapas", no formato do template da spec (`merge em <AAAA-MM-DD|sem pr>`, debitos criados e removidos no passo 4).
- Secao `## Resultado`: o que ficou pronto, PRs e data do merge, pendencias residuais e para onde foram. **Fato que nao envelhece:** "PR #12 mergeado em develop em 22/11/2026". Nada de "aguardar", "pendente de merge" ou proximo passo numa task concluida; sem proximo passo, escreva "nenhum - task concluida".
- Mova a nota para a pasta de tasks concluidas do projeto (se o projeto separa por pasta).

## 6. Conferir e sincronizar

- Rode a verificacao automatica do vault do projeto, se houver. Erro numa nota que este fechamento tocou: caso 8 para essa task, sem sincronizar a nota com erro. Erro em nota alheia: so relate.
- Sincronize o vault (commit `<ID>: concluida`).

## Relatorio

Por task: fechada | ainda em revisao | pausada (PR fechado sem merge) | parada (caso e motivo). Para as fechadas: notas de documentacao alteradas, debitos removidos e criados, resultado da verificacao do vault, commit do vault. Por ultimo, se houver: **decisoes propostas** aguardando o OK do usuario.

A ultima linha da resposta e a linha de resultado do Close, no formato de `../task-comum/regras.md`.
