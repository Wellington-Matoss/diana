# Atribuicoes

Esta skill adapta ideias (traduzidas e resumidas) de:

- **mattpocock/skills** - MIT License, Copyright (c) 2026 Matt Pocock.
  https://github.com/mattpocock/skills
  Base: `pr` (resumo visual minimo, evidencia antes/depois, perigo do merge com porta de mao unica ou dupla e raio de impacto; o `pr` credita a skill `show-me` de Dex Horthy / Humanlayer), `retro` (licoes do processo; erro mecanico vira checagem automatica).

- **pstack** - MIT License, Copyright (c) 2026 Lauren Tan; port para Claude Code: Copyright (c) 2026 Michael Denyer.
  https://github.com/cursor/plugins/tree/main/pstack (port para Claude Code: https://github.com/michael-denyer/pstack-claude)
  Base: playbook `opening-a-pr` (titulo `tipo(escopo): assunto`, corpo curto, PR pronto e nao rascunho), playbook `babysit` (acompanhar CI, maximo de rodadas, nunca merge), principio `encode-lessons-in-structure`.

- **cursor-team-kit** - MIT License, Copyright (c) 2026 Cursor.
  https://github.com/cursor/plugins/tree/main/cursor-team-kit (plugin irmao do pstack, no mesmo repositorio)
  Base: `fix-ci` (acompanhar CI, maximo de rodadas, nunca mudar esperado de teste), `make-pr-easy-to-review` (PR grande se divide, nao se maquia).

Padrao de commit baseado na especificacao Conventional Commits (https://www.conventionalcommits.org).

Os textos das licencas estao em `licencas/`. As licencas MIT exigem manter o aviso de copyright e o texto da licenca em copias ou partes substanciais. Confirme os termos vigentes nos repositorios. Isto nao e parecer juridico.
