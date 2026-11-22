# Design duas vezes (decisao sem volta)

Use so quando a forma for dificil de reverter: schema, contrato de API usado por outro sistema, dono de um dado, migracao. Para o resto, esbocar duas formas sozinho (passo 4) basta.

A primeira ideia raramente e a melhor.

## Passos

1. **Enquadre o problema** para o usuario: restricoes que qualquer interface precisa cumprir, dependencias, e um esboco ilustrativo (nao uma proposta). Mostre e continue; o usuario le enquanto os subagentes trabalham.
2. **Dispare 3 subagentes em paralelo**, cada um em contexto novo, com o mesmo brief tecnico (arquivos, acoplamentos, o que fica atras do seam, vocabulario de `vocabulario.md` e termos do glossario) e uma restricao diferente:
   - A: "Minimize a interface: 1 a 3 pontos de entrada."
   - B: "Maximize a flexibilidade: suporte muitos casos de uso."
   - C: "Otimize para o chamador mais comum: o caso padrao deve ser trivial."
3. Cada subagente entrega:
   1. interface (tipos, metodos, parametros, invariantes, ordem, modos de erro);
   2. exemplo de uso pelo chamador;
   3. o que a implementacao esconde atras do seam;
   4. dependencias e adapters;
   5. trade-offs: onde a interface rende muito, onde rende pouco.
4. **Apresente uma por vez** e depois compare por profundidade, localidade (onde a mudanca se concentra) e posicao do seam.
5. **Recomende** uma, ou um hibrido se partes combinarem bem. Seja direto: o usuario quer uma leitura forte, nao um cardapio. A decisao e do usuario.
6. Registre na nota as tres formas em uma linha cada e o motivo da escolha. Avalie se cabe uma decisao de arquitetura no vault (as tres condicoes do passo 7).
