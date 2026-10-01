#!/usr/bin/env python3
"""Featured images for the October posts in MotorBae's own black cover style (as on the August posts):
outline wordmark, eyebrow, purple condensed headline, white sub, outlined chip, footer line. 1200x627."""
import json, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
LOGO = "https://motorbae.store/cdn/shop/files/logomark_noise_gradient.png?v=1770576518&width=1920"
C = {
 "best-hoodies-for-men-india-2026": ("THE WINTER GUIDE", ["BEST HOODIES", "FOR MEN IN INDIA"], "2026 EDITION", "RANKED & COMPARED", "GSM · FIT · ZIP OR PULLOVER"),
 "best-diwali-gifts-for-car-lovers-india-2026": ("THE GIFT GUIDE", ["BEST DIWALI GIFTS", "FOR CAR LOVERS"], "INDIA 2026", "BY BUDGET FROM ₹299", "FOR HIM · FOR HER · FOR BIKERS"),
 "best-full-sleeve-t-shirts-for-men-india-2026": ("THE STYLE GUIDE", ["BEST FULL SLEEVE", "T-SHIRTS FOR MEN"], "INDIA 2026", "TYPES, FABRIC & LAYERING", "CREW · HENLEY · THERMAL · POLO"),
 "best-cargo-pants-for-men-india-2026": ("THE STYLE GUIDE", ["BEST CARGO PANTS", "FOR MEN IN INDIA"], "COMPLETE STYLE GUIDE", "5 OUTFIT FORMULAS", "FIT · FABRIC · WHAT TO WEAR ON TOP"),
 "best-jacket-for-men-india-2026": ("THE RIDERS GUIDE", ["BEST JACKET", "FOR MEN IN INDIA"], "RIDING · CASUAL · STREETWEAR", "THE LAYERING SYSTEM", "ARMOUR · WARMTH · BY CITY"),
 "best-sweater-for-men-india-2026": ("THE WINTER GUIDE", ["BEST SWEATER", "FOR MEN IN INDIA"], "2026 EDITION", "KNIT VS HOODIE", "MERINO · WOOL · COTTON · CARE"),
 "best-gifts-for-him-india-2026": ("THE GIFT GUIDE", ["BEST GIFTS", "FOR HIM IN INDIA"], "CAR & BIKE LOVER EDITION", "PICKED BY PERSONALITY", "JDM · F1 · MUSCLE · BIKERS"),
 "automotive-t-shirts-india-2026": ("THE BRAND GUIDE", ["AUTOMOTIVE", "T-SHIRTS INDIA"], "BEST BRANDS & WHERE TO BUY", "2026 EDITION", "GSM · PRINT · LICENSED VS FAN ART"),
 "best-track-pants-for-men-india-2026": ("THE COMFORT GUIDE", ["BEST TRACK PANTS", "FOR MEN IN INDIA"], "2026 EDITION", "SWEATPANTS TO TRACKSUITS", "FABRIC · FIT · HOW TO STYLE"),
 "best-winter-outfits-for-men-india-2026": ("THE STYLE GUIDE", ["BEST WINTER OUTFITS", "FOR MEN IN INDIA"], "COMPLETE STYLE GUIDE", "THE 7-PIECE CAPSULE", "BY OCCASION · BY CITY · LAYERING"),
}
HTML = """<html><head><link href="https://fonts.googleapis.com/css2?family=Oswald:wght@600;700&family=IBM+Plex+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>*{{margin:0;box-sizing:border-box}}body{{width:1200px;height:627px;background:#08080a;color:#fff;font-family:'Oswald',sans-serif;overflow:hidden;position:relative}}
.w{{position:absolute;inset:0;padding:40px 64px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start}}
.logo{{height:84px;display:block;margin-bottom:22px}}
.eb{{font-family:'IBM Plex Mono',monospace;font-weight:600;letter-spacing:.14em;font-size:24px;display:flex;align-items:center;gap:18px;margin-bottom:14px}}
.eb i{{font-style:normal;color:#9b6cf0;letter-spacing:-.05em}}
h1{{font-weight:700;text-transform:uppercase;line-height:.95;font-size:{size}px;letter-spacing:.005em;
 background:linear-gradient(180deg,#b795ea,#8a5bd6 60%,#7a4fc0);-webkit-background-clip:text;color:transparent;margin-bottom:14px}}
.sub{{font-size:34px;font-weight:600;letter-spacing:.04em;margin-bottom:22px}}
.chip{{display:inline-block;border:2px solid #9b6cf0;padding:8px 22px;font-size:30px;font-weight:600;letter-spacing:.06em;transform:skewX(-12deg);margin-bottom:22px}}
.chip span{{display:inline-block;transform:skewX(12deg)}}
.ft{{font-family:'IBM Plex Mono',monospace;font-size:20px;letter-spacing:.12em;display:flex;gap:14px}}
.ft i{{font-style:normal;color:#9b6cf0}}
.tread{{position:absolute;right:0;top:0;bottom:0;width:260px;opacity:.10;background:repeating-linear-gradient(100deg,#b795ea 0 4px,transparent 4px 30px)}}
</style></head><body><div class="tread"></div><div class="w"><img class="logo" src="{logo}">
<div class="eb">{eb} <i>///</i></div><h1>{h1}</h1><div class="sub">{sub}</div><div class="chip"><span>{chip}</span></div>
<div class="ft"><i>///</i> {ft}</div></div></body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 627}, device_scale_factor=2)
    for h, (eb, lines, sub, chip, ft) in C.items():
        size = 124 if max(len(l) for l in lines) <= 16 else 106
        pg.set_content(HTML.format(logo=LOGO, eb=eb, h1="<br>".join(lines), sub=sub, chip=chip, ft=ft, size=size))
        pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(400)
        over = pg.evaluate("document.querySelector('.w').scrollHeight > 627 || document.querySelector('h1').scrollWidth > 1100")
        pg.screenshot(path=str(ROOT / "covers" / f"{h}.png"))
        print(("OVERFLOW " if over else "ok ") + h)
    b.close()
