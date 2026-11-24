# Brief do subagente (modelo)

O lider preenche e envia. Ponteiros, nao copias.

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
- cumprir uma frase exige mudar um item do Contrato, o escopo ou o produto;
- o passo nao tem volta (dado real, branch protegida, apagar dados);
- ha ambiguidade de seguranca ou permissao;
- o mesmo erro persiste apos 2 tentativas.

## Relatorio (formato obrigatorio)
Por etapa:
- Etapa <n>: <feita | parcial | nao feita>
- Commit: <hash>
- Testes: <nome> | vermelho: <trecho da saida> | verde: <trecho da saida>
- Sem teste automatizado: <o que e por que>
- Desvios: <lista ou "nenhum">; falhas esperadas: <lista ou "nenhuma">; ATENCAO: <lista ou "nenhum">
Final: comando e saida da suite completa, do lint e do build.
```
