import asyncio, sys, glob, os
from playwright.async_api import async_playwright

LANG = sys.argv[1] if len(sys.argv) > 1 else "es"
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = f"{ROOT}/out"
os.makedirs(OUT, exist_ok=True)

async def main():
    async with async_playwright() as p:
        exe = None
        for c in ("/opt/pw-browsers/chromium", "/opt/pw-browsers/chromium-*/chrome-linux/chrome"):
            g = glob.glob(c)
            if g:
                exe = g[0]; break
        b = await p.chromium.launch(executable_path=exe) if exe else await p.chromium.launch()
        for mode, (w, h) in (("phone", (1080, 1920)), ("desk", (1920, 1080))):
            pg = await b.new_page(viewport={"width": w, "height": h})
            await pg.goto(f"file://{ROOT}/capsula_{LANG}_{mode}.html")
            await pg.evaluate("document.fonts.ready")
            await pg.wait_for_timeout(500)
            # overflow check
            res = await pg.evaluate("""() => [...document.querySelectorAll('.page')].map(s => {
                const sb = s.getBoundingClientRect(); let worst = s.scrollHeight, who = 'scroll';
                s.querySelectorAll('*').forEach(e => { const r = e.getBoundingClientRect();
                  if (r.height>0 && r.bottom - sb.top > worst) { worst = r.bottom - sb.top; who = e.className || e.tagName; } });
                const it=s.querySelector('.items');const tight=it?[...it.querySelectorAll('.item')].map(e=>Math.round(e.clientHeight-e.firstElementChild.getBoundingClientRect().height-0)):[];return [s.id, Math.round(worst), Math.round(sb.height), s.scrollHeight>sb.height+1?'OVERFLOW':'ok', tight.join('/')] })""")
            print(mode, res)
            secs = await pg.query_selector_all(".page")
            for i, s in enumerate(secs, 1):
                await s.screenshot(path=f"{OUT}/{LANG}_{mode}_{i}.png")
            await pg.pdf(path=f"{OUT}/SMBMX_capsula_{LANG}_{mode}.pdf", width=f"{w}px", height=f"{h}px",
                         print_background=True, prefer_css_page_size=True)
            await pg.close()
        await b.close()

asyncio.run(main())
