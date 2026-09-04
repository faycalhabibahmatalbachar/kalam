# Financement

*Le palier 1 est autofinançable. Le palier 2 ne l'est pas, et c'est normal :
aucun corpus vocal de 200 heures n'a jamais été construit sur fonds propres par
une startup. Ce document dit combien il faut, pour quoi, et à qui le demander.*

---

## 1. Ce que coûte une heure d'arabe tchadien

| Poste | Coût par heure d'audio validé |
|---|---|
| Lecture de livret | ~35 000 FCFA (53 EUR) |
| Parole spontanée transcrite | ~150 000 FCFA (229 EUR) |
| **Moyenne au ratio 70 / 30** | **~60 000 FCFA (92 EUR)** |

À titre de comparaison, faire transcrire une heure de parole spontanée par un
prestataire spécialisé dans une langue peu dotée coûte entre 100 et 300 EUR, et
les droits ne sont pas cédés.

Le chiffre de 92 EUR par heure est la mesure à retenir pour tout dossier : il
est vérifiable, il vient d'un calcul détaillé dans
[`STRATEGIE_RECOLTE.md`](STRATEGIE_RECOLTE.md), et il place le palier 2 à
**environ 18 400 EUR de collecte** plus le fonctionnement.

---

## 2. Les trois enveloppes

| | Palier 0 | Palier 1 | Palier 2 |
|---|---|---|---|
| Heures validées | 11 h | 65 h | 200 h |
| Collecte | 700 000 FCFA | 3 415 000 FCFA | 12 000 000 FCFA |
| Coordination | inclus | inclus | 3 000 000 FCFA |
| Marge | 200 000 FCFA | 500 000 FCFA | 1 000 000 FCFA |
| **Total FCFA** | **~900 000** | **~3 915 000** | **~16 000 000** |
| **Total EUR** | **~1 400** | **~6 000** | **~24 400** |
| Source réaliste | fonds propres | fonds propres + petite subvention | subvention |

Le palier 0 tient dans un budget personnel. Il ne sert qu'à une chose, et c'est
la plus importante : **produire la preuve chiffrée** que la chaîne fonctionne,
sans laquelle aucun bailleur ne regardera le dossier.

---

## 3. Ce qu'il faut avoir en main avant de demander

Aucun bailleur ne finance une intention. Ce qui se demande, dans l'ordre :

1. **Le jeu de test public** — 2 heures de parole spontanée, 20 locuteurs
   inédits, transcrites et publiées. C'est le seul livrable qui prouve qu'on
   sait produire de la donnée propre, et il sert ensuite à tout le monde.
2. **Un chiffre de référence publié** — le taux d'erreur d'un modèle existant
   sur ce jeu de test. Un chiffre catastrophique est un excellent argument :
   il mesure le trou qu'on propose de combler.
3. **Le corpus du palier 0 sur Hugging Face**, en CC BY 4.0, avec sa fiche de
   données et ses écarts de quotas publiés.
4. **La chaîne outillée et reproductible** — ce dépôt.
5. **L'existence légale.** RCCM, NIF, compte bancaire au nom de l'entité. C'est
   le point qui bloque le plus souvent, et il ne se règle pas en une semaine.

Les points 1 à 4 sont à portée du palier 0. Le point 5 se traite en parallèle,
dès maintenant.

---

## 4. Où demander

Pistes à vérifier au moment de candidater : les appels ouvrent et ferment, et
aucune date n'est reprise ici pour ne pas la donner fausse.

**Ciblé données linguistiques africaines**

- **Lacuna Fund** — finance explicitement la création de jeux de données pour
  les langues peu dotées, y compris vocales. C'est la cible la plus directe et
  la mieux alignée sur ce projet.
- **AI4D Africa / CRDI** — programmes de recherche appliquée en IA pour
  l'Afrique, avec un volet données.
- **FAIR Forward (GIZ)** — a financé des corpus vocaux ouverts pour plusieurs
  langues africaines, avec la même exigence de publication ouverte.
- **Masakhane** — collectif de recherche sur les langues africaines. Moins un
  bailleur qu'un réseau : co-signature scientifique, relecteurs, visibilité.

**Voix et données ouvertes**

- **Mozilla Common Voice** — l'ajout de l'arabe tchadien à la plateforme
  apporterait une infrastructure de collecte et de validation déjà construite.
  À considérer sérieusement : cela réduirait le coût d'outillage, au prix d'une
  licence CC0 et d'un moindre contrôle sur les quotas.

**Francophonie et culture**

- **Organisation internationale de la Francophonie** — le corpus est parallèle
  français / arabe tchadien, ce qui entre exactement dans ses programmes
  linguistiques.
- **UNESCO, Fonds international pour la diversité culturelle** — angle
  patrimoine linguistique et inclusion numérique.

**Industrie**

- Programmes de recherche des grands acteurs de l'IA sur les langues peu dotées.
  Rendement incertain, coût de candidature faible.

**Local**

- Opérateurs télécoms et institutions financières tchadiennes. L'argument est
  direct : un serveur vocal qui comprend l'arabe tchadien vaut mieux qu'un
  serveur vocal en français pour une clientèle qui parle arabe tchadien. Ce
  n'est pas du mécénat, c'est un achat.

---

## 5. Ce qu'on ne fait pas

**Pas de bénévolat comme modèle.** Un corpus construit sur le volontariat ne
dépasse jamais le cercle des amis du fondateur, et le cercle des amis du
fondateur n'est pas une langue. On paie, toujours, y compris quand la personne
propose de participer gratuitement.

**Pas de collecte sans consentement, même face à une échéance.** Un corpus dont
la chaîne de droits est bancale est inutilisable au moment précis où il devient
intéressant, c'est-à-dire quand quelqu'un veut le financer ou l'exploiter.

**Pas de gonflage des chiffres.** Le corpus actuel compte 45 heures et un seul
locuteur. Le présenter comme 45 heures d'arabe tchadien sans dire « une voix,
registre religieux » ferait perdre bien plus, au premier bailleur qui écoute
trois fichiers, que ce que ça ferait gagner.
