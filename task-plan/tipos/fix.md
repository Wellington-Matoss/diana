# Tipo: fix

Comportamento errado que ja existe. O Plan prova que o bug existe, qual e o sintoma exato e qual e a causa. A correcao e decidida no Design.

## Definicao de pronto

- O sintoma exato do usuario reproduz (vermelho) antes da correcao e nao reproduz (verde) depois.
- Formato dos criterios:
  - `Quando <condicao que dispara o bug>, entao <comportamento correto>.`
  - `O comando <comando de reproducao> passa de vermelho para verde.`
- Acrescente ao menos um criterio de nao regressao do comportamento vizinho.
- Das 5 categorias, use as que o bug toca (ex.: bug de concorrencia -> repeticao; bug de permissao -> acesso indevido). As outras: `nao se aplica - <motivo>`.
- Contrato: so o que a correcao muda no que outra parte enxerga (ex.: codigo de erro novo). Correcao que nao muda nada visivel alem do sintoma: `C1. Nada muda alem do comportamento das frases.`

## Investigacao (passo 3)

1. **Monte o ciclo de feedback antes de qualquer hipotese.** O ciclo e um comando que:
   - [ ] voce ja rodou ao menos uma vez (mostre o comando e a saida);
   - [ ] reproduz o **sintoma exato** que o usuario descreveu, nao um erro parecido;
   - [ ] da o mesmo resultado a cada execucao (para bug intermitente: taxa de reproducao alta e conhecida);
   - [ ] roda em segundos;
   - [ ] roda sem humano.

   Opcoes, nesta ordem: teste que falha; script HTTP contra o servidor local; chamada de CLI com entrada fixa; script de navegador; reproducao de payload capturado; harness minimo; bisseccao (`git bisect run`) quando o bug surgiu entre dois estados conhecidos.

   Se nao conseguir montar o ciclo: pare. Liste o que tentou. Peca ao usuario acesso ao ambiente que reproduz, um artefato capturado (log, HAR) ou permissao para instrumentar. **Sem ciclo, sem hipotese.**
2. **Minimize:** reduza a reproducao ao menor cenario que ainda falha. Corte um elemento por vez e rode o ciclo de novo.
3. **Encontre a causa:** liste as hipoteses. Elimine cada uma com evidencia de execucao (log, instrumentacao, teste). Comece pela hipotese que elimina mais espaco do problema. Para regressao, use o historico ("por que e assim") para achar a mudanca que introduziu o bug.
4. **Registre na nota:** comando de reproducao, saida antes, causa confirmada e evidencia, hipoteses descartadas.

Os artefatos de investigacao ficam numa pasta descartavel da task (ver contexto do projeto). Nao entram no commit. O Design decide se o teste de reproducao vira o primeiro teste do Build.

**Segredos:** antes de mostrar saida de comando, troque segredos e dados de cliente por `<REDACTED>`.

## Excecao: fix focado

Pode reduzir a entrevista a uma rodada e o teach-back a uma pergunta quando **todas** as condicoes forem verdadeiras:

- A evidencia de execucao mostra a causa em um subsistema so.
- A correcao nao muda assinatura, schema, permissao, seguranca, concorrencia ou contrato de API.
- Existe um ciclo de feedback barato que cobre a falha.
- Nao ha design concorrente nem evidencia contraditoria.

Registre na nota a evidencia de cada condicao. Se uma condicao falhar depois, volte ao fluxo completo. Tamanho do patch sozinho nunca justifica a excecao.

## Se a causa nao for encontrada

Mude o tipo para `investigacao`. O resultado do Plan passa a ser o que foi descoberto e o proximo passo de investigacao.
