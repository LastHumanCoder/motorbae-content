#!/usr/bin/env python3
"""Featured images for the October posts in MotorBae's current blog cover style (the light grey
engine-parts pattern used on the September posts), with the exact MOTORBAE wordmark the client
supplied (data/logo_wordmark.webp). 1734x907, the size of their recent covers.

Background (data/cover_bg.png) is built from a text-free strip of their own cover pattern."""
import base64, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
b64 = lambda f: base64.b64encode((ROOT / "data" / f).read_bytes()).decode()
LOGO, BG = b64("logo_wordmark.webp"), b64("cover_bg.png")
C = {  # eyebrow, headline lines, chip, footer
 "best-hoodies-for-men-india-2026": ("THE WINTER GUIDE", ["BEST HOODIES FOR", "MEN INDIA 2026"], "GSM · FIT · ZIP OR PULLOVER", "RANKED & COMPARED"),
 "best-diwali-gifts-for-car-lovers-india-2026": ("THE GIFT GUIDE", ["BEST DIWALI GIFTS", "FOR CAR LOVERS 2026"], "BY BUDGET · FOR HIM · FOR HER", "REAL PRICES FROM ₹299"),
 "best-full-sleeve-t-shirts-for-men-india-2026": ("THE STYLE GUIDE", ["BEST FULL SLEEVE", "T-SHIRTS INDIA 2026"], "CREW · HENLEY · THERMAL · POLO", "TYPES, FABRIC & LAYERING"),
 "best-cargo-pants-for-men-india-2026": ("THE STYLE GUIDE", ["BEST CARGO PANTS", "FOR MEN INDIA 2026"], "FIT · FABRIC · 5 OUTFITS", "THE COMPLETE STYLE GUIDE"),
 "best-jacket-for-men-india-2026": ("THE RIDERS GUIDE", ["BEST JACKET FOR", "MEN INDIA 2026"], "RIDING · CASUAL · STREETWEAR", "THE LAYERING SYSTEM"),
 "best-sweater-for-men-india-2026": ("THE WINTER GUIDE", ["BEST SWEATER FOR", "MEN INDIA 2026"], "MERINO · WOOL · KNIT VS HOODIE", "FABRIC, FIT & CARE"),
 "best-gifts-for-him-india-2026": ("THE GIFT GUIDE", ["BEST GIFTS FOR HIM", "INDIA 2026"], "JDM · F1 · MUSCLE · BIKERS", "CAR & BIKE LOVER EDITION"),
 "automotive-t-shirts-india-2026": ("THE BRAND GUIDE", ["AUTOMOTIVE T-SHIRTS", "INDIA 2026"], "BEST BRANDS & WHERE TO BUY", "GSM · PRINT · LICENSED VS FAN ART"),
 "best-track-pants-for-men-india-2026": ("THE COMFORT GUIDE", ["BEST TRACK PANTS", "FOR MEN INDIA 2026"], "SWEATPANTS · JOGGERS · TRACKSUITS", "FABRIC, FIT & STYLING"),
 "best-winter-outfits-for-men-india-2026": ("THE STYLE GUIDE", ["BEST WINTER OUTFITS", "FOR MEN INDIA 2026"], "THE 7-PIECE WINTER CAPSULE", "BY OCCASION · BY CITY · LAYERING"),
}
HTML = """<html><head><link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,100..125,500..900;1,100..125,700..900&display=block" rel="stylesheet">
<style>*{{margin:0;box-sizing:border-box}}
body{{width:1734px;height:907px;overflow:hidden;background:#c9c9c9 url(data:image/png;base64,{bg}) 0 0/1734px 907px;font-family:'Archivo',sans-serif;color:#0a0a0a}}
.w{{position:absolute;inset:0;padding:70px 100px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start}}
.logo{{width:960px;height:auto;display:block;margin-bottom:26px}}
.eb{{font-style:normal;font-weight:900;font-stretch:108%;transform:skewX(-9deg);transform-origin:left bottom;font-size:42px;letter-spacing:.02em;display:flex;gap:16px;margin-bottom:6px}}
.sl{{color:#0a0a0a;font-weight:900;letter-spacing:-.04em;display:inline-block;transform:skewX(-9deg)}}
h1{{font-style:normal;font-weight:900;font-stretch:102%;text-transform:uppercase;color:#7444b4;line-height:.95;letter-spacing:.01em;font-size:{size}px;white-space:nowrap;margin-bottom:28px}}
.chip{{position:relative;display:inline-block;padding:12px 54px 12px 28px;margin-bottom:26px}}.chip svg{{position:absolute;inset:0;width:100%;height:100%;overflow:visible}}
.chip span{{font-weight:600;font-stretch:110%;font-size:44px;letter-spacing:.12em}}
.ft{{font-weight:700;font-stretch:110%;font-size:33px;letter-spacing:.1em;display:flex;gap:16px}}
.l{{display:block;transform:skewX(-9deg);transform-origin:left bottom}}</style></head><body><div class="w"><img class="logo" src="data:image/webp;base64,{logo}">
<div class="eb">{eb} <span class="sl">///</span></div><h1>{h1}</h1><div class="chip"><svg></svg><span>{chip}</span></div>
<div class="ft"><span class="sl">///</span> {ft}</div></div></body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1734, "height": 907})
    for h, (eb, lines, chip, ft) in C.items():
        size = 160
        while True:  # largest headline that fits the left 76% of the card
            pg.set_content(HTML.format(bg=BG, logo=LOGO, eb=eb, h1="".join(f'<span class="l">{l}</span>' for l in lines), chip=chip, ft=ft, size=size))
            pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready.then(() => 1)")
            fits = pg.evaluate("document.querySelector('h1').scrollWidth <= 1500 && document.querySelector('.w').scrollHeight <= 907")
            if fits or size <= 96:
                break
            size -= 6
        pg.evaluate("""() => { const c = document.querySelector('.chip'), w = c.offsetWidth, h = c.offsetHeight, s = c.querySelector('svg');
            s.setAttribute('viewBox', `0 0 ${w} ${h}`);
            s.innerHTML = `<polygon points="2,2 ${w-2},2 ${w-30},${h-2} 2,${h-2}" fill="none" stroke="#7444b4" stroke-width="4" stroke-linejoin="miter"/>`; }""")
        pg.wait_for_timeout(300)
        pg.screenshot(path=str(ROOT / "covers" / f"{h}.png"))
        print(f"{'ok ' if fits else 'TIGHT'} {size}px {h}")
    b.close()
