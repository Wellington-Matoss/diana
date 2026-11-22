# Tamanho: epico

O caminho esta claro, mas o trabalho nao cabe em uma task. O epico e uma **nota-mae** com a spec do todo e **notas-filhas**, uma por fatia.

## Passos

1. Escreva a spec do todo na nota-mae (passo 7 do SKILL.md, com `tamanho: epico`).
2. **Refatoracao previa:** se uma mudanca de estrutura facilita o resto, ela e a primeira fatia. "Torne a mudanca facil, depois faca a mudanca facil."
3. **Divida em fatias verticais:**
   - Cada fatia atravessa todas as camadas necessarias (banco, API, tela, testes). Nao divida por camada ("primeiro o back, depois o front").
   - Cada fatia pode ser demonstrada ou verificada sozinha.
   - Cada fatia cabe em uma sessao do agente.
   - Cada fatia declara de quais fatias depende.
4. **Excecao, refatoracao ampla:** uma mudanca mecanica que quebra muitos pontos de uma vez (renomear coluna, trocar tipo compartilhado) segue a sequencia:
   1. **Expandir:** acrescente a forma nova ao lado da antiga. Nada quebra.
   2. **Migrar em lotes:** um lote por pacote ou pasta. Cada lote depende do expandir.
   3. **Contrair:** remova a forma antiga. Depende de todos os lotes.
5. **Mostre a divisao ao usuario** em lista numerada:
   - **Titulo**
   - **Depende de**
   - **O que entrega** (comportamento de ponta a ponta)

   Pergunte: a granularidade esta certa? As dependencias estao certas? Alguma fatia deve ser unida ou dividida? Repita ate aprovar.
6. **Crie as notas-filhas** a partir de `templates/spec.md`, na ordem das dependencias (as que nao dependem de nada primeiro):
   - `tamanho: task`, `pai: [[<nota-mae>]]`, `depende-de: [[<notas>]]` (vazio se nenhuma).
   - "Objetivo" = o que a fatia entrega. Criterios de aceite proprios da fatia.
   - Nao copie decisoes da nota-mae. Faca link.
7. Na nota-mae, liste as filhas com o que cada uma entrega.

## Fronteira

Uma fatia esta livre para comecar quando todas as notas de `depende-de` estao `concluida`. Sugira uma view na `Tasks.base` que mostra so as fatias livres.

Cada fatia passa pelo `/task-design` individualmente. Nao faca o Design de todas de uma vez.
