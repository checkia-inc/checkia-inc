# Blog CheckIA — guide de publication

Blog statique, quatre séries :

| Série | URL | Formats |
|---|---|---|
| Nouveautés produit | `/blog/nouveautes-produit/` | texte + captures, vidéo de démo |
| Le futur de l'audit | `/blog/futur-de-l-audit/` | analyses, vidéo + article |
| Vie de l'entreprise | `/blog/vie-de-l-entreprise/` | texte |
| Témoignages clients | `/blog/temoignages-clients/` | vidéo (modèle : `modele-temoignage/`) |

## Publier un article

1. **Dupliquer** l'article existant de la série le plus proche du format voulu
   (le modèle de référence complet — vidéo + texte — est
   `futur-de-l-audit/ia-commissariat-aux-comptes/index.html`) vers
   `blog/<serie>/<slug-de-l-article>/index.html`. Slug court, en minuscules,
   avec tirets, sans accents.
2. **Adapter le `<head>`** : `<title>` (50–60 caractères), `description`
   (140–160), `canonical`, balises OG/Twitter, dates ISO, JSON-LD
   (BlogPosting + BreadcrumbList, VideoObject si vidéo, FAQPage si FAQ).
3. **Vidéo** : remplacer `REMPLACER_ID_YOUTUBE` (façade + chapitres + noscript
   + JSON-LD `embedUrl`), la durée (`PT12M34S` et affichages `12:34`), la
   miniature, et coller la **transcription complète** dans `<details class="transcript">`.
   Les chapitres (`data-start` en secondes) doivent correspondre aux `Clip` du JSON-LD.
4. **Image OG** : idéalement une image dédiée 1200×630 dans `images/blog/`.
5. **Maillage** : ajouter la carte de l'article sur `/blog/` (et déplacer
   l'ancien « À la une » dans la grille si besoin), sur la page de sa série,
   et mettre à jour les blocs « À lire ensuite » / `pagenav` des articles voisins.
6. **Référencement** : ajouter l'URL dans `sitemap.xml` (avec `lastmod`) et un
   `<item>` dans `blog/feed.xml` ; mettre à jour `llms.txt`.
7. **Vérifier** : [Test des résultats enrichis](https://search.google.com/test/rich-results)
   sur la page publiée, aperçu OG (LinkedIn Post Inspector), liens internes.

## Règles SEO du gabarit (à ne pas casser)

- Un seul `<h1>` par page ; hiérarchie `h2`/`h3` sans saut.
- L'encadré « L'essentiel » (`.tldr`) reste en tête d'article : c'est lui que
  reprennent les extraits Google et les assistants IA (`speakable` y pointe).
- La FAQ visible et le bloc `FAQPage` du JSON-LD doivent être identiques mot pour mot.
- Transcription toujours dans le HTML (SEO vidéo + accessibilité + citation par les IA).
- Dates au format ISO 8601 dans `datetime`, OG et JSON-LD.
- URLs canoniques avec slash final, en `https://www.checkia.fr/…`.
