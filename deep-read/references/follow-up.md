# Follow-up close reading

Use this mode after the whole-book analysis when the reader asks a specific question about a chapter or section.

## Preserve the question

Copy the reader's observation, question, and hypothesis verbatim. Do not summarize or improve their wording.

## Select the smallest useful source window

Choose a unique table-of-contents node and analyze one level below it. For an EPUB:

```bash
python3 scripts/inspect_epub.py BOOK.epub --toc
python3 scripts/extract_epub_node.py BOOK.epub "NODE TITLE" -o node.txt
```

Verify that the target is unique, the extracted file has at least 100 non-whitespace characters, and its boundaries are sensible.

## Answer in three parts

1. **Does the source answer the question?** Label each point `answered`, `sidestepped`, or `not discussed`.
2. **Does the reader's hypothesis hold?** Label it `supported`, `rejected`, or `partly supported`; state the boundary.
3. **What could change the reader's judgment?** Give no more than three findings tied to the original question.

Return to the local source for every quotation and run `verify_quotes.py`. The final HTML begins with the reader's verbatim question.
