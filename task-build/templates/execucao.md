## Execucao

**Branch:** `<nome>` em <repositorio(s)>
**Modelo:** <modelo> - <motivo em uma linha>
**Linha de base:** testes <x passaram / y falharam pre-existentes>, lint <n apontamentos>, build <ok | falha>

| Etapa | Commit | Testes (vermelho -> verde) | Sem teste automatizado | Rodadas |
|---|---|---|---|---|
| 1 | `abc1234` | `nome do teste` | - | 1 |

**Verificacao final (rodada pelo lider):**
- Testes: `<comando>` -> <resultado>
- Lint: `<comando>` -> <resultado vs linha de base>
- Build: `<comando>` -> <resultado>

**Limpeza:**
- Geral: <o que foi removido; edicoes revertidas>
- Comentarios removidos: <quantidade, por arquivo>
- Reescritas feitas: <simbolo e regra que o codigo passou a deixar obvia>
- Pendencias criadas: <reescrita que nao coube na task, candidato a debito>
- Supressoes removidas: <regra de cada uma; mantidas e por que>

### Candidatos a Atencao (o Verify filtra o que vai para o PR)
- <frase sem teste automatizado (teste impraticavel); falha esperada registrada; decisao de dominio no lint; restricao "nao remover" confirmada (proposta de teste, tipo ou checagem); supressao que protege a correcao, com correcao fora do escopo; achado sem seam de teste; dado gravado fora do padrao sem frase na Definicao de pronto>
