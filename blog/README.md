# Blog CheckIA — master publishing guide

Objectif : être la référence francophone sur l'automatisation documentaire du
commissariat aux comptes — dans Google **et** dans les réponses des assistants
IA (ChatGPT, Claude, Perplexity, AI Overviews).

Static blog, four series:

| Series | URL | Formats |
|---|---|---|
| Nouveautés produit | `/blog/nouveautes-produit/` | text + screenshots, demo video |
| Le futur de l'audit | `/blog/futur-de-l-audit/` | analyses, video + article |
| Vie de l'entreprise | `/blog/vie-de-l-entreprise/` | text |
| Témoignages clients | `/blog/temoignages-clients/` | video (template: `modele-temoignage/`) |

## Two layers of optimization — keep them separate

Every post goes through two distinct checks. Don't conflate them:

1. **Keyword targeting** (per-post, *optional*): does this post target one of
   our priority queries? Some posts do (funnel content, product pages); some
   legitimately don't (company news, brand posts). Decide explicitly at step 2
   of the checklist — a post that doesn't target a keyword is fine, but it
   should be a decision, not an oversight.
2. **Baseline SEO & LLM optimization** (*every post, no exceptions*):
   technical SEO (head tags, JSON-LD, canonical, sitemap) and LLM/AI-search
   citability (« L'essentiel », FAQ, transcript, markdown alternates,
   `llms.txt`). This applies whether or not the post targets a keyword.

## Requêtes cibles par série

| Série | Intention | Requêtes prioritaires |
|---|---|---|
| Le futur de l'audit | informationnelle (haut de funnel) | `IA commissariat aux comptes`, `intelligence artificielle audit`, `avenir du commissariat aux comptes`, `IA et NEP`, `automatisation audit légal` |
| Nouveautés produit | navigationnelle / considération | `logiciel CAC`, `logiciel commissariat aux comptes`, `génération plan de mission`, `dossier de travail CAC`, `logiciel missions spécifiques CAC` |
| Témoignages clients | transactionnelle (preuve sociale) | `avis logiciel CAC`, `[type de cabinet] + automatisation`, requêtes de marque `CheckIA` |
| Vie de l'entreprise | marque / E-E-A-T | `CheckIA`, `qui a créé CheckIA`, requêtes de confiance |

Règles (uniquement pour les articles qui ciblent une requête) :
- **Une requête principale par article**, placée en tête du `<title>`, dans le
  `<h1>`, dans la description et dans le premier paragraphe.
- Les requêtes secondaires deviennent des `<h2>` (elles alimentent les
  « People Also Ask ») et des questions de la FAQ.
- Un article = une intention. Si deux intentions, deux articles reliés par
  maillage interne.

## Templates (3)

**The post type is never assumed. Before creating any article, ALWAYS ask the
author which type of post this is — they must specify one of the three:**

| `--format` | Post type | Template (noindex gabarit) |
|---|---|---|
| `video` | video + full text article | `futur-de-l-audit/ia-commissariat-aux-comptes/index.html` |
| `texte` | written article only, no video | `vie-de-l-entreprise/modele-texte/index.html` |
| `temoignage` | client testimonial (video) | `temoignages-clients/modele-temoignage/index.html` |

The generator refuses to run without `--format`.

## Publishing an article

1. **Ask the author for the post type** (video / texte / temoignage — see
   table above), then **generate** the article skeleton (created as `noindex`,
   with placeholders):

   ```bash
   python3 tools/new-article.py <serie> <slug-de-l-article> "Titre de l'article" --format <video|texte|temoignage>
   ```

   Slug should be short, lowercase, hyphenated, without accents.
2. **Keyword check** (layer 1): ask the author (or decide together) whether
   this post targets one of the priority queries from the table above.
   - **Yes** → apply the one-query-per-article rules: main query at the start
     of `<title>`, in the `<h1>`, description, and first paragraph; secondary
     queries as `<h2>` and FAQ questions.
   - **No** (company news, brand post…) → note it and skip keyword-placement
     rules. **All remaining steps still apply** — baseline SEO and LLM
     optimization are never optional.
3. **Adapt the `<head>`**: `<title>` (50–60 characters), `description`
   (140–160), `canonical`, OG/Twitter tags, ISO dates, JSON-LD
   (BlogPosting + BreadcrumbList, VideoObject if video, FAQPage if FAQ).
4. **Video**: replace `REMPLACER_ID_YOUTUBE` (facade + chapters + noscript
   + JSON-LD `embedUrl`), the duration (`PT12M34S` and displayed `12:34`), the
   thumbnail, and paste the **full transcript** into `<details class="transcript">`.
   Chapters (`data-start` in seconds) must match the `Clip` entries in the JSON-LD.
5. **OG image**: ideally a dedicated 1200×630 image in `images/blog/`.
6. **Internal linking**: add the article's card on `/blog/` (and move the
   previous « À la une » item into the grid if needed), on its series page,
   and update the « À lire ensuite » / `pagenav` blocks of neighboring articles.
   Each new article gets at least 2 incoming internal links and points to 1-2
   existing articles plus the relevant product page.
7. **Indexing**: switch the `robots` meta back to
   `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1`,
   add the URL to `sitemap.xml` (with `lastmod`) and an
   `<item>` to `blog/feed.xml`; update `llms.txt`.
8. **LLM layer**: regenerate the markdown alternates and `llms-full.txt`:

   ```bash
   python3 tools/build-llms.py
   ```

9. **Check**: run the automated validation — it must report 0 errors:

   ```bash
   python3 tools/check-seo.py
   ```

10. **Verify online**: [Rich Results Test](https://search.google.com/test/rich-results)
    on the published page, OG preview (LinkedIn Post Inspector), internal links.

## Template SEO rules (do not break)

- A single `<h1>` per page; `h2`/`h3` hierarchy without skipping levels.
- The « L'essentiel » box (`.tldr`) stays at the top of the article: it's what
  Google snippets and AI assistants quote (`speakable` points to it).
- The visible FAQ and the JSON-LD `FAQPage` block must be identical word for word.
- Transcript always in the HTML (video SEO + accessibility + citability by AIs).
- Dates in ISO 8601 format in `datetime`, OG, and JSON-LD.
- Canonical URLs with trailing slash, as `https://checkia.fr/…`.

## Ce qui fait référencer par les LLM (à maintenir)

- `llms.txt` (index) et `llms-full.txt` (texte intégral) à jour —
  régénérés par `tools/build-llms.py`.
- `index.md` par article (alternate markdown, lien `rel="alternate"` dans le head).
- Encadré « L'essentiel » : affirmations factuelles autonomes, citables telles
  quelles (c'est ce que reprennent les assistants).
- FAQ : formuler les questions comme les utilisateurs les posent réellement.
- Transcriptions complètes dans le HTML.
- Chiffres précis et datés (« jusqu'à 80 % du temps de formalisation ») :
  les LLM citent les sources qui donnent des chiffres.

## E-E-A-T (crédibilité, domaine réglementé)

- Auteur : à terme, signer les articles de fond avec une personne réelle
  (`Person` en JSON-LD : nom, fonction, « commissaire aux comptes », profil
  LinkedIn en `sameAs`). Un article signé par un CAC identifiable pèse plus
  qu'« équipe CheckIA » sur des requêtes réglementaires.
- Citer les sources officielles (CNCC, H2A, NEP) avec liens sortants.
- Dates de publication **et** de mise à jour visibles et exactes.

## Maintenance

- Mettre à jour `lastmod` (sitemap) et `dateModified` à chaque modification
  substantielle — Google et les LLM privilégient le contenu maintenu.

## Outils

| Commande | Rôle |
|---|---|
| `python3 tools/new-article.py <serie> <slug> "Titre" --format <…>` | crée un article depuis le gabarit |
| `python3 tools/build-llms.py` | régénère `index.md` + `llms-full.txt` |
| `python3 tools/check-seo.py` | vérifie toutes les règles SEO (0 erreur exigé) |
