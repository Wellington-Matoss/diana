# Regras comuns do fluxo

Regras que valem para Build, Verify e Ship. Cada regra fica so aqui. As skills citam este arquivo e acrescentam so o que e proprio do estagio. Esta pasta nao e skill: nao tem `SKILL.md` e vai junto na instalacao.

## Quando parar

Do Build ao Ship, o agente nao pergunta: decide, registra o motivo e segue. Ele para **somente** nos casos abaixo.

**Casos comuns:**

| Caso | Nome          | Quando                                                                                                                                         |
| ---- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| 0    | entrada       | o passo 0 (conferencia de entrada) reprova: nota errada ou ambigua, estagio anterior nao concluido, dependencia nao concluida, branch errada |
| 1    | o que         | cumprir uma frase da Definicao de pronto exige mudar **um item do Contrato, o escopo ou o produto**                                           |
| 2    | sem volta     | o proximo passo nao tem volta: alterar dado real, escrever em branch protegida, force push, apagar dados                                      |
| 3    | seguranca     | ha duvida de seguranca ou permissao (autenticacao, autorizacao, segredo, dado de cliente) que nenhuma decisao registrada resolve              |
| 4    | tentativas    | o problema persiste depois do limite da tabela "Limites de tentativas" (codigo, ambiente, credencial, dependencia quebrada)                    |

**Casos proprios do estagio:**

| Caso | Estagio | Quando                                                                       |
| ---- | ------- | ---------------------------------------------------------------------------- |
| 5    | Ship    | o diff contem segredo, credencial, `.env` ou dado de cliente                 |
| 6    | Ship    | integrar a base gera conflito na logica da task (conflito mecanico nao conta) |
| 7    | Ship    | a autenticacao para push, PR ou publicacao nao esta disponivel, ou a ferramenta de publicacao recusa |

Todo o resto: escolha a opcao mais conservadora, registre o motivo e siga. O que precisa do olho do humano, mas nao justifica parar, vai para a Atencao do PR.

## Limites de tentativas

Uma tentativa e uma correcao completa (ver "Correcao por subagente"). Passou do limite e o problema continua: caso 4.

| Estagio | O que conta                                                            | Limite                                      |
| ------- | ---------------------------------------------------------------------- | ------------------------------------------- |
| Build   | rodada de correcao depois da conferencia do lider (passo 4)            | 2                                           |
| Build   | o mesmo erro dentro do subagente, numa rodada                          | 2 (o subagente para e reporta ao lider)    |
| Build   | bloqueio de ambiente (credencial, dependencia, servico local)          | 2                                           |
| Verify  | correcao por subagente dos bloqueantes                                 | 2                                           |
| Ship    | correcao por subagente depois de integrar a base (teste, lint ou build vermelho) | 1                                 |
| Ship    | correcao por subagente de CI vermelho causado pelo diff                | 3                                           |
| Ship    | CI vermelho nao causado pelo diff                                      | 1 nova execucao; depois, Atencao (nao para) |

Cada linha conta separado. Na segunda rodada do Build e da correcao por subagente, vale a regra de modelo do passo 2 do Build.

## Saida de toda parada

Toda parada termina com uma linha de resultado. Nenhuma parada fica sem ela.

1. Nota escolhida: marque `status: bloqueada` e `atualizado`. Registre o caso e o motivo na secao do estagio (`Execucao`, `Verificacao` ou `Entrega`), numa linha `Parada: caso <n> - <motivo>`.
2. Nao mude `estagio`: ele diz o ultimo estagio concluido. Quem diz qual estagio parou e a linha `Parada`, junto com `status: bloqueada` e a linha de resultado.
3. Nao escreva a linha do estagio no "Registro de etapas": ela so nasce quando o estagio conclui.
4. Parada depois do passo 0: registre na secao do estagio o que ja foi feito (no Build: as etapas conferidas, com o commit). A retomada parte dai.
5. Sincronize o vault.
6. A ultima linha da resposta e:

```text
RESULTADO: <build|verify|ship> bloqueada - caso <n> (<nome>): <motivo em uma linha>
```

Sem nota escolhida (passo 0 sem argumento e mais de uma candidata): nao altere nenhuma nota. Liste as candidatas no motivo: `RESULTADO: build bloqueada - caso 0 (entrada): nota ambigua: <nota 1>, <nota 2>`.

O estagio que conclui encerra com `RESULTADO: <estagio> concluido - <resumo>`, no formato do passo final da skill.

## Reentrada depois de `bloqueada`

| Caso                         | Quem resolve                                                                                                                                                                                                                       | Quem roda de novo                                                                                    |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 1 (o que)                    | o humano roda `/task-plan <nota>` com o orquestrador. O Plan retoma a **mesma** nota e atualiza Contrato, Definicao de pronto e o que for preciso. Depois o humano roda `/task-design <nota>`, que revisa o Design e pede a aprovacao de novo | o Build, na mesma branch, a partir da ultima etapa concluida                                         |
| demais (0, 2, 3, 4, 5, 6, 7) | o humano resolve (ambiente, permissao, conflito, entrada) e marca `status: ativa`                                                                                                                                                   | o orquestrador roda de novo o **mesmo** estagio que parou                                            |

Regras da retomada:

- O estagio que parou encontra a nota com o `estagio` do estagio anterior e `status: ativa`: e a entrada normal do passo 0.
- O Verify e o Ship retomados leem a propria secao (`Verificacao` ou `Entrega`, com a linha `Parada`) para saber o que ja foi feito.
- O estagio reescreve a propria linha do "Registro de etapas" quando conclui.
- O Build retomado nao recria a branch e nao refaz etapa ja commitada e conferida na Execucao. Etapa que o Design reaprovado mudou conta como nao feita.

## Correcao por subagente

Problema de **como** (bloqueante do Verify, vermelho depois de integrar a base, CI vermelho pelo diff) nao volta ao estagio anterior. O estagio que achou o problema corrige ali mesmo:

1. Dispare um **subagente novo** com o brief do Build (`../task-build/templates/brief-subagente.md`) e a lista objetiva do problema. Nao continue um subagente anterior.
2. Confira a correcao como no passo 4 do Build: testes do plano intactos; rode de novo testes, lint e build e compare com a linha de base.
3. Aplique a limpeza (b) de `../task-build/referencias/limpeza.md` sobre o diff da correcao.
4. Cada commit da correcao tem o rodape `Task: <ID>` (`../task-ship/referencias/commits.md`).
5. Confira de novo so o que motivou a correcao.

Cada correcao conta uma tentativa na tabela de limites.

## Sem subagente

Se nao for possivel disparar subagente, quem dispararia faz o trabalho ele mesmo, numa passagem separada:

- releia do zero so o brief e as fontes que ele aponta. Nao use conclusao de passagem anterior;
- a conferencia continua igual, como se o trabalho fosse de outro: rode de novo testes, lint e build e compare com o plano;
- a reprovacao vira uma nova passagem, com o brief original + a lista objetiva do que falhou;
- registre o desvio "sem subagente" na nota.

Vale para Build, Verify e Ship. Cada skill acrescenta so o que e proprio dela.
