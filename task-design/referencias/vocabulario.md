# Vocabulario de forma

Use estes termos exatamente. Linguagem consistente e o objetivo.

| Termo | Significado |
|---|---|
| **Modulo** | Qualquer coisa com interface e implementacao: funcao, classe, pacote, fatia que atravessa camadas. |
| **Interface** | Tudo o que o chamador precisa saber para usar o modulo corretamente: assinatura, invariantes, ordem de chamada, modos de erro, configuracao obrigatoria, desempenho. Nao e so a assinatura. |
| **Implementacao** | O codigo dentro do modulo. |
| **Profundidade** | Quanto comportamento o chamador (ou o teste) acessa por unidade de interface que precisa aprender. **Profundo**: muito comportamento atras de interface pequena. **Raso**: interface quase tao complexa quanto a implementacao. Evite modulos rasos. |
| **Seam** | Lugar onde o comportamento pode ser trocado sem editar o codigo daquele lugar. E onde fica a interface. Onde colocar o seam e uma decisao propria. |
| **Adapter** | Coisa concreta que satisfaz a interface num seam (ex.: repositorio MongoDB, fake em memoria). |

## Regras

- **Teste da exclusao:** imagine apagar o modulo. Se a complexidade some, ele era so repasse. Se a complexidade reaparece em varios chamadores, ele se paga.
- **A interface e a superficie de teste:** chamador e teste passam pelo mesmo seam. Se o teste precisa passar por tras da interface, a forma do modulo provavelmente esta errada.
- **Um adapter = seam hipotetico. Dois adapters = seam real.** Nao crie seam se nada varia nele.
- **Profundidade e propriedade da interface:** um modulo profundo pode ter partes pequenas por dentro. Elas so nao fazem parte da interface.

## Para facilitar o teste

1. **Receba dependencias, nao crie.** `processar(pedido, gateway)` e testavel; `new Gateway()` dentro da funcao nao e.
2. **Retorne resultado, evite efeito colateral.** `calcularDesconto(carrinho): Desconto` e testavel; `aplicarDesconto(carrinho): void` que altera o carrinho e menos.
3. **Interface pequena.** Menos metodos e menos parametros = menos testes e setup mais simples.
