import locale
from datetime import datetime


months = {
    "01": "января",
    "02": "февраля",
    "03": "марта",
    "04": "апреля",
    "05": "мая",
    "06": "июня",
    "07": "июля",
    "08": "августа",
    "09": "сентября",
    "10": "октября",
    "11": "ноября",
    "12": "декабря",
}


locale.setlocale(locale.LC_TIME, 'ru_RU')

now = datetime.now()

formatted_date = now.strftime("%d-%m-%Y")

GREEN = "\033[92m"
RESET = "\033[0m"

print(GREEN + "Текущая дата: " + formatted_date + RESET)


def display_note_info(note):
    """Функция для отображения информации о заметке."""
    print("\nИмя пользователя:", note["username"])
    print("Содержание заметки:", note["content"])
    print("Статус заметки:", note["status"])
    print("Дата создания заметки:", note["created_date"])
    print("Дата истечения заметки:", note["issue_date"])
    print("Заголовки заметок:", sorted(note["titles"]))

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
            print(
                "Некорректный формат даты или несуществующая дата. Попробуйте снова (формат: дд-мм-гггг или дд/мм/гггг).")


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
        return RED + f"Внимание! Дедлайн истёк: {format_duration(expired_duration)} назад." + RESET
    else:
        remaining_duration = issue_datetime - current_date
        return GREEN + f"Оставшееся время до истечения срока: {format_duration(remaining_duration)}." + RESET


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
            confirm = input(f"Вы уверены, что хотите удалить заметку '{sorted(notes[index]['titles'])}'? (yes/no): ").strip().lower()
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

    created_date = input_valid_date(
        "Введите дату создания заметки (дд-мм-гггг или дд/мм/гггг) или оставьте поле пустым, если нужно вставить текущую дату: ")

    issue_date = input_valid_date("Введите дату истечения заметки (дд-мм-гггг или дд/мм/гггг): ")

    return {
        "username": username,
        "content": content,
        "status": status,
        "created_date": created_date,
        "issue_date": issue_date,
        "titles": list(titles)
    }


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

    # Обновление полей заметки с подтверждением действий.
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
        # Обработка изменения заголовка
        print("\nВыберите действие с заголовками:")
        action_choice = input("Вы хотите (a)добавить заголовок к существующим или (r)перезаписать все заголовки? (a/r): ").strip().lower()

        if action_choice == 'a':
            new_titles = set(selected_note['titles'])  # Существующие заголовки
            print("\nРедактирование заголовков заметки.")
            while True:
                title_action = input("Введите новый заголовок (или оставьте пустым для завершения): ").strip()
                if title_action == "":
                    break
                # Проверка на дублирование заголовков
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
        # Обработка изменения статуса
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
        # Обработка изменения даты
        new_value = input_valid_date(
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

def main():
    notes = []
    start_time = datetime.now()
    print("\nДобро пожаловать в систему заметок. Вход в ждущий режим выполнения команд.")

    while True:
        command = input("\nВведите команду create, для создания новой заметки (или 'help' для справки): ").strip().lower()

        if command == 'create':
            print("\nСоздание новой заметки...")
            while True:
                note = create_note()
                notes.append(note)
                print("Заметка успешно создана.")
                print(calculate_remaining_time(note["issue_date"]))

                while True:
                    add_more = input("Хотите добавить ещё одну заметку? (yes/no): ").lower()
                    if add_more in ['yes', 'no']:
                        break
                    print("Пожалуйста, введите 'yes' или 'no'.")

                if add_more == 'no':
                    break

            print("Создание заметок завершено.")

        elif command == 'update':
            update_note(notes)


        elif command == 'status':
            if not notes:
                print("\nНет заметок для редактирования статуса.")
            else:
                print("\nСписок доступных заметок:")
                for i, note in enumerate(notes, 1):
                    status_color = note['status']
                    print(f"{i}. {note['username']} - {note['titles']} - {status_color}")
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

        elif command == 'list':
            if not notes:
                print("\nНет доступных заметок.")
            else:
                for i, note in enumerate(notes, 1):
                    print(f"\nЗаметка {i}:")
                    display_note_info(note)
                    print(calculate_remaining_time(note["issue_date"]))

        elif command == 'delete':
            delete_note(notes)

        elif command == 'retry':
            if not notes:
                print("Нет заметок для редактирования.")
                continue


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
            print(calculate_remaining_time(note["issue_date"]))

        elif command == 'status':
            if not notes:
                print("\nНет заметок для редактирования статуса.")
            else:
                print("\nСписок доступных заметок:")
                for i, note in enumerate(notes, 1):
                    status_color = note['status']
                    print(note)

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

        elif command == 'time':
            if not notes:
                print("\nНет заметок для проверки времени.")
            else:
                for i, note in enumerate(notes, 1):
                    print(f"\nЗаметка {i}:")
                    print(calculate_remaining_time(note["issue_date"]))

        elif command == 'help':
            print("""Доступные команды:

Основные:
  create : создать новую заметку.
  list   : отобразить информацию обо всех заметках.
  delete : удалить существующую заметку.
  retry  : инициировать редактирование существующих заметок.
  status : изменить статус существующих заметок.
  update : обновить существующие заметки.

Работа со временем:
  time   : отобразить оставшееся время до истечения срока заметки.

Помощь и выход:
  help   : отобразить это сообщение.
  exit   : выйти из программы.
""")

        elif command == 'exit':
            end_time = datetime.now()
            duration = end_time - start_time
            print(f"Программа завершена. Время работы: {format_duration(duration)}")
            break

        else:
            print("Неизвестная команда. Введите 'help' для получения списка доступных команд.")

if __name__ == "__main__":
    main()

