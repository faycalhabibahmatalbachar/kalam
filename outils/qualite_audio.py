#!/usr/bin/env python3
"""Controle qualite automatique des enregistrements, avant toute ecoute humaine.

Ecarte ce qui est mesurable : echantillonnage, saturation, niveau, rapport
signal sur bruit, silences de bord, duree incoherente avec le nombre de mots
attendu. Retire typiquement 10 a 15 % des fichiers et evite de payer une double
ecoute pour rien.

    python outils/qualite_audio.py --dossier enregistrements/LOC001 \\
        --plan livrets/LOC001/plan_seance_LOC001_s1.csv --rapport qc_LOC001.csv

    python outils/qualite_audio.py --dossier voix_tts/ --profil tts
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

try:
    import numpy as np
    import soundfile as sf
except ImportError:
    sys.exit(
        "numpy et soundfile sont requis :\n    pip install -r outils/requirements.txt"
    )

EXTENSIONS = {".wav", ".flac", ".ogg", ".mp3", ".m4a"}

# Deux jeux de seuils : la reconnaissance tolere du bruit, la synthese non.
PROFILS = {
    "asr": {
        "sr_min": 16000,
        "sr_conseille": 44100,
        "snr_min": 20.0,
        "pic_max_dbfs": -0.5,
        "pic_min_dbfs": -35.0,
        "satures_max": 10,
        "silence_bord_max_s": 1.5,
        "duree_min_s": 0.7,
        "duree_max_s": 30.0,
    },
    "tts": {
        "sr_min": 44100,
        "sr_conseille": 48000,
        "snr_min": 35.0,
        "pic_max_dbfs": -1.0,
        "pic_min_dbfs": -24.0,
        "satures_max": 0,
        "silence_bord_max_s": 0.8,
        "duree_min_s": 0.7,
        "duree_max_s": 20.0,
    },
}

# Debit de lecture observe en arabe tchadien : environ 0,42 s par mot,
# plus 0,8 s de silences de bord. Sert a reperer une phrase tronquee ou une
# phrase lue deux fois de suite dans le meme fichier.
SEC_PAR_MOT = 0.42
MARGE_BORD_S = 0.8
FACTEUR_MIN = 0.55
FACTEUR_MAX = 2.2


def dbfs(x: float) -> float:
    return 20 * math.log10(x) if x > 1e-12 else -120.0


def rms_par_trame(signal: np.ndarray, sr: int, ms: int = 25) -> np.ndarray:
    taille = max(1, int(sr * ms / 1000))
    n = len(signal) // taille
    if n == 0:
        return np.array([float(np.sqrt(np.mean(signal**2)))])
    trames = signal[: n * taille].reshape(n, taille)
    return np.sqrt(np.mean(trames**2, axis=1))


def mesurer(chemin: Path, seuils: dict, mots_attendus: int | None) -> dict:
    motifs: list[str] = []
    try:
        signal, sr = sf.read(str(chemin), always_2d=True, dtype="float32")
    except Exception as e:  # fichier illisible, tronque, format inconnu
        return {
            "fichier": chemin.name,
            "verdict": "rejet",
            "motifs": f"illisible ({e})",
        }

    canaux = signal.shape[1]
    mono = signal.mean(axis=1)
    duree = len(mono) / sr

    pic = float(np.max(np.abs(mono))) if len(mono) else 0.0
    pic_db = dbfs(pic)
    satures = int(np.sum(np.abs(mono) >= 0.999))

    trames = rms_par_trame(mono, sr)
    bruit = float(np.percentile(trames, 10))
    parole = float(np.percentile(trames, 95))
    snr = dbfs(parole) - dbfs(bruit)

    # Silences de bord : premiere et derniere trame au-dessus du plancher.
    seuil_actif = max(bruit * 3, parole * 0.1)
    actives = np.where(trames > seuil_actif)[0]
    duree_trame = 0.025
    if len(actives):
        debut = float(actives[0] * duree_trame)
        fin = float((len(trames) - 1 - actives[-1]) * duree_trame)
        duree_parole = float((actives[-1] - actives[0] + 1) * duree_trame)
    else:
        debut = fin = duree
        duree_parole = 0.0
        motifs.append("aucune parole detectee")

    if sr < seuils["sr_min"]:
        motifs.append(f"echantillonnage {sr} Hz sous le minimum {seuils['sr_min']}")
    if canaux > 1:
        motifs.append(f"{canaux} canaux au lieu de 1 (converti pour la mesure)")
    if satures > seuils["satures_max"]:
        motifs.append(f"saturation : {satures} echantillons a fond")
    if pic_db > seuils["pic_max_dbfs"]:
        motifs.append(f"niveau trop fort ({pic_db:.1f} dBFS)")
    if pic_db < seuils["pic_min_dbfs"]:
        motifs.append(f"niveau trop faible ({pic_db:.1f} dBFS)")
    if snr < seuils["snr_min"]:
        motifs.append(f"bruit de fond trop present (SNR {snr:.1f} dB)")
    if debut > seuils["silence_bord_max_s"]:
        motifs.append(f"silence de {debut:.1f} s au debut")
    if fin > seuils["silence_bord_max_s"]:
        motifs.append(f"silence de {fin:.1f} s a la fin")
    if duree < seuils["duree_min_s"]:
        motifs.append(f"fichier de {duree:.2f} s, trop court")
    if duree > seuils["duree_max_s"]:
        motifs.append(f"fichier de {duree:.1f} s, trop long")

    attendue = None
    if mots_attendus:
        attendue = mots_attendus * SEC_PAR_MOT + MARGE_BORD_S
        if duree < attendue * FACTEUR_MIN:
            motifs.append(
                f"duree {duree:.1f} s pour {mots_attendus} mots : phrase tronquee ?"
            )
        elif duree > attendue * FACTEUR_MAX:
            motifs.append(
                f"duree {duree:.1f} s pour {mots_attendus} mots : "
                "phrase lue deux fois, ou parole hors phrase ?"
            )

    # Un seul defaut de niveau ou de canaux se corrige, il n'entraine pas de rejet.
    reparables = ("canaux au lieu de 1", "niveau trop fort", "niveau trop faible")
    bloquants = [m for m in motifs if not any(r in m for r in reparables)]

    return {
        "fichier": chemin.name,
        "verdict": "rejet" if bloquants else ("a_corriger" if motifs else "ok"),
        "duree_s": round(duree, 2),
        "duree_parole_s": round(duree_parole, 2),
        "duree_attendue_s": round(attendue, 2) if attendue else "",
        "mots_attendus": mots_attendus or "",
        "sr": sr,
        "canaux": canaux,
        "pic_dbfs": round(pic_db, 1),
        "satures": satures,
        "snr_db": round(snr, 1),
        "silence_debut_s": round(debut, 2),
        "silence_fin_s": round(fin, 2),
        "motifs": " | ".join(motifs),
    }


def charger_mots(plan: Path | None) -> dict[str, int]:
    if not plan or not plan.exists():
        return {}
    with plan.open(encoding="utf-8-sig", newline="") as f:
        return {
            ligne["fichier"]: int(ligne["mots"] or 0)
            for ligne in csv.DictReader(f)
            if ligne.get("fichier")
        }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dossier", type=Path, required=True)
    p.add_argument("--plan", type=Path, help="plan_seance produit par livret.py")
    p.add_argument("--rapport", type=Path, default=Path("qc.csv"))
    p.add_argument("--profil", choices=sorted(PROFILS), default="asr")
    a = p.parse_args()

    if not a.dossier.is_dir():
        sys.exit(f"dossier introuvable : {a.dossier}")

    seuils = PROFILS[a.profil]
    mots = charger_mots(a.plan)
    fichiers = sorted(
        f for f in a.dossier.rglob("*") if f.suffix.lower() in EXTENSIONS
    )
    if not fichiers:
        sys.exit(f"aucun fichier audio dans {a.dossier}")

    resultats = [mesurer(f, seuils, mots.get(f.name)) for f in fichiers]

    colonnes = [
        "fichier", "verdict", "duree_s", "duree_parole_s", "duree_attendue_s",
        "mots_attendus", "sr", "canaux", "pic_dbfs", "satures", "snr_db",
        "silence_debut_s", "silence_fin_s", "motifs",
    ]
    a.rapport.parent.mkdir(parents=True, exist_ok=True)
    with a.rapport.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=colonnes, extrasaction="ignore", restval="")
        w.writeheader()
        for r in resultats:
            w.writerow(r)

    ok = sum(1 for r in resultats if r["verdict"] == "ok")
    corr = sum(1 for r in resultats if r["verdict"] == "a_corriger")
    rej = sum(1 for r in resultats if r["verdict"] == "rejet")
    total_s = sum(float(r.get("duree_s") or 0) for r in resultats if r["verdict"] != "rejet")

    print(f"Profil {a.profil} : {len(resultats)} fichiers")
    print(f"  ok          {ok:>5}")
    print(f"  a corriger  {corr:>5}   (niveau ou canaux, recuperables)")
    print(f"  rejet       {rej:>5}   ({100 * rej / len(resultats):.1f} %)")
    print(f"  audio retenu : {total_s / 60:.1f} min")

    if rej:
        print("\nPremiers rejets")
        for r in resultats:
            if r["verdict"] == "rejet":
                print(f"  {r['fichier']:<32} {r['motifs']}")
        print()
    print(f"Rapport : {a.rapport}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
