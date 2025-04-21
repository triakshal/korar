#!/usr/bin/env python3

import sys
import json
import datetime


def task_helper():
    try:
        with open("list.json", "r") as f:
            tasks = json.load(f)
            # Ensure we always return a list
            return tasks if isinstance(tasks, list) else []
    except FileNotFoundError:
        return []  # Return empty list instead of dict
    except json.decoder.JSONDecodeError:
        return []  # Return empty list instead of dict


def save_tasks(tasks):  # Renamed from save() for clarity
    with open("list.json", "w") as f:
        json.dump(tasks, f, indent=2)  # Dump the tasks, not the filename


def main():
    if len(sys.argv) < 2:
        print("Usage: korar [command] [options]")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Enter a task.")
            return
        description = " ".join(sys.argv[2:])
        tasks = task_helper()

        new_task = {
            "number": len(tasks) + 1,
            "description": description,
            "status": "incomplete",
            "createdAt": datetime.datetime.now().isoformat(),
            "updatedAt": datetime.datetime.now().isoformat(),
        }

        tasks.append(new_task)
        save_tasks(tasks)  # Fixed function call
        print(f"Task #{new_task['number']} added to your list.")

    elif command == "list":
        tasks = task_helper()

        if len(sys.argv) < 3:
            for t in tasks:
                print(f"{t['number']}: {t['description']} [{t['status']}]")
        else:
            status = sys.argv[2]
            sorted_tasks = [t for t in tasks if t["status"] == status]

            if not sorted_tasks:
                print("No tasks found.")
            else:
                for t in sorted_tasks:
                    print(f"{t['number']}: {t['description']}")

    elif command == "update":  # Changed from 'if' to 'elif'
        if len(sys.argv) < 4:
            print("Provide task # and edits.")
            return

        try:
            task_id = int(sys.argv[2])
            new_description = " ".join(sys.argv[3:])
            tasks = task_helper()
            task_found = False

            for t in tasks:
                if t["number"] == task_id:
                    t["description"] = new_description
                    t["updatedAt"] = datetime.datetime.now().isoformat()
                    task_found = True
                    break
            if task_found:
                save_tasks(tasks)
                print(f"Task #{task_id} updated.")
            else:
                print(f"Task #{task_id} not found.")
        except ValueError:
            print("Invalid task number.")

    elif command in ["mark-complete", "mark-in-progress"]:  # Fixed the comparison
        if len(sys.argv) < 3:
            print("Provide task #.")
            return

        try:
            task_id = int(sys.argv[2])
            new_status = "complete" if command == "mark-complete" else "in-progress"

            tasks = task_helper()
            task_found = False

            for t in tasks:
                if t["number"] == task_id:
                    t["status"] = new_status
                    t["updatedAt"] = datetime.datetime.now().isoformat()
                    task_found = True
                    break
            if task_found:
                save_tasks(tasks)
                print(f"Task #{task_id} marked {new_status}.")
            else:
                print(f"Task #{task_id} not found.")
        except ValueError:
            print("Invalid task number.")

    elif command == "remove":
        if len(sys.argv) < 3:
            print("Provide task #.")
            return

        try:
            task_id = int(sys.argv[2])
            tasks = task_helper()
            initial_length = len(tasks)

            tasks = [t for t in tasks if t["number"] != task_id]

            if len(tasks) < initial_length:
                save_tasks(tasks)
                print(f"Task #{task_id} removed.")
            else:
                print(f"Task #{task_id} not found.")
        except ValueError:
            print("Invalid task number.")


if __name__ == "__main__":
    main()
