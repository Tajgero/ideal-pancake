import requests
from bs4 import BeautifulSoup

# URL strony z bazą danych Eurostat
BASE_URL = "https://ec.europa.eu/eurostat/data/database"

def fetch_data(url):
    # Wysyłanie zapytania GET do strony
    response = requests.get(url)
    # Sprawdzenie statusu zapytania
    if response.status_code == 200:
        return response.text
    else:
        print(f"Problem z połączeniem: {response.status_code}")
        return None

def parse_data(html):
    # Tworzenie parsera BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    # Znalezienie wszystkich sekcji z liczbą wartości
    number_of_values = 0
    for section in soup.find_all("td", class_="infoCol"):
        # Oczyszczanie tekstu, usunięcie spacji i konwersja do liczby
        value = section.text.strip().replace(' ', '')
        if value.isdigit():  # Sprawdzenie czy string zawiera liczbę
            number_of_values += int(value)
    return number_of_values

if __name__ == "__main__":
    html_data = fetch_data(BASE_URL)
    if html_data:
        total_values = parse_data(html_data)
        print(f"Łączna ilość wartości z bazy danych: {total_values}")
