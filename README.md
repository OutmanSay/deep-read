# Deep Read Skill

A portable Codex/ChatGPT skill for analyzing expository nonfiction with Mortimer J. Adler and Charles Van Doren's fifteen rules of analytical reading.

It produces a traceable HTML reading guide that keeps the fifteen rules visible and ordered, verifies published quotations against the source text, and treats criticism as provisional rather than pretending one book can fact-check itself.

## What makes it different

- **Method before summary:** rules 1–15 are the reading path, not a hidden checklist.
- **Content before decoration:** a book-specific visual metaphor may improve comprehension but cannot replace the analytical structure.
- **Exact quotations:** bundled verification rejects paraphrases presented as quotations.
- **Clear epistemic boundaries:** textual analysis and external fact-checking remain separate.
- **Follow-up mode:** readers can return with one precise chapter question and preserve their wording verbatim.

## Install

Copy the `deep-read` directory into a skill location supported by your agent:

```bash
mkdir -p ~/.agents/skills
cp -R deep-read ~/.agents/skills/deep-read
```

Then invoke it with `$deep-read`, or ask to deeply analyze a specific nonfiction book.

## Requirements

- Python 3.10+ for the bundled standard-library EPUB and quotation utilities.
- A host agent capable of reading the source and creating HTML.
- Optional: any document-analysis or research backend available in your environment.

No proprietary research service, browser profile, local directory layout, or book-download service is required.

## Included utilities

```bash
python3 deep-read/scripts/inspect_epub.py BOOK.epub --toc
python3 deep-read/scripts/extract_epub_node.py BOOK.epub "CHAPTER TITLE" -o chapter.txt
python3 deep-read/scripts/verify_quotes.py --source fulltext.txt --quotes quotes.txt
```

The scripts use only the Python standard library.

## License

MIT. See [LICENSE](LICENSE).
