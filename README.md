# deai-text

Remove AI writing patterns from any text. Fiction, articles, marketing copy, reports — if it sounds like a machine wrote it, this skill finds the patterns and fixes them.

Remova padroes de escrita de IA de qualquer texto. Ficcao, artigos, copy de marketing, relatorios — se parece que uma maquina escreveu, essa skill encontra os padroes e corrige.

---

**[English](#english)** | **[Portugues BR](#portugues-br)**

---

## English

### What it does

deai-text audits text for AI writing patterns and rewrites it to sound human. It works in four steps:

1. **Audit** — identifies every AI pattern, quoting the offending text
2. **Rewrite** — returns a clean version with patterns removed
3. **Diff summary** — lists what changed and why
4. **Second-pass** — re-reads the rewrite to catch anything that survived

The skill uses a tiered vocabulary system (words that are always AI tells vs. words that are only suspicious in clusters), plus catalogs of structural patterns, dead metaphors, physical-tell cliches, and formatting issues.

### What it catches

**Across all text types:**
- Tier 1 vocabulary (delve, robust, seamless, leverage, holistic, cutting-edge, tapestry, etc.)
- Tier 2 cluster detection (harness + navigate + foster in the same paragraph)
- Tier 3 density analysis (significant, innovative, compelling — flagged only when overused)
- Sentence and paragraph length uniformity
- Missing voice / relentless neutrality

**Non-fiction specific:**
- Em dash overuse, bold overuse, emoji in headers
- Transition filler (Moreover, Furthermore, Additionally)
- Chatbot artifacts (Great question!, Let's dive in!, Feel free to reach out)
- Sycophantic tone, acknowledgment loops, reasoning chain artifacts
- Copula avoidance (serves as, features, boasts — instead of is/has)
- Vague attributions, significance inflation, promotional language
- Generic conclusions (The future looks bright, Only time will tell)

**Fiction specific:**
- 31 structural constructions (trailing participles, echo-line poetics, negation formulas, etc.)
- Physical tells used as emotion substitutes (jaw clenching, breath catching, pupils blown)
- Dead metaphors (gravitational attraction, temperature emotions, stone-in-water similes)
- Vague interiority placeholders (something shifted, the weight of it settled)
- Narrator-as-analyst patterns (highlighting, underscoring, showcasing)
- Elegant variation / synonym cycling for character names
- Atmospheric front-loading, faux-edgy banter, ending cliches

### Project structure

```
deai-text/
├── SKILL.md                          # Main skill — audit logic, output format, detection method
├── LICENSE                           # MIT license
├── skills/
│   ├── references/
│   │   ├── vocabulary.md             # Tier 1/2/3 word tables with replacements
│   │   ├── constructions.md          # 31 structural patterns (fiction + general)
│   │   ├── fiction-phrases.md        # Physical tells, dead metaphors, cliches
│   │   └── nonfiction-patterns.md    # Formatting, transitions, chatbot artifacts
│   └── prompts/
│       ├── standalone-en.md          # Condensed prompt for any LLM (English)
│       └── standalone-pt-br.md       # Condensed prompt for any LLM (PT-BR)
```

### Installation

#### Claude Code (CLI)

Clone the repo into your project's `.claude/skills/` directory:

```bash
mkdir -p your-project/.claude/skills
git clone https://github.com/kayquer/deai-text.git your-project/.claude/skills/deai-text
```

Or if you already cloned it somewhere else, just copy it:

```bash
cp -r deai-text/ your-project/.claude/skills/deai-text/
```

Claude Code reads skills from `.claude/skills/` — no install command needed.

#### Claude Desktop (Cowork mode)

Clone or download the repo from [github.com/kayquer/deai-text](https://github.com/kayquer/deai-text), then place the folder inside `.claude/skills/` in your selected workspace:

```
your-selected-folder/
└── .claude/
    └── skills/
        └── deai-text/
            ├── SKILL.md
            ├── LICENSE
            └── skills/
```

Claude picks it up on the next conversation.

#### Other LLMs with skill/plugin support

Any LLM that supports markdown-based skill files can use this. Clone the repo and copy the folder into whatever directory the LLM reads skills from:

```bash
git clone https://github.com/kayquer/deai-text.git
```

The SKILL.md frontmatter follows a standard format:

```yaml
---
name: deai-text
description: >
  Audit and rewrite text to remove AI writing patterns...
---
```

### Usage

Once installed, just ask Claude (or your LLM) to audit your text:

- "De-AI this text: [paste text]"
- "Remove AI patterns from this article"
- "Audit this for AI writing tells"
- "Make this sound less like AI"
- "Humanize this writing"

The skill triggers automatically when it detects these kinds of requests.

### Using as a standalone prompt (any LLM)

If your LLM doesn't support skills, you can use a condensed prompt that works on ChatGPT, Gemini, Llama, Mistral, or any other model. Paste it as a system prompt or prepend it to your message.

- **English**: [`skills/prompts/standalone-en.md`](skills/prompts/standalone-en.md)
- **Portugues BR**: [`skills/prompts/standalone-pt-br.md`](skills/prompts/standalone-pt-br.md)

You can also paste the full `SKILL.md` content directly as a system prompt for the complete experience with all reference catalogs.

---

## Portugues BR

### O que faz

deai-text audita texto em busca de padroes de escrita de IA e reescreve para soar humano. Funciona em quatro etapas:

1. **Auditoria** — identifica cada padrao de IA, citando o trecho exato
2. **Reescrita** — devolve uma versao limpa com os padroes removidos
3. **Resumo das mudancas** — lista o que mudou e por que
4. **Segunda passada** — rele a reescrita para pegar o que sobreviveu

A skill usa um sistema de vocabulario em tres niveis (palavras que sempre denunciam IA vs. palavras que so sao suspeitas em grupo), alem de catalogos de padroes estruturais, metaforas mortas, cliches de descricao fisica e problemas de formatacao.

### O que detecta

**Em todos os tipos de texto:**
- Vocabulario Nivel 1 (delve, robust, seamless, leverage, holistic, cutting-edge, tapestry, etc.)
- Deteccao de clusters Nivel 2 (harness + navigate + foster no mesmo paragrafo)
- Analise de densidade Nivel 3 (significant, innovative, compelling — so quando em excesso)
- Uniformidade de comprimento de frases e paragrafos
- Ausencia de voz / neutralidade implacavel

**Especifico para nao-ficcao:**
- Uso excessivo de travessoes, negrito e emoji em titulos
- Transicoes de enchimento (Moreover, Furthermore, Additionally)
- Artefatos de chatbot (Great question!, Let's dive in!, Feel free to reach out)
- Tom bajulador, loops de reconhecimento, artefatos de cadeia de raciocinio
- Evasao de copula (serves as, features, boasts — em vez de is/has)
- Atribuicoes vagas, inflacao de significancia, linguagem promocional
- Conclusoes genericas (The future looks bright, Only time will tell)

**Especifico para ficcao:**
- 31 construcoes estruturais (participios finais, poetica de eco, formulas de negacao, etc.)
- Descricoes fisicas como substituto de emocao (mandibula cerrando, respiracao falhando, pupilas dilatadas)
- Metaforas mortas (atracao gravitacional, emocoes como temperatura, similes de pedra-na-agua)
- Placeholders de interioridade vaga (algo mudou, o peso disso assentou)
- Padroes de narrador-como-analista (highlighting, underscoring, showcasing)
- Variacao elegante / rotacao de sinonimos para nomes de personagens
- Front-loading atmosferico, banter falso-afiado, cliches de encerramento

### Estrutura do projeto

```
deai-text/
├── SKILL.md                          # Skill principal — logica de auditoria, formato de saida
├── references/
│   ├── vocabulary.md                 # Tabelas de palavras Nivel 1/2/3 com substituicoes
│   ├── constructions.md              # 31 padroes estruturais (ficcao + geral)
│   ├── fiction-phrases.md            # Descricoes fisicas, metaforas mortas, cliches
│   └── nonfiction-patterns.md        # Formatacao, transicoes, artefatos de chatbot
└── prompts/
    ├── standalone-en.md              # Prompt condensado para qualquer LLM (Ingles)
    └── standalone-pt-br.md           # Prompt condensado para qualquer LLM (PT-BR)
```

### Instalacao

#### Claude Code (CLI)

Clone o repositorio direto na pasta `.claude/skills/` do seu projeto:

```bash
mkdir -p seu-projeto/.claude/skills
git clone https://github.com/kayquer/deai-text.git seu-projeto/.claude/skills/deai-text
```

Ou se ja clonou em outro lugar, copie:

```bash
cp -r deai-text/ seu-projeto/.claude/skills/deai-text/
```

O Claude Code le skills de `.claude/skills/` automaticamente — nao precisa de comando de instalacao.

#### Claude Desktop (modo Cowork)

Clone ou baixe o repositorio em [github.com/kayquer/deai-text](https://github.com/kayquer/deai-text), depois coloque a pasta dentro de `.claude/skills/` na pasta que voce selecionou:

```
sua-pasta-selecionada/
└── .claude/
    └── skills/
        └── deai-text/
            ├── SKILL.md
            ├── LICENSE
            └── skills/
```

O Claude detecta automaticamente na proxima conversa.

#### Outros LLMs com suporte a skills/plugins

Qualquer LLM que suporte arquivos de skill em markdown pode usar isto. Clone o repositorio e copie para o diretorio de skills do LLM:

```bash
git clone https://github.com/kayquer/deai-text.git
```

### Como usar

Com a skill instalada, basta pedir:

- "De-AI this text: [cole o texto]"
- "Remove AI patterns from this article"
- "Audite este texto para padroes de IA"
- "Faz esse texto parecer menos IA"
- "Humanize this writing"

A skill dispara automaticamente ao detectar esse tipo de pedido.

### Usando como prompt avulso (qualquer LLM)

Se o seu LLM nao suporta skills, use um prompt condensado que funciona no ChatGPT, Gemini, Llama, Mistral ou qualquer outro modelo. Cole como system prompt ou antes da sua mensagem.

- **English**: [`skills/prompts/standalone-en.md`](skills/prompts/standalone-en.md)
- **Portugues BR**: [`skills/prompts/standalone-pt-br.md`](skills/prompts/standalone-pt-br.md)

Voce tambem pode colar o conteudo completo do `SKILL.md` como system prompt para a experiencia completa com todos os catalogos de referencia.

---

## The Accumulation Principle / O Principio da Acumulacao

This is the core idea behind deai-text. No single word or pattern makes text bad. The problem is **density**: the same constructions appearing reflexively, repeatedly, and interchangeably. AI writing sounds like AI writing because it reaches for the statistically common option every time.

One em dash is fine. One "jaw tightens" is fine. One "robust" is fine. The fifth one on the same page means the text is running on autopilot.

When auditing, don't witch-hunt individual words. Ask: how many times does this appear? Is it used interchangeably across contexts? Is this the first instance (possibly fine) or the fifth (definitely a pattern)?

---

Esta e a ideia central do deai-text. Nenhuma palavra ou padrao isolado torna o texto ruim. O problema e **densidade**: as mesmas construcoes aparecendo reflexivamente, repetidamente e de forma intercambiavel. Texto de IA soa como texto de IA porque sempre escolhe a opcao estatisticamente mais comum.

Um travessao esta ok. Um "mandibula cerrou" esta ok. Um "robust" esta ok. O quinto na mesma pagina significa que o texto esta no piloto automatico.

Ao auditar, nao cace palavras individualmente. Pergunte: quantas vezes isso aparece? Esta sendo usado de forma intercambiavel entre contextos? E a primeira ocorrencia (possivelmente ok) ou a quinta (definitivamente um padrao)?

---

## Inspirations / Inspiracoes

This skill draws from two projects:

- **[BANNED: The Definitive Guide](https://www.reddit.com/r/WritingWithAI/comments/1pecxos/i_constructed_an_exhaustive_anticlich%C3%A9_style/)** — An exhaustive anti-cliche style guide by u/Aggressive_Chicken63 on r/WritingWithAI. A personal catalog of constructions, words, phrases, and patterns to ban from AI-assisted writing. The structural constructions (Part 1), fiction phrases (Part 2), and the accumulation principle (Part 3) in this skill draw heavily from that work.

- **[avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)** by Conor Bronsdon — A Claude Code skill for auditing and rewriting content to remove AI-isms. The tiered vocabulary system (Tier 1 always-flag, Tier 2 cluster-flag, Tier 3 density-flag), adapted from [brandonwise/humanizer](https://github.com/brandonwise/humanizer) vocabulary research, and the 4-section output format (audit, rewrite, diff, second-pass) come from this project.

---

## License / Licenca

MIT
