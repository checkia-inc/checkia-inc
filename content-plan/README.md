# Plan éditorial CheckIA — mode d'emploi

Ce dossier contient le plan de contenu du blog et du site pour douze mois (septembre 2026
à août 2027). Le plan vit dans le dépôt ; vous le lisez dans Google Sheets ; vous décidez
dans un onglet dédié ; l'agent (Claude Code) exécute chaque pièce en suivant `AGENTS.md`.

## À quoi sert ce dossier

- `briefs/` : un fichier par pièce (article, vidéo, entretien, témoignage, rafraîchissement,
  action hors site). Chaque brief répond d'avance aux questions d'intake d'`AGENTS.md` :
  type, série, titre de travail, angle, requête cible, questions à traiter, faits sourcés,
  auteur, image, appel à l'action, conditions, statut, dates.
- `plan.csv` et `plan-editorial.xlsx` : générés par `python3 tools/plan.py build`. Ne pas
  les modifier à la main.
- `produit-verite.md` : ce que le produit fait aujourd'hui et ce qui est prévu. Toute
  affirmation sur le produit dans un article doit s'y conformer.
- `decisions-exemple.csv` : exemple du format attendu pour l'onglet « Décisions ».

## Le tableur Google Sheets

Nom conseillé : « Plan éditorial CheckIA ». Trois onglets.

1. **Plan (repo)** — miroir du dépôt, en lecture seule. Cellule A1 :

   ```
   =IMPORTDATA("https://raw.githubusercontent.com/checkia-inc/checkia-inc/main/content-plan/plan.csv?v=" & Réglages!B1; ","; "fr_FR")
   ```

   Le miroir se rafraîchit environ toutes les heures. Pour forcer une mise à jour,
   incrémenter la cellule `Réglages!B1` (Version). Ne rien saisir dans cet onglet : il est
   écrasé à chaque rafraîchissement.

2. **Décisions** — le seul onglet que vous modifiez. Colonnes, dans cet ordre :
   `id | Statut décidé | Commentaire | Décidé par | Date`. Deux façons de l'utiliser, au
   choix : une ligne par pièce (l'id en colonne A, le statut décidé dans la liste
   déroulante en B, que l'on change au fil du temps) ou une ligne par décision. Les
   options de la liste déroulante peuvent porter une explication après un tiret
   (« Brief validé — lance la rédaction ») : seul le libellé avant le tiret compte. Seules
   les décisions humaines sont appliquées (Brief validé, Prêt à publier, À rafraîchir,
   Archivé) et uniquement dans le sens du flux : une cellule restée sur « Brief validé »
   alors que la pièce est déjà publiée est ignorée. Deux colonnes d'aide à droite :

   ```
   F2 : =IFERROR(VLOOKUP(A2; 'Plan (repo)'!A:G; 7; FALSE); "")   → Titre
   G2 : =IFERROR(VLOOKUP(A2; 'Plan (repo)'!A:B; 2; FALSE); "")   → Statut actuel
   ```

   Validation des données sur « Statut décidé » : Idée, Brief validé, En attente (condition),
   Rédaction, Relecture humaine, Prêt à publier, Publié, À rafraîchir, Archivé.

   Publier cet onglet : Fichier → Partager → Publier sur le web → onglet Décisions → CSV.
   Coller l'URL obtenue ci-dessous ; l'agent la lit au début de chaque session.

   URL CSV publiée de l'onglet Décisions :
   https://docs.google.com/spreadsheets/d/e/2PACX-1vSvUrUmRGW210fN6F6-5VV1biiCwNgi_l2zac37DQ2WTAQgPw4X9Pj8pb5kAL95GnZNoiUiYXGggtQX/pub?gid=1362190869&single=true&output=csv

3. **Réglages** — la cellule Version (B1) et les deux URL.

Secours : si IMPORTDATA ne fonctionne pas, importer `plan-editorial.xlsx` (Fichier →
Importer → Remplacer la feuille active) ; l'agent peut aussi lire un export CSV de l'onglet
Décisions avec `python3 tools/plan.py sync-sheet --file decisions.csv`.

## Décider

| Statut | Qui décide | Ce que fait l'agent ensuite |
|---|---|---|
| Idée | tout le monde | Enrichit le brief (requêtes, questions, sources). Rien dans le blog. |
| Brief validé | **humain** | Lit les articles publiés, génère le squelette, rédige. |
| En attente (condition) | agent ou humain | Rien sur la pièce tant qu'une condition est à « non ». |
| Rédaction | agent | Rédige l'article en `noindex`, images, liens, vérifications, `social.md`. |
| Relecture humaine | agent | Applique vos retours (Journal ou Décisions). Ne publie jamais. |
| Prêt à publier | **humain** | Vaut « oui » à « Prêt à publier ? » : mise en ligne complète, puis statut Publié. |
| Publié | agent | Vérifie les citations par les assistants IA à J+7 et J+30. |
| À rafraîchir | humain, ou agent avec motif | Prépare le rafraîchissement, le soumet en relecture. |
| Archivé | **humain** | Rien. |

Pour décider, ajoutez une ligne dans Décisions : l'id (ex. `P014`), le statut décidé, un
commentaire éventuel, votre prénom, la date. Pour donner un retour sans changer le statut,
laissez « Statut décidé » vide et écrivez le commentaire.

## Lire un brief

Les briefs sont dans `content-plan/briefs/` sur GitHub. Les champs à regarder en priorité :
`requete` (la requête cible, une seule par article), `questions` (les questions que
l'article doit traiter, formulées comme un commissaire aux comptes les tape), `faits`
(trois faits datés et sourcés au minimum), `conditions` (ce qui doit être vrai avant de
publier, par exemple « fonctionnalité en production — ok »), `auteur`.

## Proposer une idée

Ajoutez une ligne dans Décisions avec l'id vide et le titre dans « Commentaire ». L'agent
crée le brief au statut Idée lors de la synchronisation suivante.

## Vérité produit

`produit-verite.md` liste ce que CheckIA fait aujourd'hui et ce qui est prévu. Mettez-le à
jour **avant** toute communication sur une nouvelle fonctionnalité ; l'agent refuse un
article produit qui décrit une fonctionnalité absente de la section « En production ».

## Commandes utiles (pour l'agent, ou pour vous en ligne de commande)

```bash
python3 tools/plan.py next            # ce que l'agent doit faire maintenant
python3 tools/plan.py list --mois 2026-10
python3 tools/plan.py show P014
python3 tools/plan.py check           # cohérence du plan et du site (0 erreur attendu)
python3 tools/plan.py build           # régénère plan.csv et plan-editorial.xlsx
```
