def lesen():
    try:
        name = str(input("Bitte geben Sie den Dateinamen ein:"))
        datei = open(name, "rt")
        print(datei.read())
    except FileNotFoundError as e:
        print(f"Die Datei {e.filename} konnte nicht gefunden werden.\n Fehlernummer {e.errno} ({e.strerror})")


lesen()
