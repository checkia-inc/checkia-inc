# Blog CheckIA — publishing guide

Static blog, four series:

| Series | URL | Formats |
|---|---|---|
| Nouveautés produit | `/blog/nouveautes-produit/` | text + screenshots, demo video |
| Le futur de l'audit | `/blog/futur-de-l-audit/` | analyses, video + article |
| Vie de l'entreprise | `/blog/vie-de-l-entreprise/` | text |
| Témoignages clients | `/blog/temoignages-clients/` | video (template: `modele-temoignage/`) |

Keyword targets and editorial rules: see [STRATEGIE-SEO.md](STRATEGIE-SEO.md).

## Publishing an article

1. **Generate** the article skeleton (created as `noindex`, with placeholders):

   ```bash
   python3 tools/new-article.py <serie> <slug-de-l-article> "Titre de l'article"
   ```

   Add `--format temoignage` for a client testimonial (template:
   `temoignages-clients/modele-temoignage/`). The full video + text reference
   template is `futur-de-l-audit/ia-commissariat-aux-comptes/index.html`.
   Slug should be short, lowercase, hyphenated, without accents.
2. **Adapt the `<head>`**: `<title>` (50–60 characters), `description`
   (140–160), `canonical`, OG/Twitter tags, ISO dates, JSON-LD
   (BlogPosting + BreadcrumbList, VideoObject if video, FAQPage if FAQ).
3. **Video**: replace `REMPLACER_ID_YOUTUBE` (facade + chapters + noscript
   + JSON-LD `embedUrl`), the duration (`PT12M34S` and displayed `12:34`), the
   thumbnail, and paste the **full transcript** into `<details class="transcript">`.
   Chapters (`data-start` in seconds) must match the `Clip` entries in the JSON-LD.
4. **OG image**: ideally a dedicated 1200×630 image in `images/blog/`.
5. **Internal linking**: add the article's card on `/blog/` (and move the
   previous « À la une » item into the grid if needed), on its series page,
   and update the « À lire ensuite » / `pagenav` blocks of neighboring articles.
6. **Indexing**: switch the `robots` meta back to
   `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1`,
   add the URL to `sitemap.xml` (with `lastmod`) and an
   `<item>` to `blog/feed.xml`; update `llms.txt`.
7. **LLM layer**: regenerate the markdown alternates and `llms-full.txt`:

   ```bash
   python3 tools/build-llms.py
   ```

8. **Check**: run the automated validation — it must report 0 errors:

   ```bash
   python3 tools/check-seo.py
   ```

9. **Verify online**: [Rich Results Test](https://search.google.com/test/rich-results)
   on the published page, OG preview (LinkedIn Post Inspector), internal links.

## Template SEO rules (do not break)

- A single `<h1>` per page; `h2`/`h3` hierarchy without skipping levels.
- The « L'essentiel » box (`.tldr`) stays at the top of the article: it's what
  Google snippets and AI assistants quote (`speakable` points to it).
- The visible FAQ and the JSON-LD `FAQPage` block must be identical word for word.
- Transcript always in the HTML (video SEO + accessibility + citability by AIs).
- Dates in ISO 8601 format in `datetime`, OG, and JSON-LD.
- Canonical URLs with trailing slash, as `https://checkia.fr/…`.
