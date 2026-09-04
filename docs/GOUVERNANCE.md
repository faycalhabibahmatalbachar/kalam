# Gouvernance des données

*Ce qui entre dans le corpus public, ce qui n'y entre jamais, et pourquoi la
séparation est structurelle plutôt que déclarative.*

---

## 1. Deux ensembles, séparés à la racine

**Ensemble ouvert — publié en CC BY 4.0**

Tout ce qui est collecté par Kalam avec le formulaire de consentement du dépôt :
enregistrements, transcriptions, banque de phrases, métadonnées de locuteurs
anonymisées, jeu de test.

Le formulaire demande explicitement la cession sous CC BY 4.0. Un locuteur qui
refuse cette clause peut quand même participer : sa contribution est marquée
`usage_restreint` et reste hors publication.

**Ensemble restreint — jamais publié**

Les sources antérieures au projet, couvertes par des autorisations qui portent
sur le traitement, la transcription et l'entraînement, **et non sur la
republication** :

| Source | Ce qui est autorisé | Ce qui ne l'est pas |
|---|---|---|
| Livre *J'apprends l'arabe tchadien* (Pommerol) | consultation, arbitrage orthographique, entraînement interne | republier des phrases |
| Dictionnaire arabe tchadien / français (Karthala) | idem | idem |
| Enregistrements bibliques FCBH | entraînement interne | republier l'audio |
| Contributions de créateurs (autorisation nommant les trois opérations) | traitement, transcription, entraînement | publication en licence ouverte |

Ces sources arbitrent l'orthographe et nourrissent les modèles internes de
Toumaï AI. **Aucune de leurs phrases n'entre dans `banque/phrases.csv`.** La
banque publique se construit uniquement à partir de phrases écrites pour le
projet par des rédacteurs payés, qui en cèdent les droits.

C'est la raison pour laquelle la banque part du français plutôt que de textes
arabes existants : partir de sources existantes aurait mélangé les deux
ensembles dès la première ligne, et rendu le corpus impubliable.

---

## 2. Ce qui ne quitte jamais le terrain

| Donnée | Où elle vit | Dans le dépôt |
|---|---|---|
| Nom et prénom du locuteur | registre du coordinateur, hors dépôt | non |
| Numéro de téléphone | registre du coordinateur | non |
| Formulaire de consentement signé | archive papier + numérisation chiffrée | non |
| Identifiant `LOC001` | partout | oui |
| Genre, tranche d'âge, ville, région, langue première | métadonnées | oui |

Le lien entre `LOC001` et une personne réelle existe en un seul endroit, tenu
par le coordinateur de la ville. Le dépôt ne contient que l'identifiant. Un
`.gitignore` interdit le versionnement de `terrain/consentements_signes/` et de
tout fichier `terrain/annuaire_*.csv`.

Ce n'est pas de la prudence excessive. Un corpus vocal contient la voix des
gens : la voix est une donnée biométrique, et l'associer publiquement à un nom
expose durablement des personnes qui ont juste voulu aider.

---

## 3. Le droit de retrait

Un locuteur peut demander le retrait de ses enregistrements à tout moment, sans
justification. Le formulaire l'énonce et donne l'adresse à laquelle écrire.

Ce que le retrait fait :
- les fichiers sont supprimés du corpus et des publications suivantes ;
- l'identifiant est marqué `retire` dans le manifeste ;
- la ligne est retirée de la prochaine version publiée sur Hugging Face.

Ce que le retrait ne peut pas défaire, et qui est dit au locuteur avant qu'il
signe : les copies déjà téléchargées par des tiers, et les modèles déjà
entraînés. Promettre l'inverse serait mentir.

---

## 4. Ce que devient la voix

Le formulaire le dit en une phrase, en français et en arabe : la voix sert à
**apprendre à une machine à comprendre et à parler l'arabe tchadien**, le corpus
est **public et gratuit**, et **n'importe qui pourra l'utiliser, y compris des
entreprises**, à condition de citer la source.

Cette dernière partie est la plus souvent escamotée dans les projets de collecte,
et c'est la seule qui compte vraiment pour la personne en face. On la dit
d'emblée.

---

## 5. Pourquoi publier

Un corpus fermé meurt avec l'organisation qui le détient. Un corpus ouvert
attire des relecteurs, des chercheurs, des contributeurs, et devient la
référence que d'autres améliorent.

L'avantage compétitif de Toumaï AI n'est pas le corpus : c'est le produit
construit dessus, la chaîne de collecte, le réseau de coordinateurs et
l'antériorité. Garder les données fermées protégerait mal cet avantage et
priverait la langue de tout ce qui pourrait lui arriver de bien.

---

## 6. Qui décide

| Décision | Qui tranche |
|---|---|
| Convention d'écriture, arbitrages lexicaux | coordinateur linguistique, journal public des arbitrages |
| Contenu de la banque de phrases | rédacteurs, à deux voix contre une |
| Admission d'une source dans l'ensemble ouvert | vérification du consentement, aucune exception |
| Publication d'une version du corpus | responsable du projet, après contrôle des quotas |

Tout écart aux quotas de diversité est **publié avec le corpus** plutôt que
corrigé après coup dans le discours. Un corpus à 78 % masculin peut être utile ;
un corpus à 78 % masculin présenté comme équilibré ne l'est pas.
