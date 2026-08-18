#!/usr/bin/env python3
"""Runner de regressão da skill deai-text.

Roda cada caso de `casos/` contra o SKILL.md **deste repo** (não a cópia
instalada em ~/.claude/skills/) e confere quais regras AI-N dispararam.

Não compara texto — output de LLM não é determinístico, e o produto desta skill
é prosa reescrita, que muda a cada rodada por desenho. Verifica três coisas:

  cobertura       toda regra de `espera:` apareceu na tabela de auditoria
  falso positivo  todo termo de `nao-marca:` sobreviveu na seção 2 (Reescrita)
  âncora          todo termo de `deve-conter:` apareceu na saída

Regra extra não reprova. Uso: ./init.sh   ou   python3 tests/verify.py [caso]
"""
import os
import re
import subprocess
import sys
from pathlib import Path

MODELO = os.environ.get("DEAI_MODELO", "sonnet")
TIMEOUT = int(os.environ.get("DEAI_TIMEOUT", "300"))
TENTATIVAS = int(os.environ.get("DEAI_TENTATIVAS", "3"))
AQUI = Path(__file__).resolve().parent
REPO = AQUI.parent

VERDE, VERMELHO, AMARELO, CINZA, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[90m", "\033[0m"

REGRAS = [str(n) for n in range(1, 13)]  # AI-1..AI-12
GENEROS = ("nao-ficcao", "ficcao", "marketing")
IDIOMAS = ("pt", "en")
CHAVES = ("genero", "idioma", "espera", "nao-marca", "contra-teste", "deve-conter")

# Regras que dependem do idioma: o catálogo PT e o EN não se traduzem um no
# outro. A matriz de cobertura exige caso nos dois idiomas só para estas.
BILINGUES = {"1", "2", "3", "7", "8", "9"}


def carregar_skill():
    """Concatena a skill do repo. Testa o arquivo em edição, não o instalado."""
    partes = [REPO / "SKILL.md"]
    partes += sorted((REPO / "skills" / "references").glob("*.md"))
    faltando = [p for p in partes if not p.exists()]
    if faltando:
        sys.exit(f"erro: arquivo da skill não encontrado: {faltando[0]}")
    return "\n\n---\n\n".join(p.read_text(encoding="utf-8") for p in partes)


def parse_caso(caminho):
    """Lê e **valida** um caso. Erro de cabeçalho mata o runner, não vira verde.

    Um caso é uma asserção. Chave com typo, regra inexistente ou contra-teste
    sem termo que sobreviva produzem um caso que passa sem verificar nada — e
    um caso desses é pior que caso nenhum, porque conta como cobertura.
    """
    def erro(msg):
        sys.exit(f"erro: {caminho.name}: {msg}")

    texto = caminho.read_text(encoding="utf-8")
    cabecalho, marcador, entrada = texto.partition("## entrada")
    if not marcador:
        erro("não tem o marcador '## entrada'")
    meta = dict(re.findall(r"^([\w-]+):[ \t]*(.*)$", cabecalho, re.MULTILINE))

    if desconhecidas := sorted(set(meta) - set(CHAVES)):
        erro(f"chave desconhecida: {', '.join(desconhecidas)}"
             f"\n       conhecidas: {', '.join(CHAVES)}")

    def lista(chave):
        bruto = meta.get(chave, "").strip()
        return [x.strip() for x in bruto.split(",") if x.strip()] if bruto else []

    def regras(chave):
        """Normaliza `AI-4` para `4` e recusa o que não é regra."""
        saida = []
        for r in lista(chave):
            n = r.split("-")[-1]
            if n not in REGRAS:
                erro(f"{chave}: '{r}' não é regra (esperado AI-1..AI-{REGRAS[-1]})")
            saida.append(n)
        return saida

    caso = {
        "nome": caminho.stem,
        "genero": meta.get("genero", "nao-ficcao").strip(),
        "idioma": meta.get("idioma", "en").strip(),
        "espera": regras("espera"),
        "nao_marca": lista("nao-marca"),
        "contra_teste": regras("contra-teste"),
        "deve_conter": lista("deve-conter"),
        "entrada": entrada.strip(),
    }

    if caso["genero"] not in GENEROS:
        erro(f"genero: '{caso['genero']}' não existe (use {', '.join(GENEROS)})")
    if caso["idioma"] not in IDIOMAS:
        erro(f"idioma: '{caso['idioma']}' não existe (use {', '.join(IDIOMAS)})")
    if not caso["entrada"]:
        erro("'## entrada' está vazia")
    if not (caso["espera"] or caso["nao_marca"] or caso["deve_conter"]):
        erro("nenhuma asserção — 'espera', 'nao-marca' e 'deve-conter' vazios.\n"
             "       Um caso assim passa verde sem verificar nada. "
             "Causa comum: typo no nome da chave.")
    # `contra-teste` só alimenta a matriz de cobertura; quem assere é `nao-marca`.
    # Sem essa checagem, declarar a regra bastava para a matriz contá-la coberta.
    # ponytail: exige `nao-marca` não vazio, não um termo por regra — amarrar
    # termo↔regra pediria anotação por termo. Subir isso se um caso com 2
    # contra-testes e 1 termo virar problema de verdade.
    if caso["contra_teste"] and not caso["nao_marca"]:
        erro("'contra-teste' declara regra mas 'nao-marca' está vazio.\n"
             "       A matriz contaria a regra como coberta sem asserção nenhuma.")
    # Termo de `nao-marca` que não está na entrada não pode sobreviver a nada:
    # o caso falha 3/3 e o detalhe impresso é `corrigiu indevidamente`, que manda
    # investigar falso positivo da skill. Caso real: `caso-16` asseria
    # `estatisticamente significativo` e a entrada dizia `significativa`,
    # concordando com "diferença". Três chamadas de API para descobrir um typo.
    ausentes = [t for t in caso["nao_marca"] if t.lower() not in caso["entrada"].lower()]
    if ausentes:
        erro(f"'nao-marca' cita termo que não está na entrada: {', '.join(ausentes)}\n"
             "       Um termo que não está no texto não sobrevive a nada — o caso\n"
             "       falharia 3/3 acusando falso positivo que não existe.")
    return caso


def cobertura(casos):
    """Matriz regra × (positivo, contra-teste) × idioma. Não chama o Claude.

    É o critério de parada mecânico do goal loop em `loops/goal-cobertura.md`:
    uma regra só está coberta quando existe caso que a faz disparar E caso que
    prova que ela não dispara onde não deve. Para as regras de `BILINGUES`,
    exige as duas coisas em cada idioma — um catálogo PT sem caso PT é um
    catálogo que ninguém verificou.
    """
    pos = {n: set() for n in REGRAS}   # regra -> {idiomas com caso positivo}
    neg = {n: set() for n in REGRAS}   # regra -> {idiomas com contra-teste}
    for caminho in casos:
        c = parse_caso(caminho)
        for n in c["espera"]:
            pos[n].add(c["idioma"])
        for n in c["contra_teste"]:
            neg[n].add(c["idioma"])

    def coberta(mapa, n):
        """Bilíngue exige caso em pt E em en. As demais, um caso em qualquer um."""
        return set(IDIOMAS) <= mapa[n] if n in BILINGUES else bool(mapa[n])

    def marca(mapa, n, largura):
        """Pad antes de colorir — código ANSI conta como caractere em f-string."""
        tem = mapa[n]
        if n in BILINGUES:
            txt = "/".join(i if i in tem else "·" * len(i) for i in IDIOMAS)
            cor = VERDE if coberta(mapa, n) else (AMARELO if tem else VERMELHO)
        else:
            txt, cor = ("✓", VERDE) if tem else ("✗", VERMELHO)
        return f"{cor}{txt.ljust(largura)}{RESET}"

    print(f"{'regra':<9}{'positivo':<12}contra-teste   {CINZA}(pt/en nas regras "
          f"que dependem de idioma){RESET}")
    incompletas_pos = [n for n in REGRAS if not coberta(pos, n)]
    incompletas_neg = [n for n in REGRAS if not coberta(neg, n)]
    for n in REGRAS:
        print(f"AI-{n:<6}{marca(pos, n, 12)}{marca(neg, n, 0)}")

    total = len(REGRAS)
    fmt = lambda v: ", ".join("AI-" + n for n in v)
    print(f"\npositivo:     {total - len(incompletas_pos)}/{total}"
          + (f"  faltam {fmt(incompletas_pos)}" if incompletas_pos else "  ✓"))
    print(f"contra-teste: {total - len(incompletas_neg)}/{total}"
          + (f"  faltam {fmt(incompletas_neg)}" if incompletas_neg else "  ✓"))
    return 1 if (incompletas_pos or incompletas_neg) else 0


def rodar(skill, caso):
    # `genero` e `idioma` só mudam o comportamento se chegarem ao prompt. Ler do
    # cabeçalho e descartar dá um caso que passa por acidente — foi o que
    # aconteceu no PTC com a flag de destinatário.
    idioma = {"pt": "português do Brasil", "en": "English"}[caso["idioma"]]
    genero = {"ficcao": "ficção / prosa criativa",
              "nao-ficcao": "não-ficção (artigo, relatório, documentação)",
              "marketing": "copy de marketing"}[caso["genero"]]
    prompt = (
        f"{skill}\n\n"
        "---\n\n"
        "Aplique a skill acima ao texto abaixo. "
        f"Idioma do texto: {idioma}. Gênero: {genero}. "
        "Responda no formato de saída padrão da skill, com as quatro seções "
        "numeradas, e com a tabela da seção 1 nomeando o ID (AI-N) de cada "
        "achado.\n\n"
        f"{caso['entrada']}"
    )
    # Prompt vai por stdin, não por argv: ele começa com o frontmatter `---`
    # do SKILL.md, que o CLI interpretaria como flag desconhecida.
    try:
        r = subprocess.run(
            ["claude", "-p", "--model", MODELO],
            input=prompt, capture_output=True, text=True, timeout=TIMEOUT,
        )
    except FileNotFoundError:
        sys.exit("erro: `claude` não está no PATH. Instale o Claude Code.")
    except subprocess.TimeoutExpired:
        return None
    if r.returncode != 0:
        print(f"\n    {CINZA}{r.stderr.strip()[:200]}{RESET}", file=sys.stderr)
        return None
    return r.stdout


# Âncora pelo NÚMERO da seção, não pela palavra: o SKILL.md fixa `## 2. Rewrite`
# em inglês e `## 2. Reescrita` em português, e ancorar no número dispensa uma
# regex por idioma. Aceita 1–4 `#` e `2.` ou `2)`.
INICIO_REESCRITA = re.compile(r"^#{1,4}\s*2\s*[.)]", re.MULTILINE)
FIM_REESCRITA = re.compile(r"^#{1,4}\s*3\s*[.)]", re.MULTILINE)


def reescrita(saida):
    """Extrai só a seção 2 — o texto reescrito.

    A tabela da seção 1 cita o trecho original inteiro, então procurar termo de
    `nao-marca` na saída completa acusa falso positivo garantido: o termo está
    lá, na coluna que diz que ele é problema. A seção 2 é o único lugar onde dá
    para afirmar que a skill mudou — ou não mudou — um termo.
    """
    ini = INICIO_REESCRITA.search(saida)
    if not ini:
        return None
    resto = saida[ini.end():]
    fim = FIM_REESCRITA.search(resto)
    return resto[: fim.start()] if fim else resto


def avaliar(caso, saida):
    """Devolve (ok, faltou, corrigidos_indevidamente, nao_apareceu, sem_secao)."""
    citadas = set(re.findall(r"\bAI-(\d+)\b", saida))
    faltou = sorted(set(caso["espera"]) - citadas, key=int)

    # Contra-teste: o termo tem de sobreviver intacto na reescrita.
    alvo = reescrita(saida)
    sem_secao = alvo is None
    proibidos = [t for t in caso["nao_marca"] if t.lower() not in (alvo or saida).lower()]

    # `deve-conter` procura na saída **inteira**, não só na reescrita: o que ele
    # existe para provar — um achado citado na auditoria, uma nota da seção 3 —
    # fica fora do texto reescrito por desenho.
    ausentes = [t for t in caso["deve_conter"] if t.lower() not in saida.lower()]

    ok = not (faltou or proibidos or ausentes or sem_secao)
    return ok, faltou, proibidos, ausentes, sem_secao


def main():
    casos = sorted((AQUI / "casos").glob("*.md"))
    if not casos:
        sys.exit("erro: nenhum caso encontrado em tests/casos/")

    if "--cobertura" in sys.argv:
        return cobertura(casos)

    if len(sys.argv) > 1:
        casos = [c for c in casos if sys.argv[1] in c.stem]
        if not casos:
            sys.exit(f"erro: nenhum caso casa com '{sys.argv[1]}'")

    skill = carregar_skill()
    print(f"{CINZA}skill: {len(skill.splitlines())} linhas · "
          f"modelo: {MODELO} · {len(casos)} caso(s){RESET}\n")

    falhas = instaveis = 0
    for caminho in casos:
        caso = parse_caso(caminho)
        print(f"{caso['nome']:.<44} ", end="", flush=True)

        # Output de LLM oscila: um caso pode falhar numa rodada e passar na
        # seguinte. Sem retry, a suite acusa regressão que não existe — e pior,
        # cada rodada acusa um caso diferente. Repetir separa quebra de ruído.
        for tentativa in range(1, TENTATIVAS + 1):
            saida = rodar(skill, caso)
            if saida is None:
                ok, faltou, proibidos, ausentes, sem_secao = False, [], [], [], False
                continue
            ok, faltou, proibidos, ausentes, sem_secao = avaliar(caso, saida)
            if ok:
                break

        n = len(caso["espera"])
        if ok and tentativa == 1:
            print(f"{VERDE}PASS{RESET}  ({n}/{n} regras)")
        elif ok:
            instaveis += 1
            print(f"{AMARELO}FLAKY{RESET} (passou na {tentativa}ª de {TENTATIVAS})")
        else:
            falhas += 1
            print(f"{VERMELHO}FAIL{RESET}  ({TENTATIVAS} tentativas)")
            if faltou:
                print(f"    faltou:                 {', '.join('AI-' + x for x in faltou)}")
            if proibidos:
                print(f"    corrigiu indevidamente: {', '.join(proibidos)}")
            if ausentes:
                print(f"    não apareceu:           {', '.join(ausentes)}")
            if sem_secao:
                print(f"    {CINZA}sem seção '2.' na saída — o formato de saída do "
                      f"SKILL.md não foi seguido{RESET}")
            # Sem nenhum dos quatro: nunca houve resposta para avaliar. Continua
            # FAIL — caso não verificado não é caso verde —, mas dizer qual das
            # duas coisas aconteceu é o que separa quebra da skill de ruído de
            # infra. Sem esta linha as duas saem idênticas na tela.
            if not (faltou or proibidos or ausentes or sem_secao):
                print(f"    {CINZA}sem resposta do modelo (timeout de {TIMEOUT}s ou "
                      f"erro da API) — não é regressão da skill{RESET}")

    total = len(casos)
    print(f"\n{total - falhas}/{total} casos ok", end="")
    print(f" · {AMARELO}{instaveis} instável(is){RESET}" if instaveis else "")
    if instaveis:
        print(f"{CINZA}flaky recorrente = asserção frágil ou regra ambígua. "
              f"Ver AGENTS.md.{RESET}")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
