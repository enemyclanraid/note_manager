
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

def display_note_info(note):
    """Функция для отображения информации о заметке."""
    print("\nИмя пользователя:", note[0])
    print("Содержание заметки:", note[1])
    print("Статус заметки:", note[2])
    print("Дата создания заметки:", note[3])
    print("Дата истечения заметки:", note[4])
    print("Заголовки заметок:", sorted(note[5]))

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
    status = "в процессе"
    print("\nВыберите начальный статус заметки:")
    for key, value in {"1": "выполнено", "2": "в процессе", "3": "отложено"}.items():
        print(f"{key}. {value}")

    while True:
        choice = input("Ваш выбор: ").strip()
        if choice in {"1", "2", "3"}:
            status = {"1": "выполнено", "2": "в процессе", "3": "отложено"}[choice]
            break
        else:
            print("Некорректный выбор. Пожалуйста, выберите число от 1 до 3.")


    created_date = input("Введите дату создания заметки (дд-мм-гггг): ")
    issue_date = input("Введите дату истечения заметки (дд-мм-гггг): ")


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


    while True:
        command = input("\nВведите команду (или 'help' для справки): ").strip().lower()

        if command == 'list':
            display_note_info(note)


        elif command == 'retry':

            print("Редактирование заметки...")
            username = input("Введите новое имя пользователя (текущая: {}): ".format(note[0])) or note[0]
            content = input("Введите новое содержание заметки (текущее: {}): ".format(note[1])) or note[1]


            created_date = input("Введите новую дату создания заметки (дд-мм-гггг, текущее: {}): ".format(note[3])) or \
                           note[3]
            issue_date = input("Введите новую дату истечения заметки (дд-мм-гггг, текущее: {}): ".format(note[4])) or \
                         note[4]


            day_created, month_created = created_date[:2], created_date[3:5]
            day_issue, month_issue = issue_date[:2], issue_date[3:5]


            temp_created_date = f"{day_created} {months[month_created]}"
            temp_issue_date = f"{day_issue} {months[month_issue]}"


            note[0] = username
            note[1] = content
            note[2] = status
            note[3] = temp_created_date
            note[4] = temp_issue_date


            new_titles = set()

            while True:
                title = input("Введите новый заголовок (или оставьте пустым для завершения): ")
                if title == "":
                    break
                new_titles.add(title)

            note[5] = list(new_titles)

            print("Заметка успешно обновлена.")

        elif command == 'status':
            current_status = note[2]
            print(f"\nТекущий статус заметки: \"{current_status}\"")

            while True:
                print("\nВыберите новый статус заметки:")
                print("1. выполнено")
                print("2. в процессе")
                print("3. отложено")
                choice = input("Ваш выбор: ").strip()

                if choice == "1":
                    note[2] = "выполнено"
                    break
                elif choice == "2":
                    note[2] = "в процессе"
                    break
                elif choice == "3":
                    note[2] = "отложено"
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
            print("exit - выйти из программы.")

        elif command == 'exit':
            print("Выход из программы.")
            break

        else:
            print("Неизвестная команда. Пожалуйста, введите 'help' для получения списка команд.")

if __name__ == "__main__":
    main()
