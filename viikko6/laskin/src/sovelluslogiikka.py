class Sovelluslogiikka:
    def __init__(self, arvo=0):
        self._arvo = arvo

    def miinus(self, operandi):
        self._arvo = self._arvo - operandi

    def plus(self, operandi):
        self._arvo = self._arvo + operandi

    def nollaa(self):
        self._arvo = 0

    def aseta_arvo(self, arvo):
        self._arvo = arvo

    def arvo(self):
        return self._arvo


class Summa:
    def __init__(self, sovelluslogiikka, operandi):
        self._sovelluslogiikka = sovelluslogiikka
        self._operandi = operandi
        self._edellinen_arvo = 0

    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        arvo = int(self._operandi())
        self._sovelluslogiikka.plus(arvo)

    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)


class Erotus:
    def __init__(self, sovelluslogiikka, operandi):
        self._sovelluslogiikka = sovelluslogiikka
        self._operandi = operandi
        self._edellinen_arvo = 0

    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        arvo = int(self._operandi())
        self._sovelluslogiikka.miinus(arvo)

    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)


class Nollaus:
    def __init__(self, sovelluslogiikka, operandi):
        self._sovelluslogiikka = sovelluslogiikka
        self._operandi = operandi
        self._edellinen_arvo = 0

    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.nollaa()

    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)
