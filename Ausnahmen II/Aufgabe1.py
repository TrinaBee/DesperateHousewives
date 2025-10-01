def kehrwert():
    try:
        wert = int(input("Geben Sie eine Ganzzahl ein!:"))
        kehrwert = 1 / wert
    except ZeroDivisionError:
        print("Fehler: Division durch Null ist nicht erlaubt.")
    except ValueError:
        print("Fehler: Ungültige Eingabe. Bitte geben Sie eine ganze Zahl ein.")
    else:
        return kehrwert
    finally:
        print("Programm wurde beendet.")


kehrwert()