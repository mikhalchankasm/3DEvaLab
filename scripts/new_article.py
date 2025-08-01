#!/usr/bin/env python3
import sys, re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"[\s]+", "-", s)
    return s

def main():
    if len(sys.argv) < 3:
        print("Usage: new_article.py <section> <Title> [tag1,tag2,...]")
        print("section: getting-started | how-to | reference | recipes | glossary")
        sys.exit(1)

    section = sys.argv[1]
    title = sys.argv[2]
    tags = sys.argv[3] if len(sys.argv) > 3 else ""

    section_dir = DOCS / section
    if not section_dir.exists():
        print(f"Error: section '{section}' not found in docs/")
        sys.exit(2)

    slug = slugify(title)
    path = section_dir / f"{slug}.md"

    if path.exists():
        print(f"Error: file exists: {path}")
        sys.exit(3)

    today = date.today().isoformat()
    content = f"""---
title: {title}
tags: [{tags}]
updated: {today}
level: basic
---

# {title}

## Контекст
Кратко: когда и зачем это нужно.

## Пошагово
1. Шаг
2. Шаг
3. Шаг

## Пример кода
```pml
!; минимальный пример (при необходимости)
```

## Замечания

* Условия применимости, версии E3D/PML, ссылки.
"""
    
    path.write_text(content, encoding="utf-8")
    print(f"Created: {path}")

if __name__ == "__main__":
    main() 