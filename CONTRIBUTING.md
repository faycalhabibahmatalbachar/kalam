# Contribuer

Quatre façons d'aider, de la plus légère à la plus engageante.

---

## 1. Traduire des phrases (30 minutes)

La banque contient des phrases françaises en attente de traduction en arabe
tchadien. C'est le goulot d'étranglement actuel : sans phrases validées, aucun
livret ne peut être fabriqué, et sans livret il n'y a pas d'enregistrement.

Ouvrez [`banque/phrases.csv`](banque/phrases.csv), remplissez `shu_arabe` et
`shu_latin`, mettez votre nom dans `traducteur`, passez le statut à
`a_verifier`, et proposez la modification.

Lisez d'abord [`docs/CONVENTION_ECRITURE.md`](docs/CONVENTION_ECRITURE.md).
La règle qui compte : **on écrit ce qui se dit**, pas la forme littéraire.

## 2. Relire une traduction (20 minutes)

Une phrase ne passe au statut `valide` qu'après relecture par une personne
**autre** que le traducteur. Prenez des lignes en `a_verifier`, corrigez ou
confirmez, mettez votre nom dans `relecteur`, passez au statut `valide`.

Le contrôle automatique refuse toute phrase où traducteur et relecteur sont la
même personne.

## 3. Enregistrer un livret (1 heure)

C'est la contribution la plus utile, et la plus rare.

```bash
python outils/livret.py --locuteur VOTRE_ID --phrases 240
```

Lisez [`docs/PROTOCOLE_ENREGISTREMENT.md`](docs/PROTOCOLE_ENREGISTREMENT.md)
avant de brancher quoi que ce soit. Les deux erreurs qui gâchent une séance
entière : un ventilateur allumé, et le réducteur de bruit du téléphone laissé
actif.

Signez le formulaire de [`consentement/`](consentement/). Sans lui, les fichiers
ne peuvent pas entrer dans le corpus, même excellents.

## 4. Valider des enregistrements (1 heure)

Chaque fichier est écouté par deux personnes différentes. Le validateur a le
texte sous les yeux et répond à une seule question : **est-ce que cette personne
a bien dit ce texte-là ?**

Il ne juge ni l'accent, ni la voix, ni la vitesse. Un accent de Moundou n'est
pas un défaut, c'est de la donnée.

---

## Ce qui ne se propose pas

- **Des phrases tirées d'un livre, d'un dictionnaire ou d'un site.** Le corpus
  se veut publiable sous licence libre : une seule phrase copiée d'une source
  protégée le rend impubliable. Voir [`docs/GOUVERNANCE.md`](docs/GOUVERNANCE.md).
- **De l'audio dans une pull request.** Git n'est pas fait pour ça. Le corpus se
  publie sur Hugging Face ; les fichiers passent par le coordinateur.
- **La voix de quelqu'un d'autre sans son consentement écrit**, y compris un
  proche, y compris s'il est d'accord à l'oral.
- **Une transcription entièrement automatique.** Elle fabriquerait un corpus qui
  a l'air d'un corpus et qui apprend au modèle ses propres erreurs. La
  pré-transcription machine est autorisée, mais toujours relue par un natif et
  marquée comme brouillon jusque-là.

---

## Avant de proposer une modification

```bash
python outils/verifier_banque.py
```

Sortie en erreur, modification refusée. C'est le même contrôle qui tourne en
intégration continue.

---

## Langue de travail

Français et arabe tchadien. Les messages de commit, les issues et les documents
sont en français. Les phrases de la banque sont en arabe.
