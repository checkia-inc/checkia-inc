---
url: /securite/secret-professionnel-et-ia/
title: Secret professionnel et fournisseurs d'IA
breadcrumb_label: Secret professionnel et IA
group: Ressources
type: article
updated: 2026-08-11
published: 2026-08-11
schema: [Article]
lede: >
  Trois questions distinctes se cachent derrière « est-ce que mes données sont en
  sécurité ? ». Les confondre conduit à se rassurer avec une réponse qui ne porte
  pas sur le bon risque.
answer: |
  Le secret professionnel du commissaire aux comptes ne se traite pas par une
  seule question mais par trois, indépendantes : **où résident les données**,
  **qui peut y accéder**, et **sont-elles utilisées pour entraîner un modèle**.
  Un engagement de non-entraînement ne dit rien sur la localisation ; un
  hébergement en Europe ne dit rien sur les accès. Un déploiement en instance
  dédiée sur l'infrastructure du cabinet ramène les deux premières questions à
  celles que le cabinet traite déjà pour son serveur de fichiers.
seo:
  title: "Secret professionnel et fournisseurs d'IA : les 3 questions"
  description: "Localisation, accès, entraînement : trois questions distinctes à poser à tout éditeur avant de lui confier des dossiers couverts par le secret professionnel."

sections:
  - kind: links
    tone: grey
    eyebrow: Pour aller plus loin
    title: Ressources liées
    items:
      - eyebrow: Produit
        title: Sécurité et confidentialité
        body: Le modèle de déploiement de CheckIA, et les points encore à préciser.
        href: /securite/
      - eyebrow: Méthode
        title: IA et jugement professionnel
        body: Ce qu'un outil peut préparer, ce qu'il ne doit pas décider.
        href: /ia-et-jugement-professionnel/
      - eyebrow: Comparaison
        title: Assistant généraliste ou logiciel de mission ?
        body: Pourquoi la question du périmètre se pose différemment selon l'outil.
        href: /comparatif/chatgpt-vs-logiciel-de-mission/
---

## Trois questions, pas une

« Est-ce que mes données sont en sécurité ? » est trop large pour recevoir une
réponse utile. Un éditeur peut répondre oui de bonne foi en pensant à une
question, alors que le cabinet en avait une autre en tête.

Il faut les séparer.

### 1. Où résident les données ?

Sur quelle infrastructure les dossiers sont-ils stockés et traités ? Dans quel
pays ? Sous quelle juridiction ? S'agit-il d'une base mutualisée entre plusieurs
cabinets, ou d'un environnement dédié ?

C'est la question qui détermine si vous pouvez, en cas de contrôle ou de
contentieux, **dire où se trouvent** les informations couvertes par le secret.

### 2. Qui peut y accéder ?

Quels salariés de l'éditeur peuvent techniquement lire un dossier ? Dans quelles
conditions — support, incident, maintenance ? Les accès sont-ils journalisés ?
Quels sous-traitants ultérieurs interviennent, et pour quoi faire ?

C'est la question qui détermine l'étendue réelle du cercle des personnes exposées
au secret.

### 3. Les données servent-elles à entraîner un modèle ?

Les contenus soumis sont-ils utilisés pour améliorer un modèle, chez l'éditeur ou
chez son fournisseur de modèle ? L'engagement est-il contractuel ou tiré d'une
page d'aide ? Vaut-il pour tous les usages ou seulement pour certaines offres ?

## Pourquoi les confondre est le piège habituel

Ces trois questions sont **indépendantes**, et une réponse rassurante à l'une ne
dit rien des deux autres.

| Réponse fréquente | Ce qu'elle traite | Ce qu'elle laisse ouvert |
|---|---|---|
| « Nous n'entraînons pas nos modèles sur vos données » | L'entraînement | Où résident les données, qui y accède |
| « Nos serveurs sont en Europe » | La localisation | Les accès du support, les sous-traitants, l'entraînement |
| « Les données sont chiffrées » | Le transport et le repos | Qui détient les clés, qui accède en clair côté applicatif |
| « Nous sommes conformes au RGPD » | Le cadre général | Aucune des trois de façon spécifique |
| « Vos données sont isolées » | Le cloisonnement logique | La nature de l'isolement — logique ou physique |

> [!important] Le RGPD et le secret professionnel ne sont pas la même contrainte.
> Le RGPD protège les personnes physiques. Le secret professionnel du commissaire
> aux comptes couvre les informations de la mission, y compris quand elles ne
> concernent aucune personne physique identifiée. Une conformité RGPD
> irréprochable ne règle donc pas, à elle seule, la question du secret.

## Les questions à poser à un éditeur

À reprendre telles quelles dans un questionnaire de sécurité.

**Localisation et exécution**

1. Où s'exécute l'application, et où résident les données de mission ?
2. S'agit-il d'une base mutualisée ou d'un environnement dédié par cabinet ?
3. Le cabinet peut-il choisir ou vérifier la localisation ?

**Accès**

4. Quels rôles, chez vous, peuvent techniquement accéder à un dossier client ?
5. Dans quelles circonstances, et avec quelle journalisation ?
6. Quels sous-traitants ultérieurs interviennent, et pour quelles opérations ?

**Modèles d'IA**

7. Quel fournisseur de modèle est utilisé, et sous quel contrat ?
8. Les contenus transmis sont-ils conservés par ce fournisseur, et combien de temps ?
9. L'engagement de non-entraînement est-il contractuel, et opposable ?
10. Quelles données sont effectivement transmises au modèle — dossier complet, extraits, métadonnées ?

**Fin de relation**

11. Que deviennent les données en fin de contrat, et sous quel délai ?
12. Sous quel format sont-elles restituées ?

Une réponse évasive à la question 10 est le signal le plus utile de la liste.

## Ce que change un déploiement dédié

Lorsque le logiciel s'exécute **sur l'infrastructure du cabinet**, les deux
premières questions changent de nature : elles cessent d'être des questions sur
un tiers pour redevenir des questions d'infrastructure, que le cabinet traite
déjà pour sa messagerie et son serveur de fichiers.

La troisième question — l'usage éventuel d'un modèle d'IA et le traitement des
contenus qui lui sont soumis — **subsiste** et doit être traitée pour elle-même.
Un déploiement dédié ne la fait pas disparaître ; il la circonscrit.

C'est le modèle retenu par CheckIA. Les points qui restent à préciser sont listés
explicitement sur notre [page sécurité](/securite/), y compris le fournisseur de
modèle et la politique d'entraînement, que nous documentons par écrit dans le
cadre contractuel plutôt que par une formule générale sur une page web.

## Une note sur les engagements « entreprise »

Les offres professionnelles des grands fournisseurs d'assistants comportent
souvent un engagement de non-utilisation des contenus pour l'entraînement. C'est
un progrès réel, et il traite la troisième question.

Il ne traite ni la première, ni la deuxième. Et il ne crée pas la **piste
probante** dont un dossier de mission a besoin : un historique de conversation
n'établit pas qui a validé quoi, ni quand.

## Questions fréquentes

### Le secret professionnel interdit-il l'usage de l'IA ?

Non. Il impose de savoir où vont les informations de la mission et qui peut y
accéder. C'est une contrainte sur l'architecture de l'outil, pas une interdiction
de principe de la technologie.

### Anonymiser suffit-il ?

Cela réduit le risque sans l'éliminer. Sur une opération d'apport, le montant, le
secteur et la date suffisent souvent à réidentifier les parties. L'anonymisation
est une précaution utile, pas une réponse au problème.

### Un hébergement en France règle-t-il la question ?

Il traite la localisation. Il ne dit rien des accès du support ni du traitement
par un modèle tiers, qui peut lui-même être hébergé ailleurs.

### Faut-il une clause spécifique dans le contrat ?

Le point utile est que les engagements figurent dans le contrat et non dans une
documentation modifiable unilatéralement — en particulier sur ce qui est transmis
à un fournisseur de modèle et sur la durée de conservation chez ce dernier.
