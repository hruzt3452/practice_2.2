import json
import requests

API_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
SAVE_FILE = "save.json"

def get_data():
    try:
        return requests.get(API_URL, timeout=10).json()
    except:
        print("Ошибка загрузки данных")
        return {}

def load_groups():
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_groups(groups):
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(groups, f, ensure_ascii=False, indent=2)
    print("Группы сохранены")

def show_all(valutes):
    print(f"\n{'Код':<6} {'Название':<25} {'Курс'}")
    print("-" * 40)
    for code, v in valutes.items():
        print(f"{code:<6} {v['Name']:<25} {v['Value']:.4f}")

def show_by_code(valutes, code):
    code = code.upper()
    if code in valutes:
        v = valutes[code]
        print(f"\n{code} - {v['Name']}: {v['Value']:.4f} RUB")
    else:
        print("Валюта не найдена")

def create_group(groups):
    name = input("Название группы: ").strip()
    if name and name not in groups:
        groups[name] = []
        print(f"Группа '{name}' создана")
    return groups

def show_groups(groups):
    print("\nВаши группы:")
    for name, currencies in groups.items():
        print(f"  {name}: {currencies}")

def manage_group(groups, valutes):
    name = input("Название группы: ").strip()
    if name not in groups:
        print("Группа не найдена")
        return groups
    
    print(f"Текущий состав: {groups[name]}")
    action = input("Добавить (+) или удалить (-) валюту? ").strip()
    code = input("Код валюты: ").strip().upper()
    
    if code not in valutes:
        print("Неверный код валюты")
        return groups
    
    if action == '+' and code not in groups[name]:
        groups[name].append(code)
        print(f"{code} добавлена")
    elif action == '-' and code in groups[name]:
        groups[name].remove(code)
        print(f"{code} удалена")
    return groups

def show_group_rates(groups, valutes, name):
    if name not in groups:
        print("Группа не найдена")
        return
    print(f"\nКурсы для '{name}':")
    for code in groups[name]:
        if code in valutes:
            print(f"{code}: {valutes[code]['Value']:.4f} RUB")

def main():
    data = get_data()
    valutes = data.get('Valute', {})
    groups = load_groups()
    
    while True:
        print("\n| 1-Все валюты")
        print("| 2-По коду")
        print("| 3-Создать группу")
        print("| 4-Мои группы")
        print("| 5-Управление группой")
        print("| 6-Курсы группы")
        print("| 7-Сохранить")
        print("| 0-Выход")
       
        choice = input("Выбор: ").strip()
        
        if choice == '1':
            show_all(valutes)
        elif choice == '2':
            code = input("Код валюты: ").strip()
            show_by_code(valutes, code)
        elif choice == '3':
            groups = create_group(groups)
        elif choice == '4':
            show_groups(groups)
        elif choice == '5':
            groups = manage_group(groups, valutes)
        elif choice == '6':
            name = input("Название группы: ").strip()
            show_group_rates(groups, valutes, name)
        elif choice == '7':
            save_groups(groups)
        elif choice == '0':
            save = input("Сохранить перед выходом? (y/n): ").strip()
            if save == 'y':
                save_groups(groups)
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()