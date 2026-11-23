"""Testes do scripts/metricas.py sobre um mini-vault sintetico (git em pasta temporaria).

Rodar: python -m unittest discover scripts/tests
Todos os dados sao inventados.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import metricas  # noqa: E402

TEXTO_SECRETO = "FRASE-SECRETA-QUE-NAO-PODE-SAIR"

NOTA_TPL = """---
id: {id}
status: {status}
tipo: {tipo}
tamanho: task
estagio: {estagio}
pr: []
atualizado: 2026-11-01
{extra}---

# {id} - nota de teste

## Objetivo
{secreto}

## Entendimento
Texto.

### Prova com dado real
nao se aplica - teste sintetico

## Definicao de pronto
- **Feliz:**
  - [{marca}] Quando A, entao B
- **Erro esperado:**
  - [ ] Quando C, entao D
- **Repeticao:** nao se aplica - sem repeticao
- **Limite:**
  - [ ] Quando E, entao F
- **Acesso indevido:** nao se aplica - sem acesso

## Contrato
- **C1.** {contrato}

## Registro de etapas
{registro}
"""

REGISTRO_COMPLETO = """- plan: concluido em 2026-11-02 · tipo feature · tamanho task · prova feita · skips: nenhum
- design: concluido em 2026-11-02 · prototipos 0 · etapas 3 · skips: prototipo (sem pergunta aberta)
- build: concluido em 2026-11-02 · modelo Opus · rodadas 2 · desvios 3 · falhas esperadas 0 · skips: nenhum
- verify: concluido em 2026-11-02 · modo leve · rodadas 1 · bloqueantes 1 · atencao 2 · candidatos 5 · refutados 2 · skips: raio de impacto
- ship: concluido em 2026-11-02 · ci verde · licoes 1 · skips: nenhum"""


def nota(id_, tipo="feature", status="ativa", estagio="plan", extra="", marca=" ",
         contrato="Regra fixa.", registro="", corpo_extra=""):
    return NOTA_TPL.format(
        id=id_, tipo=tipo, status=status, estagio=estagio, extra=extra, marca=marca,
        contrato=contrato, registro=registro, secreto=TEXTO_SECRETO + "\n" + corpo_extra,
    )


class MiniVault:
    """Repositorio git temporario com commits datados."""

    def __init__(self):
        self.dir = tempfile.mkdtemp(prefix="minivault-")
        self.tasks = os.path.join(self.dir, "Tarefas")
        os.makedirs(os.path.join(self.tasks, "Pendentes"))
        os.makedirs(os.path.join(self.tasks, "Concluidas"))
        self.git("init", "-q")
        self.git("config", "user.email", "teste@example.com")
        self.git("config", "user.name", "Teste")
        self.git("config", "commit.gpgsign", "false")

    def git(self, *args, data=None):
        env = dict(os.environ)
        if data:
            env["GIT_AUTHOR_DATE"] = data
            env["GIT_COMMITTER_DATE"] = data
        return subprocess.run(["git", "-C", self.dir] + list(args), check=True,
                              capture_output=True, env=env).stdout.decode("utf-8")

    def escrever(self, rel, texto):
        caminho = os.path.join(self.tasks, rel)
        with open(caminho, "w", encoding="utf-8", newline="\n") as f:
            f.write(texto)

    def commit(self, msg, data):
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", msg, data=data)

    def mover(self, de, para):
        self.git("mv", os.path.join("Tarefas", de), os.path.join("Tarefas", para))

    def limpar(self):
        shutil.rmtree(self.dir, ignore_errors=True)


def montar_vault():
    """Cenario:
    - NOV-001 (fluxo novo): plan 09:00, design 11:00, build 15:00 (Contrato muda), verify 16:00 (x2), ship 17:00,
      concluida 18:00 no dia 2026-11-02.
    - NOV-002 (fluxo novo): plan, design, build sem alterar Contrato (so marca checkbox), parada em bloqueada.
    - OLD-001 (fluxo antigo): nova 2026-10-01 10:00 -> revisada x2 -> concluida 2026-10-02 10:00 (24 h).
    - FIX-001 (tipo fix): criada em 2026-11-05 e cita [[Task - Antiga]] (OLD-001, concluida 34 dias antes,
      fora da janela 30) e NOV-001 (concluida 3 dias antes, dentro da janela).
    - FIX-002 (tipo fix): criada em 2026-11-06 e cita so OLD-001 (fora da janela).
    """
    v = MiniVault()
    # OLD-001 - fluxo antigo
    v.escrever("Pendentes/Task - Antiga.md", nota("OLD-001", registro=""))
    v.commit("OLD-001: nova task (teste)", "2026-10-01T10:00:00-03:00")
    v.escrever("Pendentes/Task - Antiga.md", nota("OLD-001", contrato="r1"))
    v.commit("OLD-001: revisada", "2026-10-01T15:00:00-03:00")
    v.escrever("Pendentes/Task - Antiga.md", nota("OLD-001", contrato="r2"))
    v.commit("OLD-001: revisada", "2026-10-01T18:00:00-03:00")
    v.escrever("Pendentes/Task - Antiga.md", nota("OLD-001", status="concluida", contrato="r2",
                                                  extra="concluida_em: 2026-10-02\n"))
    v.mover("Pendentes/Task - Antiga.md", "Concluidas/Task - Antiga.md")
    v.commit("OLD-001: concluida", "2026-10-02T10:00:00-03:00")

    # NOV-001 - fluxo novo, Contrato alterado no build
    p = "Pendentes/Task - Nova um.md"
    reg1 = REGISTRO_COMPLETO.split("\n")
    v.escrever(p, nota("NOV-001", registro=reg1[0]))
    v.commit("NOV-001: plan", "2026-11-02T09:00:00-03:00")
    v.escrever(p, nota("NOV-001", estagio="design", registro="\n".join(reg1[:2])))
    v.commit("NOV-001: design", "2026-11-02T11:00:00-03:00")
    v.escrever(p, nota("NOV-001", estagio="build", contrato="Regra MUDADA.", marca="x",
                       registro="\n".join(reg1[:3])))
    v.commit("NOV-001: build", "2026-11-02T15:00:00-03:00")
    v.escrever(p, nota("NOV-001", estagio="verify", contrato="Regra MUDADA.", marca="x",
                       registro="\n".join(reg1[:4])))
    v.commit("NOV-001: verify", "2026-11-02T15:30:00-03:00")
    v.commit("NOV-001: verify", "2026-11-02T16:00:00-03:00")
    v.escrever(p, nota("NOV-001", estagio="ship", status="em-revisao", contrato="Regra MUDADA.", marca="x",
                       registro=REGISTRO_COMPLETO))
    v.commit("NOV-001: ship", "2026-11-02T17:00:00-03:00")
    v.escrever(p, nota("NOV-001", estagio="ship", status="concluida", contrato="Regra MUDADA.", marca="x",
                       registro=REGISTRO_COMPLETO, extra="concluida_em: 2026-11-02\n"))
    v.mover(p, "Concluidas/Task - Nova um.md")
    v.commit("NOV-001: concluida", "2026-11-02T18:00:00-03:00")

    # NOV-002 - fluxo novo, so checkbox marcado depois do design; uma parada
    p = "Pendentes/Task - Nova dois.md"
    v.escrever(p, nota("NOV-002", registro=reg1[0]))
    v.commit("NOV-002: plan", "2026-11-03T09:00:00-03:00")
    v.escrever(p, nota("NOV-002", estagio="design", registro="\n".join(reg1[:2])))
    v.commit("NOV-002: design", "2026-11-03T10:00:00-03:00")
    v.escrever(p, nota("NOV-002", estagio="build", status="bloqueada", marca="x",
                       registro="\n".join(reg1[:2])))
    v.commit("NOV-002: build parado", "2026-11-03T11:00:00-03:00")
    v.escrever(p, nota("NOV-002", estagio="build", marca="x", registro="\n".join(reg1[:3])))
    v.commit("NOV-002: build", "2026-11-03T12:00:00-03:00")

    # FIX-001 e FIX-002 - defeito escapado
    v.escrever("Pendentes/Task - Corrige.md", nota(
        "FIX-001", tipo="fix", corpo_extra="Veio de [[Task - Antiga]] e de NOV-001."))
    v.commit("FIX-001: nova task (teste)", "2026-11-05T10:00:00-03:00")
    v.escrever("Pendentes/Task - Corrige dois.md", nota(
        "FIX-002", tipo="fix", corpo_extra="Veio de [[Task - Antiga|alias]]."))
    v.commit("FIX-002: plan", "2026-11-06T10:00:00-03:00")
    return v


class TestParseRegistro(unittest.TestCase):
    def test_linha_build_com_variacoes(self):
        r = metricas.parse_linha_registro(
            "- build: concluido em 2026-11-23 · modelo Opus · rodadas 2 · desvios 6 · falhas esperadas 0 · skips: nenhum")
        self.assertTrue(r["valida"])
        self.assertEqual(r["campos"]["modelo"], "opus")
        self.assertEqual(r["campos"]["desvios"], 6)
        self.assertEqual(r["campos"]["falhas esperadas"], 0)
        self.assertEqual(r["n_skips"], 0)

    def test_modelo_sessao_e_minusculo(self):
        for modelo in ("sessao", "opus", "OPUS"):
            r = metricas.parse_linha_registro(
                "- build: concluido em 2026-11-22 · modelo %s · rodadas 1 · desvios 1 · falhas esperadas 0 · skips: nenhum" % modelo)
            self.assertTrue(r["valida"], modelo)

    def test_campo_ausente_invalida_sem_quebrar(self):
        r = metricas.parse_linha_registro("- build: concluido em 2026-11-22 · modelo sessao · rodadas 1 · skips: nenhum")
        self.assertFalse(r["valida"])
        self.assertIn("falta desvios", r["problemas"])
        self.assertNotIn("desvios", r["campos"])

    def test_linha_formato_antigo_sem_data(self):
        r = metricas.parse_linha_registro("- verify: bloqueantes 2 · atencao 1")
        self.assertIsNotNone(r)
        self.assertFalse(r["valida"])
        self.assertEqual(r["campos"]["bloqueantes"], 2)

    def test_verify_com_e_sem_candidatos(self):
        sem = metricas.parse_linha_registro(
            "- verify: concluido em 2026-11-22 · modo leve · rodadas 0 · bloqueantes 0 · atencao 1 · refutados 0 · skips: revisores, raio de impacto")
        self.assertTrue(sem["valida"])
        self.assertEqual(sem["n_skips"], 2)
        self.assertEqual(sem["skips_sem_motivo"], 2)
        com = metricas.parse_linha_registro(
            "- verify: concluido em 2026-11-22 · modo leve · rodadas 0 · bloqueantes 0 · atencao 1 · candidatos 4 · refutados 3 · skips: app real (so API, sem tela)")
        self.assertEqual(com["campos"]["candidatos"], 4)
        self.assertEqual(com["skips_sem_motivo"], 0)
        self.assertEqual(com["n_skips"], 1)

    def test_linha_close(self):
        r = metricas.parse_linha_registro(
            "- close: concluido em 2026-11-24 · merge em 2026-11-23 · debitos criados 1 · debitos removidos 2 · skips: nenhum")
        self.assertTrue(r["valida"])
        self.assertEqual(r["campos"]["debitos removidos"], 2)

    def test_registro_da_nota(self):
        reg = metricas.parse_registro(nota("X-001", registro=REGISTRO_COMPLETO))
        self.assertEqual(sorted(reg), ["build", "design", "plan", "ship", "verify"])
        self.assertTrue(all(r["valida"] for r in reg.values()))

    def test_linha_que_nao_e_registro(self):
        self.assertIsNone(metricas.parse_linha_registro("- texto livre qualquer"))


class TestRegraN(unittest.TestCase):
    def test_abaixo_de_10_sem_percentual(self):
        ind = metricas.percentual(["A-1"], ["A-%d" % i for i in range(1, 10)])
        self.assertIsNone(ind["valor"])
        self.assertEqual(ind["contagem"], 1)
        self.assertEqual(ind["n"], 9)
        self.assertEqual(ind["ids_sim"], ["A-1"])
        self.assertEqual(metricas.fmt(ind), "1 de 9")

    def test_a_partir_de_10_com_percentual(self):
        ind = metricas.percentual(["A-1", "A-2"], ["A-%d" % i for i in range(1, 11)])
        self.assertEqual(ind["valor"], 20.0)


class TestMiniVault(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v = montar_vault()
        cls.vault = metricas.Vault(cls.v.dir, "Tarefas")
        cls.vault.carregar_historicos(cls.vault.notas)

    @classmethod
    def tearDownClass(cls):
        cls.v.limpar()

    def test_fluxo_novo_e_antigo(self):
        self.assertEqual(self.vault.por_id["NOV-001"].fluxo, "novo")
        self.assertEqual(self.vault.por_id["OLD-001"].fluxo, "antigo")

    def test_historico_segue_movimento_de_pasta(self):
        n = self.vault.por_id["NOV-001"]
        self.assertEqual(len(n.historico), 6)  # o 2o verify e commit vazio
        self.assertTrue(all(v is not None for v in n.versoes))

    def test_contrato_alterado_depois_do_design(self):
        self.assertEqual(metricas.contrato_alterado(self.vault.por_id["NOV-001"]), "build")

    def test_checkbox_marcado_nao_conta_como_alteracao(self):
        self.assertEqual(metricas.contrato_alterado(self.vault.por_id["NOV-002"]), "")

    def test_sem_design_nao_se_aplica(self):
        self.assertIsNone(metricas.contrato_alterado(self.vault.por_id["OLD-001"]))

    def test_tempo_por_estagio(self):
        t = metricas.tempos_estagio(self.vault.por_id["NOV-001"])
        self.assertEqual(t, {"plan": 0.0, "design": 2.0, "build": 4.0, "verify": 1.0, "ship": 1.0, "concluida": 1.0})
        self.assertEqual(metricas.tempo_total(self.vault.por_id["NOV-001"]), 9.0)

    def test_retrabalho(self):
        self.assertEqual(metricas.estagios_repetidos(self.vault.por_id["NOV-001"]), 1)
        self.assertEqual(metricas.estagios_repetidos(self.vault.por_id["OLD-001"]), 1)
        self.assertEqual(metricas.tempo_total(self.vault.por_id["OLD-001"]), 24.0)

    def test_parada_bloqueada(self):
        p = metricas.paradas(self.vault.por_id["NOV-002"])
        self.assertEqual(len(p), 1)
        self.assertEqual(p[0][1], "build")

    def test_defeito_escapado(self):
        achados = metricas.defeitos_escapados(self.vault, "2026-11", 30)
        self.assertEqual(achados, [("FIX-001", "NOV-001")])
        largos = sorted(metricas.defeitos_escapados(self.vault, "2026-11", 40))
        self.assertEqual(largos, [("FIX-001", "NOV-001"), ("FIX-001", "OLD-001"), ("FIX-002", "OLD-001")])

    def test_execucao_completa_so_le_o_vault_e_nao_vaza_texto(self):
        antes = self.v.git("status", "--porcelain") + self.v.git("rev-parse", "HEAD")
        saida = tempfile.mkdtemp(prefix="metricas-saida-")
        try:
            cfg = os.path.join(saida, "config.json")
            with open(cfg, "w", encoding="utf-8") as f:
                json.dump({"vault": self.v.dir, "pasta_tasks": "Tarefas", "repositorios": [],
                           "janela_defeito_dias": 30}, f)
            rc = metricas.main(["--config", cfg, "--mes", "2026-11", "--meses-anteriores", "1",
                                "--saida", saida, "--sem-gh"])
            self.assertEqual(rc, 0)
            with open(os.path.join(saida, "metricas-2026-11.json"), encoding="utf-8") as f:
                txt_json = f.read()
            with open(os.path.join(saida, "metricas-2026-11.md"), encoding="utf-8") as f:
                txt_md = f.read()
            for txt in (txt_json, txt_md):
                self.assertNotIn(TEXTO_SECRETO, txt)
                self.assertNotIn("Task - ", txt)
            dados = json.loads(txt_json)
            nov = dados["periodos"][0]
            self.assertEqual(nov["mes"], "2026-11")
            self.assertEqual(dados["periodos"][1]["mes"], "2026-10")
            ga = nov["fluxo_novo"]["grupos"]["A"]
            self.assertEqual(ga["contrato_ou_dod_alterado_apos_design"]["ids_sim"], ["NOV-001"])
            self.assertIsNone(ga["contrato_ou_dod_alterado_apos_design"]["valor"])  # N < 10
            self.assertEqual(ga["defeito_escapado"]["ids"], ["FIX-001"])
            self.assertTrue(ga["defeito_escapado"]["aproximado"])
            self.assertEqual(dados["periodos"][1]["fluxo_antigo"]["tasks"]["ids"], ["OLD-001"])
            self.assertIn("NOV-001", txt_md)
            self.assertIn("| Indicador | 2026-11 | 2026-10 |", txt_md)
            self.assertEqual(sorted(os.listdir(saida)),
                             ["config.json", "metricas-2026-11.json", "metricas-2026-11.md"])
        finally:
            shutil.rmtree(saida, ignore_errors=True)
        depois = self.v.git("status", "--porcelain") + self.v.git("rev-parse", "HEAD")
        self.assertEqual(antes, depois)


if __name__ == "__main__":
    unittest.main()
