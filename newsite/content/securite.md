---
url: /securite/
title: Sécurité et confidentialité
group: Produit
type: landing
updated: 2026-08-11
seo:
  title: "Sécurité et confidentialité — Modèle de déploiement | CheckIA"
  description: "CheckIA se déploie sur l'infrastructure de votre cabinet, en instance dédiée. Modèle de déploiement, cloisonnement des données et secret professionnel."

sections:
  - kind: hero
    eyebrow: Sécurité et confidentialité
    title: Vos dossiers ne quittent pas votre infrastructure
    lede: >
      Un commissaire aux comptes est tenu au secret professionnel. Cela
      disqualifie une partie des outils disponibles, et cela justifie de poser
      des questions précises avant d'en adopter un. Cette page répond à ces
      questions — y compris là où la réponse est « à préciser avec vous ».
    ctas:
      - label: Parler à notre équipe
        href: /contact/
      - label: Réserver une démonstration
        href: /demo/
        style: ghost

  - kind: answer
    question: Où sont hébergées les données de mission ?
    body: |
      CheckIA se déploie **sur l'infrastructure du cabinet**, sous forme d'une
      instance dédiée exécutée dans un conteneur. Les données de mission, les
      documents produits et les pièces déposées par le client résident dans cet
      environnement, dont le cabinet garde la maîtrise — y compris le stockage,
      les sauvegardes et la rotation des journaux.

      Ce n'est pas une plateforme mutualisée où les dossiers de plusieurs
      cabinets cohabiteraient dans une même base. C'est une différence de nature,
      pas de configuration.
    points:
      - Le cabinet est l'unité de cloisonnement — une mission n'est visible que par les membres du cabinet auquel elle appartient
      - Le stockage est monté sur un volume dont le cabinet dispose
      - L'image logicielle est distribuée depuis un registre privé ; les données de mission n'y transitent pas

  - kind: cards
    tone: grey
    eyebrow: Modèle de déploiement
    title: Comment le logiciel arrive chez vous
    columns: 3
    items:
      - eyebrow: Distribution
        title: Une image logicielle, pas un accès à un service
        body: >
          Le cabinet reçoit des identifiants lui permettant de récupérer l'image
          applicative depuis un registre privé, puis l'exécute sur son
          instance. Ce qui transite lors de cette étape est le logiciel, pas
          vos dossiers.
      - eyebrow: Exécution
        title: Une instance par cabinet
        body: >
          Chaque cabinet exécute sa propre instance, avec sa propre base et son
          propre stockage. Il n'y a pas de base commune à plusieurs cabinets à
          cloisonner logiquement — le cloisonnement est d'abord physique.
      - eyebrow: Maîtrise
        title: Sauvegardes et journaux chez vous
        body: >
          Le chemin de stockage est monté depuis l'environnement du cabinet.
          Sauvegarde de la base et rotation des journaux relèvent donc de vos
          procédures, sur vos supports.

  - kind: split
    eyebrow: Secret professionnel
    title: Pourquoi le déploiement dédié change la question
    body: |
      La difficulté, avec un assistant généraliste, n'est pas seulement
      contractuelle. C'est qu'un dossier de mission déposé dans un service
      mutualisé quitte le périmètre du cabinet, et que le commissaire perd la
      capacité de démontrer où il se trouve.

      Avec une instance dédiée, la question redevient une question
      d'infrastructure : celle que votre cabinet sait déjà traiter pour son
      serveur de fichiers et sa messagerie.
    points:
      - Les documents de mission restent dans l'environnement du cabinet
      - L'accès aux missions est restreint aux membres du cabinet
      - Les comptes utilisateurs et l'attribution des missions sont administrés par le cabinet
    ctas:
      - label: IA et jugement professionnel
        href: /ia-et-jugement-professionnel/
        style: ghost

  - kind: table
    tone: grey
    eyebrow: Transparence
    title: Ce qui est établi, et ce qui reste à préciser avec vous
    lede: >
      Nous préférons une page incomplète à une page rassurante. Les éléments
      marqués « à préciser » ne sont pas des lacunes cachées : ce sont des
      points qui dépendent de votre environnement ou qui doivent être
      documentés contractuellement plutôt qu'affirmés sur une page web.
    head: [Sujet, État]
    rows:
      - ["Lieu d'exécution des données de mission", "Infrastructure du cabinet, en instance dédiée."]
      - ["Cloisonnement entre cabinets", "Instances distinctes ; le cabinet est l'unité d'accès aux missions."]
      - ["Signature électronique du client", "Assurée via Docusign."]
      - ["Sources de données externes interrogées", "INSEE et INPI, à partir du SIREN, pour l'identification des sociétés."]
      - ["Fournisseur de modèle d'IA et politique d'entraînement", "À préciser avec notre équipe — nous documentons ce point par écrit dans le cadre contractuel plutôt que sur cette page."]
      - ["Chiffrement au repos et en transit", "À préciser selon la configuration de votre environnement."]
      - ["Politique de conservation et de purge", "À définir avec le cabinet, le stockage étant sous sa maîtrise."]
      - ["Certifications (ISO 27001, SecNumCloud, HDS)", "Aucune certification n'est revendiquée à ce jour."]
      - ["Sous-traitants ultérieurs", "Liste communiquée dans le cadre contractuel."]
    note: >
      Si un point manquant est bloquant pour votre cabinet, écrivez-nous : nous
      préférons répondre précisément par écrit plutôt que de compléter cette
      page par une formule générale.

  - kind: faq
    eyebrow: Questions
    title: Ce que demandent les responsables informatiques
    items:
      - q: CheckIA est-il un service en ligne mutualisé ?
        a: >
          Non. Le modèle est un déploiement dédié sur l'infrastructure du
          cabinet. C'est le point de départ de toutes les autres réponses de
          cette page.
      - q: Que se passe-t-il si nous cessons d'utiliser CheckIA ?
        a: >
          La base et le stockage sont sur votre infrastructure. Vous en
          conservez la maîtrise. Les modalités précises de fin de contrat sont
          traitées dans le cadre contractuel.
      - q: Des données de mission sont-elles envoyées à CheckIA ?
        a: >
          Le fonctionnement nominal de la plateforme n'implique pas de transfert
          de vos dossiers vers nos systèmes. Les échanges avec des services
          externes — registres publics, signature électronique, traitement par
          modèle d'IA — sont énumérés dans le tableau ci-dessus ; le détail des
          flux est documenté contractuellement.
      - q: Pouvons-nous conduire un audit de sécurité avant déploiement ?
        a: >
          Oui, et c'est une demande légitime pour un cabinet soumis au secret
          professionnel. Prenez contact avec notre équipe pour en définir le
          périmètre.
      - q: Le RGPD est-il couvert ?
        a: >
          Le cabinet reste responsable de traitement pour les données de ses
          missions. Notre rôle et nos obligations sont précisés dans la
          documentation contractuelle, qui vous est communiquée avant
          déploiement.

  - kind: cta
    title: Poser vos questions de sécurité avant la démonstration
    lede: Nous répondons volontiers par écrit, en amont, à un questionnaire de sécurité.
    ctas:
      - label: Nous écrire
        href: /contact/
      - label: Réserver une démonstration
        href: /demo/
        style: ghost
---
