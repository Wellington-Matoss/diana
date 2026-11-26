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

<Detalhe para o agente e para consulta: fluxo com arquivos, rotas e models reais; cada componente e por que existe; o que o historico explica; itens "a validar". Regra ou valor do Contrato: cite o item (`ver C3`), nao repita.>

### Prova com dado real
<um dos tres:
- **Fonte** · **Consulta** (em palavras, sem dado pessoal) · **Resultado** (so agregado: contagem, minimo, mediana, maximo) · **Efeito no plano** (o que mudou, ou "nada");
- `nao se aplica - <motivo>`;
- `prova indisponivel - <motivo>`.>

## Definicao de pronto
<frases `quando ..., entao ...`, uma por teste; ajuste do arquivo de tipo. Categoria sem uso: `nao se aplica - <motivo>`.>
- **Feliz:**
  - [ ] Quando ..., entao ...
- **Erro esperado:**
  - [ ] Quando ..., entao ...
- **Repeticao:**
  - [ ] Quando ..., entao ...
- **Limite:**
  - [ ] Quando ..., entao ...
- **Acesso indevido:**
  - [ ] Quando ..., entao ...

## Contrato
<o que outra parte do sistema, o banco ou o usuario enxerga e fica fixo. Mudar = mudar o QUE (o agente para). Fora daqui, tudo e sugestao. Ate 5 sub-regras por item.>
- **C1.** ...

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
<uma linha por estagio, neste formato exato (separador " · "), para leitura por script. Ao rodar de novo, o estagio reescreve a propria linha.>
- plan: concluido em <AAAA-MM-DD> · tipo <tipo> · tamanho <tamanho> · prova <feita|nao se aplica|indisponivel> · skips: <lista ou nenhum>
- design: concluido em <AAAA-MM-DD> · prototipos <N> · etapas <N> · skips: <lista ou nenhum>
- build: concluido em <AAAA-MM-DD> · modelo <sonnet|opus|fable|haiku|sessao> · rodadas <N> · desvios <N> · falhas esperadas <N> · skips: <lista ou nenhum>
- verify: concluido em <AAAA-MM-DD> · modo <leve|completo> · rodadas <N> · bloqueantes <N> · atencao <N> · candidatos <N> · refutados <N> · skips: <lista ou nenhum>
- ship: concluido em <AAAA-MM-DD> · ci <verde|falhou|sem ci> · licoes <N> · skips: <lista ou nenhum>
- close: concluido em <AAAA-MM-DD> · merge em <AAAA-MM-DD|sem pr> · debitos criados <N> · debitos removidos <N> · skips: <lista ou nenhum>
