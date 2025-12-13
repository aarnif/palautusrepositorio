from kivi_paperi_sakset import KiviPaperiSakset


class KPSPelaajaVsPelaaja(KiviPaperiSakset):
    # toteutetaan metodi pelityypin mukaisesti
    def _toisen_siirto(self, ensimmaisen_siirto):
        tokan_siirto = input("Toisen pelaajan siirto: ")

        return tokan_siirto
