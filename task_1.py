import requests
from requests.exceptions import RequestException
import time

sites = [
    "https://github.com/",
    "https://www.binance.com/en", 
    "https://tomtit.tomsk.ru/",
    "https://jsonplaceholder.typicode.com/",
    "https://moodle.tomtit-tomsk.ru/"
]

print("Результаты проверки сайтов:")
print("=" * 70)

for site in sites:
    try:
        response = requests.get(site, timeout=10)
        code = response.status_code

        if 200 <= code < 400:
            status = "доступен"
        elif code in (401, 403):
            status = "вход запрещен"
        elif code == 404:
            status = "не найден"
        else:
            status = "не доступен"

    except RequestException:
        status = "не доступен"
        code = "?"

    print(f"{site:<45} – {status:<15} – {code}")

print("=" * 70)