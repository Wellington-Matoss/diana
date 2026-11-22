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

**Limpeza:** <o que foi removido; edicoes revertidas>

### Candidatos a Atencao (o Verify filtra o que vai para o PR)
- <desvio que mudou forma/interface/plano de testes; decisao de dominio no lint; comentario "nao remover"; achado sem seam de teste>
