# Stratégie SEO & LLM du blog CheckIA

Objectif : être la référence francophone sur l'automatisation documentaire du
commissariat aux comptes — dans Google **et** dans les réponses des assistants
IA (ChatGPT, Claude, Perplexity, AI Overviews).

## Requêtes cibles par série

| Série | Intention | Requêtes prioritaires |
|---|---|---|
| Le futur de l'audit | informationnelle (haut de funnel) | `IA commissariat aux comptes`, `intelligence artificielle audit`, `avenir du commissariat aux comptes`, `IA et NEP`, `automatisation audit légal` |
| Nouveautés produit | navigationnelle / considération | `logiciel CAC`, `logiciel commissariat aux comptes`, `génération plan de mission`, `dossier de travail CAC`, `logiciel missions spécifiques CAC` |
| Témoignages clients | transactionnelle (preuve sociale) | `avis logiciel CAC`, `[type de cabinet] + automatisation`, requêtes de marque `CheckIA` |
| Vie de l'entreprise | marque / E-E-A-T | `CheckIA`, `qui a créé CheckIA`, requêtes de confiance |

Règles :
- **Une requête principale par article**, placée en tête du `<title>`, dans le
  `<h1>`, dans la description et dans le premier paragraphe.
- Les requêtes secondaires deviennent des `<h2>` (elles alimentent les
  « People Also Ask ») et des questions de la FAQ.
- Un article = une intention. Si deux intentions, deux articles reliés par
  maillage interne.

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

## Cadence et maillage

- Chaque nouvel article doit recevoir au moins 2 liens internes entrants
  (cartes, pagenav, « À lire ensuite ») et pointer vers 1-2 articles existants
  ainsi que vers la page produit pertinente.
- Mettre à jour `lastmod` (sitemap) et `dateModified` à chaque modification
  substantielle — Google et les LLM privilégient le contenu maintenu.

## Outils

| Commande | Rôle |
|---|---|
| `python3 tools/new-article.py <serie> <slug> "Titre"` | crée un article depuis le gabarit |
| `python3 tools/build-llms.py` | régénère `index.md` + `llms-full.txt` |
| `python3 tools/check-seo.py` | vérifie toutes les règles SEO (0 erreur exigé) |
