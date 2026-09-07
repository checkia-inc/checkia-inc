# CheckIA blog — publishing guide for AI agents

This file is the single source of truth for publishing on `checkia.fr/blog`.
Read it in full before creating or editing any article. It is loaded
automatically by `CLAUDE.md`.

## Language rule

- This guide, code comments and tool docstrings are written in **English**.
- **Every deliverable is in French**: article body, `<title>`, meta
  description, OG/Twitter tags, alt text, every string in JSON-LD, FAQ,
  transcript, `index.md`, text rendered on social images, and **git commit
  messages**.
- French typography is part of the deliverable: non-breaking space before
  `? ! : ;` (`&nbsp;` in HTML), « guillemets » with non-breaking spaces,
  accents on capitals (É, À), percentages written `80 %`.

## Objective

Be the French-language reference on document automation for the
commissariat aux comptes (CAC), both in Google **and** in the answers of AI
assistants (ChatGPT, Claude, Perplexity, Google AI Overviews).

## Non-negotiable rules — ask, never assume

1. **Post type.** Always ask which of the three types the post is
   (`video`, `texte`, `temoignage`). The generator refuses to run without it.
2. **Author.** Always ask who signs the post. Default is `L'équipe CheckIA`
   when nobody is named. When a real person is named (usually a commissaire
   aux comptes), apply the full author procedure below.
3. **Images.** Always ask where the OG / social visuals come from:
   a file the author provides, the video thumbnail, or a generated card.
   A dedicated OG image is mandatory. The generic `/images/og-image.jpg` is
   allowed only when the author explicitly says so, and that decision is
   recorded in the article's meta block.
4. **Style corpus.** Only **indexed, live** posts are style references.
   Never read drafts, unpublished or `noindex` posts for tone. Templates are
   used for structure only, never for voice.
5. **Go-live gate.** Never switch `robots` to `index` on your own. When the
   post passes the checker, ask « Prêt à publier ? » and wait for a clear
   yes.
6. **Git.** Commit messages in French. Push only when the author asks.

## Series

| Series | URL | Formats |
|---|---|---|
| Nouveautés produit | `/blog/nouveautes-produit/` | text + screenshots, demo video — **only features shipped in CheckIA** (ids in `content-plan/produit-verite.md`); market and buying-guide pieces go to Le futur de l'audit |
| Le futur de l'audit | `/blog/futur-de-l-audit/` | analyses, video + article |
| Vie de l'entreprise | `/blog/vie-de-l-entreprise/` | text |
| Témoignages clients | `/blog/temoignages-clients/` | video (template: `modele-temoignage/`) |

## Style corpus and voice

Before drafting anything, list the live posts and read the three most recent
ones in full. The pool grows over time; the bigger it gets, the closer the
match must be.

```bash
grep -L 'noindex' blog/*/*/index.html
```

Voice observed in the live corpus (keep it, don't drift):

- **Register.** Vouvoiement. « Nous » for CheckIA. Professional, calm,
  factual. Never salesy, never breathless.
- **Sentences.** Short and declarative. One idea per sentence. Paragraphs of
  two to four sentences.
- **Structure.** Opening paragraph states the constat. « L'essentiel » box
  with 4–5 self-contained bullets. `h2` sections that each answer one
  question. Numbered steps when describing the product. One blockquote signed
  by the author. A « Questions fréquentes » section. One call to action to
  the 30-minute call (`https://calendar.notion.so/meet/jdcollard/checkia`).
- **The refrain.** The product automates document preparation and *never*
  replaces professional judgment. Say it once explicitly in every post:
  « sans jamais se substituer au jugement professionnel du commissaire aux
  comptes ».
- **Facts over adjectives.** Give figures with a scope (« jusqu'à 80 % du
  temps de formalisation »), cite the NEP, CNCC or H2A when relevant, and
  date every claim.
- **Vocabulary to use:** commissaire aux comptes / CAC, mission spécifique,
  audit légal, formalisation, préparation documentaire, éléments probants,
  dossier de travail, plan de mission, jugement professionnel, traçabilité,
  hébergement en France, NEP.
- **Vocabulary to avoid:** révolutionner, disrupter, game changer, magique,
  incroyable, « l'IA remplace », anglicisms when a French word exists
  (workflow → flux de travail, feature → fonctionnalité), exclamation marks.

## Two layers of optimization — keep them separate

Every post goes through two distinct checks. Don't conflate them:

1. **Keyword targeting** (per post, *optional*): does this post target one
   of our priority queries? Funnel and product posts usually do; company news
   and brand posts often don't. It is a decision recorded in the meta block
   (`query: …` or `query: none`), never an oversight.
2. **Baseline SEO and LLM optimization** (*every post, no exceptions*):
   head tags, JSON-LD, canonical, sitemap, feed, dedicated OG image, social
   visuals and social copy, « L'essentiel », FAQ, transcript, markdown
   alternate, `llms.txt`.

## Target queries

Main queries per series (used at the start of the `<title>`, in the `<h1>`,
the description and the first paragraph when a post targets one):

| Series | Intent | Priority queries |
|---|---|---|
| Le futur de l'audit | informational (top of funnel) | `IA commissariat aux comptes`, `intelligence artificielle audit`, `avenir du commissariat aux comptes`, `IA et NEP`, `automatisation audit légal` |
| Nouveautés produit | navigational / consideration | `logiciel CAC`, `logiciel commissariat aux comptes`, `génération plan de mission`, `dossier de travail CAC`, `logiciel missions spécifiques CAC` |
| Témoignages clients | transactional (social proof) | `avis logiciel CAC`, `[type de cabinet] + automatisation`, brand queries `CheckIA` |
| Vie de l'entreprise | brand / E-E-A-T | `CheckIA`, `qui a créé CheckIA`, trust queries |

Question-form queries (what AI Overviews, Perplexity and « People Also Ask »
actually match). Use them as `h2` and FAQ questions, worded exactly as a CAC
would type them:

- Futur de l'audit : « L'IA va-t-elle remplacer le commissaire aux
  comptes ? », « Comment l'IA est-elle utilisée en audit légal ? »,
  « Quelles NEP encadrent l'utilisation de l'IA par le CAC ? », « Comment un
  cabinet de CAC peut-il automatiser la formalisation ? », « L'IA est-elle
  compatible avec le secret professionnel du commissaire aux comptes ? »
- Nouveautés produit : « Quel logiciel pour les missions spécifiques du
  commissaire aux comptes ? », « Comment générer un plan de mission CAC
  automatiquement ? », « Comment centraliser les éléments probants d'une
  mission ? », « Comment standardiser les dossiers de travail d'un cabinet ? »
- Témoignages : « Quel logiciel utilisent les cabinets de CAC pour gagner du
  temps ? », « Avis CheckIA »
- Vie de l'entreprise : « Qui a créé CheckIA ? », « Où sont hébergées les
  données CheckIA ? », « CheckIA est-il conforme aux NEP ? »

Rules when a post targets a query:
- **One main query per post**, at the start of the `<title>`, in the `<h1>`,
  the meta description and the first paragraph. The checker verifies the
  title.
- Secondary queries become `<h2>` headings and FAQ questions.
- One post = one intent. Two intents = two posts linked to each other.

Search Console data is not available yet. When it is, replace the tables
above with real queries.

## Intake — ask all of this before generating

Ask in one message, in French, and wait for the answers:

1. Post type: `video` / `texte` / `temoignage`.
2. Series.
3. Working title and the angle in one sentence.
4. Target query from the tables above, or « aucune ».
5. Author: a named person (name, title, LinkedIn URL) or `L'équipe CheckIA`.
6. For video posts: YouTube ID, duration, chapters, and the full transcript.
7. Three hard facts or figures the post must contain, with their source.
8. OG / social image source: provided file, video thumbnail, or generated card.
9. Call to action (default: the 30-minute call).

## Working from the content plan

The twelve-month plan lives in `content-plan/` (see `content-plan/README.md`, in French,
for the humans' side). One brief per piece in `content-plan/briefs/<id>-<slug>.md`;
`tools/plan.py` reads and writes them; `plan.csv` and `plan-editorial.xlsx` are generated
and mirrored into the team's Google Sheet. The repo is the source of truth.

**Start of every content session**

```bash
python3 tools/plan.py sync-sheet <URL CSV publiée de l'onglet Décisions, dans content-plan/README.md>
python3 tools/plan.py next
```

`sync-sheet` applies the humans' decisions (status changes, comments) into the briefs;
`next` says what to work on and prints the commands. Never invent a piece: if there is no
brief, create one with `plan.py new` and leave it at « Idée ».

**A validated brief replaces the intake questions.** When a brief is at `brief-valide`, do
not ask the nine intake questions again. Post **one** French confirmation message that
restates the brief in six lines (type, série, titre, requête cible, auteur, image OG, vidéo
if any, appel à l'action) and ends with « Je démarre la rédaction ? ». Proceed after a yes.
If a field is missing, ask only for that field, record it with
`plan.py set <id> cle=valeur`, then start. Then:

```bash
python3 tools/plan.py set <id> statut=redaction
python3 tools/new-article.py --brief <id>
```

**Statuses.** `idee` → `brief-valide` (**human**) → `redaction` (agent) → `relecture`
(agent) → `pret-a-publier` (**human**) → `publie` (agent, after go-live) → `a-rafraichir`
→ `archive` (**human**). `en-attente` while a `conditions` item reads « — non ». The agent
never sets `brief-valide`, `pret-a-publier` or `archive`; when a human gives that decision
in chat, record it with `plan.py set <id> statut=… --humain "Prénom"`. A `pret-a-publier`
decision in the Sheet counts as the yes to « Prêt à publier ? »; still show the checker
output before flipping `robots`. After « Going live »:

```bash
python3 tools/plan.py set <id> statut=publie
python3 tools/plan.py build
```

Commit the brief, `plan.csv` and `plan-editorial.xlsx` together with the article.

**Refresh pieces** (`type: refresh`, `rafraichit: Pxxx`). Read the target post and the
reason in the brief's Journal. Edit the body only; keep the URL, the `<h1>` intent and the
target query. Update `dateModified`, `article:modified_time`, the sitemap `lastmod`, re-run
`tools/build-llms.py` and `tools/check-seo.py`. Move to `relecture` with a diff summary;
commit only after `pret-a-publier`. On `publie`, add a Journal line « rafraîchi par Pxxx »
to the target brief.

**Interview rubric « Paroles de commissaires aux comptes »** (`rubrique: paroles-de-cac`,
series Le futur de l'audit). Format `video` (chapters = questions, full transcript) or
`texte` (Q/R). The title names the interviewee (« … : entretien avec Prénom Nom,
commissaire aux comptes »). The interviewee is a `Person` node in the JSON-LD `@graph`
(`@id` `#person-prenom-nom`, `jobTitle`, `sameAs` LinkedIn) referenced from the
`BlogPosting` as `mentions`; the author stays whoever signs (author procedure applies if
the interviewee also signs). Quotes are verbatim and validated by the interviewee: the
condition « Citations validées par l'interviewé — ok » must be set before `pret-a-publier`.
The post's single blockquote is theirs.

**Product truth.** Every claim about what CheckIA does must match
`content-plan/produit-verite.md`. Features under « Feuille de route » may only be mentioned
as future (« prévu », with a date), never as available. Product briefs list
`fonctionnalites:` ids; `plan.py check` enforces the mapping. When the product changes,
update `produit-verite.md` first, then flag the affected posts `a-rafraichir`. Hosting is
worded « hébergé en France (AWS Paris) »; never « souverain ». Never cite NEP 9010–9070
until the CNCC has confirmed their status.

**Citation check (monthly).** On the first working day of the month, `plan.py next --all`
lists the due checks (7 and 30 days after `date-publiee`). Run the five engines as
described under « AI search engines », append rows to `blog/suivi-ia.md`, and when a
competitor is cited instead of us, set the brief `a-rafraichir` with the reason in its
Journal.

`python3 tools/plan.py check` must report 0 errors before any commit that touches
`content-plan/` or a blog article.

## Templates (3)

| `--format` | Post type | Template (noindex) |
|---|---|---|
| `video` | video + full text article | `futur-de-l-audit/ia-commissariat-aux-comptes/index.html` |
| `texte` | written article only, no video | `vie-de-l-entreprise/modele-texte/index.html` |
| `temoignage` | client testimonial (video) | `temoignages-clients/modele-temoignage/index.html` |

Templates are `noindex` and must never be published or used as a style
reference. Edit a template only to change the structure for all future posts.

## Per-article meta block

Every article carries an HTML comment at the top of `<head>`. The generator
creates it, you fill it in, the checker enforces it on indexed posts:

```html
<!-- checkia-meta
     format: texte
     query: logiciel missions spécifiques CAC   (or: none)
     author: L'équipe CheckIA                   (or the person's full name)
     og-image: pending                          (pending | dedicated | default)
-->
```

- `query` other than `none` → the checker requires every word of the query
  in the `<title>` and warns if the query doesn't open it.
- `author` other than `L'équipe CheckIA` → the checker requires a matching
  `Person` in JSON-LD and the name in the visible byline.
- `og-image: dedicated` → `og:image` must not be the generic image and the
  file must exist. `default` is accepted only after the author said so.
  `pending` blocks publication.

## Publishing workflow

1. **Intake** (see above), then generate the skeleton (created as `noindex`
   with placeholders and the meta block):

   ```bash
   python3 tools/new-article.py <serie> <slug> "Titre de l'article" --format <video|texte|temoignage>
   ```

   Slug: short, lowercase, hyphenated, no accents.
2. **Read the live corpus** (three most recent indexed posts) before writing
   a single sentence.
3. **Write the article** in French, in the voice above. Fill the meta block
   (`query`, `author`). Apply the keyword rules if a query is targeted.
4. **Author.** Apply the author procedure below if a person signs the post.
5. **`<head>`.** Keep the Google tag inherited from the template at the
   top of `<head>`. `<title>` 50–60 characters, description 140–160,
   canonical, full OG and Twitter set, ISO dates, JSON-LD (see the
   checklists below).
6. **Video** (video and temoignage posts): replace `REMPLACER_ID_YOUTUBE`
   (facade + chapters + noscript + JSON-LD `embedUrl`), duration (`PT12M34S`
   and displayed `12:34`), thumbnail, and paste the **full transcript** into
   `<details class="transcript">`. Chapter `data-start` values must match the
   JSON-LD `Clip` entries.
7. **Images.** Produce the OG image and the social set (see « Social
   images »). Update `og:image`, `og:image:alt`, `twitter:image` and the
   JSON-LD `image`. Set `og-image: dedicated` in the meta block. Every
   `<img>` in the article gets a descriptive French `alt`.
8. **Internal linking.** Add the card on `/blog/` (move the previous « À la
   une » item into the grid if needed) and on the series page (including its
   `ItemList` JSON-LD). Update the « À lire ensuite » / `pagenav` blocks of
   neighboring posts. Each post gets at least 2 incoming internal links and
   links out to 1–2 posts plus the relevant product page.
9. **LLM layer.** Regenerate the markdown alternates and `llms-full.txt`:

   ```bash
   python3 tools/build-llms.py
   ```

10. **Check.** Must report 0 errors while still `noindex`:

    ```bash
    python3 tools/check-seo.py
    ```

11. **Social copy.** Write `social.md` next to the article (tweet,
    Instagram caption, LinkedIn/Facebook snippet) — see « Social copy » below.
12. **Go-live gate.** Show the author the checker output and ask
    « Prêt à publier ? ». Only after a yes, follow « Going live » below.

## Author procedure (E-E-A-T)

The blog covers a regulated profession. A post signed by an identifiable
commissaire aux comptes outranks « L'équipe CheckIA » on regulatory queries.

When a person signs the post:

1. Add a `Person` node to the `@graph` and point the `BlogPosting` to it:

   ```json
   {
     "@type": "Person",
     "@id": "https://checkia.fr/#person-prenom-nom",
     "name": "Prénom Nom",
     "jobTitle": "Commissaire aux comptes",
     "worksFor": { "@id": "https://checkia.fr/#organization" },
     "sameAs": ["https://www.linkedin.com/in/…"]
   }
   ```

   ```json
   "author": { "@id": "https://checkia.fr/#person-prenom-nom" }
   ```

2. `<meta property="article:author" content="https://www.linkedin.com/in/…">`.
3. Visible byline: `<strong>Prénom Nom</strong>` in `.byline`.
4. The `.authorcard` at the end of the post: name, one-line bio (function,
   cabinet, years of practice), link to LinkedIn.
5. The blockquote `<footer>` carries the same name.
6. `author:` in the meta block is the same name, character for character.

When `L'équipe CheckIA` signs, leave the template's Organization author.

In all cases: cite official sources (CNCC, H2A, NEP) with outgoing links,
and show accurate publication **and** update dates.

## `<head>` checklist (every article)

- **Google tag (Google Analytics 4, ID `G-L4K7TZWD7Q`)** at the top of
  `<head>`, right after `<meta charset="utf-8">`, before every other tag.
  Exactly one per page. The templates already carry it, so a post created
  with `tools/new-article.py` inherits it: never remove it, never duplicate
  it, never change the ID. Every page of the site (hub, series pages,
  articles, templates) must have it:

  ```html
  <!-- Google tag (gtag.js) — Google Analytics 4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-L4K7TZWD7Q"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-L4K7TZWD7Q');
  </script>
  <script src="/js/analytics.js" defer></script>
  ```

  `js/analytics.js` sends the interaction events that are marked as key
  events (conversions) in GA4: `button_click` (every button and
  button-styled link, with `button_text` and `button_type`), `book_call`
  (Notion calendar link), `email_click` (mailto links) and
  `contact_form_submit` (successful contact form). Keep the CTA markup
  (`.btn`, `.nav-cta`, the calendar URL) so the tracking keeps working.
- `<title>` (50–60 chars, main query first when targeted, ends with `| CheckIA`)
- `<meta name="description">` (140–160 chars, answers the search intent)
- `<link rel="canonical">` — `https://checkia.fr/…/` with trailing slash
- `<meta name="robots">` — `noindex, nofollow` until go-live, then
  `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1`
- `og:type=article`, `og:site_name=CheckIA`, `og:locale=fr_FR`, `og:url`,
  `og:title`, `og:description`, `og:image` (1200×630, absolute URL),
  `og:image:width`, `og:image:height`, `og:image:alt`
- `article:published_time`, `article:modified_time` (ISO 8601 with offset),
  `article:author`, `article:section`, three `article:tag`
- `twitter:card=summary_large_image`, `twitter:site=@checkiafr`,
  `twitter:title`, `twitter:description`, `twitter:image`
- `<link rel="alternate" type="application/rss+xml">` (feed) and
  `<link rel="alternate" type="text/markdown">` (`index.md`)

## JSON-LD checklist

- `Organization` (`@id` `#organization`, logo, email, `sameAs` with the four
  social profiles)
- `BlogPosting`: headline, description, image, datePublished, dateModified,
  author, publisher, isPartOf, articleSection, keywords, inLanguage `fr-FR`,
  wordCount (real count ± 25 %), timeRequired, `speakable` pointing to
  `.article-hero__head` and `.tldr`
- `BreadcrumbList`
- `VideoObject` with `hasPart` `Clip` chapters (video posts)
- `FAQPage` identical word for word to the visible FAQ
- `Person` when a person signs

## Social images

Every published post ships with a dedicated visual set in
`images/blog/<slug>/`:

| File | Size | Used for |
|---|---|---|
| `og.jpg` | 1200×630 | `og:image`, LinkedIn, Facebook, X |
| `instagram-feed.png` | 1080×1350 | Instagram feed (4:5) |
| `instagram-square.png` | 1080×1080 | Instagram square, LinkedIn square |
| `story.png` | 1080×1920 | Instagram and Facebook stories |

The source is decided with the author every time (intake question 8):

```bash
# branded typographic card (title + first « L'essentiel » line + series)
python3 tools/social-images.py <serie> <slug> --source generated

# a photo or screenshot the author provides
python3 tools/social-images.py <serie> <slug> --source image:chemin/vers/fichier.jpg

# the YouTube thumbnail of the post's video
python3 tools/social-images.py <serie> <slug> --source video:ID_YOUTUBE
```

The tool reads the title and the first « L'essentiel » bullet from the
article (override with `--title` / `--line`) and prints the head tags to
paste. The text on the cards is French. Profiles: LinkedIn
`https://www.linkedin.com/company/checkiafr`, Instagram
`https://www.instagram.com/checkiafr`, Facebook
`https://www.facebook.com/checkiafr`, X `https://x.com/checkiafr`.

## Social copy (after the post is finished)

Once the article is final and the checker passes, write
`blog/<serie>/<slug>/social.md` with three ready-to-paste posts, in French,
in the blog's voice. Each one teases the post and sends the reader to the
article to read the rest. Never summarize the whole post: one insight, one
figure or one question, then the link.

```markdown
# Réseaux sociaux — <titre de l'article>

URL : https://checkia.fr/blog/<serie>/<slug>/

## X (tweet)
<≤ 280 caractères, lien inclus, ends with the article URL>
#CNCC #CAC #Audit

## Instagram
<hook line, 3–5 short lines, blank lines between them, invitation « Article
complet sur checkia.fr — lien en bio », then the hashtags on their own line>
#CNCC #CAC #Audit

## LinkedIn / Facebook
<hook line, 4–8 short lines with one concrete fact or figure, one line
that says the rest is on the blog, the article URL on its own line>
#CNCC #CAC #Audit
```

Rules:
- Same facts as the article, no new claims. Vouvoiement, no exclamation
  marks, no emojis beyond one at most on Instagram.
- The tweet must stay under 280 characters including the URL and hashtags.
- Instagram cannot link from a caption: say « lien en bio » and put the URL
  in the file so the author can update the bio link.
- LinkedIn and Facebook share the same snippet. The first line is the hook
  shown before « voir plus », so it carries the insight.
- Standard hashtags on every platform: `#CNCC #CAC #Audit`.
- Pair each post with the matching visual from `images/blog/<slug>/`.

## What makes LLMs cite us (maintain)

- `llms.txt` (index) and `llms-full.txt` (full text) up to date, regenerated
  by `tools/build-llms.py`.
- One `index.md` per post (markdown alternate, `rel="alternate"` in the head).
- « L'essentiel »: self-contained factual statements, quotable as-is. This
  is what assistants lift.
- Define each key term once, in one sentence, near the top (« Une mission
  spécifique est … »). LLMs quote definitions verbatim.
- FAQ questions worded the way users actually ask them.
- Full transcripts in the HTML.
- Precise, dated figures with a scope. LLMs cite sources that give numbers.
- Outgoing links to CNCC, H2A and the NEP texts.

## AI search engines (multi-model)

The « What makes LLMs cite us » layer above is shared by every assistant.
This section covers what differs between engines, and how we verify that
they actually cite us. Every rule here is checked by `tools/check-seo.py`
where a check is possible.

### Crawler policy — allow every retrieval bot, explicitly

Our objective is to be cited, so we **allow** both the retrieval bots (used
to answer a question) and the training bots. The decision is written into
`robots.txt` as an explicit `Allow: /` per user-agent, never left to the
wildcard alone: some engines treat an explicit entry as a stronger signal,
and an explicit list makes an accidental block visible in a diff.

| Engine | User-agents to keep allowed | How it finds us |
|---|---|---|
| ChatGPT search, Copilot (OpenAI) | `OAI-SearchBot` (search index), `ChatGPT-User` (live fetch), `GPTBot` (training) | own index + Bing index → IndexNow matters |
| Claude (Anthropic) | `Claude-SearchBot`, `Claude-User`, `ClaudeBot` | Brave index (no push API: clean crawl + sitemap) |
| Perplexity | `PerplexityBot`, `Perplexity-User` | own index + live fetch, favors fresh, dated pages |
| Google AI Overviews / AI Mode, Gemini | `Googlebot` (AI Overviews use the normal index), `Google-Extended` (Gemini grounding) | Google index; `max-snippet:-1` already set |
| Microsoft Copilot, Bing chat | `Bingbot` | Bing index → IndexNow |
| Mistral Le Chat (French market) | `MistralAI-User` | live fetch |
| Others worth keeping open | `Applebot`, `Applebot-Extended`, `Amazonbot`, `Meta-ExternalAgent`, `DuckAssistBot`, `CCBot` | Siri/Apple Intelligence, Alexa, Meta AI, DuckDuckGo, Common Crawl |

Rules:
- `robots.txt` lists each of these user-agents with `Allow: /`. Never add a
  `Disallow` for one of them without the author's explicit decision,
  recorded in a commit message.
- Never block by user-agent at the hosting or CDN level either (bot
  protection rules, rate limits on `*Bot`). Check this after any hosting
  change.
- `noindex` pages stay `noindex` for everyone; the crawler policy does not
  override the go-live gate.
- `llms.txt` must link to `llms-full.txt`, and both must stay reachable at
  the site root (no redirect, `text/plain` or `text/markdown`).

### What each engine weighs (write for all of them at once)

- **Freshness and dates.** Perplexity and ChatGPT search prefer pages with
  a visible, recent date. Keep `dateModified` honest and update it on every
  substantive edit (see « Maintenance »).
- **Self-contained passages.** Assistants lift one paragraph, not a page.
  Every `h2` section must be readable on its own: restate the subject in
  the first sentence instead of « ce point » or « cette fonctionnalité ».
- **Question headings.** AI Overviews and Perplexity match `h2` and FAQ
  questions almost verbatim; use the question-form queries listed under
  « Target queries ».
- **Numbers with a scope and a source.** Every engine favors pages that give
  a figure, its scope and its origin (NEP, CNCC, H2A, our own measurement
  with its date).
- **Entity consistency (brand queries).** Assistants answer « Qui a créé
  CheckIA ? » and « Où sont hébergées les données CheckIA ? » from
  third-party sources as much as from our site. Keep the one-paragraph
  company description at the top of `llms.txt`, the `Organization` JSON-LD,
  the LinkedIn page and the other profiles listed in `sameAs` identical in
  substance: same founders, same positioning, same hosting claim. Fix
  drift as soon as it appears.
- **Bing Webmaster Tools.** The site must stay verified there and the
  sitemap submitted: Bing feeds ChatGPT search and Copilot.

### Citation check (after publication)

Google Search Console is the only engine that reports on us. For the
others, we test by hand. One week after go-live, and again one month later,
ask each assistant the post's target query (or, for `query: none`, the
first FAQ question) in French, with web search enabled where it is an
option:

1. ChatGPT (search on), 2. Perplexity, 3. Claude (web search on),
4. Google AI Overviews / AI Mode, 5. Mistral Le Chat.

Record the result in `blog/suivi-ia.md` (one line per engine and date:
cited / not cited, which page was cited, which competitor was cited
instead). When an engine cites a competitor or an older post of ours, fix
the post before anything else: sharpen the « L'essentiel » bullets, add the
missing figure, tighten the `h2` question. Then update `dateModified`,
regenerate the LLM layer and re-check.

## Going live

Only after the author answered yes to « Prêt à publier ? »:

1. Set `robots` to `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1`.
2. Add the URL to `sitemap.xml` with `lastmod` = `dateModified`, an `<item>`
   to `blog/feed.xml`, and the post to `llms.txt`.
3. Run `python3 tools/build-llms.py` then `python3 tools/check-seo.py`
   (0 errors, now as an indexed page).
4. Commit with a French message. Push only if the author asks.
5. Once the site is deployed, submit the URL to Bing (IndexNow, also
   forwarded to the other IndexNow engines). Give the author this command:

   ```bash
   tools/indexnow.sh https://checkia.fr/blog/<serie>/<slug>/
   ```

   `HTTP 200` or `202` means accepted. The key file
   `<key>.txt` at the site root must stay deployed.
6. Google has no push API for blog posts: request indexing in Search Console
   (URL inspection → Demander une indexation).
7. Verify: [Rich Results Test](https://search.google.com/test/rich-results),
   LinkedIn Post Inspector for the OG preview, and click the internal links.
8. One week later: run the « Citation check » from the « AI search engines »
   section and log the result in `blog/suivi-ia.md`.

## Template rules (do not break)

- The Google tag (`G-L4K7TZWD7Q`) stays at the top of `<head>` on every
  page, exactly once (see the `<head>` checklist).
- A single `<h1>` per page; `h2`/`h3` hierarchy without skipping levels.
- « L'essentiel » (`.tldr`) stays at the top of the article.
- Visible FAQ and JSON-LD `FAQPage` identical word for word.
- Transcript always in the HTML.
- ISO 8601 dates in `datetime`, OG and JSON-LD.
- Canonical URLs with trailing slash, `https://checkia.fr/…`.

## Maintenance

- Update `lastmod` (sitemap) and `dateModified` at every substantive edit.
  Google and LLMs favor maintained content.
- When a post is unpublished, follow the comment in the template head:
  `noindex`, remove from hub, series page, `ItemList`, sitemap, feed,
  `llms.txt`.

## Tools

| Command | Role |
|---|---|
| `python3 tools/plan.py next` / `list` / `show <id>` | what to work on now; the plan's pieces and their briefs |
| `python3 tools/plan.py sync-sheet <url>` | applies the humans' decisions from the Google Sheet into the briefs |
| `python3 tools/plan.py set <id> statut=… [--humain "Prénom"]` | moves a piece through the workflow (human-only transitions need `--humain`) |
| `python3 tools/plan.py check` | validates the plan and its consistency with the site (0 errors required) |
| `python3 tools/plan.py build` | regenerates `content-plan/plan.csv` (Google Sheets mirror) and `plan-editorial.xlsx` |
| `python3 tools/new-article.py <serie> <slug> "Titre" --format <…>` | creates a post from the template, with the meta block |
| `python3 tools/new-article.py --brief <id>` | same, prefilled from the brief (format, requête, auteur, titre, vidéo) |
| `python3 tools/social-images.py <serie> <slug> --source <generated\|image:…\|video:…>` | OG image + Instagram/story set |
| `python3 tools/build-llms.py` | regenerates `index.md` + `llms-full.txt` |
| `python3 tools/check-seo.py` | validates every rule, including the AI crawler allowlist in `robots.txt` (0 errors required) |
| `tools/indexnow.sh <url…>` | submits published URLs to Bing / IndexNow |
