# Jeu de test

*Le premier livrable du projet, avant même le corpus d'entraînement. Sans lui,
aucun progrès n'est mesurable et tout ce qu'on dit sur la qualité d'un modèle
est une opinion.*

---

## 1. Les règles

**Cent pour cent spontané.** Aucune lecture de livret. Un taux d'erreur mesuré
sur de la lecture est flatteur et faux : le modèle y voit des phrases
articulées, sans hésitation ni chevauchement, souvent tirées de la même banque
que ses données d'entraînement.

**Locuteurs disjoints.** Aucun locuteur du jeu de test n'apparaît dans le
moindre jeu d'entraînement, à aucun palier, jamais. C'est vérifié
automatiquement avant chaque publication : un identifiant présent des deux côtés
bloque la sortie.

**Phrases disjointes.** Aucune phrase du jeu de test ne figure dans la banque.

**Figé.** Une fois publié, le jeu de test ne bouge plus. Le corriger après avoir
vu de mauvais résultats reviendrait à déplacer la cible.

**Public.** Publié en même temps que le premier corpus, sous la même licence.
Un banc d'essai que personne d'autre ne peut utiliser ne mesure rien.

---

## 2. Composition visée

| | Palier 0 | Palier 2 |
|---|---|---|
| Durée | 2 h | 5 h |
| Locuteurs | 20 | 60 |
| Villes | 4 | 8 |
| Genre | 50 / 50 | 50 / 50 |
| Part enregistrée en conditions ordinaires | 30 % | 30 % |
| Part contenant de l'alternance français / arabe | 20 % | 20 % |
| Segments | ~800 | ~2 000 |

Les deux dernières lignes sont volontaires. Un jeu de test sans bruit et sans
alternance de langues mesurerait une situation qui n'existe pas au Tchad.

---

## 3. Sous-ensembles

Le score global cache les échecs qui comptent. Chaque publication donne le taux
d'erreur découpé ainsi :

| Sous-ensemble | Pourquoi il est isolé |
|---|---|
| `propre` | conditions calmes, référence haute |
| `bruit` | marché, rue, ventilateur |
| `alternance` | segments contenant du français |
| `nombres` | chiffres, prix, heures, dates : là où les modèles peu dotés s'effondrent |
| `noms_propres` | noms de personnes, villes, provinces |
| `sud` | locuteurs pour qui l'arabe tchadien est une seconde langue |
| `femmes` / `hommes` | contrôle du biais de genre |

Un modèle à 22 % de taux d'erreur global mais 55 % sur `nombres` n'est pas
utilisable pour du mobile money. Le découpage sert à le voir.

---

## 4. Mesures

**Taux d'erreur sur les mots (WER)** et **sur les caractères (CER)**, calculés
après une normalisation publiée et versionnée : suppression de la ponctuation,
des signes de vocalisation, unification des formes de alif et de ya, chiffres
écrits en toutes lettres.

Le script de normalisation fait partie du jeu de test. Sans lui, deux équipes
mesurent deux choses différentes sur le même fichier et comparent des scores qui
n'ont aucun rapport.

Pour la synthèse vocale : MOS sur 20 auditeurs natifs minimum, échelle de 1 à 5,
échantillons présentés en ordre aléatoire, avec des enregistrements humains
mélangés en contrôle.

---

## 5. Le chiffre zéro

La première mesure à produire, avant toute collecte, est le taux d'erreur des
modèles existants sur ce jeu de test.

Ce chiffre sera très mauvais. C'est précisément ce qui en fait un argument :
mesuré le 12 août 2026, une phrase en arabe tchadien dictée à un assistant grand
public revient transcrite en hindi, en portugais ou en allemand. Le mettre en
nombre, sur un banc d'essai public et reproductible, vaut mieux que le raconter.

---

## 6. Ce que contient ce dossier

Pour l'instant, cette spécification seule. Le jeu de test lui-même sera publié
sur Hugging Face, avec sa fiche de données, et référencé ici. Il n'est pas
versionné dans ce dépôt : de l'audio n'a pas sa place dans git.
