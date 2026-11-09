# Bouwt alle pagina's in vijf talen (NL, EN, FR, ES, 中文) met dezelfde kop, taalknop en voet.
# Draai: python3 maak.py
#
# Bestandsnamen: Nederlands = naam.html, andere talen = naam-<taal>.html (bijv. naam-fr.html)
# (dezelfde namen die de app gebruikt voor privacy en voorwaarden).
import os, re

EMAIL = "flashapp.support05@gmail.com"
SITE = "https://thom2005bloem.github.io/flash-app"
TALEN = ["nl", "en", "fr", "es", "zh"]
HTML_LANG = {"nl": "nl", "en": "en", "fr": "fr", "es": "es", "zh": "zh-Hans"}
TAALNAAM = {"nl": "Nederlands", "en": "English", "fr": "Français", "es": "Español", "zh": "中文"}
KORT = {"nl": "NL", "en": "EN", "fr": "FR", "es": "ES", "zh": "中文"}

# Teksten van de kop en voet per taal
UI = {
    "nl": {"menu": "Hoofdmenu", "taal": "Taal", "vragen": "Vragen of feedback? Mail naar",
           "privacy": "Privacybeleid", "voorwaarden": "Voorwaarden", "van": "van {}"},
    "en": {"menu": "Main menu", "taal": "Language", "vragen": "Questions or feedback? Email",
           "privacy": "Privacy policy", "voorwaarden": "Terms of use", "van": "by {}"},
    "fr": {"menu": "Menu principal", "taal": "Langue", "vragen": "Des questions ou un avis ? Écris à",
           "privacy": "Politique de confidentialité", "voorwaarden": "Conditions d'utilisation", "van": "de {}"},
    "es": {"menu": "Menú principal", "taal": "Idioma", "vragen": "¿Preguntas o comentarios? Escribe a",
           "privacy": "Política de privacidad", "voorwaarden": "Términos de uso", "van": "de {}"},
    "zh": {"menu": "主菜单", "taal": "语言", "vragen": "有问题或建议？请发邮件至",
           "privacy": "隐私政策", "voorwaarden": "使用条款", "van": "来自 {}"},
}

MENU = {
    "nl": [("index.html", "Zo werkt het"), ("voorbeeld.html", "Voorbeeld"), ("visie.html", "Visie"), ("over.html", "Over mij"), ("support.html", "Support")],
    "en": [("index.html", "How it works"), ("voorbeeld.html", "Example"), ("visie.html", "Vision"), ("over.html", "About me"), ("support.html", "Support")],
    "fr": [("index.html", "Comment ça marche"), ("voorbeeld.html", "Exemple"), ("visie.html", "Vision"), ("over.html", "À propos"), ("support.html", "Aide")],
    "es": [("index.html", "Cómo funciona"), ("voorbeeld.html", "Ejemplo"), ("visie.html", "Visión"), ("over.html", "Sobre mí"), ("support.html", "Ayuda")],
    "zh": [("index.html", "使用方法"), ("voorbeeld.html", "示例"), ("visie.html", "愿景"), ("over.html", "关于我"), ("support.html", "支持")],
}


def naam(bestand, taal):
    """index.html -> index-en.html enz."""
    return bestand if taal == "nl" else bestand.replace(".html", f"-{taal}.html")


def url(bestand, taal):
    n = naam(bestand, taal)
    return f"{SITE}/" if n == "index.html" else f"{SITE}/{n}"


GLOBE = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/>'
         '<path d="M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></svg>')

SCRIPT = '''<script>
// Taalmenu sluiten bij klik ernaast of Escape, en de gekozen taal onthouden
(function(){
  var d=document.querySelector('.taal');if(!d)return;
  document.addEventListener('click',function(e){if(d.open&&!d.contains(e.target))d.open=false});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&d.open){d.open=false;d.querySelector('summary').focus()}});
  d.querySelectorAll('a[data-taal]').forEach(function(a){a.addEventListener('click',function(){try{localStorage.setItem('flash-taal',a.dataset.taal)}catch(_){}})});
})();
</script>'''


def pagina(bestand, taal, titel, inhoud, beschrijving):
    ui = UI[taal]
    huidig = ' aria-current="page"'
    links = "".join(f'<a href="{naam(b, taal)}"{huidig if b == bestand else ""}>{n}</a>' for b, n in MENU[taal])
    keuzes = "".join(
        f'<a href="{naam(bestand, t)}" hreflang="{HTML_LANG[t]}" lang="{HTML_LANG[t]}" data-taal="{t}"'
        f'{huidig if t == taal else ""}>{TAALNAAM[t]}</a>' for t in TALEN)
    alternatief = "\n".join(f'<link rel="alternate" hreflang="{HTML_LANG[t]}" href="{url(bestand, t)}">' for t in TALEN)
    alternatief += f'\n<link rel="alternate" hreflang="x-default" href="{url(bestand, "nl")}">'
    return f'''<!doctype html>
<html lang="{HTML_LANG[taal]}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titel}</title>
<meta name="description" content="{beschrijving}">
<meta property="og:title" content="{titel}">
<meta property="og:description" content="{beschrijving}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE}/images/kampvuur_maken.jpg">
<link rel="canonical" href="{url(bestand, taal)}">
{alternatief}
<link rel="stylesheet" href="style.css">
</head>
<body>
<header><div class="wrap kop"><a class="merk" href="{naam("index.html", taal)}"><i></i>Flash</a><nav aria-label="{ui["menu"]}">{links}</nav><details class="taal"><summary aria-label="{ui["taal"]}: {TAALNAAM[taal]}">{GLOBE}<span>{KORT[taal]}</span></summary><div class="taal-menu">{keuzes}</div></details></div></header>
<main>
{inhoud}
</main>
<footer><div class="wrap voet"><span>{ui["vragen"]} <a href="mailto:{EMAIL}">{EMAIL}</a></span><a href="{naam("privacy.html", taal)}">{ui["privacy"]}</a><a href="{naam("voorwaarden.html", taal)}">{ui["voorwaarden"]}</a></div></footer>
{SCRIPT}
</body>
</html>
'''


def foto(img, tekst, van, alt, taal="nl"):
    # Echte foto (images/<naam>.jpg) als die er is, anders de tekening (.svg)
    if os.path.exists(f"images/{img}.jpg"):
        ext = "jpg"
    elif os.path.exists(f"images/{img}.svg"):
        ext = "svg"
    else:
        return ""  # geen foto en geen tekening: polaroid weglaten
    return f'<figure class="polaroid"><img src="images/{img}.{ext}" alt="{alt}" loading="lazy"><figcaption>{tekst}<span>{UI[taal]["van"].format(van)}</span></figcaption></figure>'


P = {t: {} for t in TALEN}  # P[taal][bestand] = (titel, beschrijving, inhoud)

# ───────────────────────────── Zo werkt het (index) ─────────────────────────────

P["nl"]["index.html"] = ("Flash app – de gedeelde wegwerpcamera voor je evenementen",
"Flash is een iPhone-app: een gedeelde wegwerpcamera voor je verjaardag, reis of feest. Iedereen voegt foto's, quotes en berichten toe en alles blijft verzegeld tot de openingsdag.", f'''
<div class="wrap held">
  <div>
    <span class="status">Nu in testfase met vrienden en familie</span>
    <h1>Iedereen fotografeert. Pas later zie je alles.</h1>
    <p class="inleiding">Flash is een gedeelde wegwerpcamera voor je verjaardag, reis of feest. Iedereen voegt foto's, quotes en berichten toe, en alles blijft verzegeld tot de dag dat het evenement opengaat.</p>
    <div class="knoppen"><a class="knop vol" href="voorbeeld.html">Bekijk een voorbeeld</a><a class="knop rand" href="#zo-werkt-het">Zo werkt het</a></div>
  </div>
  <div class="stapel" aria-hidden="true">
    {foto("kampvuur_maken","Kampvuur aan het water","Noor","")}
    {foto("wandelen","Verdwaald, maar wel samen","Sam","")}
    {foto("kampvuur","Koffie bij de tent","Lars","")}
  </div>
</div>

<section id="zo-werkt-het"><div class="wrap">
  <h2>Zo werkt het</h2>
  <ol class="stappen">
    <li><h3>Maak een evenement</h3><p>Geef het een naam en kies de dag waarop het opengaat: morgen, over een maand of over een jaar.</p></li>
    <li><h3>Nodig je vrienden uit</h3><p>Deel een code. Deelnemers voegen foto's, quotes en berichten toe; kijkers zien alleen het eindresultaat.</p></li>
    <li><h3>Open het samen</h3><p>Op de openingsdag krijgt iedereen een melding en zie je eindelijk alles wat de anderen hebben vastgelegd.</p></li>
  </ol>
</div></section>

<section><div class="wrap">
  <h2>Waarom Flash anders is</h2>
  <div class="kenmerken">
    <div><h3>Verzegeld tot de openingsdag</h3><p>Je ziet alleen wat je zelf toevoegt. De rest blijft een verrassing, net als bij een rolletje dat nog ontwikkeld moet worden.</p></div>
    <div><h3>Alleen jouw groep</h3><p>Een evenement heeft maximaal 15 personen. Niemand anders kan het vinden of bekijken.</p></div>
    <div><h3>Meer dan foto's</h3><p>Leg ook vast wat er gezegd werd, of schrijf een bericht aan jullie toekomstige zelf.</p></div>
    <div><h3>Meteen in je galerij</h3><p>Als het evenement opengaat, zet Flash alle foto's in een album op je telefoon.</p></div>
  </div>
</div></section>
''')

P["en"]["index.html"] = ("Flash app – the shared disposable camera for your events",
"Flash is an iPhone app: a shared disposable camera for your birthday, trip or party. Everyone adds photos, quotes and messages, and everything stays sealed until the opening day.", f'''
<div class="wrap held">
  <div>
    <span class="status">Now in testing with friends and family</span>
    <h1>Everyone takes photos. You see them all later.</h1>
    <p class="inleiding">Flash is a shared disposable camera for your birthday, trip or party. Everyone adds photos, quotes and messages, and everything stays sealed until the day the event opens.</p>
    <div class="knoppen"><a class="knop vol" href="voorbeeld-en.html">See an example</a><a class="knop rand" href="#zo-werkt-het">How it works</a></div>
  </div>
  <div class="stapel" aria-hidden="true">
    {foto("kampvuur_maken","Campfire by the water","Noor","","en")}
    {foto("wandelen","Lost, but together","Sam","","en")}
    {foto("kampvuur","Coffee by the tent","Lars","","en")}
  </div>
</div>

<section id="zo-werkt-het"><div class="wrap">
  <h2>How it works</h2>
  <ol class="stappen">
    <li><h3>Create an event</h3><p>Give it a name and choose the day it opens: tomorrow, in a month or in a year.</p></li>
    <li><h3>Invite your friends</h3><p>Share a code. Participants add photos, quotes and messages; viewers only see the end result.</p></li>
    <li><h3>Open it together</h3><p>On the opening day everyone gets a notification and you finally see everything the others captured.</p></li>
  </ol>
</div></section>

<section><div class="wrap">
  <h2>Why Flash is different</h2>
  <div class="kenmerken">
    <div><h3>Sealed until the opening day</h3><p>You only see what you add yourself. The rest stays a surprise, just like a roll of film that still has to be developed.</p></div>
    <div><h3>Only your group</h3><p>An event has at most 15 people. Nobody else can find or view it.</p></div>
    <div><h3>More than photos</h3><p>Also capture what was said, or write a message to your future selves.</p></div>
    <div><h3>Straight to your photo library</h3><p>When the event opens, Flash puts all the photos in an album on your phone.</p></div>
  </div>
</div></section>
''')

P["zh"]["index.html"] = ("Flash 应用 – 为你的活动准备的共享一次性相机",
"Flash 是一款 iPhone 应用：为生日、旅行或派对准备的共享一次性相机。每个人都可以添加照片、语录和留言，所有内容都会封存到开启日。", f'''
<div class="wrap held">
  <div>
    <span class="status">目前正在与亲友一起测试</span>
    <h1>大家一起拍，之后才看到全部。</h1>
    <p class="inleiding">Flash 是一台共享的一次性相机，适合生日、旅行或派对。每个人都可以添加照片、语录和留言，所有内容都会被封存，直到活动开启的那一天。</p>
    <div class="knoppen"><a class="knop vol" href="voorbeeld-zh.html">查看示例</a><a class="knop rand" href="#zo-werkt-het">使用方法</a></div>
  </div>
  <div class="stapel" aria-hidden="true">
    {foto("kampvuur_maken","水边的篝火","Noor","","zh")}
    {foto("wandelen","迷路了，但在一起","Sam","","zh")}
    {foto("kampvuur","帐篷边的咖啡","Lars","","zh")}
  </div>
</div>

<section id="zo-werkt-het"><div class="wrap">
  <h2>使用方法</h2>
  <ol class="stappen">
    <li><h3>创建活动</h3><p>给它起个名字，再选好开启的日子：明天、一个月后，或者一年后。</p></li>
    <li><h3>邀请朋友</h3><p>分享一个邀请码。参与者可以添加照片、语录和留言；观看者只能看到最终结果。</p></li>
    <li><h3>一起打开</h3><p>开启当天，每个人都会收到通知，终于能看到其他人记录下的一切。</p></li>
  </ol>
</div></section>

<section><div class="wrap">
  <h2>Flash 有什么不同</h2>
  <div class="kenmerken">
    <div><h3>封存到开启日</h3><p>你只能看到自己添加的内容。其余的都是惊喜，就像一卷还没冲洗的胶卷。</p></div>
    <div><h3>只属于你们</h3><p>每个活动最多 15 人。其他人无法找到或查看。</p></div>
    <div><h3>不只是照片</h3><p>还可以记下大家说过的话，或者给未来的你们写一段留言。</p></div>
    <div><h3>自动存入相册</h3><p>活动开启后，Flash 会把所有照片放进你手机里的一个相册。</p></div>
  </div>
</div></section>
''')

# ───────────────────────────── Voorbeeld ─────────────────────────────

P["nl"]["voorbeeld.html"] = ("Voorbeeld – Flash", "Zo ziet een geopend evenement in Flash eruit.", f'''
<section><div class="wrap">
  <h1>Zo ziet een geopend evenement eruit</h1>
  <p class="inleiding">Dit is een voorbeeld met verzonnen namen. Zo ziet een weekend met vrienden eruit, op de dag dat het opengaat.</p>
</div></section>

<section><div class="wrap">
  <h2>Voor en na de openingsdag</h2>
  <div class="voorna">
    <div class="scherm"><span class="label dicht">Verzegeld</span><h3>Weekend Ardennen</h3><div class="teller">3d 14u 32m</div><p>Je ziet alleen je eigen 6 foto's. Er zitten al 41 herinneringen in van 9 vrienden.</p></div>
    <div class="scherm"><span class="label">Geopend</span><h3>Weekend Ardennen</h3><div class="teller">41</div><p>herinneringen van 9 vrienden, nu voor iedereen zichtbaar en opgeslagen in ieders galerij.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="evenement-kop"><div><span class="label">Geopend op 14 juni 2026</span><h2 style="margin:0">Weekend Ardennen</h2></div><p class="waarschuwing" style="margin:0">41 herinneringen van 9 vrienden</p></div>
  <div class="muur">
    {foto("bergen","Uitzicht op dag één","Sam","Beboste heuvels in de Ardennen")}
    <div class="quote"><blockquote>Ik weet zeker dat dit pad een kortere weg is.</blockquote><p>Lars, twee uur voordat we verdwaalden</p></div>
    {foto("wandelen","Verdwaald, maar wel samen","Thom","Twee vrienden met rugzakken in het bos")}
    {foto("kampvuur","Koffie bij de tent","Noor","Vrienden rond een kampvuur bij een tent")}
    {foto("kampvuur_maken","Kampvuur aan het water","Mila","Vrienden rond een kampvuur bij zonsondergang")}
    <div class="bericht"><strong>Bericht aan de toekomst</strong><p>Als jullie dit lezen: hebben we het volgende weekend al gepland? Zo niet, doe het nu.</p><small>van Jesse</small></div>
    {foto("feest","Verjaardag van Sam om middernacht","Jesse","Verjaardagstaart met kaarsjes")}
    {foto("strand","Zondag nog even naar het water","Sam","Tekening van een strand met een parasol")}
    <div class="quote"><blockquote>Nog één spelletje en dan gaan we slapen.</blockquote><p>Noor, om half vier 's nachts</p></div>
    {foto("stad","Terug in de stad","Mila","Tekening van een stad bij nacht")}
  </div>
</div></section>

<section><div class="wrap">
  <div class="evenement-kop"><div><span class="label">Geopend op 1 april 2026</span><h2 style="margin:0">Skivakantie 2026</h2></div><p class="waarschuwing" style="margin:0">58 herinneringen van 7 vrienden</p></div>
  <div class="muur">
    {foto("skivakantie-2026-1","Klaar voor de eerste afdaling","Lars","Skiër op de piste met bergen op de achtergrond")}
    <div class="quote"><blockquote>Rode piste? Dat is toch gewoon een blauwe met een andere kleur.</blockquote><p>Sam, vlak voor zijn eerste val</p></div>
    {foto("skivakantie-2026-2","Even genieten van het uitzicht","Noor","Skiër kijkt uit over besneeuwde bergtoppen")}
    {foto("skivakantie-2026-3","Blauwe lucht, verse sneeuw","Thom","Skipiste met liften en bergen")}
    <div class="bericht"><strong>Bericht aan de toekomst</strong><p>Zelfde week volgend jaar? Niemand mag zeggen dat hij geen tijd heeft.</p><small>van Mila</small></div>
    {foto("skivakantie-2026-4","Lunchpauze bij de lift","Jesse","Ski's en stokken in de sneeuw bij een skilift")}
  </div>
</div></section>

<section><div class="wrap">
  <div class="evenement-kop"><div><span class="label">Geopend op 1 januari 2026</span><h2 style="margin:0">Vakantie Indonesië 2025</h2></div><p class="waarschuwing" style="margin:0">73 herinneringen van 12 reisgenoten</p></div>
  <div class="muur">
    {foto("vakantie-indonesie-2025-1","Rijstvelden bij het dorp","Mila","Rijstvelden voor een dorp met palmbomen")}
    {foto("vakantie-indonesie-2025-3","Uitzicht op de Bromo-vlakte","Lars","Vulkaan en vlakte achter tropische bomen")}
    <div class="quote"><blockquote>Nog één tempel en dan gaan we echt naar het zwembad.</blockquote><p>Noor, drie tempels geleden</p></div>
    {foto("vakantie-indonesie-2025-5","Groepsfoto bij de Borobudur","Thom","Groep reizigers bij de stoepa's van de Borobudur")}
    {foto("vakantie-indonesie-2025-2","Uitzicht over de jungle","Sam","Palmbomen en rijstterrassen in de jungle")}
    <div class="bericht"><strong>Bericht aan de toekomst</strong><p>Weet je nog hoe warm het was? Bewaar deze foto's voor een koude dag in januari.</p><small>van Jesse</small></div>
    {foto("vakantie-indonesie-2025-4","Afkoelen in het zwembad","Noor","Zwembad tussen palmbomen")}
  </div>
  <p class="waarschuwing">De foto's hierboven zijn voorbeeldfoto's. In de app staan de echte foto's van jouw groep.</p>
</div></section>
''')

P["en"]["voorbeeld.html"] = ("Example – Flash", "This is what an opened event in Flash looks like.", f'''
<section><div class="wrap">
  <h1>This is what an opened event looks like</h1>
  <p class="inleiding">This is an example with made-up names: a weekend with friends, on the day it opens.</p>
</div></section>

<section><div class="wrap">
  <h2>Before and after the opening day</h2>
  <div class="voorna">
    <div class="scherm"><span class="label dicht">Sealed</span><h3>Weekend in the Ardennes</h3><div class="teller">3d 14h 32m</div><p>You only see your own 6 photos. It already holds 41 memories from 9 friends.</p></div>
    <div class="scherm"><span class="label">Opened</span><h3>Weekend in the Ardennes</h3><div class="teller">41</div><p>memories from 9 friends, now visible to everyone and saved in everyone's photo library.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="evenement-kop"><div><span class="label">Opened on 14 June 2026</span><h2 style="margin:0">Weekend in the Ardennes</h2></div><p class="waarschuwing" style="margin:0">41 memories from 9 friends</p></div>
  <div class="muur">
    {foto("bergen","The view on day one","Sam","Wooded hills in the Ardennes","en")}
    <div class="quote"><blockquote>I'm sure this path is a shortcut.</blockquote><p>Lars, two hours before we got lost</p></div>
    {foto("wandelen","Lost, but together","Thom","Two friends with backpacks in the forest","en")}
    {foto("kampvuur","Coffee by the tent","Noor","Friends around a campfire next to a tent","en")}
    {foto("kampvuur_maken","Campfire by the water","Mila","Friends around a campfire at sunset","en")}
    <div class="bericht"><strong>Message to the future</strong><p>If you're reading this: have we planned the next weekend yet? If not, do it now.</p><small>from Jesse</small></div>
    {foto("feest","Sam's birthday at midnight","Jesse","Birthday cake with candles","en")}
    {foto("strand","One last trip to the water on Sunday","Sam","Drawing of a beach with a parasol","en")}
    <div class="quote"><blockquote>One more game and then we'll go to sleep.</blockquote><p>Noor, at half past three in the morning</p></div>
    {foto("stad","Back in the city","Mila","Drawing of a city at night","en")}
  </div>
</div></section>

<section><div class="wrap">
  <div class="evenement-kop"><div><span class="label">Opened on 1 April 2026</span><h2 style="margin:0">Ski trip 2026</h2></div><p class="waarschuwing" style="margin:0">58 memories from 7 friends</p></div>
  <div class="muur">
    {foto("skivakantie-2026-1","Ready for the first run","Lars","Skier on the slope with mountains in the background","en")}
    <div class="quote"><blockquote>Red slope? That's just a blue one in a different colour.</blockquote><p>Sam, right before his first fall</p></div>
    {foto("skivakantie-2026-2","Taking in the view","Noor","Skier looking out over snowy peaks","en")}
    {foto("skivakantie-2026-3","Blue sky, fresh snow","Thom","Ski slope with lifts and mountains","en")}
    <div class="bericht"><strong>Message to the future</strong><p>Same week next year? Nobody gets to say they don't have time.</p><small>from Mila</small></div>
    {foto("skivakantie-2026-4","Lunch break by the lift","Jesse","Skis and poles in the snow by a ski lift","en")}
  </div>
</div></section>

<section><div class="wrap">
  <div class="evenement-kop"><div><span class="label">Opened on 1 January 2026</span><h2 style="margin:0">Indonesia trip 2025</h2></div><p class="waarschuwing" style="margin:0">73 memories from 12 travel companions</p></div>
  <div class="muur">
    {foto("vakantie-indonesie-2025-1","Rice fields by the village","Mila","Rice fields in front of a village with palm trees","en")}
    {foto("vakantie-indonesie-2025-3","View of the Bromo plain","Lars","Volcano and plain behind tropical trees","en")}
    <div class="quote"><blockquote>One more temple and then we're really going to the pool.</blockquote><p>Noor, three temples ago</p></div>
    {foto("vakantie-indonesie-2025-5","Group photo at Borobudur","Thom","Group of travellers at the stupas of Borobudur","en")}
    {foto("vakantie-indonesie-2025-2","View over the jungle","Sam","Palm trees and rice terraces in the jungle","en")}
    <div class="bericht"><strong>Message to the future</strong><p>Remember how hot it was? Save these photos for a cold day in January.</p><small>from Jesse</small></div>
    {foto("vakantie-indonesie-2025-4","Cooling off in the pool","Noor","Swimming pool between palm trees","en")}
  </div>
  <p class="waarschuwing">The photos above are sample photos. In the app you'll see the real photos of your group.</p>
</div></section>
''')

P["zh"]["voorbeeld.html"] = ("示例 – Flash", "在 Flash 中，一个已开启的活动是这样的。", f'''
<section><div class="wrap">
  <h1>已开启的活动是这样的</h1>
  <p class="inleiding">这是一个使用虚构名字的示例：朋友们的一个周末，在开启当天的样子。</p>
</div></section>

<section><div class="wrap">
  <h2>开启日前后</h2>
  <div class="voorna">
    <div class="scherm"><span class="label dicht">已封存</span><h3>阿登周末</h3><div class="teller">3天 14时 32分</div><p>你只能看到自己的 6 张照片。里面已经有 9 位朋友的 41 条回忆。</p></div>
    <div class="scherm"><span class="label">已开启</span><h3>阿登周末</h3><div class="teller">41</div><p>条来自 9 位朋友的回忆，现在所有人都能看到，并已保存到每个人的相册。</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="evenement-kop"><div><span class="label">开启于 2026 年 6 月 14 日</span><h2 style="margin:0">阿登周末</h2></div><p class="waarschuwing" style="margin:0">9 位朋友的 41 条回忆</p></div>
  <div class="muur">
    {foto("bergen","第一天的风景","Sam","阿登地区林木茂密的山丘","zh")}
    <div class="quote"><blockquote>我敢肯定这条路是近路。</blockquote><p>Lars，在我们迷路前两小时</p></div>
    {foto("wandelen","迷路了，但在一起","Thom","两个背着背包的朋友走在森林里","zh")}
    {foto("kampvuur","帐篷边的咖啡","Noor","朋友们在帐篷旁围着篝火","zh")}
    {foto("kampvuur_maken","水边的篝火","Mila","日落时分围着篝火的朋友们","zh")}
    <div class="bericht"><strong>给未来的留言</strong><p>如果你们看到这条：下一个周末计划好了吗？还没有的话，现在就定。</p><small>来自 Jesse</small></div>
    {foto("feest","午夜时分 Sam 的生日","Jesse","插着蜡烛的生日蛋糕","zh")}
    {foto("strand","周日再去一次水边","Sam","一幅画着沙滩和遮阳伞的插图","zh")}
    <div class="quote"><blockquote>再玩一局就睡觉。</blockquote><p>Noor，凌晨三点半</p></div>
    {foto("stad","回到城市","Mila","一幅城市夜景插图","zh")}
  </div>
</div></section>

<section><div class="wrap">
  <div class="evenement-kop"><div><span class="label">开启于 2026 年 4 月 1 日</span><h2 style="margin:0">2026 滑雪之旅</h2></div><p class="waarschuwing" style="margin:0">7 位朋友的 58 条回忆</p></div>
  <div class="muur">
    {foto("skivakantie-2026-1","准备好第一次滑降","Lars","雪道上的滑雪者，背景是群山","zh")}
    <div class="quote"><blockquote>红道？不就是换了个颜色的蓝道嘛。</blockquote><p>Sam，在他第一次摔倒之前</p></div>
    {foto("skivakantie-2026-2","停下来欣赏风景","Noor","滑雪者眺望白雪覆盖的山峰","zh")}
    {foto("skivakantie-2026-3","蓝天，新雪","Thom","有缆车和群山的滑雪道","zh")}
    <div class="bericht"><strong>给未来的留言</strong><p>明年同一周？谁都不许说没时间。</p><small>来自 Mila</small></div>
    {foto("skivakantie-2026-4","缆车旁的午休","Jesse","滑雪缆车旁插在雪里的雪板和雪杖","zh")}
  </div>
</div></section>

<section><div class="wrap">
  <div class="evenement-kop"><div><span class="label">开启于 2026 年 1 月 1 日</span><h2 style="margin:0">2025 印度尼西亚之旅</h2></div><p class="waarschuwing" style="margin:0">12 位旅伴的 73 条回忆</p></div>
  <div class="muur">
    {foto("vakantie-indonesie-2025-1","村庄旁的稻田","Mila","棕榈树环绕的村庄前的稻田","zh")}
    {foto("vakantie-indonesie-2025-3","眺望布罗莫平原","Lars","热带树木后的火山和平原","zh")}
    <div class="quote"><blockquote>再看一座寺庙，然后我们真的去泳池。</blockquote><p>Noor，三座寺庙之前</p></div>
    {foto("vakantie-indonesie-2025-5","在婆罗浮屠的合影","Thom","一群旅行者在婆罗浮屠的佛塔旁","zh")}
    {foto("vakantie-indonesie-2025-2","俯瞰丛林","Sam","丛林中的棕榈树和梯田","zh")}
    <div class="bericht"><strong>给未来的留言</strong><p>还记得那时有多热吗？把这些照片留到一月的某个冷天再看。</p><small>来自 Jesse</small></div>
    {foto("vakantie-indonesie-2025-4","在泳池里降温","Noor","棕榈树之间的泳池","zh")}
  </div>
  <p class="waarschuwing">以上照片均为示例照片。在应用中，你会看到你们小组的真实照片。</p>
</div></section>
''')

# ───────────────────────────── Visie ─────────────────────────────

P["nl"]["visie.html"] = ("Visie – Flash", "Waarom Flash bestaat en waar het naartoe gaat.", '''
<section><div class="wrap">
  <h1>Visie</h1>
  <p class="inleiding">Waarom Flash bestaat en waar het naartoe gaat.</p>
</div></section>

<section><div class="wrap">
  <p class="uitspraak">De mooiste momenten beleef je samen. Flash zorgt dat je ze ook samen terugziet.</p>
</div></section>

<section><div class="wrap">
  <h2>Waar Flash voor staat</h2>
  <div class="principes">
    <div><h3>Eerst beleven</h3><p>Omdat je de foto's pas later ziet, hoef je niet de hele avond op je telefoon te kijken wat anderen posten. Je maakt het moment mee en kijkt later terug.</p></div>
    <div><h3>Samen herinneren</h3><p>Na een weekend staan de foto's verspreid over tien telefoons. Flash brengt ze bij elkaar, samen met wat er gezegd werd.</p></div>
    <div><h3>De verrassing terug</h3><p>Vroeger wachtte je dagen op je ontwikkelde rolletje. Flash brengt dat gevoel terug: de openingsdag is een klein feest op zich.</p></div>
    <div><h3>Privé en eerlijk</h3><p>Geen advertenties, geen volgers, geen openbare profielen. Je herinneringen zijn alleen voor de mensen die erbij waren. Gasten doen altijd gratis mee.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <h2>Waar Flash nu staat</h2>
  <ol class="tijdlijn">
    <li><strong>De app is gebouwd</strong><p>Evenementen, uitnodigingscodes, foto's, quotes, berichten en de openingsdag werken.</p></li>
    <li class="nu"><strong>Nu: testen met vrienden en familie</strong><p>Een kleine groep gebruikt Flash bij echte evenementen en geeft feedback.</p></li>
    <li><strong>Verbeteren op basis van feedback</strong><p>Wat testers missen of lastig vinden, wordt eerst opgelost.</p></li>
    <li><strong>Lancering in de App Store</strong><p>Daarna kan iedereen met een iPhone Flash downloaden.</p></li>
  </ol>
</div></section>
''')

P["en"]["visie.html"] = ("Vision – Flash", "Why Flash exists and where it is heading.", '''
<section><div class="wrap">
  <h1>Vision</h1>
  <p class="inleiding">Why Flash exists and where it is heading.</p>
</div></section>

<section><div class="wrap">
  <p class="uitspraak">The best moments are the ones you share. Flash makes sure you look back on them together too.</p>
</div></section>

<section><div class="wrap">
  <h2>What Flash stands for</h2>
  <div class="principes">
    <div><h3>Live it first</h3><p>Because you only see the photos later, you don't spend the whole evening on your phone checking what others are posting. You enjoy the moment and look back later.</p></div>
    <div><h3>Remember together</h3><p>After a weekend away, the photos are scattered across ten phones. Flash brings them together, along with what was said.</p></div>
    <div><h3>The surprise is back</h3><p>You used to wait days for your film to be developed. Flash brings that feeling back: the opening day is a small celebration in itself.</p></div>
    <div><h3>Private and fair</h3><p>No ads, no followers, no public profiles. Your memories are only for the people who were there. Guests always join for free.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <h2>Where Flash is now</h2>
  <ol class="tijdlijn">
    <li><strong>The app is built</strong><p>Events, invite codes, photos, quotes, messages and the opening day all work.</p></li>
    <li class="nu"><strong>Now: testing with friends and family</strong><p>A small group uses Flash at real events and gives feedback.</p></li>
    <li><strong>Improving based on feedback</strong><p>Whatever testers miss or find difficult gets fixed first.</p></li>
    <li><strong>Launch in the App Store</strong><p>After that, anyone with an iPhone can download Flash.</p></li>
  </ol>
</div></section>
''')

P["zh"]["visie.html"] = ("愿景 – Flash", "Flash 为什么存在，以及它将走向何方。", '''
<section><div class="wrap">
  <h1>愿景</h1>
  <p class="inleiding">Flash 为什么存在，以及它将走向何方。</p>
</div></section>

<section><div class="wrap">
  <p class="uitspraak">最美好的时刻是一起度过的。Flash 让你们也能一起回味。</p>
</div></section>

<section><div class="wrap">
  <h2>Flash 的理念</h2>
  <div class="principes">
    <div><h3>先去经历</h3><p>因为照片要过后才能看到，你不必整晚盯着手机看别人发了什么。先享受当下，之后再回顾。</p></div>
    <div><h3>一起回忆</h3><p>一个周末过后，照片散落在十部手机里。Flash 把它们和大家说过的话汇集在一起。</p></div>
    <div><h3>找回惊喜</h3><p>以前要等好几天才能拿到冲洗好的胶卷。Flash 把这种感觉带了回来：开启日本身就是一个小小的庆祝。</p></div>
    <div><h3>私密而公平</h3><p>没有广告，没有粉丝，没有公开主页。你的回忆只属于在场的人。受邀者始终免费参与。</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <h2>Flash 目前的进展</h2>
  <ol class="tijdlijn">
    <li><strong>应用已经完成</strong><p>活动、邀请码、照片、语录、留言和开启日都已可以使用。</p></li>
    <li class="nu"><strong>现在：与亲友一起测试</strong><p>一小群人在真实活动中使用 Flash 并提供反馈。</p></li>
    <li><strong>根据反馈改进</strong><p>测试者觉得缺少或难用的地方会优先解决。</p></li>
    <li><strong>在 App Store 上线</strong><p>之后，任何拥有 iPhone 的人都可以下载 Flash。</p></li>
  </ol>
</div></section>
''')

# ───────────────────────────── Over mij ─────────────────────────────

P["nl"]["over.html"] = ("Over mij – Flash", "Wie Flash maakt en hoe het begon.", f'''
<section><div class="wrap over">
  <figure class="polaroid portret"><img src="images/thom.jpg" alt="Thom, de maker van Flash"><figcaption>Thom<span>maker</span></figcaption></figure>
  <div>
    <h1>Hoi, ik ben Thom</h1>
    <p class="inleiding">Ik ben student Bouwkunde en Flash is mijn eigen project, naast mijn studie.</p>
    <h2 style="margin-top:40px">Hoe Flash begon</h2>
    <p>Na elke verjaardag, vakantie of feest hetzelfde verhaal: iedereen heeft foto's, maar ze komen nooit bij elkaar. Ze blijven verspreid over telefoons en groepsapps, en na een week kijkt niemand er meer naar.</p>
    <p>Ik wilde zelf een app bouwen en koos het idee dat mij het leukst leek: een gedeelde herinneringencapsule. Samen vullen, pas later openen. Daaruit is Flash ontstaan.</p>
    <h2 style="margin-top:40px">Wat ik van je wil horen</h2>
    <p>Flash wordt nu getest door vrienden en familie. Werkt iets niet, mis je iets of heb je een idee? Mail me op <a href="mailto:{EMAIL}">{EMAIL}</a>. Elke tip helpt om Flash beter te maken.</p>
  </div>
</div></section>
''')

P["en"]["over.html"] = ("About me – Flash", "Who makes Flash and how it started.", f'''
<section><div class="wrap over">
  <figure class="polaroid portret"><img src="images/thom.jpg" alt="Thom, the maker of Flash"><figcaption>Thom<span>maker</span></figcaption></figure>
  <div>
    <h1>Hi, I'm Thom</h1>
    <p class="inleiding">I study Building Engineering, and Flash is my own project alongside my studies.</p>
    <h2 style="margin-top:40px">How Flash started</h2>
    <p>After every birthday, holiday or party it's the same story: everyone has photos, but they never end up in one place. They stay scattered across phones and group chats, and after a week nobody looks at them anymore.</p>
    <p>I wanted to build an app myself and chose the idea I liked most: a shared memory capsule. Fill it together, open it later. That's how Flash was born.</p>
    <h2 style="margin-top:40px">What I'd love to hear from you</h2>
    <p>Flash is currently being tested by friends and family. Something not working, missing something, or have an idea? Email me at <a href="mailto:{EMAIL}">{EMAIL}</a>. Every tip helps make Flash better.</p>
  </div>
</div></section>
''')

P["zh"]["over.html"] = ("关于我 – Flash", "Flash 的开发者是谁，以及它是怎么开始的。", f'''
<section><div class="wrap over">
  <figure class="polaroid portret"><img src="images/thom.jpg" alt="Thom，Flash 的开发者"><figcaption>Thom<span>开发者</span></figcaption></figure>
  <div>
    <h1>你好，我是 Thom</h1>
    <p class="inleiding">我是一名建筑工程专业的学生，Flash 是我在学业之余的个人项目。</p>
    <h2 style="margin-top:40px">Flash 的由来</h2>
    <p>每次生日、旅行或派对之后都是同样的情况：每个人都拍了照片，但它们从来没有汇集到一起。照片散落在各自的手机和群聊里，一周之后就再也没人看了。</p>
    <p>我想自己开发一个应用，于是选了我最喜欢的点子：一个共享的回忆胶囊。一起填满，以后再打开。Flash 就这样诞生了。</p>
    <h2 style="margin-top:40px">我想听听你的想法</h2>
    <p>Flash 目前正在由亲友测试。有什么不好用、缺少什么功能，或者有新点子？请发邮件给我：<a href="mailto:{EMAIL}">{EMAIL}</a>。每一条建议都能让 Flash 变得更好。</p>
  </div>
</div></section>
''')

# ───────────────────────────── Support ─────────────────────────────

P["nl"]["support.html"] = ("Support – Flash", "Hulp en contact voor Flash.", f'''
<section><div class="wrap smal tekst">
  <h1>Support</h1>
  <p class="inleiding">Hulp nodig bij Flash? Hier vind je de antwoorden op de meest gestelde vragen.</p>
  <h2>Hoe doe ik mee met een evenement?</h2>
  <p>Vraag de maker om een code. Tik in Flash op meedoen en vul de code in. Met een deelnemerscode kun je herinneringen toevoegen; met een kijkcode zie je alleen het eindresultaat.</p>
  <h2>Waarom zie ik de foto's van anderen niet?</h2>
  <p>Het evenement is nog verzegeld. Je ziet alleen wat je zelf hebt toegevoegd. Op de openingsdag zie je alles.</p>
  <h2>Ik ben mijn wachtwoord kwijt</h2>
  <p>Mail naar het adres hieronder vanaf het e-mailadres van je account. Je krijgt dan een link om een nieuw wachtwoord te kiezen.</p>
  <h2>Hoe verwijder ik mijn account?</h2>
  <p>In de app, via je profiel. Je account, je herinneringen en de evenementen die jij hebt gemaakt worden dan verwijderd. Lees meer in het <a href="privacy.html">privacybeleid</a>.</p>
  <h2>Contact</h2>
  <p>Mail naar <a href="mailto:{EMAIL}">{EMAIL}</a>. Je krijgt meestal binnen twee dagen antwoord.</p>
</div></section>
''')

P["en"]["support.html"] = ("Support – Flash", "Help and contact for Flash.", f'''
<section><div class="wrap smal tekst">
  <h1>Support</h1>
  <p class="inleiding">Need help with Flash? Here you'll find answers to the most frequently asked questions.</p>
  <h2>How do I join an event?</h2>
  <p>Ask the creator for a code. In Flash, tap join and enter the code. With a participant code you can add memories; with a viewer code you only see the end result.</p>
  <h2>Why can't I see other people's photos?</h2>
  <p>The event is still sealed. You only see what you added yourself. On the opening day you'll see everything.</p>
  <h2>I forgot my password</h2>
  <p>Email the address below from your account's email address. You'll then get a link to choose a new password.</p>
  <h2>How do I delete my account?</h2>
  <p>In the app, via your profile. Your account, your memories and the events you created will then be deleted. Read more in the <a href="privacy-en.html">privacy policy</a>.</p>
  <h2>Contact</h2>
  <p>Email <a href="mailto:{EMAIL}">{EMAIL}</a>. You'll usually get a reply within two days.</p>
</div></section>
''')

P["zh"]["support.html"] = ("支持 – Flash", "Flash 的帮助与联系方式。", f'''
<section><div class="wrap smal tekst">
  <h1>支持</h1>
  <p class="inleiding">使用 Flash 时需要帮助？这里有常见问题的解答。</p>
  <h2>如何加入活动？</h2>
  <p>向活动创建者索取邀请码。在 Flash 中点击“加入”并输入邀请码。使用参与者邀请码可以添加回忆；使用观看者邀请码只能看到最终结果。</p>
  <h2>为什么我看不到别人的照片？</h2>
  <p>活动仍处于封存状态。你只能看到自己添加的内容。到了开启日，你就能看到全部。</p>
  <h2>我忘记了密码</h2>
  <p>请用你账户的电子邮箱发邮件到下面的地址。你会收到一个设置新密码的链接。</p>
  <h2>如何删除我的账户？</h2>
  <p>在应用中通过你的个人资料操作。你的账户、你的回忆以及你创建的活动都会被删除。详情请阅读<a href="privacy-zh.html">隐私政策</a>。</p>
  <h2>联系我们</h2>
  <p>发送邮件至 <a href="mailto:{EMAIL}">{EMAIL}</a>。通常会在两天内回复。</p>
</div></section>
''')

# ───────────────────────────── Frans ─────────────────────────────

P["fr"]["index.html"] = ("Application Flash – l'appareil photo jetable partagé pour tes événements",
"Flash est une application iPhone : un appareil photo jetable partagé pour ton anniversaire, ton voyage ou ta fête. Chacun ajoute des photos, des citations et des messages, et tout reste scellé jusqu'au jour de l'ouverture.", f'''
<div class="wrap held">
  <div>
    <span class="status">En test avec les amis et la famille</span>
    <h1>Tout le monde prend des photos. Tu découvres tout plus tard.</h1>
    <p class="inleiding">Flash est un appareil photo jetable partagé pour ton anniversaire, ton voyage ou ta fête. Chacun ajoute des photos, des citations et des messages, et tout reste scellé jusqu'au jour où l'événement s'ouvre.</p>
    <div class="knoppen"><a class="knop vol" href="voorbeeld-fr.html">Voir un exemple</a><a class="knop rand" href="#zo-werkt-het">Comment ça marche</a></div>
  </div>
  <div class="stapel" aria-hidden="true">
    {foto("kampvuur_maken","Feu de camp au bord de l'eau","Noor","","fr")}
    {foto("wandelen","Perdus, mais ensemble","Sam","","fr")}
    {foto("kampvuur","Café près de la tente","Lars","","fr")}
  </div>
</div>

<section id="zo-werkt-het"><div class="wrap">
  <h2>Comment ça marche</h2>
  <ol class="stappen">
    <li><h3>Crée un événement</h3><p>Donne-lui un nom et choisis le jour où il s'ouvre : demain, dans un mois ou dans un an.</p></li>
    <li><h3>Invite tes amis</h3><p>Partage un code. Les participants ajoutent des photos, des citations et des messages ; les spectateurs voient seulement le résultat final.</p></li>
    <li><h3>Ouvrez-le ensemble</h3><p>Le jour de l'ouverture, tout le monde reçoit une notification et vous découvrez enfin tout ce que les autres ont capturé.</p></li>
  </ol>
</div></section>

<section><div class="wrap">
  <h2>Pourquoi Flash est différent</h2>
  <div class="kenmerken">
    <div><h3>Scellé jusqu'à l'ouverture</h3><p>Tu ne vois que ce que tu ajoutes toi-même. Le reste reste une surprise, comme une pellicule qui doit encore être développée.</p></div>
    <div><h3>Seulement ton groupe</h3><p>Un événement compte 15 personnes maximum. Personne d'autre ne peut le trouver ni le voir.</p></div>
    <div><h3>Plus que des photos</h3><p>Garde aussi ce qui a été dit, ou écris un message à vous-mêmes dans le futur.</p></div>
    <div><h3>Directement dans ta galerie</h3><p>Quand l'événement s'ouvre, Flash met toutes les photos dans un album sur ton téléphone.</p></div>
  </div>
</div></section>
''')

P["fr"]["voorbeeld.html"] = ("Exemple – Flash", "Voici à quoi ressemble un événement ouvert dans Flash.", f'''
<section><div class="wrap">
  <h1>Voici à quoi ressemble un événement ouvert</h1>
  <p class="inleiding">Voici un exemple avec des prénoms inventés : un week-end entre amis, le jour où il s'ouvre.</p>
</div></section>

<section><div class="wrap">
  <h2>Avant et après l'ouverture</h2>
  <div class="voorna">
    <div class="scherm"><span class="label dicht">Scellé</span><h3>Week-end dans les Ardennes</h3><div class="teller">3j 14h 32m</div><p>Tu ne vois que tes 6 propres photos. Il contient déjà 41 souvenirs de 9 amis.</p></div>
    <div class="scherm"><span class="label">Ouvert</span><h3>Week-end dans les Ardennes</h3><div class="teller">41</div><p>souvenirs de 9 amis, maintenant visibles par tous et enregistrés dans la galerie de chacun.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="evenement-kop"><div><span class="label">Ouvert le 14 juin 2026</span><h2 style="margin:0">Week-end dans les Ardennes</h2></div><p class="waarschuwing" style="margin:0">41 souvenirs de 9 amis</p></div>
  <div class="muur">
    {foto("bergen","La vue du premier jour","Sam","Collines boisées des Ardennes","fr")}
    <div class="quote"><blockquote>Je suis sûr que ce chemin est un raccourci.</blockquote><p>Lars, deux heures avant qu'on se perde</p></div>
    {foto("wandelen","Perdus, mais ensemble","Thom","Deux amis avec des sacs à dos dans la forêt","fr")}
    {foto("kampvuur","Café près de la tente","Noor","Amis autour d'un feu de camp près d'une tente","fr")}
    {foto("kampvuur_maken","Feu de camp au bord de l'eau","Mila","Amis autour d'un feu de camp au coucher du soleil","fr")}
    <div class="bericht"><strong>Message pour le futur</strong><p>Si vous lisez ceci : avons-nous déjà prévu le prochain week-end ? Sinon, faites-le maintenant.</p><small>de Jesse</small></div>
    {foto("feest","L'anniversaire de Sam à minuit","Jesse","Gâteau d'anniversaire avec des bougies","fr")}
    {foto("strand","Un dernier tour au bord de l'eau dimanche","Sam","Dessin d'une plage avec un parasol","fr")}
    <div class="quote"><blockquote>Encore une partie et on va dormir.</blockquote><p>Noor, à trois heures et demie du matin</p></div>
    {foto("stad","Retour en ville","Mila","Dessin d'une ville la nuit","fr")}
  </div>
</div></section>

<section><div class="wrap">
  <div class="evenement-kop"><div><span class="label">Ouvert le 1er avril 2026</span><h2 style="margin:0">Vacances au ski 2026</h2></div><p class="waarschuwing" style="margin:0">58 souvenirs de 7 amis</p></div>
  <div class="muur">
    {foto("skivakantie-2026-1","Prêt pour la première descente","Lars","Skieur sur la piste avec des montagnes en arrière-plan","fr")}
    <div class="quote"><blockquote>Une piste rouge ? C'est juste une bleue d'une autre couleur.</blockquote><p>Sam, juste avant sa première chute</p></div>
    {foto("skivakantie-2026-2","Profiter de la vue","Noor","Skieur regardant des sommets enneigés","fr")}
    {foto("skivakantie-2026-3","Ciel bleu, neige fraîche","Thom","Piste de ski avec remontées et montagnes","fr")}
    <div class="bericht"><strong>Message pour le futur</strong><p>Même semaine l'année prochaine ? Personne n'a le droit de dire qu'il n'a pas le temps.</p><small>de Mila</small></div>
    {foto("skivakantie-2026-4","Pause déjeuner près du télésiège","Jesse","Skis et bâtons plantés dans la neige près d'un téléski","fr")}
  </div>
</div></section>

<section><div class="wrap">
  <div class="evenement-kop"><div><span class="label">Ouvert le 1er janvier 2026</span><h2 style="margin:0">Voyage en Indonésie 2025</h2></div><p class="waarschuwing" style="margin:0">73 souvenirs de 12 compagnons de voyage</p></div>
  <div class="muur">
    {foto("vakantie-indonesie-2025-1","Rizières près du village","Mila","Rizières devant un village avec des palmiers","fr")}
    {foto("vakantie-indonesie-2025-3","Vue sur la plaine du Bromo","Lars","Volcan et plaine derrière des arbres tropicaux","fr")}
    <div class="quote"><blockquote>Encore un temple et après, promis, on va à la piscine.</blockquote><p>Noor, il y a trois temples</p></div>
    {foto("vakantie-indonesie-2025-5","Photo de groupe à Borobudur","Thom","Groupe de voyageurs près des stupas de Borobudur","fr")}
    {foto("vakantie-indonesie-2025-2","Vue sur la jungle","Sam","Palmiers et rizières en terrasses dans la jungle","fr")}
    <div class="bericht"><strong>Message pour le futur</strong><p>Vous vous souvenez de la chaleur ? Gardez ces photos pour une froide journée de janvier.</p><small>de Jesse</small></div>
    {foto("vakantie-indonesie-2025-4","Se rafraîchir dans la piscine","Noor","Piscine entre les palmiers","fr")}
  </div>
  <p class="waarschuwing">Les photos ci-dessus sont des photos d'exemple. Dans l'application, tu verras les vraies photos de ton groupe.</p>
</div></section>
''')

P["fr"]["visie.html"] = ("Vision – Flash", "Pourquoi Flash existe et où va le projet.", '''
<section><div class="wrap">
  <h1>Vision</h1>
  <p class="inleiding">Pourquoi Flash existe et où va le projet.</p>
</div></section>

<section><div class="wrap">
  <p class="uitspraak">Les plus beaux moments se vivent ensemble. Flash fait en sorte que vous les revoyiez ensemble aussi.</p>
</div></section>

<section><div class="wrap">
  <h2>Ce que défend Flash</h2>
  <div class="principes">
    <div><h3>Vivre d'abord</h3><p>Comme tu ne vois les photos que plus tard, tu n'as pas besoin de regarder ton téléphone toute la soirée pour voir ce que les autres publient. Tu vis le moment et tu le revois plus tard.</p></div>
    <div><h3>Se souvenir ensemble</h3><p>Après un week-end, les photos sont éparpillées sur dix téléphones. Flash les rassemble, avec ce qui a été dit.</p></div>
    <div><h3>Le retour de la surprise</h3><p>Avant, on attendait des jours le développement de sa pellicule. Flash fait revivre ce sentiment : le jour de l'ouverture est une petite fête en soi.</p></div>
    <div><h3>Privé et honnête</h3><p>Pas de publicité, pas d'abonnés, pas de profils publics. Tes souvenirs sont uniquement pour les personnes qui étaient là. Les invités participent toujours gratuitement.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <h2>Où en est Flash</h2>
  <ol class="tijdlijn">
    <li><strong>L'application est construite</strong><p>Les événements, les codes d'invitation, les photos, les citations, les messages et le jour de l'ouverture fonctionnent.</p></li>
    <li class="nu"><strong>Maintenant : tests avec les amis et la famille</strong><p>Un petit groupe utilise Flash lors de vrais événements et donne son avis.</p></li>
    <li><strong>Améliorer grâce aux retours</strong><p>Ce qui manque aux testeurs ou ce qu'ils trouvent difficile est corrigé en premier.</p></li>
    <li><strong>Lancement sur l'App Store</strong><p>Ensuite, tout le monde avec un iPhone pourra télécharger Flash.</p></li>
  </ol>
</div></section>
''')

P["fr"]["over.html"] = ("À propos – Flash", "Qui fait Flash et comment tout a commencé.", f'''
<section><div class="wrap over">
  <figure class="polaroid portret"><img src="images/thom.jpg" alt="Thom, le créateur de Flash"><figcaption>Thom<span>créateur</span></figcaption></figure>
  <div>
    <h1>Salut, moi c'est Thom</h1>
    <p class="inleiding">J'étudie le génie civil et la construction, et Flash est mon propre projet, à côté de mes études.</p>
    <h2 style="margin-top:40px">Comment Flash a commencé</h2>
    <p>Après chaque anniversaire, vacances ou fête, c'est la même histoire : tout le monde a des photos, mais elles ne sont jamais réunies. Elles restent éparpillées sur les téléphones et dans les groupes de discussion, et au bout d'une semaine, plus personne ne les regarde.</p>
    <p>Je voulais créer moi-même une application et j'ai choisi l'idée qui me plaisait le plus : une capsule de souvenirs partagée. La remplir ensemble, l'ouvrir plus tard. C'est ainsi qu'est né Flash.</p>
    <h2 style="margin-top:40px">Ce que j'aimerais savoir</h2>
    <p>Flash est en cours de test par des amis et la famille. Quelque chose ne fonctionne pas, il te manque quelque chose ou tu as une idée ? Écris-moi à <a href="mailto:{EMAIL}">{EMAIL}</a>. Chaque conseil aide à améliorer Flash.</p>
  </div>
</div></section>
''')

P["fr"]["support.html"] = ("Aide – Flash", "Aide et contact pour Flash.", f'''
<section><div class="wrap smal tekst">
  <h1>Aide</h1>
  <p class="inleiding">Besoin d'aide avec Flash ? Tu trouveras ici les réponses aux questions les plus fréquentes.</p>
  <h2>Comment rejoindre un événement ?</h2>
  <p>Demande un code au créateur. Dans Flash, appuie sur rejoindre et saisis le code. Avec un code participant, tu peux ajouter des souvenirs ; avec un code spectateur, tu vois seulement le résultat final.</p>
  <h2>Pourquoi je ne vois pas les photos des autres ?</h2>
  <p>L'événement est encore scellé. Tu ne vois que ce que tu as ajouté toi-même. Le jour de l'ouverture, tu verras tout.</p>
  <h2>J'ai oublié mon mot de passe</h2>
  <p>Écris à l'adresse ci-dessous depuis l'adresse e-mail de ton compte. Tu recevras un lien pour choisir un nouveau mot de passe.</p>
  <h2>Comment supprimer mon compte ?</h2>
  <p>Dans l'application, via ton profil. Ton compte, tes souvenirs et les événements que tu as créés seront alors supprimés. Pour en savoir plus, lis la <a href="privacy-fr.html">politique de confidentialité</a>.</p>
  <h2>Contact</h2>
  <p>Écris à <a href="mailto:{EMAIL}">{EMAIL}</a>. Tu recevras généralement une réponse sous deux jours.</p>
</div></section>
''')

# ───────────────────────────── Spaans ─────────────────────────────

P["es"]["index.html"] = ("App Flash – la cámara desechable compartida para tus eventos",
"Flash es una app para iPhone: una cámara desechable compartida para tu cumpleaños, viaje o fiesta. Todos añaden fotos, frases y mensajes, y todo queda sellado hasta el día de la apertura.", f'''
<div class="wrap held">
  <div>
    <span class="status">En pruebas con amigos y familia</span>
    <h1>Todos hacen fotos. Lo ves todo más tarde.</h1>
    <p class="inleiding">Flash es una cámara desechable compartida para tu cumpleaños, viaje o fiesta. Todos añaden fotos, frases y mensajes, y todo queda sellado hasta el día en que se abre el evento.</p>
    <div class="knoppen"><a class="knop vol" href="voorbeeld-es.html">Ver un ejemplo</a><a class="knop rand" href="#zo-werkt-het">Cómo funciona</a></div>
  </div>
  <div class="stapel" aria-hidden="true">
    {foto("kampvuur_maken","Hoguera junto al agua","Noor","","es")}
    {foto("wandelen","Perdidos, pero juntos","Sam","","es")}
    {foto("kampvuur","Café junto a la tienda","Lars","","es")}
  </div>
</div>

<section id="zo-werkt-het"><div class="wrap">
  <h2>Cómo funciona</h2>
  <ol class="stappen">
    <li><h3>Crea un evento</h3><p>Ponle un nombre y elige el día en que se abre: mañana, dentro de un mes o dentro de un año.</p></li>
    <li><h3>Invita a tus amigos</h3><p>Comparte un código. Los participantes añaden fotos, frases y mensajes; los espectadores solo ven el resultado final.</p></li>
    <li><h3>Abridlo juntos</h3><p>El día de la apertura, todos reciben una notificación y por fin veis todo lo que los demás han capturado.</p></li>
  </ol>
</div></section>

<section><div class="wrap">
  <h2>Por qué Flash es diferente</h2>
  <div class="kenmerken">
    <div><h3>Sellado hasta la apertura</h3><p>Solo ves lo que añades tú. El resto sigue siendo una sorpresa, como un carrete que aún hay que revelar.</p></div>
    <div><h3>Solo tu grupo</h3><p>Un evento tiene como máximo 15 personas. Nadie más puede encontrarlo ni verlo.</p></div>
    <div><h3>Más que fotos</h3><p>Guarda también lo que se dijo, o escribe un mensaje a vuestro yo del futuro.</p></div>
    <div><h3>Directo a tu galería</h3><p>Cuando se abre el evento, Flash pone todas las fotos en un álbum de tu teléfono.</p></div>
  </div>
</div></section>
''')

P["es"]["voorbeeld.html"] = ("Ejemplo – Flash", "Así es un evento abierto en Flash.", f'''
<section><div class="wrap">
  <h1>Así es un evento abierto</h1>
  <p class="inleiding">Este es un ejemplo con nombres inventados: un fin de semana con amigos, el día en que se abre.</p>
</div></section>

<section><div class="wrap">
  <h2>Antes y después de la apertura</h2>
  <div class="voorna">
    <div class="scherm"><span class="label dicht">Sellado</span><h3>Fin de semana en las Ardenas</h3><div class="teller">3d 14h 32m</div><p>Solo ves tus 6 fotos. Ya contiene 41 recuerdos de 9 amigos.</p></div>
    <div class="scherm"><span class="label">Abierto</span><h3>Fin de semana en las Ardenas</h3><div class="teller">41</div><p>recuerdos de 9 amigos, ahora visibles para todos y guardados en la galería de cada uno.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="evenement-kop"><div><span class="label">Abierto el 14 de junio de 2026</span><h2 style="margin:0">Fin de semana en las Ardenas</h2></div><p class="waarschuwing" style="margin:0">41 recuerdos de 9 amigos</p></div>
  <div class="muur">
    {foto("bergen","Las vistas del primer día","Sam","Colinas boscosas de las Ardenas","es")}
    <div class="quote"><blockquote>Estoy seguro de que este camino es un atajo.</blockquote><p>Lars, dos horas antes de perdernos</p></div>
    {foto("wandelen","Perdidos, pero juntos","Thom","Dos amigos con mochilas en el bosque","es")}
    {foto("kampvuur","Café junto a la tienda","Noor","Amigos alrededor de una hoguera junto a una tienda","es")}
    {foto("kampvuur_maken","Hoguera junto al agua","Mila","Amigos alrededor de una hoguera al atardecer","es")}
    <div class="bericht"><strong>Mensaje para el futuro</strong><p>Si estáis leyendo esto: ¿ya hemos planeado el próximo fin de semana? Si no, hacedlo ahora.</p><small>de Jesse</small></div>
    {foto("feest","El cumpleaños de Sam a medianoche","Jesse","Tarta de cumpleaños con velas","es")}
    {foto("strand","Una última vuelta al agua el domingo","Sam","Dibujo de una playa con una sombrilla","es")}
    <div class="quote"><blockquote>Una partida más y nos vamos a dormir.</blockquote><p>Noor, a las tres y media de la madrugada</p></div>
    {foto("stad","De vuelta en la ciudad","Mila","Dibujo de una ciudad de noche","es")}
  </div>
</div></section>

<section><div class="wrap">
  <div class="evenement-kop"><div><span class="label">Abierto el 1 de abril de 2026</span><h2 style="margin:0">Viaje de esquí 2026</h2></div><p class="waarschuwing" style="margin:0">58 recuerdos de 7 amigos</p></div>
  <div class="muur">
    {foto("skivakantie-2026-1","Listo para la primera bajada","Lars","Esquiador en la pista con montañas al fondo","es")}
    <div class="quote"><blockquote>¿Pista roja? Si es una azul de otro color.</blockquote><p>Sam, justo antes de su primera caída</p></div>
    {foto("skivakantie-2026-2","Disfrutando de las vistas","Noor","Esquiador mirando cumbres nevadas","es")}
    {foto("skivakantie-2026-3","Cielo azul, nieve fresca","Thom","Pista de esquí con remontes y montañas","es")}
    <div class="bericht"><strong>Mensaje para el futuro</strong><p>¿La misma semana el año que viene? Nadie puede decir que no tiene tiempo.</p><small>de Mila</small></div>
    {foto("skivakantie-2026-4","Pausa para comer junto al remonte","Jesse","Esquís y bastones en la nieve junto a un remonte","es")}
  </div>
</div></section>

<section><div class="wrap">
  <div class="evenement-kop"><div><span class="label">Abierto el 1 de enero de 2026</span><h2 style="margin:0">Viaje a Indonesia 2025</h2></div><p class="waarschuwing" style="margin:0">73 recuerdos de 12 compañeros de viaje</p></div>
  <div class="muur">
    {foto("vakantie-indonesie-2025-1","Arrozales junto al pueblo","Mila","Arrozales delante de un pueblo con palmeras","es")}
    {foto("vakantie-indonesie-2025-3","Vistas de la llanura del Bromo","Lars","Volcán y llanura detrás de árboles tropicales","es")}
    <div class="quote"><blockquote>Un templo más y luego, de verdad, nos vamos a la piscina.</blockquote><p>Noor, hace tres templos</p></div>
    {foto("vakantie-indonesie-2025-5","Foto de grupo en Borobudur","Thom","Grupo de viajeros junto a las estupas de Borobudur","es")}
    {foto("vakantie-indonesie-2025-2","Vistas sobre la selva","Sam","Palmeras y terrazas de arroz en la selva","es")}
    <div class="bericht"><strong>Mensaje para el futuro</strong><p>¿Os acordáis del calor que hacía? Guardad estas fotos para un día frío de enero.</p><small>de Jesse</small></div>
    {foto("vakantie-indonesie-2025-4","Refrescándonos en la piscina","Noor","Piscina entre palmeras","es")}
  </div>
  <p class="waarschuwing">Las fotos de arriba son fotos de ejemplo. En la app verás las fotos reales de tu grupo.</p>
</div></section>
''')

P["es"]["visie.html"] = ("Visión – Flash", "Por qué existe Flash y hacia dónde va.", '''
<section><div class="wrap">
  <h1>Visión</h1>
  <p class="inleiding">Por qué existe Flash y hacia dónde va.</p>
</div></section>

<section><div class="wrap">
  <p class="uitspraak">Los mejores momentos se viven juntos. Flash hace que también los volváis a ver juntos.</p>
</div></section>

<section><div class="wrap">
  <h2>Lo que defiende Flash</h2>
  <div class="principes">
    <div><h3>Primero vivirlo</h3><p>Como solo ves las fotos más tarde, no tienes que pasarte la noche mirando el móvil para ver qué publican los demás. Vives el momento y lo recuerdas después.</p></div>
    <div><h3>Recordar juntos</h3><p>Después de un fin de semana, las fotos están repartidas en diez móviles. Flash las reúne, junto con lo que se dijo.</p></div>
    <div><h3>Vuelve la sorpresa</h3><p>Antes esperabas días a que revelaran tu carrete. Flash recupera esa sensación: el día de la apertura es una pequeña fiesta en sí misma.</p></div>
    <div><h3>Privado y honesto</h3><p>Sin anuncios, sin seguidores, sin perfiles públicos. Tus recuerdos son solo para las personas que estuvieron allí. Los invitados siempre participan gratis.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <h2>En qué punto está Flash</h2>
  <ol class="tijdlijn">
    <li><strong>La app está hecha</strong><p>Los eventos, los códigos de invitación, las fotos, las frases, los mensajes y el día de la apertura funcionan.</p></li>
    <li class="nu"><strong>Ahora: pruebas con amigos y familia</strong><p>Un grupo pequeño usa Flash en eventos reales y da su opinión.</p></li>
    <li><strong>Mejorar con las opiniones</strong><p>Lo que echan en falta los probadores o les resulta difícil se soluciona primero.</p></li>
    <li><strong>Lanzamiento en la App Store</strong><p>Después, cualquiera con un iPhone podrá descargar Flash.</p></li>
  </ol>
</div></section>
''')

P["es"]["over.html"] = ("Sobre mí – Flash", "Quién hace Flash y cómo empezó.", f'''
<section><div class="wrap over">
  <figure class="polaroid portret"><img src="images/thom.jpg" alt="Thom, el creador de Flash"><figcaption>Thom<span>creador</span></figcaption></figure>
  <div>
    <h1>Hola, soy Thom</h1>
    <p class="inleiding">Estudio Ingeniería de la Edificación y Flash es mi propio proyecto, además de mis estudios.</p>
    <h2 style="margin-top:40px">Cómo empezó Flash</h2>
    <p>Después de cada cumpleaños, viaje o fiesta pasa lo mismo: todos tienen fotos, pero nunca se juntan. Se quedan repartidas en móviles y chats de grupo, y al cabo de una semana nadie las vuelve a mirar.</p>
    <p>Quería crear una app yo mismo y elegí la idea que más me gustaba: una cápsula de recuerdos compartida. Llenarla juntos, abrirla más tarde. Así nació Flash.</p>
    <h2 style="margin-top:40px">Lo que me gustaría saber</h2>
    <p>Ahora mismo Flash lo están probando amigos y familia. ¿Algo no funciona, echas algo en falta o tienes una idea? Escríbeme a <a href="mailto:{EMAIL}">{EMAIL}</a>. Cada sugerencia ayuda a mejorar Flash.</p>
  </div>
</div></section>
''')

P["es"]["support.html"] = ("Ayuda – Flash", "Ayuda y contacto de Flash.", f'''
<section><div class="wrap smal tekst">
  <h1>Ayuda</h1>
  <p class="inleiding">¿Necesitas ayuda con Flash? Aquí tienes las respuestas a las preguntas más frecuentes.</p>
  <h2>¿Cómo me uno a un evento?</h2>
  <p>Pide un código al creador. En Flash, toca unirse e introduce el código. Con un código de participante puedes añadir recuerdos; con un código de espectador solo ves el resultado final.</p>
  <h2>¿Por qué no veo las fotos de los demás?</h2>
  <p>El evento sigue sellado. Solo ves lo que has añadido tú. El día de la apertura lo verás todo.</p>
  <h2>He olvidado mi contraseña</h2>
  <p>Escribe a la dirección de abajo desde el correo de tu cuenta. Recibirás un enlace para elegir una nueva contraseña.</p>
  <h2>¿Cómo elimino mi cuenta?</h2>
  <p>En la app, desde tu perfil. Se eliminarán tu cuenta, tus recuerdos y los eventos que creaste. Más información en la <a href="privacy-es.html">política de privacidad</a>.</p>
  <h2>Contacto</h2>
  <p>Escribe a <a href="mailto:{EMAIL}">{EMAIL}</a>. Normalmente respondemos en dos días.</p>
</div></section>
''')

# ───────────────────────────── Bouwen ─────────────────────────────

for taal in TALEN:
    for bestand, (titel, beschrijving, inhoud) in P[taal].items():
        open(naam(bestand, taal), "w", encoding="utf-8").write(pagina(bestand, taal, titel, inhoud, beschrijving))

# Privacybeleid en voorwaarden: de bestaande tekst (uit <main>) opnieuw in de kop en voet van de juiste taal.
# De losse regel "Nederlands · English · 中文" valt weg; daarvoor is nu de taalknop rechtsboven.
for bestand in ["privacy.html", "voorwaarden.html"]:
    for taal in TALEN:
        n = naam(bestand, taal)
        if not os.path.exists(n):
            continue
        oud = open(n, encoding="utf-8").read()
        main = re.search(r"<main>\n?(.*?)\n?</main>", oud, re.S)
        titel = re.search(r"<title>(.*?)</title>", oud, re.S)
        besch = re.search(r'<meta name="description" content="(.*?)">', oud, re.S)
        if not (main and titel and besch):
            print("overgeslagen:", n)
            continue
        inhoud = re.sub(r'\n?<p class="klein"><a href="[\w-]+\.html">Nederlands</a>.*?</p>', "", main.group(1), flags=re.S)
        open(n, "w", encoding="utf-8").write(pagina(bestand, taal, titel.group(1), inhoud, besch.group(1)))

# Sitemap met alle talen
regels = []
for bestand in ["index.html", "voorbeeld.html", "visie.html", "over.html", "support.html", "privacy.html", "voorwaarden.html"]:
    for taal in TALEN:
        regels.append(f"  <url><loc>{url(bestand, taal)}</loc><lastmod>2026-11-09</lastmod></url>")
open("sitemap.xml", "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(regels) + "\n</urlset>\n")
print("klaar")
