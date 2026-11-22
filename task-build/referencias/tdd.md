# TDD: o ciclo

O titulo de cada teste e a **frase da Definicao de pronto**, igual: `quando ..., entao ...`.

Para **cada teste** do plano de testes da etapa, nesta ordem:

1. **Escreva um teste.** So um. Ele descreve o comportamento do criterio de pronto. O valor esperado vem da spec ou de um exemplo conhecido, nunca do codigo.
2. **Rode e veja falhar pelo motivo certo.** Leia a mensagem de falha. Ela precisa mostrar o sintoma esperado (ex.: "esperado alerta, recebido sem alerta"). Falha por erro de importacao, sintaxe ou funcao inexistente **nao conta**: ajuste ate a falha ser o sintoma. Guarde a saida (vai para o relatorio).
3. **Escreva o minimo de codigo** para esse teste passar. Nada de refatorar ou "aproveitar para melhorar" nesta hora.
4. **Rode e veja passar.** Guarde a saida.
5. Rode a suite do modulo. Tudo verde: proximo teste.

Ao fim da etapa: suite completa verde + type check (se houver) -> commit local.

Se o teste ja passa no passo 2 (ex.: teste de nao regressao do comportamento vizinho), registre "verde de inicio: protege comportamento existente" e siga.

## O que um bom teste e

- Passa pela **interface publica** (o mesmo seam que o chamador usa), nunca por funcao privada ou detalhe interno.
- Quebra quando o comportamento quebra. Continua passando quando so o interno muda.
- Le como uma especificacao: o nome diz qual capacidade existe ("gera alerta quando a leitura e igual ao limite").
- Uma ideia por teste.

## Anti-padroes (proibidos)

- **Todos os testes primeiro, todo o codigo depois.** Um teste, um codigo, repete.
- **Teste preso a implementacao:** mock de colaborador interno, teste de metodo privado, verificacao por canal lateral (consultar o banco em vez de usar a interface).
- **Teste tautologico:** o esperado e calculado do mesmo jeito que o codigo (`expect(soma(a, b)).toBe(a + b)`). Ele passa por construcao.
- **Mudar o teste para casar com o codigo errado.** Teste do plano errado: pare a etapa e reporte ao lider.
- **Enfraquecer assercao** ou marcar teste como `skip`/`only`/`todo` para a suite ficar verde.

## Mock

So na **fronteira do sistema**:
- envio de e-mail, SMS, mensageria;
- API de terceiros;
- relogio e aleatoriedade (para o teste ser deterministico).

**Banco:** use o banco de teste do projeto, conforme o guia de testes do projeto. Nao faca mock do banco se o projeto tem banco de teste.

**Nunca** faca mock do proprio codigo (services, utils, modulos internos).

## Bug real fora do escopo: falha esperada

Se um teste (novo ou existente) falha por um **bug real que nao e desta task**:

- **Nao corrija** (o escopo cresceria) e **nao altere nem pule** o teste.
- Marque o teste como **falha esperada** no recurso do framework (ex.: `test.fails` no Vitest, `xfail` no pytest), com um comentario apontando a linha nos debitos do projeto.
- Acrescente a linha na lista de debitos do projeto (secao de bugs conhecidos, se houver), com link para a task.
- A falha esperada passa enquanto o bug existe e **quebra quando alguem o corrige**: quem corrigir troca por teste normal e apaga a linha do debito.
- Bug dentro do escopo da task: corrija na task.

## Quando o teste e impraticavel

Se o teste planejado exige infraestrutura cara, mock fragil, estado que so existe em producao ou fixture enorme: nao force. **Melhor nenhum teste novo do que um teste ruim.** Use a verificacao executavel mais proxima (script, comando de reproducao, automacao de navegador) e registre como desvio com o motivo.
