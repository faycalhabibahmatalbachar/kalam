# Stratégie de récolte

*Comment on passe d'une idée à 200 heures d'arabe tchadien validé.*

---

## 1. L'idée, et pourquoi elle tient

On écrit d'abord le texte, on enregistre ensuite. Le locuteur reçoit un livret,
il le lit au micro, et la transcription est connue **avant** que le micro
s'allume. Il n'y a plus rien à transcrire, seulement à vérifier.

C'est le renversement du coût :

| | Parole spontanée | Lecture de livret |
|---|---|---|
| 1 h d'audio brut | 1 h de terrain | 1 h de terrain |
| Découpage | automatique | automatique |
| Obtenir le texte | **6 h de transcription humaine** | 0 h, il existe déjà |
| Contrôle | 1 h de relecture | **0,8 h de double écoute** |
| **Total humain / h d'audio** | **≈ 7 h** | **≈ 0,8 h** |

**Facteur 8.** À budget égal, la lecture produit huit fois plus d'heures. C'est
ce qui rend un corpus de 200 heures atteignable pour une startup tchadienne
plutôt que pour un laboratoire.

### La limite, dite franchement

La lecture n'est pas de la parole. Il manque les hésitations, les reprises, le
débit rapide, les chevauchements, l'alternance français/arabe qui est la norme
au Tchad. Un modèle nourri uniquement de livrets reconnaît très bien des gens
qui lisent, et se trompe lourdement dès qu'on lui parle.

C'est pour ça que la lecture ne représente que **70 %** du corpus, que les
30 % restants sont du spontané payé au prix fort, et que **l'évaluation ne se
fait que sur du spontané**. La lecture donne le volume, la couverture lexicale
et les voix TTS. Le spontané donne le réalisme et la vérité des scores.

---

## 2. L'arithmétique du livret

Tous les chiffres qui suivent découlent de trois mesures simples.

**Une phrase = 7 secondes.** Phrases de 8 à 14 mots, débit ordinaire, silences
de bord compris. Donc :

```
500 phrases lues  =  1 heure d'audio net
```

**Une séance de 45 minutes rend 28 minutes utiles.** Le reste part en
installation, essais de niveau, reprises, pauses, tournage de page. Rendement
mesuré : 0,62. Donc :

```
1 séance de 45 min  =  240 phrases  =  28 min net
```

**Chaque phrase est lue par 3 locuteurs différents.** La redondance sert à
trois choses : elle donne au modèle la même phrase dans trois voix, elle permet
de repérer une phrase mal traduite (trois lecteurs qui butent au même endroit),
et elle fournit gratuitement des triplets pour l'évaluation de la synthèse.

### Ce que ça donne par palier

| | Palier 0 | Palier 1 | Palier 2 |
|---|---|---|---|
| Heures de lecture visées | 8 h | 50 h | 140 h |
| Lectures à produire | 4 000 | 25 000 | 70 000 |
| **Phrases uniques nécessaires** (÷ 3) | **1 400** | **8 400** | **23 400** |
| Banque à constituer (marge 20 %) | **3 000** | **10 000** | **25 000** |
| Séances de 45 min | 17 | 105 | 292 |
| **Locuteurs** (1 à 2 séances chacun) | **30** | **110** | **300** |

Lecture inverse, plus parlante : **un locuteur qui donne 45 minutes de son temps
apporte 28 minutes au corpus.** Il faut donc à peu près **deux personnes par
heure d'arabe tchadien**. Deux cents heures, c'est trois cents personnes qui
disent oui une fois.

---

## 3. La banque de phrases

C'est le livre de l'idée de départ, et c'est le seul actif du projet qui se
construit avant de sortir sur le terrain.

### Ce qu'elle contient

Une ligne = une phrase, avec sa source française, sa traduction en arabe
tchadien (écriture arabe et translittération latine), son domaine, son statut
et son quota de lectures. Format et règles : [`../banque/README.md`](../banque/README.md).

### Comment elle se remplit

1. **Le français d'abord.** Les phrases sources sont écrites en français,
   domaine par domaine, selon [`../banque/plan_domaines.yaml`](../banque/plan_domaines.yaml).
   C'est là qu'on décide ce que la langue devra savoir dire. Un amorçage de
   168 phrases est déjà dans [`../banque/phrases.csv`](../banque/phrases.csv).
2. **La traduction par des natifs payés.** Trois rédacteurs traduisent, en se
   relisant les uns les autres. Une phrase traduite par un seul rédacteur reste
   au statut `a_verifier` et **n'entre dans aucun livret**.
3. **Le contrôle automatique.** `outils/verifier_banque.py` refuse les doublons,
   les phrases trop courtes ou trop longues, les déséquilibres de domaine, et
   signale les mots absents du glossaire de 5 180 entrées (candidats à une
   coquille).

### Pourquoi partir du français et non de l'arabe

Parce que la couverture se décide en amont. Écrire d'abord en français permet
de garantir qu'on aura des phrases sur le mobile money, la pharmacie, les prix
du marché et les commandes adressées à un assistant, dans les proportions
choisies. Partir de textes arabes existants donnerait ce que ces textes
contiennent, c'est-à-dire, dans le cas du corpus actuel, de la narration
religieuse et rien d'autre.

Bénéfice secondaire non négligeable : la banque terminée **est** un corpus
parallèle français / arabe tchadien de 25 000 phrases. C'est de quoi affiner un
modèle de traduction, gratuitement, comme sous-produit.

### Ce qu'on ne fait pas

Les sources déjà en notre possession (le livre de Pommerol, le dictionnaire
Karthala, les enregistrements FCBH) sont couvertes par des autorisations qui
portent sur le traitement, la transcription et l'entraînement — **pas sur la
republication**. Elles servent de référence orthographique et de matière
d'entraînement interne. Aucune de leurs phrases n'entre dans la banque publique.
Voir [`GOUVERNANCE.md`](GOUVERNANCE.md).

---

## 4. Le terrain

### Les points de collecte

Huit villes, un coordinateur par ville. Le coordinateur n'est pas un
technicien : c'est quelqu'un du lieu qui sait à qui parler.

Ordre d'ouverture : N'Djamena et Abéché au palier 0, plus Sarh, Moundou et
Mongo au palier 1, le reste au palier 2.

### Où trouver 300 personnes

Par ordre de rendement observé dans ce type de projet :

1. **Établissements** — lycées, universités, centres de formation, écoles
   coraniques. Une autorisation du directeur, une salle, et trente personnes
   dans la journée. C'est de loin la source la plus rapide, et elle biaise vers
   les 18 à 25 ans : d'où l'intérêt de ne pas s'y limiter.
2. **Associations et coopératives** — groupements de femmes, associations de
   quartier, coopératives agricoles. C'est là qu'on trouve les 41 à 60 ans et
   les femmes, les deux catégories que les corpus vocaux ratent toujours.
3. **Radios communautaires** — un passage à l'antenne explique le projet et
   amène des volontaires, en particulier en province.
4. **Marchés et gares routières** — pour les enregistrements en conditions
   ordinaires, et pour toucher des gens qui ne viendraient jamais d'eux-mêmes.
5. **Cercle proche des contributeurs** — efficace mais à plafonner : au-delà de
   deux ou trois personnes par contributeur, on récolte un réseau social, pas
   une langue.

### Le déroulé d'une séance

Trente minutes de préparation, quarante-cinq minutes de micro.

1. **Expliquer** — ce qu'on fait, pourquoi, ce que deviendra la voix, le fait
   que le corpus sera public sous licence CC BY. Deux minutes, en arabe
   tchadien.
2. **Signer** — le formulaire de [`../consentement/`](../consentement/), en
   français ou en arabe, au choix. Pour une personne non lettrée : lecture à
   voix haute du formulaire, **enregistrée**, puis empreinte ou marque. Sans
   consentement archivé, la séance n'a pas lieu.
3. **Fiche locuteur** — identifiant, genre, tranche d'âge, ville, région
   d'origine, langue première, langues parlées. Aucun nom de famille, aucun
   numéro de téléphone dans le corpus : le lien identifiant / personne reste
   chez le coordinateur, hors du dépôt.
4. **Essai de niveau** — trois phrases, on écoute, on corrige la distance au
   micro. C'est l'étape qu'on saute et qu'on regrette.
5. **Lecture** — une phrase, un fichier. Le lecteur relit dès qu'il bute. Une
   phrase qu'il ne comprend pas, il la saute et le note : c'est un signal sur
   la banque, pas sur lui.
6. **Indemnité et reçu** — versée à la fin, séance validée ou non. On ne
   conditionne pas le paiement à la qualité, sinon les gens cachent leurs
   erreurs.

### Le matériel

| Usage | Matériel | Coût unitaire indicatif |
|---|---|---|
| Lecture ordinaire | téléphone Android + casque-micro filaire | 8 000 FCFA le casque |
| Lecture ordinaire | application d'enregistrement en WAV 48 kHz mono | gratuit |
| Voix TTS | enregistreur de terrain type Zoom H1 ou Tascam DR-05 | 90 000 FCFA |
| Partout | carte mémoire 64 Go, batterie externe | 20 000 FCFA |

Le téléphone suffit. Ce qui fait la qualité n'est pas le prix du micro, c'est la
**pièce** : jamais dehors, jamais dans une pièce nue en béton, jamais avec un
ventilateur ou une climatisation en marche. Une chambre avec un matelas, des
rideaux et des habits accrochés vaut mieux qu'un bureau vide. La nuit est plus
silencieuse que le jour. Détails et seuils mesurables :
[`PROTOCOLE_ENREGISTREMENT.md`](PROTOCOLE_ENREGISTREMENT.md).

---

## 5. La validation

Deux oreilles par enregistrement, jamais une.

```
2 acceptations          -> validé, entre dans le corpus
2 rejets                -> écarté, motif enregistré
1 partout               -> troisième oreille, qui tranche
```

Le validateur a le texte sous les yeux et l'audio dans l'oreille. Il répond à
une seule question : **est-ce que cette personne a bien dit ce texte-là ?** Il
ne juge ni l'accent, ni le grain de voix, ni la vitesse. Un accent de Moundou
n'est pas un défaut, c'est de la donnée.

Motifs de rejet acceptés : texte différent de ce qui est lu, mot avalé ou
coupé, deuxième voix audible, saturation, bruit qui couvre la parole, silence.

Avant l'oreille humaine, `outils/qualite_audio.py` écarte automatiquement ce
qui est mesurable : mauvais échantillonnage, saturation, rapport signal/bruit
insuffisant, durée incohérente avec le nombre de mots attendu. Cela retire
typiquement 10 à 15 % des fichiers et évite de payer une écoute pour rien.

Un validateur traite environ **1 h 15 d'audio par heure de travail** sur de la
lecture, parce qu'il peut rejeter avant la fin. Deux passes donnent le
0,8 h/h annoncé plus haut.

---

## 6. La part spontanée

Trente pour cent du corpus, et la totalité du jeu de test.

Sources, par ordre de propreté juridique :

1. **Enregistrements provoqués** — deux personnes qui se connaissent discutent
   vingt minutes sur un thème donné (le marché, un voyage, une panne). Les deux
   signent. C'est la source la plus propre et la plus riche : chevauchements,
   rires, alternance français/arabe, tout ce qui manque au livret.
2. **Contributions de créateurs** avec autorisation écrite nommant les trois
   opérations : traitement, transcription, entraînement. C'est le cadre déjà
   utilisé pour les 919 segments de Khalid.
3. **Radios communautaires** avec convention signée avec la station.

La transcription suit la chaîne existante : pré-transcription machine marquée
comme brouillon, puis relecture obligatoire par un locuteur natif. La
transcription entièrement automatique est **écartée** : elle fabriquerait un
corpus qui a l'air d'un corpus et qui apprend au modèle ses propres erreurs.

Convention d'écriture arrêtée avant toute transcription, sinon on obtient mille
segments écrits de neuf façons : [`CONVENTION_ECRITURE.md`](CONVENTION_ECRITURE.md).

---

## 7. Le budget

Hypothèses à valider sur le terrain, marquées comme telles. Palier 1 :
65 heures validées, 110 locuteurs, cinq villes, douze mois.

| Poste | Calcul | Montant FCFA |
|---|---|---|
| Rédaction et traduction de la banque | 10 000 phrases x 60 FCFA | 600 000 |
| Indemnités locuteurs | 140 séances x 3 000 FCFA | 420 000 |
| Coordinateurs terrain | 5 villes x 40 000 FCFA x 8 mois | 1 600 000 |
| Validation des lectures | 50 h x 0,8 h x 1 500 FCFA/h | 60 000 |
| Transcription du spontané | 15 h x 6 h x 1 500 FCFA/h | 135 000 |
| Matériel | 15 casques, 5 téléphones, 2 enregistreurs, cartes | 600 000 |
| Calcul et stockage | Kaggle et Colab gratuits, R2 déjà en place | 0 |
| Marge 15 % | | 500 000 |
| **Total** | | **≈ 3 915 000 FCFA** (≈ 6 000 EUR) |

Soit **60 000 FCFA par heure d'arabe tchadien validé**, environ 92 EUR. À titre
de comparaison, faire transcrire une heure de parole spontanée par un
prestataire spécialisé coûte entre 100 et 300 EUR pour une langue peu dotée,
sans les droits.

Le palier 2 (200 h, 300 locuteurs, 8 villes) se situe autour de **16 M FCFA**,
soit environ 24 000 EUR. Ce n'est plus de l'autofinancement, c'est un dossier
de subvention : [`FINANCEMENT.md`](FINANCEMENT.md).

L'indemnité de 3 000 FCFA par séance de 45 minutes est un choix, pas une
contrainte. Elle se situe au-dessus d'une demi-journée de petit commerce et
reste soutenable à l'échelle du projet. **On paie toujours.** Un corpus construit
sur du bénévolat ne dépasse jamais le cercle des amis, et le cercle des amis
n'est pas une langue.

---

## 8. Ce qui est ouvert et ce qui ne l'est pas

**Publié en CC BY 4.0** : les enregistrements collectés par Kalam avec le
formulaire de consentement du dépôt, la banque de phrases, les métadonnées de
locuteurs anonymisées, le jeu de test.

**Jamais publié** : les noms et coordonnées des locuteurs, les formulaires
signés (archivés hors dépôt), les sources antérieures au projet et les corpus
sous autorisation restreinte.

Publier le corpus n'est pas un geste de générosité, c'est la condition de sa
survie. Un corpus fermé meurt avec l'entreprise qui le détient. Un corpus
ouvert attire des contributeurs, des relecteurs, des chercheurs, et devient la
référence que d'autres améliorent.
