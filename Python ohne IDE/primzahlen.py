import time
def ist_primzahl(x: int) -> bool:
    if x <= 1:
        return False
    for i in range(2, x):
        if x % i == 0:
            return False
    return True


def anzahl_primzahlen_von_1_bis_n(n: int):
    return len([x for x in range(1, n + 1) if ist_primzahl(x)])


start = time.time()
print("Beginne Berechnung...")
print(anzahl_primzahlen_von_1_bis_n(100_000))
print("Dauer:", time.time() - start, "Sekunden")