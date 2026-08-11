# Audit du site existant — checkia.fr

*Réalisé le 2026-08-11. Sources : ce dépôt (`checkia-inc`, état `main`) et le dépôt produit `checkia-app` (`docs/workflow/`, `docs/manual/`, `docs/cncc/`, `docs/glossary.md`).*

Ce document consigne ce qui a été **conservé**, **supprimé**, **corrigé** et **ajouté** lors de la refonte. Il sert de trace de décision : chaque allégation retirée l'a été pour une raison documentée ici.

---

## 1. Périmètre audité

| Élément | État constaté |
|---|---|
| Pages | `index.html`, `about.html`, `customer-stories.html`, `blog.html`, `404.html`, + 2 articles sous `blog/` |
| Stack | HTML statique, un fichier par page, **bloc `<style>` dupliqué intégralement dans chaque page** |
| Déploiement | GitHub Pages, déploiement par branche (`CNAME` → `www.checkia.fr`), **aucun workflow GitHub Actions**, aucune étape de build |
| Tokens de marque | `--ink:#3C3D47`, `--blue:#165498`, `--cyan:#5AE9FD`, `--grey:#F6F8FC`, Inter (Google Fonts) |
| `robots.txt` | Correct (allow all + référence sitemap) |
| `sitemap.xml` | **4 URL seulement**, toutes en `.html`, sans `lastmod` |
| Données structurées | `Organization` + un second bloc JSON-LD sur l'accueil |
| Métadonnées | Title/description/OG/Twitter/canonical présents et corrects sur l'accueil |
| Images | Référencées en absolu vers `https://www.checkia.fr/images/…` — **le dossier `images/` a été supprimé du dépôt** (suppressions non commitées visibles dans `git status`) |

---

## 2. Constat central : périmètre produit ≠ périmètre affiché

C'est le point le plus important de cet audit.

**Ce que fait CheckIA aujourd'hui**, d'après la spec de workflow canonique (`checkia-app/docs/workflow/mission-caa-workflow.md`, V3 du 2026-06-08), le manuel utilisateur (17 écrans documentés) et le catalogue de templates (9 templates `.docx` en production) :

> Une plateforme de conduite et de production documentaire pour les missions de **commissariat aux apports** et de **commissariat à la transformation** : création de mission, attribution signataire/collaborateur, récupération des données société via **INSEE/INPI** à partir du SIREN, génération des documents de mission depuis des templates hydratés, cycle de validation/signature (collaborateur → CAC → client via Docusign), traçabilité des statuts, fin de mission à l'envoi du rapport.

Les 9 documents réellement produits : fiche d'acceptation, attestations d'indépendance (signataire et collaborateur), préparation budget, lettre de mission, plan de mission, organisation du dossier, lettre d'affirmation, rapport du commissaire aux apports.

**Ce que le site affichait** : « missions CAC », « dossier de travail », « éléments probants », « contrôles qualité », « alignés sur les NEP » — le vocabulaire de l'**audit légal des comptes annuels**, qui est un métier différent et un périmètre que le produit ne couvre pas aujourd'hui.

La page d'accueil disait par ailleurs, correctement, « 2 familles de missions couvertes : Apports et Transformation » — l'information juste était présente mais noyée sous un habillage plus large.

**Décision** : les pages **produit et commerciales** sont strictement cadrées sur apports / transformation. Le contenu **éditorial et pédagogique** peut couvrir l'univers CAC au sens large, sans jamais laisser entendre que le produit exécute ces fonctions.

---

## 3. Allégations retirées ou reformulées

### 3.1 « Conformité CNCC » — **retiré**

Présent dans le pied de page de **toutes** les pages. Formulation qui suggère une conformité validée, voire un agrément, par la Compagnie nationale des commissaires aux comptes. Aucun élément documentaire dans les deux dépôts n'étaye une certification, un agrément ou une validation par la CNCC.

Remplacé par une formulation vérifiable décrivant ce qui existe réellement : des trames de documents construites à partir de la doctrine professionnelle publiée.

### 3.2 « 100 % Alignés sur les NEP » — **retiré**

Trois problèmes cumulés :

1. Un pourcentage de conformité normative n'est pas une grandeur mesurable et n'est pas défendable devant un contrôle qualité.
2. **La mission de commissariat aux apports n'est régie par aucune NEP dédiée.** Son cadre est le **code de commerce** (L. 225-8, L. 225-147, L. 223-9, R. 225-7/8/14, R. 223-6 ; statut : L. 822-1 et L. 822-11). Source : *Avis technique CNCC — Commissariat aux apports* (20/01/2011), vendorisé dans `checkia-app/docs/cncc/`. Les seules NEP citées par l'avis le sont explicitement « pour s'en inspirer » : **NEP 560** (événements postérieurs) et **NEP 620** (intervention d'un expert).
3. Afficher un alignement NEP sur le métier réellement couvert est donc, au mieux, hors sujet — au pire, une erreur technique qu'un CAC repère immédiatement.

Remplacé par le cadre juridique exact, cité avec ses références.

### 3.3 « Infrastructure souveraine » — **mis en attente de confirmation**

L'`ONBOARDING.md` du dépôt produit décrit une distribution par **image Docker tirée depuis un registre AWS ECR `us-east-1`**, déployée sur l'instance du client, avec base SQLite et stockage montés côté client. Ce modèle **auto-hébergé / sur l'infrastructure du cabinet** est un argument de confidentialité fort et réel — mais ce n'est pas la même chose que « infrastructure souveraine », et le registre de distribution est américain.

La section sécurité décrit désormais le modèle de déploiement réel. Les points non vérifiables sont marqués `À CONFIRMER` dans le contenu plutôt qu'affirmés.

### 3.4 Témoignages clients — **retirés**

`customer-stories.html` présentait **six témoignages vidéo** avec durées, mois de publication et un cabinet nommé (**Eurex**), dont un logo « Ils structurent leurs missions avec CheckIA » sur l'accueil. Aucun de ces éléments n'est étayé dans les dépôts, et le produit est décrit comme étant en **alpha** dans sa propre documentation (`docs/manual/00-screens-index.md` : « Screens Index — Alpha Checkia »).

La citation anonyme « Commissaire aux comptes · Cabinet partenaire » n'est pas non plus sourcée.

Ces éléments sont retirés dans l'attente d'accords clients écrits. La page reste dans l'architecture, prête à être remplie.

### 3.5 Blog — **reconstruit**

`blog.html` était **rédigé en anglais** sur un site français ciblant des CAC français, avec des articles fictifs (« Product Update », « Inside CheckIA's Evidence Organization Workflow ») décrivant des fonctionnalités inexistantes (organisation et indexation des éléments probants). Contenu de gabarit non retiré.

Remplacé par un **centre de ressources** structuré par thème, en français, sans article fictif.

---

## 4. Éléments conservés et renforcés

Le positionnement de fond était juste et a été gardé au centre :

- La formalisation absorbe une part majeure du temps de mission → c'est le problème adressé.
- **Le commissaire conserve le jugement** ; l'outil structure et produit, il ne conclut pas. Renforcé en section dédiée.
- Homogénéisation des trames entre dossiers, traçabilité, centralisation.
- Conception avec des praticiens + expertise IA française.
- Cloisonnement des données par cabinet — étayé par le modèle multi-tenant décrit dans le glossaire produit (« une mission appartient à un cabinet et n'est visible que par ses membres »).
- Les tokens de marque (bleu `#165498`, encre `#3C3D47`, Inter) sont conservés ; le système typographique et la grille sont refondus autour d'eux.
- CTA principal inchangé : **Réserver une démonstration**.

---

## 5. Dette technique corrigée

| Problème | Correction |
|---|---|
| Bloc `<style>` dupliqué dans chaque page (~15 ko × N) | Feuille de style partagée unique, mise en cache |
| Aucun moyen d'ajouter une page sans copier-coller tout le châssis | Générateur statique + contenu en Markdown/frontmatter |
| URL en `.html` | URL propres (`/commissariat-aux-apports/`) + redirections depuis les anciennes URL |
| Sitemap à 4 entrées, sans `lastmod` | Sitemap généré, complet, avec `lastmod` |
| Aucun fil d'Ariane, aucun `BreadcrumbList` | Générés automatiquement depuis l'arborescence |
| Site partiellement en anglais | Contenu public intégralement en français |
| Images pointant vers des URL absolues de production, dossier `images/` supprimé du dépôt | Visuels reconstruits en SVG inline versionné (aucune dépendance externe, aucun poids réseau) |
| Aucun `llms.txt` | Généré |

---

## 6. Réserves ouvertes

1. **Le classeur `CheckIA_France_CAC_SEO_AI_Keyword_Strategy.xlsx` n'a pas été fourni** — introuvable sur la machine. L'arborescence a été construite à partir de la liste d'URL du brief et de la connaissance du domaine ; le mappage précis mots-clés → pages reste à recaler à réception du fichier.
2. Métrique « 5 heures → 1 heure » : mentionnée dans le brief comme *potentiellement* publiable. **Non publiée** faute de source dans les dépôts.
3. Statut du produit : la documentation interne le décrit en **alpha**. Le ton du site l'assume (produit conçu avec des cabinets partenaires) sans revendiquer une base installée.
