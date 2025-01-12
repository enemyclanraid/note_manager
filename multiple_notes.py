import locale
from datetime import datetime

# Словарь для преобразования числового представления месяца в текстовое
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

# Устанавливаем локаль на русский язык
locale.setlocale(locale.LC_TIME, 'ru_RU')

# Получаем текущую дату и время
now = datetime.now()

# Форматируем вывод
formatted_date = now.strftime("%d-%m-%Y")
# ANSI escape code для зеленого цвета
GREEN = "\033[92m"
RESET = "\033[0m"  # Сброс цвета
# Выводим результат в консоль
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
        date_str = input(prompt)
        try:
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            return date_str
        except ValueError:
            print("Некорректный формат даты или несуществующая дата. Попробуйте снова (формат: дд-мм-гггг).")

def check_expiry(issue_date):
    """Проверяет, истек ли срок выполнения заметки."""
    current_date = datetime.now()
    issue_datetime = datetime.strptime(issue_date, "%d-%m-%Y")

    RED = "\033[31m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    if current_date.date() == issue_datetime.date():
        print(YELLOW + "\nДедлайн сегодня!" + RESET)
    elif current_date > issue_datetime:
        expired_duration = current_date - issue_datetime
        print(RED + "\nСрок выполнения заметки истёк!" + RESET)
        print(RED + "Внимание! Дедлайн истёк: " + format_duration(expired_duration) + RESET)
    else:
        remaining_duration = issue_datetime - current_date
        print(GREEN + "\nСрок выполнения заметки ещё не истёк." + RESET)
        print(GREEN + "Оставшееся время до истечения срока: " + format_duration(remaining_duration) + RESET)

def calculate_remaining_time(issue_date):
    """Вычисляет и возвращает оставшееся время до истечения срока."""
    current_date = datetime.now()

    # Преобразуем строку "дд месяц" обратно в объект datetime
    try:
        day, month_name = issue_date.split()
        month_number = list(months.values()).index(month_name) + 1  # Получаем номер месяца
        issue_datetime = datetime.strptime(f"{day}-{month_number}-{current_date.year}", "%d-%m-%Y")
    except ValueError as e:
        return f"Ошибка: Некорректный формат даты. {e}"

    # ANSI escape codes для цветов
    RED = "\033[31m"  # Красный цвет
    GREEN = "\033[92m"  # Зеленый цвет
    YELLOW = "\033[33m"  # Желтый цвет
    RESET = "\033[0m"  # Сброс цвета

    if current_date.date() == issue_datetime.date():
        return YELLOW + "Дедлайн сегодня!" + RESET
    elif current_date > issue_datetime:
        expired_duration = current_date - issue_datetime
        return RED + f"Внимание! Дедлайн истёк: {format_duration(expired_duration)} назад." + RESET
    else:
        remaining_duration = issue_datetime - current_date
        return GREEN + f"Оставшееся время до истечения срока: {format_duration(remaining_duration)}." + RESET


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

    created_date = input_valid_date("Введите дату создания заметки (дд-мм-гггг): ")
    issue_date = input_valid_date("Введите дату истечения заметки (дд-мм-гггг): ")

    day_created, month_created = created_date[:2], created_date[3:5]
    day_issue, month_issue = issue_date[:2], issue_date[3:5]

    temp_created_date = f"{day_created} {months[month_created]}"
    temp_issue_date = f"{day_issue} {months[month_issue]}"

    return {
        "username": username,
        "content": content,
        "status": status,
        "created_date": temp_created_date,
        "issue_date": temp_issue_date,
        "titles": list(titles)
    }

def main():
    notes = []
    start_time = datetime.now()
    print("\nДобро пожаловать в систему заметок. Вход в ждущий режим выполнения команд.")

    while True:
        command = input("\nВведите команду create, для создания новой заметки (или 'help' для справки): ").strip().lower()

        if command == 'create':
            print("\nСоздание новой заметки...")
            note = create_note()
            notes.append(note)
            print("Заметка успешно создана.")

        elif command == 'list':
            if not notes:
                print("\nНет доступных заметок.")
            else:
                for i, note in enumerate(notes, 1):
                    print(f"\nЗаметка {i}:")
                    display_note_info(note)

        elif command == 'time':
            if not notes:
                print("\nНет заметок для проверки времени.")
            else:
                for i, note in enumerate(notes, 1):
                    print(f"\nЗаметка {i}:")
                    print(calculate_remaining_time(note["issue_date"]))



        elif command == 'retry':

            if not notes:  # Проверяем, есть ли заметки

                print("Нет заметок для редактирования.")

                continue

            # Отображаем список заметок для выбора

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

            # Редактирование выбранной заметки

            print("\nРедактирование выбранной заметки:")

            # Редактирование имени пользователя

            new_username = input(f"Введите новое имя пользователя (текущая: {selected_note['username']}): ").strip()

            if new_username:
                selected_note['username'] = new_username

            # Редактирование заголовков

            print("\nРедактирование заголовков заметки.")

            new_titles = set(selected_note['titles'])

            while True:

                title_action = input("Введите новый заголовок (или оставьте пустым для завершения): ").strip()

                if not title_action:
                    break

                new_titles.add(title_action)

            selected_note['titles'] = list(new_titles)

            # Редактирование содержания

            new_content = input(f"Введите новое содержание заметки (текущее: {selected_note['content']}): ").strip()

            if new_content:
                selected_note['content'] = new_content

            # Редактирование даты создания

            new_created_date = input_valid_date(

                f"Введите новую дату создания заметки (текущая: {selected_note['created_date']}): "

            )

            if new_created_date:
                day_created, month_created = new_created_date[:2], new_created_date[3:5]

                selected_note['created_date'] = f"{day_created} {months[month_created]}"

            # Редактирование даты истечения

            new_issue_date = input_valid_date(

                f"Введите новую дату истечения заметки (текущая: {selected_note['issue_date']}): "

            )

            if new_issue_date:
                day_issue, month_issue = new_issue_date[:2], new_issue_date[3:5]

                selected_note['issue_date'] = f"{day_issue} {months[month_issue]}"

            print("Заметка успешно обновлена!")



        elif command == 'status':
            if not notes:
                print("\nНет заметок для редактирования статуса.")
            else:
                for i, note in enumerate(notes, 1):
                    print(f"{i}. {note['titles']}")
                while True:
                    choice = input("Выберите номер заметки для изменения статуса: ").strip()
                    if choice.isdigit() and 1 <= int(choice) <= len(notes):
                        selected_note = notes[int(choice) - 1]
                        print(f"Текущий статус заметки: {selected_note['status']}")

                        status_dict = {
                            "1": "\033[92mвыполнено\033[0m",
                            "2": "\033[93mв процессе\033[0m",
                            "3": "\033[31mотложено\033[0m"
                        }

                        for key, value in status_dict.items():
                            print(f"{key}. {value}")

                        while True:
                            new_status = input("Ваш выбор: ").strip()
                            if new_status in status_dict:
                                selected_note['status'] = status_dict[new_status]
                                print("Статус успешно обновлён.")
                                break
                            else:
                                print("Некорректный выбор. Попробуйте снова.")
                        break
                    else:
                        print("Некорректный номер. Попробуйте снова.")

        elif command == 'help':
            print("""
Доступные команды:

Основные:
  create : создать новую заметку.
  list   : отобразить информацию обо всех заметках.
  retry  : инициировать редактирование существующих заметок.
  status : изменить статус существующей заметки.

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
