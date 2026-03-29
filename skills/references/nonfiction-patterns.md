# Non-Fiction AI Patterns — Detection Catalog

Patterns specific to articles, blog posts, reports, marketing copy, and other non-fiction writing. These complement the vocabulary catalog (which applies to all text types).

---

## Formatting Issues

### Em Dashes
Target: zero. Hard max: one per 1,000 words. Replace with commas, periods, parentheses, or rewrite as two sentences. This applies to headings and titles too. Catch both the Unicode em dash (—) and the double-hyphen substitute (--).

### Bold Overuse
Strip bold from most phrases. One bolded phrase per major section at most, or none. If something's important enough to bold, restructure the sentence to lead with it.

### Emoji in Headers
Remove entirely. No "## 🚀 What This Means". Exception: social posts may use one or two emoji sparingly — at the end of a line, never mid-sentence.

### Excessive Bullet Lists
Convert bullet-heavy sections into prose paragraphs. Bullets only for genuinely list-like content (feature comparisons, step-by-step instructions, API parameters).

### Inline-Header Lists
Bullet lists where each item starts with a bold header that repeats itself: "**Performance:** Performance improved by..." Strip the bold header and write the point directly.

### Title Case Headings
AI over-capitalizes: "Strategic Negotiations And Key Partnerships" instead of "Strategic negotiations and key partnerships." Use sentence case for subheadings.

---

## Sentence Structure Issues

### "It's not X — it's Y" Construction
Rewrite as a direct positive statement. Max one per piece, and only if it serves the argument.

### Hollow Intensifiers
Cut: genuine, real (as in "a real improvement"), truly, quite frankly, to be honest, let's be clear, it's worth noting that. Just state the fact.

### Hedging
Cut: perhaps, could potentially, it's important to note that, to be clear. Make the point directly.

### Missing Bridge Sentences
Each paragraph should connect to the last. If paragraphs could be rearranged without the reader noticing, add connective tissue.

### Compulsive Rule of Three
Vary groupings. Use two items, four items, or a full sentence instead of triads. Max one "adjective, adjective, and adjective" pattern per piece.

---

## Transition Phrases to Remove or Rewrite

- "Moreover" / "Furthermore" / "Additionally" → restructure so the connection is obvious, or use "and," "also," "on top of that"
- "In today's [X]" / "In an era where" → cut or state specific context
- "It's worth noting that" / "Notably" → just state the fact
- "In conclusion" / "To summarize" → your conclusion should be obvious
- "When it comes to" → just talk about the thing directly
- "At the end of the day" → cut
- "That said" / "That being said" → cut or use "but," "yet," or "however" (don't overuse any one)

---

## Template Phrases

Slot-fill constructions that signal a sentence was generated, not written:

- "a [adjective] step towards [adjective] AI infrastructure"
- "a [adjective] step forward for [noun]"

If a phrase has a blank where a noun or adjective could go and still sound the same, it's too generic. Describe the specific capability, benchmark, or outcome.

---

## Chatbot Artifacts

Remove entirely:
- "I hope this helps!"
- "Certainly!" / "Absolutely!"
- "Great question!"
- "Feel free to reach out"
- "Let me know if you need anything else"
- "In this article, we will explore…"
- "Let's dive in!"

---

## "Let's" Constructions

"Let's explore," "Let's take a look," "Let's break this down," "Let's examine" — AI uses "let's" as a false-collaborative opener. It's filler that delays the actual point. Just start with the point. Flag any "let's + verb" functioning as a transition rather than a genuine invitation to act.

---

## Sycophantic Tone

Remove entirely:
- "Great question!"
- "Excellent point!"
- "You're absolutely right!"
- "That's a really insightful observation"

Distinct from chatbot artifacts: sycophancy specifically validates the reader/questioner.

---

## Acknowledgment Loops

- "You're asking about..."
- "The question of whether..."
- "To answer your question..."
- "That's a great question. The..."

AI restates the prompt before answering. The reader knows what they asked. Just answer.

Also: opening a section by summarizing what the previous section said. If the structure is clear, no recap needed.

---

## Reasoning Chain Artifacts

- "Let me think step by step"
- "Breaking this down"
- "To approach this systematically"
- "Step 1:"
- "Here's my thought process"
- "First, let's consider"
- "Working through this logically"

These are chain-of-thought scaffolding leaking into prose. State the conclusion, then the evidence.

---

## Confidence Calibration Phrases

- "It's worth noting that"
- "Interestingly"
- "Surprisingly"
- "Importantly"
- "Significantly"
- "Notably"
- "Certainly"
- "Undoubtedly"
- "Without a doubt"

AI uses these to signal how the reader should feel about a fact. One "notably" in 2,000 words is fine. Three in 500 words is AI-style emphasis stacking. Flag by density.

---

## Promotional / Brochure Language

- nestled (unless literal geography)
- in the heart of
- boasts a
- stunning [anything] / breathtaking [anything]
- continues to captivate
- rich tapestry of
- vibrant culture/community/scene
- bustling / picturesque / idyllic

These are advertising words. They tell the reader to be impressed rather than creating the impression through specific detail.

---

## Significance Inflation

- "marking a pivotal moment in the evolution of..."
- "a watershed moment for the industry"
- "cannot be overstated"
- "a game-changer for..."

These inflate routine events into history-making ones. State what happened and let the reader judge. If the sentence still works after deleting the inflation clause, delete it.

---

## Copula Avoidance

AI avoids "is" and "has" by substituting fancier verbs:
- "serves as" → use "is"
- "features" → use "has" or "includes"
- "boasts" → use "has"
- "presents" → use "is," "shows," or "gives"
- "represents" → often just "is"

Default to "is" or "has" unless a more specific verb genuinely adds meaning.

---

## Synonym Cycling

AI rotates synonyms to avoid repeating a word: "developers… engineers… practitioners… builders" in the same paragraph. Human writers repeat the clearest word. If the same noun or verb appears three times and it's the right word, keep all three.

---

## Vague Attributions

- "Experts believe"
- "Studies show"
- "Research suggests"
- "Industry leaders agree"

Without naming the expert, study, or leader. Either cite a specific source or drop the attribution and state the claim directly.

---

## Excessive Structure

- Too many headers in short text: 3+ headings in under 300 words is almost always AI trying to look organized
- Too many list items: 8+ bullet points in under 200 words means the content should be a paragraph
- Formulaic section headers: "Overview," "Key Points," "Summary," "Conclusion," "Introduction" — default AI scaffolding. Use headers that tell the reader something specific.

---

## Cutoff Disclaimers

- "While specific details are limited based on available information"
- "As of my last update"
- "I don't have access to real-time data"

Model limitations leaking into prose. Either find the information or remove the hedge.

---

## Superficial -ing Analyses

Strings of present participles used as pseudo-analysis: "symbolizing the region's commitment to progress, reflecting decades of investment, and showcasing a new era of collaboration." These say nothing. Replace with specific facts or cut entirely.

---

## Notability Name-Dropping

AI piles on prestigious citations to manufacture credibility: "cited in The New York Times, BBC, Financial Times, and The Hindu." If a source matters, use it with context: "In a 2024 NYT interview, she argued..." One specific reference beats four name-drops.

---

## Formulaic Challenges

"Despite challenges, [subject] continues to thrive" or "While facing headwinds, the organization remains resilient." This is a non-statement. Name the actual challenge and the actual response, or cut.

---

## False Ranges

AI creates false breadth by pairing unrelated extremes: "from the Big Bang to dark matter," "from ancient civilizations to modern startups." List the actual topics or pick the one that matters.

---

## Generic Conclusions

- "The future looks bright"
- "Only time will tell"
- "One thing is certain"
- "As we move forward"

Filler disguised as conclusions. Cut them. If the piece needs a closing thought, make it specific to the argument.

---

## Emotional Flatline

AI claims emotions as a structural crutch without conveying them: "What surprised me most," "I was fascinated to discover," "What struck me was," "The most interesting part."

The fix isn't "never say surprised." It's: if you claim an emotion, the writing around it should earn it. Otherwise cut the claim and present the thing directly.
