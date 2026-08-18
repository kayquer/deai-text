#!/usr/bin/env python3
"""Gera `prompts/bundle.md` e confere que os prompts avulsos não ficaram para trás.

Duas coisas, e só duas:

  bundle       SKILL.md + skills/references/*.md achatados num arquivo só, para colar em
               LLM que não tem suporte a skill. É GERADO — não edite `bundle.md`.

  --verificar  confere que os prompts avulsos (`standalone-*.md`), que são
               escritos à mão, citam todos os IDs `AI-1..AI-N` do SKILL.md, e
               que o bundle está em dia.

Por que o `--verificar` existe: os prompts avulsos são prosa condensada, não dá
para gerá-los mecanicamente a partir do SKILL.md. O que dá para garantir é que
ninguém acrescente uma regra ao SKILL.md e esqueça de propagá-la — que é
exatamente o jeito de os prompts avulsos virarem uma skill diferente da testada,
em silêncio.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUNDLE = REPO / "skills" / "prompts" / "bundle.md"
AVULSOS = ["standalone-en.md", "standalone-pt-br.md"]

CABECALHO = """<!-- GERADO por tools/build.py — não edite este arquivo.
     Edite SKILL.md / skills/references/*.md e rode `python3 tools/build.py`. -->

# deai-text — bundle completo

A skill inteira num arquivo só, para colar como system prompt em qualquer LLM.
Onde o texto abaixo mandar "read `skills/references/X.md`", a seção correspondente já
está neste mesmo arquivo, mais abaixo.

---

"""


def fontes():
    partes = [REPO / "SKILL.md"] + sorted((REPO / "skills" / "references").glob("*.md"))
    faltando = [p for p in partes if not p.exists()]
    if faltando:
        sys.exit(f"erro: arquivo da skill não encontrado: {faltando[0]}")
    return partes


def gerar():
    """Achata as fontes. Tira o frontmatter YAML — num arquivo colado ele não é
    metadado de skill, é a primeira coisa que o modelo lê."""
    blocos = []
    for p in fontes():
        texto = p.read_text(encoding="utf-8")
        texto = re.sub(r"\A---\n.*?\n---\n", "", texto, flags=re.DOTALL)
        blocos.append(texto.strip())
    return CABECALHO + "\n\n---\n\n".join(blocos) + "\n"


def ids_do_skill():
    ids = set(re.findall(r"\bAI-(\d+)\b", (REPO / "SKILL.md").read_text(encoding="utf-8")))
    if not ids:
        sys.exit("erro: SKILL.md não tem nenhum ID AI-N. O formato mudou?")
    return sorted(ids, key=int)


def verificar():
    problemas = []

    esperado = gerar()
    if not BUNDLE.exists():
        problemas.append(f"{BUNDLE.relative_to(REPO)} não existe — rode `python3 tools/build.py`")
    elif BUNDLE.read_text(encoding="utf-8") != esperado:
        problemas.append(f"{BUNDLE.relative_to(REPO)} está defasado — rode `python3 tools/build.py`")

    ids = ids_do_skill()
    for nome in AVULSOS:
        caminho = REPO / "skills" / "prompts" / nome
        if not caminho.exists():
            problemas.append(f"skills/prompts/{nome} não existe")
            continue
        texto = caminho.read_text(encoding="utf-8")
        faltando = [f"AI-{n}" for n in ids if f"AI-{n}" not in texto]
        if faltando:
            problemas.append(
                f"skills/prompts/{nome} não cita {', '.join(faltando)} — "
                f"regra nova no SKILL.md que não chegou no prompt avulso")

    if problemas:
        print("build desatualizado:", file=sys.stderr)
        for p in problemas:
            print(f"  · {p}", file=sys.stderr)
        return 1
    print(f"build ok · bundle em dia · prompts avulsos citam AI-1..AI-{ids[-1]}")
    return 0


def main():
    if "--verificar" in sys.argv:
        return verificar()
    BUNDLE.write_text(gerar(), encoding="utf-8")
    print(f"escrito: {BUNDLE.relative_to(REPO)} "
          f"({len(BUNDLE.read_text(encoding='utf-8').splitlines())} linhas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
