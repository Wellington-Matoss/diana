# Brief do subagente (modelo)

O lider preenche e envia. Ponteiros, nao copias. Todo `<caminho>` e preenchido pelo lider com o caminho absoluto: o subagente nao resolve caminho relativo a skill. Isso vale tambem para o arquivo de regras comuns (`task-comum/regras.md`, ao lado da pasta desta skill).

Dois modos: **etapas** (o Build, passo 3) e **correcao** ("Correcao por subagente" de `task-comum/regras.md`, no Verify ou no Ship).

## Modo etapas

```markdown
Voce implementa a task <ID> - <nome curto>.

## Fontes (leia antes de comecar)
- Nota da task: <caminho>. Leia: Definicao de pronto, Design (Forma, Plano de testes, Etapas).
- Regras de TDD: <caminho>/referencias/tdd.md
- Contexto do projeto: <CLAUDE.md do subprojeto>, <guia de testes do subprojeto>
- Comandos: teste `<cmd>`, lint `<cmd>`, build `<cmd>`
- Linha de base (falhas pre-existentes, nao sao suas): <lista ou "nenhuma">

## Branch
<nome da branch> em <repositorio(s)>. Nao troque de branch. Nao faca push.

## O que fazer
1. Siga as etapas do Design na ordem.
2. Para cada teste planejado da etapa: escreva o teste -> veja falhar pelo motivo certo -> codigo minimo -> veja passar. Guarde as duas saidas.
3. Fim da etapa: suite verde -> commit local no padrao `tipo(escopo): assunto` com rodape `Task: <ID>` (ver `task-ship/referencias/commits.md`). Fix: o teste de reproducao e um commit `test(...)` antes da correcao, vermelho (com hook que roda testes, marcado como falha esperada); a correcao e um commit `fix(...)` com a causa no corpo, a suite verde e o teste sem a marca.
4. Regras do tipo <tipo>: <linha da tabela "Por tipo" do SKILL.md>

## Desvios
- Fora do Contrato (forma, nomes, arquivos, divisao das etapas): decida, faca e registre no relatorio com o motivo.
- Muda um item do Contrato (rota, formato, status, campo gravado, permissao, log): NAO faca. Pare a etapa e reporte.
- Teste planejado impraticavel: use a verificacao executavel mais proxima, registre e marque ATENCAO.
- Bug real fora do escopo: falha esperada, conforme `referencias/tdd.md`. Registre no relatorio.
- Teste do plano parece errado: NAO altere. Pare a etapa e reporte.
- A etapa le dado ja gravado e a Definicao de pronto nao tem frase para dado fora do padrao: NAO decida o comportamento. Registre no relatorio como ATENCAO: "dado gravado fora do padrao sem frase na Definicao de pronto".

## Pare e reporte se
- ocorrer um dos casos 1, 2 ou 3 de "Quando parar" em <caminho absoluto de task-comum/regras.md>;
- o mesmo erro persistir alem do limite do subagente (nota "Erro dentro do subagente" do mesmo arquivo).

## Relatorio (formato obrigatorio)
Por etapa:
- Etapa <n>: <feita | parcial | nao feita>
- Commit: <hash>
- Testes: <nome> | vermelho: <trecho da saida> | verde: <trecho da saida>
- Sem teste automatizado: <o que e por que>
- Desvios: <lista ou "nenhum">; falhas esperadas: <lista ou "nenhuma">; ATENCAO: <lista ou "nenhum">
Final: comando e saida da suite completa, do lint e do build.
```

## Modo correcao

Curto. O problema ja existe; o subagente so corrige.

```markdown
Voce corrige um problema da task <ID> - <nome curto>.

## Problema (objetivo)
<achado CONFIRMADO do Verify, com a prova | primeiro erro acionavel do CI | saida vermelha de teste, lint ou build depois de integrar a base>

## Fontes
- Nota da task: <caminho>. Leia: Definicao de pronto, Contrato, Design.
- Diff atual da task: <caminho do arquivo com `diff <base>...HEAD`>
- Regras de TDD: <caminho>/referencias/tdd.md
- Regras comuns: <caminho absoluto de task-comum/regras.md>
- Comandos: teste `<cmd>`, lint `<cmd>`, build `<cmd>`

## Branch
<nome da branch> em <repositorio(s)>. Nao troque de branch. Nao faca push.

## O que fazer
1. Problema de comportamento: escreva antes um **teste de regressao** e veja falhar pelo motivo certo. Titulo: a frase da Definicao de pronto que o problema quebra + " - regressao". Sem frase que cubra o problema: o titulo descreve o achado. Registre o teste como desvio no relatorio.
2. Faca a correcao minima e veja a suite verde.
3. Commit local `tipo(escopo): assunto` com rodape `Task: <ID>`.

## Nao faca
- Nao mude item do Contrato nem teste do plano (esperado, assercao, skip). Se a correcao exigir: pare e reporte (caso 1).
- Nao corrija nada fora do problema.

## Pare e reporte se
- ocorrer um dos casos 1, 2 ou 3 de "Quando parar" nas regras comuns;
- o mesmo erro persistir alem do limite do subagente (nota "Erro dentro do subagente").

## Relatorio
- Problema: <corrigido | nao corrigido>
- Commit: <hash>
- Teste de regressao: <titulo> | vermelho: <trecho> | verde: <trecho> (ou "nao se aplica - <motivo>")
- Desvios: <lista>
Final: comando e saida da suite completa, do lint e do build.
```
