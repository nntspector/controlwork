# Реализовать консольное приложение заметки, с сохранением, чтением,
# добавлением, редактированием и удалением заметок. Заметка должна
# содержать идентификатор, заголовок, тело заметки и дату/время создания или
# последнего изменения заметки. Сохранение заметок необходимо сделать в
# формате json или csv формат (разделение полей рекомендуется делать через
# точку с запятой).



import json
import os
import argparse
from datetime import datetime

NOTES_FILE = "notes.json"


def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as file:
            return json.load(file)
    return []


def save_notes(notes):
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, indent=4)


def add_note(title, message):
    notes = load_notes()
    note = {
        "id": len(notes) + 1,
        "title": title,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    notes.append(note)
    save_notes(notes)
    print("Заметка успешно сохранена")


def list_notes():
    notes = load_notes()
    if notes:
        print("Список заметок:")
        for note in notes:
            print(f"{note['id']}. {note['title']} - {note['timestamp']}")
    else:
        print("Заметок пока нет")


def edit_note(note_id, title, message):
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            note["title"] = title
            note["message"] = message
            note["timestamp"] = datetime.now().isoformat()
            save_notes(notes)
            print("Заметка успешно отредактирована")
            return
    print("Заметка с указанным ID не найдена")


def delete_note(note_id):
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            save_notes(notes)
            print("Заметка успешно удалена")
            return
    print("Заметка с указанным ID не найдена")


def filter_notes_by_date(date_str):
    try:
        date_filter = datetime.strptime(date_str, "%Y-%m-%d")
        notes = load_notes()
        filtered_notes = [note for note in notes if datetime.fromisoformat(
            note["timestamp"]) >= date_filter]
        if filtered_notes:
            print("Заметки после указанной даты:")
            for note in filtered_notes:
                print(f"{note['id']}. {note['title']} - {note['timestamp']}")
        else:
            print("Заметок после указанной даты нет")
    except ValueError:
        print("Ошибка: некорректный формат даты. Используйте YYYY-MM-DD")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Управление заметками")
    parser.add_argument("command", nargs="?", choices=[
                        "add", "list", "edit", "delete", "filter"], help="Команда")
    parser.add_argument("--title", help="Заголовок заметки")
    parser.add_argument("--msg", help="Тело заметки")
    parser.add_argument(
        "--id", type=int, help="ID заметки для редактирования или удаления")
    parser.add_argument(
        "--date", help="Дата для фильтрации заметок (формат: YYYY-MM-DD)")

    args = parser.parse_args()

    if args.command == "add":
        if args.title and args.msg:
            add_note(args.title, args.msg)
        else:
            print("Ошибка: не указан заголовок или тело заметки")
    elif args.command == "list":
        list_notes()
    elif args.command == "edit":
        if args.id and args.title and args.msg:
            edit_note(args.id, args.title, args.msg)
        else:
            print("Ошибка: не указан ID, заголовок или тело заметки")
    elif args.command == "delete":
        if args.id:
            delete_note(args.id)
        else:
            print("Ошибка: не указан ID заметки для удаления")
    elif args.command == "filter":
        if args.date:
            filter_notes_by_date(args.date)
        else:
            print("Ошибка: не указана дата для фильтрации")
    else:
        parser.print_help()
