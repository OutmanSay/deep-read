---
name: deep-read
description: Systematically analyze a nonfiction expository book with Mortimer Adler's 15 rules of analytical reading, verify quotations against the source text, and deliver a traceable HTML reading guide. Use for requests to deeply read, unpack, or structurally analyze a specific book. Do not use for fiction, poetry, simple recommendations, or note-taking from the user's own reading.
---

# Deep Read

Use Mortimer J. Adler and Charles Van Doren's fifteen rules of analytical reading as a fixed, auditable path through one expository book.

The outcome is not a generic summary. It is a source-grounded reading guide that lets the reader answer all fifteen questions in order.

## Hard boundaries

1. Apply this workflow only to expository nonfiction. Do not force it onto novels, poetry, or drama.
2. Treat rules 12–15 as **questions for the reader**, not final verdicts against the author.
3. Cite stable structural locations such as chapters or sections. Do not invent page numbers.
4. Distinguish internal textual analysis from external fact-checking. A book can establish what its author claims, not whether every historical or scientific claim is true.
5. The HTML is a visualization of analytical reading. Visual design may support the framework, but must not reorder, merge, or hide rules 1–15.

## Inputs and workspace

Prefer a user-provided EPUB, PDF, or plain-text source. If no source is available, locate a lawful copy through the tools available in the host environment or ask the user to provide one.

Create a per-book working directory chosen for the current environment. Keep a `log.md` beside the output so later sessions can reuse the source, analysis, open questions, and artifacts rather than starting over.

If the source is EPUB, inspect its real metadata and table of contents:

```bash
python3 scripts/inspect_epub.py BOOK.epub --toc
```

Record fields supplied by the file. Mark missing fields as missing; do not infer them from a filename.

## 1. Classify before analyzing

Determine whether the work is expository and whether it is primarily theoretical or practical.

For dialogue, letters, speeches, memoir, or interviews, proceed only when the work uses those forms to establish claims. Extract the propositions and their dependencies before applying the rules. Narrative events may function as evidence, but narrative form alone does not make a work expository.

Stop and explain if the work is imaginative literature.

## 2. Obtain complete source text

Use any capable document or research backend available in the host environment. Verify that extraction is complete by comparing reported and actual character counts or by checking the beginning, middle, and end against the source.

Never analyze a silently truncated export.

## 3. Run three separate analytical passes

Read [references/adler-prompts.md](references/adler-prompts.md) and run the three prompts separately. Do not combine all fifteen rules into one request.

- Pass 1, rules 1–4: what the book is about.
- Pass 2, rules 5–8: what the book says and how it argues.
- Pass 3, rules 9–15: whether the book is sound, with rules 12–15 clearly marked as provisional.

When the analysis backend returns quotations, treat them only as candidates.

## 4. Verify every quotation locally

Return to the extracted source text, select the exact sentences to publish, and place one quotation per line in a UTF-8 file.

```bash
python3 scripts/verify_quotes.py --source fulltext.txt --quotes quotes.txt
```

The result must be 100%. Replace or remove every failed quotation before publication. Never accept “the meaning is right” as a substitute for an exact match.

## 5. Build the HTML reading guide

Read [references/html-contract.md](references/html-contract.md) before writing the page.

First articulate a visual thesis:

> The book's central claim is ___. Its native real-world form is ___. Therefore the page uses ___ as its visual language.

Then preserve the analytical hierarchy:

- The fixed cognitive backbone is rules 1→15.
- Each rule shows the original question, a direct answer, and its evidence or evidence boundary.
- The book-specific visual metaphor can shape typography, diagrams, and section treatment, but cannot replace the framework.
- Put the book's structural outline inside rule 3, terminology inside rule 5, argument chains inside rule 7, and provisional criticism inside rules 12–15.

Deliver a self-contained HTML file unless the user asks for another format.

## 6. Verify the artifact

Before delivery:

1. Confirm rules 1–15 are present, ordered, and individually answerable.
2. Confirm rule 1 explicitly states category, expository status, theoretical/practical orientation, and reasons.
3. Confirm all published book quotations belong to the verified set.
4. Confirm rules 12–15 carry evidence labels such as `text-internal` or `requires external verification`.
5. Render at desktop width and approximately 390 px mobile width; check overflow, legibility, long quotations, and navigation.
6. Confirm the page still works offline if it claims to be self-contained.

## Follow-up close reading

When the reader returns with a specific question about one chapter or section, read [references/follow-up.md](references/follow-up.md). Preserve the user's question verbatim and analyze only the smallest source window that can answer it.

## Completion report

Report the verified edition, missing metadata, classification, output path, rule coverage, quotation result, visual QA status, and the provisional status of rules 12–15.

Update the per-book `log.md` with source identifiers, artifacts, questions already explored, settled conclusions, and unverified inferences.
