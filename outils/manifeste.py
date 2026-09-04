#!/usr/bin/env python3
"""Assemble le corpus : plans de seance + controle qualite + double ecoute + locuteurs.

Ne retient qu'un enregistrement qui a passe les quatre etapes :
  1. il figure dans un plan de seance (donc son texte est connu d'avance) ;
  2. son locuteur figure dans terrain/locuteurs.csv avec une reference de
     consentement non vide ;
  3. son verdict de controle qualite n'est pas 'rejet' ;
  4. deux validateurs differents l'ont accepte.

Produit le manifeste et le bilan de diversite, puis signale les ecarts aux
quotas de banque/plan_diversite.yaml.

    python outils/manifeste.py --audio enregistrements --sortie corpus/manifeste.csv
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent


def charger_yaml(chemin: Path) -> dict:
    try:
        import yaml
    except ImportError:
        sys.exit("PyYAML manquant : pip install -r outils/requirements.txt")
    with chemin.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def lire_csv(chemin: Path) -> list[dict]:
    if not chemin.exists():
        return []
    with chemin.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def lire_glob(racine: Path, motif: str) -> list[dict]:
    lignes: list[dict] = []
    for chemin in sorted(racine.glob(motif)):
        lignes.extend(lire_csv(chemin))
    return lignes


def groupe_langue(langue: str) -> str:
    langue = (langue or "").strip().lower()
    return "shu" if langue in {"shu", "arabe tchadien", "arabe_tchadien"} else "autre"


def double_ecoute(validations: list[dict]) -> dict[str, tuple[str, list[str]]]:
    """Applique la regle : 2 acceptations valident, 2 rejets ecartent, 1-1 attend."""
    par_fichier: dict[str, list[dict]] = collections.defaultdict(list)
    for v in validations:
        if v.get("fichier"):
            par_fichier[v["fichier"]].append(v)

    resultat: dict[str, tuple[str, list[str]]] = {}
    for fichier, votes in par_fichier.items():
        # Un validateur ne compte qu'une fois, meme s'il a ecoute deux fois.
        vus: dict[str, str] = {}
        for v in votes:
            vus[(v.get("validateur") or "").strip()] = (v.get("verdict") or "").strip()
        acc = [n for n, verdict in vus.items() if verdict == "accepte"]
        rej = [n for n, verdict in vus.items() if verdict == "rejete"]
        motifs = [v.get("motif", "") for v in votes if v.get("motif")]
        if len(acc) >= 2:
            resultat[fichier] = ("valide", motifs)
        elif len(rej) >= 2:
            resultat[fichier] = ("ecarte", motifs)
        else:
            resultat[fichier] = ("en_attente", motifs)
    return resultat


def assembler(a: argparse.Namespace) -> int:
    plans = lire_glob(a.livrets, "*/plan_seance_*.csv")
    if not plans:
        print(f"Aucun plan de seance sous {a.livrets}. Lancer d'abord outils/livret.py.")
        return 1

    locuteurs = {l["id_locuteur"]: l for l in lire_csv(a.locuteurs) if l.get("id_locuteur")}
    qc = {q["fichier"]: q for q in lire_glob(a.qc.parent, a.qc.name) if q.get("fichier")}
    verdicts = double_ecoute(lire_csv(a.validations))

    audios = {f.name: f for f in a.audio.rglob("*") if f.is_file()}

    retenus: list[dict] = []
    exclus = collections.Counter()

    for p in plans:
        fichier = p["fichier"]
        loc = locuteurs.get(p["id_locuteur"])

        if fichier not in audios:
            exclus["fichier audio absent"] += 1
            continue
        if loc is None:
            exclus["locuteur absent de locuteurs.csv"] += 1
            continue
        if not (loc.get("consentement_reference") or "").strip():
            exclus["consentement non reference"] += 1
            continue
        mesure = qc.get(fichier)
        if mesure is None:
            exclus["controle qualite non effectue"] += 1
            continue
        if mesure["verdict"] == "rejet":
            exclus["rejet au controle qualite"] += 1
            continue
        etat = verdicts.get(fichier, ("en_attente", []))[0]
        if etat != "valide":
            exclus[f"double ecoute : {etat}"] += 1
            continue

        retenus.append(
            {
                "fichier": fichier,
                "chemin": str(audios[fichier].relative_to(a.audio)).replace("\\", "/"),
                "id_phrase": p["id_phrase"],
                "id_locuteur": p["id_locuteur"],
                "seance": p.get("seance", ""),
                "domaine": p.get("domaine", ""),
                "source": "lecture",
                "texte": p["shu_arabe"],
                "texte_latin": p.get("shu_latin", ""),
                "traduction_fr": p.get("fr", ""),
                "duree_s": mesure.get("duree_s", ""),
                "sr": mesure.get("sr", ""),
                "snr_db": mesure.get("snr_db", ""),
                "genre": loc.get("genre", ""),
                "tranche_age": loc.get("tranche_age", ""),
                "ville_collecte": loc.get("ville_collecte", ""),
                "region_origine": loc.get("region_origine", ""),
                "langue_premiere": loc.get("langue_premiere", ""),
                "licence": "CC-BY-4.0",
            }
        )

    if not retenus:
        print("Aucun enregistrement retenu.")
        for motif, n in exclus.most_common():
            print(f"  {n:>5}  {motif}")
        return 1

    a.sortie.parent.mkdir(parents=True, exist_ok=True)
    with a.sortie.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(retenus[0].keys()))
        w.writeheader()
        w.writerows(retenus)

    chemin_jsonl = a.sortie.with_suffix(".jsonl")
    with chemin_jsonl.open("w", encoding="utf-8") as f:
        for r in retenus:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # ---- bilan ----
    plan = charger_yaml(a.plan_diversite)
    tol = plan["tolerance_points"]
    total_s = sum(float(r["duree_s"] or 0) for r in retenus)
    par_loc = collections.Counter(r["id_locuteur"] for r in retenus)
    secondes_par_loc = collections.Counter()
    for r in retenus:
        secondes_par_loc[r["id_locuteur"]] += float(r["duree_s"] or 0)

    print(f"Corpus : {len(retenus)} enregistrements, {total_s / 3600:.2f} h, "
          f"{len(par_loc)} locuteurs")
    print(f"  duree mediane par locuteur : "
          f"{sorted(secondes_par_loc.values())[len(secondes_par_loc) // 2] / 60:.1f} min")

    if exclus:
        print("\nEcartes")
        for motif, n in exclus.most_common():
            print(f"  {n:>5}  {motif}")

    alertes: list[str] = []

    def comparer(titre: str, cle: str, cibles: dict, transformer=lambda v: v) -> None:
        compte = collections.Counter(transformer(r[cle]) for r in retenus)
        n = sum(compte.values())
        print(f"\n{titre}")
        for valeur, part in cibles.items():
            reel = 100 * compte.get(str(valeur), 0) / n if n else 0
            ecart = reel - part
            marque = "  " if abs(ecart) <= tol else "!!"
            print(f"{marque}{str(valeur):<18} {compte.get(str(valeur), 0):>5} "
                  f"{reel:>5.1f}% (cible {part}%)")
            if abs(ecart) > tol:
                alertes.append(f"{titre} / {valeur} : {reel:.1f}% au lieu de {part}%")
        inconnus = set(compte) - {str(v) for v in cibles}
        if inconnus:
            print(f"  hors plan : {', '.join(sorted(inconnus))}")

    comparer("Genre", "genre", plan["genre"])
    comparer("Tranche d'age", "tranche_age", plan["tranche_age"])
    comparer("Ville de collecte", "ville_collecte", plan["ville_collecte"])
    comparer("Langue premiere", "langue_premiere", plan["langue_premiere_groupe"],
             groupe_langue)

    plafonds = plan["plafonds"]
    for loc, sec in secondes_par_loc.items():
        part = 100 * sec / total_s if total_s else 0
        if part > plafonds["part_max_un_locuteur"]:
            alertes.append(
                f"le locuteur {loc} pese {part:.1f}% du corpus "
                f"(plafond {plafonds['part_max_un_locuteur']}%)"
            )
        if sec / 60 > plafonds["minutes_max_par_locuteur"]:
            alertes.append(
                f"le locuteur {loc} totalise {sec / 60:.0f} min "
                f"(plafond {plafonds['minutes_max_par_locuteur']})"
            )

    if alertes:
        print(f"\n{len(alertes)} ecart(s) aux quotas, a publier avec le corpus")
        for x in alertes:
            print(f"  ~ {x}")
    else:
        print("\nQuotas de diversite respectes.")

    print(f"\n{a.sortie}\n{chemin_jsonl}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--audio", type=Path, default=RACINE / "enregistrements")
    p.add_argument("--livrets", type=Path, default=RACINE / "livrets")
    p.add_argument("--locuteurs", type=Path, default=RACINE / "terrain" / "locuteurs.csv")
    p.add_argument("--validations", type=Path,
                   default=RACINE / "terrain" / "validations.csv")
    p.add_argument("--qc", type=Path, default=RACINE / "terrain" / "qc_*.csv",
                   help="motif des rapports de controle qualite")
    p.add_argument("--plan-diversite", type=Path,
                   default=RACINE / "banque" / "plan_diversite.yaml")
    p.add_argument("--sortie", type=Path, default=RACINE / "corpus" / "manifeste.csv")
    return assembler(p.parse_args())


if __name__ == "__main__":
    sys.exit(main())
