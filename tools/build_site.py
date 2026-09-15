#!/usr/bin/env python3
"""Build empirecorporation.eu: copy static pages and render the scheduled blog.

Posts live in blog-src/posts/<slug>.html (a JSON META comment + body HTML).
blog-src/schedule.json maps slug -> publish date. A post goes live on the first
build run on or after its date, so a daily cron publishes the queue over time.

Usage:
  build_site.py --out DIR [--state FILE] [--ping] [--today YYYY-MM-DD]
"""

import argparse
import datetime as dt
import email.utils
import html
import json
import math
import os
import re
import shutil
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent
POSTS_DIR = SRC / "blog-src" / "posts"
SCHEDULE = SRC / "blog-src" / "schedule.json"
BASE = "https://empirecorporation.eu"
ORG_NAME = "Empire Corporation Paweł Głowacz"
EMAIL = "empirecorporation.eu@gmail.com"
PHONE = "+48 501 979 488"
PHONE_HREF = "tel:+48501979488"
AUTHOR = "Paweł Głowacz"
INDEXNOW_KEY = "3f9c1e7a5b2d4c8e9a6f0b1d2c3e4f5a"

STATIC = [".htaccess", "index.html", "en.html", "privacy.html", "404.html",
          "robots.txt", "favicon.ico", f"{INDEXNOW_KEY}.txt"]
CATEGORIES = ["Bezpieczeństwo", "AI w firmie", "Aplikacje", "Technologia i zarządzanie"]
MONTHS = ["stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca", "lipca",
          "sierpnia", "września", "października", "listopada", "grudnia"]
ALLOWED_TAGS = {"p", "h2", "h3", "ul", "ol", "li", "strong", "em", "a", "code", "pre",
                "blockquote", "table", "thead", "tbody", "tr", "th", "td", "aside", "br"}

CTA = {
    "Bezpieczeństwo": ("Strona zainfekowana albo dziwnie się zachowuje?",
                       "Usuwamy malware, zamykamy backdoory i zabezpieczamy serwer, żeby infekcja nie wróciła. "
                       "Przy incydencie wpisz w temacie „PILNE”.", "Pomoc przy incydencie"),
    "AI w firmie": ("Chcesz wdrożyć agenta AI w swojej firmie?",
                    "Zaczynamy od jednego procesu i mierzalnego pilota. Pomożemy wybrać zadania, zbudować agenta "
                    "i bezpiecznie podłączyć go do Twoich systemów.", "Wdrożenie AI"),
    "Aplikacje": ("Planujesz aplikację mobilną?",
                  "Pomożemy oszacować zakres, wybrać technologię i przeprowadzić aplikację aż do publikacji "
                  "w App Store i Google Play.", "Aplikacja mobilna"),
    "Technologia i zarządzanie": ("Potrzebujesz niezależnej oceny technologii?",
                                  "Jako zewnętrzny CTO robimy audyty, dajemy drugą opinię do ofert i porządkujemy IT "
                                  "w firmie.", "Konsultacja CTO"),
}


# ---------------------------------------------------------------- helpers

def esc(s):
    return html.escape(str(s), quote=True)


def today_warsaw():
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo("Europe/Warsaw")).date()
    except Exception:
        return dt.date.today()


def pl_date(d):
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def slugify(text):
    table = str.maketrans("ąćęłńóśźżĄĆĘŁŃÓŚŹŻ", "acelnoszzACELNOSZZ")
    text = re.sub(r"<[^>]+>", "", text).translate(table).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:60].strip("-") or "sekcja"


class TextExtractor(HTMLParser):
    """HTML fragment -> readable Markdown-ish text (for word counts and llms-full.txt)."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.list_stack, self.in_pre, self.href = [], [], False, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("p", "blockquote", "aside", "table"):
            self.out.append("\n\n")
        elif tag == "h2":
            self.out.append("\n\n## ")
        elif tag == "h3":
            self.out.append("\n\n### ")
        elif tag in ("ul", "ol"):
            self.list_stack.append(tag)
            self.out.append("\n")
        elif tag == "li":
            self.out.append("\n" + "  " * (len(self.list_stack) - 1) + "- ")
        elif tag == "pre":
            self.in_pre = True
            self.out.append("\n\n```\n")
        elif tag == "tr":
            self.out.append("\n| ")
        elif tag == "br":
            self.out.append("\n")
        elif tag == "a":
            self.href = a.get("href")

    def handle_endtag(self, tag):
        if tag in ("ul", "ol") and self.list_stack:
            self.list_stack.pop()
        elif tag == "pre":
            self.in_pre = False
            self.out.append("\n```")
        elif tag in ("td", "th"):
            self.out.append(" | ")
        elif tag == "a" and self.href:
            if self.href.startswith("http"):
                self.out.append(f" ({self.href})")
            elif self.href.startswith("/"):
                self.out.append(f" ({BASE}{self.href})")
            self.href = None

    def handle_data(self, data):
        self.out.append(data if self.in_pre else re.sub(r"\s+", " ", data))

    def text(self):
        t = "".join(self.out)
        t = re.sub(r"[ \t]+\n", "\n", t)
        return re.sub(r"\n{3,}", "\n\n", t).strip()


def html_to_text(fragment):
    p = TextExtractor()
    p.feed(fragment)
    return p.text()


# ---------------------------------------------------------------- posts

def load_posts(today, warnings):
    schedule = json.loads(SCHEDULE.read_text(encoding="utf-8")) if SCHEDULE.exists() else {}
    position = {slug: i for i, slug in enumerate(schedule)}
    posts = []
    for f in sorted(POSTS_DIR.glob("*.html")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--META\s*(\{.*?\})\s*META-->\s*(.*)\Z", raw, re.S)
        if not m:
            warnings.append(f"{f.name}: missing META block, skipped")
            continue
        try:
            meta = json.loads(m.group(1))
        except json.JSONDecodeError as e:
            warnings.append(f"{f.name}: invalid META JSON ({e}), skipped")
            continue
        slug = meta.get("slug") or f.stem
        if slug != f.stem:
            warnings.append(f"{f.name}: slug '{slug}' differs from file name, using file name")
            slug = f.stem
        missing = [k for k in ("title", "description", "category") if not meta.get(k)]
        if missing:
            warnings.append(f"{slug}: missing {missing}, skipped")
            continue
        if meta["category"] not in CATEGORIES:
            warnings.append(f"{slug}: unknown category '{meta['category']}'")
        if slug not in schedule:
            warnings.append(f"{slug}: not in schedule.json, not published")
            continue
        date = dt.date.fromisoformat(schedule[slug])
        body = m.group(2).strip()
        bad = sorted({t for t in re.findall(r"<\s*([a-zA-Z0-9]+)", body)} - ALLOWED_TAGS)
        if bad:
            warnings.append(f"{slug}: unexpected tags {bad}")
        text = html_to_text(body)
        words = len(re.findall(r"\w+", text))
        posts.append({
            **meta,
            "slug": slug,
            "date": date,
            "updated": dt.date.fromisoformat(meta["updated"]) if meta.get("updated") else date,
            "body": body,
            "text": text,
            "words": words,
            "minutes": max(1, math.ceil(words / 200)),
            "url": f"{BASE}/blog/{slug}/",
            "path": f"/blog/{slug}/",
            "published": date <= today,
            "position": position[slug],
        })
    for slug in schedule:
        if not (POSTS_DIR / f"{slug}.html").exists():
            warnings.append(f"schedule.json: '{slug}' has no post file yet")
    # newest first; posts sharing a date keep their schedule order
    posts.sort(key=lambda p: (-p["date"].toordinal(), p["position"]))
    return posts


def process_body(body, published_slugs):
    toc = []

    def add_id(m):
        attrs, inner = m.group(1), m.group(2)
        hid = re.search(r'id="([^"]+)"', attrs)
        hid = hid.group(1) if hid else slugify(inner)
        base, n = hid, 2
        while any(t[0] == hid for t in toc):
            hid, n = f"{base}-{n}", n + 1
        toc.append((hid, re.sub(r"<[^>]+>", "", inner)))
        attrs = re.sub(r'\s*id="[^"]*"', "", attrs)
        return f'<h2 id="{hid}"{attrs}>{inner}</h2>'

    body = re.sub(r"<h2([^>]*)>(.*?)</h2>", add_id, body, flags=re.S)

    def link(m):
        slug = m.group(1)
        return m.group(0) if slug in published_slugs else m.group(2)

    body = re.sub(r'<a\s+href="/blog/([a-z0-9-]+)/?(?:#[^"]*)?"[^>]*>(.*?)</a>', link, body, flags=re.S)
    body = re.sub(r'<a\s+href="(https?://[^"]+)"(?![^>]*rel=)', r'<a href="\1" rel="noopener"', body)
    body = re.sub(r"<table>", '<div class="table-wrap"><table>', body)
    body = re.sub(r"</table>", "</table></div>", body)
    return body, toc


# ---------------------------------------------------------------- page shell

def org_node():
    return {
        "@type": "Organization",
        "@id": f"{BASE}/#organization",
        "name": ORG_NAME,
        "alternateName": "Empire Corporation",
        "url": f"{BASE}/",
        "logo": {"@type": "ImageObject", "url": f"{BASE}/assets/img/logo-512.png", "width": 512, "height": 512},
        "email": EMAIL,
        "telephone": PHONE.replace(" ", ""),
        "taxID": "6642140734",
    }


def author_node():
    return {"@type": "Person", "@id": f"{BASE}/#author", "name": AUTHOR, "url": f"{BASE}/",
            "worksFor": {"@id": f"{BASE}/#organization"}}


def ld_script(graph):
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    return '<script type="application/ld+json">\n' + data.replace("</", "<\\/") + "\n</script>"


def page(*, title, description, canonical, body, og_image, og_type="website", ld=None, year):
    return f"""<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{esc(canonical)}">
  <link rel="alternate" type="application/rss+xml" title="Blog Empire Corporation" href="/blog/feed.xml">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/assets/img/favicon-96.png" sizes="96x96" type="image/png">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <meta name="theme-color" content="#f3f1ec">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Empire Corporation">
  <meta property="og:locale" content="pl_PL">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(canonical)}">
  <meta property="og:image" content="{esc(og_image)}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preload" href="/assets/fonts/ibm-plex-sans-400-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/style.css">
  {ld or ""}
</head>
<body>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Empire Corporation — strona główna">
      <img src="/assets/img/logo.svg" alt="" width="32" height="32">
      Empire Corporation
    </a>
    <nav class="nav" aria-label="Główna nawigacja">
      <a href="/#uslugi">Usługi</a>
      <a href="/#bezpieczenstwo">Bezpieczeństwo</a>
      <a href="/blog/">Blog</a>
      <a class="nav-contact" href="/#kontakt">Kontakt</a>
      <a class="lang" href="/en.html" hreflang="en" lang="en">EN</a>
    </nav>
  </div>
</header>

<main>
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <span>© {year} {ORG_NAME}</span>
    <nav aria-label="Stopka">
      <a href="/blog/">Blog</a>
      <a href="/privacy.html">Polityka prywatności</a>
      <a href="/en.html" hreflang="en" lang="en">English</a>
    </nav>
  </div>
</footer>

</body>
</html>
"""


def og_image_for(slug):
    return f"{BASE}/assets/img/blog/{slug}.png" if (SRC / "assets/img/blog" / f"{slug}.png").exists() \
        else f"{BASE}/assets/img/og.png"


# ---------------------------------------------------------------- renderers

def render_post(post, published, year):
    published_slugs = {p["slug"] for p in published}
    body, toc = process_body(post["body"], published_slugs)
    cat = post["category"]
    cta_title, cta_text, subject = CTA.get(cat, CTA["Technologia i zarządzanie"])
    mailto = f"mailto:{EMAIL}?subject={urllib.parse.quote(subject + ': ' + post['title'])}"

    tldr = "".join(f"<li>{esc(t)}</li>" for t in post.get("tldr", []))
    tldr_html = f'<aside class="tldr" aria-label="W skrócie"><p class="label">W skrócie</p><ul>{tldr}</ul></aside>' if tldr else ""

    toc_html = ""
    if len(toc) >= 3:
        items = "".join(f'<li><a href="#{hid}">{esc(t)}</a></li>' for hid, t in toc)
        toc_html = f'<nav class="toc" aria-label="Spis treści"><p class="label">Spis treści</p><ol>{items}</ol></nav>'

    faq = post.get("faq", [])
    faq_html = ""
    if faq:
        items = "".join(f'<div class="faq-item"><h3>{esc(q["q"])}</h3><p>{esc(q["a"])}</p></div>' for q in faq)
        faq_html = f'<section class="faq" aria-labelledby="faq"><h2 id="faq">Najczęściej zadawane pytania</h2>{items}</section>'

    sources = post.get("sources", [])
    sources_html = ""
    if sources:
        items = "".join(f'<li><a href="{esc(s["url"])}" rel="noopener">{esc(s["title"])}</a></li>' for s in sources)
        sources_html = f'<section class="sources" aria-labelledby="zrodla"><h2 id="zrodla">Źródła</h2><ul>{items}</ul></section>'

    related = [p for p in published if p["slug"] != post["slug"] and p["category"] == cat][:3]
    if len(related) < 3:
        related += [p for p in published if p["slug"] != post["slug"] and p not in related][:3 - len(related)]
    related_html = ""
    if related:
        items = "".join(
            f'<li><a href="{p["path"]}"><span class="label">{esc(p["category"])}</span>'
            f'<strong>{esc(p["title"])}</strong><span class="desc">{esc(p["description"])}</span></a></li>'
            for p in related)
        related_html = f'<section class="related" aria-labelledby="powiazane"><div class="wrap"><h2 id="powiazane">Przeczytaj też</h2><ul class="post-cards">{items}</ul></div></section>'

    updated = ""
    if post["updated"] != post["date"]:
        updated = f' · aktualizacja <time datetime="{post["updated"].isoformat()}">{pl_date(post["updated"])}</time>'

    article = f"""<article class="post">
  <div class="wrap post-wrap">
    <nav class="breadcrumbs" aria-label="Okruszki"><a href="/">Strona główna</a> <span>/</span> <a href="/blog/">Blog</a> <span>/</span> <span>{esc(cat)}</span></nav>
    <header class="post-head">
      <p class="label">{esc(cat)}</p>
      <h1>{esc(post["title"])}</h1>
      <p class="post-meta"><span>{AUTHOR}</span> · <time datetime="{post["date"].isoformat()}">{pl_date(post["date"])}</time>{updated} · {post["minutes"]} min czytania</p>
    </header>
    {tldr_html}
    {toc_html}
    <div class="prose">
{body}
    </div>
    {faq_html}
    <aside class="cta" aria-label="Kontakt">
      <p class="label">Empire Corporation</p>
      <h2>{esc(cta_title)}</h2>
      <p>{esc(cta_text)}</p>
      <p class="cta-actions"><a class="btn btn-accent" href="{esc(mailto)}">Napisz: {EMAIL}</a> <a class="btn btn-ghost" href="{PHONE_HREF}">{PHONE}</a></p>
    </aside>
    <aside class="author" aria-label="Autor">
      <img src="/assets/img/logo.svg" alt="" width="44" height="44">
      <div><p class="author-name">{AUTHOR}</p><p>Założyciel Empire Corporation. Buduje aplikacje mobilne i webowe, wdraża agentów AI w firmach i zabezpiecza strony oraz serwery.</p></div>
    </aside>
    {sources_html}
  </div>
</article>
{related_html}"""

    ld = [
        org_node(),
        author_node(),
        {
            "@type": "BlogPosting",
            "@id": post["url"] + "#article",
            "headline": post["title"],
            "description": post["description"],
            "datePublished": post["date"].isoformat(),
            "dateModified": post["updated"].isoformat(),
            "inLanguage": "pl-PL",
            "mainEntityOfPage": post["url"],
            "url": post["url"],
            "image": og_image_for(post["slug"]),
            "articleSection": cat,
            "keywords": ", ".join(post.get("tags", [])),
            "wordCount": post["words"],
            "author": {"@id": f"{BASE}/#author"},
            "publisher": {"@id": f"{BASE}/#organization"},
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Strona główna", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/blog/"},
                {"@type": "ListItem", "position": 3, "name": post["title"], "item": post["url"]},
            ],
        },
    ]
    if faq:
        ld.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in faq]})

    return page(
        title=post.get("metaTitle") or post["title"],
        description=post["description"],
        canonical=post["url"],
        body=article,
        og_image=og_image_for(post["slug"]),
        og_type="article",
        ld=ld_script(ld),
        year=year,
    )


def post_card(p):
    return (f'<li><a href="{p["path"]}"><span class="label">{esc(p["category"])} · '
            f'<time datetime="{p["date"].isoformat()}">{pl_date(p["date"])}</time></span>'
            f'<strong>{esc(p["title"])}</strong><span class="desc">{esc(p["description"])}</span></a></li>')


def render_index(published, year):
    if published:
        rows = "".join(
            f'<li class="blog-row"><div class="blog-row-meta"><span class="label">{esc(p["category"])}</span>'
            f'<time datetime="{p["date"].isoformat()}">{pl_date(p["date"])}</time> · {p["minutes"]} min</div>'
            f'<div><h2><a href="{p["path"]}">{esc(p["title"])}</a></h2><p>{esc(p["description"])}</p></div></li>'
            for p in published)
        listing = f'<ol class="blog-list">{rows}</ol>'
    else:
        listing = '<p class="empty">Pierwsze wpisy pojawią się wkrótce.</p>'
    body = f"""<section class="section blog-index">
  <div class="wrap">
    <div class="section-head">
      <div>
        <p class="label">Blog</p>
        <h1>Poradniki i analizy</h1>
      </div>
      <p>Piszemy o tym, czym zajmujemy się na co dzień: aplikacje mobilne, agenci AI i automatyzacja, porządek w IT oraz bezpieczeństwo stron i serwerów. <a href="/blog/feed.xml">RSS</a></p>
    </div>
    {listing}
  </div>
</section>"""
    ld = [org_node(), {
        "@type": "Blog",
        "@id": f"{BASE}/blog/#blog",
        "name": "Blog Empire Corporation",
        "url": f"{BASE}/blog/",
        "inLanguage": "pl-PL",
        "publisher": {"@id": f"{BASE}/#organization"},
        "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": p["url"],
                      "datePublished": p["date"].isoformat()} for p in published],
    }]
    return page(title="Blog: aplikacje, agenci AI i bezpieczeństwo — Empire Corporation",
                description="Praktyczne poradniki o aplikacjach mobilnych, wdrażaniu agentów AI, automatyzacji, "
                            "zarządzaniu IT i bezpieczeństwie stron oraz serwerów.",
                canonical=f"{BASE}/blog/", body=body, og_image=f"{BASE}/assets/img/og.png",
                ld=ld_script(ld), year=year)


def render_home_section(published):
    if not published:
        return ""
    cards = "".join(post_card(p) for p in published[:3])
    return f"""<section class="section" id="blog" style="border-top:1px solid var(--rule)">
    <div class="wrap">
      <div class="section-head">
        <div>
          <p class="label">Blog</p>
          <h2>Poradniki i analizy</h2>
        </div>
        <p>Piszemy o tym, czym zajmujemy się na co dzień. <a href="/blog/">Wszystkie wpisy</a></p>
      </div>
      <ul class="post-cards">{cards}</ul>
    </div>
  </section>"""


def render_feed(published):
    items = []
    for p in published[:30]:
        pub = email.utils.format_datetime(dt.datetime.combine(p["date"], dt.time(7, 0), dt.timezone.utc))
        body, _ = process_body(p["body"], {x["slug"] for x in published})
        body = body.replace('href="/', f'href="{BASE}/')
        items.append(f"""    <item>
      <title>{esc(p["title"])}</title>
      <link>{p["url"]}</link>
      <guid isPermaLink="true">{p["url"]}</guid>
      <pubDate>{pub}</pubDate>
      <category>{esc(p["category"])}</category>
      <description>{esc(p["description"])}</description>
      <content:encoded><![CDATA[{body.replace("]]>", "]]&gt;")}]]></content:encoded>
    </item>""")
    last = email.utils.format_datetime(dt.datetime.now(dt.timezone.utc))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Blog Empire Corporation</title>
    <link>{BASE}/blog/</link>
    <atom:link href="{BASE}/blog/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Aplikacje mobilne, agenci AI, automatyzacja i bezpieczeństwo IT.</description>
    <language>pl-PL</language>
    <lastBuildDate>{last}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""


def render_sitemap(published, today):
    latest = published[0]["date"].isoformat() if published else today.isoformat()
    alt = (f'    <xhtml:link rel="alternate" hreflang="pl" href="{BASE}/"/>\n'
           f'    <xhtml:link rel="alternate" hreflang="en" href="{BASE}/en.html"/>\n'
           f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/"/>\n')
    urls = [
        f"  <url>\n    <loc>{BASE}/</loc>\n    <lastmod>{latest}</lastmod>\n{alt}  </url>",
        f"  <url>\n    <loc>{BASE}/en.html</loc>\n    <lastmod>2026-09-15</lastmod>\n{alt}  </url>",
        f"  <url>\n    <loc>{BASE}/blog/</loc>\n    <lastmod>{latest}</lastmod>\n  </url>",
    ]
    urls += [f"  <url>\n    <loc>{p['url']}</loc>\n    <lastmod>{p['updated'].isoformat()}</lastmod>\n  </url>"
             for p in published]
    urls.append(f"  <url>\n    <loc>{BASE}/privacy.html</loc>\n    <lastmod>2026-09-15</lastmod>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(urls) + "\n</urlset>\n")


ABOUT = f"""# Empire Corporation

> Empire Corporation ({ORG_NAME}, NIP 6642140734) to polski software house. Budujemy aplikacje mobilne na iOS i Androida oraz aplikacje webowe, wdrażamy agentów AI w firmach (serwery MCP, RAG), wprowadzamy AI do procesu wytwarzania oprogramowania, działamy jako zewnętrzny CTO i zajmujemy się bezpieczeństwem stron, serwerów i sieci.

Kontakt: {EMAIL}, tel. {PHONE}. Obsługujemy firmy z Polski i Unii Europejskiej, po polsku i po angielsku.

## Usługi

- Aplikacje mobilne: natywne i cross-platform na iOS i Androida, backend i API, publikacja w App Store i Google Play, utrzymanie.
- Aplikacje webowe: systemy i panele dla firm, platformy SaaS, sklepy, integracje (Laravel, PHP, React, TypeScript, Node.js).
- Wdrażanie agentów AI: agenci do obsługi e-maili, dokumentów, zgłoszeń i raportów; serwery MCP do systemów firmy; RAG na firmowych dokumentach.
- Usprawnianie SDLC z AI: specyfikacje, code review, testy, CI/CD.
- Zewnętrzny CTO: audyt architektury i kodu, druga opinia do ofert software house'ów, roadmapa, nadzór nad dostawcą, przygotowanie do due diligence.
- Automatyzacja środowisk: infrastruktura jako kod, Ansible, Docker, Linux, CI/CD.
- Blockchain: smart kontrakty, tokeny i NFT, integracje z portfelami (Ethereum, EVM, web3).
- Bezpieczeństwo: testy penetracyjne, usuwanie malware ze stron (m.in. ClickFix, SocGholish, backdoory PHP), zabezpieczanie stron i serwerów, wdrożenia Wazuh, Suricata, Elastic Stack (ELK), Prometheus i Grafana.
- Strony internetowe: szybkie strony firmowe, techniczne SEO, bezpieczeństwo.

## Strony

- [Strona główna (PL)]({BASE}/): usługi, proces współpracy, kontakt
- [English version]({BASE}/en.html): services and contact in English
- [Blog]({BASE}/blog/): poradniki o aplikacjach, AI i bezpieczeństwie
- [Polityka prywatności]({BASE}/privacy.html)
"""


def render_llms(published):
    lines = [ABOUT, "## Blog\n"]
    lines += [f"- [{p['title']}]({p['url']}): {p['description']}" for p in published]
    return "\n".join(lines).rstrip() + "\n"


def render_llms_full(published):
    parts = [ABOUT, "\n# Wpisy z bloga\n"]
    for p in published:
        tldr = "\n".join(f"- {t}" for t in p.get("tldr", []))
        faq = "\n\n".join(f"**{q['q']}**\n{q['a']}" for q in p.get("faq", []))
        body, _ = process_body(p["body"], {x["slug"] for x in published})
        parts.append(
            f"\n---\n\n# {p['title']}\n\nURL: {p['url']}\nKategoria: {p['category']}\n"
            f"Data publikacji: {p['date'].isoformat()}\nAutor: {AUTHOR}, {ORG_NAME}\n\n"
            + (f"## W skrócie\n\n{tldr}\n\n" if tldr else "")
            + html_to_text(body)
            + (f"\n\n## Najczęściej zadawane pytania\n\n{faq}" if faq else "")
            + "\n")
    return "\n".join(parts)


# ---------------------------------------------------------------- output

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = content.encode("utf-8") if isinstance(content, str) else content
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def ping_indexnow(urls, log):
    if not urls:
        return
    payload = json.dumps({"host": "empirecorporation.eu", "key": INDEXNOW_KEY,
                          "keyLocation": f"{BASE}/{INDEXNOW_KEY}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=payload,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            log(f"IndexNow: HTTP {r.status} for {len(urls)} URL(s)")
    except Exception as e:
        log(f"IndexNow failed: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--state", type=Path, help="JSON file remembering already announced URLs")
    ap.add_argument("--ping", action="store_true", help="notify IndexNow about newly published URLs")
    ap.add_argument("--today", type=dt.date.fromisoformat)
    args = ap.parse_args()

    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = lambda msg: print(f"[{now}] {msg}")
    today = args.today or today_warsaw()
    warnings = []
    posts = load_posts(today, warnings)
    published = [p for p in posts if p["published"]]
    queued = sorted((p for p in posts if not p["published"]), key=lambda p: p["date"])
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    # static files and assets
    for name in STATIC:
        src = SRC / name
        if src.exists():
            if name == "index.html":
                content = src.read_text(encoding="utf-8").replace("<!-- BLOG:LATEST -->", render_home_section(published))
                write(out / name, content)
            else:
                write(out / name, src.read_bytes())
    shutil.copytree(SRC / "assets", out / "assets", dirs_exist_ok=True)

    # blog: render into a fresh directory, then swap it in
    staging = out / ".blog-staging"
    shutil.rmtree(staging, ignore_errors=True)
    year = today.year
    write(staging / "index.html", render_index(published, year))
    write(staging / "feed.xml", render_feed(published))
    for p in published:
        write(staging / p["slug"] / "index.html", render_post(p, published, year))
    old = out / ".blog-old"
    shutil.rmtree(old, ignore_errors=True)
    if (out / "blog").exists():
        os.replace(out / "blog", old)
    os.replace(staging, out / "blog")
    shutil.rmtree(old, ignore_errors=True)

    write(out / "sitemap.xml", render_sitemap(published, today))
    write(out / "llms.txt", render_llms(published))
    write(out / "llms-full.txt", render_llms_full(published))

    for w in warnings:
        log(f"WARN {w}")
    log(f"today={today} published={len(published)} queued={len(queued)}"
        + (f" next={queued[0]['date']} {queued[0]['slug']}" if queued else ""))

    if args.state:
        state = json.loads(args.state.read_text(encoding="utf-8")) if args.state.exists() else {"announced": []}
        announced = set(state["announced"])
        current = [f"{BASE}/", f"{BASE}/blog/"] + [p["url"] for p in published]
        new_posts = [u for u in current if u not in announced]
        if new_posts:
            log("new URLs: " + ", ".join(new_posts))
            if args.ping:
                ping_indexnow(sorted(set(new_posts) | {f"{BASE}/", f"{BASE}/blog/"}), log)
            state["announced"] = sorted(announced | set(current))
            write(args.state, json.dumps(state, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
