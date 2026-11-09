# Bouwt alle pagina's met dezelfde kop en voet. Draai: python3 maak.py
import os, re
EMAIL = "flashapp.support05@gmail.com"
PAGINAS = [("index.html","Zo werkt het"),("voorbeeld.html","Voorbeeld"),("visie.html","Visie"),("over.html","Over mij"),("support.html","Support")]

def pagina(bestand, titel, inhoud, beschrijving):
    huidig = ' aria-current="page"'
    links = "".join(f'<a href="{b}"{huidig if b==bestand else ""}>{n}</a>' for b,n in PAGINAS)
    return f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titel}</title>
<meta name="description" content="{beschrijving}">
<meta property="og:title" content="{titel}">
<meta property="og:description" content="{beschrijving}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://thom2005bloem.github.io/flash-app/images/kampvuur_maken.jpg">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header><div class="wrap kop"><a class="merk" href="index.html"><i></i>Flash</a><nav aria-label="Hoofdmenu">{links}</nav></div></header>
<main>
{inhoud}
</main>
<footer><div class="wrap voet"><span>Vragen of feedback? Mail naar <a href="mailto:{EMAIL}">{EMAIL}</a></span><a href="privacy.html">Privacybeleid</a><a href="voorwaarden.html">Voorwaarden</a></div></footer>
</body>
</html>
'''

def foto(img, tekst, van, alt):
    # Echte foto (images/<naam>.jpg) als die er is, anders de tekening (.svg)
    if os.path.exists(f"images/{img}.jpg"):
        ext = "jpg"
    elif os.path.exists(f"images/{img}.svg"):
        ext = "svg"
    else:
        return ""  # geen foto en geen tekening: polaroid weglaten
    return f'<figure class="polaroid"><img src="images/{img}.{ext}" alt="{alt}" loading="lazy"><figcaption>{tekst}<span>van {van}</span></figcaption></figure>'

home = f'''
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
'''

voorbeeld = f'''
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
'''

visie = '''
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
'''

over = '''
<section><div class="wrap over">
  <figure class="polaroid portret"><img src="images/thom.jpg" alt="Thom, de maker van Flash"><figcaption>Thom<span>maker</span></figcaption></figure>
  <div>
    <h1>Hoi, ik ben Thom</h1>
    <p class="inleiding">Ik ben student Bouwkunde en Flash is mijn eigen project, naast mijn studie.</p>
    <h2 style="margin-top:40px">Hoe Flash begon</h2>
    <p>Na elke verjaardag, vakantie of feest hetzelfde verhaal: iedereen heeft foto's, maar ze komen nooit bij elkaar. Ze blijven verspreid over telefoons en groepsapps, en na een week kijkt niemand er meer naar.</p>
    <p>Ik wilde zelf een app bouwen en koos het idee dat mij het leukst leek: een gedeelde herinneringencapsule. Samen vullen, pas later openen. Daaruit is Flash ontstaan.</p>
    <h2 style="margin-top:40px">Wat ik van je wil horen</h2>
    <p>Flash wordt nu getest door vrienden en familie. Werkt iets niet, mis je iets of heb je een idee? Mail me op <a href="mailto:flashapp.support05@gmail.com">flashapp.support05@gmail.com</a>. Elke tip helpt om Flash beter te maken.</p>
  </div>
</div></section>
'''

support = '''
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
  <p>Mail naar <a href="mailto:flashapp.support05@gmail.com">flashapp.support05@gmail.com</a>. Je krijgt meestal binnen twee dagen antwoord.</p>
</div></section>
'''

open("index.html","w").write(pagina("index.html","Flash app – de gedeelde wegwerpcamera voor je evenementen",home,"Flash is een iPhone-app: een gedeelde wegwerpcamera voor je verjaardag, reis of feest. Iedereen voegt foto\'s, quotes en berichten toe en alles blijft verzegeld tot de openingsdag."))
open("voorbeeld.html","w").write(pagina("voorbeeld.html","Voorbeeld – Flash",voorbeeld,"Zo ziet een geopend evenement in Flash eruit."))
open("visie.html","w").write(pagina("visie.html","Visie – Flash",visie,"Waarom Flash bestaat en waar het naartoe gaat."))
open("over.html","w").write(pagina("over.html","Over mij – Flash",over,"Wie Flash maakt en hoe het begon."))
open("support.html","w").write(pagina("support.html","Support – Flash",support,"Hulp en contact voor Flash."))

# privacybeleid: bestaande tekst in de nieuwe opmaak
oud = open("privacy.html").read()
m = re.search(r'<h1>Privacybeleid</h1>(.*?)</div></section>', oud, re.S)
if m:
    body = m.group(1).replace('class="muted"','class="klein"')
    open("privacy.html","w").write(pagina("privacy.html","Privacybeleid – Flash", f'<section><div class="wrap smal tekst"><h1>Privacybeleid</h1>{body}</div></section>',"Privacybeleid van de app Flash."))
print("klaar")
