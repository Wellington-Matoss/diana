# Comprovar no app real

## Ambiente

- **Padrao: ambiente local isolado**, iniciado por esta verificacao, com banco de teste populado (seed) e conta de teste. A skill `verify` do projeto define como subir, conferir a saude, operar e desligar.
- **Nunca** opere um ambiente compartilhado com dados reais de clientes, a menos que o contexto do projeto autorize explicitamente e defina limites.
- **Nunca** digite senha ou codigo de autenticacao do usuario. Use so credenciais de conta de teste definidas na configuracao local do projeto.
- **LGPD:** se uma tela mostrar dado pessoal, nao copie para nota, PR ou commit. Descreva de forma generica ("lista com 12 dispositivos").
- Desligue tudo o que voce subiu. A evidencia fica; o ambiente vai embora.

## Padrao de prova

- Percorra o **caminho real do usuario**, nao um atalho interno ou endpoint de teste.
- Capture a **acao e o estado resultante**, nao so a tela final.
- Confira o **efeito colateral** junto com o visivel: registro gravado, chamada feita, mensagem enviada.
- Prefira texto da pagina, status das chamadas de rede e console a captura de tela. Captura so quando a evidencia for visual.
- Status de rede prova regra de backend (ex.: 403 para perfil sem acesso).
- Falha na comprovacao: antes de culpar o codigo, confira o metodo de observacao (instancia certa? branch certa? seed certo?).
- Modo de teste ou "dry-run": confirme pelo que acontece (arquivos, rede), nao pelo nome.

## Sem skill `verify` no projeto

- API: tente comprovar por HTTP contra o backend local com banco de teste, se o contexto do projeto disser como subir.
- Tela ou caminho nao alcancavel: marque `nao comprovado - sem skill verify` e gere o **roteiro manual** para o PR: perfil, passos, resultado esperado por criterio, e quais passos gravam dado.

## Criar a skill `verify` do projeto (uma vez por projeto)

Gere `.claude/skills/verify/SKILL.md` no repositorio do projeto (em monorepo, no pacote tocado), escrita para um agente que nunca viu o app:

1. **Investigue o repositorio, nao o usuario:** superficie (web, API, CLI), como sobe localmente, como um agente opera (Playwright, HTTP, PTY), que evidencia da para capturar, se duas instancias rodam lado a lado.
2. Secoes obrigatorias, com comandos reais do projeto:
   - **Launch:** comando que sobe do zero (com migracao e seed) e como saber que esta pronto para uso;
   - **Doctor:** uma checagem somente leitura (processo de pe, versao certa, porta nossa);
   - **Drive:** como operar, com seletores estaveis (rotulo acessivel, atributo de teste), nunca coordenada;
   - **Evidence:** o que capturar e onde guardar;
   - **Cleanup:** como desligar o que foi iniciado. Nunca mate processo pelo nome.
3. **Mapa de funcionalidades:** `.claude/skills/verify/features/README.md` + um arquivo por funcionalidade principal (comece com 3 a 5): o que e, como o usuario chega, como operar, que estado final prova que funciona, armadilhas. Nunca enfraqueca um roteiro para ele passar.
4. **Prove a skill:** rode uma vez de ponta a ponta (launch, doctor, uma funcionalidade, evidencia, cleanup) e confirme que a evidencia sobreviveu ao cleanup.

## Numeros

Quando a task produz ou melhora um numero, responda com evidencia antes de reportar:

1. **Qual o gargalo?** Por que nao e o dobro?
2. **Estava ajustado como em producao?** Build de producao, mesmas configuracoes e dados.
3. **Passa de algum limite fisico?** Se passa, mediu outra coisa (cache, no-op, bug).
4. **Teve erro?** Conte falhas; resposta rapida pode ser rejeicao.
5. **Reproduz?** Ao menos 5 execucoes por lado, alternadas. Reporte mediana e faixa.
6. **Importa?** Meca tambem o caminho de ponta a ponta que o usuario espera.
7. **O trabalho aconteceu?** A requisicao chegou, o dado foi gravado, o resultado foi usado.

Sem responder 4 e 7, ou sem nomear o gargalo: veredito `inconclusivo`.
