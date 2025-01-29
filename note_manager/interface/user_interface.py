def display_note_info(note):
    """Функция для отображения информации о заметке."""
    print("\nuid:", note["uid"])
    print("\nИмя пользователя:", note["username"])
    print("Содержание заметки:", note["content"])
    print("Статус заметки:", note["status"])
    print("Дата создания заметки:", note["created_date"])
    print("Дата истечения заметки:", note["issue_date"])
    print("Заголовки заметок:", sorted(note["titles"]))


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


    return {
        "username": username,
        "content": content,
        "status": status,
        "created_date": created_date,
        "issue_date": issue_date,
        "titles": list(titles)
    }
