import psutil

def show_cpu():
    cpu = psutil.cpu_percent(interval=1)
    print(f"Загрузка CPU: {cpu}%")

def show_ram():
    memory = psutil.virtual_memory()
    print(f"Использовано RAM: {memory.percent}%")

def show_disk():
    disk = psutil.disk_usage('/') 
    print(f"Загруженность диска: {disk.percent}%")

def main():
    print(" " * 5, "СИСТЕМНЫЙ МОНИТОР")
    print("=" * 30)
    
    show_cpu()
    show_ram()
    show_disk()
    print("=" * 30)

if __name__ == "__main__":
    main()
