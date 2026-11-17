# Detection checklists by genre

The genre checklists the audit runs after Step 1 of the detection method. Each item names its rule ID and points to the full catalog.

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

- **`AI-6` Formatting**: em dash accumulation (two or more in a paragraph, or more than one per 300 words; a single em dash is never a finding), bold overuse, emoji in headers, excessive bullet lists
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
