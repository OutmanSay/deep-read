#!/usr/bin/env python3
"""Verify one-book-quote-per-line against an extracted source."""

from __future__ import annotations

import argparse
import difflib
import re
import sys


def normalize(text: str) -> str:
    table = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "\u3000": " "})
    return re.sub(r"\s+", "", text.translate(table)).strip('"\'')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--quotes", required=True, help="UTF-8 file with one final book quote per line")
    args = parser.parse_args()
    source = open(args.source, encoding="utf-8").read()
    quotes = [line.strip() for line in open(args.quotes, encoding="utf-8") if line.strip()]
    if not quotes:
        print("ERROR: quotes file is empty", file=sys.stderr)
        return 2
    normalized_source = normalize(source)
    candidates = [normalize(x) for x in re.split(r"(?<=[。！？!?])|\n", source) if len(normalize(x)) >= 8]
    failures = 0
    for index, quote in enumerate(quotes, 1):
        target = normalize(quote)
        if target and target in normalized_source:
            print(f"PASS {index}: {quote}")
            continue
        failures += 1
        match = difflib.get_close_matches(target, candidates, n=1, cutoff=0.35)
        hint = match[0][:80] if match else "无相近候选"
        print(f"FAIL {index}: {quote}\n  candidate: {hint}")
    print(f"RESULT: {len(quotes) - failures}/{len(quotes)} exact matches")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
