# deai-text

Remove padrões de escrita de IA de qualquer texto. Ficção, artigos, copy de marketing, relatórios — se parece que uma máquina escreveu, essa skill encontra os padrões e corrige.

*Removes AI writing patterns from any text. Fiction, articles, marketing copy, reports.* → [English](#english)

---

## Antes e depois

Três casos reais. Todos saíram da suíte de testes do repo — `tests/casos/` — não foram escritos para o README.

### 1. Release note (o gerúndio final)

> **Antes**
>
> A nova versão do sistema **possui** integração com o gateway de pagamento, **garantindo mais segurança nas transações**. O módulo financeiro **conta com** relatórios automáticos, **proporcionando maior eficiência para a equipe**. A ferramenta **dispõe de** painel personalizado, **permitindo que o gestor acompanhe os indicadores em tempo real** e **contribuindo para uma tomada de decisão mais assertiva**.

> **Depois**
>
> A nova versão integra o gateway de pagamento. Os dados do cartão não passam mais pelo nosso servidor — quem guarda é o adquirente.
>
> O módulo financeiro fecha os relatórios sozinho, todo dia 1º. O painel agora aceita filtro por corretor, que era o pedido mais repetido no suporte.

| ID | O que era |
|---|---|
| `AI-9` | `possui`, `conta com`, `dispõe de` — três fugas de `tem` em três frases |
| `AI-10` | quatro gerúndios finais: `garantindo`, `proporcionando`, `permitindo`, `contribuindo` |
| `AI-1` | `assertiva` como decalque de *accurate* — em português significa outra coisa |

O gerúndio final é **o** tique de texto de IA em português, e não tem equivalente em inglês. Repare no que ele fazia: `garantindo mais segurança` não diz segurança contra o quê. O depois diz — os dados não passam pelo servidor. A oração de gerúndio não estava enfeitando a informação, estava ocupando o lugar dela.

### 2. Artigo institucional (vocabulário e conector)

> **Antes**
>
> **Nos dias de hoje**, **em um mundo cada vez mais digital**, as empresas precisam **alavancar** soluções **robustas** e **abrangentes** para se manterem competitivas. **Além disso**, nossa plataforma **de ponta** **configura-se como** **um verdadeiro divisor de águas**. **Vale ressaltar que** **especialistas apontam** que este é **um marco** para o setor. **Ademais**, a plataforma **possui** uma experiência de usuário impecável. **Por fim**, **o futuro é promissor**.

> **Depois**
>
> Nada. O parágrafo não afirma um fato verificável em cinco frases — nem o que a plataforma faz, nem para quem, nem quem são os especialistas.
>
> A reescrita honesta é uma pergunta: **o que ela faz?** Escreva a resposta e você terá o parágrafo.

| ID | O que era |
|---|---|
| `AI-1` | `nos dias de hoje`, `em um mundo cada vez mais`, `alavancar`, `robustas`, `abrangentes`, `de ponta`, `divisor de águas`, `vale ressaltar`, `o futuro é promissor` |
| `AI-7` | `Além disso`, `Ademais`, `Por fim` — três parágrafos costurados por conector, sem relação lógica entre eles |
| `AI-9` | `configura-se como`, `possui`, `especialistas apontam` sem nomear ninguém, `um marco` |

Este é o caso que a skill mais encontra e o único cujo conserto não é reescrever: é descobrir que não havia texto.

### 3. Resposta de assistente (em inglês)

> **Antes**
>
> **Great question!** **Let's dive into this together.** 🚀
>
> ## Overview
> **To answer your question**, let me **break this down step by step**.
> - **First**, it's important to understand the basics
> - **Second**, we need to consider the broader context
>
> ## Summary
> **I hope this helps!** **Feel free to reach out** if you have any other questions.

> **Depois**
>
> O prazo de carência do saque-aniversário do FGTS é de 90 dias.

| ID | O que era |
|---|---|
| `AI-8` | `Great question!`, `Let's dive in`, `To answer your question`, `break this down step by step`, `I hope this helps!`, `Feel free to reach out` |
| `AI-6` | emoji em título, negrito em tudo, dois cabeçalhos-fórmula e uma lista de bullets num texto de 60 palavras |

### O que ela **não** faz

Igualmente importante — estes quatro passam intactos, e existe caso de teste garantindo isso:

| Texto | Por que sobrevive |
|---|---|
| `erro-padrão robusto agrupado por município` | `robusto` é termo de econometria, não inflação |
| `O imóvel possui matrícula 44.312` | `possui` com posse real, registro cartorial |
| `Vamos supor que o corretor tenha 400 imóveis` | imperativo de quem ensina, não tique de chatbot |
| `Por outro lado, o MySQL…` | um conector marcando o contraste real do texto |

O modo de falha característico de um de-AI não é deixar passar. É **corrigir o que já estava certo**.

---

## Português BR

### O que faz

Quatro etapas:

1. **Auditoria** — cada padrão encontrado, citado, com um ID de regra
2. **Reescrita** — a versão limpa, sem os padrões
3. **O que mudou** — as edições que importam, e o que foi mantido de propósito
4. **Segunda passada** — relê a reescrita para pegar o que sobreviveu

Duas coisas que fazem dela mais que uma lista de palavras proibidas:

**Catálogos separados por idioma.** O catálogo em português não é a tradução do catálogo em inglês. Metade do que denuncia texto de IA em português não existe em inglês — o gerúndio final, o `possui` no lugar de `tem`, os decalques de tradução como `acionável` e `alavancar` — e metade do catálogo em inglês não tem equivalente em português. Ler o catálogo errado não encontra quase nada.

**Uma suíte de regressão.** Doze IDs de regra, cada um com casos que provam que ela dispara **e** casos que provam que ela não dispara onde não deve. Ver [Desenvolvimento](#desenvolvimento).

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

### Estrutura do projeto

```
deai-text/
├── SKILL.md                          # os IDs, método de detecção, formato de saída
├── skills/
│   ├── references/
│   │   ├── vocabulary.md             # níveis 1/2/3, inglês
│   │   ├── vocabulary-pt-br.md       # níveis 1/2/3, português + gerúndio, cópula, decalque
│   │   ├── constructions.md          # 31 construções estruturais
│   │   ├── fiction-phrases.md        # descrição física, metáfora morta, clichê
│   │   └── nonfiction-patterns.md    # formatação, transição, artefato de assistente
│   └── prompts/
│       ├── standalone-en.md          # prompt condensado para qualquer LLM (inglês)
│       ├── standalone-pt-br.md       # prompt condensado para qualquer LLM (PT-BR)
│       └── bundle.md                 # GERADO: a skill inteira num arquivo só
├── tests/                            # suíte de regressão — ver AGENTS.md
├── loops/                            # goal loop de cobertura
├── LICENSE
└── AGENTS.md                         # para quem for editar a skill
```

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

## English

### What it does

Four steps: **audit** (every pattern quoted, with a rule ID) · **rewrite** · **what changed** (including what was kept on purpose) · **second pass** over the rewrite.

Two things make it more than a word blacklist:

**Separate catalogs per language.** The Portuguese catalog is not a translation of the English one. Half of what marks AI text in Portuguese has no English equivalent — the trailing gerund (`…, garantindo mais segurança`), `possui` standing in for `tem`, calques like `acionável` and `alavancar` — and half the English catalog has no Portuguese counterpart. Reading the wrong one finds almost nothing.

**A regression suite.** Twelve rule IDs, each with cases that prove it fires and cases that prove it *doesn't* fire where it shouldn't.

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

### Installation

```bash
# As a plugin (recommended) — the repo is both marketplace and plugin
claude plugin marketplace add kayquer/deai-text
claude plugin install deai-text

# As a personal skill
git clone https://github.com/kayquer/deai-text.git ~/.claude/skills/deai-text

# As a project skill
git clone https://github.com/kayquer/deai-text.git your-project/.claude/skills/deai-text
```

For any other LLM, paste `skills/prompts/bundle.md` as a system prompt — it is `SKILL.md` plus every catalog flattened into one file. `skills/prompts/standalone-en.md` is the condensed version.

### Usage

"De-AI this text: [paste]" · "Remove AI patterns from this article" · "Audit this for AI writing tells" · "Humanize this writing". The skill triggers automatically on requests like these.

### Development

```bash
./init.sh                     # run everything
./init.sh caso-01             # one case
./init.sh --cobertura         # coverage matrix; free, makes no API calls
DEAI_MODELO=opus ./init.sh    # different model (default: sonnet)
```

The runner does not compare text — LLM output is not deterministic, and the product here is rewritten prose that changes every run by design. It checks three things: the expected rule IDs appeared, the `nao-marca` terms survived in section 2, and the `deve-conter` anchors appeared.

**Read [`AGENTS.md`](AGENTS.md) before editing anything.** This repo contains AI slop on purpose — it is the test input. An agent that "improves" the text in `tests/casos/` breaks the suite silently: the tests keep running and stop detecting anything.

---

## O Princípio da Acumulação

Nenhuma palavra ou padrão isolado torna o texto ruim. O problema é **densidade**: as mesmas construções aparecendo reflexivamente, repetidamente e de forma intercambiável. Texto de IA soa como texto de IA porque sempre escolhe a opção estatisticamente mais comum.

Um travessão está ok. Uma "mandíbula cerrou" está ok. Um "robusto" está ok. O quinto na mesma página significa que o texto está no piloto automático.

O corolário importa tanto quanto: **não conserte o que está certo.** O modo de falha característico de uma passada de de-AI é marcar texto que nunca esteve quebrado — o `robust standard errors` preciso de um artigo de econometria, o `possui matrícula` de uma certidão de imóvel, o único travessão que um humano usou de propósito. Entrada de catálogo é motivo para olhar, não motivo para mudar.

*No single word or pattern makes text bad. The problem is **density**. One em dash is fine; the fifth on the same page means the text is on autopilot. And the corollary matters as much: **do not fix what is correct.** A catalog entry is a reason to look, not a reason to change.*

---

## Inspirações / Inspirations

- **[BANNED: The Definitive Guide](https://www.reddit.com/r/WritingWithAI/comments/1pecxos/i_constructed_an_exhaustive_anticlich%C3%A9_style/)** — guia anti-clichê de u/Aggressive_Chicken63 no r/WritingWithAI. As construções estruturais, as frases de ficção e o princípio da acumulação vêm em grande parte dali.

- **[avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)**, de Conor Bronsdon. O sistema de níveis de vocabulário (nível 1 sempre marca, nível 2 marca em cluster, nível 3 marca por densidade), adaptado da pesquisa de vocabulário do [brandonwise/humanizer](https://github.com/brandonwise/humanizer), e o formato de saída em quatro seções vêm deste projeto.

- O harness de testes — casos como asserção, retry contra flakiness, matriz de cobertura como critério de parada mecânico — segue o desenho do goal loop do [learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering).

---

## Licença / License

MIT — ver [LICENSE](LICENSE).
