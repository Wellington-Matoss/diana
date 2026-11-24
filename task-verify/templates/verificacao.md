## Verificacao

**Modo:** <leve | completo> - <motivo>
**Rodadas de volta ao Build:** <n>
**Testes:** `<comando>` -> <resultado>   **Lint:** <resultado nos arquivos/linhas do diff>
**Copia isolada:** <local> · linha de base reproduzida <sim|nao> · removida <sim|nao>   <!-- so se algum revisor executou codigo -->

### Comprovacao no app
**Ambiente:** <local isolado com seed | outro, conforme contexto do projeto>
| Criterio | Resultado | Evidencia |
|---|---|---|
| Quando ..., entao ... | comprovado / falhou / nao comprovado (motivo) | <status, texto da tela, registro gravado> |

### Achados
**Bloqueantes (corrigidos):**
- [Alto] <achado> - <prova> - corrigido no commit `<hash>`

**Atencao (vai para o PR):**
- <item> - <por que precisa do usuario>

**Nota (nao vai para o PR):**
- [Medio] <achado> - <prova ou PLAUSIVEL>

**Refutados:**
- <candidato> - <prova de que nao procede>

### Sugestoes para o projeto
<!-- padrao: "Nenhuma." So preencha se a revisao encontrou algo que cumpre os 4 criterios. -->
Nenhuma.
- **<titulo>** - Problema: ... | Onde: `arq:linha`, `arq:linha` | Proposta: ... | Beneficio: ... | Esforco: P/M/G

### Resumo do diff (para o PR)
<ate ~100 palavras: o que mudou, onde mexeu, o que divergiu do plano e por que>

### Roteiro manual pendente
<so se houver criterio nao comprovado: perfil, passos, resultado esperado; marque passos que gravam dado>
