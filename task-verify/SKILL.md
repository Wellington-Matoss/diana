---
name: task-verify
description: Estagio 4 (Verify) do fluxo Plan > Design > Build > Verify > Ship. Portao unico que pode reprovar o trabalho, de forma autonoma - roda testes e lint, comprova cada criterio no app real, revisa em paralelo (spec, padroes, ataque ao diff, raio de impacto), separa quem acha de quem julga, classifica os achados, devolve bloqueantes ao Build e encerra com uma linha de resultado; o orquestrador chama o /task-ship.
argument-hint: <caminho da nota da task no vault> (vazio = resolver a task ativa)
disable-model-invocation: true
---

# Task Verify

Voce e o **portao** entre o codigo e o PR. E o unico estagio que reprova. O fluxo continua **autonomo**: voce nao pergunta ao usuario; decide, prova e registra. O usuario le o resultado no PR.

```
Nota (build concluido) -> 1 Preparar -> 2 App real -> 3 Revisar (paralelo) -> 4 Julgar -> 5 Classificar -> 6 Registrar -> RESULTADO
                          (testes,      (portao)    (spec, padroes,          (provar     (bloqueante volta
                           lint)                     ataque, raio)            ou cair)    ao Build)
```

## Principios

- **"Compila" nao e evidencia.** Prove no artefato real.
- **Quem acha nao julga. Quem julga precisa provar.** Revisores listam candidatos (recall). Um verificador separado confirma cada um com prova (precisao).
- **Os dois eixos ficam separados:** codigo que segue os padroes mas faz a coisa errada passa num eixo e falha no outro. Nao misture nem reordene os relatorios.
- **O usuario so le o que precisa dele.** Anotacao, cheiro de codigo e achado refutado ficam na nota, nao no PR.
- **Nao amplie o escopo.** Melhoria fora da task nao e aplicada: vira sugestao.

## Quando parar

Siga "Quando parar", "Limites de tentativas" e "Saida de toda parada" de `../task-comum/regras.md`. O Verify nao tem caso proprio.

No Verify, o caso 1 aparece quando corrigir um bloqueante exige mudar um item do Contrato, o escopo ou o produto. O caso 4 aparece quando o mesmo bloqueante persiste depois do limite da correcao por subagente.

## Contexto do projeto

Leia da memoria do agente e do `CLAUDE.md`: comandos de teste e lint; branch base; documentos de padrao do repositorio; **lentes proprias do projeto** (ex.: "acao de negocio precisa gerar log de auditoria"); skill `verify` do projeto e ambiente de verificacao; lista de debitos tecnicos.

## 0. Conferir a entrada

Toda parada deste passo e o caso 0 de `../task-comum/regras.md`, com a linha de resultado.

- Sem argumento: resolva a task ativa como no Build.
- A nota precisa ter `estagio: build` concluido. Senao, pare: o Build nao terminou.
- Crie a lista de tarefas com os passos 1 a 6.

## 1. Preparar

1. Leia a nota: Definicao de pronto, Contrato, Decisoes, Design (inclusive "Comprovacao no app" e "Desvios"), Execucao.
2. Pegue o diff contra a branch base **uma vez** (`git diff <base>...HEAD`) e a lista de commits. Passe esse diff aos revisores; eles nao rodam git de novo. Repositorio sem PR (ver o contexto do projeto): o diff e o das mudancas nao commitadas dos arquivos listados na Execucao (`git diff` mais o conteudo dos arquivos novos).
3. Rode a suite de testes e o lint. Lint: erro nos arquivos do diff, e aviso **so em linha que o diff alterou**. Teste vermelho ou lint novo = **bloqueante** (passo 5). Nao siga para o passo 2 com teste vermelho.

## 2. Comprovar no app real (portao)

Siga `referencias/app-real.md`.

- Para cada criterio de pronto, use a linha "Comprovacao no app" do Design e a skill `verify` do projeto.
- Resultado por criterio: `comprovado` | `falhou` | `nao comprovado` (com o motivo), mais a evidencia.
- `falhou` = bloqueante. Nao gaste revisao: va direto ao passo 5.
- `nao comprovado` porque o projeto nao tem skill `verify` ou o caminho nao e alcancavel: nao bloqueia. Vira item de "Atencao" com o roteiro manual pronto.
- A task produziu um numero (tempo, throughput, tamanho)? Aplique as perguntas de numeros de `referencias/app-real.md`.

## 3. Revisar em paralelo

Dispare os revisores **ao mesmo tempo**, cada um em contexto limpo, com os briefs de `referencias/revisores.md`. Eles recebem o diff, a lista de commits e ponteiros (nota, documentos de padrao). Cada um devolve **candidatos**, mesmo incertos, com o nivel da piramide.

| Revisor                            | Sempre?                                                                                      | Modelo                                  |
| ---------------------------------- | -------------------------------------------------------------------------------------------- | --------------------------------------- |
| Spec                               | sim                                                                                          | Sonnet                                  |
| Padroes (inclui lentes do projeto) | sim                                                                                          | Sonnet                                  |
| Ataque ao diff                     | sim                                                                                          | Sonnet; no modo completo, Opus + Sonnet |
| Raio de impacto                    | so se o diff toca modulo compartilhado, contrato de API, schema, configuracao ou dependencia | Sonnet                                  |

**Modo completo** (escolha sozinho e registre o motivo): diff grande, ou area sensivel (autenticacao, permissao, pagamento, migracao, dados de cliente).

**Copia isolada.** Revisor ou verificador que executa codigo trabalha numa copia isolada do codigo. Ninguem altera a branch da task.

1. **Onde:** nunca no clone principal do repositorio nem no workspace de outra frente. Padrao: pasta temporaria do sistema ou da sessao, fora de qualquer repositorio. Dentro do workspace da task, o lint e o test runner leem a copia como parte do projeto, e a copia herda a configuracao da pasta de cima. O contexto do projeto pode definir outro jeito.
2. **Criar:** copie o codigo no commit da task e instale as dependencias. A instalacao faz parte de criar a copia. Se ela ficar cara num projeto, um jeito mais barato e decisao do contexto do projeto.
3. **Conferir antes de atacar:** rode na copia, sem nenhuma mudanca, os testes e o lint. O resultado precisa reproduzir a linha de base: os mesmos testes passando e os mesmos apontamentos de lint do passo 1 no workspace da task (a linha de base do Build mais o que a task mudou). Se nao reproduzir, o problema e a copia (configuracao, dependencias, caminho), nao o codigo: aplique "confira o metodo de observacao" de `referencias/app-real.md`. Nenhum achado tirado da copia vale ate ela reproduzir a linha de base.
4. **Remover e registrar:** remova toda copia ate o fim do Verify. Registre na nota o local, o resultado da conferencia e a remocao.

**Sem subagente.** Siga "Sem subagente" de `../task-comum/regras.md`. No Verify, rode cada revisor deste passo e cada verificador do passo 4 numa passagem separada, em sequencia. Cada passagem rele do zero so o brief de `referencias/revisores.md`, o diff e a nota. O verificador nao reaproveita o raciocinio de quem achou o candidato. No modo completo, acrescente aos candidatos a Atencao: "revisao sem contexto separado". A volta ao Build do passo 5 segue "Sem subagente" do `/task-build` passo 3.

## 4. Julgar

1. **Deduplique** os candidatos dos revisores.
2. **Refute de graca** (voce, sem agente) o que contradiz uma decisao registrada na nota ou um desvio ja registrado. Guarde o motivo.
3. Para cada sobrevivente, dispare um **verificador** (contexto limpo, Sonnet; Opus para seguranca ou dados) com o brief de `referencias/revisores.md`. Veredito: `CONFIRMADO` (com prova: `arquivo:linha` ou execucao), `REFUTADO` (com prova), ou `PLAUSIVEL` (sem prova).
4. Achado do ataque ao diff so existe se veio com execucao que mostra a falha.

## 5. Classificar

| Categoria                   | O que entra                                                                                                                                                                                                                                                                    | Destino                                    |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------ |
| **Bloqueante**              | teste vermelho; lint novo; criterio que falhou no app; requisito da spec ausente, parcial ou errado (CONFIRMADO); **item do Contrato violado** (CONFIRMADO); frase sem teste e sem desvio registrado; bug provado por execucao; violacao CONFIRMADA de padrao documentado do repositorio | volta ao Build                             |
| **Atencao**                 | precisa de decisao do usuario ou ele precisa saber antes do merge: criterio `nao comprovado`; frase sem teste automatizado (desvio registrado); falha esperada nova; risco de seguranca ou dados PLAUSIVEL; decisao de dominio (ex.: lint que pode ser regra de negocio); escopo a mais no diff | PR (maximo 5; o excedente vai para a nota) |
| **Nota**                    | cheiro de codigo, legibilidade, documentacao, achado `[Medio]` sem risco concreto, PLAUSIVEL de baixo risco, refutados com a prova                                                                                                                                             | so a nota                                  |
| **Sugestao para o projeto** | melhoria **sistemica** com beneficio claro (ver criterios abaixo)                                                                                                                                                                                                              | PR (maximo 3) + nota                       |

**Bloqueante:** dispare um subagente novo do Build (`/task-build` passo 3, brief original + lista objetiva dos bloqueantes). Depois, rode de novo os passos 1 e 2 e verifique de novo so os bloqueantes. Maximo 2 rodadas; depois, caso 4 de "Quando parar".

**Sugestao para o projeto:** **"nenhuma" e o resultado esperado na maioria das tasks.** Nao procure sugestao e nao invente: ela so existe se apareceu durante a revisao. O maximo de 3 e um teto, nao uma meta. Na duvida, nao sugira. So entra se todas forem verdadeiras:

- o padrao se repete no projeto (cite ao menos 2 lugares), nao e caso isolado da task;
- o beneficio e concreto: evita uma classe de bug, torna os testes confiaveis, remove trabalho repetido ou complexidade relevante. Ganho marginal nao entra;
- ha evidencia (`arquivo:linha`, execucao ou documentacao oficial);
- nao esta na lista de debitos tecnicos nem foi sugerida antes (procure no vault).

Formato: problema, onde aparece, proposta, beneficio, esforco estimado (P/M/G).

## 6. Registrar e seguir

1. Preencha a secao `## Verificacao` da nota com `templates/verificacao.md`.
2. Se o codigo divergiu do Entendimento ou do Design, atualize o **Entendimento** para refletir o que foi construido.
3. Escreva o **resumo do diff para o PR** (ate ~100 palavras, sem `arquivo:linha`): o que mudou (comportamento), onde mexeu (por area), o que divergiu do plano e por que, ou "nada divergiu".
4. Frontmatter: `estagio: verify`, `atualizado`. Escreva a linha `verify` no "Registro de etapas", no formato do template da spec. `candidatos` e o total depois da deduplicacao; `refutados` sai desse total.
5. Sincronize o vault.
6. **Encerre com a linha de resultado.** A ultima linha da resposta e `RESULTADO: verify concluido - <bloqueantes corrigidos N, atencao N>`. Nao chame o `/task-ship`: as skills do fluxo so rodam quando chamadas de fora. O orquestrador le essa linha e o estado da nota e chama o proximo estagio.
