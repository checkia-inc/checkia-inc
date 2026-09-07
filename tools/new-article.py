#!/usr/bin/env python3
"""Génère un nouvel article du blog à partir du gabarit de référence.

Usage :
  python3 tools/new-article.py <serie> <slug> "Titre de l'article" --format video|texte|temoignage
  python3 tools/new-article.py --brief P014      (série, slug, titre, format, requête, auteur
                                                  et image lus dans content-plan/briefs/)

  <serie>  : nouveautes-produit | futur-de-l-audit | vie-de-l-entreprise | temoignages-clients
  <slug>   : court, minuscules, tirets, sans accents (ex. cloture-des-comptes-ia)
  --format : OBLIGATOIRE — toujours demander à l'auteur le type d'article :
             video      = article complet vidéo + texte ;
             texte      = article écrit seul, sans vidéo ;
             temoignage = témoignage client (vidéo).

L'article est créé en `noindex` avec les placeholders du gabarit et un bloc
`checkia-meta` (format / query / author / og-image) à compléter. Suivre la
checklist affichée, puis `python3 tools/check-seo.py` avant publication.
"""

import html
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


def load_brief(bid):
    """Return the Brief object for <bid> (tools/plan.py is the single reader of briefs)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from plan import find_brief, fold  # noqa: F401  (plan.py has no import side effects)
    return find_brief(bid), fold


def main():
    argv = sys.argv[1:]
    args, fmt, brief_id = [], None, None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--format") or a.startswith("--brief"):
            if "=" in a:
                val = a.split("=", 1)[1]
            else:
                i += 1
                val = argv[i] if i < len(argv) else None
            if a.startswith("--format"):
                fmt = val
            else:
                brief_id = val
        else:
            args.append(a)
        i += 1

    # --brief <id>: the validated brief answers the intake (type, série, slug, titre,
    # requête, auteur, image). Positional arguments still override it.
    brief, fold = (None, None)
    if brief_id:
        brief, fold = load_brief(brief_id)
        btype = brief.get("type")
        if btype not in TEMPLATES:
            sys.exit("Le brief %s est de type « %s » : pas d'article à générer (refresh → modifier "
                     "l'article existant ; linkedin/annuaire → hors site)." % (brief.id, btype))
        if fmt and fmt != btype:
            sys.exit("--format %s contredit le type du brief (%s)." % (fmt, btype))
        fmt = btype
        if brief.get("serie") == "site":
            sys.exit("Le brief %s est une page du site (hors blog) : la créer à la main avec la checklist <head>." % brief.id)
        defaults = [brief.get("serie"), brief.get("slug"), brief.get("titre")]
        args = args + defaults[len(args):]

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

    # Per-article meta block (read by tools/check-seo.py on indexed posts)
    query, author, og, brief_line = "none", "L'équipe CheckIA", "pending", ""
    if brief:
        q = brief.get("requete") or "none"
        query = "none" if fold(q) in ("aucune", "none", "") else q
        author = brief.get("auteur") or author
        og = "default" if brief.get("image-og") == "generique" else "pending"
        brief_line = f"       brief: {brief.id}\n"
        # Prefill title, description, h1 and video id from the brief.
        # [^<]* : the template's head comment also contains the string « <title> »,
        # so a lazy .*? with re.S would swallow the comment and its closing tag.
        m = re.search(r"<title>([^<]*)</title>", text)
        if m:
            old_title = re.sub(r"\s*\|\s*CheckIA\s*$", "", m.group(1).strip())
            if old_title:
                text = text.replace(old_title, html.escape(title, quote=False))
        m = re.search(r'<meta name="description" content="([^"]*)"', text)
        if m and brief.get("description"):
            text = text.replace(m.group(1), html.escape(brief.get("description"), quote=True))
        m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S)
        if m:
            text = text.replace(m.group(1), html.escape(title, quote=False))
        if brief.get("video-id"):
            text = text.replace("REMPLACER_ID_YOUTUBE", brief.get("video-id"))
        if brief.get("video-duree"):
            text = re.sub(r'"duration":\s*"PT[^"]*"', '"duration": "%s"' % brief.get("video-duree"), text)
    block = (
        "  <!-- checkia-meta\n"
        f"       format: {fmt}\n"
        f"       query: {query}\n"
        f"       author: {author}\n"
        f"       og-image: {og}\n"
        f"{brief_line}"
        "  -->\n"
    )
    if "checkia-meta" in text:
        text = re.sub(r"[ \t]*<!--\s*checkia-meta.*?-->\n?", block, text, count=1, flags=re.S)
    else:
        text = text.replace("<head>\n", "<head>\n" + block, 1)

    dest.mkdir(parents=True)
    (dest / "index.html").write_text(text, encoding="utf-8")

    print(f"Créé : blog/{serie}/{slug}/index.html (noindex)\n")
    print(f"Titre à intégrer : « {title} »\n")
    if brief:
        print(f"Brief : {brief.id} — python3 tools/plan.py show {brief.id}")
        print(f"Statut : python3 tools/plan.py set {brief.id} statut=redaction (si ce n'est pas déjà fait)\n")
    print("Checklist avant publication (voir AGENTS.md) :")
    print("  1. Lire les 3 derniers articles indexés (ton et style) : grep -L noindex blog/*/*/index.html")
    print("  2. Remplacer titres, description, contenus, FAQ, TLDR (« L'essentiel »).")
    print("  3. Bloc checkia-meta : query (requête cible ou none), author (personne ou L'équipe CheckIA).")
    if fmt != "texte":
        print("  4. Vidéo : ID YouTube, durée, chapitres/Clip, miniature, transcription.")
    print("  5. Images : demander la source (fichier fourni / miniature vidéo / carte générée) puis")
    print(f"     python3 tools/social-images.py {serie} {slug} --source <generated|image:…|video:…>")
    print("     → reporter og:image / og:image:alt / twitter:image / JSON-LD image, og-image: dedicated.")
    print("  6. Cartes : /blog/, page de série (+ ItemList JSON-LD), pagenav/« À lire ensuite » des voisins.")
    print("  7. python3 tools/build-llms.py   (index.md + llms-full.txt)")
    print("  8. python3 tools/check-seo.py    (0 erreur, encore en noindex)")
    print(f"  9. Rédiger blog/{serie}/{slug}/social.md : tweet, légende Instagram, texte LinkedIn/Facebook")
    print("     (en français, une idée + le lien vers l'article, #CNCC #CAC #Audit).")
    print(" 10. Demander « Prêt à publier ? ». Si oui : robots en index, sitemap.xml (lastmod),")
    print("     blog/feed.xml, llms.txt, build-llms + check-seo à nouveau, commit (message en français).")
    print(f" 11. Après déploiement : tools/indexnow.sh {SITE}/blog/{serie}/{slug}/")


if __name__ == "__main__":
    main()
