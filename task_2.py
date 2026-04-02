import psutil
import os
import time

try:
    from colorama import init, Fore, Style
    init()
    USE_COLORS = True
except ImportError:
    USE_COLORS = False


def colorize(text, color_code):
    """Добавляет цвет к тексту, если цвет поддерживается."""
    if USE_COLORS:
        return f"{color_code}{text}{Style.RESET_ALL}"
    return text


def get_status_color(percent):
    """Возвращает цвет в зависимости от нагрузки."""
    if percent < 50:
        return Fore.GREEN
    elif percent < 80:
        return Fore.YELLOW
    else:
        return Fore.RED


def show_cpu():
    """Показывает загрузку процессора с цветом."""
    cpu = psutil.cpu_percent(interval=1)
    color = get_status_color(cpu)
    print(f"Загрузка CPU: {colorize(f'{cpu}%', color)}")


def show_ram():
    """Показывает использование оперативной памяти с цветом."""
    memory = psutil.virtual_memory()
    used_gb = memory.used / (1024 ** 3)
    total_gb = memory.total / (1024 ** 3)
    percent = memory.percent
    color = get_status_color(percent)
    
    print(f"Использовано RAM: {colorize(f'{used_gb:.2f} ГБ / {total_gb:.2f} ГБ ({percent}%)', color)}")


def show_disk():
    """Показывает загруженность системного диска с цветом."""
    path = "C:\\" if os.name == "nt" else "/"
    disk = psutil.disk_usage(path)
    percent = disk.percent
    color = get_status_color(percent)
    
    print(f"Загруженность диска: {colorize(f'{percent}%', color)}")


def clear_screen():
    """Очищает экран кроссплатформенно."""
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    """Выводит заголовок программы."""
    clear_screen()
    print(" " * 8, "🖥️ СИСТЕМНЫЙ МОНИТОР")
    print("=" * 40)
    print("Для выхода нажмите: Ctrl+C")
    print("-" * 40)


def main():
    """Главная функция с циклом обновления."""
    print_header()
    
    try:
        while True:
            # Показываем данные
            show_cpu()
            show_ram()
            show_disk()
            
            # Время обновления
            print("-" * 40)
            print(f"Обновлено: {time.strftime('%H:%M:%S')}")
            print("Обновление через 2 сек... (Ctrl+C для выхода)")
            
            # Пауза перед следующим циклом
            time.sleep(2)
            
            # Очищаем экран для следующего обновления
            print_header()
            
    except KeyboardInterrupt:
        print("\n" + "=" * 40)
        print(colorize("✅ Мониторинг завершён", Fore.GREEN))
        print("=" * 40)


if __name__ == "__main__":
    main()