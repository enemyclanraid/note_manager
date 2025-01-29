from datetime import datetime
import uuid
from colorama import Fore, Style, init
import note_manager.interface.user_interface as interface
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


def list_notes(notes):
    """Отображает список всех заметок."""
    if not notes:
        print("\nНет доступных заметок.")
    else:
        for i, note in enumerate(notes, 1):
            print(f"\nЗаметка №{i}:")
            interface.display_note_info(note)
            print(calculate_remaining_time(note["issue_date"]))
            print("\n------------------------------")



#======================= вывел часть команд в сокрощённом виде

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

def clear_duplicates(notes):
    notes = cleard_duplicates(notes)
    print("Повторяющиеся заметки удалены.")
    return notes

def show_remaining_time(notes):
    if not notes:
        print("\nНет заметок для проверки времени.")
    else:
        for i, note in enumerate(notes, 1):
            print(f"\nЗаметка №{i}:")
            print(helpers.calculate_remaining_time(note["issue_date"]))

def show_help():
    print(Fore.CYAN + """Доступные команды:
    Основные:
      create : создать новую заметку.
      list   : отобразить информацию обо всех заметках списком.
      table  : отобразить информацию обо всех заметках в виде таблицы.
      delete : удалить существующую заметку.
      retry  : инициировать редактирование существующих заметок.
      status : изменить статус существующих заметок.
      update : обновить существующие заметки.
      search : поиск заметок по ключевым словам.
      save   : сохранение текущих заметок.
      import : импортирование заметок из файла txt.
      cleard : удаление дубликатов заметок.
      append : добавление заметок в уже существующий файл.
      savejs : Сохраняет заметки в формате JSON.
      test   : Тестирование.

    Работа со временем:
      time   : отобразить оставшееся время до истечения срока заметки.

    Помощь и выход:
      help   : отобразить это сообщение.
      exit   : выйти из программы.
    """)



#======================= конец списка сокрощенных команд

def search_command(notes):
    """Поиск по ключевым словам в заметках."""
    keyword = input("Введите ключевое слово для поиска (или оставьте пустым для пропуска): ").strip()
    status_choice = input("Введите статус для поиска (выполнено, в процессе, отложено) или оставьте пустым для пропуска: ").strip()

    status_dict = {
        "выполнено": "\033[92mвыполнено\033[0m",
        "в процессе": "\033[93mв процессе\033[0m",
        "отложено": "\033[31mотложено\033[0m"
    }
    status = status_dict.get(status_choice)
    search_notes(notes, keyword if keyword else None, status)


def update_note_status(notes):
    """Обновляет статус выбранной заметки."""
    if not notes:
        print("\nНет заметок для редактирования статуса.")
        return

    print("\nСписок доступных заметок:")
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note['username']} - {', '.join(note['titles'])} (Текущий статус: {note['status']})")

    while True:
        choice = input("Выберите номер заметки для изменения статуса: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(notes):
            selected_note = notes[int(choice) - 1]
            current_status = selected_note['status']
            print(f"\nТекущий статус заметки: \"{current_status}\"")
            print("\nВыберите новый статус заметки:")
            print("1. \033[92mвыполнено\033[0m")
            print("2. \033[93mв процессе\033[0m")
            print("3. \033[31mотложено\033[0m")
            status_dict = {
                "1": "\033[92mвыполнено\033[0m",
                "2": "\033[93mв процессе\033[0m",
                "3": "\033[31mотложено\033[0m"
            }
            while True:
                new_status_choice = input("Ваш выбор: ").strip()
                if new_status_choice in status_dict:
                    selected_note['status'] = status_dict[new_status_choice]
                    print(f"Статус заметки успешно обновлён на: \"{selected_note['status']}\"")
                    return
                else:
                    print("Некорректный выбор. Пожалуйста, введите число от 1 до 3.")
        else:
            print("Некорректный номер. Попробуйте снова.")


def edit_note(notes):
    """Редактирует существующую заметку."""
    if not notes:
        print("Нет заметок для редактирования.")
        return

    print("\nСписок доступных заметок:")
    for idx, note in enumerate(notes, 1):
        print(f"{idx}. {note['username']} - {note['titles']}")

    while True:
        try:
            note_index = int(input("Введите номер заметки, которую хотите отредактировать: ")) - 1
            if 0 <= note_index < len(notes):
                selected_note = notes[note_index]
                break
            else:
                print("Некорректный номер. Попробуйте снова.")
        except ValueError:
            print("Введите число.")

    print("\nРедактирование выбранной заметки:")

    new_username = input(f"Введите новое имя пользователя (текущая: {selected_note['username']}): ").strip()
    if new_username:
        selected_note['username'] = new_username

    print("\nРедактирование заголовков заметки.")
    new_titles = set(selected_note['titles'])
    while True:
        title_action = input("Введите новый заголовок (или оставьте пустым для завершения): ").strip()
        if not title_action:
            break
        new_titles.add(title_action)
    selected_note['titles'] = list(new_titles)

    new_content = input(f"Введите новое содержание заметки (текущее: {selected_note['content']}): ").strip()
    if new_content:
        selected_note['content'] = new_content

    new_created_date = input_valid_date(
        f"Введите новую дату создания заметки (текущая: {selected_note['created_date']}): "
    )
    selected_note['created_date'] = new_created_date

    new_issue_date = input_valid_date(
        f"Введите новую дату истечения заметки (текущая: {selected_note['issue_date']}): "
    )
    selected_note['issue_date'] = new_issue_date

    print("Заметка успешно обновлена!")
    print(calculate_remaining_time(selected_note["issue_date"]))


def update_note_status(notes):
    """Обновляет статус выбранной заметки."""
    if not notes:
        print("\nНет заметок для редактирования статуса.")
        return

    print("\nСписок доступных заметок:")
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note['username']} - {', '.join(note['titles'])} (Статус: {note['status']})")

    while True:
        choice = input("Выберите номер заметки для изменения статуса: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(notes):
            selected_note = notes[int(choice) - 1]
            current_status = selected_note['status']
            print(f"\nТекущий статус заметки: \"{current_status}\"")
            print("\nВыберите новый статус заметки:")
            print("1. \033[92mвыполнено\033[0m")
            print("2. \033[93mв процессе\033[0m")
            print("3. \033[31mотложено\033[0m")

            status_dict = {
                "1": "\033[92mвыполнено\033[0m",
                "2": "\033[93mв процессе\033[0m",
                "3": "\033[31mотложено\033[0m"
            }

            while True:
                new_status_choice = input("Ваш выбор: ").strip()
                if new_status_choice in status_dict:
                    selected_note['status'] = status_dict[new_status_choice]
                    print(f"Статус заметки успешно обновлён на: \"{selected_note['status']}\"")
                    break
                else:
                    print("Некорректный выбор. Пожалуйста, введите число от 1 до 3.")
            break
        else:
            print("Некорректный номер. Попробуйте снова.")

def table_notes(notes):
    """Отображает список заметок с возможностью сортировки и постраничного вывода."""
    if not notes:
        print("\nНет доступных заметок.")
        return

    sort_choice = input(
        "Хотите отсортировать заметки? (d) по дате создания, (e) по дедлайну, (s) по статусу, (n) без сортировки: ").strip().lower()

    if sort_choice == 'd':
        notes.sort(key=lambda note: note['created_date'])
    elif sort_choice == 'e':
        notes.sort(key=lambda note: note['issue_date'])
    elif sort_choice == 's':
        notes.sort(key=lambda note: note['status'])

    items_per_page = 5
    total_notes = len(notes)
    total_pages = (total_notes + items_per_page - 1) // items_per_page

    current_page = 1

    while True:
        print(f"\nСтраница {current_page}/{total_pages}")
        start_index = (current_page - 1) * items_per_page
        end_index = min(start_index + items_per_page, total_notes)

        print(
            f"{'№':<3} {'Имя пользователя':<15} {'Заголовок':<26} {'Содержание':<38} {'Дата создания':<15} {'Дедлайн':<15} {'Статус':<15}")
        print("-" * 130)

        for i in range(start_index, end_index):
            note = notes[i]
            titles_str = ", ".join(note['titles']) if isinstance(note['titles'], list) else note['titles']
            content_str = note['content'] if 'content' in note else ''
            print(
                f"{i + 1:<3} {note['username']:<15} {titles_str:<26} {content_str:<38} {note['created_date']:<15} {note['issue_date']:<15} {note['status']:<15}")

        print("-" * 130)

        next_action = input(
            "Нажмите 'n' для следующей страницы, 'b' для предыдущей страницы или 'q' для выхода: ").strip().lower()

        if next_action == 'n':
            if current_page < total_pages:
                current_page += 1
            else:
                print("Вы уже на последней странице.")
        elif next_action == 'b':
            if current_page > 1:
                current_page -= 1
            else:
                print("Вы уже на первой странице.")
        elif next_action == 'q':
            break
        else:
            print("Некорректный ввод. Пожалуйста, используйте 'n', 'b' или 'q'.")



def update_note(notes):
    """Обновляет существующую заметку по номеру."""
    if not notes:
        print("\nНет доступных заметок для редактирования.")
        return

    print("\nСписок доступных заметок:")
    for idx, note in enumerate(notes, 1):
        print(f"{idx}. {note['username']} - {note['titles']}")

    while True:
        try:
            note_index = int(input("Введите номер заметки для редактирования: ")) - 1
            if 0 <= note_index < len(notes):
                selected_note = notes[note_index]
                break
            else:
                print("Некорректный номер. Попробуйте снова.")
        except ValueError:
            print("Введите число.")

    fields_to_update = {
        'username': 'Имя пользователя',
        'titles': 'Заголовок',
        'content': 'Содержание',
        'status': 'Статус',
        'created_date': 'Дата создания',
        'issue_date': 'Дата истечения'
    }

    while True:
        print("\nВыберите поле для обновления:")
        for i, (field_key, field_name) in enumerate(fields_to_update.items(), 1):
            print(f"{i}. {field_name}")

        try:
            field_choice = int(input("Введите номер поля для редактирования: ")) - 1

            if 0 <= field_choice < len(fields_to_update):
                field_key = list(fields_to_update.keys())[field_choice]
                field_name = fields_to_update[field_key]
                break
            else:
                print("Некорректный номер. Попробуйте снова.")

        except ValueError:
            print("Введите число.")

    if field_key == 'titles':
        print("\nВыберите действие с заголовками:")
        action_choice = input(
            "Вы хотите (a)добавить заголовок к существующим или (r)перезаписать все заголовки? (a/r): ").strip().lower()

        if action_choice == 'a':
            new_titles = set(selected_note['titles'])
            print("\nРедактирование заголовков заметки.")
            while True:
                title_action = input("Введите новый заголовок (или оставьте пустым для завершения): ").strip()
                if title_action == "":
                    break

                if title_action in new_titles:
                    print("Этот заголовок уже существует. Пожалуйста, введите другой.")
                else:
                    new_titles.add(title_action)

            selected_note['titles'] = list(new_titles)
            print(f"Заголовки успешно обновлены на: {selected_note['titles']}")

        elif action_choice == 'r':
            new_titles = []
            print("\nСоздание нового списка заголовков.")
            while True:
                title_action = input("Введите новый заголовок (или оставьте пустым для завершения): ").strip()
                if title_action == "":
                    break
                new_titles.append(title_action)

            selected_note['titles'] = new_titles
            print(f"Заголовки успешно обновлены на: {selected_note['titles']}")

    elif field_key == 'status':
        status_dict = {
            "1": "\033[92mвыполнено\033[0m",
            "2": "\033[93mв процессе\033[0m",
            "3": "\033[31mотложено\033[0m"
        }

        print("\nВыберите новый статус заметки:")
        for key, value in status_dict.items():
            print(f"{key}. {value}")

        while True:
            new_status_choice = input("Ваш выбор: ").strip()
            if new_status_choice in status_dict:
                selected_note[field_key] = status_dict[new_status_choice]
                print(f"{field_name} успешно обновлено на '{selected_note[field_key]}'.")
                break
            else:
                print("Некорректный выбор. Попробуйте снова.")

    elif field_key in ['created_date', 'issue_date']:
        new_value = helpers.input_valid_date(
            f"Введите новую дату для {field_name} (текущая: {selected_note[field_key]}), или оставьте пустым для отмены: ")

        if new_value == "":
            print(f"Обновление поля '{field_name}' отменено.")
            return

        selected_note[field_key] = new_value
        print(f"{field_name} успешно обновлено на '{new_value}'.")

    else:
        new_value = input(
            f"Введите новое значение для {field_name} (текущая: {selected_note[field_key]}), или оставьте пустым для пропуска: ").strip()

        if new_value == "":
            print(f"Обновление поля '{field_name}' отменено.")
            return

        confirm = input(f"Вы уверены, что хотите обновить поле '{field_name}'? (yes/no): ").strip().lower()

        if confirm == 'yes':
            selected_note[field_key] = new_value
            print(f"{field_name} успешно обновлено на '{new_value}'.")
        else:
            print(f"Обновление поля '{field_name}' отменено.")


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


def search_notes(notes, keyword=None, status=None):
    """Ищет заметки по ключевым словам и/или статусу."""
    if not notes:
        print("Заметки, соответствующие запросу, не найдены.")
        return []

    found_notes = []

    for note in notes:
        if keyword:
            if (keyword.lower() in note["username"].lower() or
                    keyword.lower() in note["content"].lower() or
                    any(keyword.lower() in title.lower() for title in note["titles"])):
                found_notes.append(note)

        if status and note["status"] == status:
            found_notes.append(note)

    if keyword and status:
        found_notes = [note for note in found_notes if note["status"] == status]

    if found_notes:
        print("\nНайденные заметки:")
        for idx, note in enumerate(found_notes, 1):
            interface.display_note_info(note)
            print("------------------------------")
    else:
        print("Заметки, соответствующие запросу, не найдены.")

    return found_notes

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