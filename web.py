import re, shutil, sys, os
from pathlib import Path
sys.argv = ["build.py", "es"]
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import build as B

SLUG = "pildora"
OUT = ROOT / "site" / "p" / SLUG
if OUT.parent.exists(): shutil.rmtree(OUT.parent)
OUT.mkdir(parents=True)
for d in ("assets", "photos"):
    shutil.copytree(ROOT / d, OUT / d)
# remove unused endorsement-on-light asset
(OUT / "assets/GRUPO-VOES_Endorsement_ES_OnLight.svg").unlink(missing_ok=True)

def scope(css, pre):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out = []
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        sel = sel.strip()
        if sel.startswith("@"): continue
        out.append(",".join(f"{pre} {s.strip()}" for s in sel.split(",")) + "{" + body + "}")
    return "\n".join(out)

def sections(mode):
    h = B.cover_page(mode) + "".join(B.product_page(p, mode) for p in B.C["pages"]) + B.closing_page(mode)
    h = re.sub(r' id="p\d"', "", h)
    parts = re.findall(r"<section class=\"(page[^\"]*)\">(.*?)</section>", h, flags=re.S)
    return parts

def slides(mode, cls):
    out = []
    for i, (c, inner) in enumerate(sections(mode)):
        dark = " dark" if "close" in c else (" cv" if "cover" in c else "")
        out.append(f'<section class="slide {cls}{dark}" data-i="{i}"><div class="stage {c}">{inner}</div></section>')
    return "".join(out)

EXTRA = """
html{scroll-snap-type:y mandatory;overflow-y:scroll;background:#fff;-webkit-text-size-adjust:100%}
body{margin:0}
.slide{height:100vh;height:100dvh;width:100%;scroll-snap-align:start;scroll-snap-stop:always;position:relative;overflow:hidden;background:#fff}
.slide.dark{background:#1A355C}
.slide.cv{background:linear-gradient(#1A355C 40%,#fff 40%)}
.slide .stage{position:absolute;left:50%;top:50%;margin:0;transform-origin:0 0;flex:none}
.dk{display:none}
@media (min-aspect-ratio:1/1){.ph{display:none}.dk{display:block}}
.contact{position:relative}
.contact a::after,.foot a::after{content:"";position:absolute;inset:-8px 0}
.ph .foot{position:relative}
.dots{position:fixed;right:max(6px,env(safe-area-inset-right));top:50%;transform:translateY(-50%);display:flex;flex-direction:column;gap:2px;z-index:5}
.dots button{width:22px;height:22px;border:0;background:none;padding:0;display:grid;place-items:center;cursor:pointer}
.dots i{width:6px;height:6px;border-radius:50%;background:#1A355C;opacity:.28;transition:all .2s}
.dots button.on i{opacity:1;height:16px;border-radius:3px}
body.dark .dots i{background:#fff}
@media (max-aspect-ratio:99/100){.dots{display:none}}
@media (min-aspect-ratio:1/1){.hint{display:none!important}}
.hint{position:fixed;right:max(14px,env(safe-area-inset-right));bottom:max(16px,env(safe-area-inset-bottom));z-index:6;display:flex;align-items:center;gap:10px;border:0;background:none;padding:0;cursor:pointer;font:500 15px "Encode Sans",Arial,sans-serif;color:#1A355C;-webkit-tap-highlight-color:transparent}
.hint .lbl{background:#fff;padding:8px 12px;border-radius:20px;box-shadow:0 2px 10px rgba(26,53,92,.18);transition:opacity .4s}
.hint.seen .lbl{opacity:0;pointer-events:none;width:0;padding:0;overflow:hidden}
.hint .arr{width:48px;height:48px;border-radius:50%;background:#1A355C;display:grid;place-items:center;box-shadow:0 3px 12px rgba(26,53,92,.3);animation:bob 1.6s ease-in-out infinite}
.hint .arr svg{width:24px;height:24px;stroke:#fff;fill:none;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;transition:transform .3s}
body.last .hint .arr svg{transform:rotate(180deg)}
body.dark .hint .arr{background:#fff}body.dark .hint .arr svg{stroke:#1A355C}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(6px)}}
@media (prefers-reduced-motion:reduce){.hint .arr{animation:none}}
@keyframes lift{0%{transform:translateY(calc(var(--i)*var(--sh))) scaleY(1)}}
@keyframes fadein{from{opacity:0}}
@media (prefers-reduced-motion:no-preference){
html{scroll-behavior:smooth}
.slide .slats i{animation:lift 2s cubic-bezier(.7,0,.25,1) both;animation-delay:calc((23 - var(--i))*.03s + .45s)}
.slide .czone,.slide .cbottom,.slide .clogo{animation:fadein 1s ease both;animation-delay:1.6s}
}
"""

JS = """
(function(){
var W={ph:[1080,1920],dk:[1920,1080]};
function mode(){return innerWidth>=innerHeight?'dk':'ph'}
function fit(){
  var m=mode(),w=W[m][0],h=W[m][1],H=document.documentElement.clientHeight||innerHeight,Wd=document.documentElement.clientWidth||innerWidth;
  var s=Math.min(Wd/w,H/h);
  document.querySelectorAll('.slide.'+m+' .stage').forEach(function(e){
    e.style.transform='translate('+(-w*s/2)+'px,'+(-h*s/2)+'px) scale('+s+')';
  });
  build();
}
var dots=document.getElementById('dots'),hint=document.getElementById('hint'),io,cur=0;
hint.onclick=function(){var sl=[].slice.call(document.querySelectorAll('.slide.'+mode()));var t=cur>=sl.length-1?0:cur+1;sl[t].scrollIntoView({behavior:'smooth'});};
function build(){
  var m=mode(),sl=[].slice.call(document.querySelectorAll('.slide.'+m));
  dots.innerHTML='';
  sl.forEach(function(el,i){
    var b=document.createElement('button');b.setAttribute('aria-label','Página '+(i+1));b.innerHTML='<i></i>';
    b.onclick=function(){el.scrollIntoView({behavior:'smooth'})};dots.appendChild(b);
  });
  if(io)io.disconnect();
  io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){var i=sl.indexOf(e.target);
      [].forEach.call(dots.children,function(d,j){d.classList.toggle('on',i===j)});
      document.body.classList.toggle('dark',e.target.classList.contains('dark'));
      document.body.classList.toggle('last',i===sl.length-1);
      if(i>0)hint.classList.add('seen');cur=i;}
  })},{threshold:.55});
  sl.forEach(function(el){io.observe(el)});
}
addEventListener('resize',fit);addEventListener('orientationchange',fit);
(document.fonts&&document.fonts.ready||Promise.resolve()).then(fit);fit();
})();
"""

css = B.BASE_CSS + scope(B.PHONE_CSS, ".ph") + "\n" + scope(B.DESK_CSS, ".dk") + EXTRA
# override position for stage after mode css (stage carries .page)
css += ".slide .stage{position:absolute;left:50%;top:50%;overflow:hidden}"
# set stage fixed size explicitly per mode so transform math is exact
css += ".ph .stage{width:1080px;height:1920px}.dk .stage{width:1920px;height:1080px}"

desc = "Protección solar, seguridad y confort desde el exterior."
html = f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow,noarchive,noimageindex">
<meta name="theme-color" content="#1A355C">
<title>Simple Made Blinds Mexico · Sistemas exteriores para ventanas</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website"><meta property="og:locale" content="es_MX">
<meta property="og:title" content="Simple Made Blinds Mexico · Sistemas exteriores para ventanas">
<meta property="og:url" content="https://simplemadeblinds.mx/p/pildora/"><meta property="og:site_name" content="Simple Made Blinds Mexico">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://simplemadeblinds.mx/p/pildora/og-v3.jpg"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="1200"><meta property="og:image:alt" content="Simple Made Blinds Mexico">
<meta name="twitter:card" content="summary_large_image">
<style>{css}</style></head><body>
{slides("phone","ph")}{slides("desk","dk")}
<nav class="dots" id="dots" aria-label="Páginas"></nav>
<button class="hint" id="hint" aria-label="Siguiente página"><span class="lbl">Deslice hacia arriba</span><span class="arr"><svg viewBox="0 0 24 24"><path d="M5 9l7 7 7-7"/></svg></span></button>
<script>{JS}</script></body></html>'''
(OUT / "index.html").write_text(html, encoding="utf-8")

(OUT / ".htaccess").write_text('''Options -Indexes
<IfModule mod_headers.c>
  Header set X-Robots-Tag "noindex, nofollow, noarchive"
  Header set Referrer-Policy "no-referrer-when-downgrade"
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpeg "access plus 7 days"
  ExpiresByType font/ttf "access plus 30 days"
  ExpiresByType image/svg+xml "access plus 30 days"
</IfModule>
AddType font/ttf .ttf
''')
(OUT / "robots.txt").write_text("User-agent: *\nDisallow: /\n")

from PIL import Image
shutil.copy(ROOT / "out" / "og-v3.jpg", OUT / "og-v3.jpg")
print("ok", OUT, sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())//1024, "KB")
