# Словарь для отображения месяцев текстом
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

# Получаем данные от пользователя
username = input("Введите имя пользователя: ")
title1 = input("Введите заголовок заметки 1: ")
title2 = input("Введите заголовок заметки 2: ")
title3 = input("Введите заголовок заметки 3: ")
titles = [title1, title2, title3 ]
content = input("Введите описание заметки: ")
status = input("Введите статус заметки: ")

# Запрашиваем даты у пользователя с указанием формата
created_date = input("Введите дату создания заметки (дд-мм-гггг): ")
issue_date = input("Введите дату истечения заметки (дд-мм-гггг): ")

# Временные переменные
day_created, month_created = created_date[:2], created_date[3:5]
day_issue, month_issue = issue_date[:2], issue_date[3:5]

# Преобразуем месяц в текст
temp_created_date = f"{day_created} {months[month_created]}"
temp_issue_date = f"{day_issue} {months[month_issue]}"

# Выводим значения переменных
print("\nИмя пользователя:", username)
print("Заголовки заметок:", titles)
print("Описание заметки:", content)
print("Статус заметки:", status)
print("Дата создания заметки:", temp_created_date)
print("Дата истечения заметки:", temp_issue_date)