import cloudscraper

def sprawdz_sklep(nazwa, url):
    scraper = cloudscraper.create_scraper(
        browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
    )
    try:
        print(f"Testuję połączenie z {nazwa}...")
        response = scraper.get(url, timeout=10)
        print(f"Status odpowiedzi dla {nazwa}: {response.status_code}")
        if response.status_code == 200:
            print(f"-> SUKCES! {nazwa} nas wpuszcza. Możemy go użyć.\n")
        else:
            print(f"-> BLOKADA (Kod {response.status_code})\n")
    except Exception as e:
        print(f"-> BŁĄD połączenia z {nazwa}: {e}\n")

# Wklej tutaj PRAWDZIWE linki do jakichkolwiek produktów z tych sklepów
link_media_expert = "https://www.taniaksiazka.pl/ladne-kwiatki-p-2476482.html?_gl=1*18vx51d*_up*MQ..*_gs*MQ..&gclid=CjwKCAjw857RBhAgEiwAI-1yKLLPk3T_A22KP0OkvmurF4sJsfzzwiKP8aRLefTPNmxTOuHpqF10nBoCjb4QAvD_BwE&gbraid=0AAAAAD9tTHUhA_6Qnpt2xdHG6IMR72n_Q"
link_komputronik = "https://www.komputronik.pl/product/1014231/apple-macbook-air-m5-10-8-13-6-16gb-512gb-mac-os-srebrny-us.html"

sprawdz_sklep("Media Expert", link_media_expert)
sprawdz_sklep("Komputronik", link_komputronik)