---
id: <PREFIXO-NNN>
status: ativa            # ativa | aguardando | bloqueada | em-revisao | pausada | concluida
tipo: <fix|feature|refatoracao|investigacao|docs|infra|decisao>
tamanho: <task|epico|mapa>
estagio: plan            # plan | design | build | verify | ship
pr: []                   # URLs dos PRs (preenchido pelo /task-ship)
subprojeto: <nome>       # lista YAML se tocar mais de um
pai:                     # [[nota-mae]] se for fatia de epico ou decisao de mapa
depende-de: []           # [[notas]] que precisam estar concluidas antes
atualizado: <AAAA-MM-DD>
resumo: <1 linha para a Base>
tags: [task]
---

# <ID> - <nome curto>

## Objetivo
<problema e resultado esperado, na visao de quem pediu. Origem da demanda.>

## Entendimento
<Resumo em 1 minuto do teach-back (problema, onde encaixa, o que muda, caminho descartado).>

<Detalhe para o agente e para consulta: fluxo com arquivos, rotas e models reais; cada componente e por que existe; o que o historico explica; itens "a validar".>

## Definicao de pronto
<formato do arquivo de tipo>
- [ ] Quando ..., entao ...
- [ ] Quando ..., entao ...

## Decisoes
- <decisao> - <motivo em uma linha>

## Fora do escopo
- <item> - <motivo> <link para nova nota, se houver>

## Perguntas em aberto
<nao bloqueantes; o Design resolve ou ficam para depois>

## Evidencias da investigacao
<fix: comando de reproducao, saida antes, causa e evidencia, hipoteses descartadas>
<refatoracao: contrato, cobertura, estrutura que falta>
<fatos externos: conclusao + fonte>

## Design
<preenchido pelo /task-design>

## Registro de etapas
- plan: concluido em <AAAA-MM-DD>. Skips: <lista de `skip: motivo`, ou "nenhum">
