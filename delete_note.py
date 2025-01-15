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

# Устанавливаем локаль на русский язык. Для отображения даты на русском языке.
locale.setlocale(locale.LC_TIME, 'ru_RU')
# Получаем текущую дату и время
now = datetime.now()
# Форматируем вывод
formatted_date = now.strftime("%d-%m-%Y")
# ANSI escape code для зеленого цвета
GREEN = "\033[92m"
RESET = "\033[0m"
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


def create_note():
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
            while True:
                note = create_note()
                notes.append(note)
                print("Заметка успешно создана.")

                while True:
                    add_more = input("Хотите добавить ещё одну заметку? (да/нет): ").lower()
                    if add_more in ['да', 'нет']:
                        break
                    print("Пожалуйста, введите 'да' или 'нет'.")

                if add_more == 'нет':
                    break

            print("Создание заметок завершено.")

        elif command == 'list':
            if not notes:
                print("\nНет доступных заметок.")
            else:
                for i, note in enumerate(notes, 1):
                    print(f"\nЗаметка {i}:")
                    display_note_info(note)


        elif command == 'delete':
            if not notes:
                print("\nНет доступных заметок для удаления.")
            else:
                print("\nВы можете удалить заметку по имени пользователя, заголовку или номеру.")
                criteria = input("Введите имя пользователя, заголовок или номер заметки для удаления: ").strip()

                found = False

                if criteria.isdigit():
                    index = int(criteria) - 1
                    if 0 <= index < len(notes):
                        deleted_note = notes.pop(index)
                        print(f"Заметка '{deleted_note['titles']}' успешно удалена.")
                        found = True
                    else:
                        print("Некорректный номер заметки.")

                else:
                    for i in range(len(notes) - 1, -1, -1):
                        if notes[i]["username"] == criteria or criteria in notes[i]["titles"]:
                            deleted_note = notes.pop(i)
                            print(f"Заметка '{deleted_note['titles']}' успешно удалена.")
                            found = True
                if not found:
                    print("Заметка не найдена.")

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

