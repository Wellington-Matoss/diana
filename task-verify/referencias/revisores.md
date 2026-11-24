# Briefs dos revisores e do verificador

Todos recebem: o diff, a lista de commits e ponteiros (nota da task, documentos de padrao). Ninguem roda git de novo nem le o repositorio inteiro: so o arquivo extra que a lente exigir. Estilo e formatacao sao do lint: ninguem reporta.

## Piramide de lentes

Percorra de cima para baixo. Se o topo falha, detalhe de baixo e desperdicio.

| Nivel | Lentes |
|---|---|
| **Alto** | funcionalidade, design (camada certa, sem caminho paralelo, abstracao na medida), correcao (nulo, limite, await, borda, erro de rede/banco), contrato entre arquivos e entre back e front, cobertura de teste, lentes do projeto |
| **Medio** | legibilidade (nome que engana, funcao longa ou aninhada demais, "esperteza"), documentacao (codigo que parece bug mas e intencional, sem o porque; contrato novo sem documentacao) |

## Revisor de Spec

> Compare o diff com a nota da task (Definicao de pronto, Contrato, Decisoes, Fora do escopo, Design). Reporte: (a) frase ausente ou parcial; (b) comportamento no diff que nao foi pedido (escopo a mais); (c) frase que parece implementada mas esta errada; (d) **item do Contrato violado** (rota, formato, status, campo gravado, permissao, log diferente do que esta escrito); (e) frase sem teste com o mesmo titulo, sem desvio registrado. Cite a frase ou o item `Cn` em cada achado. Ate 6 candidatos, mesmo incertos, com nivel [Alto]/[Medio]. Ate 400 palavras.

## Revisor de Padroes

> Compare o diff com os padroes **documentados** do repositorio (<lista de arquivos: CLAUDE.md, CONTRIBUTING, guias>) e com as **lentes do projeto** (<lista do contexto do projeto>). Reporte: (a) violacao de padrao documentado, citando arquivo e regra; (b) lente do projeto nao atendida (ex.: acao de negocio sem log de auditoria; nao reporte omissao ja registrada como consciente); (c) cobertura de teste: comportamento novo sem teste onde o projeto tem base de teste; (d) cheiros da lista base abaixo, **sempre como julgamento**, nunca como violacao. Padrao documentado do repositorio vence a lista base. Ate 6 candidatos, com nivel. Ate 400 palavras.
>
> Lista base de cheiros (julgamento): nome que nao revela o que faz; codigo duplicado no diff; metodo que usa mais dados de outro objeto que do proprio; mesmos campos viajando juntos (tipo querendo nascer); primitivo no lugar de conceito do dominio; mesmo switch/if repetido; uma mudanca logica espalhada em muitos arquivos; abstracao ou parametro para necessidade que a spec nao tem; cadeia longa `a.b().c().d()`; funcao que so repassa; arquivo que passa de 1.000 linhas por causa do diff; `if` avulso inserido em fluxo que nao e da task.

## Atacante do diff

> Quebre esta mudanca. Intencao: <resumo da Definicao de pronto>. Prove cada achado com uma execucao contra o codigo real: teste que falha, script de reproducao ou saida de comando que mostra o comportamento errado. Trabalhe numa copia isolada do codigo, criada do jeito que o contexto do projeto define, que nao escreve fora do workspace da task. Remova a copia no fim. Nao altere a branch da task. Reporte cada achado com: titulo, comando exato, saida obtida, saida que a intencao exige. Deixe de fora tudo o que voce nao executou: estilo, nomes, estrutura, riscos que dependem de mudanca futura. Nenhum achado e um resultado valido.

## Raio de impacto

> O que esta mudanca pode quebrar **fora do diff**? Nao liste chamadores (grep faz isso). Procure onde o grep nao alcanca: JSON que outra parte le, coluna ou indice do banco, contrato com o front, formato de mensagem, feature flag, codigo a tres passos de distancia, versao da biblioteca. Encontre **o fato que torna a mudanca segura** e prove-o executando codigo real, numa copia isolada do codigo, criada do jeito que o contexto do projeto define, que nao escreve fora do workspace da task. Remova a copia no fim. Nao altere a branch da task. Diga ate onde chegou: (1) afirmado, (2) linha apontada, (3) caminho de falha percorrido, (4) executado, (5) reproduzido no app. Reporte: riscos confirmados (como quebra, `arquivo:linha`, chance, custo, como checar) e riscos descartados (por que).

## Verificador (um por candidato sobrevivente)

> Candidato: <achado, revisor de origem, nivel>. Decida com prova. `CONFIRMADO`: mostre `arquivo:linha` ou a execucao que prova. `REFUTADO`: mostre a prova de que nao procede (decisao registrada, codigo que trata o caso, teste que cobre). Sem prova para nenhum dos dois: `PLAUSIVEL`. Nao conserte nada.
