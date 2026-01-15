"""
Les mots de la langue française
Manipulation d'un corpus de mots (1 mot par ligne).
"""

from __future__ import annotations

import random
from typing import Iterable


def read_data(filename: str) -> list[str]:
    """
    Lit un fichier texte contenant 1 mot par ligne et renvoie la liste des mots.

    On retire le '\n' final de chaque ligne via str.strip() (ou rstrip('\n')).
    """
    with open(filename, "r", encoding="utf-8") as f:
        # strip() retire aussi d'éventuels espaces/retours chariot
        return [line.strip() for line in f]


def ensemble_mots(filename: str) -> set[str]:
    """
    Renvoie l'ensemble (set) des mots du fichier, sans duplication de code :
    on réutilise read_data().
    """
    return set(read_data(filename))


def mots_de_n_lettres(mots: set[str], n: int) -> set[str]:
    """Sous-ensemble des mots de longueur n."""
    return {w for w in mots if len(w) == n}


def mots_avec(mots: set[str], s: str) -> set[str]:
    """Sous-ensemble des mots contenant la chaîne s."""
    return {w for w in mots if s in w}


def cherche1(mots: set[str], start: str, stop: str, n: int) -> set[str]:
    """
    Mots de n lettres commençant par start et se terminant par stop.
    """
    return {
        w
        for w in mots
        if len(w) == n and w.startswith(start) and w.endswith(stop)
    }


def _contains_mid_not_edges(word: str, mid: str) -> bool:
    """
    True si mid apparaît dans word mais ni au début ni à la fin.
    Ex: mid='ç' -> il faut un 'ç' quelque part sauf en position 0 ou dernière.
    """
    if not mid:
        return False
    i = word.find(mid)
    while i != -1:
        if i > 0 and i + len(mid) < len(word):
            return True
        i = word.find(mid, i + 1)
    return False


def cherche2(
    mots: set[str],
    lstart: list[str],
    lmid: list[str],
    lstop: list[str],
    nmin: int,
    nmax: int,
) -> set[str]:
    """
    Sous-ensemble des mots :
    - longueur entre nmin et nmax (inclus)
    - commence par un élément de lstart
    - contient un élément de lmid, ni au début ni à la fin
    - se termine par un élément de lstop
    """
    res: set[str] = set()

    for w in mots:
        lw = len(w)
        if lw < nmin or lw > nmax:
            continue

        if lstart and not any(w.startswith(st) for st in lstart):
            continue

        if lstop and not any(w.endswith(sp) for sp in lstop):
            continue

        if lmid:
            ok_mid = any(_contains_mid_not_edges(w, mid) for mid in lmid)
            if not ok_mid:
                continue

        res.add(w)

    return res


def _sample_display(items: Iterable[str], k: int = 10) -> list[str]:
    """Affiche un échantillon aléatoire (sans erreur si pas assez d'items)."""
    lst = list(items)
    if not lst:
        return []
    k = min(k, len(lst))
    return random.sample(lst, k)


def main() -> None:
    filename = "corpus.txt"

    # --- Lecture des données
    data = read_data(filename)
    print(f"Nombre de lignes (mots) : {len(data)}")

    positions = [24499, 28281, 57305, 118091, 199316, 223435, 336455]
    print("\nMots aux positions demandées (je montre 1-based et 0-based pour être sûr) :")
    for p in positions:
        w1 = data[p - 1] if 1 <= p <= len(data) else None  # position humaine (ligne p)
        w0 = data[p] if 0 <= p < len(data) else None       # index python (p)
        print(f"p={p:6d} | 1-based -> {w1!r} | 0-based -> {w0!r}")

    # --- L'ensemble des mots
    mots = ensemble_mots(filename)
    print(f"\nNombre de mots distincts (set) : {len(mots)}")

    for test_word in ["chronophage", "procrastinateur", "dangerosité", "gratifiant"]:
        print(f"{test_word!r} in mots ? -> {test_word in mots}")

    # --- Mots de n lettres (Scrabble : 7 lettres)
    mots7 = mots_de_n_lettres(mots, 7)
    print(f"\nNombre de mots de 7 lettres : {len(mots7)}")
    print("Exemples :", _sample_display(mots7, k=10))

    # Même idée pour d'autres tailles (exemple)
    for n in [2, 3, 4, 8, 10, 12]:
        subset = mots_de_n_lettres(mots, n)
        print(f"Nombre de mots de {n} lettres : {len(subset)}")

    # Distribution longueur -> nombre de mots (sans tracer)
    dist = {}
    for w in mots:
        dist[len(w)] = dist.get(len(w), 0) + 1
    print("\nDistribution (longueur -> nombre de mots), extrait :")
    for length in sorted(dist)[:15]:
        print(f"{length:2d} -> {dist[length]}")

    # --- Mots spéciaux : contenant 'k' puis 'oo'
    with_k = mots_avec(mots, "k")
    print(f"\nNombre de mots contenant 'k' : {len(with_k)}")
    print("Exemples :", _sample_display(with_k, k=10))

    with_oo = mots_avec(mots, "oo")
    print(f"Nombre de mots contenant 'oo' : {len(with_oo)}")
    print("Exemples :", _sample_display(with_oo, k=10))

    # --- Recherche complexe (cherche1)
    z14 = cherche1(mots, start="z", stop="", n=14)  # stop="" => pas de contrainte de fin
    print(f"\nMots de 14 lettres commençant par 'z' : {len(z14)}")
    print("Exemples :", _sample_display(z14, k=10))

    endz18 = cherche1(mots, start="", stop="z", n=18)  # start="" => pas de contrainte de début
    print(f"Mots de 18 lettres se terminant par 'z' : {len(endz18)}")
    print("Exemples :", _sample_display(endz18, k=10))

    sur_ons_17 = {
        w
        for w in cherche1(mots,
