#!/usr/bin/env python3
"""Write blog-src/linkedin.md: ready-to-post LinkedIn texts in publication order."""

import json
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
BASE = "https://empirecorporation.eu"


def main():
    schedule = json.loads((SRC / "blog-src" / "schedule.json").read_text(encoding="utf-8"))
    out = ["# Posty na LinkedIn",
           "",
           "Wrzuć post w dniu publikacji wpisu (cron publikuje o 6:10). "
           "Link w poście prowadzi do artykułu; obrazek podglądu wczyta się sam.",
           ""]
    for slug, date in schedule.items():
        f = SRC / "blog-src" / "posts" / f"{slug}.html"
        if not f.exists():
            out += [f"## {date} · {slug}", "", "_Wpis jeszcze nie jest gotowy._", ""]
            continue
        meta = json.loads(re.match(r"\s*<!--META\s*(\{.*?\})\s*META-->", f.read_text(encoding="utf-8"), re.S).group(1))
        url = f"{BASE}/blog/{slug}/"
        text = meta.get("linkedin", "").replace("{url}", url).strip()
        out += [f"## {date} · {meta['title']}", "", url, "", text, "", "---", ""]
    (SRC / "blog-src" / "linkedin.md").write_text("\n".join(out), encoding="utf-8", newline="\n")
    print("wrote blog-src/linkedin.md")


if __name__ == "__main__":
    main()
