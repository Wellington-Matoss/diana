# Regras comuns do fluxo

Regras que valem para os estagios que rodam sem o humano: Build, Verify, Ship e Close. Cada regra fica so aqui. As skills citam este arquivo e acrescentam so o que e proprio do estagio. Esta pasta nao e skill: nao tem `SKILL.md` e vai junto na instalacao.

## Quando parar

Nesses estagios, o agente nao pergunta: decide, registra o motivo e segue. Ele para **somente** nos casos abaixo.

**Casos comuns:**

| Caso | Nome       | Quando                                                                                                                                                          |
| ---- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0    | entrada    | o passo 0 (conferencia de entrada) reprova: nenhuma nota candidata, nota ambigua, estagio anterior nao concluido, dependencia nao concluida, branch errada |
| 1    | o que      | cumprir uma frase da Definicao de pronto exige mudar **um item do Contrato, o escopo ou o produto**                                                            |
| 2    | sem volta  | o proximo passo nao tem volta: alterar dado real, escrever em branch protegida, force push, apagar dados                                                       |
| 3    | seguranca ou permissao | ha duvida de seguranca ou permissao (autenticacao, autorizacao, acesso a dado) que nenhuma decisao registrada resolve, ou o ambiente negou uma permissao      |
| 4    | tentativas | o problema persiste depois do limite da tabela "Limites de tentativas"                                                                                         |

**Casos proprios do estagio:**

| Caso | Nome             | Estagio      | Quando                                                                                                         |
| ---- | ---------------- | ------------ | -------------------------------------------------------------------------------------------------------------- |
| 5    | segredo          | Ship         | o diff contem segredo ou dado pessoal                                                                          |
| 6    | conflito na base | Ship         | integrar a base ou publicar direto gera conflito na logica da task (conflito mecanico nao conta)              |
| 7    | autenticacao     | Ship e Close | a autenticacao para push, PR, consulta do PR ou publicacao nao esta disponivel, ou a ferramenta de publicacao recusa |
| 8    | vault com erro   | Close        | a verificacao automatica do vault continua com erro numa nota que o Close tocou, depois do limite de tentativas |

**Permissao negada pelo ambiente.** Sem humano na sessao, ninguem aprova uma permissao. Comando, pasta ou rede negados pelo ambiente param na hora, no caso 3, com o comando negado no motivo. Nao conta como tentativa de correcao e nao se tenta de novo.

Todo o resto: escolha a opcao mais conservadora, registre o motivo e siga. O que precisa do olho do humano, mas nao justifica parar, vai para a Atencao do PR.

## Limites de tentativas

A unidade e a **tentativa de correcao**: uma correcao completa, conferida (ver "Correcao por subagente"; no Build, o passo 4; no Close, o passo 6). Cada linha conta separado. Passou do limite e o problema continua: caso 4, exceto na linha do Close, que leva ao caso 8.

| Estagio | Tentativa de correcao                                                 | Limite |
| ------- | --------------------------------------------------------------------- | ------ |
| Build   | nova passagem do subagente depois de uma reprovacao do lider (passo 4) | 2      |
| Build   | correcao de bloqueio de ambiente (credencial, dependencia, servico local) | 2   |
| Verify  | correcao por subagente dos bloqueantes                                | 2      |
| Ship    | correcao por subagente depois de integrar a base                      | 1      |
| Ship    | correcao por subagente de CI vermelho causado pelo diff ou de pedido de mudanca no PR | 3 |
| Close   | correcao das proprias edicoes depois de erro da verificacao do vault numa nota que o Close tocou | 2 |

**Modelo:** a segunda tentativa de correcao usa o modelo forte da tabela de modelo do Build (passo 2).

Notas (nao sao linhas da tabela):

- **Erro dentro do subagente:** o subagente tenta o mesmo erro no maximo 2 vezes e devolve o relatorio. Isso faz parte da tentativa do lider, nao e tentativa propria.
- **CI vermelho nao causado pelo diff** (instabilidade, infraestrutura, falha que ja existe na base): uma nova execucao. Persistindo, vai para a Atencao do PR. Nao e tentativa de correcao e nao para.

## Saida de toda parada

Toda parada termina com uma linha de resultado. Nenhuma parada fica sem ela.

1. Nota escolhida: marque `status: bloqueada` e `atualizado`. Registre o caso e o motivo na secao do estagio (`Execucao`, `Verificacao`, `Entrega` ou `Resultado`), numa linha `Parada: caso <n> - <motivo>`.
2. Nao mude `estagio`: ele diz o ultimo estagio concluido. Quem diz qual estagio parou e a linha `Parada`, junto com `status: bloqueada` e a linha de resultado.
3. Nao escreva a linha do estagio no "Registro de etapas": ela so nasce quando o estagio conclui.
4. Parada depois do passo 0: registre na secao do estagio o que ja foi feito (no Build: as etapas conferidas, com o commit). A retomada parte dai.
5. Sincronize o vault, exceto no caso 8 (nao sincronize nota com erro).
6. A ultima linha da resposta e:

```text
RESULTADO: <build|verify|ship|close> bloqueada - caso <n> (<nome>): <motivo em uma linha>
```

Caso 0 por estagio anterior nao concluido: nao altere a nota. Ela pode estar no meio de outro estagio.

Build, Verify e Ship sem nota escolhida (passo 0 sem argumento, nenhuma candidata ou mais de uma): nao altere nenhuma nota. Liste as candidatas no motivo, ou diga que nao ha nenhuma: `RESULTADO: build bloqueada - caso 0 (entrada): nota ambigua: <nota 1>, <nota 2>`.

O estagio que conclui encerra com `RESULTADO: <estagio> concluido - <resumo>`, no formato do passo final da skill.

**Close:** sem argumento, ele varre todas as notas `em-revisao` e fecha as que estiverem prontas. Zero ou varias notas e o normal: nao e caso 0. Uma parada vale so para a task em que ocorreu; o Close segue com as outras. PR ainda aberto nao e parada: a task fica "ainda em revisao". A linha final e uma destas:

```text
RESULTADO: close concluido - nenhuma task em revisao
RESULTADO: close concluido - fechadas <N>, em revisao <N>, pausadas <N>
RESULTADO: close bloqueada - fechadas <N>, em revisao <N>, pausadas <N>, paradas <N>: <ID> caso <n> (<nome>); <ID> caso <n> (<nome>)
```

## Reentrada depois de `bloqueada`

| Caso                       | Quem resolve                                                                                                                                                                                                                    | Quem roda de novo                                                     |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| 0, nota ambigua ou ausente | o humano indica a nota                                                                                                                                                                                                          | o orquestrador roda o mesmo estagio, com a nota como argumento        |
| 0, estagio anterior nao concluido | ninguem: a nota nao foi alterada                                                                                                                                                                                         | o orquestrador roda o estagio anterior; se ele e Plan ou Design, chama o humano. O Close so roda depois do merge |
| 0, demais (dependencia, branch) | o humano resolve e marca `status: ativa`                                                                                                                                                                                    | o mesmo estagio                                                       |
| 1 (o que)                  | o humano roda `/task-plan <nota>` com o orquestrador. O Plan retoma a **mesma** nota e atualiza Contrato, Definicao de pronto e o que for preciso. Depois o humano roda `/task-design <nota>`, que revisa o Design e pede a aprovacao de novo | o Build, na mesma branch (ver "Regras da retomada")                   |
| 2 a 7                      | o humano resolve (ambiente, permissao, conflito) e marca `status: ativa` (no Close, `status: em-revisao`)                                                                                                                       | o mesmo estagio que parou                                             |
| 8 (Close)                  | o Close ja desfez o fechamento (passo 6 do `/task-close`): a nota voltou a pasta e ao estado de antes, com `status: bloqueada`. O humano corrige o vault e marca `status: em-revisao`                                              | o orquestrador ou a rotina agendada roda o Close                       |

Regras da retomada:

- O estagio que parou encontra a nota com o `estagio` do estagio anterior e `status: ativa`: e a entrada normal do passo 0.
- **Verify e Ship sem mudanca de codigo** (casos 2 a 8): leem a propria secao (`Verificacao` ou `Entrega`, com a linha `Parada`) para saber o que ja foi feito.
- **Verify e Ship com codigo novo** (depois do caso 1, ou com commit da task posterior a propria secao): rodam inteiros, do zero. Renomeie a secao antiga para `### Verificacao anterior (<AAAA-MM-DD>)` ou `### Entrega anterior (<AAAA-MM-DD>)` e nao a use como trabalho feito: e historico.
- O estagio reescreve a propria linha do "Registro de etapas" quando conclui.
- **Build retomado:** nao recria a branch. Depois do caso 1, refaz cada etapa marcada como alterada no Design (`[alterada em AAAA-MM-DD]`) e todas as que vem depois dela; as anteriores ficam. Os commits novos vao por cima, sem reescrever o historico, e a Execucao e reescrita para essas etapas. Ao terminar de refazer, remove as marcas `[alterada em ...]` da lista de Etapas: o registro fica na Execucao, e uma parada posterior nao refaz as mesmas etapas. Nos demais casos (nenhuma etapa marcada), parte da primeira etapa sem commit conferido na Execucao.

## Correcao por subagente

Problema de **como** (bloqueante do Verify, vermelho depois de integrar a base, CI vermelho pelo diff, pedido de mudanca no PR aberto) nao volta ao estagio anterior. O estagio que achou o problema corrige ali mesmo:

1. Dispare um **subagente novo** com o brief do Build no **modo correcao** (`../task-build/templates/brief-subagente.md`). Nao continue um subagente anterior.
2. Confira a correcao como no passo 4 do Build: testes do plano intactos; rode de novo testes, lint e build e compare com a linha de base. Registre o teste de regressao do relatorio na secao "Desvios" do Design (titulo: modo correcao do brief).
3. Aplique a limpeza (b) de `../task-build/referencias/limpeza.md` sobre o diff da correcao.
4. **Ataque a correcao:** rode o Atacante do diff sobre o diff da correcao, com o brief de `../task-verify/referencias/revisores.md`, numa copia isolada (ver "Copia isolada" do `/task-verify` passo 3). No Ship, isso vem antes do push. Achado provado por execucao: nova tentativa de correcao.
5. Cada commit da correcao tem o rodape `Task: <ID>` ("Conferencia do rodape" de `../task-ship/referencias/commits.md`).
6. Confira de novo so o que motivou a correcao.

Cada correcao conta uma tentativa na tabela de limites.

## Sem subagente

Se nao for possivel disparar subagente, quem dispararia faz o trabalho ele mesmo, numa passagem separada:

- releia do zero so o brief e as fontes que ele aponta. Nao use conclusao de passagem anterior;
- a conferencia continua igual, como se o trabalho fosse de outro: rode de novo testes, lint e build e compare com o plano;
- a reprovacao vira uma nova passagem, com o brief original + a lista objetiva do que falhou;
- registre o desvio "sem subagente" na nota.

Vale para Build, Verify e Ship. Cada skill acrescenta so o que e proprio dela.
