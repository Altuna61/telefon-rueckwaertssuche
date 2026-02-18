# unittest ist das eingebaute Test-Modul von Python
import unittest

# Importiert die Funktion suche_nummer aus meiner Hauptdatei
# Wichtig: Dateiname muss exakt stimmen (ohne .py am Ende)
from telefonabfrage import suche_nummer


# Testklasse für die Rückwärtssuche
# Erbt von unittest.TestCase → dadurch erkennt Python es als Test
class TestRueckwaertssuche(unittest.TestCase):

    # Test 1: Prüft, was passiert, wenn keine Nummer eingegeben wird
    def test_leere_nummer(self):
        # Funktion mit leerem String aufrufen
        result = suche_nummer("")
        # Prüfen, ob die richtige Fehlermeldung enthalten ist
        # assertIn(a,b) -> prüft,ob a irgendwo in b drin ist.
        self.assertIn("Keine Telefonnummer eingegeben", result)

    # Test 2: Prüft eine ungültige Nummer
    def test_ungueltige_nummer(self):
        # Funktion mit offensichtlich falscher Nummer aufrufen
        result = suche_nummer("000000000")
        # Prüfen, ob überhaupt ein String zurückgegeben wird
        # assertTrue(c) -> prüft, ob c wahr ist (True)
        self.assertTrue(isinstance(result, str))

    # Test 3: Prüft eine normale Nummer (Format-Test)
    def test_format(self):
        # Funktion mit echter Nummer aufrufen
        result = suche_nummer("053618486467")
        # Prüfen, ob das Ergebnis ein String ist
        self.assertTrue(isinstance(result, str))


# Startet die Tests, wenn die Datei direkt ausgeführt wird
# Ohne diesen Block würden die Tests nicht automatisch laufen
if __name__ == "__main__":
    unittest.main()