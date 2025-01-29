import locale
from datetime import datetime
from colorama import Fore, Style, init
import note_manager.utils.helpers as helpers
from note_manager.tests.test_notes import run_tests


def main():
    init(autoreset=True)
    locale.setlocale(locale.LC_TIME, 'ru_RU')
    now = datetime.now()
    formatted_date = now.strftime("%d-%m-%Y")

    GREEN = "\033[92m"
    RESET = "\033[0m"

    print(GREEN + "Текущая дата: " + formatted_date + RESET)
    notes = []
    start_time = datetime.now()
    print(Fore.GREEN + "\nДобро пожаловать в систему заметок. Вход в ждущий режим выполнения команд.")

    commands = {
        "1": "create - Создать новую заметку",
        "2": "list - Отобразить информацию обо всех заметках списком.",
        "3": "table - Отобразить информацию обо всех заметках в виде таблицы.",
        "4": "delete - Удалить существующую заметку.",
        "5": "retry - Инициировать редактирование существующих заметок.",
        "6": "status - Изменить статус существующих заметок.",
        "7": "update - Обновить существующие заметки.",
        "8": "search - Поиск заметок по ключевым словам.",
        "9": "time - Отобразить оставшееся время до истечения срока заметки.",
        "10": "help - Отобразить это сообщение.",
        "11": "exit - Выйти из программы.",
        "12": "save - Сохранить заметки в файл.",
        "13": "import - Импортировать заметки.",
        "14": "cleard - Удалить дубликаты заметок.",
        "15": "append - Добавить заметки в уже существующий файл.",
        "16": "savejs - Сохраняет заметки в формате JSON",
        "17": "test   - Тестирование."

    }

    while True:
        print(Fore.CYAN + "\nДоступные команды:")
        for key, value in commands.items():
            print(Fore.YELLOW + f"{key}. {value}")

        command_input = input(Fore.BLUE + "\nВведите команду (или номер команды): ").strip().lower()

        if command_input in commands:
            command_input = commands[command_input].split(" ")[0]

        if command_input == 'create':
            notes = helpers.create_notes(notes)

        elif command_input == 'list':
            helpers.list_notes(notes)

        elif command_input == 'table':
            helpers.table_notes(notes)

        elif command_input == 'delete':
            helpers.delete_note(notes)

        elif command_input == 'retry':
            helpers.edit_note(notes)

        elif command_input == 'status':
            helpers.update_note_status(notes)

        elif command_input == 'update':
            helpers.update_note(notes)

        elif command_input == 'search':
            helpers.search_command(notes)

        elif command_input == 'time':
            helpers.show_remaining_time(notes)

        elif command_input == 'help':
            helpers.show_help()

        elif command_input == 'exit':
            print(Fore.RED + "Выход из системы.")
            break

        elif command_input == 'save':
            helpers.save_notes(notes)

        elif command_input == 'import':
            notes = helpers.import_notes(notes)

        elif command_input == 'cleard':
            notes = helpers.clear_duplicates(notes)

        elif command_input == 'append':
            helpers.append_notes(notes)

        elif command_input == 'savejs':
            helpers.save_notes_json(notes)


        elif command_input == 'test':
            test_result = run_tests()
            if test_result:
                print("Все тесты успешно пройдены.")
            else:
                print("Некоторые тесты не пройдены. Проверьте вывод для подробностей.")
        else:
            print(Fore.RED + "Некорректная команда. Попробуйте снова.")

if __name__ == "__main__":
    main()
