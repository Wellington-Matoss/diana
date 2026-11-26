---
name: task-design
description: Estagio 2 (Design) do fluxo Plan > Design > Build > Verify > Ship. Define COMO construir uma task ja planejada - resolve perguntas abertas com prototipo descartavel, nomeia, escolhe a forma do codigo entre duas alternativas, define o plano de testes e as etapas. Termina com uma aprovacao do usuario. Nao escreve codigo de producao.
argument-hint: <caminho da nota da task no vault>
disable-model-invocation: true
---

# Task Design

Voce conduz o **Design**: definir a estrutura antes da implementacao. A entrada e a nota da task que saiu do `/task-plan`. A saida e a secao `## Design` dessa nota, aprovada pelo usuario, que o `/task-build` executa.

```
Nota (plan concluido) -> 1 Ler -> 2 Prototipar -> 3 Nomear -> 4 Dar forma -> 5 Plano de testes -> 6 Etapas -> 7 Aprovar
                                   (so se houver    (glossario   (2 formas,     (1 teste por        (<=7, cada
                                    pergunta)        -> codigo)   escolher 1)    criterio)           uma verde)
```

## Principios

- **O Plan decidiu O QUE. O Design decide COMO.** Se o Design mostrar que o Plan esta errado (criterio impossivel, escopo grande demais, pergunta de produto que ninguem decidiu), pare e volte ao `/task-plan`. Nao corrija o Plan em silencio.
- **O Contrato e fixo.** A forma do codigo pode ser qualquer uma que cumpra o Contrato e as frases. Mudar um item do Contrato e mudar o QUE: so com o OK do humano, na propria nota. Marque o item `(alterado em AAAA-MM-DD no Design, aprovado por <humano>)`, atualize as frases e o Plano de testes que dependem dele e siga as regras do Contrato do passo 5 do `/task-plan` e, se o item tira ou muda um campo, "Consumidores do campo" do passo 3.
- **Os fatos sao seus. As decisoes sao do usuario.** Mesma regra do Plan.
- **Nao escreva codigo de producao.** Prototipo e codigo descartavel, em branch descartavel. Trecho curto de tipo ou assinatura na nota e permitido quando descreve a decisao melhor que texto.
- **Siga o precedente.** Se o projeto ja resolve algo parecido, use o mesmo padrao, a menos que haja motivo registrado para nao usar.
- **Nenhum passo some em silencio.** Passo que nao se aplica fica como `skip: <motivo>`.

## Skills e referencias de apoio

- `referencias/vocabulario.md`: termos para discutir forma (modulo, interface, seam, profundidade). Leia antes do passo 4.
- `referencias/prototipo-ui.md` e `referencias/prototipo-logica.md`: passo 2.
- `referencias/design-duas-vezes.md`: passo 4, so para decisao sem volta.
- `templates/design.md`: estrutura da secao `## Design`.
- Contexto do projeto (caminhos, convencoes, comandos de teste): memoria do agente e `CLAUDE.md`.
- Sincronizacao do vault e sintaxe Obsidian: as mesmas skills de ferramenta do `/task-plan`.

## 0. Conferir a entrada e abrir a lista de tarefas

Pare e explique o motivo se:

- a nota nao tem `estagio: plan` concluido ou o teach-back nao foi confirmado -> `/task-plan`;
- `tamanho` e `epico` ou `mapa` -> o Design e feito em cada nota-filha com `tamanho: task`;
- `tipo: investigacao` -> nao ha Design;
- alguma nota de `depende-de` nao esta `concluida` -> avise e pergunte se continua.

Crie a lista de tarefas com os passos 1 a 7.

## 1. Ler a nota

- Esta sessao pode continuar a conversa do Plan (task pequena) ou ser nova. Em sessao nova, a nota e a unica fonte: leia a nota, o glossario e o `CLAUDE.md` do subprojeto.
- Confira se a nota ainda e verdadeira: veja os commits nos arquivos citados desde a data do Plan. Se algo mudou, registre e avalie se afeta a task.
- Nota que ja tem Design aprovado e voltou do Plan (reentrada do caso 1 de `../task-comum/regras.md`): revise a secao existente, nao recomece. Marque cada etapa que mudou com `[alterada em AAAA-MM-DD]`, no formato de `templates/design.md`, e peca a aprovacao de novo (passo 7). O que o Build refaz: "Build retomado" em `../task-comum/regras.md`.
- Liste as "Perguntas em aberto" que o Design precisa resolver.

## 2. Prototipar (so se houver pergunta)

Prototipo existe para responder **uma pergunta**. Sem pergunta, `skip: sem pergunta aberta`.

| Pergunta                                                    | Ramo                                         | Referencia                        |
| ----------------------------------------------------------- | -------------------------------------------- | --------------------------------- |
| "Como deve parecer?" (tela, layout, densidade)              | UI                                           | `referencias/prototipo-ui.md`     |
| "Essa regra ou esse modelo de estados aguenta os casos?"    | Logica                                       | `referencias/prototipo-logica.md` |
| "Qual opcao e mais rapida ou funciona com essa biblioteca?" | Script minimo que mede ou mostra o resultado | -                                 |

- Ajuste pequeno de tela: um mockup unico basta (`skip: ajuste pequeno, mockup unico`).
- O prototipo fica na branch `prototype/<ID>`. Nunca na main. Nunca vira codigo de producao direto: o Build reescreve.
- Registre na nota: pergunta, variantes, escolha e motivo, link da branch.
- Escolha de produto ou preferencia: e do usuario. Mostre as variantes e espere.

## 3. Nomear

- Leve os termos do glossario para nomes no codigo: tipos, funcoes, rotas, colecoes, componentes.
- Siga a convencao de nomes que o projeto ja usa.
- Termo novo do dominio que nao esta no glossario: proponha a definicao, confirme com o usuario e atualize o glossario.
- Um conceito, um nome. Nao use dois nomes para a mesma coisa.

## 4. Dar forma

Leia `referencias/vocabulario.md`.

1. **Rastreie** os modulos e sistemas que a mudanca toca.
2. **Nomeie a forma dos dados primeiro** (tipo, estrutura, maquina de estados, tabela). Regra espalhada em varios `if` e sinal de estrutura que falta.
3. **Esboce duas formas** diferentes: tipos, assinaturas, onde fica cada modulo, onde ficam os seams. Pode ser em texto curto ou trecho de assinatura.
4. **Escolha** a forma em que:
   - cada estado tem um dono so;
   - cada tarefa tem um jeito so de ser feita;
   - o chamador precisa saber o minimo (interface pequena, modulo profundo);
   - o teste passa pela mesma interface que o chamador usa.

   Aplique o teste da exclusao a cada modulo novo: se apagar o modulo e a complexidade sumir, ele e so repasse. Remova.

5. **Decisao sem volta** (schema, contrato de API usado por outro sistema, dono de um dado, migracao): use `referencias/design-duas-vezes.md` em vez de esbocar sozinho.
6. Registre a forma escolhida e a descartada, com o motivo em uma linha.

## 5. Plano de testes

1. **Escolha os seams de teste:** prefira os que ja existem; teste no nivel mais alto possivel; quanto menos seams, melhor (o ideal e um).
2. **Um teste por frase da Definicao de pronto, com o titulo igual a frase.** Para cada frase: nivel (unidade, integracao, e2e), seam, dado de entrada. Frase `nao se aplica` nao gera teste. Item do Contrato que nenhuma frase cobre (ex.: log gerado, campo gravado): acrescente a verificacao a frase mais proxima ou um teste proprio.
3. **Teste comportamento, nao implementacao:** o teste verifica o que o chamador observa. Ele quebra quando o comportamento quebra e continua passando quando so o interno muda.
4. **Comprovacao no app:** para cada criterio, uma linha de como o Verify vai comprovar no aplicativo real (tela, acao, resultado esperado).
5. Ajuste por tipo:

| Tipo        | Regra do plano de testes                                                                                                                                                           |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| fix         | O teste de reproducao do Plan e o primeiro teste. Decida se o script de `.scratch` vira teste definitivo ou se o teste e reescrito no seam certo. Inclua o teste de nao regressao. |
| refatoracao | A trava de comportamento (teste de caracterizacao, snapshot ou comparacao antigo x novo) e a etapa 1, antes de qualquer mudanca de estrutura. Os testes existentes nao mudam.      |
| feature     | Um teste por criterio "quando/entao", incluindo erro e permissao. Siga o padrao de teste do precedente.                                                                            |

## 6. Etapas

- **No maximo 7 etapas de trabalho.** Se precisar de mais, a task e grande demais: volte ao `/task-plan` e divida em epico.
- Ordem:
  1. remocao de codigo morto e refatoracao previa ("torne a mudanca facil, depois faca a mudanca facil"). No fix: a refatoracao previa (se houver, com a suite verde), depois o teste de reproducao (vermelho de proposito), depois a correcao. Na refatoracao, a etapa 1 e a trava (tabela do passo 5);
  2. a parte de maior risco ou incerteza;
  3. o resto.
- Cada etapa diz: **o que muda**, **onde** (modulos), **qual teste fica verde** ao fim dela.
- **Changelog:** se o tipo da mudanca entra no changelog do projeto (contexto do projeto), a ultima etapa e o bullet, sem teste: uma linha para o usuario final, no formato do projeto, commit `docs(changelog): <assunto>`. A etapa diz: conferencia no Verify.
- Cada etapa termina com a suite verde (excecao: o commit do teste de reproducao no fix, ver "Por tipo" do /task-build). Teste, lint e build nao sao etapas separadas: fazem parte de cada etapa.
- Etapa bem escrita e uma instrucao clara para o subagente do Build.

## 7. Escrever e aprovar

1. Preencha a secao `## Design` da nota com `templates/design.md`.
2. **Decisao de arquitetura:** so se for dificil de reverter, surpreendente sem contexto e resultado de um trade-off real. Ela entra na aprovacao unica (passo 3) e so e registrada no vault com o OK do usuario. Senao, fica so na nota.
3. **Aprovacao unica.** Numa mensagem so, mostre:
   - forma escolhida e forma descartada (2-4 linhas);
   - tabela do plano de testes;
   - lista de etapas;
   - prototipos e escolhas (se houver);
   - decisao de arquitetura proposta (se houver).

   Pergunte: "Aprova forma, testes e etapas?". Ajuste ate aprovar.

4. Atualize o frontmatter: `estagio: design`, `atualizado`. Escreva a linha `design` no "Registro de etapas", no formato do template da spec.
5. Sincronize o vault.

## Escala

Fix focado ou ajuste pequeno: passo 2 `skip`; passo 4 com uma forma so e o motivo de nao haver alternativa; Design inteiro em poucas linhas. O tamanho do Design acompanha o risco, nao a vontade de documentar.

## Criterio de saida e handoff

- [ ] Perguntas em aberto do Plan resolvidas ou registradas como fora do escopo.
- [ ] Forma escolhida e descartada registradas.
- [ ] Todo criterio de pronto tem teste e comprovacao no app.
- [ ] Etapas (<=7) com o teste que fica verde em cada uma.
- [ ] Aprovacao do usuario.
- [ ] Vault sincronizado.

Esta e a **ultima aprovacao do usuario antes do PR**. Diga isso na mensagem de aprovacao do passo 7.

Proximo passo: **`/task-build <nota>`**, em **sessao nova**. A nota e o handoff: o Build nao precisa desta conversa. Do Build em diante o fluxo segue sem o usuario: o orquestrador chama Build -> Verify -> Ship, um estagio por sessao, ate abrir o PR.
