#!/usr/bin/env python3
"""Verifie la banque de phrases : schema, doublons, longueurs, equilibre des domaines.

Sort en code 1 si une erreur bloquante est trouvee, 0 sinon. Les avertissements
n'arretent pas la chaine mais sont comptes.

    python outils/verifier_banque.py
    python outils/verifier_banque.py --banque banque/phrases.csv --plan banque/plan_domaines.yaml
"""
from __future__ import annotations

import argparse
import collections
import csv
import re
import sys
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

COLONNES = [
    "id",
    "domaine",
    "fr",
    "shu_arabe",
    "shu_latin",
    "statut",
    "traducteur",
    "relecteur",
    "lectures_cible",
    "notes",
]

STATUTS = {"a_traduire", "a_verifier", "valide", "rejete"}

# Un id ressemble a  sal-001 : trois lettres, tiret, trois chiffres au moins.
MOTIF_ID = re.compile(r"^[a-z]{3}-\d{3,}$")


def charger_plan(chemin: Path) -> dict:
    try:
        import yaml
    except ImportError:
        sys.exit(
            "PyYAML manquant. Installer avec :\n"
            "    pip install -r outils/requirements.txt"
        )
    with chemin.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def normaliser(texte: str) -> str:
    """Cle de comparaison pour detecter les doublons a la casse et aux accents pres."""
    texte = unicodedata.normalize("NFKD", texte.lower())
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    return " ".join(texte.split())


def compter_mots(texte: str) -> int:
    return len([m for m in re.split(r"[\s،؛]+", texte.strip()) if m])


def verifier(banque: Path, plan_chemin: Path) -> int:
    plan = charger_plan(plan_chemin)
    parts = {d["code"]: d["part"] for d in plan["domaines"]}
    titres = {d["code"]: d["titre"] for d in plan["domaines"]}
    plafonds = {
        d["code"]: (
            25 if d["code"] == "recits" else plan["longueur"]["mots_max"]
        )
        for d in plan["domaines"]
    }
    mots_min = plan["longueur"]["mots_min"]
    tolerance = plan["tolerance_points"]

    with banque.open(encoding="utf-8-sig", newline="") as f:
        lignes = list(csv.DictReader(f))

    erreurs: list[str] = []
    avertissements: list[str] = []

    if not lignes:
        print("Banque vide.")
        return 1

    manquantes = [c for c in COLONNES if c not in lignes[0]]
    if manquantes:
        erreurs.append(f"colonnes absentes du fichier : {', '.join(manquantes)}")
        for e in erreurs:
            print(f"ERREUR  {e}")
        return 1

    vus_id: dict[str, int] = {}
    vus_fr: dict[str, str] = {}
    vus_shu: dict[str, str] = {}
    par_domaine = collections.Counter()
    par_statut = collections.Counter()
    longueurs: list[int] = []

    for n, ligne in enumerate(lignes, start=2):
        ident = (ligne["id"] or "").strip()
        dom = (ligne["domaine"] or "").strip()
        fr = (ligne["fr"] or "").strip()
        arabe = (ligne["shu_arabe"] or "").strip()
        latin = (ligne["shu_latin"] or "").strip()
        statut = (ligne["statut"] or "").strip()

        if not ident:
            erreurs.append(f"ligne {n} : id vide")
        elif not MOTIF_ID.match(ident):
            avertissements.append(f"ligne {n} : id '{ident}' hors convention xxx-000")
        elif ident in vus_id:
            erreurs.append(f"ligne {n} : id '{ident}' deja utilise ligne {vus_id[ident]}")
        else:
            vus_id[ident] = n

        if dom not in parts:
            erreurs.append(f"ligne {n} : domaine '{dom}' absent du plan")
        else:
            par_domaine[dom] += 1

        if statut not in STATUTS:
            erreurs.append(f"ligne {n} : statut '{statut}' inconnu")
        else:
            par_statut[statut] += 1

        if not fr:
            erreurs.append(f"ligne {n} : phrase francaise vide")
        else:
            cle = normaliser(fr)
            if cle in vus_fr:
                erreurs.append(f"ligne {n} : francais identique a {vus_fr[cle]}")
            else:
                vus_fr[cle] = ident

        if arabe:
            cle = normaliser(arabe)
            if cle in vus_shu:
                erreurs.append(f"ligne {n} : traduction identique a {vus_shu[cle]}")
            else:
                vus_shu[cle] = ident
            nb = compter_mots(arabe)
            longueurs.append(nb)
            plafond = plafonds.get(dom, 18)
            if nb < mots_min:
                avertissements.append(
                    f"ligne {n} ({ident}) : {nb} mots, sous le minimum de {mots_min}"
                )
            elif nb > plafond:
                avertissements.append(
                    f"ligne {n} ({ident}) : {nb} mots, au-dessus du plafond de {plafond}"
                )

        if statut == "valide":
            if not arabe:
                erreurs.append(f"ligne {n} ({ident}) : statut valide sans ecriture arabe")
            if not latin:
                avertissements.append(
                    f"ligne {n} ({ident}) : statut valide sans translitteration latine"
                )
            if not ligne["traducteur"].strip() or not ligne["relecteur"].strip():
                erreurs.append(
                    f"ligne {n} ({ident}) : statut valide sans traducteur ET relecteur nommes"
                )
            if ligne["traducteur"].strip() == ligne["relecteur"].strip():
                erreurs.append(
                    f"ligne {n} ({ident}) : traducteur et relecteur sont la meme personne"
                )

    total = len(lignes)
    print(f"Banque : {total} phrases, {len(par_domaine)} domaines\n")

    print("Statuts")
    for st in ("valide", "a_verifier", "a_traduire", "rejete"):
        n = par_statut.get(st, 0)
        print(f"  {st:<12} {n:>6}  ({100 * n / total:4.1f} %)")

    print("\nEquilibre des domaines")
    print(f"  {'domaine':<15} {'reel':>6} {'part':>6} {'cible':>6} {'ecart':>6}")
    for code in parts:
        n = par_domaine.get(code, 0)
        reel = 100 * n / total
        ecart = reel - parts[code]
        marque = "  " if abs(ecart) <= tolerance else "!!"
        print(
            f"{marque}{code:<15} {n:>6} {reel:>5.1f}% {parts[code]:>5}% {ecart:>+5.1f}"
        )
        if abs(ecart) > tolerance:
            avertissements.append(
                f"domaine {code} ({titres[code]}) a {reel:.1f}% au lieu de {parts[code]}%"
            )

    if longueurs:
        longueurs.sort()
        med = longueurs[len(longueurs) // 2]
        print(
            f"\nLongueur des traductions : mediane {med} mots, "
            f"min {longueurs[0]}, max {longueurs[-1]}"
        )
        cible = plan["longueur"]["mots_cible_median"]
        if abs(med - cible) > 2:
            avertissements.append(
                f"mediane a {med} mots au lieu de {cible} : les segments audio "
                "ne feront pas la duree prevue"
            )

    valides = par_statut.get("valide", 0)
    lectures = valides * plan["lectures_par_phrase"]
    print(
        f"\nCapacite actuelle : {valides} phrases validees, "
        f"{lectures} lectures possibles, "
        f"soit {lectures * 7 / 3600:.1f} h d'audio au rythme de 7 s par phrase"
    )

    if avertissements:
        print(f"\n{len(avertissements)} avertissement(s)")
        for a in avertissements[:30]:
            print(f"  ~ {a}")
        if len(avertissements) > 30:
            print(f"  ... et {len(avertissements) - 30} autres")

    if erreurs:
        print(f"\n{len(erreurs)} ERREUR(S) bloquante(s)")
        for e in erreurs[:30]:
            print(f"  x {e}")
        if len(erreurs) > 30:
            print(f"  ... et {len(erreurs) - 30} autres")
        return 1

    print("\nAucune erreur bloquante.")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--banque", type=Path, default=RACINE / "banque" / "phrases.csv")
    p.add_argument("--plan", type=Path, default=RACINE / "banque" / "plan_domaines.yaml")
    a = p.parse_args()
    return verifier(a.banque, a.plan)


if __name__ == "__main__":
    sys.exit(main())
