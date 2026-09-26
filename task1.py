import os
import shutil
from concurrent.futures import ThreadPoolExecutor
import argparse
import time
from functools import wraps

def perftimer(fnc):
    @wraps(fnc)
    def wrapper(*args,**kwargs):
        t0 = time.perf_counter()
        res=fnc(*args, **kwargs)
        t1 = time.perf_counter()
        print(f"Done by {t1-t0:.4f} seconds")
        return res
    return wrapper

def get_extension(file_path: str) -> str:
    # Визначає розширення файлу та очищає його від крапки перед використанням як назви папки.
   
    _, ext = os.path.splitext(file_path)
    return ext[1:].lower() if ext else "no_extension"


def copy_file_worker(source_path: str, target_root: str):
    
    # Воркер функція, яка виконує копіювання одного файлу в його відповідний підкаталог.
    
    try:
        extension = get_extension(source_path)
        target_dir = os.path.join(target_root, extension)
        os.makedirs(target_dir, exist_ok=True)
        destination_path = os.path.join(target_dir, os.path.basename(source_path))
        shutil.copy2(source_path, destination_path)
        return f"Успішно скопійовано: {os.path.basename(source_path)} -> {extension}/"
    except FileNotFoundError:
        return f"Помилка (файл не знайдено): {source_path}"
    except PermissionError:
        return f"Помилка (доступ заборонено) для файлу: {source_path}"
    except Exception as e:
        return f"Невідома помилка при обробці {source_path}: {e}"


def process_directory(source_dir: str, target_root: str, max_workers: int = 10):
    """
    Головна функція для рекурсивного сканування та паралельного копіювання файлів.
    """
    print("-" * 50)
    print(f"Початок обробки директорії.")
    print(f"Вихідна папка: {os.path.abspath(source_dir)}")
    print(f"Папка призначення: {os.path.abspath(target_root)}")
    print("-" * 50)

    # Перевірка існуючих директорій
    if not os.path.isdir(source_dir):
        print(f"\n Вихідна директорія не існує чи не є каталогом: {source_dir}")
        return

    if os.path.exists(target_root):
        print(f"Обережно: Цільова директорія '{target_root}' вже існує.")

    # Збір усіх файлів для обробки
    files_to_process = []
    print("Сканування директорії та збір шляхів...")
    for root, _, files in os.walk(source_dir):
        for file in files:
            full_path = os.path.join(root, file)
            files_to_process.append(full_path)

    if not files_to_process:
        print(f"He знайдено файлів для копіювання.")
        return
    
    total_files = len(files_to_process)
    print(f"Знайдено всього {total_files} файлів. Починається паралельне копіювання...")

    # Паралельна обробка за допомогою ThreadPoolExecutor
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Створення завдань
        features = [executor.submit(copy_file_worker, file_path, target_root) for file_path in files_to_process]

        for feature in features:
            results.append(feature.result())


    print("\n" + "=" * 60)
    print("ОБРОБКА ЗАВЕРШЕНА!")
    print("Успішно!")
    print("=" * 60)

@perftimer
def main():
   
    parser = argparse.ArgumentParser(
        description="Копіює всі файли з джерельної директорії (i піддиректорій) до цільової, сортуючи їх за розширенням y окремі папки.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "source_dir", 
        help="Шлях до директорії з файлами для обробки (Хлам)."
    )
    parser.add_argument(
        "--target", 
        default="dist", 
        help="Цільова директорія, де будуть розміщені відсортовані файли. За замовчуванням: 'dist'."
    )
    # Параметр для кількості потоків
    parser.add_argument(
        "--workers", 
        type=int, 
        default=10, 
        help="Максимальна кількість потоків (воркерів) для обробки файлів."
    )

    args = parser.parse_args()

    process_directory(args.source_dir, args.target, args.workers)


if __name__ == "__main__":
    main()

