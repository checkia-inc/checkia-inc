# CheckIA — site public (checkia.fr)

Site statique de **checkia.fr**, généré depuis des fichiers de contenu Markdown et
déployé tel quel sur GitHub Pages.

```bash
python3 build.py          # génère le site à la racine du dépôt
python3 build.py --check  # contrôles d'intégrité seuls, sans écriture
```

**Aucune dépendance.** Le générateur n'utilise que la bibliothèque standard de
Python 3 — pas de npm, pas de pip, pas d'étape de build en CI. Le déploiement
GitHub Pages par branche continue de fonctionner sans modification : on commite
le HTML généré.

---

## Comment ça marche

```
content/           ← la seule chose à modifier pour écrire du contenu
  _data/site.md    ← navigation, pied de page, redirections
  index.md         ← page d'accueil
  produit/…        ← une page = un fichier .md
lib/               ← moteur (frontmatter, markdown, sections, visuels)
site/assets/       ← feuille de style, JS, favicon (copiés vers /assets/)
build.py           ← générateur
```

Tout le reste à la racine (`index.html`, `produit/`, `sitemap.xml`, `robots.txt`,
`llms.txt`, `assets/`, les redirections) est **généré**. Ne pas l'éditer à la
main : la prochaine génération écrase les modifications.

### Ajouter une page

Créer un fichier dans `content/`, par exemple `content/ressources/mon-guide.md` :

```markdown
---
url: /ressources/mon-guide/
title: Titre affiché en h1
group: Ressources          # regroupement dans llms.txt
type: article              # "article" (prose) ou "landing" (sections)
updated: 2026-08-11
seo:
  title: "Titre SEO — 65 caractères maximum"
  description: "Meta description, 165 caractères maximum."
---

## Première section

Le corps en Markdown. Les `##` deviennent des `h2` et alimentent le sommaire.
```

Puis `python3 build.py`. La page est écrite, ajoutée au sitemap et à `llms.txt`,
son fil d'Ariane et son `BreadcrumbList` sont dérivés de l'URL.

### Deux types de page

| `type` | Pour quoi | Contenu défini par |
|---|---|---|
| `article` | Guides, contenu réglementaire, glossaire | Corps Markdown sous le frontmatter (+ sommaire, sources, date de vérification) |
| `landing` | Accueil, pages produit, hubs | Liste `sections:` dans le frontmatter |

Les sections disponibles sont dans `lib/sections.py` (`REGISTRY` en bas de
fichier) : `hero`, `trust`, `answer`, `cards`, `steps`, `split`, `visual`,
`table`, `prose`, `faq`, `links`, `quote`, `cta`, `sources`. Ajouter une mise en
page = ajouter une fonction et une entrée au registre ; aucun gabarit de page
n'est jamais dupliqué.

### Schémas et métadonnées

`schema: [Organization, Article, SoftwareApplication, WebSite, DefinedTerm]`
déclare les blocs JSON-LD. `FAQPage` est ajouté **automatiquement**, et
uniquement si une section `faq` est réellement rendue sur la page — pas de
données structurées sans contenu visible correspondant.

### Redirections

Les anciennes URL sont déclarées dans `content/_data/site.md` sous `redirects:`.
GitHub Pages ne gère pas les redirections serveur : le générateur écrit une page
de renvoi avec `canonical`, `noindex` et `meta refresh`.

---

## Contrôles automatiques

`python3 build.py` échoue (code de sortie 1) et liste les problèmes en cas de :

- lien interne mort ;
- page orpheline (aucun lien entrant, hors navigation et pages `noindex`) ;
- cible de navigation inexistante ;
- URL, title SEO ou meta description en double ;
- title SEO manquant ou de plus de 65 caractères ;
- meta description manquante ou de plus de 165 caractères ;
- page comportant zéro ou plusieurs `h1`.

À lancer avant tout commit.

---

## Design system

Une seule feuille de style, `site/assets/theme.css` (auparavant dupliquée en
ligne dans chaque page). Jetons de marque conservés du site précédent :

- **Bleu** `#165498` · **Cyan** `#5AE9FD` · **Encre** `#23242B` / `#3C3D47`
- **Fond secondaire** `#F7F9FC` · **Filets** `#E2E7F0` · **Sombre** `#0E2544`
- **Typographie** Inter, échelle fluide en `clamp()`
- Mouvement réduit respecté (`prefers-reduced-motion`), styles d'impression inclus

Les diagrammes sont des **SVG générés** (`lib/visuals.py`), stylés par variables
CSS : aucun binaire, aucune requête réseau, et ils suivent le thème.

---

## Règles éditoriales

Elles sont contraignantes, et deux documents expliquent pourquoi :

- [`docs/AUDIT-SITE-EXISTANT.md`](docs/AUDIT-SITE-EXISTANT.md) — ce qui a été conservé, retiré et corrigé du site précédent, avec les motifs.
- [`docs/MAPPING-MOTS-CLES.md`](docs/MAPPING-MOTS-CLES.md) — la réconciliation du classeur SEO (`docs/checkia_Keyword.xlsx`) avec le périmètre produit réel.

Les règles :

1. **Aucune allégation réglementaire non étayée.** Pas de « conformité CNCC »,
   pas de pourcentage d'alignement normatif.
2. **Aucune fonctionnalité inventée.** Le périmètre produit est le commissariat
   aux apports et le commissariat à la transformation. Les pages pédagogiques
   peuvent traiter d'autres sujets sans laisser entendre que le produit les
   couvre.
3. **Aucun chiffre non sourcé**, aucun client nommé sans accord écrit.
4. **Les points inconnus sont marqués comme tels** plutôt que comblés par une
   formule rassurante (voir le tableau de la page sécurité).
5. **Les pages réglementaires portent une date** de mise à jour et de
   vérification, et citent leurs sources.

---

## Déploiement

Inchangé : **Settings → Pages → Deploy from a branch**, `main` / racine.
`CNAME` fixe le domaine `www.checkia.fr`.

```bash
python3 build.py
git add -A
git commit -m "…"
git push
```
