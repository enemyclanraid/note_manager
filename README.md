# Описание проекта

Этот проект состоит из нескольких скриптов, каждый из которых выполняет свою задачу, поэтапно выражая одну - "Заметки".

## Скрипты

1. **create_note_function.py**  
   Финальная версия с исправлениями:
    - Добавлена возможность ввода текущей даты без заполнения, просто оставив ввод пустым.
    - Корректная калькуляцией дней с учётом года.
    - Добавлена поддержка формата 01/01/2033
    - Восстановлена команда retry и доработана команда status

2. **update_note_function.py**  
    Добавлена функция update_note, вызываемая по команде update, обновление существующих заметок, отдельно по категориям.

3. **display_notes_function.py**  
    Добавлена функция list_notes, вызываемая по команде table, отображает список в виде таблицы с постраничной 
    навигацией и сортировкой по дате создания, по дедлайну, по статусу и без сортировки.

4. **search_notes_function.py**  
    Добавлена функция search_notes, поиск заметок по заданным критериям.

5. **menu.py**  
    Добавлено отображение меню при старте программы, доступен ввод команд по числовому значению. Необходимо установить 
    библиотеку для отображения цветного текста меню "pip install colorama".   

6. **save_notes_to_file.py**  
    Добавлены три новые функции:
   - Сохранение заметок, вызываемая командой save.
   - Импортирование заметок, вызываемая командой import.
   - Удаление дубликатов заметок, вызываемая командой cleard.

## Использование

1. Скачайте или клонируйте репозиторий.
2. Убедитесь, что у вас установлен Python.
3. Запустите каждый файл поочерёдно для проверки на выполнения его задачи.
4. Итоговая работа собрана и выводится в `menu.py`.

## Пример вывода

```plaintext
Текущая дата: 16-01-2025

Добро пожаловать в систему заметок. Вход в ждущий режим выполнения команд.

Введите команду create, для создания новой заметки (или 'help' для справки): create

Создание новой заметки...
Введите имя пользователя: geo
Введите заголовок (или оставьте пустым для завершения): 1
Введите заголовок (или оставьте пустым для завершения): 2
Введите заголовок (или оставьте пустым для завершения): 
Введите описание заметки: test

Выберите статус заметки:
1. выполнено
2. в процессе
3. отложено
Ваш выбор: 2
Введите дату создания заметки (дд-мм-гггг или дд/мм/гггг) или оставьте поле пустым, если нужно вставить текущую дату: 
Введите дату истечения заметки (дд-мм-гггг или дд/мм/гггг): 01-02-2033
Заметка успешно создана.
Оставшееся время до истечения срока: 8 лет, 0 месяцев, 2 недель, 3 дней, 9 часов, 40 минут, 39 секунд.
Хотите добавить ещё одну заметку? (yes/no): 
