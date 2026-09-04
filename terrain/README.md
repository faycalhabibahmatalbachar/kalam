# Terrain

Les registres tenus par les coordinateurs. Trois fichiers, un role chacun.

## `locuteurs.csv`

Un locuteur, une ligne. C'est le fichier qui autorise ou bloque l'entree d'un
enregistrement dans le corpus : sans `consentement_reference`, `manifeste.py`
ecarte tout ce que la personne a enregistre.

| Colonne | Valeurs |
|---|---|
| `id_locuteur` | `LOC001`, jamais un nom |
| `genre` | `femme`, `homme` |
| `tranche_age` | `18-25`, `26-40`, `41-60`, `60+` |
| `ville_collecte` | `ndjamena`, `abeche`, `sarh`, `moundou`, `am_timan`, `ati`, `mongo`, `moussoro` |
| `region_origine` | province d'origine, en clair |
| `langue_premiere` | `shu` si l'arabe tchadien est la langue premiere, sinon la langue reelle |
| `langues_parlees` | separees par des points-virgules |
| `niveau_etudes` | facultatif |
| `consentement_reference` | reference du formulaire signe, archive hors depot |
| `date_inscription` | AAAA-MM-JJ |

## `lectures.csv`

Le journal de ce qui a deja ete lu. `livret.py` s'en sert pour ne jamais faire
relire a quelqu'un une phrase qu'il a deja lue, et pour savoir quelles phrases
n'ont pas atteint leurs trois lectures.

## `validations.csv`

Un vote par ligne : `fichier`, `validateur`, `verdict` (`accepte` ou `rejete`),
`motif`, `date`. Deux acceptations valident, deux rejets ecartent, une voix
partout appelle une troisieme oreille.

## Ce qui ne va PAS ici

Aucun nom, aucun numero de telephone, aucun formulaire signe. Ces elements
restent chez le coordinateur. Le `.gitignore` bloque
`terrain/consentements_signes/` et `terrain/annuaire_*.csv`.
