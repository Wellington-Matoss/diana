# Prototipo de logica

Responde "essa regra, esse modelo de estados ou essa forma de dados aguenta os casos reais?". Gera **um arquivo HTML unico** que qualquer pessoa abre com dois cliques e opera com botoes.

## Passos

1. **Escreva a pergunta** no topo da pagina, visivel (nao so em comentario).
2. **Isole a logica num modulo puro** dentro de um `<script>`: sem DOM, sem `document`. A pagina chama o modulo; nada vai no sentido contrario. Escolha a forma que responde a pergunta:
   - reducer `(estado, acao) => estado`, para eventos discretos;
   - maquina de estados, quando "quais acoes sao permitidas agora" faz parte da pergunta;
   - funcoes puras sobre um tipo simples, quando nao ha estado atual.
3. **Monte a pagina** em linguagem do dominio, nao do codigo:
   1. titulo e a pergunta em uma linha;
   2. **estado atual** em painel legivel (campos com rotulo, nao JSON cru), atualizado a cada clique, destacando o que mudou;
   3. **botoes livres**, um por acao, sempre disponiveis;
   4. **roteiros guiados**, um por aba: descricao do cenario e os botoes na ordem. Cada roteiro comeca de um estado inicial conhecido. Inclua: caminho feliz, caso de borda dificil, tentativa de algo que deveria ser proibido.
4. HTML, CSS e JS inline, sem framework, sem servidor. Visual limpo, sem animacao.
5. Entregue o arquivo. Os momentos uteis sao "espera, isso nao deveria ser possivel" e "eu achava que X seria diferente": sao erros na ideia, encontrados antes do codigo.

## Depois da resposta

- Registre na nota: pergunta, cenarios testados, resposta.
- O modulo puro validado pode ser levado para o codigo real no Build (com testes). A pagina HTML fica na branch `prototype/<ID>`.
