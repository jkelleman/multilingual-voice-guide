#!/usr/bin/env python3
"""Lint every locale file against the en-US source.

Errors (exit 1):
  - a turn in the source is missing from a locale
  - placeholders like {date} don't match the source
  - a glossary term in the source turn isn't rendered with the locale's term
  - register violation (e.g. formal Sie in a du locale)

Warnings (reported, don't fail):
  - banned phrases (support-speak, overly formal scripts)
  - text expansion above the locale's budget
  - estimated speaking time above the voice budget

    python scripts/lint_locales.py
    python scripts/lint_locales.py --locale de-DE
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER = re.compile(r"\{[a-z_]+\}")


def load_locales() -> dict[str, dict]:
    return {p.stem: yaml.safe_load(p.read_text(encoding="utf-8"))
            for p in sorted((ROOT / "locales").glob("*.yaml"))}


def load_glossary() -> list[dict]:
    with (ROOT / "glossary" / "glossary.csv").open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", help="lint one locale only")
    args = parser.parse_args()

    config = yaml.safe_load((ROOT / "scripts" / "lint_config.yaml").read_text(encoding="utf-8"))
    locales = load_locales()
    glossary = load_glossary()
    src_id = config["source_locale"]
    source = locales[src_id]["turns"]
    max_secs = config["max_voice_seconds"]

    errors: list[str] = []
    warnings: list[str] = []
    rows = []

    targets = [args.locale] if args.locale else list(locales)
    for loc in targets:
        data = locales[loc]
        cfg = config["locales"].get(loc, {})
        turns = data.get("turns", {})
        cps = cfg.get("chars_per_second", 15)
        longest = 0.0

        for tid, src_text in source.items():
            text = turns.get(tid)
            if text is None:
                errors.append(f"{loc}/{tid}: missing turn")
                continue

            if sorted(PLACEHOLDER.findall(text)) != sorted(PLACEHOLDER.findall(src_text)):
                errors.append(f"{loc}/{tid}: placeholders {PLACEHOLDER.findall(text)} "
                              f"!= source {PLACEHOLDER.findall(src_text)}")

            for term in glossary:
                if term[src_id].lower() in src_text.lower() and loc != src_id:
                    expected = term.get(loc, "")
                    if expected and expected.lower() not in text.lower():
                        errors.append(f"{loc}/{tid}: glossary '{term['term_id']}' "
                                      f"should use '{expected}'")

            for pattern in cfg.get("register_violations", []):
                if re.search(pattern, text):
                    errors.append(f"{loc}/{tid}: register violation /{pattern}/")

            for phrase in cfg.get("banned", []):
                if phrase.lower() in text.lower():
                    warnings.append(f"{loc}/{tid}: banned phrase '{phrase}'")

            ratio = len(text) / len(src_text)
            if "max_expansion" in cfg and ratio > cfg["max_expansion"]:
                warnings.append(f"{loc}/{tid}: {ratio:.2f}x longer than source "
                                f"(budget {cfg['max_expansion']}x)")

            secs = len(PLACEHOLDER.sub("xxxxx", text)) / cps
            longest = max(longest, secs)
            if secs > max_secs:
                warnings.append(f"{loc}/{tid}: ~{secs:.0f}s spoken (budget {max_secs}s)"
                                " - trim or split for voice")

        total_src = sum(len(t) for t in source.values())
        total_loc = sum(len(turns.get(t, "")) for t in source)
        rows.append((loc, data.get("register", {}).get("choice", "?"),
                     len(turns), total_loc / total_src, longest,
                     data.get("review_status", "?")))

    print(f"{'locale':<8}{'register':<14}{'turns':>6}{'length':>8}{'longest':>9}  review")
    for loc, reg, n, ratio, longest, status in rows:
        print(f"{loc:<8}{reg[:13]:<14}{n:>6}{ratio:>7.2f}x{longest:>8.0f}s  {status}")

    if warnings:
        print(f"\n{len(warnings)} warning(s)")
        for w in warnings:
            print(f"  ! {w}")
    if errors:
        print(f"\n{len(errors)} error(s)")
        for e in errors:
            print(f"  x {e}")
        return 1
    print("\nOK: all locales cover every turn, placeholders and glossary terms match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
