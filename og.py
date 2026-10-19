"""Genera out/og-v3.jpg (1200x1200, ikona SMB) - miniatura para WhatsApp / redes (logo + sistemas exteriores)."""
import asyncio, glob, os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT = Path(__file__).resolve().parent
(ROOT / "out").mkdir(exist_ok=True)
HTML = f"""<!doctype html><meta charset=utf-8><style>
*{{margin:0}}body{{width:1200px;height:1200px;background:#fff;display:grid;place-items:center}}
img{{width:820px;height:820px;display:block}}
</style><body><img src="file://{ROOT}/assets/SMBMX_Icon_v3_Powder.svg"></body>"""
async def main():
    async with async_playwright() as p:
        g = glob.glob("/opt/pw-browsers/chromium*/chrome-linux/chrome") + glob.glob("/opt/pw-browsers/chromium")
        b = await p.chromium.launch(executable_path=g[0]) if g else await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 1200})
        (ROOT / "out" / "og.html").write_text(HTML, encoding="utf-8")
        await pg.goto(f"file://{ROOT}/out/og.html"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
        await pg.screenshot(path=str(ROOT / "out" / "og-v3.png"))
        await b.close()
    from PIL import Image
    Image.open(ROOT / "out" / "og-v3.png").convert("RGB").save(ROOT / "out" / "og-v3.jpg", quality=88)
asyncio.run(main())
