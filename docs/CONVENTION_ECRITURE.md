# Convention d'écriture de l'arabe tchadien

*À arrêter avant la première traduction, pas après. Un corpus de dix mille
phrases écrites de neuf façons différentes n'est pas un corpus, c'est neuf
corpus de mille phrases.*

---

## 1. Deux écritures, deux rôles

Chaque phrase de la banque porte **deux** transcriptions, et elles ne servent
pas à la même chose.

| Colonne | Écriture | Sert à |
|---|---|---|
| `shu_arabe` | arabe | **la vérité d'entraînement**, ce que le modèle apprend à produire |
| `shu_latin` | latine | aide à la lecture, contrôle croisé, recherche dans le glossaire |

L'arabe est la référence. En cas de désaccord entre les deux colonnes, c'est
l'arabe qui fait foi. La colonne latine existe parce qu'une partie des
locuteurs et des relecteurs lit mieux le latin que l'arabe, et parce que le
glossaire de 5 180 entrées hérité du projet est en écriture latine.

---

## 2. Principe général

**On écrit ce qui se dit, pas ce qui s'écrirait en arabe littéraire.**

L'arabe tchadien n'est pas de l'arabe standard mal écrit. Corriger une forme
tchadienne vers sa forme littéraire détruit exactement la donnée qu'on cherche
à récolter.

| À écrire | À ne pas écrire | Raison |
|---|---|---|
| la forme entendue localement | la forme littéraire correspondante | le corpus documente la langue parlée |
| le mot français emprunté, tel qu'il est dit | sa traduction arabe | l'emprunt fait partie de la langue |
| la variante régionale du locuteur | une forme unifiée | les variantes sont de la donnée, pas du bruit |

Le seul unificateur autorisé est **orthographique** : deux locuteurs qui disent
la même chose l'écrivent pareil. Deux locuteurs qui disent des choses
différentes les écrivent différemment.

---

## 3. Règles fixes

**Vocalisation.** Les voyelles brèves (fatha, kasra, damma) sont notées sur les
mots dont la lecture serait ambiguë sans elles, et **omises ailleurs**. Un texte
entièrement vocalisé ralentit la traduction sans améliorer le modèle ; un texte
sans aucune voyelle rend certaines phrases illisibles à voix haute, ce qui est
rédhibitoire pour un livret de lecture.

**Ponctuation.** Point, virgule et point d'interrogation arabes (`.` `،` `؟`).
Pas de point-virgule, pas de points de suspension, pas de guillemets. Une phrase
de livret est une phrase, elle ne contient pas de dialogue rapporté.

**Chiffres.** Écrits **en toutes lettres** dans `shu_arabe`. Un modèle qui voit
le caractère `5` n'apprend pas à écrire ce qu'il entend, il apprend à deviner.
Le domaine `nombres` existe précisément pour lui enseigner les formes parlées.

**Emprunts français.** Transcrits en écriture arabe selon leur prononciation
tchadienne, jamais laissés en caractères latins au milieu d'une phrase arabe.
La colonne `shu_latin` peut, elle, garder la forme française d'origine entre
parenthèses.

**Noms propres.** Orthographe usuelle au Tchad. La forme retenue pour un nom de
ville, de province ou d'institution est fixée une fois et reprise partout : la
liste des formes arrêtées se tient dans `banque/noms_propres.csv`, qui fait
autorité sur toute autre source.

**Majuscules.** Sans objet en arabe. Dans `shu_latin`, majuscule initiale des
noms propres uniquement.

---

## 4. Arbitrage des mots hésitants

Dans cet ordre, et on s'arrête au premier qui tranche :

1. **Le glossaire existant** (5 180 entrées, écriture latine, hérité du corpus
   Toumaï). Il fixe la forme latine, dont on dérive la forme arabe.
2. **Le dictionnaire arabe tchadien / français Karthala** et le livre de
   Pommerol. Ces sources sont sous autorisation de consultation et
   d'entraînement, **pas de republication** : elles arbitrent, elles ne
   fournissent pas de phrases à la banque.
3. **Le vote des trois rédacteurs.** À deux voix contre une, la forme majoritaire
   passe et la minoritaire est notée dans `notes`.
4. **L'arbitrage du coordinateur linguistique**, consigné dans
   `docs/journal_arbitrages.md` avec la date et le motif.

Une décision d'arbitrage ne se rediscute pas phrase par phrase. Elle se
rediscute une fois, et la banque entière est mise à jour.

---

## 5. Transcription du spontané

Les segments de parole spontanée obéissent aux mêmes règles, plus trois
étiquettes qui n'existent pas dans le livret.

| Étiquette | Quand | Exemple d'usage |
|---|---|---|
| `[fr]` … `[/fr]` | passage prononcé en français | alternance de langues, très fréquente |
| `[inaudible]` | mot ou groupe incompréhensible | ne jamais deviner |
| `[bruit]` | événement sonore qui couvre la parole | klaxon, moto, cri |

Les hésitations (`euh`, reprises, faux départs) **sont transcrites**. C'est ce
qui distingue un corpus spontané d'un corpus de lecture, et c'est ce qui rend le
modèle capable d'encaisser la parole réelle.

Un segment contenant une deuxième voix non consentante est écarté, jamais
transcrit.

---

## 6. Contrôle

`outils/verifier_banque.py` applique automatiquement ce qui est vérifiable :
doublons, longueurs, phrases validées sans traducteur ni relecteur distincts,
équilibre des domaines. Le reste relève de la relecture humaine, et une phrase
relue par une seule personne ne passe jamais au statut `valide`.
