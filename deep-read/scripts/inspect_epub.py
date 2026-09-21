#!/usr/bin/env python3
"""Inspect EPUB package metadata and table of contents using the stdlib only."""

from __future__ import annotations

import argparse
import posixpath
import sys
import zipfile
from dataclasses import dataclass
from xml.etree import ElementTree as ET


CONTAINER = "META-INF/container.xml"
DC = "http://purl.org/dc/elements/1.1/"
OPF = "http://www.idpf.org/2007/opf"
XHTML = "http://www.w3.org/1999/xhtml"
NCX = "http://www.daisy.org/z3986/2005/ncx/"


@dataclass
class TocItem:
    title: str
    href: str
    depth: int


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def package_path(zf: zipfile.ZipFile) -> str:
    root = ET.fromstring(zf.read(CONTAINER))
    for element in root.iter():
        if local(element.tag) == "rootfile" and element.get("full-path"):
            return element.get("full-path", "")
    raise ValueError("EPUB container has no OPF rootfile")


def read_package(zf: zipfile.ZipFile):
    opf_path = package_path(zf)
    root = ET.fromstring(zf.read(opf_path))
    base = posixpath.dirname(opf_path)
    manifest = {
        item.get("id", ""): {
            "href": posixpath.normpath(posixpath.join(base, item.get("href", ""))),
            "media": item.get("media-type", ""),
            "properties": item.get("properties", ""),
        }
        for item in root.iter()
        if local(item.tag) == "item"
    }
    spine = [manifest[x.get("idref", "")]["href"] for x in root.iter() if local(x.tag) == "itemref" and x.get("idref", "") in manifest]
    return opf_path, root, manifest, spine


def metadata(root: ET.Element) -> dict[str, list[str]]:
    wanted = {"title", "creator", "contributor", "publisher", "date", "identifier", "language"}
    out = {key: [] for key in wanted}
    out["edition"] = []
    for element in root.iter():
        name = local(element.tag)
        value = " ".join("".join(element.itertext()).split())
        if name in wanted and value:
            out[name].append(value)
        if name == "meta" and value and any(token in (element.get("property", "") + element.get("name", "")).lower() for token in ("edition", "version")):
            out["edition"].append(value or element.get("content", ""))
    return out


def parse_nav(zf: zipfile.ZipFile, nav_path: str) -> list[TocItem]:
    root = ET.fromstring(zf.read(nav_path))
    result: list[TocItem] = []

    def walk(ol: ET.Element, depth: int) -> None:
        for li in list(ol):
            if local(li.tag) != "li":
                continue
            anchor = next((x for x in li.iter() if local(x.tag) == "a" and x.get("href")), None)
            if anchor is not None:
                title = " ".join("".join(anchor.itertext()).split())
                href = posixpath.normpath(posixpath.join(posixpath.dirname(nav_path), anchor.get("href", "")))
                result.append(TocItem(title, href, depth))
            for child in list(li):
                if local(child.tag) == "ol":
                    walk(child, depth + 1)

    nav = next((x for x in root.iter() if local(x.tag) == "nav" and (x.get("{%s}type" % OPF) == "toc" or x.get("type") == "toc")), None)
    if nav is None:
        nav = next((x for x in root.iter() if local(x.tag) == "nav"), None)
    if nav is None:
        return result
    first_ol = next((x for x in nav.iter() if local(x.tag) == "ol"), None)
    if first_ol is not None:
        walk(first_ol, 0)
    return result


def parse_ncx(zf: zipfile.ZipFile, ncx_path: str) -> list[TocItem]:
    root = ET.fromstring(zf.read(ncx_path))
    result: list[TocItem] = []

    def walk(parent: ET.Element, depth: int) -> None:
        for point in list(parent):
            if local(point.tag) != "navPoint":
                continue
            text = next((x for x in point.iter() if local(x.tag) == "text"), None)
            content = next((x for x in point.iter() if local(x.tag) == "content" and x.get("src")), None)
            if text is not None and content is not None:
                title = " ".join("".join(text.itertext()).split())
                href = posixpath.normpath(posixpath.join(posixpath.dirname(ncx_path), content.get("src", "")))
                result.append(TocItem(title, href, depth))
            walk(point, depth + 1)

    nav_map = next((x for x in root.iter() if local(x.tag) == "navMap"), None)
    if nav_map is not None:
        walk(nav_map, 0)
    return result


def table_of_contents(zf: zipfile.ZipFile, manifest: dict) -> list[TocItem]:
    nav = next((v["href"] for v in manifest.values() if "nav" in v["properties"].split()), None)
    if nav:
        items = parse_nav(zf, nav)
        if items:
            return items
    ncx = next((v["href"] for v in manifest.values() if v["media"] == "application/x-dtbncx+xml"), None)
    return parse_ncx(zf, ncx) if ncx else []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("epub")
    parser.add_argument("--toc", action="store_true", help="print the table of contents")
    args = parser.parse_args()
    try:
        with zipfile.ZipFile(args.epub) as zf:
            _, root, manifest, _ = read_package(zf)
            for key, values in metadata(root).items():
                print(f"{key}: {'; '.join(values) if values else '[文件未提供]'}")
            if args.toc:
                print("\nTOC:")
                for index, item in enumerate(table_of_contents(zf, manifest), 1):
                    print(f"{index:03d} {'  ' * item.depth}{item.title} -> {item.href}")
    except (OSError, zipfile.BadZipFile, ET.ParseError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
