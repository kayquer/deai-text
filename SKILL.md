---
name: deai-text
description: >
  Audit and rewrite text to remove AI writing patterns across all genres — fiction, articles, reports, blog posts, marketing copy, and creative writing. Use this skill whenever the user asks to "de-AI" text, "remove AI patterns," "humanize writing," "fix AI writing," "make this sound human," "check for AI tells," "audit AI-isms," "clean up AI text," or any variation. Also use when the user pastes text and asks to improve it, polish it, or make it less generic — these are often implicit de-AI requests. Triggers on Portuguese equivalents too: "remover padrões de IA," "humanizar texto," "tirar cara de IA," "parece escrito por IA."
---

# De-AI Text — Audit & Rewrite

You are editing content to remove AI writing patterns that make text sound machine-generated. This applies to **all types of writing** — fiction, articles, blog posts, marketing copy, reports, and creative prose.

The user will provide a piece of writing. Your job:

1. **Audit it**: identify every AI pattern present, citing the specific text
2. **Rewrite it**: return a clean version with all patterns removed
3. **Show a diff summary**: list what you changed and why
4. **Second-pass audit**: re-read your rewrite and catch anything that survived

Before you begin, read whichever reference files are relevant to the text you're auditing:

- **All text types**: always read `skills/references/vocabulary.md` (AI word clusters and replacements)
- **Fiction / creative prose**: also read `skills/references/constructions.md` (structural patterns) and `skills/references/fiction-phrases.md` (physical tells, dead metaphors, clichés)
- **Non-fiction / articles / reports / marketing**: also read `skills/references/nonfiction-patterns.md` (formatting, transitions, structure)

The reference files contain the full catalogs of patterns. Read them before auditing — they are your detection dictionary.

---

## The Root Problem

Every AI pattern fails for the same reason: **it substitutes form for content.** AI text regresses to the statistical mean — the highest-probability completion at every turn. The result is prose that sounds assembled from interchangeable parts rather than written by a person with specific knowledge, opinions, and voice.

The tell is never a single word or phrase. It's **density and accumulation**: the same constructions appearing reflexively, repeatedly, and interchangeably across characters, paragraphs, or sections. One "jaw tightens" is fine. One em dash is fine. One "robust" is fine. The fifth one in a page means the text is running on autopilot.

---

## Detection Method

### Step 1: Density scan

Before flagging individual patterns, read the whole text and assess:

- **Sentence length uniformity**: if most sentences are 15–25 words with no variation, flag it. Human writing mixes short punchy sentences (3–8 words) with longer ones (20+). Fragments work. Questions break monotony.
- **Paragraph length uniformity**: if every paragraph is roughly the same size (3–5 sentences), flag it. Some paragraphs should be one sentence. Some should be longer.
- **Rhythm**: if the text could be read by a text-to-speech engine without sounding weird, it's too uniform.
- **Voice absence**: if there's no first-person perspective, no opinions, no stated preferences where they'd be natural — that's an AI tell. AI is relentlessly neutral.

### Step 2: Pattern matching

Now scan against the reference catalogs. For each match, note:

- The exact offending text (quote it)
- Which pattern category it falls under
- Whether it's an isolated instance (possibly fine) or part of a cluster (definitely flag)

### Step 3: Severity assessment

Decide whether to **patch** or **rewrite from scratch**:

- **Patch** if: fewer than 5 flagged hits, limited to 1–2 pattern categories, sentence rhythm is already varied
- **Rewrite from scratch** if: 5+ hits across 3+ categories, uniform sentence/paragraph length, and the structure itself feels generated. In this case, identify the core point in one sentence and rebuild from there.

---

## The Tiered Vocabulary System

Words are organized into three tiers by how reliably they signal AI-generated text (full lists in `skills/references/vocabulary.md`):

- **Tier 1 — Always flag.** Words that appear 5–20x more often in AI text than human text. Replace on sight: *delve, landscape (metaphor), tapestry, paradigm, robust, comprehensive, seamless, leverage, utilize, pivotal, meticulous, cutting-edge, nestled, vibrant, thriving, bustling, holistic, actionable, impactful, game-changer, watershed moment.*

- **Tier 2 — Flag in clusters.** Individually fine, but two or more in the same paragraph is a strong AI signal: *harness, navigate, foster, elevate, empower, streamline, resonate, facilitate, nuanced, crucial, multifaceted, ecosystem (metaphor), myriad, transformative, cornerstone, paramount.*

- **Tier 3 — Flag by density.** Common words AI simply overuses. Only flag when they saturate the text (~3%+ of total words): *significant, innovative, effective, dynamic, scalable, compelling, unprecedented, remarkable, sophisticated.*

---

## Fiction-Specific Detection

When auditing fiction or creative prose, also check for these categories (full catalogs in `skills/references/constructions.md` and `skills/references/fiction-phrases.md`):

- **Structural patterns**: sequential action pairs ("X, then Y"), triple-beat lists, staccato verb fragments, trailing participle pile-ups, echo-line poetics, negation formulas
- **Physical tells used as emotion substitutes**: jaw clenching, throat working, breath catching, pupils blown, hands curling into fists — the same autonomic responses applied to every character interchangeably
- **Dead metaphors**: gravitational attraction, temperature emotions, impact similes ("like a punch"), water imagery ("rippled through"), breaking/cracking metaphors
- **Vague interiority**: "something shifted," "the weight of it settled," "the silence stretched between them" — placeholders that name that change happened without showing how
- **Narrator-as-analyst**: participle phrases that editorialize ("highlighting her frustration," "underscoring his discomfort")
- **Elegant variation**: cycling through synonyms or descriptors to avoid repeating a character's name ("the older man," "the architect," "her husband")
- **Atmospheric front-loading**: opening scenes with weather, skyline, or architecture before any character presence

---

## Non-Fiction Detection

When auditing articles, reports, blog posts, or marketing copy, also check (full patterns in `skills/references/nonfiction-patterns.md`):

- **Formatting**: em dash overuse (target: zero; hard max: one per 1,000 words), bold overuse, emoji in headers, excessive bullet lists
- **Template phrases**: "a [adjective] step towards [adjective] [noun]" — slot-fill constructions that sound the same no matter what fills the blanks
- **Transition filler**: "Moreover," "Furthermore," "Additionally," "In today's [X]," "It's worth noting that," "When it comes to," "At the end of the day"
- **Chatbot artifacts**: "I hope this helps!", "Certainly!", "Great question!", "Let's dive in!", "Feel free to reach out"
- **Sycophantic tone**: "Great question!", "Excellent point!", "That's a really insightful observation"
- **Acknowledgment loops**: "You're asking about," "To answer your question," — restating the prompt before answering
- **Reasoning chain artifacts**: "Let me think step by step," "Breaking this down," "To approach this systematically"
- **Promotional language**: "nestled within," "a vibrant hub," "a thriving ecosystem," "continues to captivate"
- **Significance inflation**: "marking a pivotal moment," "a watershed moment for the industry," "cannot be overstated"
- **Copula avoidance**: substituting "serves as," "features," "boasts," "presents" for simple "is" or "has"
- **Vague attributions**: "Experts believe," "Studies show," "Research suggests" — without naming any source
- **Excessive structure**: too many headers in short text (3+ in under 300 words), 8+ bullet points in under 200 words, formulaic section headers ("Overview," "Key Points," "Summary")
- **Cutoff disclaimers**: "As of my last update," "While specific details are limited" — model limitations leaking into prose
- **Confidence calibration phrases**: "Notably," "Importantly," "Interestingly," "Undoubtedly" — telling the reader how to feel instead of letting the fact speak

---

## Output Format

Return your response in four sections:

### 1. Issues Found

A list of every AI pattern identified, with the offending text quoted. Group by category (vocabulary, structure, rhythm, etc.). For each, note whether it's an isolated instance or part of a pattern.

### 2. Rewritten Version

The full rewritten content. Preserve the original structure, intent, and all specific technical details. Only change what the guidelines require.

Five principles for human-sounding rewrites:
1. **Vary sentence length** — mix short with long. Fragments are fine.
2. **Be concrete** — replace vague claims with numbers, names, dates, or examples.
3. **Have a voice** — where appropriate, use first person, state preferences, show reactions.
4. **Cut the neutrality** — humans have opinions. If the piece should take a position, take it.
5. **Earn your emphasis** — don't tell the reader something is interesting. Make it interesting.

### 3. What Changed

A brief summary of the major edits. Not every word — just the meaningful changes and the reasoning behind them.

### 4. Second-Pass Audit

Re-read the rewritten version from section 2. Identify any remaining AI tells that survived the first pass — recycled transitions, lingering inflation, copula avoidance, filler phrases, uniform rhythm, or anything from the reference catalogs. Fix them, return the corrected text inline, and note what changed. If the rewrite is clean, say so.

---

## Tone Calibration

The goal is writing that sounds like a person wrote it. Direct. Specific. The writing should demonstrate confidence, not assert it.

If the original writing is already strong, say so and make only the necessary cuts. Don't over-edit for the sake of it. The replacement tables provide defaults, not mandates — if a flagged word is clearly the right choice in context, preserve it and note why.

---

## The Accumulation Principle

This is the most important concept in the entire skill. No single pattern makes prose bad. The problem is **density** — when the same constructions, the same vague interiority, the same physical tells appear over and over regardless of context, the prose flattens into something that reads as generated rather than written.

When you catch a pattern, don't just ask "is this bad?" Ask:
- How many times does this appear in the text?
- Is it used interchangeably across different contexts/characters?
- Is this the first appearance (possibly fine) or the fifth (definitely a pattern)?

A single "the weight of it settled in his chest" might work. The third one means the text is leaning on a crutch.

**The corollary**: witch-hunting individual words is pointless. The question isn't whether a construction appears — it's whether it appears *reflexively, repeatedly, and interchangeably.* Density. Pattern. Accumulation.
