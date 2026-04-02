"""
Напишите программу, которая мониторит курс валют по данному
URL(https://www.cbr-xml-daily.ru/daily_json.js).
Предусмотрите следующий функционал приложения:
1) Приложение должно давать возможность просматривать текущий
курс всех валют.
2) Приложение должно давать возможность посмотреть отдельно
валюту по ее коду.
3) Приложение должно давать возможность создавать группы валют,
куда можно будет добавить валюты для отслеживания.
4) Приложение должно давать возможность посмотреть все
созданные пользователем группы валют.
5) Приложение должно давать возможность изменять список
отслеживаемых валют(удалить выбранную валюту, добавить валюту по коду).
6) Сохранять группы с валютами в файле save.json
7) Считывать созданные группы с валютой из файла save.json
"""

import requests
import json
import os

URL = "https://www.cbr-xml-daily.ru/daily_json.js"
FILE_NAME = "save.json"


def get_currencies():
    try:
        response = requests.get(URL)
        data = response.json()
        return data["Valute"]
    except:
        print("Ошибка загрузки данных")
        return None


def show_all(currencies):
    if not currencies:
        return

    print("\nКУРСЫ ВАЛЮТ:")
    print("-" * 50)
    for code in currencies:
        name = currencies[code]["Name"]
        value = currencies[code]["Value"]
        nominal = currencies[code]["Nominal"]
        print(f"{code}: {nominal} {name} = {value} руб.")
    print("-" * 50)


def find_currency(currencies, code):
    code = code.upper()
    if code in currencies:
        c = currencies[code]
        print(f"\n{code}: {c['Nominal']} {c['Name']} = {c['Value']} руб.")
    else:
        print("Валюта не найдена")


def load_groups():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_groups(groups):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(groups, f, ensure_ascii=False, indent=2)


def create_group(groups):
    name = input("Введите название группы: ")
    if name not in groups:
        groups[name] = []
        print(f"Группа '{name}' создана")
    else:
        print("Такая группа уже есть")


def show_groups(groups, currencies):
    if not groups:
        print("Нет созданных групп")
        return

    print("\nГРУППЫ ВАЛЮТ:")
    for group in groups:
        print(f"\n{group}:")
        if not groups[group]:
            print("  (пусто)")
        for code in groups[group]:
            if code in currencies:
                value = currencies[code]["Value"]
                print(f"  {code}: {value} руб.")
            else:
                print(f"  {code}: (нет данных)")


def add_to_group(groups, currencies):
    show_groups(groups, currencies)

    group = input("Введите название группы: ")
    if group not in groups:
        print("Группа не найдена")
        return

    code = input("Введите код валюты: ").upper()
    if code in currencies:
        if code not in groups[group]:
            groups[group].append(code)
            print(f"{code} добавлен в группу {group}")
        else:
            print("Такая валюта уже есть в группе")
    else:
        print("Валюта не найдена")


def remove_from_group(groups):
    show_groups(groups, {})

    group = input("Введите название группы: ")
    if group not in groups:
        print("Группа не найдена")
        return

    code = input("Введите код валюты: ").upper()
    if code in groups[group]:
        groups[group].remove(code)
        print(f"{code} удален из группы {group}")
    else:
        print("Валюты нет в группе")


def main():
    currencies = get_currencies()
    if not currencies:
        return

    groups = load_groups()

    while True:
        print("\n" + "=" * 30)
        print(" " * 7, "МОНИТОР ВАЛЮТ")
        print("=" * 30)
        print("1. Показать все валюты")
        print("2. Найти валюту по коду")
        print("3. Создать группу")
        print("4. Показать все группы")
        print("5. Добавить валюту в группу")
        print("6. Удалить валюту из группы")
        print("7. Выход")
        print("-" * 30)

        choice = input("Выберите действие: ")

        if choice == "1":
            show_all(currencies)
        elif choice == "2":
            code = input("Введите код валюты (например USD): ")
            find_currency(currencies, code)
        elif choice == "3":
            create_group(groups)
            save_groups(groups)
        elif choice == "4":
            show_groups(groups, currencies)
        elif choice == "5":
            add_to_group(groups, currencies)
            save_groups(groups)
        elif choice == "6":
            remove_from_group(groups)
            save_groups(groups)
        elif choice == "7":
            print("До свидания!")
            break
        else:
            print("Неверный выбор")

        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()