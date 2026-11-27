# Tamanho: epico

O caminho esta claro, mas o trabalho nao cabe em uma task. O epico e uma **nota-mae** com a spec do todo e **notas-filhas**, uma por fatia.

## Passos

1. Escreva a spec do todo na nota-mae (passo 7 do SKILL.md, com `tamanho: epico`).
2. **Refatoracao previa:** se uma mudanca de estrutura facilita o resto, ela e a primeira fatia. "Torne a mudanca facil, depois faca a mudanca facil."
3. **Divida em fatias verticais:**
   - Cada fatia atravessa todas as camadas necessarias (banco, API, tela, testes). Nao divida por camada ("primeiro o back, depois o front").
   - Cada fatia pode ser demonstrada ou verificada sozinha.
   - Cada fatia cabe em uma sessao do agente.
   - Cada fatia declara de quais fatias depende e o esforco estimado (P/M/G).
4. **Excecao, refatoracao ampla:** uma mudanca mecanica que quebra muitos pontos de uma vez (renomear coluna, trocar tipo compartilhado) segue a sequencia:
   1. **Expandir:** acrescente a forma nova ao lado da antiga. Nada quebra.
   2. **Migrar em lotes:** um lote por pacote ou pasta. Cada lote depende do expandir.
   3. **Contrair:** remova a forma antiga. Depende de todos os lotes.
5. **Mostre a divisao ao usuario como mapa em ondas:**
   - **Ondas:** a onda 1 tem as fatias sem dependencia. Uma fatia fica na onda seguinte a mais tardia das que ela precisa. Fatias da mesma onda podem rodar em paralelo.
   - **Por fatia:** titulo; esforco; depende de (e por que); por que existe (o que fica faltando sem ela); o que entrega (comportamento de ponta a ponta).
   - **Caminho critico:** a cadeia de dependencias com maior esforco somado (P=1, M=2, G=3). Atraso nela atrasa o epico.
   - **Formato:** o do contexto do projeto (pagina, diagrama). Sem ele, uma lista agrupada por onda.

   Pergunte: a granularidade esta certa? As dependencias estao certas? Alguma fatia deve ser unida ou dividida? Da para tirar alguma fatia do caminho critico? Repita ate aprovar.
6. **Crie as notas-filhas** a partir de `templates/spec.md`, na ordem das dependencias (as que nao dependem de nada primeiro):
   - `tamanho: task`, `pai: [[<nota-mae>]]`, `depende-de: [[<notas>]]` (vazio se nenhuma).
   - "Objetivo" = o que a fatia entrega. Criterios de aceite proprios da fatia.
   - Nao copie decisoes da nota-mae. Faca link.
7. Na nota-mae, liste as filhas por onda, com o que cada uma entrega, e marque o caminho critico.

## Fronteira

Uma fatia esta livre para comecar quando todas as notas de `depende-de` estao `concluida`.

Cada fatia passa pelo `/task-design` individualmente. Nao faca o Design de todas de uma vez.
