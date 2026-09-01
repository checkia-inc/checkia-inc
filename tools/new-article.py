#!/usr/bin/env python3
"""Génère un nouvel article du blog à partir du gabarit de référence.

Usage :
  python3 tools/new-article.py <serie> <slug> "Titre de l'article" --format video|texte|temoignage

  <serie>  : nouveautes-produit | futur-de-l-audit | vie-de-l-entreprise | temoignages-clients
  <slug>   : court, minuscules, tirets, sans accents (ex. cloture-des-comptes-ia)
  --format : OBLIGATOIRE — toujours demander à l'auteur le type d'article :
             video      = article complet vidéo + texte ;
             texte      = article écrit seul, sans vidéo ;
             temoignage = témoignage client (vidéo).

L'article est créé en `noindex` avec les placeholders du gabarit. Suivre la
checklist affichée, puis `python3 tools/check-seo.py` avant publication.
"""

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://checkia.fr"

SERIES = {
    "nouveautes-produit": "Nouveautés produit",
    "futur-de-l-audit": "Le futur de l'audit",
    "vie-de-l-entreprise": "Vie de l'entreprise",
    "temoignages-clients": "Témoignages clients",
}

TEMPLATES = {
    "video": ("futur-de-l-audit", "ia-commissariat-aux-comptes"),
    "texte": ("vie-de-l-entreprise", "modele-texte"),
    "temoignage": ("temoignages-clients", "modele-temoignage"),
}

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]


def main():
    argv = sys.argv[1:]
    args, fmt = [], None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--format"):
            if "=" in a:
                fmt = a.split("=", 1)[1]
            else:
                i += 1
                fmt = argv[i] if i < len(argv) else None
        else:
            args.append(a)
        i += 1
    if len(args) < 3:
        sys.exit(__doc__)
    if fmt not in TEMPLATES:
        sys.exit("--format est obligatoire : video, texte ou temoignage.\n"
                 "Toujours demander à l'auteur quel type d'article il veut publier.")
    serie, slug, title = args[0], args[1], args[2]

    if serie not in SERIES:
        sys.exit(f"Série inconnue : {serie}. Choix : {', '.join(SERIES)}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        sys.exit("Slug invalide : minuscules, chiffres et tirets uniquement, sans accents.")

    dest = ROOT / "blog" / serie / slug
    if dest.exists():
        sys.exit(f"{dest} existe déjà.")

    src_serie, src_slug = TEMPLATES[fmt]
    src = ROOT / "blog" / src_serie / src_slug / "index.html"
    text = src.read_text(encoding="utf-8")

    # URLs et fil d'Ariane
    text = text.replace(f"/blog/{src_serie}/{src_slug}/", f"/blog/{serie}/{slug}/")
    text = text.replace(f"/blog/{src_serie}/", f"/blog/{serie}/")
    text = text.replace(SERIES[src_serie], SERIES[serie])

    # Dates du jour
    today = date.today()
    iso = today.isoformat()
    text = re.sub(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}",
                  f"{iso}T09:00:00+02:00", text)
    text = re.sub(r'(<time datetime="[^"]*">)[^<]*(</time>)',
                  rf"\g<1>{today.day} {MOIS[today.month - 1]} {today.year}\g<2>",
                  text, count=1)

    # Rester en noindex tant que l'article n'est pas prêt
    text = re.sub(r'<meta name="robots" content="[^"]*">',
                  '<meta name="robots" content="noindex, nofollow">', text)

    dest.mkdir(parents=True)
    (dest / "index.html").write_text(text, encoding="utf-8")

    print(f"Créé : blog/{serie}/{slug}/index.html (noindex)\n")
    print(f"Titre à intégrer : « {title} »\n")
    print("Checklist avant publication :")
    print("  1. Remplacer titres, description, contenus, FAQ, TLDR (« L'essentiel »).")
    if fmt != "texte":
        print("  2. Vidéo : ID YouTube, durée, chapitres/Clip, miniature, transcription.")
    print("  3. Image OG dédiée 1200×630 dans images/blog/.")
    print("  4. Repasser robots en « index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1 ».")
    print("  5. Cartes : /blog/, page de série (+ ItemList JSON-LD), pagenav/« À lire ensuite » des voisins.")
    print("  6. sitemap.xml (lastmod), blog/feed.xml, llms.txt.")
    print("  7. python3 tools/build-llms.py   (index.md + llms-full.txt)")
    print("  8. python3 tools/check-seo.py    (doit sortir sans erreur)")


if __name__ == "__main__":
    main()
