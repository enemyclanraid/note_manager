from datetime import datetime
import uuid
from colorama import Fore, Style, init
import note_manager.utils.helpers as helpers
import note_manager.data.file_operations as file_ops


def create_notes(notes):
    """Создает новые заметки и добавляет их в список."""
    print("\nСоздание новой заметки...")
    while True:
        note = create_note()
        notes.append(note)
        print(Fore.GREEN + "Заметка успешно создана.")
        print(calculate_remaining_time(note["issue_date"]))

        while True:
            add_more = input(Fore.BLUE + "Хотите добавить ещё одну заметку? (yes/no): ").lower()
            if add_more in ['yes', 'no']:
                break
            print(Fore.RED + "Пожалуйста, введите 'yes' или 'no'.")

        if add_more == 'no':
            break

    print(Fore.GREEN + "Создание заметок завершено.")
    return notes

#====== вспомогательные функции вызова команд

def save_notes_json(notes):
    filename = input("Введите имя файла для сохранения заметок: ")
    file_ops.save_notes_json(notes, filename)

def save_notes(notes):
    filename = input("Введите имя файла для сохранения заметок: ")
    file_ops.save_notes_to_file(notes, filename)

def append_notes(notes):
    filename = input("Введите имя файла для сохранения заметок: ")
    file_ops.append_notes_to_file(notes, filename)

def import_notes(notes):
    filename = input("Введите имя файла для загрузки заметок: ")
    loaded_notes = file_ops.open_notes_from_file(filename)
    if loaded_notes:
        notes.extend(loaded_notes)
        print(f"Загружено {len(loaded_notes)} заметок.")
    return notes

#====== вспомогательные функции вызова команд

def clear_duplicates(notes):
    notes = cleard_duplicates(notes)
    print("Повторяющиеся заметки удалены.")
    return notes

def create_note():
    """Создаёт новую заметку."""
    username = input("Введите имя пользователя: ")
    titles = set()

    while True:
        title = input("Введите заголовок (или оставьте пустым для завершения): ")
        if title == "":
            break
        if title in titles:
            print("Этот заголовок уже существует. Пожалуйста, введите другой.")
        else:
            titles.add(title)

    content = input("Введите описание заметки: ")
    print("\nВыберите статус заметки:")
    status_dict = {
        "1": "\033[92mвыполнено\033[0m",
        "2": "\033[93mв процессе\033[0m",
        "3": "\033[31mотложено\033[0m"
    }

    for key, value in status_dict.items():
        print(f"{key}. {value}")

    while True:
        choice = input("Ваш выбор: ")
        if choice in status_dict:
            status = status_dict[choice]
            break
        else:
            print("Некорректный выбор. Пожалуйста, выберите один из предложенных вариантов.")

    created_date = helpers.input_valid_date(
        "Введите дату создания заметки (дд-мм-гггг или дд/мм/гггг) или оставьте поле пустым, если нужно вставить текущую дату: ")

    issue_date = helpers.input_valid_date("Введите дату истечения заметки (дд-мм-гггг или дд/мм/гггг): ")

    return {
        "uid": helpers.generate_uid(),
        "username": username,
        "content": content,
        "status": status,
        "created_date": created_date,
        "issue_date": issue_date,
        "titles": list(titles)
    }


def delete_note(notes):
    """Функция удаления заметок"""
    if not notes:
        print("\nНет доступных заметок для удаления.")
        return

    print("\nВы можете удалить заметку по имени пользователя, заголовку или номеру.")
    criteria = input("Введите имя пользователя, заголовок или номер заметки для удаления: ").strip().lower()
    found = False

    if criteria.isdigit():
        index = int(criteria) - 1
        if 0 <= index < len(notes):
            confirm = input(
                f"Вы уверены, что хотите удалить заметку '{sorted(notes[index]['titles'])}'? (yes/no): ").strip().lower()
            if confirm == 'yes':
                deleted_note = notes.pop(index)
                print(f"Заметка '{deleted_note['titles']}' успешно удалена.")
                found = True
            else:
                print("Удаление отменено.")
        else:
            print("Некорректный номер заметки.")

    else:
        for i in range(len(notes) - 1, -1, -1):
            if notes[i]["username"].lower() == criteria or criteria in (title.lower() for title in notes[i]["titles"]):
                confirm = input(
                    f"Вы уверены, что хотите удалить заметку '{sorted(notes[i]['titles'])}'? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    deleted_note = notes.pop(i)
                    print(f"Заметка '{deleted_note['titles']}' успешно удалена.")
                    found = True
                else:
                    print("Удаление отменено.")

    if not found:
        print("Заметка не найдена.")

def calculate_remaining_time(issue_date):
    """Вычисляет и возвращает оставшееся время до истечения срока."""
    current_date = datetime.now()

    try:
        if '-' in issue_date:
            issue_datetime = datetime.strptime(issue_date, "%d-%m-%Y")
        elif '/' in issue_date:
            issue_datetime = datetime.strptime(issue_date, "%d/%m/%Y")
        else:
            raise ValueError("Некорректный формат даты.")
    except ValueError as e:
        return f"Ошибка: Некорректный формат даты. {e}"

    RED = "\033[31m"
    GREEN = "\033[92m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"

    if current_date.date() == issue_datetime.date():
        return YELLOW + "Дедлайн сегодня!" + RESET
    elif current_date > issue_datetime:
        expired_duration = current_date - issue_datetime
        return RED + f"Внимание! Дедлайн истёк: {helpers.format_duration(expired_duration)} назад." + RESET
    else:
        remaining_duration = issue_datetime - current_date
        return GREEN + f"Оставшееся время до истечения срока: {helpers.format_duration(remaining_duration)}." + RESET


def generate_uid():
    """Генерирует уникальный идентификатор (UID)."""
    return str(uuid.uuid4())

def format_duration(duration):
    """Форматирует длительность в годах:месяцах:неделях:днях:часах:минутах:секундах."""
    days, seconds = duration.days, duration.seconds
    years = days // 365
    days %= 365
    months = days // 30
    days %= 30
    weeks = days // 7
    days %= 7
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{years} лет, {months} месяцев, {weeks} недель, {days} дней, {hours} часов, {minutes} минут, {seconds} секунд"

def input_valid_date(prompt):
    """Запрашивает ввод даты у пользователя и проверяет ее корректность."""
    while True:
        date_str = input(prompt).strip()
        if date_str == "":
            return datetime.now().strftime("%d-%m-%Y")
        try:
            if '-' in date_str:
                date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            elif '/' in date_str:
                date_obj = datetime.strptime(date_str, "%d/%m/%Y")
            else:
                raise ValueError("Некорректный формат даты.")

            return date_str
        except ValueError as e:
            print("Некорректный формат даты или несуществующая дата. Попробуйте снова (формат: дд-мм-гггг или дд/мм/гггг).")

def cleard_duplicates(notes):
    """Удаляет повторяющиеся заметки из списка."""
    unique_notes = []
    seen = set()
    duplicates_removed = 0

    for note in notes:
        note_key = (note['username'], tuple(sorted(note['titles'])), note['content'])

        if note_key not in seen:
            seen.add(note_key)
            unique_notes.append(note)
        else:
            duplicates_removed += 1

    notes[:] = unique_notes

    print(f"Удалено {duplicates_removed} повторяющихся заметок.")
    return notes