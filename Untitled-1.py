"""
Разработайте приложение, которое будет работать с GitHub
API(https://docs.github.com/en/rest?apiVersion=2022-11-28) для получения
следующей информации:
1) Просмотр профиля пользователя(имя, ссылка на профиль,
количество репозиториев, количество обсуждений, количество подписок,
количество подписчиков).
2) Получение всех репозиториев выбранного пользователя(название,
ссылка на репозиторий, количество просмотров, используемый язык,
видимость, ветка по умолчанию).
3) Поиск репозиториев по названию.
"""

import requests


def get_user():
    username = input("Введите имя пользователя GitHub: ")

    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        user = response.json()
        print("\n" + "=" * 40)
        print("ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ")
        print("=" * 40)
        print(f"Имя: {user.get('name', 'Не указано')}")
        print(f"Профиль: {user.get('html_url', 'Нет')}")
        print(f"Репозиториев: {user.get('public_repos', 0)}")
        print(f"Подписчиков: {user.get('followers', 0)}")
        print(f"Подписок: {user.get('following', 0)}")
        print(f"Обсуждений: {user.get('public_gists', 0)}")
    else:
        print("Пользователь не найден или ошибка API")


def get_repos():
    username = input("Введите имя пользователя GitHub: ")

    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code == 200:
        repos = response.json()

        if not repos:
            print("У пользователя нет репозиториев")
            return

        print("\n" + "=" * 40)
        print(f"РЕПОЗИТОРИИ {username}")
        print("=" * 40)

        for repo in repos:
            print(f"\nНазвание: {repo['name']}")
            print(f"Ссылка: {repo['html_url']}")
            print(f"Язык: {repo.get('language', 'Не указан')}")
            print(f"Видимость: {'Приватный' if repo['private'] else 'Публичный'}")
            print(f"Ветка: {repo['default_branch']}")
            print(f"Просмотров: {repo.get('watchers_count', 0)}")
            print("-" * 30)
    else:
        print("Пользователь не найден или ошибка API")


def search_repos():
    query = input("Введите название для поиска: ")

    url = f"https://api.github.com/search/repositories?q={query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        repos = data.get('items', [])

        print(f"\nНайдено репозиториев: {data.get('total_count', 0)}")
        print("=" * 40)

        for repo in repos[:5]:  # Показываем первые 5 результатов
            print(f"\nНазвание: {repo['name']}")
            print(f"Автор: {repo['owner']['login']}")
            print(f"Ссылка: {repo['html_url']}")
            print(f"Описание: {repo.get('description', 'Нет описания')}")
            print(f"Язык: {repo.get('language', 'Не указан')}")
            print(f"Звёзд: {repo.get('stargazers_count', 0)}")
            print("-" * 30)
    else:
        print("Ошибка при поиске")


def main():
    while True:
        print("\n" + "=" * 30)
        print("GITHUB API")
        print("=" * 30)
        print("1. Информация о пользователе")
        print("2. Репозитории пользователя")
        print("3. Поиск репозиториев")
        print("4. Выход")
        print("-" * 30)

        choice = input("Выберите действие: ")

        if choice == "1":
            get_user()
        elif choice == "2":
            get_repos()
        elif choice == "3":
            search_repos()
        elif choice == "4":
            print("До свидания!")
            break
        else:
            print("Неверный выбор")

        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()