# 📈 Price Tracker - Monitor Cen Produktów

Aplikacja desktopowa napisana w języku Python, służąca do automatycznego monitorowania cen wybranych produktów w popularnych sklepach internetowych (np. Komputronik, Tania Książka). Projekt został zrealizowany w ramach laboratorium z kursu **"Języki skryptowe"**.

Rozwiązuje on rzeczywisty problem użytkowników (wymóg biznesowy) – pozwala śledzić zmiany cen w czasie, chroniąc przed "fałszywymi promocjami" i automatycznie powiadamiając o faktycznych obniżkach.

## ✨ Główne funkcjonalności

* **Śledzenie cen:** Pobieranie aktualnych cen z wykorzystaniem bibliotek `BeautifulSoup` oraz `cloudscraper` (omijanie podstawowych zabezpieczeń antybotowych m.in. Cloudflare).
* **Baza danych SQLite:** Lokalna, bezobsługowa baza danych zapisująca pełną historię cen (CRUD: dodawanie, odczyt, usuwanie).
* **Nowoczesne GUI:** Ciemny, responsywny interfejs użytkownika stworzony w `CustomTkinter`. Zapewnia pełną separację od logiki biznesowej (uruchamianie zadań w osobnych wątkach - `threading`).
* **Wizualizacja danych:** Generowanie dynamicznych wykresów historii cen za pomocą `matplotlib`.
* **Powiadomienia systemowe:** Integracja z biblioteką `plyer` w celu wysyłania natywnych powiadomień na pulpit w momencie wykrycia spadku lub wzrostu ceny.
* **Integracja z przeglądarką:** Łatwe wyszukiwanie produktów bezpośrednio z poziomu aplikacji (`webbrowser`).  

## 🖥️ Przewodnik po interfejsie (GUI)

Aplikacja została zaprojektowana z myślą o intuicyjnej obsłudze. Interfejs dzieli się na dwie główne strefy:

### 🎛️ Panel Boczny (Nawigacja i Akcje Główne)
Znajduje się po lewej stronie i służy do globalnego zarządzania aplikacją:
* **Przycisk "Sprawdź teraz ceny":** Ręcznie wymusza połączenie ze sklepami, omija zabezpieczenia antybotowe i aktualizuje ceny dla wszystkich produktów na liście. Działa w osobnym wątku (nie zawiesza aplikacji).
* **Przycisk "+ Dodaj produkt":** Otwiera nowy formularz, pozwalający na wybór obsługiwanego sklepu z listy rozwijanej, wklejenie linku URL oraz nadanie własnej nazwy.
* **Przełącznik "🔄 Autopilot (1h)":** Uruchamia tryb działania w tle. Aplikacja automatycznie odświeża ceny co wyznaczony czas, wysyłając natywne powiadomienie systemowe (Push) na pulpit, gdy tylko wykryje zmianę.

### 📋 Obszar Główny (Lista Produktów)
Znajduje się po prawej stronie i wyświetla bazę danych w formie czytelnych, niezależnych kafelków:
* Przestronny, scrollowany widok prezentujący wszystkie śledzone produkty wraz z ich aktualną ceną i nazwą sklepu.
* **Przycisk "Wykres" (przy każdym produkcie):** Generuje interaktywny wykres (`matplotlib`) przedstawiający wizualną historię zmian ceny w czasie dla konkretnego przedmiotu.
* **Przycisk "🗑️ Usuń" (przy każdym produkcie):** Błyskawicznie i bezpiecznie usuwa dany produkt oraz całą przypisaną do niego historię z lokalnej bazy SQLite.

## 🛠️ Wykorzystane technologie

* **Python 3.x**
* **Interfejs:** `customtkinter`
* **Scraping:** `beautifulsoup4`, `cloudscraper`
* **Baza Danych:** `sqlite3` (wbudowana)
* **Wykresy:** `matplotlib`
* **Powiadomienia:** `plyer`
* **Testy:** `pytest`
* **Pakowanie:** `pyinstaller`

## 📂 Struktura projektu

Projekt został zbudowany z zachowaniem zasad czystej architektury i separacji warstw:

```text
📦 Price-monitor-app
 ┣ 📂 src/
 ┃ ┣ 📂 database/     # Warstwa danych (połączenie z SQLite, operacje CRUD)
 ┃ ┣ 📂 gui/          # Warstwa widoku (interfejs CustomTkinter, okna dialogowe)
 ┃ ┣ 📂 scraper/      # Warstwa logiki pobierania danych (czyszczenie stringów, zapytania)
 ┃ ┃ ┣ 📜 core.py     # Główny silnik parsujący ceny
 ┃ ┃ ┗ 📜 config.py   # Konfiguracja selektorów dla poszczególnych sklepów (Open/Closed Principle)
 ┃ ┗ 📜 monitor.py    # Kontroler - łączy scraper, bazę i powiadomienia
 ┣ 📂 tests/          # Testy jednostkowe (pytest)
 ┣ 📜 main.py         # Punkt wejściowy aplikacji
 ┣ 📜 requirements.txt# Lista zależności projektu
 ┗ 📜 README.md       # Dokumentacja

```
## 🚀 Uruchomienie (Dla deweloperów)
Aby uruchomić projekt ze źródeł, postępuj zgodnie z poniższymi instrukcjami:  

Sklonuj repozytorium:

Bash  
git clone https://github.com/Antim0s/Price-monitor-app  
cd Price-monitor-app  
Utwórz i aktywuj środowisko wirtualne:

Windows:

Bash  
python -m venv venv  
.\venv\Scripts\activate

Linux/macOS:

Bash  
python3 -m venv venv  
source venv/bin/activate  
Zainstaluj wymagane zależności:  

Bash  
pip install -r requirements.txt  
Uruchom aplikację:  

Bash  
python main.py  

## 🧪 Uruchamianie testów jednostkowych
Kluczowe komponenty aplikacji (scraper oraz baza danych) zostały pokryte testami jednostkowymi. Do testowania bazy wykorzystano mechanizm tymczasowych plików na dysku (tmp_path), aby nie ingerować w prawdziwą bazę użytkownika.

Aby uruchomić testy, wpisz w terminalu:

Bash  
pytest  

## 📦 Wdrożenie (Uruchomienie dla użytkownika końcowego)
Aplikacja może zostać skompilowana do jednego, samodzielnego pliku wykonywalnego (.exe) za pomocą narzędzia PyInstaller. Dzięki temu użytkownik nie musi posiadać zainstalowanego środowiska Python.

Komenda generująca paczkę:

Bash  
pyinstaller --noconfirm --onefile --windowed --collect-all customtkinter --collect-all matplotlib main.py  
Gotowy program znajdzie się w wygenerowanym folderze dist/ pod nazwą main.exe. Wystarczy go uruchomić dwukrotnym kliknięciem.

Autor: Bartłomeij Sieradzki