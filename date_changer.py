# Создаем переменные
username = "Иван"
title = "Заметка о проекте"
content = "Необходимо завершить проект к дедлайну."
status = "В процессе"
created_date = "10-11-2024"
issue_date = "10-12-2024"

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

# Временные переменные
day_created, month_created = created_date[:2], created_date[3:5]
day_issue, month_issue = issue_date[:2], issue_date[3:5]

# Преобразуем месяц в текст
temp_created_date = f"{day_created} {months[month_created]}"
temp_issue_date = f"{day_issue} {months[month_issue]}"


# Выводим значения переменных
print("Имя пользователя:", username)
print("Заголовок заметки:", title)
print("Описание заметки:", content)
print("Статус заметки:", status)
print("Дата создания заметки:", temp_created_date)
print("Дата истечения заметки:", temp_issue_date)