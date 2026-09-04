#!/usr/bin/env python3
"""Fabrique le livret de lecture d'un locuteur et le plan de seance qui va avec.

Le livret est un fichier HTML pret a imprimer (ou a lire sur telephone) ; le plan
de seance est le CSV qui relie chaque numero de phrase au nom de fichier audio
attendu. C'est ce CSV que lisent ensuite qualite_audio.py et manifeste.py.

Le choix des phrases obeit a trois regles, dans cet ordre :
  1. le locuteur ne relit jamais une phrase qu'il a deja lue ;
  2. les proportions de domaines du livret suivent banque/plan_domaines.yaml ;
  3. a l'interieur d'un domaine, on prend d'abord les phrases qui manquent le
     plus de lectures, puis celles qui apportent le plus de bigrammes nouveaux
     (approximation de couverture sonore sans dictionnaire phonetique).

    python outils/livret.py --locuteur LOC001 --phrases 240
    python outils/livret.py --locuteur LOC001 --phrases 240 --seance 2
"""
from __future__ import annotations

import argparse
import collections
import csv
import html
import re
import sys
from datetime import date
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

# Lettres arabes et signes de vocalisation ; tout le reste est ignore pour la
# couverture (espaces, ponctuation, chiffres latins).
MOTIF_ARABE = re.compile(r"[ء-يً-ْٰ]")


def bigrammes(texte: str) -> set[str]:
    suite = "".join(MOTIF_ARABE.findall(texte))
    return {suite[i : i + 2] for i in range(len(suite) - 1)}


def charger_plan(chemin: Path) -> dict:
    try:
        import yaml
    except ImportError:
        sys.exit("PyYAML manquant : pip install -r outils/requirements.txt")
    with chemin.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def charger_journal(chemin: Path) -> tuple[collections.Counter, dict[str, set[str]]]:
    """Retourne (lectures par phrase, phrases deja lues par locuteur)."""
    faites: collections.Counter = collections.Counter()
    par_locuteur: dict[str, set[str]] = collections.defaultdict(set)
    if not chemin.exists():
        return faites, par_locuteur
    with chemin.open(encoding="utf-8-sig", newline="") as f:
        for ligne in csv.DictReader(f):
            pid = (ligne.get("id_phrase") or "").strip()
            loc = (ligne.get("id_locuteur") or "").strip()
            if not pid:
                continue
            faites[pid] += 1
            if loc:
                par_locuteur[loc].add(pid)
    return faites, par_locuteur


def choisir(
    phrases: list[dict],
    quotas: dict[str, int],
    faites: collections.Counter,
    deja_lues: set[str],
    total: int,
) -> tuple[list[dict], set[str]]:
    disponibles = [
        p
        for p in phrases
        if p["statut"] == "valide"
        and p["shu_arabe"].strip()
        and p["id"] not in deja_lues
        and faites[p["id"]] < int(p["lectures_cible"] or 3)
    ]
    if not disponibles:
        return [], set()

    par_domaine: dict[str, list[dict]] = collections.defaultdict(list)
    for p in disponibles:
        par_domaine[p["domaine"]].append(p)

    # Nombre de phrases visees pour chaque domaine dans ce livret.
    cibles = {code: round(part / 100 * total) for code, part in quotas.items()}

    choisies: list[dict] = []
    prises: set[str] = set()
    couverture: set[str] = set()

    for code in sorted(cibles, key=lambda c: -cibles[c]):
        candidats = par_domaine.get(code, [])
        for _ in range(min(cibles[code], len(candidats))):
            meilleur, meilleur_score = None, None
            for p in candidats:
                if p["id"] in prises:
                    continue
                manque = int(p["lectures_cible"] or 3) - faites[p["id"]]
                nouveaux = len(bigrammes(p["shu_arabe"]) - couverture)
                score = (manque * 3) + nouveaux
                if meilleur_score is None or score > meilleur_score:
                    meilleur, meilleur_score = p, score
            if meilleur is None:
                break
            choisies.append(meilleur)
            prises.add(meilleur["id"])
            couverture |= bigrammes(meilleur["shu_arabe"])

    # S'il manque des phrases (domaine epuise), on complete au meilleur apport.
    reste = [p for p in disponibles if p["id"] not in prises]
    while len(choisies) < total and reste:
        meilleur = max(reste, key=lambda p: len(bigrammes(p["shu_arabe"]) - couverture))
        choisies.append(meilleur)
        prises.add(meilleur["id"])
        couverture |= bigrammes(meilleur["shu_arabe"])
        reste.remove(meilleur)

    return choisies, couverture


GABARIT = """<meta charset="utf-8">
<title>Livret {loc} - seance {seance}</title>
<style>
  @page {{ size: A4; margin: 15mm; }}
  body {{ font-family: "Segoe UI", system-ui, sans-serif; color: #111; margin: 0; }}
  .garde {{ page-break-after: always; }}
  h1 {{ font-size: 26px; margin: 0 0 4px; }}
  .sous {{ color: #555; font-size: 14px; margin-bottom: 24px; }}
  .consignes {{ background: #f5f3ee; border-left: 4px solid #b08d57;
                padding: 14px 18px; font-size: 14px; line-height: 1.65; }}
  .consignes li {{ margin-bottom: 6px; }}
  table.meta {{ border-collapse: collapse; margin-top: 20px; font-size: 14px; }}
  table.meta td {{ border: 1px solid #ccc; padding: 7px 12px; }}
  table.meta td:first-child {{ background: #fafafa; font-weight: 600; width: 190px; }}
  .phrase {{ border-bottom: 1px solid #e4e4e4; padding: 14px 0; page-break-inside: avoid; }}
  .num {{ display: inline-block; min-width: 54px; font-weight: 700;
          color: #b08d57; font-size: 15px; vertical-align: top; }}
  .corps {{ display: inline-block; width: calc(100% - 60px); }}
  .ar {{ direction: rtl; text-align: right; font-size: 27px; line-height: 1.9;
         font-family: "Traditional Arabic", "Amiri", "Noto Naskh Arabic", serif; }}
  .lat {{ color: #666; font-size: 14px; font-style: italic; margin-top: 3px; }}
  .fr {{ color: #999; font-size: 12px; margin-top: 2px; }}
  .fichier {{ color: #b08d57; font-size: 11px; font-family: monospace; margin-top: 3px; }}
</style>

<div class="garde">
  <h1>Livret de lecture - Kalam</h1>
  <div class="sous">Corpus ouvert de l'arabe tchadien &middot; {date}</div>

  <div class="consignes">
    <strong>Avant de commencer</strong>
    <ol>
      <li>Piece fermee, sans ventilateur, sans climatisation, sans radio.</li>
      <li>Micro du casque a environ 3 doigts du coin de la bouche, jamais devant.</li>
      <li>Lire les 3 premieres phrases, ecouter, corriger la distance : c'est l'etape
          qu'on saute et qu'on regrette.</li>
      <li><strong>Un fichier par phrase.</strong> Le nom du fichier est ecrit sous
          chaque phrase, en petit.</li>
      <li>Une hesitation, un mot avale : on recommence la phrase entiere, on ne
          recolle pas un morceau.</li>
      <li>Une phrase qu'on ne comprend pas ou qui sonne faux : on la saute et on
          entoure son numero. C'est un signal sur la phrase, pas sur le lecteur.</li>
      <li>Lire naturellement, a la vitesse ordinaire. Ni theatre, ni dictee.</li>
    </ol>
  </div>

  <table class="meta">
    <tr><td>Identifiant locuteur</td><td>{loc}</td></tr>
    <tr><td>Seance</td><td>{seance}</td></tr>
    <tr><td>Nombre de phrases</td><td>{n}</td></tr>
    <tr><td>Duree estimee au micro</td><td>{minutes} minutes</td></tr>
    <tr><td>Date de la seance</td><td>&nbsp;</td></tr>
    <tr><td>Lieu / ville</td><td>&nbsp;</td></tr>
    <tr><td>Materiel utilise</td><td>&nbsp;</td></tr>
    <tr><td>Consentement signe</td><td>oui / non&nbsp;&nbsp;(sans signature, pas de seance)</td></tr>
    <tr><td>Phrases sautees</td><td>&nbsp;</td></tr>
  </table>
</div>

{corps}
"""


def fabriquer(args: argparse.Namespace) -> int:
    plan = charger_plan(args.plan)
    quotas = {d["code"]: d["part"] for d in plan["domaines"]}

    with args.banque.open(encoding="utf-8-sig", newline="") as f:
        phrases = list(csv.DictReader(f))

    faites, par_locuteur = charger_journal(args.journal)
    deja = par_locuteur.get(args.locuteur, set())

    choisies, couverture = choisir(phrases, quotas, faites, deja, args.phrases)
    if not choisies:
        print(
            "Aucune phrase disponible.\n"
            "Causes possibles : la banque ne contient encore aucune ligne au statut "
            "'valide', ou ce locuteur a deja lu tout ce qui reste a lire.\n"
            "Verifier avec : python outils/verifier_banque.py"
        )
        return 1

    dossier = args.sortie / args.locuteur
    dossier.mkdir(parents=True, exist_ok=True)

    blocs = []
    lignes_plan = []
    for i, p in enumerate(choisies, start=1):
        fichier = f"{args.locuteur}_s{args.seance}_{i:03d}.wav"
        blocs.append(
            '<div class="phrase"><span class="num">{i:03d}</span>'
            '<div class="corps">'
            '<div class="ar">{ar}</div>'
            '<div class="lat">{lat}</div>'
            '<div class="fr">{fr}</div>'
            '<div class="fichier">{f}</div>'
            "</div></div>".format(
                i=i,
                ar=html.escape(p["shu_arabe"]),
                lat=html.escape(p["shu_latin"]),
                fr=html.escape(p["fr"]),
                f=fichier,
            )
        )
        lignes_plan.append(
            {
                "ordre": i,
                "fichier": fichier,
                "id_phrase": p["id"],
                "id_locuteur": args.locuteur,
                "seance": args.seance,
                "domaine": p["domaine"],
                "shu_arabe": p["shu_arabe"],
                "shu_latin": p["shu_latin"],
                "fr": p["fr"],
                "mots": len(p["shu_arabe"].split()),
            }
        )

    minutes = round(len(choisies) * 7 / 60 / 0.62)
    page = GABARIT.format(
        loc=html.escape(args.locuteur),
        seance=args.seance,
        n=len(choisies),
        minutes=minutes,
        date=date.today().isoformat(),
        corps="\n".join(blocs),
    )
    chemin_html = dossier / f"livret_{args.locuteur}_s{args.seance}.html"
    chemin_html.write_text(page, encoding="utf-8")

    chemin_csv = dossier / f"plan_seance_{args.locuteur}_s{args.seance}.csv"
    with chemin_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(lignes_plan[0].keys()))
        w.writeheader()
        w.writerows(lignes_plan)

    repartition = collections.Counter(p["domaine"] for p in choisies)
    print(f"Livret {args.locuteur} seance {args.seance}")
    print(f"  {len(choisies)} phrases, {minutes} min de micro estimees")
    print(f"  {len(couverture)} bigrammes arabes distincts couverts")
    print("  repartition :", ", ".join(f"{d}={n}" for d, n in repartition.most_common()))
    print(f"  {chemin_html}")
    print(f"  {chemin_csv}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--locuteur", required=True, help="identifiant, ex. LOC001")
    p.add_argument("--phrases", type=int, default=240, help="240 = une seance de 45 min")
    p.add_argument("--seance", type=int, default=1)
    p.add_argument("--banque", type=Path, default=RACINE / "banque" / "phrases.csv")
    p.add_argument("--plan", type=Path, default=RACINE / "banque" / "plan_domaines.yaml")
    p.add_argument("--journal", type=Path, default=RACINE / "terrain" / "lectures.csv")
    p.add_argument("--sortie", type=Path, default=RACINE / "livrets")
    return fabriquer(p.parse_args())


if __name__ == "__main__":
    sys.exit(main())
