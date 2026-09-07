# Vérité produit — ce que CheckIA fait aujourd'hui

Dernière mise à jour : 2026-09-07 — établie à partir du code (dépôt `checkia-app`,
commit 98e54de du 4 septembre 2026). **À valider par Jean-David Collard** avant toute
communication sur une fonctionnalité : les lignes marquées « à confirmer » ne sont pas
tranchées.

Règle : un article ne décrit comme disponible que ce qui figure sous « En production ».
Ce qui figure sous « Feuille de route » se dit « prévu », avec une échéance, jamais au présent.
Les identifiants entre crochets sont ceux à reporter dans le champ `fonctionnalites` des briefs ;
`tools/plan.py check` vérifie la correspondance.

## En production

- [pre-remplissage-registres] Pré-remplissage automatique de la mission à partir du SIREN : dénomination, forme juridique, capital, objet social, adresse, code APE, effectifs et représentants légaux, via INSEE Sirene et INPI RNE — depuis 2026-06
- [donnees-mission] Modèle de données structuré de la mission (sociétés apporteuse et bénéficiaire, associés, répartition du capital, honoraires, dates, signataire et collaborateur) avec écran de revue et corrections manuelles conservées — depuis 2026-07
- [generation-documentaire] Génération des documents du commissariat aux apports à partir des données de la mission, selon les trames du cabinet : fiche d'acceptation, attestations d'indépendance (collaborateur et signataire), lettre de mission, préparation du budget, plan de mission, organisation du dossier, lettre d'affirmation, rapport du commissaire aux apports — depuis 2026-05
- [mission-apport-titres] Mission « apport de titres » (commissariat aux apports) complète — depuis 2026-05
- [mission-apport-nature] Mission « apport en nature » ouverte, sur les mêmes trames que l'apport de titres — à confirmer (trames dédiées à venir)
- [workflow-etapes] Parcours de mission en six étapes (acceptation, contractualisation, planification, travaux, restitution) avec verrouillage de l'étape Travaux — depuis 2026-08
- [validation-documents] Validation et retrait de validation de chaque document, avec auteur et horodatage, et report des dates de validation dans les documents générés — depuis 2026-07
- [historique-validations] Historique horodaté des validations et dévalidations, consultable document par document — depuis 2026-07
- [editeur-docx] Éditeur DOCX natif (pagination, tableaux) et export PDF — depuis 2026-08
- [pieces-dossier] Dépôt et classement des pièces du dossier (Kbis, statuts, comptes annuels, contrat d'apport, documents client, PV de désignation) avec règles de complétude avant génération — depuis 2026-07
- [recherche-missions] Recherche, filtres (collaborateur, signataire, dates) et tri de la liste des missions ; vue cartes ou tableau — depuis 2026-07
- [cloisonnement-cabinet] Cloisonnement strict des données par cabinet ; rôles utilisateur, administrateur de cabinet, administrateur plateforme ; désactivation d'un cabinet — depuis l'origine
- [identifiants-inpi-chiffres] Identifiants INPI/RNE propres à chaque cabinet, chiffrés (AES-256-GCM) — depuis 2026-07
- [guide-professionnel] Guide professionnel contextuel par étape (références CNCC et Code de commerce, version 1 à affiner) — depuis 2026-08
- [hebergement-france] Hébergement et traitement des données en France (AWS, région Paris), stockage chiffré, sauvegardes conservées 180 jours, aucun port entrant ouvert — depuis l'origine
- [aucune-ia-externe] Aucune donnée de mission transmise à un fournisseur d'intelligence artificielle externe — vrai à ce jour ; à réévaluer dès l'intégration de l'IA (T4 2026)

## Feuille de route (ne jamais présenter comme disponible)

- [ia-assistance] Assistance par intelligence artificielle dans la préparation des documents — prévu T4 2026 ; les articles produit sur ce sujet portent la condition « fonctionnalité en production »
- [mission-transformation] Commissariat à la transformation — annoncé dans l'application (« Bientôt disponible »), à confirmer
- [audit-legal] Audit légal — annoncé (« Bientôt disponible »), sans date
- [signature-electronique] Signature électronique des documents — prévu (Beta 2)
- [extraction-pieces] Extraction automatique d'informations à partir des pièces déposées (OCR) — prévu (Beta 2)
- [recherche-entreprise] Recherche d'entreprise intégrée — prévu (Beta 2)
- [sso] Authentification unique (SSO) — non planifié
- [mission-fusion] Commissariat à la fusion — non planifié

## Formulations validées

- « CheckIA automatise la préparation documentaire, sans jamais se substituer au jugement professionnel du commissaire aux comptes. »
- « Les données sont hébergées et traitées en France (AWS, région Paris). »
- « Aucune donnée de mission n'est transmise à un fournisseur d'intelligence artificielle externe. » (tant que [aucune-ia-externe] est vrai)
- « jusqu'à 80 % du temps de formalisation » — uniquement avec son périmètre : « sur les missions spécifiques couvertes, selon nos mesures internes » ; chiffre repris du site existant, méthode de mesure à documenter

## Formulations à éviter dans les nouveaux contenus

- « infrastructure souveraine », « cloud souverain » → dire « hébergé en France (AWS Paris) »
- « conforme aux NEP » sans nuance → dire « conçu dans le respect des exigences des NEP »
- Toute référence aux NEP 9010 à 9070 (diligences directement liées) tant que leur statut n'est pas confirmé par la CNCC → dire « interventions à la demande de l'entité dans le cadre des SACC »
- « l'IA extrait », « l'IA rédige », « OCR », « signature électronique », « audit légal », « transformation » comme fonctionnalités disponibles
- Tout chiffre de gain de temps sans périmètre ni date
