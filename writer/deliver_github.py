#!/usr/bin/env python3
"""Lay out a Shopify client's built posts as a GitHub Pages repo.

  python3 deliver_github.py <client-dir> <repo-dir>

<repo>/<handle>.html      preview: viewport + noindex shell, featured image + theme-style H1, then the article
<repo>/raw/<handle>.html  exactly what to paste into Shopify's article HTML editor
<repo>/shopify/<handle>.json  the Shopify fields (title, handle, SEO title/description, excerpt, tags, date)
<repo>/covers/<handle>.png    featured image to upload
<repo>/writer/                the sources and tools that produced it
"""
import html as H
import json
import pathlib
import shutil
import sys

WRITER = pathlib.Path(__file__).resolve().parent

PREVIEW = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{title} (preview)</title><meta name="description" content="{desc}">
<style>body{{margin:0;background:#fff;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif}}
.pv{{background:#232329;color:#e1e1e1;font:12.5px/1.5 ui-monospace,Menlo,monospace;padding:10px 16px}}
.pv a{{color:#b795ea}}.art{{max-width:1100px;margin:0 auto;padding:24px 16px 0}}
.art .feat{{display:block;width:100%;height:auto;border-radius:3px}}
.art h1{{font-family:Oswald,Arial Narrow,sans-serif;font-size:clamp(28px,4.4vw,44px);line-height:1.15;margin:22px 0 6px;color:#232329}}
.art .meta{{color:#6b6b73;font-size:13px;margin-bottom:8px}}</style></head><body>
<div class="pv">PREVIEW ONLY &middot; paste <a href="raw/{handle}.html">raw/{handle}.html</a> into Shopify &middot; fields in <a href="shopify/{handle}.json">shopify/{handle}.json</a> &middot; <a href="./">all posts</a></div>
<div class="art"><img class="feat" src="covers/{handle}.png" alt="{title} featured image"><h1>{title}</h1><div class="meta">The Garage &middot; {date}</div></div>
{body}
</body></html>
"""


def main(client_dir, repo_dir):
    d, repo = pathlib.Path(client_dir), pathlib.Path(repo_dir)
    cfg = json.loads((d / "client.json").read_text())
    for sub in ("raw", "shopify", "covers", "writer/src", "writer/data"):
        (repo / sub).mkdir(parents=True, exist_ok=True)
    rows = []
    for h in cfg["october"]:
        body = (d / "out" / f"{h}.html").read_text()
        meta = json.loads((d / "out" / f"{h}.json").read_text())
        meta["featured_image_file"] = f"covers/{h}.png"
        (repo / "raw" / f"{h}.html").write_text(body)
        (repo / "shopify" / f"{h}.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
        shutil.copy(d / "covers" / f"{h}.png", repo / "covers" / f"{h}.png")
        (repo / f"{h}.html").write_text(PREVIEW.format(title=H.escape(meta["title"]), desc=H.escape(meta["seo_description"]),
                                                     handle=h, date=meta["published"], body=body))
        rows.append(meta)
    for f in ("harvest.py", "build.py", "deliver_github.py"):
        shutil.copy(WRITER / f, repo / "writer" / f)
    for f in ("client.json", cfg["css"], "make_covers.py", "verify_live_theme.py"):
        shutil.copy(d / f, repo / "writer" / f)
    for f in ("catalog.json", "alts.json"):
        shutil.copy(d / "data" / f, repo / "writer" / "data" / f)
    for f in sorted((d / "src").glob("*.html")):
        shutil.copy(f, repo / "writer" / "src" / f.name)
    cards = "".join(
        f'<a class="c" href="{m["handle"]}.html"><img src="covers/{m["handle"]}.png" alt="{H.escape(m["title"])} featured image" loading="lazy">'
        f'<b>{H.escape(m["title"])}</b><span>{m["published"]} &middot; /blogs/{cfg["blog"]}/{m["handle"]}</span></a>' for m in rows)
    (repo / "index.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="robots" content="noindex,nofollow"><title>MotorBae October 2026 blog previews</title><style>'
        'body{margin:0;background:#0b0b0d;color:#e1e1e1;font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif}'
        '.w{max-width:1100px;margin:0 auto;padding:32px 16px}h1{color:#b795ea;margin:0 0 6px}p{color:#9a9aa3;margin:0 0 22px}'
        '.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}'
        '.c{display:flex;flex-direction:column;gap:6px;background:#17171b;border:1px solid #2a2a31;border-radius:6px;overflow:hidden;color:#fff;text-decoration:none;padding-bottom:12px}'
        '.c img{width:100%;height:auto;display:block}.c b,.c span{padding:0 12px}.c span{color:#8f8f99;font-size:12.5px;font-family:ui-monospace,Menlo,monospace;overflow-wrap:anywhere}'
        f'</style></head><body><div class="w"><h1>MotorBae: October 2026 blogs</h1><p>{len(rows)} Shopify-ready posts for The Garage. '
        'Each preview shows the post as the theme renders it; the paste-ready HTML is in raw/. See the README for publishing steps.</p>'
        f'<div class="g">{cards}</div></div></body></html>\n')
    print(f"wrote {len(rows)} posts to {repo}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
