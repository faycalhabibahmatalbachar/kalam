# Objectifs chiffrés

*Version du 4 septembre 2026. Chaque chiffre de ce document est soit mesuré sur
le corpus existant, soit dérivé d'un calcul explicité ici. Rien n'est repris
d'une intuition.*

---

## 1. Le point de départ, mesuré

| Matière | Volume | Locuteurs | Registre | Utilisable pour |
|---|---|---|---|---|
| `asr_shu` (narration biblique alignée) | **45,4 h** · 18 468 segments · 47 livres | **1** | lecture religieuse | pré-entraînement, amorçage |
| Segments conversationnels Khalid | 1 h 58 · 919 segments | 1 | spontané | rien tant que non transcrit |
| Conversationnel validé | 5 segments | 1 | spontané | rien |
| Glossaire `shu` vers fr/en | 5 180 entrées | — | lexical | contrôle orthographique |

**Ce que ça veut dire.** 45 heures paraissent beaucoup. Elles ne le sont pas :
un modèle entraîné sur une seule voix apprend cette voix. Sur la capacité à
généraliser à un locuteur inconnu, ces 45 heures valent à peu près ce que
vaudraient 2 à 3 heures réparties sur trente personnes. Le corpus actuel est
riche en heures et pauvre en langue.

**Corollaire opérationnel :** tout effort qui ajoute des heures sans ajouter de
locuteurs est un effort gaspillé.

---

## 2. Combien d'heures ? Combien de locuteurs ?

### La règle qui gouverne le dimensionnement

En dessous de 100 heures, la performance d'un modèle affiné sur une langue peu
dotée est bornée par le **nombre de locuteurs**, pas par le volume. Les seuils
observés dans les corpus comparables (Common Voice, FLEURS, NaijaVoices,
travaux MMS) :

- **moins de 20 locuteurs** : le modèle mémorise les voix, s'effondre sur une
  voix inconnue
- **50 à 100 locuteurs** : la généralisation commence
- **300 locuteurs et plus** : robuste aux voix, accents et débits nouveaux

Le rendement par personne sature vite : au-delà d'environ **1 heure par
locuteur**, les minutes supplémentaires n'apportent presque rien. La zone utile
est **20 à 40 minutes par locuteur**.

D'où la relation de dimensionnement retenue :

```
heures utiles  =  nombre de locuteurs  x  0,4 h
```

C'est cette égalité qui fixe les deux colonnes des paliers ci-dessous. Elles ne
sont pas indépendantes : viser 200 h sans viser 300 locuteurs produirait un
corpus gros et inutile.

### Les paliers

| | Palier 0 · Amorçage | Palier 1 · Utilisable | Palier 2 · Solide | Palier 3 · Référence |
|---|---|---|---|---|
| **Échéance** | +4 mois | +12 mois | +24 mois | +36 mois |
| **Locuteurs** | **30** | **110** | **300** | **800** |
| Heures lecture (livret) | 8 h | 50 h | 140 h | 400 h |
| Heures spontané transcrit | 3 h | 15 h | 60 h | 180 h |
| **Total validé** | **11 h** | **65 h** | **200 h** | **580 h** |
| Phrases uniques en banque | 3 000 | 10 000 | 25 000 | 50 000 |
| WER attendu (spontané) | 45 à 55 % | 28 à 35 % | 18 à 25 % | 12 à 16 % |
| Ce que ça permet | démonstration, jeu de test public | dictée courte avec confirmation à l'écran | assistant vocal au quotidien | usage général |
| Voix TTS | 0 | 1 (5 h studio) | 3 (5 h chacune) | 3 + expressivité |
| Budget estimé | ~0,9 M FCFA | ~3,9 M FCFA | ~16 M FCFA | subvention |

**Le palier qui compte est le 2.** C'est celui où l'arabe tchadien devient une
langue qu'une machine comprend. Le palier 1 est l'étape qui prouve que la chaîne
fonctionne et qui rend le 2 finançable.

### Répartition lecture / spontané

**70 % lecture, 30 % spontané.** Ce n'est pas un compromis paresseux, c'est la
conséquence de deux coûts très différents et de deux apports différents.

| | Lecture (livret) | Spontané |
|---|---|---|
| Coût humain par heure d'audio | **0,8 h** (validation) | **6 h** (transcription) |
| Alignement texte/audio | parfait, connu d'avance | à produire |
| Couverture lexicale | contrôlée, on choisit | subie |
| Prosodie, hésitations, alternance FR | absentes | présentes |
| Utilisable pour la synthèse vocale | oui | non |
| Ressemble à ce que dira un utilisateur | non | oui |

Un modèle entraîné à 100 % sur de la lecture perd typiquement 10 à 20 points de
WER quand on lui présente de la conversation réelle. Un modèle entraîné à 100 %
sur du spontané coûterait sept fois plus cher pour le même volume et ne donnerait
aucune voix TTS. Le mélange 70/30 prend le volume d'un côté et le réalisme de
l'autre.

**Règle non négociable : le jeu de test est à 100 % spontané, avec des
locuteurs qui n'apparaissent dans aucun jeu d'entraînement.** Un WER mesuré sur
de la lecture serait flatteur et faux. Spécification : [`../eval/README.md`](../eval/README.md).

---

## 3. Les quotas de diversité

Un corpus de 300 hommes de N'Djamena entre 20 et 30 ans n'est pas un corpus de
l'arabe tchadien. Les quotas suivants s'appliquent à chaque palier et sont
vérifiés par `outils/manifeste.py`, qui refuse de produire un jeu déséquilibré
sans alerte explicite.

**Genre** — 50 % femmes / 50 % hommes, tolérance 10 points.
C'est le biais le mieux documenté des corpus vocaux ouverts : Common Voice
plafonne autour de 80 % de voix masculines, et les modèles qui en sortent
reconnaissent moins bien les femmes. On refuse d'hériter de ce défaut.

**Âge** — 18 à 25 ans : 30 % · 26 à 40 ans : 35 % · 41 à 60 ans : 25 % · 60 ans et plus : 10 %.

**Origine et variante régionale** — au moins huit points de collecte :

| Point | Région | Part visée |
|---|---|---|
| N'Djamena | Chari-Baguirmi | 25 % |
| Abéché | Ouaddaï | 15 % |
| Am Timan | Salamat | 8 % |
| Ati | Batha | 8 % |
| Mongo | Guéra | 8 % |
| Moussoro | Kanem | 8 % |
| Sarh | Moyen-Chari | 14 % |
| Moundou | Logone Occidental | 14 % |

Sarh et Moundou sont dans le sud, où l'arabe tchadien est massivement une
**seconde langue véhiculaire**. C'est délibéré : c'est aussi cet arabe-là que
les utilisateurs parleront.

**Langue première** — arabe tchadien L1 : 65 % · L2 véhiculaire : 35 %.
Chaque locuteur déclare sa L1 réelle (sara, kanembou, ngambaye, massa, gorane,
zaghawa, hadjaraï, peul, français). Le champ est enregistré, jamais deviné.

**Conditions d'enregistrement** — 70 % en intérieur calme, 30 % en conditions
ordinaires (marché, rue, ventilateur). Un corpus enregistré uniquement au
calme donne un modèle qui ne marche qu'au calme.

---

## 4. Ce qu'il faut pour la synthèse vocale

La synthèse n'obéit pas aux mêmes règles que la reconnaissance : peu de
locuteurs, beaucoup de propreté.

| Élément | Exigence |
|---|---|
| Locuteurs | 1 par voix, jamais mélangés |
| Durée par voix | **5 h nettes** (2 h donnent déjà un résultat, 8 h ne rendent presque rien de plus) |
| Échantillonnage | 48 kHz, 24 bits si possible, mono |
| Bruit de fond | SNR au moins 35 dB, bien plus strict que pour l'ASR |
| Alignement | phrase par phrase, exact |
| Constance | même pièce, même micro, même distance, sur toutes les séances |

Les 5 heures d'une voix TTS représentent environ **2 500 phrases**, soit
**11 séances de 45 minutes**. C'est le seul poste du projet qui demande de
choisir une personne et de la mobiliser longtemps. Il vient au palier 1, une
fois la chaîne de lecture rodée, et pas avant.

Ordre imposé : **comprendre d'abord, parler ensuite.** Un assistant qui comprend
mal mais parle bien est plus exaspérant qu'un assistant qui comprend bien et
parle avec un accent.

---

## 5. Les jalons de vérification

Un palier n'est atteint que si ces trois conditions sont vraies en même temps.

| | Volume | Diversité | Preuve |
|---|---|---|---|
| Palier 0 | 11 h validées | 30 locuteurs, quotas genre respectés | jeu de test spontané publié, 2 h, 20 voix inédites |
| Palier 1 | 65 h validées | 110 locuteurs, 5 régions | WER mesuré et publié sur le jeu de test |
| Palier 2 | 200 h validées | 300 locuteurs, 8 régions | WER sous 25 %, 3 voix TTS, corpus publié sur Hugging Face |

Aucun palier ne se déclare atteint sur le volume seul.
