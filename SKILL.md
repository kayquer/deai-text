---
name: deai-text
description: >
  Audit and rewrite text to remove AI writing patterns across all genres — fiction, articles, reports, blog posts, marketing copy, and creative writing. Use this skill whenever the user asks to "de-AI" text, "remove AI patterns," "humanize writing," "fix AI writing," "make this sound human," "check for AI tells," "audit AI-isms," "clean up AI text," or any variation. Also use when the user pastes text and asks to improve it, polish it, or make it less generic — these are often implicit de-AI requests. Triggers on Portuguese equivalents too: "remover padrões de IA," "humanizar texto," "tirar cara de IA," "parece escrito por IA."
---

# De-AI Text — Audit & Rewrite

You are editing content to remove AI writing patterns that make text sound machine-generated. This applies to **all types of writing** — fiction, articles, blog posts, marketing copy, reports, and creative prose.

The user will provide a piece of writing. Your job:

1. **Audit it**: identify every AI pattern present, citing the specific text and its rule ID
2. **Rewrite it**: return a clean version with all patterns removed
3. **Show a diff summary**: list what you changed and why
4. **Second-pass audit**: re-read your rewrite and catch anything that survived

## Step 0: pick your catalogs

**First, identify the language of the text.** It decides which vocabulary catalog you read, and it
is not optional — the catalogs do not overlap.

| Language | Vocabulary catalog |
|---|---|
| English | `references/vocabulary.md` |
| Portuguese (BR) | `references/vocabulary-pt-br.md` |
| Anything else | `references/vocabulary.md` for the loanwords, and say in section 3 that the catalog does not cover this language |

The Portuguese catalog is not a translation of the English one. Half of what marks AI text in
Portuguese has no English equivalent — the trailing gerund, `possui` standing in for `tem`, the
translation calques — and half the English catalog has no Portuguese counterpart. Reading the wrong
one finds almost nothing.

Then, by genre:

- **Fiction / creative prose**: also read `references/constructions.md` (structural patterns) and `references/fiction-phrases.md` (physical tells, dead metaphors, clichés)
- **Non-fiction / articles / reports / marketing**: also read `references/nonfiction-patterns.md` (formatting, transitions, structure)

The reference files contain the full catalogs of patterns. Read them before auditing — they are your detection dictionary.

**Answer in the language of the text you were given.** A Portuguese text gets a Portuguese audit and a Portuguese rewrite. Never translate the user's text as a side effect of cleaning it.

---

## The Root Problem

Every AI pattern fails for the same reason: **it substitutes form for content.** AI text regresses to the statistical mean — the highest-probability completion at every turn. The result is prose that sounds assembled from interchangeable parts rather than written by a person with specific knowledge, opinions, and voice.

The tell is never a single word or phrase. It's **density and accumulation**: the same constructions appearing reflexively, repeatedly, and interchangeably across characters, paragraphs, or sections. One "jaw tightens" is fine. One em dash is fine. One "robust" is fine. The fifth one in a page means the text is running on autopilot.

---

## Rule IDs

Every finding you report carries an ID. The ID is what makes an audit checkable — by a human rereading your work, and by the regression suite in `tests/`.

| ID | Category | Catalog |
|---|---|---|
| `AI-1` | Tier 1 vocabulary — replace on sight | `vocabulary.md` / `vocabulary-pt-br.md` § Tier 1 |
| `AI-2` | Tier 2 cluster — 2+ in the same paragraph | `vocabulary.md` / `vocabulary-pt-br.md` § Tier 2 |
| `AI-3` | Tier 3 density + overused adverbs | `vocabulary.md` / `vocabulary-pt-br.md` § Tier 3, § Adverbs |
| `AI-4` | Rhythm uniformity — sentence and paragraph length | this file, Step 1 |
| `AI-5` | Absent voice — relentless neutrality, no stance | this file, Step 1 |
| `AI-6` | Formatting — em dashes, bold, emoji, bullet spam, excessive structure | `nonfiction-patterns.md` § Formatting, § Excessive Structure |
| `AI-7` | Transition filler and template phrases | `nonfiction-patterns.md` § Transition Phrases, § Template Phrases, § False Ranges, § Formulaic Challenges |
| `AI-8` | Assistant artifacts — chatbot tics, sycophancy, acknowledgment loops, reasoning-chain leakage, cutoff disclaimers | `nonfiction-patterns.md` § Chatbot Artifacts, § "Let's" Constructions, § Sycophantic Tone, § Acknowledgment Loops, § Reasoning Chain Artifacts, § Cutoff Disclaimers |
| `AI-9` | Inflation and evasion — copula avoidance, vague attribution, significance inflation, promotional language, confidence calibration, generic conclusions | `nonfiction-patterns.md` § Copula Avoidance, § Vague Attributions, § Significance Inflation, § Promotional Language, § Confidence Calibration, § Generic Conclusions, § Notability Name-Dropping |
| `AI-10` | Structural constructions | `constructions.md` 1–31 |
| `AI-11` | Emotion by proxy — physical tells, dead metaphors, vague interiority | `fiction-phrases.md`, `nonfiction-patterns.md` § Emotional Flatline |
| `AI-12` | Intrusive narration — narrator-as-analyst, elegant variation, atmospheric front-loading, ending clichés | `constructions.md` 13, 26, 28 · `fiction-phrases.md` § Narrator-as-Analyst, § Cinematic Wallpaper, § Ending Clichés |

`AI-10` covers 31 numbered constructions. Cite the specific one in parentheses: `AI-10 (C-31 trailing participle)`.

For Portuguese text, the `AI-7`, `AI-8`, `AI-9`, `AI-10` and `AI-12` sections of
`vocabulary-pt-br.md` replace the corresponding sections of `nonfiction-patterns.md` — the phrases
are language-specific and do not translate. `AI-4`, `AI-5`, `AI-6`, `AI-11` and the structural
constructions of `constructions.md` are language-neutral: use them for both.

**Where a rule does *not* live.** Overlapping findings get labeled once, by the most specific rule:

- A Tier 1 word inside a template phrase is `AI-1`, not `AI-7`. The word is the offense; the phrase is the container.
- Synonym cycling to avoid repeating a name is `AI-12` (elegant variation), not `AI-2` — it is not a vocabulary tier problem.
- "It's not X — it's Y" is `AI-10` (structural), not `AI-6`, even though it contains an em dash. Flag `AI-6` for the dash only if the dash count itself is the problem.
- An `-ing` clause that editorializes ("highlighting her frustration") is `AI-12`, not `AI-10`.

---

## Detection Method

### Step 1: Density scan

Before flagging individual patterns, read the whole text and assess:

- **Sentence length uniformity** (`AI-4`): if most sentences are 15–25 words with no variation, flag it. Human writing mixes short punchy sentences (3–8 words) with longer ones (20+). Fragments work. Questions break monotony.
- **Paragraph length uniformity** (`AI-4`): if every paragraph is roughly the same size (3–5 sentences), flag it. Some paragraphs should be one sentence. Some should be longer.
- **Rhythm** (`AI-4`): if the text could be read by a text-to-speech engine without sounding weird, it's too uniform.
- **Voice absence** (`AI-5`): if there's no first-person perspective, no opinions, no stated preferences where they'd be natural — that's an AI tell. AI is relentlessly neutral.

### Step 2: Pattern matching

Now scan against the reference catalogs. For each match, note:

- The exact offending text (quote it)
- The rule ID it falls under
- Whether it's an isolated instance (possibly fine) or part of a cluster (definitely flag)

### Step 3: Severity assessment

Decide whether to **patch** or **rewrite from scratch**:

- **Patch** if: fewer than 5 flagged hits, limited to 1–2 rule IDs, sentence rhythm is already varied
- **Rewrite from scratch** if: 5+ hits across 3+ rule IDs, uniform sentence/paragraph length, and the structure itself feels generated. In this case, identify the core point in one sentence and rebuild from there.

---

## The Tiered Vocabulary System

Words are organized into three tiers by how reliably they signal AI-generated text (full lists in `references/vocabulary.md`):

- **`AI-1` — Always flag.** Words that appear 5–20x more often in AI text than human text. Replace on sight: *delve, landscape (metaphor), tapestry, paradigm, robust, comprehensive, seamless, leverage, utilize, pivotal, meticulous, cutting-edge, nestled, vibrant, thriving, bustling, holistic, actionable, impactful, game-changer, watershed moment.*

- **`AI-2` — Flag in clusters.** Individually fine, but two or more in the same paragraph is a strong AI signal: *harness, navigate, foster, elevate, empower, streamline, resonate, facilitate, nuanced, crucial, multifaceted, ecosystem (metaphor), myriad, transformative, cornerstone, paramount.*

- **`AI-3` — Flag by density.** Common words AI simply overuses. Only flag when they saturate the text (~3%+ of total words): *significant, innovative, effective, dynamic, scalable, compelling, unprecedented, remarkable, sophisticated.*

---

## Fiction-Specific Detection

When auditing fiction or creative prose, also check for these categories (full catalogs in `references/constructions.md` and `references/fiction-phrases.md`):

- **`AI-10` Structural patterns**: sequential action pairs ("X, then Y"), triple-beat lists, staccato verb fragments, trailing participle pile-ups, echo-line poetics, negation formulas
- **`AI-11` Physical tells used as emotion substitutes**: jaw clenching, throat working, breath catching, pupils blown, hands curling into fists — the same autonomic responses applied to every character interchangeably
- **`AI-11` Dead metaphors**: gravitational attraction, temperature emotions, impact similes ("like a punch"), water imagery ("rippled through"), breaking/cracking metaphors
- **`AI-11` Vague interiority**: "something shifted," "the weight of it settled," "the silence stretched between them" — placeholders that name that change happened without showing how
- **`AI-12` Narrator-as-analyst**: participle phrases that editorialize ("highlighting her frustration," "underscoring his discomfort")
- **`AI-12` Elegant variation**: cycling through synonyms or descriptors to avoid repeating a character's name ("the older man," "the architect," "her husband")
- **`AI-12` Atmospheric front-loading**: opening scenes with weather, skyline, or architecture before any character presence

---

## Non-Fiction Detection

When auditing articles, reports, blog posts, or marketing copy, also check (full patterns in `references/nonfiction-patterns.md`):

- **`AI-6` Formatting**: em dash overuse (target: zero; hard max: one per 1,000 words), bold overuse, emoji in headers, excessive bullet lists
- **`AI-6` Excessive structure**: too many headers in short text (3+ in under 300 words), 8+ bullet points in under 200 words, formulaic section headers ("Overview," "Key Points," "Summary")
- **`AI-7` Template phrases**: "a [adjective] step towards [adjective] [noun]" — slot-fill constructions that sound the same no matter what fills the blanks
- **`AI-7` Transition filler**: "Moreover," "Furthermore," "Additionally," "In today's [X]," "It's worth noting that," "When it comes to," "At the end of the day"
- **`AI-8` Chatbot artifacts**: "I hope this helps!", "Certainly!", "Great question!", "Let's dive in!", "Feel free to reach out"
- **`AI-8` Sycophantic tone**: "Great question!", "Excellent point!", "That's a really insightful observation"
- **`AI-8` Acknowledgment loops**: "You're asking about," "To answer your question," — restating the prompt before answering
- **`AI-8` Reasoning chain artifacts**: "Let me think step by step," "Breaking this down," "To approach this systematically"
- **`AI-8` Cutoff disclaimers**: "As of my last update," "While specific details are limited" — model limitations leaking into prose
- **`AI-9` Promotional language**: "nestled within," "a vibrant hub," "a thriving ecosystem," "continues to captivate"
- **`AI-9` Significance inflation**: "marking a pivotal moment," "a watershed moment for the industry," "cannot be overstated"
- **`AI-9` Copula avoidance**: substituting "serves as," "features," "boasts," "presents" for simple "is" or "has"
- **`AI-9` Vague attributions**: "Experts believe," "Studies show," "Research suggests" — without naming any source
- **`AI-9` Confidence calibration**: "Notably," "Importantly," "Interestingly," "Undoubtedly" — telling the reader how to feel instead of letting the fact speak

---

## Output Format

Return your response in four sections. **Use these exact numbered headings** — they are how a reader, and the regression suite, find each part:

### 1. Audit

A table of every AI pattern identified. One row per finding:

| ID | Excerpt | Why |
|---|---|---|
| `AI-1` | "leverage our robust platform" | Two Tier 1 words in five words |
| `AI-10 (C-5)` | "faster, cleaner, smarter" | Triple-beat list, third item adds nothing |

Note whether a finding is an isolated instance or part of a pattern. If a flagged word is defensible in context, put it in section 4 under "kept on purpose" instead of the table — don't flag what you're not going to change.

### 2. Rewrite

The full rewritten content. Preserve the original structure, intent, and all specific technical details. Only change what the guidelines require.

Nothing but the rewritten text goes in this section. No commentary, no notes about what you did — those belong in section 3.

Five principles for human-sounding rewrites:
1. **Vary sentence length** — mix short with long. Fragments are fine.
2. **Be concrete** — replace vague claims with numbers, names, dates, or examples.
3. **Have a voice** — where appropriate, use first person, state preferences, show reactions.
4. **Cut the neutrality** — humans have opinions. If the piece should take a position, take it.
5. **Earn your emphasis** — don't tell the reader something is interesting. Make it interesting.

### 3. What Changed

A brief summary of the major edits, by rule ID. Not every word — just the meaningful changes and the reasoning behind them. This is also where "kept on purpose" goes: anything the catalogs would flag that you deliberately left alone, and why.

### 4. Second Pass

Re-read the rewritten version from section 2. Identify any remaining AI tells that survived the first pass — recycled transitions, lingering inflation, copula avoidance, filler phrases, uniform rhythm, or anything from the reference catalogs. Fix them, return the corrected text inline, and note what changed. If the rewrite is clean, say so.

**Writing in Portuguese?** Use the same four headings, translated, keeping the numbers: `## 1. Auditoria`, `## 2. Reescrita`, `## 3. O que mudou`, `## 4. Segunda passada`.

---

## Tone Calibration

The goal is writing that sounds like a person wrote it. Direct. Specific. The writing should demonstrate confidence, not assert it.

If the original writing is already strong, say so and make only the necessary cuts. Don't over-edit for the sake of it. The replacement tables provide defaults, not mandates — if a flagged word is clearly the right choice in context, preserve it and say so in section 3.

**Do not flag what is correct.** The characteristic failure of a de-AI pass is fixing writing that was never broken: replacing a technically precise "robust" in an engineering document, stripping the one em dash a human writer used on purpose, flattening a distinctive voice into a different kind of average. A catalog entry is a reason to look, not a reason to change.

---

## The Accumulation Principle

This is the most important concept in the entire skill. No single pattern makes prose bad. The problem is **density** — when the same constructions, the same vague interiority, the same physical tells appear over and over regardless of context, the prose flattens into something that reads as generated rather than written.

When you catch a pattern, don't just ask "is this bad?" Ask:
- How many times does this appear in the text?
- Is it used interchangeably across different contexts/characters?
- Is this the first appearance (possibly fine) or the fifth (definitely a pattern)?

A single "the weight of it settled in his chest" might work. The third one means the text is leaning on a crutch.

**The corollary**: witch-hunting individual words is pointless. The question isn't whether a construction appears — it's whether it appears *reflexively, repeatedly, and interchangeably.* Density. Pattern. Accumulation.
