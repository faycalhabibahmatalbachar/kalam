# La banque de phrases

C'est le livre que lisent les locuteurs. Une ligne, une phrase, sa traduction,
son statut.

## Colonnes de `phrases.csv`

| Colonne | Contenu | Obligatoire quand |
|---|---|---|
| `id` | trois lettres, tiret, trois chiffres (`mar-004`) | toujours |
| `domaine` | code présent dans `plan_domaines.yaml` | toujours |
| `fr` | la phrase source, en français | toujours |
| `shu_arabe` | traduction en écriture arabe, **la vérité d'entraînement** | statut `valide` |
| `shu_latin` | translittération latine, aide à la lecture | statut `valide` |
| `statut` | `a_traduire`, `a_verifier`, `valide`, `rejete` | toujours |
| `traducteur` | qui a traduit | statut `valide` |
| `relecteur` | qui a relu, **différent du traducteur** | statut `valide` |
| `lectures_cible` | nombre de locuteurs qui doivent la lire (3 par défaut) | toujours |
| `notes` | doute lexical, variante écartée, remarque de terrain | jamais |

## Le cycle d'une phrase

```
a_traduire  ->  a_verifier  ->  valide  ->  entre dans les livrets
                     |
                     +------->  rejete   (intraduisible, ambiguë, doublon de sens)
```

Une phrase au statut `valide` a été traduite par une personne **et** relue par
une autre. `outils/verifier_banque.py` refuse tout `valide` où le traducteur et
le relecteur sont la même personne, ou dont l'un des deux champs est vide.
Ce n'est pas de la bureaucratie : c'est le seul contrôle qui empêche une
traduction fausse d'être lue à voix haute par trente personnes.

## Ce qui n'entre jamais dans la banque

Aucune phrase extraite du livre de Pommerol, du dictionnaire Karthala, des
textes bibliques ou d'une source sous autorisation restreinte. Ces sources
arbitrent l'orthographe ; elles ne fournissent pas de contenu.
Voir [`../docs/GOUVERNANCE.md`](../docs/GOUVERNANCE.md).

## Les deux plans

- [`plan_domaines.yaml`](plan_domaines.yaml) — de quoi la banque doit parler, et
  dans quelles proportions. Sert aussi à composer les livrets.
- [`plan_diversite.yaml`](plan_diversite.yaml) — qui doit lire, et dans quelles
  proportions. Sert au bilan du corpus.

## État actuel

168 phrases françaises d'amorçage, toutes au statut `a_traduire`, réparties sur
les 14 domaines. La prochaine étape est la traduction par trois rédacteurs
natifs payés, puis l'extension à 3 000 phrases pour le palier 0.

```bash
python outils/verifier_banque.py
```
