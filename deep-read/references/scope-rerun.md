# Scope rerun (deep dive)

Use this mode when the reader asks to go deeper into a concept, a part, or "this section, one more layer" — rather than asking one specific question (that is [follow-up.md](follow-up.md)).

The difference: follow-up drives deep along **one question**; a scope rerun fixes **one range** and runs the same fifteen rules again inside it.

## The skeleton is the fifteen rules — no custom outline

Do not invent section headings for the deep dive. In testing, a deep-dive page organized under seven self-invented headings was rejected by the reader as "confusing", although the content was sound. Rebuilt on rules 1→15, the same material read as clear.

The value of the framework is that the reader always knows which rule they are on, and the order was set by Adler, not by the model. A custom outline swaps an external, checkable ruler for an ad-hoc essay plan.

## Range

Any table-of-contents node, or a concept range that spans nodes (for example, the two chapters where a key term is developed). Extract it with `scripts/extract_epub_node.py` and verify the boundaries as in follow-up mode.

## Four mechanical adjustments

These are adjustments, not omissions. State them at the top of the page.

| Rule | At deep-dive scale |
|---|---|
| 1 · Classification | Downgrade to a local check: report only whether the range is consistent with the whole-book classification. |
| 3 · Outline | Upgrade — this is the body of the page. The whole-book guide stops at the first level; the deep dive fills in the second and third levels. |
| 5 · Terms | Do not repeat whole-book definitions. Report how the same word shifts meaning inside the range, and why it has to. |
| 12–15 · Criticism | Narrow to internal consistency within the range. One chapter cannot settle whether the author is right about the world. Diff against the whole-book verdicts. |

Run every other rule unchanged.

## Output

The first block on the page states its relation to the whole-book guide: same ruler, finer scale, and which rules were adjusted. Reuse the whole-book page's visual components rather than starting a new style, and save it beside the whole-book guide. Verify every quotation with `scripts/verify_quotes.py` and record the run in the per-book `log.md`.
