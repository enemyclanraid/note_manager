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

from datetime import datetime, timedelta

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

def check_expiry(issue_date):
    """Проверяет, истек ли срок выполнения заметки."""
    current_date = datetime.now()
    issue_datetime = datetime.strptime(issue_date, "%d-%m-%Y")

    if current_date > issue_datetime:
        expired_duration = current_date - issue_datetime
        print("\nСрок выполнения заметки истёк!")
        print("Время, прошедшее с истечения срока:", format_duration(expired_duration))
    else:
        remaining_duration = issue_datetime - current_date
        print("\nСрок выполнения заметки ещё не истёк. Отобразить оставшееся время можно введя команду time")
        print("Оставшееся время до истечения срока:", format_duration(remaining_duration))

def calculate_remaining_time(issue_date):
    """Вычисляет и возвращает оставшееся время до истечения срока."""
    current_date = datetime.now()
    issue_datetime = datetime.strptime(issue_date, "%d-%m-%Y")

    if current_date > issue_datetime:
        expired_duration = current_date - issue_datetime
        return f"Срок выполнения истёк {format_duration(expired_duration)} назад."
    else:
        remaining_duration = issue_datetime - current_date
        return f"Оставшееся время до истечения срока: {format_duration(remaining_duration)}."

def main():
    # Запрос имени пользователя
    username = input("Введите имя пользователя: ")
    titles = set()  # Используем множество для хранения уникальных заголовков

    # Цикл для ввода заголовков заметок
    while True:
        title = input("Введите заголовок (или оставьте пустым для завершения): ")

        if title == "":
            break

        if title in titles:
            print("Этот заголовок уже существует. Пожалуйста, введите другой.")
        else:
            titles.add(title)  # Добавляем заголовок в множество

    # Ввод основной информации о заметке
    content = input("Введите описание заметки: ")
    print("\nВыберите статус заметки:")
    status_dict = {"1": "выполнено", "2": "в процессе", "3": "отложено"}
    for key, value in status_dict.items():
        print(f"{key}. {value}")

    while True:
        choice = input("Ваш выбор: ")
        if choice in status_dict:
            status = status_dict[choice]
            break
        else:
            print("Некорректный выбор. Пожалуйста, выберите один из предложенных вариантов.")

    # Ввод дат создания и истечения заметки
    created_date = input("Введите дату создания заметки (дд-мм-гггг): ")
    issue_date = input("Введите дату истечения заметки (дд-мм-гггг): ")

    # Разбор введенных дат
    day_created, month_created = created_date[:2], created_date[3:5]
    day_issue, month_issue = issue_date[:2], issue_date[3:5]

    # Форматирование дат с использованием словаря months
    temp_created_date = f"{day_created} {months[month_created]}"
    temp_issue_date = f"{day_issue} {months[month_issue]}"

    # Создание списка с информацией о заметке
    note = [
        username,
        content,
        status,
        temp_created_date,
        temp_issue_date,
        list(titles)  # Преобразуем множество обратно в список для вывода
    ]

    # Установка таймера
    start_time = datetime.now()
    print("\nЗаметка успешно создана. Вход в ждущий режим выполнения команд.")

    # Проверка срока выполнения заметки
    check_expiry(issue_date)

    # Вход в ждущий режим выполнения команд
    while True:
        command = input("\nВведите команду (или 'help' для справки): ").strip().lower()

        if command == 'list':
            display_note_info(note)

        elif command == 'retry':
            print("Редактирование заметки...")
            username = input("Введите новое имя пользователя (текущая: {}): ".format(note[0])) or note[0]
            content = input("Введите новое содержание заметки (текущее: {}): ".format(note[1])) or note[1]

            # Ввод новых дат
            created_date = input("Введите новую дату создания заметки (дд-мм-гггг, текущее: {}): ".format(note[3])) or \
                           note[3]
            issue_date = input("Введите новую дату истечения заметки (дд-мм-гггг, текущее: {}): ".format(note[4])) or \
                         note[4]

            # Разбор введенных дат
            day_created, month_created = created_date[:2], created_date[3:5]
            day_issue, month_issue = issue_date[:2], issue_date[3:5]

            # Форматирование дат с использованием словаря months
            temp_created_date = f"{day_created} {months[month_created]}"
            temp_issue_date = f"{day_issue} {months[month_issue]}"

            # Обновление заметки
            note[0] = username
            note[1] = content
            note[3] = temp_created_date
            note[4] = temp_issue_date

            # Заголовки могут быть изменены или оставлены без изменений
            new_titles = set()

            while True:
                title = input("Введите новый заголовок (или оставьте пустым для завершения): ")
                if title == "":
                    break
                new_titles.add(title)

            note[5] = list(new_titles)

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

        elif command == 'help':
            print("\nДоступные команды:")
            print("list - отобразить всю информацию о заметке.")
            print("retry - редактировать содержание и статус заметки.")
            print("status - изменить статус заметки.")
            print("help - отобразить список доступных команд.")
            print("time - отобразить оставшееся время до истечения срока заметки.")
            print("exit - выйти из программы.")

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
