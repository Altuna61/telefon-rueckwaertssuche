# certifi sorgt dafür, dass HTTPS-Verbindungen verifiziert werden,
# auch wenn Mac keine Systemzertifikate richtig hat
import certifi

# Macht die grafische Oberfläche (Fenster, Buttons, Textfelder)
import tkinter as tk

# Macht HTTP-Anfragen (um Webseiten zu laden)
import requests

# Parst HTML, also liest die Webseite aus, damit wir Name & Adresse rausziehen können
from bs4 import BeautifulSoup

# Für das Durchsuchen des JavaScript-Blocks nach handlerData
import re

# ------------------ Funktion zur echten Rückwärtssuche ------------------
# mit Standardparameter
def suche_nummer(telefonnummer, requester=requests.get):
    try:
        # Wenn keine Nummer eingegeben wurde
        if not telefonnummer:
            return "Keine Telefonnummer eingegeben."

        # URL der Webseite
        url = "https://www.dasoertliche.de/"
        
        # Parameter, die in die URL eingefügt werden (Telefonnummer)
        params = {
            "form_name": "search_inv",  # Form Name auf der Webseite
            "ph": telefonnummer         # Telefonnummer, die gesucht wird
        }

        # Webseite laden mit Requests
        response = requester(
            url,
            params=params,         # Parameter übergeben
            timeout=10,            # Abbruch nach 10 Sekunden, falls die Seite nicht reagiert
            verify=False           # SSL-Zertifikat nicht prüfen (wegen Mac-Fehler)
        )

        # Prüfen, ob die Seite geladen werden konnte
        if response.status_code != 200:
            return "Webseite nicht erreichbar."

        # HTML-Seite wird lesbar gemacht → Elemente suchbar
        soup = BeautifulSoup(response.text, "html.parser")

        # JavaScript-Block handlerData als Text auslesen
        text = str(soup)
        result = []

        # Jede Zeile durchsuchen, um handlerData zu finden
        for line in text.splitlines():
            if "var handlerData " in line:
                # Alle Strings (zwischen Anführungszeichen) extrahieren
                result = re.findall(r'"(.*?)"', line)

        # Wenn etwas gefunden wurde, Name und Adresse extrahieren
        if result:
            try:
                name = result[14]          # Name
                strasse = result[9]        # Straße
                hausnummer = result[10]    # Hausnummer
                stadt = result[4]          # Stadt
                plz = result[8]            # Postleitzahl

                # Unicode-Sequenzen wie \u0026 in & umwandeln
                name = name.encode('utf-8').decode('unicode_escape')
                strasse = strasse.encode('utf-8').decode('unicode_escape')
                stadt = stadt.encode('utf-8').decode('unicode_escape')

                # Gibt Name + Adresse als Text zurück
                return f"{name}\n{strasse} {hausnummer}\n{plz} {stadt}"
            except IndexError:
                # Falls die Struktur sich geändert hat und etwas fehlt
                return "Eintrag gefunden, aber Struktur unerwartet."

        # Falls handlerData nicht gefunden wurde
        return "Kein Eintrag gefunden."

    except Exception as e:
        # Falls ein Fehler passiert (z. B. Internetproblem)
        return f"Fehler bei der Suche: {e}"

# ------------------ GUI ------------------
def suchen():
    # Holt die Nummer aus dem Eingabefeld
    nummer = eingabe.get().replace(" ", "")  # Leerzeichen entfernen
    # Führt die Rückwärtssuche aus
    ergebnis = suche_nummer(nummer)
    # Löscht alte Ergebnisse im Textfeld
    ausgabe.delete("1.0", tk.END)
    # Zeigt das neue Ergebnis an
    ausgabe.insert(tk.END, ergebnis)

# ------------------ Hauptfenster erstellen ------------------
fenster = tk.Tk()                # Erstellt das Hauptfenster
fenster.title("Telefon Rückwärtssuche")  # Fenstertitel

# Label (Text) über dem Eingabefeld
tk.Label(fenster, text="Telefonnummer eingeben:").pack(pady=5)

# Eingabefeld für Telefonnummer
eingabe = tk.Entry(fenster)
eingabe.pack(fill="x", padx=10)  # fill="x" → horizontal ausfüllen, padx → Abstand links/rechts

# Button, der bei Klick die Funktion suchen() ausführt
tk.Button(fenster, text="Suchen", command=suchen).pack(pady=10)

# Textfeld für die Ergebnisse (mehrzeilig)
ausgabe = tk.Text(fenster, height=8)
ausgabe.pack(fill="both", padx=10, pady=5)  # fill="both" → horizontal + vertikal ausfüllen

# Hält das Fenster offen (ohne mainloop() würde es sofort schließen)
# damit GUI nicht automatisch startet, wenn wir die Datei importieren
if __name__ == "__main__":
    fenster.mainloop()

# ------------------ Git Hinweise ------------------
# Git Repo erstellen:
# git init                                -> initialisiere Git-Repository
# git add .                               -> fügt alle Dateien zum Commit hinzu
# git commit -m "Initial commit – Rückwärtssuche GUI" -> erster Commit
# Auf Github:
# 	1. https://github.com/new
# 	2. Name: telefon-rueckwaertssuche
# 	3. Public auswählen
# 	4. „Create repository“
# git remote add origin https://github.com/DeinBenutzername/telefon-rueckwaertssuche.git
# git branch -M main
# git push -u origin main
# Änderungen hochladen:
# git add .
# git commit -m "Beschreibung der Änderung"
# git push

# Hinweis:
# immer Ctrl+C im Terminal drücken und Programm neu starten, wenn GUI hängt

# Best Practices for Writing Commit Messages
# Limit the subject line to 50 characters.
# Capitalize only the first letter of the subject.
# Do not end the subject line with a period.
# Insert a blank line between the subject and body.
# Wrap the body at 72 characters.
# Use the imperative mood (e.g., "Add feature" instead of "Added feature").
# Describe what was done and why, but not how.
 

# source venv/bin/activate
# python telefonnrabfrage.py