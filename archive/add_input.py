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

username = input("Введите имя пользователя: ")
title = input("Введите заголовок заметки: ")
content = input("Введите описание заметки: ")
status = input("Введите статус заметки: ")

created_date = input("Введите дату создания заметки (дд-мм-гггг): ")
issue_date = input("Введите дату истечения заметки (дд-мм-гггг): ")

day_created, month_created = created_date[:2], created_date[3:5]
day_issue, month_issue = issue_date[:2], issue_date[3:5]

temp_created_date = f"{day_created} {months[month_created]}"
temp_issue_date = f"{day_issue} {months[month_issue]}"

print("\nИмя пользователя:", username)
print("Заголовок заметки:", title)
print("Описание заметки:", content)
print("Статус заметки:", status)
print("Дата создания заметки:", temp_created_date)
print("Дата истечения заметки:", temp_issue_date)