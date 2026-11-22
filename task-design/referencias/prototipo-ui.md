# Prototipo de UI

Responde "como deve parecer?". Gera **3 variantes estruturalmente diferentes** (maximo 5) para o usuario comparar no navegador.

## Onde montar

- **Preferido: dentro da pagina real.** As variantes ficam na rota que ja existe, com os dados, o cabecalho e o menu reais, trocadas por `?variant=A|B|C`. Variante isolada numa pagina vazia parece boa sempre e esconde problemas.
- Algo novo que vai morar dentro de uma pagina existente (nova secao, novo card, novo passo de um fluxo): monte dentro dessa pagina.
- **Ultimo caso: rota nova** com `prototype` no nome, seguindo a convencao de rotas do projeto.

## Passos

1. Escreva a pergunta e o plano em uma linha no topo do arquivo. Ex.: "3 variantes do painel do sensor via `?variant=`, na rota `/sensores/:id`".
2. Gere as variantes. Elas precisam diferir em **layout, hierarquia da informacao ou acao principal**, nao so em cor ou texto. Use a biblioteca de componentes do projeto. Se duas sairem parecidas, refaca uma com restricao explicita (ex.: "sem grade de cards").
3. Ligue as variantes a um seletor unico: os dados continuam sendo buscados acima do seletor; so a renderizacao muda.
4. Barra flutuante no rodape: seta anterior, nome da variante, seta seguinte; setas do teclado tambem trocam (exceto com foco em campo de texto). A barra atualiza o `?variant=` na URL. A barra nao aparece em build de producao.
5. Somente leitura. Se uma variante precisar gravar, use stub.
6. Entregue a URL e as chaves das variantes. O retorno mais util costuma ser "o cabecalho da B com a lateral da C".

## Depois da escolha

- Registre na nota: variante escolhida e motivo.
- Todas as variantes e o seletor ficam na branch `prototype/<ID>`. A main nao recebe nada do prototipo.
- O Build reescreve a variante escolhida com testes e tratamento de erro. Nao promova o codigo do prototipo direto.
