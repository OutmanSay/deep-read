# HTML reading-guide contract

## Priority

The page is an analytical-reading guide first and an editorial design artifact second.

The fixed reading order is rules 1→15. For every rule, show:

1. the rule number and original question;
2. a direct answer;
3. book-internal evidence or an explicit evidence boundary;
4. when useful, how the rule leads to the next one.

Rule 1 must answer all four classification questions: kind, expository status, theoretical/practical orientation, and reasons. A format label such as “memoir” or “interview” is not enough.

Do not turn the rules into fifteen visually identical cards. Use the book's native visual metaphor to vary diagrams and typography, but never reorder, merge, compress, rename away, or hide the rules.

## Required content

- edition and source card;
- rules 1–15 in order;
- one-sentence whole-book statement;
- structural outline inside rule 3;
- key terms inside rule 5;
- verified quotations inside rule 6;
- argument chains inside rule 7;
- solved and unsolved problems inside rule 8;
- qualifications inside rules 9–11;
- rules 12–15 marked provisional with evidence labels;
- Adler's four closing questions.

Visually distinguish `source text`, `analysis`, and `to verify`.

## Visual and interaction requirements

- No horizontal scrolling at a 390 px viewport.
- Keep desktop prose lines at a comfortable reading measure.
- Do not hide essential content behind hover.
- Use working anchor navigation and preserve browser back behavior.
- Respect `prefers-reduced-motion`.
- Core reading and navigation must remain usable if optional network assets fail.

## Acceptance test

- Can the reader identify every rule without interpreting a metaphor?
- Can the reader find each rule's direct answer and evidence?
- Does the visual concept clarify the book without becoming a replacement outline?
- Are all quotations drawn from the verified quotation set?
- Are rules 12–15 visibly provisional?
- Does the rendered page work on desktop and mobile?

If the page exposes only renamed “movements,” “modules,” or “voices” while hiding the Adler questions, it fails.
