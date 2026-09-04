# Protocole d'enregistrement

*Ce qui fait la qualité d'un corpus vocal n'est pas le prix du micro, c'est la
pièce et la constance. Un téléphone dans une bonne pièce bat un enregistreur
professionnel dans une mauvaise.*

---

## 1. Le matériel

| Usage | Ce qu'il faut | Coût indicatif |
|---|---|---|
| Lecture ordinaire | téléphone Android récent + casque-micro filaire | 8 000 FCFA le casque |
| Lecture ordinaire | application capable d'enregistrer en WAV, 48 kHz, mono | gratuite |
| Voix de synthèse | enregistreur de terrain (Zoom H1, Tascam DR-05) + bonnette | 90 000 FCFA |
| Partout | carte mémoire 64 Go, batterie externe | 20 000 FCFA |

**Pas de Bluetooth.** Un casque sans fil compresse le son avant de l'envoyer au
téléphone : ce qui arrive dans le fichier a déjà perdu les aigus, et aucun
traitement ne les rend. Le fil, toujours.

**Pas de WhatsApp** pour transmettre les fichiers. WhatsApp recompresse et
ramène tout à un débit faible. Transmission par carte mémoire, câble USB, ou
téléversement direct du fichier d'origine.

---

## 2. La pièce

Par ordre d'importance :

1. **Aucune machine en marche.** Ventilateur, climatiseur, réfrigérateur,
   groupe électrogène. C'est la cause numéro un des rejets automatiques : un
   ventilateur pose un bruit continu qui écrase le rapport signal sur bruit.
2. **Pas de murs nus.** Une pièce en béton vide fait de l'écho, et l'écho ne se
   retire pas. Une chambre avec un matelas, des rideaux, des habits accrochés
   et un tapis vaut mieux que n'importe quel bureau.
3. **Loin de la rue.** Fenêtres fermées, porte fermée, pas de cour animée
   derrière la cloison.
4. **La nuit plutôt que le jour** quand c'est possible. Après 21 h, le fond
   sonore d'un quartier de N'Djamena descend de 10 à 15 dB.

Le contre-exemple utile : **30 % du corpus s'enregistre volontairement en
conditions ordinaires** (marché, cour, ventilateur allumé). Un modèle entraîné
uniquement au calme ne marche qu'au calme. Ces séances-là sont marquées
`conditions=ordinaire` dans la fiche locuteur, et elles ne servent jamais aux
voix de synthèse.

---

## 3. Le micro

- Micro du casque à environ **trois doigts du coin de la bouche**, sur le côté,
  **jamais dans l'axe du souffle**. De face, chaque `p` et chaque `b` produit
  une bouffée qui sature.
- Distance constante pendant toute la séance. Un lecteur qui se penche vers la
  page fait varier son niveau de 6 dB, et le corpus devient irrégulier.
- Ne pas toucher le fil ni le micro pendant qu'on parle.
- Téléphone posé sur un tissu, jamais directement sur une table qui transmet
  les chocs.

---

## 4. Les réglages du fichier

| Réglage | Lecture ordinaire | Voix de synthèse |
|---|---|---|
| Format | WAV ou FLAC, non compressé | WAV |
| Fréquence | 48 kHz (44,1 accepté) | 48 kHz obligatoire |
| Résolution | 16 bits | 24 bits si l'appareil le permet |
| Canaux | mono | mono |
| Niveau de crête | entre -12 et -3 dBFS | entre -12 et -6 dBFS |
| Réduction de bruit de l'appareil | **désactivée** | **désactivée** |
| Gain automatique | **désactivé** | **désactivé** |

Les deux dernières lignes comptent autant que toutes les autres. Le débruiteur
d'un téléphone est conçu pour la téléphonie : il coupe des morceaux de parole et
laisse des artefacts. Ce qu'il enlève ne se retrouve jamais, alors qu'un bruit
de fond mesuré reste exploitable.

---

## 5. Le déroulé

1. **Consentement signé et archivé.** Sans lui, la séance n'a pas lieu. Pour une
   personne non lettrée : lecture du formulaire à voix haute, **enregistrée**,
   puis empreinte ou marque, en présence d'un témoin nommé.
2. **Fiche locuteur remplie** (`terrain/locuteurs.csv`) : identifiant, genre,
   tranche d'âge, ville, région d'origine, langue première, langues parlées.
   Aucun nom, aucun numéro de téléphone dans le dépôt.
3. **Essai de niveau.** Trois phrases, on écoute au casque, on corrige la
   distance. Cinq minutes ici en sauvent quarante plus tard.
4. **Lecture.** Une phrase, un fichier, nommé comme l'indique le livret
   (`LOC001_s1_017.wav`). Le lecteur reprend la phrase **entière** dès qu'il
   bute : on ne recolle pas des morceaux.
5. **Phrase incomprise.** Le lecteur la saute et entoure son numéro. C'est un
   signal sur la banque de phrases, pas sur lui, et ça se remonte au rédacteur.
6. **Indemnité versée à la fin**, que la séance passe le contrôle ou non. Payer
   à la qualité pousse les gens à cacher leurs erreurs.

Durée : 45 minutes au micro, environ 240 phrases, environ 28 minutes d'audio
retenu.

---

## 6. Nommage et transfert

```
LOC001_s1_017.wav
 |     |   |
 |     |   +-- numero de la phrase dans le livret
 |     +------ numero de seance
 +------------ identifiant du locuteur
```

Un dossier par locuteur, un sous-dossier par séance. Le `plan_seance_*.csv`
produit par `outils/livret.py` accompagne toujours les fichiers : c'est lui qui
relie chaque fichier à son texte. **Des enregistrements sans leur plan de séance
sont inexploitables**, quelle que soit leur qualité sonore.

---

## 7. Les seuils automatiques

`outils/qualite_audio.py` applique ces seuils avant toute écoute humaine.

| Mesure | Lecture (profil `asr`) | Synthèse (profil `tts`) |
|---|---|---|
| Fréquence minimale | 16 000 Hz | 44 100 Hz |
| Rapport signal sur bruit | 20 dB | 35 dB |
| Crête maximale | -0,5 dBFS | -1,0 dBFS |
| Crête minimale | -35 dBFS | -24 dBFS |
| Échantillons saturés tolérés | 10 | 0 |
| Silence de bord maximal | 1,5 s | 0,8 s |
| Durée par rapport aux mots attendus | entre 0,55x et 2,2x | idem |

Le rapport de durée est le contrôle le plus utile : il attrape les phrases
tronquées, les phrases lues deux fois dans le même fichier, et les fichiers où
le lecteur commente sa lecture après l'avoir finie.

Un défaut de niveau ou un fichier stéréo n'entraîne **pas** de rejet : c'est
récupérable, et le rapport le marque `a_corriger`. Tout le reste est rejeté
avant qu'on paie une écoute.

Taux de rejet attendu : 10 à 15 % lors des premières séances d'un coordinateur,
moins de 5 % ensuite. Au-delà de 25 %, le problème est la pièce ou le réglage
du gain automatique, pas les lecteurs.
