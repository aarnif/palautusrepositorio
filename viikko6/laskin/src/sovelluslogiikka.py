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

    def suorita(self):
        arvo = int(self._operandi())
        self._sovelluslogiikka.plus(arvo)


class Erotus:
    def __init__(self, sovelluslogiikka, operandi):
        self._sovelluslogiikka = sovelluslogiikka
        self._operandi = operandi

    def suorita(self):
        arvo = int(self._operandi())
        self._sovelluslogiikka.miinus(arvo)


class Nollaus:
    def __init__(self, sovelluslogiikka, operandi):
        self._sovelluslogiikka = sovelluslogiikka
        self._operandi = operandi

    def suorita(self):
        self._sovelluslogiikka.nollaa()
