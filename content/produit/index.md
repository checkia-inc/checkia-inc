---
url: /produit/
title: La plateforme
breadcrumb_label: Produit
group: Produit
type: landing
updated: 2026-08-11
schema: [SoftwareApplication]
seo:
  title: "La plateforme CheckIA — Conduite d'une mission d'apport"
  description: "Création de mission, données société via INSEE et INPI, production documentaire depuis vos trames, validation et signature tracées jusqu'au rapport."

sections:
  - kind: hero
    eyebrow: Vue d'ensemble
    title: Une mission d'apport, conduite de bout en bout
    lede: >
      CheckIA n'est pas une bibliothèque de modèles ni un assistant de rédaction.
      C'est le déroulé d'une mission de commissariat aux apports, transposé dans
      un logiciel : les étapes, les documents attendus à chaque étape, et le
      circuit de validation qui les fait avancer.
    visual: pipeline
    ctas:
      - label: Réserver une démonstration
        href: /demo/
      - label: Voir la génération documentaire
        href: /produit/generation-documentaire/
        style: ghost

  - kind: answer
    question: Que fait exactement la plateforme ?
    body: |
      CheckIA prend en charge quatre choses : l'**ouverture et l'attribution**
      de la mission, la **collecte et la vérification des données** des sociétés
      concernées, la **production des neuf documents de mission** à partir des
      trames du cabinet, et le **circuit de validation et de signature** qui va
      du collaborateur au commissaire puis au client.

      Ce qu'elle ne fait pas : évaluer les apports, apprécier une méthode
      d'évaluation, conclure sur l'absence de surévaluation, signer. Ces actes
      relèvent du commissaire.

  - kind: steps
    tone: grey
    eyebrow: Le déroulé
    title: Les cinq étapes, et ce que fait la plateforme à chacune
    items:
      - title: Ouverture et attribution
        body: >
          L'administrateur du cabinet dépose le procès-verbal de désignation,
          crée la mission, puis désigne le signataire et le collaborateur parmi
          les comptes du cabinet. Les deux sont notifiés. Un conflit d'intérêts
          déclaré plus tard ramène la mission à cette étape pour réattribution.
        meta: Cadre de mission — société concernée, type de mission, temps prévu, honoraires, dates
      - title: Données de mission
        body: >
          Le collaborateur renseigne l'identification de la société apporteuse
          et de la société bénéficiaire. À partir du SIREN, la plateforme
          interroge l'INSEE et l'INPI et pré-remplit dénomination, forme
          juridique, adresse du siège et activité. Une société en cours
          d'immatriculation se saisit à la main. Le collaborateur vérifie
          l'ensemble avant de continuer.
        meta: Répartition du capital saisie en actionnaires ou en associés selon la forme juridique
      - title: Acceptation
        body: >
          Trois documents en parallèle : attestation d'indépendance du
          signataire, attestation d'indépendance du collaborateur, fiche
          d'acceptation de mission. C'est le point où la mission peut s'arrêter —
          conflit d'intérêts déclaré par l'un ou l'autre, ou refus de la mission
          par le commissaire, qui produit alors la lettre de refus.
        meta: Étape 1
      - title: Contractualisation, puis planification
        body: >
          Lettre de mission et préparation du budget, puis plan de mission et
          organisation du dossier. La lettre de mission suit le circuit complet :
          validation interne, signature du commissaire, envoi au client pour
          signature électronique, retour au dossier.
        meta: Étapes 2 et 3
      - title: Travaux, puis restitution
        body: >
          Les documents de travail sont créés dans la plateforme ou importés
          depuis le poste du collaborateur, sans limite de nombre pratique. La
          restitution enchaîne la lettre d'affirmation, signée par le client, et
          le rapport, signé par le commissaire puis adressé au client — ce qui
          clôt la mission.
        meta: Étapes 4 et 5 — le rapport ne peut partir avant le retour signé de la lettre d'affirmation

  - kind: cards
    eyebrow: Les briques
    title: Ce que vous manipulez au quotidien
    columns: 3
    items:
      - eyebrow: Données
        title: Identification alimentée par les registres
        body: >
          INSEE et INPI interrogés par SIREN. Le pré-remplissage fait gagner la
          saisie ; l'étape de vérification garantit que rien n'entre dans un
          document sans avoir été regardé.
      - eyebrow: Documents
        title: Vos trames, alimentées
        body: >
          Les modèles Word du cabinet sont déposés une fois, les emplacements à
          alimenter identifiés, puis remplis à chaque mission avec les données
          déjà vérifiées.
        href: /produit/generation-documentaire/
        link_label: Voir en détail
      - eyebrow: Édition
        title: Reprise directe dans le navigateur
        body: >
          Chaque document produit s'ouvre dans un éditeur, avec enregistrement
          automatique. Le collaborateur reprend le texte là où il doit être
          repris, sans aller-retour de fichiers.
      - eyebrow: Circuit
        title: Validation, signature, retour client
        body: >
          Validation interne du collaborateur, signature du commissaire,
          signature électronique du client par Docusign. Chaque passage est
          daté et attribué.
        href: /produit/validation-signature/
        link_label: Voir le circuit
      - eyebrow: Dossier
        title: Documents de mission et documents client séparés
        body: >
          Les pièces reçues du client et les documents produits par le cabinet
          sont distingués dans le dossier, ce qui évite de chercher l'origine
          d'une pièce six mois plus tard.
      - eyebrow: Suivi
        title: Un tableau de bord des missions
        body: >
          L'état d'avancement de chaque mission du cabinet, sans avoir à ouvrir
          les dossiers un par un ni à relancer par courriel pour savoir où en
          est un document.

  - kind: split
    tone: grey
    eyebrow: Périmètre
    title: Ce que CheckIA ne fait pas
    body: |
      Nous préférons l'écrire noir sur blanc plutôt que de le laisser découvrir
      en démonstration.

      CheckIA ne procède à aucune évaluation d'apport et n'apprécie pas la
      pertinence d'une méthode d'évaluation. Il ne conclut pas sur l'absence de
      surévaluation. Il ne couvre pas aujourd'hui l'audit légal des comptes
      annuels, ni le commissariat à la fusion, ni la certification des
      informations en matière de durabilité.
    points:
      - Aucune opinion, aucune conclusion produite par la machine
      - Pas de mission de certification des comptes annuels
      - Pas de dépôt automatisé au greffe
      - Les diligences restent celles du commissaire
    ctas:
      - label: Notre position sur l'IA et le jugement
        href: /ia-et-jugement-professionnel/
        style: ghost

  - kind: faq
    eyebrow: Questions
    title: Sur le fonctionnement
    items:
      - q: Peut-on importer des documents de travail existants ?
        a: >
          Oui. À l'étape des travaux, les documents peuvent être créés dans la
          plateforme ou importés depuis le poste du collaborateur. Ces
          documents-là ne suivent pas de circuit de validation : ils constituent
          le dossier de travail.
      - q: Que se passe-t-il si le commissaire refuse de signer un document ?
        a: >
          Pour la fiche d'acceptation, la lettre de mission et le rapport, le
          signataire peut renvoyer le document en rédaction plutôt que le
          signer. Il repasse alors à l'état « à valider » et le collaborateur le
          reprend. L'aller-retour reste inscrit dans l'historique du document.
      - q: Le collaborateur peut-il revenir sur sa propre validation ?
        a: >
          Oui, tant que le document n'est pas signé. C'est le seul changement
          d'état réversible de la plateforme : un document validé peut être
          repassé en rédaction par le collaborateur qui l'a validé.
      - q: Comment sont gérés les utilisateurs du cabinet ?
        a: >
          Les comptes appartiennent au cabinet, qui est l'unité de cloisonnement
          de la plateforme. Une mission appartient à un cabinet et n'est
          visible que par ses membres. L'attribution du signataire et du
          collaborateur se fait parmi ces comptes.

  - kind: cta
    title: Voir la plateforme sur une mission
    lede: Une démonstration sur le déroulé complet d'une mission d'apport, avec vos trames si vous le souhaitez.
    ctas:
      - label: Réserver une démonstration
        href: /demo/
---
