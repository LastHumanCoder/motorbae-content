#!/usr/bin/env python3
"""Render each built article inside MotorBae's real theme (a live published post as host) at
390px and 1280px: sideways scroll, clipped elements, broken images, H1 count, smallest text."""
import json, pathlib, sys
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent
HOST = "https://motorbae.store/blogs/the-garage/best-streetwear-brands-for-car-enthusiasts-india"
cfg = json.loads((ROOT / "client.json").read_text())
JS = """async (html) => {
  const old = document.querySelector('.mb-post');
  const host = old.parentElement; host.innerHTML = html;
  const root = host.querySelector('.mb-post');
  for (const im of root.querySelectorAll('img')) im.loading = 'eager';
  for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); }
  await Promise.all([...root.querySelectorAll('img')].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 12000); })));
  const vw = document.documentElement.clientWidth;
  const scr = [...root.querySelectorAll('*')].filter(e => ['auto','scroll'].includes(getComputedStyle(e).overflowX));
  const clipped = [...root.querySelectorAll('p,li,td,th,h2,h3,img,a,summary,figcaption')].filter(e => {
    const b = e.getBoundingClientRect(); return b.width && b.right > vw + 1 && !scr.some(s => s !== e && s.contains(e)); }).length;
  const small = Math.min(...[...root.querySelectorAll('p,li,td,a,span,summary')].filter(e => e.innerText && e.innerText.trim()).map(e => parseFloat(getComputedStyle(e).fontSize)));
  return {vw, doc: document.documentElement.scrollWidth, clipped, broken: [...root.querySelectorAll('img')].filter(i => !i.naturalWidth).length,
          imgs: root.querySelectorAll('img').length, h1: document.querySelectorAll('h1').length, small};
}"""
with sync_playwright() as p:
    b = p.chromium.launch()
    bad = 0
    for vw in (390, 1280):
        pg = b.new_page(viewport={"width": vw, "height": 900}, is_mobile=vw < 500)
        for h in cfg["october"]:
            pg.goto(HOST, wait_until="domcontentloaded", timeout=60000); pg.wait_for_selector(".mb-post", timeout=60000)
            m = pg.evaluate(JS, (ROOT / "out" / f"{h}.html").read_text())
            ok = m["doc"] <= m["vw"] and not m["clipped"] and not m["broken"] and m["h1"] == 1 and m["small"] >= 11
            bad += not ok
            print(f"{'ok ' if ok else 'BAD'} {vw} {h:46} {m}")
            if h == "best-hoodies-for-men-india-2026":
                pg.evaluate("document.querySelector('.pgrid').scrollIntoView({block:'start'})"); pg.wait_for_timeout(600)
                pg.screenshot(path=str(ROOT / "data" / f"_theme_{vw}.png"))
        pg.close()
    b.close()
    sys.exit(1 if bad else 0)
