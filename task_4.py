import requests

BASE_URL = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}
TIMEOUT = 10


def _safe_request(url: str, params: dict = None) -> dict | None:
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print("Не найдено")
        elif response.status_code == 403:
            print("Превышен лимит запросов (попробуйте позже или добавьте токен)")
        else:
            print(f"Ошибка API: {response.status_code}")
    except requests.Timeout:
        print("Таймаут соединения")
    except requests.RequestException as e:
        print(f"Ошибка сети: {e}")
    return None


def get_user():
    username = input("Введите имя пользователя GitHub: ").strip()
    if not username:
        return
    
    data = _safe_request(f"{BASE_URL}/users/{username}")
    if not data:
        return

    print("\n" + "=" * 40)
    print("        ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ")
    print("=" * 40)
    print(f"Имя: {data.get('name') or data['login']}")
    print(f"Профиль: {data['html_url']}")
    print(f"Репозиториев: {data['public_repos']}")
    print(f"Публичных гистов: {data['public_gists']}")
    print(f"Подписки (following): {data['following']}")
    print(f"Подписчики (followers): {data['followers']}")
    if data.get('bio'):
        print(f"Био: {data['bio']}")
    if data.get('location'):
        print(f"Локация: {data['location']}")


def get_repos():
    username = input("Введите имя пользователя GitHub: ").strip()
    if not username:
        return
    
    data = _safe_request(f"{BASE_URL}/users/{username}/repos", {"per_page": 50, "sort": "updated"})
    if not data:
        return

    if not data:
        print("У пользователя нет публичных репозиториев")
        return

    print(f"\nРЕПОЗИТОРИИ {username} ({len(data)} найдено, показываем первые 10)")
    print("=" * 50)

    for repo in data[:10]:
        print(f"\n{repo['name']}")
        print(f"Ссылка: {repo['html_url']}")
        print(f"Язык: {repo['language'] or 'Не указан'}")
        print(f"Видимость: {'Приватный' if repo['private'] else 'Публичный'}")
        print(f"Ветка по умолчанию: {repo['default_branch']}")
        print(f"Звёзд: {repo['stargazers_count']} | Форков: {repo['forks_count']}")
        if repo.get('description'):
            desc = repo['description']
            print(f"Описание: {desc[:60]}{'...' if len(desc) > 60 else ''}")
        print("-" * 40)


def search_repos():
    query = input("Введите название для поиска: ").strip()
    if not query:
        return

    data = _safe_request(f"{BASE_URL}/search/repositories", {
        "q": f"in:name {query}",
        "sort": "stars",
        "order": "desc",
        "per_page": 10
    })
    if not data:
        return

    items = data.get('items', [])
    if not items:
        print("Ничего не найдено")
        return

    print(f"\nРЕЗУЛЬТАТЫ ПОИСКА '{query}' (найдено: {data.get('total_count', 0)})")
    print("=" * 50)

    for repo in items:
        print(f"\n{repo['full_name']}")
        print(f"Автор: {repo['owner']['login']}")
        print(f"Ссылка: {repo['html_url']}")
        print(f"Язык: {repo['language'] or 'Не указан'} | Видимость: {'Приватный' if repo['private'] else 'Публичный'}")
        print(f"Звёзд: {repo['stargazers_count']} | Форков: {repo['forks_count']}")
        if repo.get('description'):
            desc = repo['description']
            print(f"Описание: {desc[:60]}{'...' if len(desc) > 60 else ''}")
        print("-" * 40)


def main():
    while True:
        print("\n" + "=" * 35)
        print("        GITHUB API CLIENT")
        print("=" * 35)
        print("1. Профиль пользователя")
        print("2. Репозитории пользователя") 
        print("3. Поиск репозиториев")
        print("4. Выход")
        print("-" * 35)

        choice = input("Выберите действие (1-4): ").strip()

        if choice == "1":
            get_user()
        elif choice == "2":
            get_repos()
        elif choice == "3":
            search_repos()
        elif choice == "4":
            print("Покаа!")
            break
        else:
            print("Неверный выбор, попробуйте снова")
            continue

        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()