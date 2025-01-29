import yaml
import json



def save_notes_to_file(notes, filename):
    """Сохраняет список заметок в файл в формате YAML."""
    for note in notes:
        note['status'] = note['status'].replace('\033[92m', '').replace('\033[93m', '').replace('\033[31m', '').replace(
            '\033[0m', '')

    with open(filename, 'w', encoding='utf-8') as file:
        yaml.dump(notes, file, allow_unicode=True, sort_keys=False)

    print(f"Заметки успешно сохранены в файл {filename}")



def open_notes_from_file(filename):
    """Загружает заметки из файла в формате YAML и присваивает цвета статусам."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            notes = yaml.safe_load(file)

        if not isinstance(notes, list):
            print(f"Файл {filename} не содержит корректный формат заметок.")
            return []

        status_colors = {
            "выполнено": "\033[92mвыполнено\033[0m",
            "в процессе": "\033[93mв процессе\033[0m",
            "отложено": "\033[31mотложено\033[0m"
        }

        for note in notes:
            if 'status' in note:
                status = note['status'].lower().strip()
                note['status'] = status_colors.get(status, note['status'])

        print(f"Заметки успешно загружены из файла {filename}")
        return notes
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return []
    except yaml.YAMLError as e:
        print(f"Ошибка чтения YAML из файла {filename}: {e}")
        return []
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return []

def append_notes_to_file(notes, filename):
    """Добавляет список заметок в файл в формате YAML."""
    try:
        existing_notes = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                existing_notes = yaml.safe_load(file) or []
        except FileNotFoundError:
            print(f"Файл {filename} не найден. Будет создан новый файл.")
        except yaml.YAMLError as e:
            print(f"Ошибка чтения YAML из файла {filename}: {e}")
            return

        for note in notes:
            note['status'] = note['status'].replace('\033[92m', '').replace('\033[93m', '').replace('\033[31m',
                                                                                                    '').replace(
                '\033[0m', '')

        existing_notes.extend(notes)

        with open(filename, 'w', encoding='utf-8') as file:
            yaml.dump(existing_notes, file, allow_unicode=True, sort_keys=False)

        print(f"Заметки успешно добавлены в файл {filename}")
    except Exception as e:
        print(f"Произошла ошибка при добавлении заметок в файл: {e}")

def save_notes_json(notes, filename):
    """Сохраняет список заметок в JSON файл."""
    json_notes = []
    for note in notes:
        json_note = {
            "username": note["username"],
            "title": ", ".join(note["titles"]),
            "content": note["content"],
            "status": note["status"].replace('\033[92m', '').replace('\033[93m', '').replace('\033[31m', '').replace(
                '\033[0m', ''),
            "created_date": note["created_date"],
            "issue_date": note["issue_date"]
        }
        json_notes.append(json_note)

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(json_notes, file, ensure_ascii=False, indent=4)

    print(f"Заметки успешно сохранены в файл {filename} в формате JSON")