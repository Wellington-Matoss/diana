#!/usr/bin/env python3
"""Metricas das notas de task do fluxo Plan -> Design -> Build -> Verify -> Ship -> Close.

Uso:
    python scripts/metricas.py --config <arquivo.json> --mes AAAA-MM
        [--meses-anteriores N] --saida <pasta> [--sem-gh]

Le o vault (notas + historico git) e gera metricas-AAAA-MM.json e
metricas-AAAA-MM.md na pasta de saida. So le o vault: usa apenas comandos git
de leitura (log, cat-file, rev-parse) e nao escreve em nenhum lugar alem da
pasta de saida.

Regras de saida:
- so IDs e numeros: nenhum texto da nota vai para a saida (LGPD);
- indicador percentual com N < 10 vira contagem + lista de IDs.

Somente biblioteca padrao.
"""

import argparse
import json
import os
import re
import statistics
import subprocess
import sys
import unicodedata
from datetime import date, datetime, timedelta

ESTAGIOS_NOVOS = ["plan", "design", "build", "verify", "ship"]
ORDEM_NOVA = ESTAGIOS_NOVOS + ["concluida"]
ROTULOS_ANTIGOS = ["nova", "implementada", "revisada", "concluida"]
ROTULOS = set(ORDEM_NOVA) | set(ROTULOS_ANTIGOS)
N_MINIMO_PERCENTUAL = 10

ID_RE = re.compile(r"\b[A-Z][A-Z0-9]{1,9}-\d{1,4}(?:-[A-Z0-9]{1,4})?\b")
COMMIT_ESTAGIO_RE = re.compile(r"^\s*([A-Z][A-Z0-9]{1,9}-\d{1,4}(?:-[A-Z0-9]{1,4})?):\s*([A-Za-z]+)")
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")

# Campos de cada linha do Registro de etapas (template da spec).
# "opcionais" sao campos novos: linhas antigas sem eles continuam validas.
CAMPOS_REGISTRO = {
    "plan": {"obrigatorios": ["tipo", "tamanho", "prova"], "opcionais": [], "numericos": []},
    "design": {"obrigatorios": ["prototipos", "etapas"], "opcionais": [], "numericos": ["prototipos", "etapas"]},
    "build": {
        "obrigatorios": ["modelo", "rodadas", "desvios", "falhas esperadas"],
        "opcionais": [],
        "numericos": ["rodadas", "desvios", "falhas esperadas"],
    },
    "verify": {
        "obrigatorios": ["modo", "rodadas", "bloqueantes", "atencao", "refutados"],
        "opcionais": ["candidatos"],
        "numericos": ["rodadas", "bloqueantes", "atencao", "candidatos", "refutados"],
    },
    "ship": {"obrigatorios": ["ci", "licoes"], "opcionais": [], "numericos": ["licoes"]},
    "close": {
        "obrigatorios": ["merge em", "debitos criados", "debitos removidos"],
        "opcionais": [],
        "numericos": ["debitos criados", "debitos removidos"],
    },
}
MODELOS = {"sonnet", "opus", "fable", "haiku", "sessao"}
CATEGORIAS_DOD = ["feliz", "erro esperado", "repeticao", "limite", "acesso indevido"]

LINHA_REGISTRO_RE = re.compile(
    r"^\s*[-*]\s*(plan|design|build|verify|ship|close)\s*:\s*(.*)$", re.IGNORECASE
)
CONCLUIDO_RE = re.compile(r"^concluido em\s+(\d{4}-\d{2}-\d{2})\s*$", re.IGNORECASE)


# ---------------------------------------------------------------- utilidades


def normalizar(texto):
    """Minusculas e sem acento, para comparar rotulos."""
    sem = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in sem if not unicodedata.combining(c)).lower()


def parse_data_iso(texto):
    return datetime.fromisoformat(texto.strip())


def horas(delta):
    return round(delta.total_seconds() / 3600.0, 1)


def resumo_numerico(valores):
    if not valores:
        return None
    return {
        "mediana": round(statistics.median(valores), 1),
        "minimo": round(min(valores), 1),
        "maximo": round(max(valores), 1),
    }


def meses_analisados(mes, anteriores):
    ano, m = (int(x) for x in mes.split("-"))
    saida = []
    for i in range(anteriores + 1):
        a, mm = ano, m - i
        while mm <= 0:
            mm += 12
            a -= 1
        saida.append("%04d-%02d" % (a, mm))
    return saida


# ---------------------------------------------------------------- git (so leitura)


class Git:
    """Executa somente comandos git de leitura no repositorio do vault."""

    def __init__(self, pasta):
        self.pasta = pasta
        self.env = dict(os.environ)
        # nao deixa o git atualizar o index nem pegar lock
        self.env["GIT_OPTIONAL_LOCKS"] = "0"
        self.env["GIT_TERMINAL_PROMPT"] = "0"
        self.raiz = self.run("rev-parse", "--show-toplevel").strip()

    def run(self, *args):
        cmd = ["git", "-c", "core.quotepath=false", "-C", self.pasta] + list(args)
        res = subprocess.run(
            cmd, capture_output=True, env=self.env, check=False
        )
        if res.returncode != 0:
            raise RuntimeError("git falhou: %s" % " ".join(args[:2]))
        return res.stdout.decode("utf-8", errors="replace")

    def commits(self):
        """Todos os commits: (sha, data, assunto), do mais antigo ao mais novo."""
        saida = self.run("log", "--reverse", "--format=%H%x1f%cI%x1f%s")
        lista = []
        for linha in saida.splitlines():
            partes = linha.split("\x1f")
            if len(partes) == 3:
                lista.append((partes[0], parse_data_iso(partes[1]), partes[2]))
        return lista

    def historicos(self, pasta_rel, caminhos):
        """Historico de varias notas numa passada so (segue renomeacao dentro da pasta).

        caminhos: caminhos atuais (relativos a raiz do repositorio).
        Devolve {caminho_atual: [(sha, data, assunto, caminho_no_commit), ...]} do mais antigo ao mais novo.
        """
        saida = self.run(
            "log", "-M", "--name-status", "--format=%x1e%H%x1f%cI%x1f%s", "--", ":(top)" + pasta_rel
        )
        vivo = {c: c for c in caminhos}  # caminho no ponto atual da varredura -> caminho atual
        hist = {c: [] for c in caminhos}
        for bloco in saida.split(""):
            linhas = [l for l in bloco.splitlines() if l.strip()]
            if not linhas:
                continue
            partes = linhas[0].split("")
            if len(partes) != 3:
                continue
            sha, data, assunto = partes[0], parse_data_iso(partes[1]), partes[2]
            for linha in linhas[1:]:
                campos = linha.split("	")
                st = campos[0][:1]
                if st == "R" and len(campos) >= 3:
                    velho, novo = campos[1], campos[2]
                    if novo in vivo:
                        atual = vivo.pop(novo)
                        hist[atual].append((sha, data, assunto, novo))
                        vivo[velho] = atual
                elif len(campos) >= 2 and campos[1] in vivo:
                    atual = vivo[campos[1]]
                    if st == "D":
                        continue
                    hist[atual].append((sha, data, assunto, campos[1]))
                    if st == "A":
                        vivo.pop(campos[1])
        for c in hist:
            hist[c].reverse()
        return hist

    def conteudos(self, pedidos):
        """Le varios 'sha:caminho' de uma vez (git cat-file --batch)."""
        if not pedidos:
            return []
        entrada = "".join(p + "\n" for p in pedidos).encode("utf-8")
        res = subprocess.run(
            ["git", "-C", self.pasta, "cat-file", "--batch"],
            input=entrada, capture_output=True, env=self.env, check=False,
        )
        dados = res.stdout
        pos = 0
        saida = []
        for _ in pedidos:
            fim = dados.index(b"\n", pos)
            cabecalho = dados[pos:fim].decode("utf-8", errors="replace")
            pos = fim + 1
            if cabecalho.endswith("missing") or len(cabecalho.split()) < 3:
                saida.append(None)
                continue
            tamanho = int(cabecalho.split()[2])
            saida.append(dados[pos:pos + tamanho].decode("utf-8", errors="replace"))
            pos += tamanho + 1
        return saida


# ---------------------------------------------------------------- parse da nota


def parse_frontmatter(texto):
    """YAML minimo: chave: valor e listas (inline [a, b] ou em bloco)."""
    fm = {}
    if not texto.startswith("---"):
        return fm
    linhas = texto.splitlines()
    chave_lista = None
    for linha in linhas[1:]:
        if linha.strip() == "---":
            break
        if chave_lista and re.match(r"^\s+-\s*", linha):
            fm[chave_lista].append(linha.strip()[1:].strip().strip("'\""))
            continue
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", linha)
        if not m:
            continue
        chave, valor = m.group(1), m.group(2)
        valor = re.sub(r"\s+#.*$", "", valor).strip()
        chave_lista = None
        if valor == "":
            fm[chave] = []
            chave_lista = chave
        elif valor.startswith("[") and valor.endswith("]"):
            itens = [v.strip().strip("'\"") for v in valor[1:-1].split(",")]
            fm[chave] = [v for v in itens if v]
        else:
            fm[chave] = valor.strip("'\"")
    return fm


def secao(texto, titulo, nivel=2):
    """Texto de uma secao '## titulo' (ate o proximo titulo de nivel <= nivel)."""
    alvo = normalizar(titulo)
    linhas = texto.splitlines()
    dentro = False
    saida = []
    for linha in linhas:
        m = re.match(r"^(#{1,6})\s+(.*)$", linha)
        if m:
            n = len(m.group(1))
            if dentro and n <= nivel:
                break
            if n == nivel and normalizar(m.group(2)).strip() == alvo:
                dentro = True
                continue
        if dentro:
            saida.append(linha)
    return "\n".join(saida) if dentro else None


def dividir_skips(texto):
    """Divide 'a (x, y), b' em ['a (x, y)', 'b'], respeitando parenteses."""
    itens, atual, nivel = [], "", 0
    for c in texto:
        if c == "(":
            nivel += 1
        elif c == ")":
            nivel = max(0, nivel - 1)
        if c in ",;" and nivel == 0:
            itens.append(atual.strip())
            atual = ""
        else:
            atual += c
    if atual.strip():
        itens.append(atual.strip())
    return [i for i in itens if i]


def skip_tem_motivo(item):
    return bool(re.search(r"\(.+\)", item)) or bool(re.search(r"\s[-:]\s\S", item))


def parse_linha_registro(linha):
    """Interpreta uma linha do Registro. Tolerante: devolve None se nao for linha de estagio."""
    m = LINHA_REGISTRO_RE.match(linha)
    if not m:
        return None
    estagio = m.group(1).lower()
    resto = m.group(2)
    partes = [p.strip() for p in re.split(r"\s*·\s*", resto) if p.strip()]
    esquema = CAMPOS_REGISTRO[estagio]
    chaves = sorted(esquema["obrigatorios"] + esquema["opcionais"], key=len, reverse=True)
    reg = {"estagio": estagio, "data": None, "campos": {}, "skips": None, "problemas": []}
    for i, parte in enumerate(partes):
        pn = normalizar(parte)
        if i == 0:
            mc = CONCLUIDO_RE.match(pn)
            if mc:
                reg["data"] = mc.group(1)
                continue
            reg["problemas"].append("sem data")
        if pn.startswith("skips:") or pn.startswith("skip:"):
            reg["skips"] = parte.split(":", 1)[1].strip()
            continue
        achou = False
        for chave in chaves:
            if pn == chave or pn.startswith(chave + " "):
                valor = parte[len(chave):].strip()
                if chave in esquema["numericos"]:
                    valor = int(valor) if re.fullmatch(r"\d+", valor) else valor
                    if not isinstance(valor, int):
                        reg["problemas"].append("%s nao numerico" % chave)
                if chave == "modelo":
                    valor = normalizar(valor)
                    if valor not in MODELOS:
                        reg["problemas"].append("modelo fora da lista")
                reg["campos"][chave] = valor
                achou = True
                break
        if not achou:
            reg["problemas"].append("campo desconhecido")
    for chave in esquema["obrigatorios"]:
        if chave not in reg["campos"]:
            reg["problemas"].append("falta %s" % chave)
    if reg["skips"] is None:
        reg["problemas"].append("falta skips")
    reg["valida"] = not reg["problemas"]
    # skips
    if reg["skips"] is not None and normalizar(reg["skips"]).strip() not in ("nenhum", "nenhuma", ""):
        itens = dividir_skips(reg["skips"])
        reg["n_skips"] = len(itens)
        reg["skips_sem_motivo"] = sum(1 for i in itens if not skip_tem_motivo(i))
    else:
        reg["n_skips"] = 0
        reg["skips_sem_motivo"] = 0
    return reg


def parse_registro(texto_nota):
    """Linhas do 'Registro de etapas'. Se um estagio aparece duas vezes, vale a ultima."""
    corpo = secao(texto_nota, "Registro de etapas")
    if corpo is None:
        return {}
    registro = {}
    for linha in corpo.splitlines():
        reg = parse_linha_registro(linha)
        if reg:
            registro[reg["estagio"]] = reg
    return registro


def normalizar_secao(texto):
    """Para comparar versoes: ignora marcacao de checkbox e espacos."""
    if texto is None:
        return None
    t = re.sub(r"\[[xX ]\]", "[ ]", texto)
    linhas = [re.sub(r"\s+", " ", l).strip() for l in t.splitlines()]
    return "\n".join(l for l in linhas if l)


def checar_dod(texto_nota):
    """Quantas das 5 categorias da Definicao de pronto estao preenchidas."""
    corpo = secao(texto_nota, "Definicao de pronto")
    if corpo is None:
        return 0
    blocos = {}
    atual = None
    for linha in corpo.splitlines():
        ln = normalizar(linha)
        m = re.match(r"^\s*[-*]\s*\*\*([^*:]+):?\*\*:?(.*)$", ln)
        if m and m.group(1).strip() in CATEGORIAS_DOD:
            atual = m.group(1).strip()
            blocos[atual] = [m.group(2)]
            continue
        if atual:
            blocos[atual].append(ln)
    ok = 0
    for cat in CATEGORIAS_DOD:
        linhas = blocos.get(cat, [])
        texto = "\n".join(linhas)
        if re.search(r"nao se aplica\s*-\s*\S", texto):
            ok += 1
        elif any(re.search(r"\[[x ]\]\s*\S", l) and "..." not in l for l in linhas):
            ok += 1
    return ok


def checar_prova(texto_nota):
    corpo = secao(texto_nota, "Prova com dado real", nivel=3)
    if corpo is None:
        return False
    t = normalizar(corpo).strip()
    if not t or t.startswith("<"):
        return False
    return bool(re.search(r"fonte|nao se aplica\s*-\s*\S|prova indisponivel\s*-\s*\S", t))


def checar_contrato(texto_nota):
    corpo = secao(texto_nota, "Contrato")
    return bool(corpo and re.search(r"\bC1\b", corpo))


# ---------------------------------------------------------------- modelo


class Nota:
    def __init__(self, caminho_rel, texto):
        self.caminho = caminho_rel
        self.texto = texto
        self.fm = parse_frontmatter(texto)
        self.id = self.fm.get("id") if isinstance(self.fm.get("id"), str) else None
        self.tipo = normalizar(self.fm.get("tipo", "")) if isinstance(self.fm.get("tipo"), str) else ""
        self.registro = parse_registro(texto)
        self.historico = None  # lista de (sha, data, assunto, caminho)
        self.versoes = None    # textos, na mesma ordem do historico
        self.commits_id = []   # commits do vault que citam o ID: (sha, data, assunto, rotulo)
        pr = self.fm.get("pr", [])
        self.prs = [p for p in (pr if isinstance(pr, list) else [pr]) if p.startswith("http")]
        self.stem = os.path.splitext(os.path.basename(caminho_rel))[0]

    def rotulos(self, rotulo):
        return [c for c in self.commits_id if c[3] == rotulo]

    @property
    def fluxo(self):
        if self.registro or any(c[3] in ESTAGIOS_NOVOS for c in self.commits_id):
            return "novo"
        return "antigo"

    def concluida_em(self):
        """Data de conclusao: ultimo commit '<ID>: concluida' ou concluida_em do frontmatter."""
        c = self.rotulos("concluida")
        if c:
            return c[-1][1]
        v = self.fm.get("concluida_em")
        if isinstance(v, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
            return datetime.fromisoformat(v + "T23:59:59")
        return None

    def criada_em(self):
        datas = [c[1] for c in self.commits_id]
        if self.historico:
            datas.append(self.historico[0][1])
        return min(datas) if datas else None


class Vault:
    def __init__(self, caminho_vault, pasta_tasks):
        self.git = Git(caminho_vault)
        base = os.path.join(caminho_vault, pasta_tasks)
        self.notas = []
        self.sem_id = 0
        for raiz, _dirs, arquivos in os.walk(base):
            for nome in arquivos:
                if not nome.endswith(".md"):
                    continue
                cheio = os.path.join(raiz, nome)
                with open(cheio, encoding="utf-8", errors="replace") as f:
                    texto = f.read()
                rel = os.path.relpath(cheio, self.git.raiz).replace("\\", "/")
                nota = Nota(rel, texto)
                if nota.id:
                    self.notas.append(nota)
                elif nota.fm:
                    self.sem_id += 1
        self.por_id = {n.id: n for n in self.notas}
        pasta_rel = os.path.relpath(base, self.git.raiz).replace("\\", "/")
        self._historicos = self.git.historicos(pasta_rel, [n.caminho for n in self.notas])
        self.por_stem = {normalizar(n.stem): n for n in self.notas}
        self._indexar_commits()

    def _indexar_commits(self):
        for sha, data, assunto in self.git.commits():
            m = COMMIT_ESTAGIO_RE.match(assunto)
            rotulo_id, rotulo = None, None
            if m and m.group(1) in self.por_id and normalizar(m.group(2)) in ROTULOS:
                rotulo_id, rotulo = m.group(1), normalizar(m.group(2))
            citados = set(t for t in ID_RE.findall(assunto) if t in self.por_id)
            for i in citados:
                self.por_id[i].commits_id.append((sha, data, "", rotulo if i == rotulo_id else None))

    def carregar_historicos(self, notas):
        """Le todas as versoes das notas pedidas numa chamada so do git cat-file."""
        faltam = [n for n in notas if n.historico is None]
        pedidos = []
        for n in faltam:
            n.historico = self._historicos.get(n.caminho, [])
            pedidos.extend("%s:%s" % (h[0], h[3]) for h in n.historico)
        textos = self.git.conteudos(pedidos)
        pos = 0
        for n in faltam:
            n.versoes = textos[pos:pos + len(n.historico)]
            pos += len(n.historico)


# ---------------------------------------------------------------- indicadores


def indicador(valor, ids, unidade="", detalhe=None, **extra):
    ind = {"valor": valor, "n": len(ids), "ids": sorted(ids), "unidade": unidade}
    if detalhe is not None:
        ind["detalhe"] = {k: detalhe[k] for k in sorted(detalhe)}
    ind.update(extra)
    return ind


def percentual(sim_ids, base_ids, **extra):
    """Percentual com a regra N < 10: abaixo disso, so contagem e IDs."""
    n = len(base_ids)
    ind = {"n": n, "ids": sorted(base_ids), "unidade": "%", "contagem": len(sim_ids), "ids_sim": sorted(sim_ids)}
    if n >= N_MINIMO_PERCENTUAL:
        ind["valor"] = round(100.0 * len(sim_ids) / n, 1)
    else:
        ind["valor"] = None
        ind["nota"] = "N < %d: sem percentual" % N_MINIMO_PERCENTUAL
    ind.update(extra)
    return ind


def no_mes(data, mes):
    return data is not None and data.strftime("%Y-%m") == mes


def tarefas_do_mes(vault, mes):
    ativas = []
    for n in vault.notas:
        if any(no_mes(c[1], mes) for c in n.commits_id):
            ativas.append(n)
            continue
        ce = n.fm.get("concluida_em")
        if isinstance(ce, str) and ce.startswith(mes):
            ativas.append(n)
    return ativas


def tempos_estagio(nota):
    """Horas por estagio pelos commits do vault (fim do estagio = ultimo commit dele)."""
    if not nota.commits_id:
        return {}
    inicio = nota.commits_id[0][1]
    fins = {}
    for e in ORDEM_NOVA:
        cs = nota.rotulos(e)
        if cs:
            fins[e] = cs[-1][1]
    tempos = {}
    anterior = inicio
    for e in ORDEM_NOVA:
        if e not in fins:
            continue
        d = horas(fins[e] - anterior)
        if d >= 0:
            tempos[e] = d
        anterior = fins[e]
    return tempos


def tempo_total(nota):
    conc = nota.rotulos("concluida")
    if not conc or not nota.commits_id:
        return None
    if nota.fluxo == "antigo":
        novas = nota.rotulos("nova")
        inicio = novas[0][1] if novas else nota.commits_id[0][1]
    else:
        inicio = nota.commits_id[0][1]
    d = horas(conc[-1][1] - inicio)
    return d if d >= 0 else None


def estagios_repetidos(nota):
    """Commits a mais do mesmo estagio (retrabalho)."""
    rotulos = ESTAGIOS_NOVOS if nota.fluxo == "novo" else ["revisada"]
    return sum(max(0, len(nota.rotulos(r)) - 1) for r in rotulos)


def contrato_alterado(nota):
    """Primeiro estagio em que Contrato ou Definicao de pronto mudou depois do ultimo commit '<ID>: design'.

    Devolve None (sem commit de design ou sem historico), "" (nao mudou) ou o rotulo do commit.
    """
    designs = nota.rotulos("design")
    if not designs or not nota.historico:
        return None
    data_design = designs[-1][1]
    sha_design = designs[-1][0]
    idx = None
    for i, h in enumerate(nota.historico):
        if h[0] == sha_design or h[1] <= data_design:
            idx = i
        if h[0] == sha_design:
            break
    if idx is None or nota.versoes[idx] is None:
        return None
    base = nota.versoes[idx]
    ref = (normalizar_secao(secao(base, "Contrato")), normalizar_secao(secao(base, "Definicao de pronto")))
    for i in range(idx + 1, len(nota.historico)):
        v = nota.versoes[i]
        if v is None:
            continue
        atual = (normalizar_secao(secao(v, "Contrato")), normalizar_secao(secao(v, "Definicao de pronto")))
        if atual != ref:
            m = COMMIT_ESTAGIO_RE.match(nota.historico[i][2])
            rot = normalizar(m.group(2)) if m and m.group(1) == nota.id else "outro"
            return rot if rot in ROTULOS else "outro"
    return ""


def paradas(nota):
    """Entradas em status bloqueada no historico, por estagio no momento (o motivo em texto nao sai)."""
    if not nota.versoes:
        return []
    saida = []
    anterior = None
    for i, v in enumerate(nota.versoes):
        if v is None:
            continue
        fm = parse_frontmatter(v)
        st = normalizar(fm.get("status", "")) if isinstance(fm.get("status"), str) else ""
        if st == "bloqueada" and anterior != "bloqueada":
            est = fm.get("estagio") if isinstance(fm.get("estagio"), str) else ""
            est = normalizar(est)
            saida.append((nota.historico[i][1], est if est in ESTAGIOS_NOVOS else "desconhecido"))
        anterior = st
    return saida


def autonoma(nota):
    """True se foi do Build ao Ship sem bloqueada; None se nao passou pelos dois."""
    builds, ships = nota.rotulos("build"), nota.rotulos("ship")
    if not builds or not ships:
        return None
    ini, fim = builds[0][1], ships[-1][1]
    for data, _est in paradas(nota):
        if ini <= data <= fim:
            return False
    return True


def epico(id_task):
    """'LIC-005-G' -> 'LIC-005'; 'DEB-011' -> 'DEB-011'."""
    return "-".join(id_task.split("-")[:2])


def defeitos_escapados(vault, mes, janela):
    """Task tipo fix criada no mes que cita (link ou ID) task concluida ate <janela> dias antes."""
    achados = []  # (fix_id, origem_id)
    for n in vault.notas:
        if n.tipo != "fix":
            continue
        criada = n.criada_em()
        if not no_mes(criada, mes):
            continue
        corpo = n.texto.split("---", 2)[-1] if n.texto.startswith("---") else n.texto
        alvos = set()
        for link in LINK_RE.findall(corpo):
            alvo = vault.por_stem.get(normalizar(link.strip()))
            if alvo:
                alvos.add(alvo)
        for t in ID_RE.findall(corpo):
            if t in vault.por_id:
                alvos.add(vault.por_id[t])
        # exclui o que e relacao de plano, nao defeito: pai, depende-de e tasks do mesmo epico
        relacionadas = set()
        for chave in ("pai", "depende-de"):
            v = n.fm.get(chave)
            for item in (v if isinstance(v, list) else [v] if isinstance(v, str) else []):
                for link in LINK_RE.findall(item):
                    alvo = vault.por_stem.get(normalizar(link.strip()))
                    if alvo:
                        relacionadas.add(alvo.id)
        familia = epico(n.id)
        for alvo in alvos:
            if alvo is n or alvo.id in relacionadas or epico(alvo.id) == familia:
                continue
            conc = alvo.concluida_em()
            if conc is None:
                continue
            dias = (criada.replace(tzinfo=None) - conc.replace(tzinfo=None)).total_seconds() / 86400.0
            if 0 <= dias <= janela:
                achados.append((n.id, alvo.id))
    return achados


# ---------------------------------------------------------------- PR via gh


def consultar_pr(url, repos):
    m = re.match(r"https://github\.com/([^/]+/[^/]+)/pull/(\d+)", url)
    if not m:
        return {"estado": "url invalida"}
    if repos and m.group(1).lower() not in {r.lower() for r in repos}:
        return {"estado": "fora da config"}
    try:
        res = subprocess.run(
            ["gh", "pr", "view", url, "--json", "createdAt,mergedAt,commits,reviews,statusCheckRollup"],
            capture_output=True, check=False, timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired):
        return {"estado": "indisponivel"}
    if res.returncode != 0:
        return {"estado": "indisponivel"}
    try:
        dados = json.loads(res.stdout.decode("utf-8", errors="replace"))
    except ValueError:
        return {"estado": "indisponivel"}
    criado = parse_data_iso(dados["createdAt"].replace("Z", "+00:00"))
    depois = 0
    for c in dados.get("commits") or []:
        d = c.get("committedDate")
        if d and parse_data_iso(d.replace("Z", "+00:00")) > criado:
            depois += 1
    changes = sum(1 for r in dados.get("reviews") or [] if r.get("state") == "CHANGES_REQUESTED")
    ci_vermelho = any(
        (c.get("conclusion") or c.get("state") or "").upper() in ("FAILURE", "ERROR", "TIMED_OUT")
        for c in dados.get("statusCheckRollup") or []
    )
    return {
        "estado": "ok",
        "merged_at": dados.get("mergedAt"),
        "commits_depois_da_abertura": depois,
        "changes_requested": changes,
        "ci_vermelho": ci_vermelho,
    }


# ---------------------------------------------------------------- calculo por mes


def calcular_mes(vault, mes, config, usar_gh, cache_pr):
    janela = int(config.get("janela_defeito_dias", 30))
    ativas = tarefas_do_mes(vault, mes)
    vault.carregar_historicos(ativas)
    escapados = defeitos_escapados(vault, mes, janela)
    resultado = {"mes": mes, "fluxo_novo": {}, "fluxo_antigo": {}}

    novas = [n for n in ativas if n.fluxo == "novo"]
    antigas = [n for n in ativas if n.fluxo == "antigo"]
    resultado["fluxo_novo"]["tasks"] = indicador(len(novas), [n.id for n in novas], "tasks")
    resultado["fluxo_antigo"]["tasks"] = indicador(len(antigas), [n.id for n in antigas], "tasks")

    # --- fluxo novo
    g = {"A": {}, "B": {}, "C": {}, "D": {}}

    # A. A nota acertou?
    alt, base_alt = {}, []
    for n in novas:
        r = contrato_alterado(n)
        if r is None:
            continue
        base_alt.append(n.id)
        if r:
            alt[n.id] = r
    g["A"]["contrato_ou_dod_alterado_apos_design"] = percentual(
        list(alt), base_alt, estagio_da_alteracao=alt
    )
    desv = {n.id: n.registro["build"]["campos"]["desvios"] for n in novas
            if "build" in n.registro and isinstance(n.registro["build"]["campos"].get("desvios"), int)}
    g["A"]["desvios_por_task"] = indicador(
        resumo_numerico(list(desv.values())), list(desv), "desvios", detalhe=desv
    )
    par_por_motivo, par_ids = {}, {}
    for n in novas:
        ps = paradas(n)
        if ps:
            par_ids[n.id] = len(ps)
        for _d, est in ps:
            par_por_motivo[est] = par_por_motivo.get(est, 0) + 1
    g["A"]["paradas_bloqueada"] = indicador(
        sum(par_ids.values()), list(par_ids), "paradas", detalhe=par_ids,
        por_estagio=par_por_motivo,
        nota="motivo = estagio no momento da parada; o texto do motivo nao sai (LGPD)",
    )
    fixes = sorted({f for f, _o in escapados})
    g["A"]["defeito_escapado"] = indicador(
        len(fixes), fixes, "fixes",
        origens=sorted({o for _f, o in escapados}),
        pares=[[f, o] for f, o in sorted(escapados)],
        aproximado=True, janela_dias=janela,
    )

    # B. O fluxo andou bem?
    concl = [n for n in novas if no_mes(n.concluida_em(), mes) and n.rotulos("concluida")]
    tt = {n.id: tempo_total(n) for n in concl}
    tt = {k: v for k, v in tt.items() if v is not None}
    g["B"]["tempo_total_horas"] = indicador(resumo_numerico(list(tt.values())), list(tt), "h", detalhe=tt,
                                            nota="tasks concluidas no mes")
    por_estagio = {}
    for e in ORDEM_NOVA:
        vals = {}
        for n in novas:
            t = tempos_estagio(n)
            cs = n.rotulos(e)
            if e in t and cs and no_mes(cs[-1][1], mes):
                vals[n.id] = t[e]
        por_estagio[e] = indicador(resumo_numerico(list(vals.values())), list(vals), "h", detalhe=vals)
    g["B"]["tempo_por_estagio_horas"] = por_estagio
    rep = {n.id: estagios_repetidos(n) for n in novas}
    rep = {k: v for k, v in rep.items() if v > 0}
    g["B"]["retrabalho_estagio_repetido"] = indicador(sum(rep.values()), list(rep), "commits a mais", detalhe=rep)
    for e in ("build", "verify"):
        rod = {n.id: n.registro[e]["campos"]["rodadas"] for n in novas
               if e in n.registro and isinstance(n.registro[e]["campos"].get("rodadas"), int)}
        g["B"]["rodadas_%s" % e] = indicador(resumo_numerico(list(rod.values())), list(rod), "rodadas", detalhe=rod)
    aut_base, aut_sim = [], []
    for n in novas:
        ships = n.rotulos("ship")
        if not ships or not no_mes(ships[-1][1], mes):
            continue
        a = autonoma(n)
        if a is None:
            continue
        aut_base.append(n.id)
        if a:
            aut_sim.append(n.id)
    g["B"]["autonomia_build_ship"] = percentual(aut_sim, aut_base)
    prs = {}
    if usar_gh:
        for n in novas:
            for url in n.prs:
                if url not in cache_pr:
                    cache_pr[url] = consultar_pr(url, config.get("repositorios", []))
                prs.setdefault(n.id, []).append(cache_pr[url])
    pr_ids = sorted(prs)
    indisp = sorted(i for i, l in prs.items() if any(p["estado"] == "indisponivel" for p in l))
    fora = sorted(i for i, l in prs.items() if any(p["estado"] in ("fora da config", "url invalida") for p in l))
    ok = {i: [p for p in l if p["estado"] == "ok"] for i, l in prs.items()}
    g["B"]["pr"] = {
        "n": len(pr_ids), "ids": pr_ids,
        "estado": "nao consultado (--sem-gh)" if not usar_gh else "ok",
        "indisponivel": indisp,
        "fora_da_config": fora,
        "mergeados": sorted(i for i, l in ok.items() if l and all(p["merged_at"] for p in l)),
        "commits_depois_da_abertura": {i: sum(p["commits_depois_da_abertura"] for p in l) for i, l in ok.items() if l},
        "changes_requested": {i: sum(p["changes_requested"] for p in l) for i, l in ok.items() if l},
        "ci_vermelho": sorted(i for i, l in ok.items() if any(p["ci_vermelho"] for p in l)),
    }

    # C. O Verify acertou?
    bloq = {n.id: n.registro["verify"]["campos"]["bloqueantes"] for n in novas
            if "verify" in n.registro and isinstance(n.registro["verify"]["campos"].get("bloqueantes"), int)}
    origens = {o for _f, o in escapados}
    depois = {}
    for i in bloq:
        motivos = []
        if i in g["B"]["pr"]["ci_vermelho"]:
            motivos.append("ci_vermelho")
        if g["B"]["pr"]["changes_requested"].get(i):
            motivos.append("changes_requested")
        if i in origens:
            motivos.append("defeito_escapado")
        if motivos:
            depois[i] = motivos
    g["C"]["bloqueantes_no_verify"] = indicador(sum(bloq.values()), list(bloq), "bloqueantes", detalhe=bloq)
    g["C"]["problemas_depois_do_verify"] = indicador(
        len(depois), list(depois), "tasks", detalhe=depois,
        verify_sem_bloqueante=sorted(i for i in depois if bloq.get(i) == 0),
        nota="CI vermelho e CHANGES_REQUESTED dependem do gh; defeito escapado e aproximado",
    )
    ref = {n.id: (n.registro["verify"]["campos"].get("refutados"), n.registro["verify"]["campos"].get("candidatos"))
           for n in novas if "verify" in n.registro}
    com_cand = {i: v for i, v in ref.items() if isinstance(v[1], int) and isinstance(v[0], int)}
    if com_cand:
        tot_c = sum(v[1] for v in com_cand.values())
        tot_r = sum(v[0] for v in com_cand.values())
        g["C"]["refutados_sobre_candidatos"] = indicador(
            {"refutados": tot_r, "candidatos": tot_c}, list(com_cand), "contagem",
            detalhe={i: "%d/%d" % (v[0], v[1]) for i, v in com_cand.items()},
        )
    else:
        g["C"]["refutados_sobre_candidatos"] = indicador(
            None, [], "contagem", nota="sem dado: campo candidatos ausente nas linhas verify"
        )
    at = {n.id: n.registro["verify"]["campos"]["atencao"] for n in novas
          if "verify" in n.registro and isinstance(n.registro["verify"]["campos"].get("atencao"), int)}
    g["C"]["atencao_por_task"] = indicador(resumo_numerico(list(at.values())), list(at), "itens", detalhe=at)

    # D. A nota esta bem formada?
    com_registro = [n for n in novas if n.registro]
    dod5 = [n.id for n in com_registro if checar_dod(n.texto) == 5]
    g["D"]["dod_5_categorias"] = percentual(dod5, [n.id for n in com_registro])
    c1 = [n.id for n in com_registro if checar_contrato(n.texto)]
    g["D"]["contrato_com_c1"] = percentual(c1, [n.id for n in com_registro])
    pv = [n.id for n in com_registro if checar_prova(n.texto)]
    g["D"]["prova_com_dado_real"] = percentual(pv, [n.id for n in com_registro])
    linhas_ok = [n.id for n in com_registro if all(r["valida"] for r in n.registro.values())]
    invalidas = {n.id: sorted(e for e, r in n.registro.items() if not r["valida"]) for n in com_registro}
    invalidas = {k: v for k, v in invalidas.items() if v}
    g["D"]["registro_formato_valido"] = percentual(
        linhas_ok, [n.id for n in com_registro], estagios_invalidos=invalidas
    )
    sem_motivo = {n.id: sum(r["skips_sem_motivo"] for r in n.registro.values()) for n in com_registro}
    total_skips = {n.id: sum(r["n_skips"] for r in n.registro.values()) for n in com_registro}
    com_motivo = [i for i in sem_motivo if sem_motivo[i] == 0]
    g["D"]["skips_com_motivo"] = percentual(
        com_motivo, [n.id for n in com_registro],
        skips_sem_motivo={k: v for k, v in sem_motivo.items() if v},
        total_skips=sum(total_skips.values()),
    )
    resultado["fluxo_novo"]["grupos"] = g

    # --- fluxo antigo: so o que da
    concl_a = [n for n in antigas if no_mes(n.concluida_em(), mes) and n.rotulos("concluida")]
    tta = {n.id: tempo_total(n) for n in concl_a}
    tta = {k: v for k, v in tta.items() if v is not None}
    repa = {n.id: estagios_repetidos(n) for n in antigas}
    repa = {k: v for k, v in repa.items() if v > 0}
    resultado["fluxo_antigo"]["grupos"] = {
        "B": {
            "tempo_total_horas": indicador(resumo_numerico(list(tta.values())), list(tta), "h", detalhe=tta,
                                           nota="nova -> concluida; tasks concluidas no mes"),
            "retrabalho_revisada_repetida": indicador(sum(repa.values()), list(repa), "commits a mais", detalhe=repa),
        }
    }
    return resultado


# ---------------------------------------------------------------- saida


def fmt(ind):
    """Texto curto de um indicador para a tabela."""
    if ind is None:
        return "-"
    if ind.get("unidade") == "%":
        if ind.get("valor") is None:
            return "%d de %d" % (ind["contagem"], ind["n"])
        return "%.1f%% (N=%d)" % (ind["valor"], ind["n"])
    v = ind.get("valor")
    if v is None:
        return "- (N=%d)" % ind["n"]
    if isinstance(v, dict) and "mediana" in v:
        return "med %s (%s-%s; N=%d)" % (v["mediana"], v["minimo"], v["maximo"], ind["n"])
    if isinstance(v, dict):
        return " / ".join(str(x) for x in v.values()) + " (N=%d)" % ind["n"]
    return "%s (N=%d)" % (v, ind["n"])


LINHAS_TABELA_NOVO = [
    ("Tasks ativas", lambda r: r["fluxo_novo"]["tasks"]),
    ("A. Contrato/DoD alterado apos Design", lambda r: r["fluxo_novo"]["grupos"]["A"]["contrato_ou_dod_alterado_apos_design"]),
    ("A. Desvios por task (build)", lambda r: r["fluxo_novo"]["grupos"]["A"]["desvios_por_task"]),
    ("A. Paradas (bloqueada)", lambda r: r["fluxo_novo"]["grupos"]["A"]["paradas_bloqueada"]),
    ("A. Defeito escapado (aproximado)", lambda r: r["fluxo_novo"]["grupos"]["A"]["defeito_escapado"]),
    ("B. Tempo total (h)", lambda r: r["fluxo_novo"]["grupos"]["B"]["tempo_total_horas"]),
    ("B. Retrabalho (estagio repetido)", lambda r: r["fluxo_novo"]["grupos"]["B"]["retrabalho_estagio_repetido"]),
    ("B. Rodadas build", lambda r: r["fluxo_novo"]["grupos"]["B"]["rodadas_build"]),
    ("B. Rodadas verify", lambda r: r["fluxo_novo"]["grupos"]["B"]["rodadas_verify"]),
    ("B. Autonomia Build -> Ship", lambda r: r["fluxo_novo"]["grupos"]["B"]["autonomia_build_ship"]),
    ("C. Bloqueantes no Verify", lambda r: r["fluxo_novo"]["grupos"]["C"]["bloqueantes_no_verify"]),
    ("C. Problemas depois do Verify", lambda r: r["fluxo_novo"]["grupos"]["C"]["problemas_depois_do_verify"]),
    ("C. Refutados / candidatos", lambda r: r["fluxo_novo"]["grupos"]["C"]["refutados_sobre_candidatos"]),
    ("C. Atencao por task", lambda r: r["fluxo_novo"]["grupos"]["C"]["atencao_por_task"]),
    ("D. DoD com 5 categorias", lambda r: r["fluxo_novo"]["grupos"]["D"]["dod_5_categorias"]),
    ("D. Contrato com C1", lambda r: r["fluxo_novo"]["grupos"]["D"]["contrato_com_c1"]),
    ("D. Prova com dado real", lambda r: r["fluxo_novo"]["grupos"]["D"]["prova_com_dado_real"]),
    ("D. Registro em formato valido", lambda r: r["fluxo_novo"]["grupos"]["D"]["registro_formato_valido"]),
    ("D. Skips com motivo", lambda r: r["fluxo_novo"]["grupos"]["D"]["skips_com_motivo"]),
]
LINHAS_TABELA_ANTIGO = [
    ("Tasks ativas", lambda r: r["fluxo_antigo"]["tasks"]),
    ("B. Tempo total (h)", lambda r: r["fluxo_antigo"]["grupos"]["B"]["tempo_total_horas"]),
    ("B. Retrabalho (revisada repetida)", lambda r: r["fluxo_antigo"]["grupos"]["B"]["retrabalho_revisada_repetida"]),
]


def fora_do_padrao(res):
    """Top 3 do mes: pontos = retrabalho + desvios + paradas; desempate pelo maior tempo total."""
    g = res["fluxo_novo"]["grupos"]
    ids = set(res["fluxo_novo"]["tasks"]["ids"])
    rep = g["B"]["retrabalho_estagio_repetido"].get("detalhe", {})
    desv = g["A"]["desvios_por_task"].get("detalhe", {})
    par = g["A"]["paradas_bloqueada"].get("detalhe", {})
    tt = g["B"]["tempo_total_horas"].get("detalhe", {})
    linhas = []
    for i in ids:
        pts = rep.get(i, 0) + desv.get(i, 0) + par.get(i, 0)
        linhas.append((pts, tt.get(i, 0) or 0, i))
    linhas.sort(key=lambda x: (-x[0], -x[1], x[2]))
    return [
        {"id": i, "pontos": p, "retrabalho": rep.get(i, 0), "desvios": desv.get(i, 0),
         "paradas": par.get(i, 0), "tempo_total_h": tt.get(i)}
        for p, _t, i in linhas[:3] if p > 0 or tt.get(i)
    ]


def gerar_markdown(dados):
    atual = dados["periodos"][0]
    meses = [p["mes"] for p in dados["periodos"]]
    g = atual["fluxo_novo"]["grupos"]
    out = []
    out.append("# Metricas das notas de task - %s" % atual["mes"])
    out.append("")
    out.append("Gerado em %s por `scripts/metricas.py` (v%s). So IDs e numeros." % (dados["gerado_em"], dados["versao"]))
    out.append("Os indicadores servem para achar onde olhar. Nao sao meta.")
    out.append("")
    out.append("## Resumo")
    out.append("")
    tt = g["B"]["tempo_total_horas"]["valor"]
    alt = g["A"]["contrato_ou_dod_alterado_apos_design"]
    resumo = [
        "- Tasks com atividade: %d no fluxo novo, %d no fluxo antigo." % (
            atual["fluxo_novo"]["tasks"]["n"], atual["fluxo_antigo"]["tasks"]["n"]),
        "- Tempo total (fluxo novo, concluidas no mes): %s." % (
            "mediana %s h, N=%d" % (tt["mediana"], g["B"]["tempo_total_horas"]["n"]) if tt else "sem dado"),
        "- Retrabalho: %d tasks com estagio repetido; Contrato/DoD alterado apos Design: %s." % (
            g["B"]["retrabalho_estagio_repetido"]["n"], fmt(alt)),
        "- Defeito escapado (aproximado): %d; problemas depois do Verify: %d tasks." % (
            g["A"]["defeito_escapado"]["valor"], g["C"]["problemas_depois_do_verify"]["n"]),
        "- Registro em formato valido: %s; skips com motivo: %s." % (
            fmt(g["D"]["registro_formato_valido"]), fmt(g["D"]["skips_com_motivo"])),
    ]
    out.extend(resumo[:5])
    out.append("")
    for titulo, linhas, nota in (
        ("Fluxo novo: mes x meses anteriores", LINHAS_TABELA_NOVO, None),
        ("Fluxo antigo (linha de base): mes x meses anteriores", LINHAS_TABELA_ANTIGO,
         "Sem Registro: so tempo total (nova -> concluida) e retrabalho (revisada repetida)."),
    ):
        out.append("## %s" % titulo)
        out.append("")
        if nota:
            out.append(nota)
            out.append("")
        out.append("| Indicador | " + " | ".join(meses) + " |")
        out.append("| --- | " + " | ".join("---" for _ in meses) + " |")
        for nome, f in linhas:
            out.append("| %s | " % nome + " | ".join(fmt(f(p)) for p in dados["periodos"]) + " |")
        out.append("")
    out.append("Formato: `med X (min-max; N)` para tempos e contagens; `k de N` quando N < %d (sem percentual)." % N_MINIMO_PERCENTUAL)
    out.append("")
    out.append("## 3 tasks mais fora do padrao (%s)" % atual["mes"])
    out.append("")
    out.append("Criterio: pontos = retrabalho (commits a mais do mesmo estagio) + desvios (linha build) + paradas (bloqueada). Empate: maior tempo total.")
    out.append("")
    top = dados["fora_do_padrao"]
    if top:
        out.append("| ID | Pontos | Retrabalho | Desvios | Paradas | Tempo total (h) |")
        out.append("| --- | --- | --- | --- | --- | --- |")
        for t in top:
            out.append("| %s | %d | %d | %d | %d | %s |" % (
                t["id"], t["pontos"], t["retrabalho"], t["desvios"], t["paradas"],
                "-" if t["tempo_total_h"] is None else t["tempo_total_h"]))
    else:
        out.append("Nenhuma task com pontos no mes.")
    out.append("")
    out.append("## IDs por indicador (%s, fluxo novo)" % atual["mes"])
    out.append("")
    for nome, f in LINHAS_TABELA_NOVO:
        ind = f(atual)
        ids = ind.get("ids_sim", ind.get("ids", [])) if ind.get("unidade") == "%" else ind.get("ids", [])
        extra = ""
        if ind.get("unidade") == "%":
            extra = " (de %d: %s)" % (ind["n"], ", ".join(ind["ids"]) or "-")
        out.append("- %s: %s%s" % (nome, ", ".join(ids) or "-", extra))
    pr = g["B"]["pr"]
    out.append("- B. PR (gh): %s; tasks com PR: %s; mergeados: %s; indisponivel: %s; fora da config: %s; CI vermelho: %s" % (
        pr["estado"], ", ".join(pr["ids"]) or "-", ", ".join(pr["mergeados"]) or "-",
        ", ".join(pr["indisponivel"]) or "-", ", ".join(pr["fora_da_config"]) or "-",
        ", ".join(pr["ci_vermelho"]) or "-"))
    out.append("")
    out.append("Detalhe completo (valores por ID): `metricas-%s.json`." % atual["mes"])
    out.append("")
    out.append("Gerado por script elaborado com suporte de IA - Revisado por [Nome do Responsavel]")
    out.append("")
    return "\n".join(out)


VERSAO = "1"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Metricas mensais das notas de task (so leitura no vault).")
    ap.add_argument("--config", required=True)
    ap.add_argument("--mes", required=True, help="AAAA-MM")
    ap.add_argument("--meses-anteriores", type=int, default=2)
    ap.add_argument("--saida", required=True)
    ap.add_argument("--sem-gh", action="store_true", help="nao consulta PRs no GitHub")
    args = ap.parse_args(argv)

    if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", args.mes):
        ap.error("--mes deve ser AAAA-MM")
    with open(args.config, encoding="utf-8") as f:
        config = json.load(f)
    vault = Vault(config["vault"], config.get("pasta_tasks", "."))
    cache_pr = {}
    periodos = [
        calcular_mes(vault, m, config, not args.sem_gh, cache_pr)
        for m in meses_analisados(args.mes, args.meses_anteriores)
    ]
    dados = {
        "versao": VERSAO,
        "gerado_em": date.today().isoformat(),
        "mes": args.mes,
        "meses_anteriores": args.meses_anteriores,
        "notas_lidas": len(vault.notas),
        "notas_sem_id": vault.sem_id,
        "regras": {
            "n_minimo_percentual": N_MINIMO_PERCENTUAL,
            "notas_do_mes": "commit do vault com o ID no mes ou concluida_em no mes",
            "lgpd": "so IDs e numeros; nenhum texto de nota",
        },
        "periodos": periodos,
    }
    dados["fora_do_padrao"] = fora_do_padrao(periodos[0])

    os.makedirs(args.saida, exist_ok=True)
    base = os.path.join(args.saida, "metricas-%s" % args.mes)
    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2, default=str)
    with open(base + ".md", "w", encoding="utf-8") as f:
        f.write(gerar_markdown(dados))
    print("gerado: %s.json e %s.md" % (base, base))
    return 0


if __name__ == "__main__":
    sys.exit(main())
