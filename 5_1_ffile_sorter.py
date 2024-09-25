import asyncio
import aiofiles
import logging
from pathlib import Path

# Встановлюємо шляхи до вихідної та цільової папок
source_path = Path('source_folder')
output_path = Path('output_folder')

logging.basicConfig(level=logging.ERROR, filename='file_sorter_errors.log')

# Функція для створення вихідної та цільової папок, якщо вони не існують
def create_folders():
    if not source_path.exists():
        source_path.mkdir(parents=True, exist_ok=True)
        print(f'Вихідна папка "{source_path}" створена.')
    else:
        print(f'Вихідна папка "{source_path}" вже існує.')

    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)
        print(f'Цільова папка "{output_path}" створена.')
    else:
        print(f'Цільова папка "{output_path}" вже існує.')

# Функція для створення тестових файлів у вихідній папці
def create_test_files():
    # Перевіряємо, чи папка порожня
    if any(source_path.iterdir()):
        print(f'Вихідна папка "{source_path}" не порожня. Тестові файли не створені.')
        return
    else:
        # Створюємо кілька тестових файлів з різними розширеннями
        extensions = ['txt', 'jpg', 'pdf', 'docx', 'png', 'unknown']
        for i, ext in enumerate(extensions, 1):
            if ext == 'unknown':
                file_name = source_path / f'test_file_{i}'
            else:
                file_name = source_path / f'test_file_{i}.{ext}'
            file_name.touch()
        print(f'Тестові файли створені у папці "{source_path}".')

async def read_folder(folder):
    try:
        for item in folder.iterdir():
            if item.is_dir():
                await read_folder(item)
            else:
                await copy_file(item)
    except Exception as e:
        logging.error(f'Помилка при читанні папки {folder}: {e}')

async def copy_file(file):
    try:
        ext = file.suffix[1:]  # Отримуємо розширення без крапки
        if not ext:
            ext = 'unknown'
        dest_folder = output_path / ext
        dest_folder.mkdir(parents=True, exist_ok=True)
        dest_file = dest_folder / file.name
        async with aiofiles.open(file, 'rb') as fsrc:
            async with aiofiles.open(dest_file, 'wb') as fdst:
                while True:
                    chunk = await fsrc.read(1024*1024)  # Читаємо по 1МБ
                    if not chunk:
                        break
                    await fdst.write(chunk)
    except Exception as e:
        logging.error(f'Помилка при копіюванні файлу {file}: {e}')

if __name__ == '__main__':
    create_folders()
    create_test_files()
    asyncio.run(read_folder(source_path))
    print('Сортування файлів завершено.')
