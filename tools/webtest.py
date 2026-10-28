import asyncio, glob
from playwright.async_api import async_playwright
U="file://"+__import__("os").path.abspath("site/p/capsula/index.html")+""
async def main():
    async with async_playwright() as p:
        g=glob.glob("/opt/pw-browsers/chromium*/chrome-linux/chrome")+glob.glob("/opt/pw-browsers/chromium")
        b=await p.chromium.launch(executable_path=g[0]) if g else await p.chromium.launch()
        for name,(w,h) in {"m":(390,844),"d":(1440,900)}.items():
            pg=await b.new_page(viewport={"width":w,"height":h},device_scale_factor=2 if name=="m" else 1)
            errs=[]; pg.on("console",lambda m: errs.append(m.text) if m.type=="error" else None)
            pg.on("requestfailed",lambda r: errs.append("FAIL "+r.url))
            await pg.goto(U); await pg.wait_for_timeout(700)
            n=await pg.evaluate("document.querySelectorAll('.slide:not([style*=none])').length")
            vis=await pg.evaluate("[...document.querySelectorAll('.slide')].filter(e=>e.offsetHeight>0).length")
            print(name,"visible slides",vis,errs)
            for i in range(vis):
                await pg.evaluate(f"window.scrollTo({{top:{i*h},behavior:'instant'}})"); await pg.wait_for_timeout(350)
                await pg.screenshot(path=f"out/web_{name}_{i+1}.png")
            links=await pg.evaluate("[...document.querySelectorAll('.slide')].filter(e=>e.offsetHeight>0).flatMap(s=>[...s.querySelectorAll('a')].map(a=>a.href))")
            print(sorted(set(links)))
            await pg.close()
        await b.close()
asyncio.run(main())
