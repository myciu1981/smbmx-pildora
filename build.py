#!/usr/bin/env python3
# Pildora de productos SMB MX - ES - telefono (1080x2400) y escritorio (1920x1080)
import json, sys, asyncio, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANG = sys.argv[1] if len(sys.argv) > 1 else "es"

# ---------- ICONS (viewBox 48, linea 2.6, sin relleno) ----------
def sun(cx, cy, r, rays=True):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'
    if rays:
        s += (f'<path d="M{cx} {cy-r-3}v-3M{cx-r-3} {cy}h-3M{cx+r+3} {cy}h3'
              f'M{cx-r*0.75-2.5} {cy-r*0.75-2.5}l-2-2M{cx+r*0.75+2.5} {cy-r*0.75-2.5}l2-2"/>')
    return s

ICONS = {
    "calor": sun(24, 15, 6) + '<path d="M8 30h32M8 36h32M8 42h32"/>',
    "oscuridad": '<path d="M30 6A18 18 0 1 0 42 30 14 14 0 0 1 30 6z"/>',
    "ruido": '<path d="M7 19h7l10-8v26l-10-8H7z"/><path d="M31 18a8 8 0 0 1 0 12M36 13a15 15 0 0 1 0 22"/>',
    "seguridad": '<path d="M24 5l15 5v11c0 10-6.5 17-15 21C15.5 38 9 31 9 21V10z"/><path d="M17 23l5 5 9-10"/>',
    "control": '<path d="M16 39V10M9 17l7-7 7 7"/><path d="M32 9v29M25 31l7 7 7-7"/>',
    "fachada": '<rect x="9" y="6" width="30" height="36"/><path d="M15 12h6v6h-6zM27 12h6v6h-6zM15 23h6v6h-6zM27 23h6v6h-6zM21 42v-7h6v7"/>',
    "lamas": '<rect x="7" y="6" width="34" height="36"/><path d="M12 17l24-5M12 26l24-5M12 35l24-5"/>',
    "vista": '<path d="M4 24c5-9 12-14 20-14s15 5 20 14c-5 9-12 14-20 14S9 33 4 24z"/><circle cx="24" cy="24" r="6"/>',
    "malla": sun(24, 13, 5.5) + '<rect x="8" y="25" width="32" height="17"/><path d="M16 25v17M24 25v17M32 25v17M8 33.5h32"/>',
    "ancho": '<path d="M6 24h36M14 16l-8 8 8 8M34 16l8 8-8 8"/>',
    "aire": '<path d="M5 17h24a6 6 0 1 0-6-6M5 25h32a6 6 0 1 1-6 6M5 33h16"/>',
    "plisado": '<path d="M6 8h36M6 40h36M8 12l8 24 8-24 8 24 8-24"/>',
    "gota": '<path d="M24 6c8 10 13 16 13 23a13 13 0 0 1-26 0c0-7 5-13 13-23z"/><path d="M17 30a7 7 0 0 0 6 6"/>',
    "switch": '<rect x="5" y="15" width="38" height="18" rx="9"/><circle cx="34" cy="24" r="5.5"/>',
    "tel": '<rect x="14" y="5" width="20" height="38" rx="4"/><path d="M21 37h6"/>',
    "mail": '<rect x="5" y="11" width="38" height="26" rx="3"/><path d="M6 13l18 14 18-14"/>',
    "web": '<circle cx="24" cy="24" r="18"/><ellipse cx="24" cy="24" rx="7.5" ry="18"/><path d="M6 24h36M9 15h30M9 33h30"/>',
    "pin": '<path d="M24 43S10 29 10 19a14 14 0 0 1 28 0c0 10-14 24-14 24z"/><circle cx="24" cy="19" r="5"/>',
}

def icon(name, cls="ic"):
    return (f'<svg class="{cls}" viewBox="0 0 48 48" fill="none" stroke="currentColor" '
            f'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')

# ---------- CONTENT ----------
CONTENT = {
 "es": {
  "footer_prod": 'Fabricado en Europa · <a href="https://simplemadeblinds.mx/">simplemadeblinds.mx</a>',
  "pages": [
   {"key":"p1","label":"Calor y oscuridad","name":"Persianas europeas de seguridad",
    "tag":"Detiene el calor antes de que llegue al vidrio.",
    "desc":"Persianas de aluminio que se instalan por fuera de la ventana. Al bajar, protegen el interior del sol y permiten oscurecer la habitación.",
    "items":[("calor","Menos calor","protección solar desde el exterior."),
             ("oscuridad","Más oscuridad","habitaciones totalmente oscuras cuando se necesita."),
             ("ruido","Menos ruido","puede reducir el ruido de la calle.")],
    "small":"", "photos":["p1","p4"]},
   {"key":"p2","label":"Seguridad","name":"Persianas europeas de seguridad",
    "tag":"Más seguridad. Sin rejas.",
    "desc":"Las mismas persianas de aluminio, en versiones con perfiles y guías reforzados para proyectos que requieren mayor seguridad.",
    "items":[("seguridad","Antirrobo","versiones antirrobo certificadas RC2 y RC3."),
             ("control","Control","manual o con motor eléctrico o solar."),
             ("fachada","Diseño","cajón compacto y colores a elegir.")],
    "small":"Certificación RC2 y RC3 (EN 1627) según la versión y la configuración.", "photos":["p2","p3"]},
   {"key":"p3","label":"","name":"Persianas venecianas exteriores",
    "tag":"Luz y sombra bajo control.",
    "desc":"Lamas de aluminio orientables que se instalan por fuera de la ventana. Regulan la entrada de luz natural y limitan la radiación solar.",
    "items":[("lamas","Luz regulable","se ajusta la inclinación de las lamas."),
             ("vista","Sin deslumbramiento","luz natural, sin reflejos molestos."),
             ("fachada","Diseño","aspecto contemporáneo, integrado a la fachada.")],
    "small":"", "photos":["v1","v2"]},
   {"key":"p4","label":"","name":"Cortinas enrollables exteriores",
    "tag":"Menos sol, la misma vista.",
    "desc":"Cortinas de tejido técnico que se instalan por fuera de la ventana. Filtran el sol antes de que llegue al vidrio y conservan la vista hacia afuera.",
    "items":[("malla","Menos calor y brillo","filtran la radiación solar."),
             ("vista","Vista y privacidad","vista hacia el exterior, con privacidad de día."),
             ("ancho","Grandes ventanales","hasta 6 m de ancho.")],
    "small":"Vista, privacidad y medidas máximas según el tejido y el sistema.", "photos":["s2","s1"]},
   {"key":"p5","label":"","name":"Mosquiteros",
    "tag":"Aire fresco, sin insectos.",
    "desc":"Mosquiteros discretos para ventanas y puertas. Dejan pasar el aire y detienen mosquitos y otros insectos.",
    "items":[("aire","Ventilación","aire fresco con tranquilidad."),
             ("ancho","Grandes accesos","plisados hasta 4 m (sencillo) o 6 m (doble)."),
             ("plisado","Discreto","se recoge cuando no se usa.")],
    "small":"Medidas según el modelo.", "photos":["m2","m1"]},
   {"key":"p6","label":"Nuevo · próximamente","badge":True,"name":"Pérgola bioclimática",
    "tag":"Terraza útil todo el año.",
    "desc":"Estructura de aluminio con lamas orientables para regular el sol, la ventilación y la protección contra la lluvia. Versiones manual y automática.",
    "items":[("lamas","Sombra regulable","las lamas se orientan según el sol."),
             ("gota","Contra la lluvia","con drenaje integrado."),
             ("switch","Control","manual o automática; iluminación LED opcional.")],
    "small":"", "photos":["pg"], "wide":True},
  ],
  "cover": {"title":"Sistemas exteriores para ventanas",
    "lines":["Protección solar","Seguridad","Confort desde el exterior"],
    "lead":"Nuestras soluciones:",
    "items":["Persianas enrollables de aluminio","Persianas venecianas exteriores","Screens solares exteriores","Mosquiteros"],
    "foot":"Fabricados en Europa · Para proyectos residenciales, comerciales y hoteleros."},
  "closing": {
    "title":"Protección solar exterior premium para proyectos que exigen más.",
    "body":"Sistemas de protección solar, seguridad y confort fabricados en Europa, para proyectos residenciales, comerciales y hoteleros.",
    "b2b":"Atendemos exclusivamente a empresas y proyectos (B2B).",
    "with_title":"Trabajamos con:",
    "with":["Desarrolladores y constructoras.","Hoteles y empresas de hospitalidad.",
            "Fabricantes y distribuidores de ventanas y sistemas de protección solar."],
    "quote":"Cada proyecto se cotiza a la medida.",
    "talk":"Hablemos de tu proyecto",
    "contacts":[("tel","+52 81 2590 1796","tel:+528125901796"),
                ("mail","info@simplemadeblinds.mx","mailto:info@simplemadeblinds.mx"),
                ("web","simplemadeblinds.mx","https://simplemadeblinds.mx/"),
                ("pin","Showroom en Monterrey, Cambridge 103 · próximamente",None)],
    "endorse":"GRUPO-VOES_Endorsement_ES_OnDark.svg",
  },
 },
}
IDEAL = {"es": {
  "p1": "recámaras, habitaciones de hotel y oficinas con sol directo.",
  "p2": "planta baja, locales comerciales y accesos a terrazas o jardines.",
  "p3": "oficinas, fachadas comerciales y áreas de trabajo.",
  "p4": "grandes ventanales, terrazas y áreas con vista.",
  "p5": "ventanas y puertas corredizas de viviendas, hoteles y oficinas.",
  "p6": "terrazas, restaurantes y áreas comunes de hoteles y desarrollos."}}
C = CONTENT[LANG]
for _p in C["pages"]:
    _p["ideal"] = IDEAL[LANG][_p["key"]]

# ---------- CSS ----------
BASE_CSS = """
@font-face{font-family:"Encode Sans";font-weight:400;src:url("assets/EncodeSans-Regular.ttf")}
@font-face{font-family:"Encode Sans";font-weight:500;src:url("assets/EncodeSans-Medium.ttf")}
@font-face{font-family:"Encode Sans";font-weight:600;src:url("assets/EncodeSans-SemiBold.ttf")}
:root{--navy:#1A355C;--powder:#F5F5F0;--texto:#21242C;--gris:#697080;--linea:#DDDFE3;--blanco:#FFFFFF}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:"Encode Sans",Arial,sans-serif;color:var(--texto);-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.page{position:relative;overflow:hidden;page-break-after:always;break-after:page;background:var(--blanco)}
.page:last-child{page-break-after:auto;break-after:auto}
.ic{display:block;color:var(--navy);flex:none}
img{display:block}
.photo{background-size:cover;background-repeat:no-repeat;background-color:var(--powder)}
.label{font-weight:600;text-transform:uppercase;letter-spacing:.16em;color:var(--navy)}
.badge{display:inline-block;border:2px solid var(--navy);color:var(--navy);font-weight:600;letter-spacing:.14em;text-transform:uppercase}
.name{font-weight:500;color:var(--navy);letter-spacing:-.01em}
.tag{font-weight:500;color:var(--texto)}
.desc{font-weight:400;color:var(--texto)}
.item b{font-weight:600;color:var(--navy)}
.small{color:var(--gris)}
.foot{color:var(--gris)}
.foot a{color:var(--navy);font-weight:600}
"""

PHONE_CSS = """
@page{size:1080px 1920px;margin:0}
.page{width:1080px;height:1920px;padding:72px 72px 0 72px;display:flex;flex-direction:column}
.logo{height:68px;width:auto;align-self:flex-start}
.top{margin-top:36px}
.label{font-size:26px;margin-bottom:12px}
.badge{font-size:26px;padding:8px 22px;margin-bottom:16px;border-radius:0}
.name{font-size:84px;line-height:1.04}
.tag{font-size:46px;line-height:1.2;margin-top:18px}
.desc{font-size:38px;line-height:1.36;margin-top:16px}
.photos{display:flex;gap:32px;margin-top:28px}
.photos .photo{width:452px;height:603px}
.photos .photo.wide{width:936px;height:527px;background-size:100% 100%}
.items{margin-top:22px;border-top:2px solid var(--linea);flex:1;display:flex;flex-direction:column}
.item{flex:1;display:flex;gap:26px;align-items:center;padding:12px 0;border-bottom:2px solid var(--linea);font-size:38px;line-height:1.28}
.item .ic{width:76px;height:76px}
.foot{padding:20px 0 48px 0;max-width:800px}
.foot .ideal{font-size:30px;line-height:1.33;color:var(--texto)}
.foot .ideal b{font-weight:600;color:var(--navy)}
.foot .small{font-size:25px;line-height:1.3;margin-top:8px}
.foot .link{display:block;font-size:30px;margin-top:12px}
/* cover */
.page.cover{background:#fff;color:var(--texto);padding:72px 72px 80px}
.cover .ctitle{font-weight:500;color:var(--navy);font-size:100px;line-height:1.04;letter-spacing:-.01em;margin-top:64px}
.cover .clines{margin-top:36px;font-size:46px;line-height:1.3;color:var(--texto)}
.cover .cl{padding:6px 0}
.cover .cphoto{flex:1;min-height:0;margin:56px 0 52px;background-size:cover;background-position:center;box-shadow:0 26px 54px -10px rgba(26,53,92,.34),0 4px 14px rgba(26,53,92,.12)}
.cover .lead{font-weight:600;color:var(--navy);font-size:30px;letter-spacing:.14em;text-transform:uppercase}
.cover .sol{font-weight:500;color:var(--texto);font-size:42px;line-height:1.34;margin-top:14px}
.cover .nw{white-space:nowrap}
.cover .sol .d{color:#601B22;font-weight:600;margin:0 .1em}
.cover .cfoot{font-size:27px;line-height:1.35;color:var(--gris);margin-top:34px}
/* closing */
.page.close{background:var(--navy);color:#fff;padding-bottom:0}
.close .logo{height:68px}
.close h1{font-weight:500;font-size:68px;line-height:1.1;margin-top:64px;letter-spacing:-.01em}
.close .body{font-size:36px;line-height:1.4;margin-top:24px;color:#fff}
.close .b2b{font-weight:600;font-size:40px;line-height:1.3;margin-top:32px;padding-left:26px;border-left:6px solid #fff}
.close .with{margin-top:34px;font-size:34px;font-weight:600}
.close ul{list-style:none;margin-top:8px}
.close li{font-size:34px;line-height:1.32;padding:12px 0 12px 44px;position:relative;border-bottom:2px solid rgba(255,255,255,.28)}
.close li:before{content:"";position:absolute;left:0;top:1.05em;width:26px;height:3px;background:#fff}
.close .quote{font-size:36px;font-weight:500;margin-top:30px}
.close h2{font-weight:500;font-size:56px;margin-top:48px}
.contacts{margin-top:14px}
.contact{display:flex;align-items:center;gap:26px;font-size:40px;padding:16px 0;font-weight:500}
.contact .ic{color:#fff;width:60px;height:60px}
.contact.sm{font-size:34px;font-weight:400;line-height:1.3}
.endorse{margin-top:auto;padding:0 0 56px 0}
.endorse img{height:34px;width:auto}
"""

DESK_CSS = """
@page{size:1920px 1080px;margin:0}
.page{width:1920px;height:1080px}
.left{position:absolute;left:80px;top:56px;width:790px}
.logo{height:60px;width:auto;display:block}
.top{margin-top:34px}
.label{font-size:22px;margin-bottom:12px}
.badge{font-size:20px;padding:6px 18px;margin-bottom:14px}
.name{font-size:84px;line-height:1.04}
.tag{font-size:40px;line-height:1.2;margin-top:14px}
.desc{font-size:29px;line-height:1.38;margin-top:12px;width:790px}
.photos{position:absolute;right:0;top:0;height:640px;display:flex;gap:8px}
.photos .photo{width:480px;height:640px}
.photos .photo.wide{width:1138px;background-size:100% 100%}
.page.pg .left{width:680px}
.page.pg .desc{width:680px}
.band{position:absolute;left:0;right:0;top:640px;height:440px;background:var(--powder)}
.items{position:absolute;left:80px;right:80px;top:654px;height:330px;display:grid;grid-template-columns:repeat(3,1fr);gap:56px;align-content:center;align-items:start}
.item{display:flex;gap:24px;align-items:flex-start;font-size:38px;line-height:1.3}
.item .ic{width:92px;height:92px}
.foot{position:absolute;left:80px;right:80px;bottom:38px;display:flex;justify-content:space-between;align-items:flex-end}
.foot .ideal{font-size:28px;line-height:1.35;color:var(--texto)}
.foot .ideal b{font-weight:600;color:var(--navy)}
.foot .small{font-size:22px;margin-top:4px}
.foot .link{font-size:28px}
/* cover */
.page.cover{background:#fff;color:var(--texto)}
.cover .ctitle{position:absolute;left:80px;top:190px;width:880px;font-weight:500;color:var(--navy);font-size:92px;line-height:1.04;letter-spacing:-.01em}
.cover .clines{position:absolute;left:80px;top:440px;width:880px;font-size:40px;line-height:1.3;color:var(--texto)}
.cover .cl{padding:5px 0}
.cover .cphoto{position:absolute;left:1030px;top:56px;width:810px;height:648px;background-size:cover;background-position:center;box-shadow:0 24px 50px -10px rgba(26,53,92,.34),0 4px 14px rgba(26,53,92,.12)}
.cover .cbottom{position:absolute;left:80px;right:80px;top:790px}
.cover .lead{font-weight:600;color:var(--navy);font-size:24px;letter-spacing:.14em;text-transform:uppercase}
.cover .sol{font-weight:500;color:var(--texto);font-size:38px;line-height:1.34;margin-top:10px}
.cover .sol .d{color:#601B22;font-weight:600;margin:0 .1em}
.cover .cfoot{position:absolute;left:80px;bottom:48px;font-size:24px;color:var(--gris)}
/* closing */
.page.close{background:var(--navy);color:#fff}
.close .left{width:1000px}
.close h1{font-weight:500;font-size:70px;line-height:1.1;margin-top:60px;letter-spacing:-.01em}
.close .body{font-size:31px;line-height:1.45;margin-top:22px;width:900px}
.close .b2b{font-weight:600;font-size:34px;line-height:1.3;margin-top:28px;padding-left:22px;border-left:5px solid #fff}
.close .with{margin-top:28px;font-size:29px;font-weight:600}
.close ul{list-style:none;margin-top:8px;width:900px}
.close li{font-size:29px;line-height:1.3;padding:9px 0 9px 40px;position:relative;border-bottom:2px solid rgba(255,255,255,.28)}
.close li:before{content:"";position:absolute;left:0;top:1.05em;width:24px;height:3px;background:#fff}
.close .quote{font-size:31px;font-weight:500;margin-top:26px}
.rcol{position:absolute;left:1180px;top:176px;width:660px}
.close h2{font-weight:500;font-size:56px;margin:0}
.contacts{margin-top:26px}
.contact{display:flex;align-items:center;gap:24px;font-size:33px;padding:18px 0;font-weight:500}
.contact .ic{color:#fff;width:56px;height:56px}
.contact.sm{font-size:28px;font-weight:400;line-height:1.3}
.endorse{position:absolute;right:88px;bottom:46px}
.endorse img{height:34px;width:auto}
"""

def logo(variant="Primary"):
    return f'<img class="logo" src="assets/SMBMX_Logo_v3_{variant}.svg" alt="Simple Made Blinds Mexico">'

def product_page(p, mode):
    items = "".join(f'<div class="item">{icon(i)}<div><b>{b}:</b> {t}</div></div>' for i, b, t in p["items"])
    label = ""
    if p.get("badge"):
        label = f'<div class="badge">{p["label"]}</div>'
    elif p.get("label"):
        label = f'<div class="label">{p["label"]}</div>'
    cls = "page pg" if p.get("wide") else "page"
    wide = " wide" if p.get("wide") else ""
    ph = '<div class="photos">' + "".join(f'<div class="photo{wide}" style="background-image:url(photos/{x}.jpg);background-position:50% 45%"></div>' for x in p["photos"]) + '</div>'
    small = f'<div class="small">{p["small"]}</div>' if p.get("small") else ""
    foot = (f'<div class="foot"><div class="fl"><div class="ideal"><b>Ideal para:</b> {p["ideal"]}</div>{small}</div>'
            f'<a class="link" href="https://simplemadeblinds.mx/">simplemadeblinds.mx</a></div>')
    if mode == "phone":
        return (f'<section class="{cls}" id="{p["key"]}">{logo()}<div class="top">{label}'
                f'<div class="name">{p["name"]}</div><div class="tag">{p["tag"]}</div>'
                f'<div class="desc">{p["desc"]}</div></div>{ph}<div class="items">{items}</div>{foot}</section>')
    return (f'<section class="{cls}" id="{p["key"]}"><div class="left">{logo()}<div class="top">{label}'
            f'<div class="name">{p["name"]}</div><div class="tag">{p["tag"]}</div>'
            f'<div class="desc">{p["desc"]}</div></div></div>{ph}<div class="band"></div>'
            f'<div class="items">{items}</div>{foot}</section>')

def cover_page(mode):
    c = C["cover"]
    items = c["items"]
    sol = "".join(f'<span class="nw">{t}&nbsp;<span class="d">&middot;</span></span> ' for t in items[:-1]) + f'<span class="nw">{items[-1]}</span>'
    lines = "".join(f'<div class="cl">{t}</div>' for t in c["lines"])
    photo = '<div class="cphoto" style="background-image:url(photos/cover_facade.jpg)"></div>'
    head = f'{logo()}<div class="ctitle">{c["title"]}</div><div class="clines">{lines}</div>'
    low = f'<div class="lead">{c["lead"]}</div><div class="sol">{sol}</div>'
    foot = f'<div class="cfoot">{c["foot"]}</div>'
    if mode == "phone":
        return f'<section class="page cover" id="p0">{head}{photo}{low}{foot}</section>'
    return (f'<section class="page cover" id="p0"><div style="position:absolute;left:80px;top:56px">{logo()}</div>'
            f'<div class="ctitle">{c["title"]}</div><div class="clines">{lines}</div>{photo}'
            f'<div class="cbottom">{low}</div>{foot}</section>')

def closing_page(mode):
    c = C["closing"]
    lis = "".join(f"<li>{x}</li>" for x in c["with"])
    def contact(i, t, href):
        txt = f'<a href="{href}">{t}</a>' if href else t
        return f'<div class="contact{"" if href else " sm"}">{icon(i)}<span>{txt}</span></div>'
    contacts = "".join(contact(*x) for x in c["contacts"])
    endorse = f'<div class="endorse"><img src="assets/{c["endorse"]}" alt="Una marca de GRUPO VOES, S.A. de C.V."></div>'
    if mode == "phone":
        return (f'<section class="page close" id="p7">{logo("White")}<h1>{c["title"]}</h1>'
                f'<div class="body">{c["body"]}</div><div class="b2b">{c["b2b"]}</div>'
                f'<div class="with">{c["with_title"]}</div><ul>{lis}</ul><div class="quote">{c["quote"]}</div>'
                f'<h2>{c["talk"]}</h2><div class="contacts">{contacts}</div>{endorse}</section>')
    return (f'<section class="page close" id="p7"><div class="left">{logo("White")}<h1>{c["title"]}</h1>'
            f'<div class="body">{c["body"]}</div><div class="b2b">{c["b2b"]}</div>'
            f'<div class="with">{c["with_title"]}</div><ul>{lis}</ul><div class="quote">{c["quote"]}</div></div>'
            f'<div class="rcol"><h2>{c["talk"]}</h2><div class="contacts">{contacts}</div></div>{endorse}</section>')

def build(mode):
    css = BASE_CSS + (PHONE_CSS if mode == "phone" else DESK_CSS)
    body = cover_page(mode) + "".join(product_page(p, mode) for p in C["pages"]) + closing_page(mode)
    return (f'<!doctype html><html lang="{LANG}"><head><meta charset="utf-8">'
            f'<title>Simple Made Blinds Mexico</title><style>{css}</style></head><body>{body}</body></html>')

if __name__ == "__main__":
    for mode in ("phone", "desk"):
        (ROOT / f"pildora_{LANG}_{mode}.html").write_text(build(mode), encoding="utf-8")
    # icon preview sheet
    names = list(ICONS)
    cells = "".join(f'<div style="width:160px;text-align:center;font:14px Arial;color:#333">{icon(n)}<div>{n}</div></div>' for n in names)
    (ROOT / "icons_preview.html").write_text(
        '<html><body style="background:#fff"><style>.ic{width:90px;height:90px;margin:10px auto;color:#1A355C}</style>'
        f'<div style="display:flex;flex-wrap:wrap;gap:10px;padding:20px;width:1100px">{cells}</div></body></html>',
        encoding="utf-8")
    print("html ok")
