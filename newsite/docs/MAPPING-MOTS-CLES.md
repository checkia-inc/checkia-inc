# Réconciliation du classeur SEO avec le périmètre produit

*Source : `checkia_Keyword.xlsx`, 10 feuilles, 3 125 mots-clés master + 633 long-tail + 937 prompts IA. Analysé le 2026-08-11.*

Ce document explique comment le classeur a été utilisé — et pourquoi il ne l'a pas été tel quel.

---

## 1. Le constat central

Le classeur a été construit pour le marché de **l'audit légal des comptes annuels**. CheckIA couvre le **commissariat aux apports et à la transformation**.

Mesure exacte de l'intersection :

| Feuille | Lignes | Lignes dans le périmètre produit | Part |
|---|---|---|---|
| Master Keywords | 3 125 | **52** | 1,7 % |
| Long Tail | 633 | 10 | 1,6 % |
| AI Search Prompts | 937 | 10 | 1,1 % |
| Semantic Entities | 214 | 0 | 0 % |
| Content Gaps | 25 | 0 | 0 % |
| Site Architecture | 83 pages | **0** | 0 % |
| Competitors | 9 | 2 (substituts) | 22 % |

Les 52 mots-clés en périmètre sont **tous** dans un seul cluster : `Missions spéciales du CAC`, rattaché au pilier `/missions-speciales-cac/`.

### Trois anomalies du classeur, relevées et corrigées

**1. Le pilier `/missions-speciales-cac/` n'existe pas dans la feuille Site Architecture.** La feuille Master Keywords y rattache 52 mots-clés ; la feuille Site Architecture, qui décrit 83 pages, n'en comporte aucune. Le seul cluster correspondant au produit réel est donc orphelin de l'architecture recommandée.

**2. Le Priority Score déprioriserait systématiquement le seul cluster pertinent.** Le score est corrélé au volume et à l'intention commerciale moyenne du cluster :

| Cluster | Mots-clés | Intention commerciale moy. | Dans le périmètre produit ? |
|---|---|---|---|
| NEP et conformité | 548 | 3,0 | Non |
| Logiciel CAC | 124 | 7,7 | Non |
| Concurrents et alternatives | 236 | 7,0 | Non |
| **Missions spéciales du CAC** | **52** | **3,4** | **Oui** |

Suivre le Priority Score revient à construire le site d'un autre produit. Le score a donc été utilisé **à l'intérieur** du cluster pertinent, pas entre clusters.

**3. Le gabarit long-tail impose « conformément aux NEP » à des requêtes hors NEP.** Les feuilles Long Tail et AI Search Prompts sont générées par gabarit : 10 variantes par graine, dont « Comment X **conformément aux NEP** ? ». Appliqué à `préparer un rapport de commissaire aux apports`, cela produit une question dont la prémisse est fausse — la mission n'est régie par aucune NEP dédiée (voir [l'audit](./AUDIT-SITE-EXISTANT.md), §3.2). Ces formulations n'ont pas été reprises telles quelles.

---

## 2. Ce qui a été retenu du classeur

### 2.1 Le cluster en périmètre, par Priority Score

| Score | Mot-clé | Intention | Page cible |
|---|---|---|---|
| 64 | logiciel commissaire aux apports **prix** | Transactional | `/logiciel-commissaire-aux-apports/` |
| 64 | logiciel commissaire aux apports **démonstration** | Transactional | `/logiciel-commissaire-aux-apports/` |
| 58 | automatiser rapport mission spéciale | Informational | `/logiciel-commissaire-aux-apports/` |
| 55 | mission spéciale CAC | Informational | `/missions-speciales-cac/` |
| 55 | logiciel commissaire aux apports **avis** | Commercial | `/logiciel-commissaire-aux-apports/` |
| 52 | logiciel commissaire aux apports | Commercial | `/logiciel-commissaire-aux-apports/` |
| 49 | commissaire aux apports | Informational | `/commissariat-aux-apports/` |
| — | rapport commissaire aux apports · modèle rapport apports | Informational | `/commissariat-aux-apports/rapport/` |
| — | évaluation apports | Informational | `/commissariat-aux-apports/evaluation-des-apports/` |
| — | dossier travail commissaire aux apports | Informational | `/commissariat-aux-apports/dossier-de-travail/` |
| — | commissaire à la transformation · rapport commissaire à la transformation | Informational | `/commissariat-a-la-transformation/` |
| — | transformation SARL SAS commissaire · programme travail commissaire transformation | Informational | `/commissariat-a-la-transformation/sarl-en-sas/` |
| — | fusion commissaire aux apports · scission commissaire aux apports | Informational | `/commissariat-a-la-fusion/` |
| — | augmentation capital apports · mission apport en nature | Informational | `/commissariat-aux-apports/` |
| — | avantages particuliers | Informational | `/commissariat-aux-apports/evaluation-des-apports/` |

**« logiciel commissaire aux apports » et ses variantes prix / avis / démonstration sont les seuls mots-clés transactionnels du classeur qui correspondent réellement au produit.** C'est le manque le plus coûteux de la phase 1 — la page a été créée.

### 2.2 Concurrents retenus — et écartés

La feuille Competitors liste 7 concurrents directs (RevisAudit Premium, DreamAudit, AuditSoft Premier, Caseware, Intelligent Audit, CACAO, Acropole Expert CAC). **Aucun n'est un concurrent de CheckIA sur les missions d'apport** : ce sont des outils de dossier de travail pour la certification des comptes annuels. Publier « alternative à RevisAudit » attirerait un acheteur que le produit ne peut pas servir, et provoquerait la déception au premier contact commercial.

Les **deux substituts** de la feuille sont en revanche exactement les bons concurrents :

| Substitut | Page construite |
|---|---|
| Excel + Word + dossiers | `/comparatif/excel-word-vs-logiciel-de-mission/` |
| ChatGPT / Claude / Gemini | `/comparatif/chatgpt-vs-logiciel-de-mission/` |

### 2.3 Content Gaps transposables

Sur 25 gaps, la plupart supposent le périmètre certification (NEP 230/315/330/600/911/912, FEC, OCR, CSRD, revue analytique). Quatre sont transposables tels quels parce qu'ils portent sur l'IA et la confiance, pas sur le type de mission :

| Gap du classeur | Transposition |
|---|---|
| Secret professionnel et fournisseurs de LLM | `/securite/secret-professionnel-et-ia/` |
| « Prompting n'est pas documentation » | Traité dans `/ia-et-jugement-professionnel/` et `/comparatif/chatgpt-vs-logiciel-de-mission/` |
| Audit trail des décisions humaines et IA | Traité dans `/produit/validation-signature/` |
| Mesure du coût de la documentation | `/productivite-cabinet/cout-de-la-formalisation/` |
| FAQ conversationnelle · Glossaire | Déjà construits en phase 1 |

### 2.4 Gabarit long-tail → blocs FAQ, pas pages

Les 10 variantes par graine (« Comment X ? », « Quelles bonnes pratiques pour X ? », « Quel logiciel permet de X ? », « Comment gagner du temps pour X ? », « Quels documents conserver pour X ? »…) satisfont **la même intention**. Conformément à la règle « si 20 mots-clés sont satisfaits par une page excellente, construire une page », elles alimentent les blocs `faq` des pages concernées — jamais une page par variante.

---

## 3. Ce que le classeur ne couvre pas, et qu'il a fallu ajouter

Recherche exacte sur les termes du métier, toutes feuilles confondues :

| Terme | Occurrences dans le classeur |
|---|---|
| traité d'apport | **0** |
| société apporteuse / bénéficiaire des apports | **0** |
| surévaluation | **0** |
| commissariat à la fusion | **0** |
| apports en nature (dispense, seuil 30 000 €, moitié du capital) | **0** |
| capitaux propres au sens de la transformation | **0** |
| société apporteuse personne physique / fonds de commerce | **0** |

Ce sont les questions qu'un commissaire aux apports se pose réellement, et celles qu'un dirigeant ou un avocat tape avant de désigner un professionnel. L'univers de mots-clés du niche a donc été étendu au-delà du classeur, à partir de la doctrine (avis technique CNCC, guide Apports-Fusion) et des textes (code de commerce).

---

## 4. Entités sémantiques

La feuille Semantic Entities (214 entités) est orientée certification. Les entités retenues et effectivement couvertes sur le site :

**Organisations** — H2A (et H3C en historique), CNCC, CRCC, INSEE, INPI.
**Textes** — code de commerce (L. 225-8, L. 225-147, L. 223-9, L. 224-3, L. 227-1, L. 227-3, L. 223-43, R. 225-7/8/14, R. 223-6, L. 822-1, L. 822-11), avis technique CNCC 2011, guide Apports-Fusion 2012.
**Documents** — traité d'apport, lettre de mission, fiche d'acceptation, attestation d'indépendance, plan de mission, organisation du dossier, lettre d'affirmation, rapport du commissaire aux apports, lettre de refus.
**Concepts** — apport en nature, avantages particuliers, surévaluation, capitaux propres, capital social, prime d'émission, société apporteuse, société bénéficiaire, dispense, responsabilité solidaire quinquennale, jugement professionnel, traçabilité.

Entités du classeur **volontairement non revendiquées** côté produit (traitées uniquement en pédagogie si un jour utile) : NEP 230/315/330/500/520/600/700, FEC, circularisation, échantillonnage, CSRD, ESRS, contrôle interne, continuité d'exploitation.

---

## 5. Recommandation sur le classeur

Le classeur reste utile — mais pour un autre produit que celui d'aujourd'hui. Deux usages possibles :

1. **Si le périmètre produit s'élargit** à la certification des comptes, le classeur redevient la feuille de route directe et l'architecture des 83 pages s'applique.
2. **En l'état**, il sert de carte du marché adjacent : il indique ce que cherchent les CAC en général, donc les sujets sur lesquels CheckIA peut construire une autorité pédagogique sans revendiquer de fonctionnalité.

Une v2 du classeur centrée sur le périmètre réel devrait développer les sept termes à zéro occurrence du §3 — c'est là que se trouve la demande non servie.
