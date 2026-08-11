---
url: /produit/validation-signature/
title: Validation et signature
group: Produit
type: landing
updated: 2026-08-11
seo:
  title: "Validation et signature — Le circuit du dossier | CheckIA"
  description: "Validation du collaborateur, signature du commissaire, signature électronique du client. Chaque état est daté et attribué, y compris les renvois en rédaction."

sections:
  - kind: hero
    eyebrow: Validation et signature
    title: Rien n'avance sans que quelqu'un l'ait décidé
    lede: >
      Chaque document de mission suit un cycle explicite, du premier jet à la
      signature. Le passage d'un état au suivant est un acte humain, attribué et
      daté. Reconstituer la chronologie d'un dossier ne devrait pas demander de
      relire six mois de courriels.
    visual: lifecycle
    ctas:
      - label: Réserver une démonstration
        href: /demo/
      - label: Revenir à la vue d'ensemble
        href: /produit/
        style: ghost

  - kind: answer
    question: Comment un document circule-t-il dans CheckIA ?
    body: |
      Un document naît à l'état **à valider**. Le collaborateur le reprend, puis
      le **valide**. Il passe alors **en attente de signature** et le
      commissaire est notifié. Une fois **signé**, il est soit versé au dossier,
      soit envoyé au client pour signature électronique — il devient alors
      **signé par le client**.

      Deux retours en arrière existent. Le collaborateur peut repasser en
      rédaction un document qu'il a lui-même validé, tant qu'il n'est pas signé.
      Et sur trois documents — fiche d'acceptation, lettre de mission, rapport —
      le commissaire peut renvoyer le document **à mettre à jour** au lieu de le
      signer.

  - kind: table
    tone: grey
    eyebrow: Les états
    title: Les sept états d'un document
    head: [État, Qui agit, Ce que cela signifie]
    rows:
      - ["À valider", "Collaborateur", "Le document est produit ou repris, il n'a encore été validé par personne."]
      - ["Validé", "Collaborateur", "Validation interne faite. Le commissaire est notifié s'il doit signer."]
      - ["En attente de signature", "Commissaire", "Le document attend la signature du commissaire. C'est aussi le point où un conflit d'intérêts ou un refus de mission peut être déclaré."]
      - ["Signé", "Commissaire", "Signature apposée. Le document part au client s'il doit lui être adressé."]
      - ["En attente signature client", "Client", "Envoyé au client pour signature électronique via Docusign."]
      - ["Signé par le client", "Client", "Retour signé. Le document est versé au dossier."]
      - ["À mettre à jour", "Commissaire", "Le commissaire renvoie le document en rédaction plutôt que de le signer. Réservé à la fiche d'acceptation, à la lettre de mission et au rapport."]
    note: >
      Un document déjà signé ne redevient pas modifiable. Le seul changement
      d'état réversible est le retour de « validé » à « à valider » par le
      collaborateur qui a validé.

  - kind: cards
    eyebrow: Les circuits
    title: Tous les documents ne suivent pas le même chemin
    lede: >
      Le circuit dépend de qui doit engager sa responsabilité sur le document.
      Un budget interne n'appelle pas de signature ; une lettre de mission
      engage le cabinet et le client.
    columns: 2
    items:
      - eyebrow: Validation interne seule
        title: Budget, plan de mission, organisation du dossier
        body: >
          Le collaborateur valide, le commissaire est notifié. Pas de signature :
          ces documents structurent le travail, ils ne l'engagent pas
          vis-à-vis d'un tiers.
      - eyebrow: Signature du commissaire
        title: Attestations d'indépendance, fiche d'acceptation
        body: >
          Validation interne, puis signature du commissaire. Sur la fiche
          d'acceptation, c'est le moment où la mission peut être refusée.
      - eyebrow: Double signature
        title: Lettre de mission
        body: >
          Validation interne, signature du commissaire, envoi au client pour
          signature électronique, retour au dossier. Le seul document à parcourir
          l'ensemble du circuit.
      - eyebrow: Signature du client seule
        title: Lettre d'affirmation
        body: >
          Validée en interne puis adressée directement au client. Le commissaire
          ne la signe pas — c'est une déclaration du client, pas du cabinet.
      - eyebrow: Signature puis envoi final
        title: Rapport du commissaire aux apports
        body: >
          Validé, signé par le commissaire, puis adressé au client. Cet envoi
          clôt la mission. Il ne peut intervenir qu'une fois la lettre
          d'affirmation revenue signée.
      - eyebrow: Sans circuit
        title: Documents de travail et pièces client
        body: >
          Les documents créés ou importés à l'étape des travaux, et le
          procès-verbal de désignation fourni par le client, sont versés au
          dossier sans passer par un circuit de validation.

  - kind: split
    eyebrow: Sorties anticipées
    title: Ce qui se passe quand la mission ne doit pas continuer
    body: |
      Un outil de mission qui ne prévoit que le chemin nominal est un outil qui
      sera contourné le jour où le dossier sort du cadre. Trois sorties sont
      prévues, toutes à l'étape d'acceptation, au moment où un document attend
      la signature du commissaire.
    points:
      - "Conflit d'intérêts déclaré par le commissaire — la mission retourne à l'attribution pour désignation d'un autre signataire"
      - "Conflit d'intérêts déclaré par le collaborateur — même retour, avec notification du commissaire"
      - "Refus de la mission par le commissaire — la lettre de refus est produite, signée, et la mission est close"
    panel:
      title: Points de sortie
      rows:
        - k: Attestation d'indépendance — signataire
          v: Conflit d'intérêts
        - k: Attestation d'indépendance — collaborateur
          v: Conflit d'intérêts
        - k: Fiche d'acceptation de mission
          v: Refus de mission
        - k: Fiche d'acceptation, lettre de mission, rapport
          v: Renvoi en rédaction

  - kind: faq
    tone: grey
    eyebrow: Questions
    title: Sur le circuit
    items:
      - q: La signature du commissaire est-elle une signature électronique qualifiée ?
        a: >
          La signature du client se fait par signature électronique via Docusign.
          Les modalités techniques de la signature apposée par le commissaire
          dans la plateforme sont à préciser avec notre équipe selon le niveau
          exigé par votre cabinet.
      - q: Peut-on savoir qui a validé quoi et quand ?
        a: >
          Oui. Chaque changement d'état porte son auteur et sa date, y compris
          les retours en rédaction. C'est ce qui permet de présenter
          l'historique d'un dossier sans le reconstituer.
      - q: Que devient un document renvoyé en rédaction ?
        a: >
          Il repasse à l'état « à valider » et le collaborateur le reprend. Le
          renvoi reste inscrit dans l'historique — il n'est pas effacé par la
          version suivante.
      - q: Le rapport peut-il partir avant la lettre d'affirmation ?
        a: >
          Non. Les deux documents de restitution peuvent être préparés en
          parallèle, mais l'envoi du rapport signé est conditionné au retour
          signé de la lettre d'affirmation, celle-ci étant un élément d'entrée
          du rapport.

  - kind: cta
    title: Voir le circuit sur un dossier
    lede: La démonstration suit un document de bout en bout, du premier jet à la signature.
    ctas:
      - label: Réserver une démonstration
        href: /demo/
---
