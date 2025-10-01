import random
import tkinter as tk


class Spieler:

    def __init__(self, name: str, bild: tk.PhotoImage, spiel: 'Spiel'):
        # Datenmodell
        self.name = name

        # View
        frame = tk.Frame(spiel.fenster)
        self.label = tk.Label(frame, text=name)
        self.label.pack(side=tk.TOP)

        for feld in range(3):
            Feld(frame, Figur(self, bild), spiel).view.pack()

        frame.pack(side=tk.LEFT)

        self.view = frame

    def markiere_dich(self, an: bool):
        if an:
            self.label.config(bg='red')
        else:
            self.label.config(bg='SystemButtonFace')


class Figur:

    def __init__(self, spieler: Spieler, bild: tk.PhotoImage):
        # Datenmodell
        self.spieler = spieler
        self.bild = bild


class Feld:

    def __init__(self, frame: tk.Frame, figur: Figur, spiel: 'Spiel'):
        # Datenmodell
        self.figur = figur
        self.spieler = figur.spieler
        self.spiel = spiel

        # View
        self.view = tk.Frame(frame)

        self.setze_figur(figur)

    def setze_figur(self, figur: Figur):
        self.figur = figur

        for widget in self.view.winfo_children():
            widget.destroy()

        label = tk.Label(self.view, image=figur.bild)
        label.pack(pady=5, padx=5)
        label.bind('<Button-1>', lambda event: self.spiel.click(self))

    def markiere_dich(self, an: bool):
        if an:
            self.view.config(bg='blue')
        else:
            if self.spieler is None:
                self.view.config(bg='gray')
            else:
                self.view.config(bg='SystemButtonFace')


class Spielbrett:

    def __init__(self, spiel: 'Spiel', blank: tk.PhotoImage):
        # View
        frame = tk.Frame(spiel.fenster)

        # Datenmodell
        self.spielfelder = tuple(tuple(Feld(frame, Figur(None, blank), spiel) for x in range(3)) for y in range(3))

        for x in range(3):
            for y in range(3):
                self.spielfelder[x][y].view.grid(column=x, row=y)
                self.spielfelder[x][y].view.config(bg='gray')
        frame.pack(side=tk.LEFT)
        self.view = frame


class Spiel:

    def __init__(self, bild_blank: str, bild_spieler1: str, bild_spieler2: str):
        self.fenster = tk.Tk()
        self.bilder = (
        tk.PhotoImage(file=bild_blank), tk.PhotoImage(file=bild_spieler1), tk.PhotoImage(file=bild_spieler2))

        # erstellt die Struktur

        self.spieler = []
        # Spieler 1
        spieler = Spieler('Spieler 1', self.bilder[1], self)
        self.spieler.append(spieler)

        # Spielbrett
        self.spielbrett = Spielbrett(self, self.bilder[0])

        # Spieler 2
        spieler = Spieler('Spieler 2', self.bilder[2], self)
        self.spieler.append(spieler)

        self.aktiver_spieler = random.randint(0, 1)
        self.spieler[self.aktiver_spieler].markiere_dich(True)

        self.zustand = 'von'

        self.fenster.mainloop()

    def spieler_wechsel(self):
        if self.gewonnen():
            return

        self.spieler[self.aktiver_spieler].markiere_dich(False)
        self.aktiver_spieler = 1 - self.aktiver_spieler
        self.spieler[self.aktiver_spieler].markiere_dich(True)

    def gewonnen(self) -> bool:
        moegliche_gewinnpositionen = (
            ((0, 0), (1, 1), (2, 2)),
            ((0, 2), (1, 1), (2, 0)),
            ((0, 0), (0, 1), (0, 2)),
            ((1, 0), (1, 1), (1, 2)),
            ((2, 0), (2, 1), (2, 2)),
            ((0, 0), (1, 0), (2, 0)),
            ((0, 1), (1, 1), (2, 1)),
            ((0, 2), (1, 2), (2, 2)))
        for gewinnposition in moegliche_gewinnpositionen:
            s =self.spieler[self.aktiver_spieler]
            if (self.spielbrett.spielfelder[gewinnposition[0][0]][gewinnposition[0][1]].figur.spieler == s and
                self.spielbrett.spielfelder[gewinnposition[1][0]][gewinnposition[1][1]].figur.spieler == s and
                self.spielbrett.spielfelder[gewinnposition[2][0]][gewinnposition[2][1]].figur.spieler == s):

                for widget in self.fenster.winfo_children():
                    widget.destroy()

                tk.Label(self.fenster, text=self.spieler[self.aktiver_spieler].name + " hat gewonnen!").pack(pady=20, padx=20)

                return True
        return False

    def click(self, feld: Feld):

        if self.zustand == 'von':
            if feld.figur.spieler:
                if feld.figur.spieler == self.spieler[self.aktiver_spieler]:
                    # markiere das Feld
                    feld.markiere_dich(True)
                    # merke dir das Feld
                    self.von_feld = feld
                    # wechsel den Zustand
                    self.zustand = 'nach'
                    # (warte auf nächsten Klick)
        else:
            if feld.figur.spieler is None:
                if feld.spieler is None:
                    figur = self.von_feld.figur
                    self.von_feld.setze_figur(feld.figur)
                    self.von_feld.markiere_dich(False)
                    feld.setze_figur(figur)

                    self.spieler_wechsel()
                    self.zustand = 'von'


bild_spieler1 = 'ritter.png'
bild_spieler2 = 'wikinger.png'
bild_blank = 'blank.png'
Spiel(bild_blank, bild_spieler1, bild_spieler2)
