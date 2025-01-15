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
    print("\nИмя пользователя:", note[0])
    print("Содержание заметки:", note[1])
    print("Статус заметки:", note[2])
    print("Дата создания заметки:", note[3])
    print("Дата истечения заметки:", note[4])
    print("Заголовки заметок:", sorted(note[5]))

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
            # Проверяем дату с форматом дд-мм-гггг
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            return date_str  # Возвращаем строку, если дата корректна
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
        print(GREEN + "\nСрок выполнения заметки ещё не истёк. Отобразить оставшееся время можно введя команду time" + RESET)
        print(GREEN + "Оставшееся время до истечения срока: " + format_duration(remaining_duration) + RESET)


def calculate_remaining_time(issue_date):
    """Вычисляет и возвращает оставшееся время до истечения срока."""
    current_date = datetime.now()
    issue_datetime = datetime.strptime(issue_date, "%d-%m-%Y")


    RED = "\033[31m"
    GREEN = "\033[92m"
    RESET = "\033[0m"

    if current_date > issue_datetime:
        expired_duration = current_date - issue_datetime
        return RED + f"Внимание! Дедлайн истёк: {format_duration(expired_duration)} назад." + RESET
    else:
        remaining_duration = issue_datetime - current_date
        return GREEN + f"Оставшееся время до истечения срока: {format_duration(remaining_duration)}." + RESET

def main():

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


    print("\n")
    created_date = input_valid_date("Введите дату создания заметки (дд-мм-гггг): ")
    issue_date = input_valid_date("Введите дату истечения заметки (дд-мм-гггг): ")


    day_created, month_created = created_date[:2], created_date[3:5]
    day_issue, month_issue = issue_date[:2], issue_date[3:5]


    temp_created_date = f"{day_created} {months[month_created]}"
    temp_issue_date = f"{day_issue} {months[month_issue]}"


    note = [
        username,
        content,
        status,
        temp_created_date,
        temp_issue_date,
        list(titles)
    ]


    start_time = datetime.now()
    print("\nЗаметка успешно создана. Вход в ждущий режим выполнения команд.")


    check_expiry(issue_date)


    while True:
        command = input("\nВведите команду (или 'help' для справки): ").strip().lower()


        if command == 'list':
            display_note_info(note)


        elif command == 'retry':
            print("Редактирование заметки...")

            username = input("Введите новое имя пользователя (текущая: {}): ".format(note[0])) or note[0]
            content = input("Введите новое содержание заметки (текущее: {}): ".format(note[1])) or note[1]


            created_date = input_valid_date(
                "Введите новую дату создания заметки (дд-мм-гггг, текущее: {}): ".format(note[3])) or note[3]
            issue_date = input_valid_date(
                "Введите новую дату истечения заметки (дд-мм-гггг, текущее: {}): ".format(note[4])) or note[4]


            note[3] = f"{created_date[:2]} {months[created_date[3:5]]}"
            note[4] = f"{issue_date[:2]} {months[issue_date[3:5]]}"


            new_titles = set()
            while True:

                title = input("Введите новый заголовок (или оставьте пустым для завершения): ")
                if title == "":
                    break

                new_titles.add(title)

            note[5] = list(new_titles)


            note[0] = username
            note[1] = content
            print("Заметка успешно обновлена.")

        elif command == 'status':
            print(f"\nТекущий статус заметки: \"{note[2]}\"")

            while True:
                print("\nВыберите новый статус заметки:")
                print("1. выполнено")
                print("2. в процессе")
                print("3. отложено")
                choice = input("Ваш выбор: ").strip()

                if choice in status_dict:
                    note[2] = status_dict[choice]
                    break
                else:
                    print("Некорректный выбор. Пожалуйста, введите число от 1 до 3.")

            print(f"Статус заметки успешно обновлён на: \"{note[2]}\"")

        if command == 'help':

            print("\nДоступные команды:\n")
            print("Основные команды:")
            print("  list   : отобразить всю информацию о заметке.")
            print("  retry  : редактировать содержание и статус заметки.")
            print("  status  : изменить статус заметки.")
            print()
            print("Информация о времени:")
            print("  time   : отобразить оставшееся время до истечения срока заметки.")
            print()
            print("Помощь и выход:")
            print("  help   : отобразить список доступных команд.")
            print("  exit   : выйти из программы.")

        elif command == 'time':
            remaining_time_message = calculate_remaining_time(issue_date)
            print(remaining_time_message)

        elif command == 'exit':
            end_time = datetime.now()
            duration = end_time - start_time
            formatted_duration = format_duration(duration)
            print(f"Программа завершена. Время выполнения: {formatted_duration}")
            break

        else:
            print("Неизвестная команда. Пожалуйста, введите 'help' для получения списка команд.")

if __name__ == "__main__":
    main()