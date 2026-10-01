#!/usr/bin/env python3
"""Harvest a Shopify store's real catalogue from its public JSON, so blogs quote only real
products, prices, fabric facts, images and URLs.

  python3 harvest.py <store-domain> <client-dir>     e.g. motorbae.store ../Motorbae_PSEO

Writes <client-dir>/data/catalog.json:
  products: handle, title, url, price, compare_at, available, gsm, fit, colors, sizes, images, collections
  collections: handle, title, url, count
  articles: handle, title, url, published   (the store's existing blog posts, for internal links)
"""
import html
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def get(url, tries=6):
    """Shopify rate-limits public JSON (429); back off and retry."""
    for n in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or n == tries - 1:
                raise
            time.sleep(2 ** n)


def store_cdn(src, domain, width=1200):
    """cdn.shopify.com/s/files/1/<a>/<b>/files/NAME?v=X -> https://<domain>/cdn/shop/files/NAME?v=X&width=W
    (same file, served from the store's own domain like the theme does)."""
    m = re.search(r".*/files/([^/?]+)\?v=(\d+)", src)
    return f"https://{domain}/cdn/shop/files/{m.group(1)}?v={m.group(2)}&width={width}" if m else src


def paged(domain, path, key):
    out, page = [], 1
    while True:
        j = json.loads(get(f"https://{domain}/{path}{'&' if '?' in path else '?'}limit=250&page={page}"))
        if not j.get(key):
            return out
        out += j[key]
        page += 1


def main(domain, client_dir):
    data = pathlib.Path(client_dir) / "data"
    data.mkdir(parents=True, exist_ok=True)
    cols = paged(domain, "collections.json", "collections")
    member = {}
    for c in cols:
        for p in paged(domain, f"collections/{c['handle']}/products.json", "products"):
            member.setdefault(p["handle"], []).append(c["handle"])
    products = []
    for p in paged(domain, "products.json", "products"):
        body = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", p.get("body_html") or "")).split())
        v = p["variants"]
        opts = {o["name"].lower(): o["values"] for o in p["options"]}
        gsm = re.search(r"(\d{3})\s*GSM", body, re.I)
        fit = re.search(r"Fit\s*:\s*([^.]+)", body, re.I)
        products.append({
            "handle": p["handle"], "title": p["title"].strip(),
            "url": f"https://{domain}/products/{p['handle']}",
            "price": min(float(x["price"]) for x in v),
            "compare_at": max([float(x["compare_at_price"]) for x in v if x.get("compare_at_price")] or [0]) or None,
            "available": any(x.get("available") for x in v),
            "gsm": int(gsm.group(1)) if gsm else None,
            "fit": fit.group(1).strip()[:120] if fit else None,
            "colors": opts.get("color") or opts.get("colour") or [],
            "sizes": opts.get("size") or [],
            "tags": p["tags"],
            "images": [store_cdn(i["src"], domain) for i in p["images"]],
            "collections": member.get(p["handle"], []),
            "description": body[:900],
        })
    atom = get(f"https://{domain}/blogs/the-garage.atom").decode("utf-8", "ignore")
    articles = []
    for e in re.findall(r"<entry>(.*?)</entry>", atom, re.S):
        url = re.search(r'<link[^>]*href="([^"]+)"', e).group(1)
        articles.append({"handle": url.rsplit("/", 1)[-1], "url": url,
                         "title": html.unescape(re.search(r"<title>(.*?)</title>", e).group(1)),
                         "published": re.search(r"<published>(.{10})", e).group(1)})
    cat = {"domain": domain, "products": products, "articles": articles,
           "collections": [{"handle": c["handle"], "title": c["title"].strip(),
                            "url": f"https://{domain}/collections/{c['handle']}",
                            "count": c.get("products_count")} for c in cols]}
    (data / "catalog.json").write_text(json.dumps(cat, indent=1, ensure_ascii=False))
    print(f"{len(products)} products, {len(cols)} collections, {len(articles)} articles -> {data / 'catalog.json'}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
