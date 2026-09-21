#!/usr/bin/env python3
"""Extract a TOC node (or a leaf's ±1 sibling window) from an EPUB."""

from __future__ import annotations

import argparse
import html
import posixpath
import re
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path

from inspect_epub import read_package, table_of_contents


class TextExtractor(HTMLParser):
    BLOCKS = {"address", "article", "aside", "blockquote", "br", "div", "h1", "h2", "h3", "h4", "h5", "h6", "li", "p", "section", "table", "tr"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.hidden = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style"}:
            self.hidden += 1
        if not self.hidden and tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.hidden:
            self.hidden -= 1
        if not self.hidden and tag in self.BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self.hidden:
            self.parts.append(data)

    def text(self) -> str:
        value = html.unescape("".join(self.parts)).replace("\u3000", " ")
        value = re.sub(r"[ \t]+", " ", value)
        value = re.sub(r"\n\s*\n+", "\n\n", value)
        return value.strip()


def norm_title(value: str) -> str:
    return re.sub(r"[\W_]+", "", value, flags=re.UNICODE).casefold()


def doc_path(href: str) -> str:
    return href.split("#", 1)[0]


def choose(items, query: str):
    needle = norm_title(query)
    exact = [i for i, item in enumerate(items) if norm_title(item.title) == needle]
    matches = exact or [i for i, item in enumerate(items) if needle and needle in norm_title(item.title)]
    if len(matches) != 1:
        label = "no match" if not matches else "ambiguous match"
        candidates = matches or list(range(len(items)))
        shown = "\n".join(f"  {i + 1:03d} {items[i].title}" for i in candidates[:20])
        raise ValueError(f"{label} for {query!r}. Candidates:\n{shown}")
    return matches[0]


def toc_range(items, index: int) -> tuple[int, int, str]:
    target = items[index]
    next_child = index + 1 < len(items) and items[index + 1].depth > target.depth
    if next_child:
        end = index + 1
        while end < len(items) and items[end].depth > target.depth:
            end += 1
        return index, end, "subtree"

    siblings = [i for i, item in enumerate(items) if item.depth == target.depth]
    position = siblings.index(index)
    start = siblings[max(0, position - 1)]
    last = siblings[min(len(siblings) - 1, position + 1)]
    end = last + 1
    while end < len(items) and items[end].depth > items[last].depth:
        end += 1
    return start, end, "leaf ±1 sibling window"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("epub")
    parser.add_argument("node", help="unique full title or unique title fragment")
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()
    try:
        with zipfile.ZipFile(args.epub) as zf:
            _, _, manifest, spine = read_package(zf)
            items = table_of_contents(zf, manifest)
            if not items:
                raise ValueError("EPUB has no readable NCX/nav table of contents")
            selected = choose(items, args.node)
            start, end, mode = toc_range(items, selected)
            selected_docs = {doc_path(item.href) for item in items[start:end]}
            spine_indexes = [i for i, path in enumerate(spine) if path in selected_docs]
            if not spine_indexes:
                raise ValueError("TOC selection does not map to any OPF spine document")
            lo, hi = min(spine_indexes), max(spine_indexes)
            docs = spine[lo : hi + 1]
            sections = []
            for path in docs:
                parser_ = TextExtractor()
                parser_.feed(zf.read(path).decode("utf-8", errors="replace"))
                text = parser_.text()
                if text:
                    sections.append(f"## {posixpath.basename(path)}\n\n{text}")
            body = "\n\n".join(sections).strip() + "\n"
            if len(re.sub(r"\s", "", body)) < 100:
                raise ValueError("extraction produced fewer than 100 non-whitespace characters")
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(body, encoding="utf-8")
            print(f"node: {items[selected].title}")
            print(f"mode: {mode}")
            print(f"toc entries: {end - start}")
            print(f"spine documents: {len(docs)}")
            print(f"characters: {len(body)}")
            print(f"output: {output}")
            if any("#" in item.href for item in items[start:end]):
                print("warning: fragment-level TOC detected; extraction includes complete spine documents, so inspect boundary text manually")
    except (OSError, zipfile.BadZipFile, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
