# deai-text

Remove AI writing patterns from any text. Fiction, articles, marketing copy, reports — if it sounds like a machine wrote it, this skill finds the patterns and fixes them.

Remove padrões de escrita de IA de qualquer texto. Ficção, artigos, copy de marketing, relatórios — se parece que uma máquina escreveu, essa skill encontra os padrões e corrige.

---

**[English](#english)** | **[Português BR](#português-br)**

---

## English

### What it does

deai-text audits text for AI writing patterns and rewrites it to sound human. Four steps:

1. **Audit** — every pattern found, quoted, with a rule ID
2. **Rewrite** — a clean version with the patterns removed
3. **What changed** — the meaningful edits, and what was kept on purpose
4. **Second pass** — re-reads the rewrite to catch what survived

Two things make it more than a word blacklist:

**Separate catalogs per language.** The Portuguese catalog is not a translation of the English one. Half of what marks AI text in Portuguese has no English equivalent — the trailing gerund (`…, garantindo mais segurança`), `possui` standing in for `tem`, translation calques like `acionável` and `alavancar` — and half the English catalog has no Portuguese counterpart. Reading the wrong one finds almost nothing.

**A regression suite.** Twelve rule IDs, each with cases that prove it fires and cases that prove it *doesn't* fire where it shouldn't. See [Development](#development).

### The twelve rule IDs

| ID | Category |
|---|---|
| `AI-1` | Tier 1 vocabulary — replace on sight |
| `AI-2` | Tier 2 cluster — 2+ in the same paragraph |
| `AI-3` | Tier 3 density + overused adverbs |
| `AI-4` | Rhythm uniformity — sentence and paragraph length |
| `AI-5` | Absent voice — relentless neutrality |
| `AI-6` | Formatting — em dashes, bold, emoji, bullet spam, excessive structure |
| `AI-7` | Transition filler and template phrases |
| `AI-8` | Assistant artifacts — chatbot tics, sycophancy, reasoning-chain leakage |
| `AI-9` | Inflation and evasion — copula avoidance, vague attribution, promotional language |
| `AI-10` | Structural constructions (31 of them, cited as `AI-10 (C-5)`) |
| `AI-11` | Emotion by proxy — physical tells, dead metaphors, vague interiority |
| `AI-12` | Intrusive narration — narrator-as-analyst, elegant variation, atmospheric front-loading |

### Project structure

```
deai-text/
├── SKILL.md                          # rule IDs, detection method, output format
├── skills/
│   ├── references/
│   │   ├── vocabulary.md             # Tier 1/2/3, English
│   │   ├── vocabulary-pt-br.md       # Tier 1/2/3, Portuguese + gerund, copula, calques
│   │   ├── constructions.md          # 31 structural patterns
│   │   ├── fiction-phrases.md        # physical tells, dead metaphors, clichés
│   │   └── nonfiction-patterns.md    # formatting, transitions, assistant artifacts
│   └── prompts/
│       ├── standalone-en.md          # condensed prompt for any LLM (English)
│       ├── standalone-pt-br.md       # condensed prompt for any LLM (PT-BR)
│       └── bundle.md                 # GENERATED: the whole skill in one file
├── tests/                            # regression suite — see AGENTS.md
├── loops/                            # coverage goal loop
├── LICENSE
└── AGENTS.md                         # for editing the skill itself
```

### Installation

#### As a plugin (recommended)

```bash
claude plugin marketplace add kayquer/deai-text
claude plugin install deai-text
```

The repo is both the marketplace and the plugin. `claude plugin details deai-text` shows what it loads.

#### As a personal skill

```bash
git clone https://github.com/kayquer/deai-text.git ~/.claude/skills/deai-text
```

#### As a project skill

```bash
git clone https://github.com/kayquer/deai-text.git your-project/.claude/skills/deai-text
```

Claude picks it up on the next session. Same layout works for Claude Desktop — put the folder under `.claude/skills/` inside your selected workspace.

#### Any other LLM

Paste `skills/prompts/bundle.md` as a system prompt — it is `SKILL.md` plus every catalog flattened into one file. If your context budget is tight, `skills/prompts/standalone-en.md` is the condensed version.

### Usage

- "De-AI this text: [paste]"
- "Remove AI patterns from this article"
- "Audit this for AI writing tells"
- "Humanize this writing"
- "Tira a cara de IA desse texto"

The skill triggers automatically on requests like these.

### Development

The skill has a regression suite. Cases live in `tests/casos/`, each one asserting which rule IDs must fire, and — more importantly — which terms must survive untouched.

```bash
./init.sh                     # run everything
./init.sh caso-01             # one case
./init.sh --cobertura         # coverage matrix; free, makes no API calls
DEAI_MODELO=opus ./init.sh    # different model (default: sonnet)
```

The runner does not compare text — LLM output is not deterministic, and the product here is rewritten prose that changes every run by design. It checks three things: the expected rule IDs appeared, the `nao-marca` terms survived in section 2, and the `deve-conter` anchors appeared.

**Read [`AGENTS.md`](AGENTS.md) before editing anything.** This repo contains AI slop on purpose — it is the test input. An agent that "improves" the text in `tests/casos/` breaks the suite silently: the tests keep running and stop detecting anything.

---

## Português BR

### O que faz

deai-text audita texto em busca de padrões de escrita de IA e reescreve para soar humano. Quatro etapas:

1. **Auditoria** — cada padrão encontrado, citado, com um ID de regra
2. **Reescrita** — a versão limpa, sem os padrões
3. **O que mudou** — as edições que importam, e o que foi mantido de propósito
4. **Segunda passada** — relê a reescrita para pegar o que sobreviveu

Duas coisas que fazem dela mais que uma lista de palavras proibidas:

**Catálogos separados por idioma.** O catálogo em português não é a tradução do catálogo em inglês. Metade do que denuncia texto de IA em português não existe em inglês — o gerúndio final (`…, garantindo mais segurança`), o `possui` no lugar de `tem`, os decalques de tradução como `acionável` e `alavancar` — e metade do catálogo em inglês não tem equivalente em português. Ler o catálogo errado não encontra quase nada.

**Uma suíte de regressão.** Doze IDs de regra, cada um com casos que provam que ela dispara e casos que provam que ela **não** dispara onde não deve. Ver [Desenvolvimento](#desenvolvimento).

### Os doze IDs

| ID | Categoria |
|---|---|
| `AI-1` | Vocabulário nível 1 — substituir sempre |
| `AI-2` | Cluster nível 2 — 2+ no mesmo parágrafo |
| `AI-3` | Densidade nível 3 + advérbios superusados |
| `AI-4` | Uniformidade de ritmo — comprimento de frase e parágrafo |
| `AI-5` | Ausência de voz — neutralidade implacável |
| `AI-6` | Formatação — travessão, negrito, emoji, excesso de bullet e de estrutura |
| `AI-7` | Conectores de enchimento e frases-molde |
| `AI-8` | Artefatos de assistente — tique de chatbot, bajulação, cadeia de raciocínio |
| `AI-9` | Inflação e evasão — evasão de cópula, atribuição vaga, linguagem promocional |
| `AI-10` | Construções estruturais (31 delas, citadas como `AI-10 (C-5)`) — inclui o gerúndio final |
| `AI-11` | Emoção por procuração — descrição física, metáfora morta, interioridade vaga |
| `AI-12` | Narração intrusiva — narrador-analista, variação elegante, abertura atmosférica |

### Instalação

#### Como plugin (recomendado)

```bash
claude plugin marketplace add kayquer/deai-text
claude plugin install deai-text
```

O repositório é o marketplace e o plugin ao mesmo tempo. `claude plugin details deai-text` mostra o que ele carrega.

#### Como skill pessoal

```bash
git clone https://github.com/kayquer/deai-text.git ~/.claude/skills/deai-text
```

#### Como skill de projeto

```bash
git clone https://github.com/kayquer/deai-text.git seu-projeto/.claude/skills/deai-text
```

O Claude detecta na próxima sessão. O mesmo layout serve para o Claude Desktop — coloque a pasta em `.claude/skills/` dentro da pasta que você selecionou.

#### Qualquer outro LLM

Cole `skills/prompts/bundle.md` como system prompt — é o `SKILL.md` mais todos os catálogos num arquivo só. Se o contexto for curto, `skills/prompts/standalone-pt-br.md` é a versão condensada.

### Como usar

- "Tira a cara de IA desse texto: [cole]"
- "Audite este artigo para padrões de IA"
- "Humanize essa escrita"
- "Esse texto parece escrito por IA, arruma"

A skill dispara automaticamente nesse tipo de pedido.

### Desenvolvimento

```bash
./init.sh                     # roda tudo
./init.sh caso-01             # um caso
./init.sh --cobertura         # matriz de cobertura; grátis, não chama a API
DEAI_MODELO=opus ./init.sh    # outro modelo (default: sonnet)
```

O runner **não compara texto** — output de LLM não é determinístico, e aqui o produto é prosa reescrita, que muda a cada rodada por desenho. Ele verifica três coisas: os IDs esperados apareceram, os termos de `nao-marca` sobreviveram na seção 2, e as âncoras de `deve-conter` apareceram.

**Leia o [`AGENTS.md`](AGENTS.md) antes de editar qualquer coisa.** Este repositório contém slop de IA de propósito — é a entrada dos testes. Um agente que "melhora" o texto de `tests/casos/` quebra a suíte em silêncio: os testes continuam rodando e passam a não detectar nada.

---

## The Accumulation Principle / O Princípio da Acumulação

No single word or pattern makes text bad. The problem is **density**: the same constructions appearing reflexively, repeatedly, and interchangeably. AI writing sounds like AI writing because it reaches for the statistically common option every time.

One em dash is fine. One "jaw tightens" is fine. One "robust" is fine. The fifth one on the same page means the text is running on autopilot.

The corollary matters as much: **do not fix what is correct.** The characteristic failure of a de-AI pass is flagging writing that was never broken — the technically precise `robust standard errors` in an econometrics paper, the `possui matrícula` of a Brazilian property record, the one em dash a human used on purpose. A catalog entry is a reason to look, not a reason to change.

---

Nenhuma palavra ou padrão isolado torna o texto ruim. O problema é **densidade**: as mesmas construções aparecendo reflexivamente, repetidamente e de forma intercambiável. Texto de IA soa como texto de IA porque sempre escolhe a opção estatisticamente mais comum.

Um travessão está ok. Uma "mandíbula cerrou" está ok. Um "robusto" está ok. O quinto na mesma página significa que o texto está no piloto automático.

O corolário importa tanto quanto: **não conserte o que está certo.** O modo de falha característico de uma passada de de-AI é marcar texto que nunca esteve quebrado — o `robust standard errors` preciso de um artigo de econometria, o `possui matrícula` de uma certidão de imóvel, o único travessão que um humano usou de propósito. Entrada de catálogo é motivo para olhar, não motivo para mudar.

---

## Inspirations / Inspirações

- **[BANNED: The Definitive Guide](https://www.reddit.com/r/WritingWithAI/comments/1pecxos/i_constructed_an_exhaustive_anticlich%C3%A9_style/)** — anti-cliché style guide by u/Aggressive_Chicken63 on r/WritingWithAI. The structural constructions, fiction phrases, and the accumulation principle draw heavily from that work.

- **[avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)** by Conor Bronsdon. The tiered vocabulary system (Tier 1 always-flag, Tier 2 cluster-flag, Tier 3 density-flag), adapted from [brandonwise/humanizer](https://github.com/brandonwise/humanizer) vocabulary research, and the four-section output format come from this project.

- The test harness — cases as assertions, retry against flakiness, coverage matrix as a mechanical stopping criterion — follows the design of the [learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering) goal loop.

---

## License / Licença

MIT — see [LICENSE](LICENSE).
