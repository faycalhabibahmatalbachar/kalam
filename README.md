# Kalam — كلام

**Corpus ouvert et outils pour l'arabe tchadien parlé (ISO 639-3 : `shu`).**

L'arabe tchadien est la langue véhiculaire d'environ 12 millions de personnes.
Aucun système de reconnaissance vocale ne la reconnaît aujourd'hui : mesuré le
12 août 2026, une phrase en arabe tchadien dictée à un assistant grand public
revient transcrite en hindi, en portugais ou en allemand. Ce n'est pas un
réglage manquant, c'est l'absence pure et simple de la langue dans les modèles
disponibles.

Kalam existe pour combler ce trou, avec une méthode chiffrée et vérifiable.

---

## Ce qu'on veut obtenir

| Capacité | Cible mesurable | Palier visé |
|---|---|---|
| Comprendre (ASR) | WER < 25 % sur parole spontanée non vue | Palier 2 |
| Parler (TTS) | 3 voix naturelles, MOS > 3,8 | Palier 2 |
| Traduire (FR ↔ shu) | 30 000 phrases parallèles validées | Palier 2 |

Le détail des paliers, avec le calcul qui les justifie, est dans
[`docs/OBJECTIFS.md`](docs/OBJECTIFS.md).

## En deux chiffres

**200 heures validées** et **300 locuteurs différents** pour un système
utilisable au quotidien. Aujourd'hui : 45 h existent mais avec **une seule
voix**, ce qui vaut, pour la capacité à généraliser, à peu près autant que
2 h bien diversifiées.

Le nombre de locuteurs compte davantage que le nombre d'heures tant qu'on est
sous les 100 heures. C'est le principe qui gouverne tout ce dépôt.

## La méthode : le livret de lecture

On écrit une banque de phrases françaises couvrant la vie réelle au Tchad, des
locuteurs natifs les traduisent en arabe tchadien, puis **d'autres** locuteurs
les lisent au micro. La transcription est donc connue **avant** l'enregistrement.

C'est ce qui rend le projet finançable : transcrire de la parole spontanée coûte
environ **6 heures de travail humain par heure d'audio**, valider de la lecture
en coûte **moins d'une**. Facteur 6 à 8.

La contrepartie est réelle et on ne la cache pas : la lecture n'a ni les
hésitations, ni le débit, ni l'alternance de langues de la parole réelle. Un
modèle entraîné uniquement sur du livret s'effondre en conversation. D'où la
règle du dépôt :

> **70 % lecture, 30 % spontané — et l'évaluation se fait uniquement sur du
> spontané.** Sinon les scores mentent.

Marche à suivre complète : [`docs/STRATEGIE_RECOLTE.md`](docs/STRATEGIE_RECOLTE.md).

## Ce que contient le dépôt

```
banque/        la banque de phrases (source française, traductions, statuts)
outils/        les programmes : livrets, contrôle qualité audio, manifeste
docs/          objectifs chiffrés, stratégie, conventions, budget
consentement/  les formulaires FR et AR, sans lesquels rien n'est collecté
eval/          la spécification du jeu de test spontané
```

## Démarrer

```bash
pip install -r outils/requirements.txt
python outils/verifier_banque.py            # état de la banque de phrases
python outils/livret.py --locuteur LOC001 --phrases 240 --sortie livrets/
python outils/qualite_audio.py --dossier enregistrements/LOC001 --rapport qc.csv
python outils/manifeste.py --seances seances/ --sortie manifeste.csv
```

## Licences

- **Code** : MIT ([`LICENSE`](LICENSE))
- **Données collectées par Kalam** : CC BY 4.0 ([`LICENSE-DATA`](LICENSE-DATA))

La cession en CC BY est demandée explicitement dans le formulaire de
consentement. Un enregistrement dont le formulaire n'est pas signé n'entre pas
dans le corpus, et aucune source antérieure au projet n'est republiée ici :
voir [`docs/GOUVERNANCE.md`](docs/GOUVERNANCE.md).

## Statut

Palier 0 en cours. Le dépôt est ouvert aux contributions : traduire des phrases,
enregistrer un livret, valider des enregistrements. Voir
[`CONTRIBUTING.md`](CONTRIBUTING.md).
