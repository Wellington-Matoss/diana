# Limpeza do diff

Escopo: o diff da task contra a branch base, incluindo mudancas nao commitadas. Nao mexa em codigo fora do diff.

## Remover

- **Comentario desnecessario:** comentario que repete o codigo, narra o que a linha faz, ou e diferente do estilo local. Fica so comentario que explica o **porque** de algo que o codigo nao consegue dizer (restricao externa, regra de negocio nao obvia, contorno de bug de biblioteca com link).
- **Defesa fora do normal:** `try/catch`, verificacao de nulo ou validacao em caminho interno que ja recebe dado validado. Validacao fica na fronteira (entrada da API, leitura de arquivo, resposta externa).
- **Cast para contornar tipo** (`as any`, `as unknown as X`) sem validacao antes.
- **Aninhamento** que um retorno antecipado resolve.
- **Codigo morto** criado pela task: funcao, variavel, import ou parametro sem uso.
- **Log de debug** e `console.log` deixados pela task.
- **Padrao diferente do arquivo:** nomes, formatacao ou estrutura que nao seguem o resto do arquivo.

## Regras

- Comportamento nao muda.
- Edicoes pequenas e focadas. Nada de reescrever.
- Depois de limpar: rode testes, lint e build. **Reverta** a edicao de limpeza que quebrar algo.
- Comentario que diz "nao remover" ou "falar com X antes de mudar": mantenha e marque "Atencao" para o PR.
