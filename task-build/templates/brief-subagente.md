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
3. Fim da etapa: suite verde -> commit local no padrao `tipo(escopo): assunto` com rodape `Task: <ID>` (ver `task-ship/referencias/commits.md`). Fix: o teste vermelho e um commit `test(...)`, a correcao e um commit `fix(...)` com a causa no corpo.
4. Regras do tipo <tipo>: <linha da tabela "Por tipo" do SKILL.md>

## Desvios
- Nao muda forma, interface nem plano de testes: faca e registre no relatorio.
- Muda forma, interface ou plano de testes: escolha a opcao mais conservadora, faca, registre com o motivo e marque ATENCAO.
- Teste do plano parece errado: NAO altere. Pare a etapa e reporte.

## Pare e reporte se
- cumprir um criterio exige mudar escopo ou produto;
- o passo nao tem volta (dado real, branch protegida, apagar dados);
- ha ambiguidade de seguranca ou permissao;
- o mesmo erro persiste apos 2 tentativas.

## Relatorio (formato obrigatorio)
Por etapa:
- Etapa <n>: <feita | parcial | nao feita>
- Commit: <hash>
- Testes: <nome> | vermelho: <trecho da saida> | verde: <trecho da saida>
- Sem teste automatizado: <o que e por que>
- Desvios: <lista ou "nenhum">; ATENCAO: <lista ou "nenhum">
Final: comando e saida da suite completa, do lint e do build.
```
