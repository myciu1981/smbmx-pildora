"""Genera out/og-v2.jpg (1200x630) - miniatura para WhatsApp / redes (logo + sistemas exteriores)."""
import asyncio, glob, os
from pathlib import Path
from playwright.async_api import async_playwright
ROOT = Path(__file__).resolve().parent
(ROOT / "out").mkdir(exist_ok=True)
HTML = f"""<!doctype html><meta charset=utf-8><style>
@font-face{{font-family:E;font-weight:400;src:url(file://{ROOT}/assets/EncodeSans-Regular.ttf)}}
@font-face{{font-family:E;font-weight:500;src:url(file://{ROOT}/assets/EncodeSans-Medium.ttf)}}
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:#fff;font-family:E,Arial,sans-serif;color:#21242C;display:flex;flex-direction:column;justify-content:center;padding:0 96px}}
img{{width:520px;display:block}}
h1{{font-weight:500;color:#1A355C;font-size:70px;line-height:1.05;margin-top:54px;letter-spacing:-.01em}}
p{{font-size:34px;line-height:1.3;margin-top:20px}}
</style><body><img src="file://{ROOT}/assets/SMBMX_Logo_v3_Primary.svg">
<h1>Sistemas exteriores<br>para ventanas</h1><p>Protección solar, seguridad y confort desde el exterior.</p></body>"""
async def main():
    async with async_playwright() as p:
        g = glob.glob("/opt/pw-browsers/chromium*/chrome-linux/chrome") + glob.glob("/opt/pw-browsers/chromium")
        b = await p.chromium.launch(executable_path=g[0]) if g else await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        (ROOT / "out" / "og.html").write_text(HTML, encoding="utf-8")
        await pg.goto(f"file://{ROOT}/out/og.html"); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
        await pg.screenshot(path=str(ROOT / "out" / "og-v2.png"))
        await b.close()
    from PIL import Image
    Image.open(ROOT / "out" / "og-v2.png").convert("RGB").save(ROOT / "out" / "og-v2.jpg", quality=88)
asyncio.run(main())
