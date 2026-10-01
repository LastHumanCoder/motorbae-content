#!/usr/bin/env python3
"""Build Shopify blog-article bodies from authored sources + the harvested catalogue, and gate them.

  python3 build.py <client-dir> [handle ...]

Source: <client-dir>/src/<handle>.html = a header comment (title, meta, keyword, lede, quick...)
followed by the body sections, then <!--FAQ--> and five <details class="faq-item">.
Placeholders resolved from data/catalog.json, so prices, images and URLs are always real:
  {{PRODUCTS:h1,h2,...}}         product card grid (image, name, price, GSM, link)
  {{IMG:handle#n|caption}}       captioned product photo (alt from data/alts.json for n=0)
  {{PRICE:handle}}               the live price, e.g. Rs 1,599 shown as ₹1,599
  {{P:handle|anchor}}            link to a product
  {{C:handle|anchor}}            link to a collection
  {{SHOP:c:handle|Label;p:handle|Label}}  pill CTA row

Output: <client-dir>/out/<handle>.html (paste into Shopify's article HTML view) + <handle>.json
(title, SEO description, excerpt, handle, tags for the Shopify fields).
"""
import html as H
import json
import pathlib
import re
import sys

PAREN = re.compile(r"\{\{(\w+):([^}]*)\}\}")


def load(client_dir):
    d = pathlib.Path(client_dir)
    cfg = json.loads((d / "client.json").read_text())
    cat = json.loads((d / "data" / "catalog.json").read_text())
    alts = json.loads((d / "data" / "alts.json").read_text())
    return d, cfg, cat, alts


def rupees(x):
    return "₹" + f"{x:,.0f}"


def head(src):
    m = re.match(r"\s*<!--(.*?)-->", src, re.S)
    meta, key = {}, None
    for line in m.group(1).splitlines():
        k = re.match(r"^([a-z_]+):\s?(.*)$", line)
        if k:
            key = k.group(1); meta[key] = k.group(2).strip()
        elif key and line.strip():
            meta[key] += " " + line.strip()
    return meta, src[m.end():]


class Ctx:
    def __init__(self, cfg, cat, alts):
        self.cfg, self.alts = cfg, alts
        self.P = {p["handle"]: p for p in cat["products"]}
        self.C = {c["handle"]: c for c in cat["collections"]}
        self.base = f"https://{cfg['domain']}"

    def prod(self, h):
        if h not in self.P:
            raise KeyError(f"unknown product {h}")
        return self.P[h]

    def card(self, h):
        p = self.prod(h)
        img = p["images"][0]
        was = f"<s>{rupees(p['compare_at'])}</s>" if p["compare_at"] and p["compare_at"] > p["price"] else ""
        spec = " · ".join(x for x in (f"{p['gsm']} GSM" if p["gsm"] else "", f"{len(p['colors'])} colours" if len(p["colors"]) > 1 else "") if x)
        return (f'<a class="pcard" href="{p["url"]}"><img src="{img.replace("width=1200", "width=600")}" '
                f'alt="{H.escape(self.alts[h])}" loading="lazy" width="600" height="600"><span class="pbody">'
                f'<span class="pname">{H.escape(p["title"])}</span><span class="pprice">{rupees(p["price"])}{was}</span>'
                f'{f"<span class=pspec>{spec}</span>" if spec else ""}</span></a>')

    def expand(self, s):
        def sub(m):
            kind, arg = m.group(1), m.group(2)
            if kind == "PRODUCTS":
                return '<div class="pgrid">' + "".join(self.card(h.strip()) for h in arg.split(",")) + "</div>"
            if kind == "IMG":
                ref, cap = arg.split("|", 1)
                h, n = (ref.split("#") + ["0"])[:2]
                p = self.prod(h); n = int(n)
                alt = self.alts[h] if n == 0 else cap
                return (f'<figure><img src="{p["images"][n]}" alt="{H.escape(alt)}" loading="lazy">'
                        f'<figcaption>{cap} <a href="{p["url"]}">{H.escape(p["title"])}</a>, {rupees(p["price"])}.</figcaption></figure>')
            if kind == "PRICE":
                return rupees(self.prod(arg)["price"])
            if kind == "P":
                h, a = arg.split("|"); return f'<a href="{self.prod(h)["url"]}">{a}</a>'
            if kind == "C":
                h, a = arg.split("|")
                if h != "all" and h not in self.C:
                    raise KeyError(f"unknown collection {h}")
                return f'<a href="{self.base}/collections/{h}">{a}</a>'
            if kind == "SHOP":
                out = []
                for item in arg.split(";"):
                    ref, label = item.split("|")
                    t, h = ref.split(":")
                    url = self.prod(h)["url"] if t == "p" else f"{self.base}/collections/{h}"
                    if t == "c" and h != "all" and h not in self.C:
                        raise KeyError(f"unknown collection {h}")
                    out.append(f'<a href="{url}">{label}</a>')
                return '<div class="shoplinks">' + "".join(out) + "</div>"
            raise KeyError(kind)
        return PAREN.sub(sub, s)


def build(d, cfg, cat, alts, handle):
    x = Ctx(cfg, cat, alts)
    meta, rest = head((d / "src" / f"{handle}.html").read_text())
    body, faq = rest.split("<!--FAQ-->")
    body = x.expand(body.strip()); faq = faq.strip()
    qa = re.findall(r"<summary>(.*?)</summary>\s*<p class=\"faq-a\">(.*?)</p>", faq, re.S)
    plain = lambda t: H.unescape(re.sub(r"<[^>]+>", "", t)).strip()
    url = f"{x.base}/blogs/{cfg['blog']}/{handle}"
    post = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": meta["title"],
            "description": meta["meta"], "author": {"@type": "Organization", "name": cfg["brand"]},
            "publisher": {"@type": "Organization", "name": cfg["brand"], "logo": {"@type": "ImageObject", "url": cfg["logo"]}},
            "datePublished": meta["date"], "dateModified": meta["date"], "mainEntityOfPage": url,
            "image": x.prod(meta["cover"].split("|")[0].split("#")[0])["images"][0]}
    faqld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in qa]}
    cref, calt = meta["cover"].split("|", 1)
    ch, cn = (cref.split("#") + ["0"])[:2]
    cover = x.prod(ch)["images"][int(cn)]
    nav = "".join(f'<a href="#{i}">{t}</a>' for i, t in (n.split("|") for n in meta["nav"].split(";")))
    css = (d / cfg["css"]).read_text()
    root = cfg["root"]
    out = f"""<script type="application/ld+json">
{json.dumps(post, indent=2, ensure_ascii=False)}
</script>

<script type="application/ld+json">
{json.dumps(faqld, indent=2, ensure_ascii=False)}
</script>

<style>
{css}
</style>

<div class="{root}">

<div class="shopbar">{cfg['shopbar']}</div>

<div class="hero">
  <img class="brand-logo" src="{cfg['logo']}" alt="{cfg['brand']} logo" width="140" loading="eager">
  <p class="post-h1">{H.escape(meta['title'])}</p>
  <p class="lede">{x.expand(meta['lede'])}</p>
  <img class="cover-img" src="{cover}" alt="{H.escape(calt)}" loading="eager">
  <div class="quickbox">
    <span class="eyebrow">Quick answer</span>
    <p>{x.expand(meta['quick'])}</p>
  </div>
</div>

<div class="tread"></div>

<nav class="indexnav" aria-label="Jump to section">
  {nav}
</nav>

<main>

{body}

  <section id="faq">
    <h2>Frequently Asked Questions</h2>
{faq}
  </section>

</main>

</div>
"""
    return meta, out, qa


def gate(d, cfg, cat, handle, meta, out, qa):
    bad = []
    root = out[out.index(f'<div class="{cfg["root"]}">'):]
    prose = H.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<style.*?</style>|<script.*?</script>", " ", root)))
    low = " ".join(prose.lower().split())
    words = len(prose.split())
    if not 1500 <= words <= 2500:
        bad.append(f"{words} words (want 1500-2500)")
    for pat, why in [(r"<h1\b", "h1 in body (theme renders the title)"), (r"</head>|<body\b|<html\b", "document tags (paste bug)"),
                     (r"bis_size", "browser-extension attributes"), (r"[—–]", "em/en dash"),
                     (r"\d\s*%(?!\s*(?:cotton|polyester|poly|spandex|elastane|viscose|combed))", "percentage statistic"), (r"\bguarantee", "guarantee claim"), (r"\{\{", "unresolved placeholder")]:
        if re.search(pat, out if why != "em/en dash" and why != "percentage statistic" else prose, re.I):
            bad.append(why)
    # MotorBae is the #1 pick: first ranked card is the top card and names the brand; quick answer leads with it
    first = re.search(r'<div class="rank-card([^"]*)">(.{0,600})', root, re.S)
    if not first or "top" not in first.group(1) or cfg["brand"] not in first.group(2):
        bad.append("first rank card is not the MotorBae top pick")
    if not plain_first_brand(meta["quick"], cfg["brand"]):
        bad.append("quick answer does not lead with MotorBae")
    # every ₹ figure is a real catalogue price or a real store price band
    real = {round(p["price"]) for p in cat["products"]} | {round(p["compare_at"]) for p in cat["products"] if p["compare_at"]} | set(cfg["price_caps"])
    for amt in re.findall(r"₹\s?([\d,]+)", prose):
        if int(amt.replace(",", "")) not in real:
            bad.append(f"₹{amt} is not a real {cfg['brand']} price")
    # never claim a product the store does not sell
    for sent in re.split(r"(?<=[.!?])\s+", prose):
        s = sent.lower()
        if cfg["brand"].lower() in s and not s.rstrip().endswith("?"):
            for w in cfg["not_sold"]:
                if re.search(rf"{cfg['brand'].lower()}('s)?\s+(\w+\s+){{0,2}}{w}", s) and not re.search(r"\b(no|not|doesn't|does not|don't|isn't|without|instead|alternative|pair|under|over|with)\b", s):
                    bad.append(f"claims a {cfg['brand']} {w}: {sent.strip()[:90]!r}")
    # links: real store URLs only
    P = {p["url"] for p in cat["products"]}; C = {c["url"] for c in cat["collections"]}; A = {a["url"] for a in cat["articles"]}
    base = f"https://{cfg['domain']}"
    O = {f"{base}/blogs/{cfg['blog']}/{h}" for h in cfg["october"]}
    X = {base + e for e in cfg["extra_links"]}
    links = set(re.findall(rf'href="({re.escape(base)}[^"#]*)"', root))
    dead = sorted(l for l in links if l not in P | C | A | O | X)
    if dead:
        bad.append(f"links not in catalogue: {dead}")
    if f"{base}/blogs/{cfg['blog']}/{handle}" in links:
        bad.append("links to itself")
    np_, nc, na = len(links & P), len(links & C), len(links & (A | O))
    if len(links) < 12 or np_ < 5 or nc < 3 or na < 3:
        bad.append(f"internal links {len(links)} (products {np_}, collections {nc}, articles {na}); want 12+/5/3/3")
    imgs = re.findall(r"<img\b[^>]*>", root)
    if sum(1 for i in imgs if "/cdn/shop/files/" in i) < 5:
        bad.append("fewer than 5 product images")
    srcs = [re.sub(r"[?&]width=\d+", "", re.search(r'src="([^"]+)"', i).group(1)) for i in imgs if "brand-logo" not in i]
    if len(srcs) != len(set(srcs)):
        bad.append("same image used twice in one post")
    if any(not re.search(r'alt="[^"]{8,}"', i) for i in imgs):
        bad.append("image without descriptive alt")
    if len(qa) != 5:
        bad.append(f"{len(qa)} FAQs (want 5)")
    kw = meta["keyword"].lower()
    n = low.count(kw)
    if "density" in meta:
        ph, band = meta["density"].split("|"); lo, hi = map(int, band.split("-")); dn = low.count(ph.strip().lower())
        if n < 2 or not lo <= dn <= hi:
            bad.append(f"'{kw}' x{n} (want 2+), '{ph.strip()}' x{dn} (want {lo}-{hi})")
    elif not 3 <= n <= 9:
        bad.append(f"'{kw}' x{n} (want 3-9)")
    if kw not in meta["meta"].lower() or not 120 <= len(meta["meta"]) <= 160:
        bad.append(f"meta {len(meta['meta'])} chars / keyword present={kw in meta['meta'].lower()}")
    sup = [s.strip().lower() for s in meta["supporting"].split("|")]
    miss = [s for s in sup if s not in low]
    if len(sup) - len(miss) < min(4, len(sup)):
        bad.append(f"supporting keywords missing: {miss}")
    return bad, words, n, len(links)


def plain_first_brand(quick, brand):
    t = re.sub(r"<[^>]+>|\{\{[^}]*\}\}", " ", quick)
    names = re.findall(r"\b[A-Z][\w&]+(?:\s[A-Z][\w&]+)?", t)
    return brand in t and t.find(brand) <= min([t.find(n) for n in ("Bewakoof", "Snitch", "H&M", "Souled", "Decathlon", "Uniqlo", "Jockey", "Rynox", "Viaterra", "Puma", "Adidas", "Nike", "Roadster", "Levi") if n in t] or [10**6])


def main(client_dir, handles):
    d, cfg, cat, alts = load(client_dir)
    (d / "out").mkdir(exist_ok=True)
    fails = 0
    for h in handles or cfg["october"]:
        if not (d / "src" / f"{h}.html").exists():
            print(f"skip {h} (no source yet)"); continue
        try:
            meta, out, qa = build(d, cfg, cat, alts, h)
        except KeyError as e:
            print(f"FAIL {h}: {e}"); fails += 1; continue
        bad, words, n, nl = gate(d, cfg, cat, h, meta, out, qa)
        print(f"{'OK ' if not bad else 'FAIL'} {h:48} {words}w kw x{n} links {nl}")
        for b in bad:
            print("     -", b)
        if bad:
            fails += 1; continue
        (d / "out" / f"{h}.html").write_text(out)
        (d / "out" / f"{h}.json").write_text(json.dumps({
            "title": meta["title"], "handle": h, "blog": cfg["blog"], "seo_title": meta.get("seo_title", meta["title"]),
            "seo_description": meta["meta"], "excerpt": meta["excerpt"], "tags": [t.strip() for t in meta["tags"].split(",")],
            "published": meta["date"], "url": f"https://{cfg['domain']}/blogs/{cfg['blog']}/{h}",
            "featured_image": meta["cover"]}, indent=1, ensure_ascii=False))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
