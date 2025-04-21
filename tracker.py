import sys
import json
import datetime

# if __name__ == "__main__":
#     main()

def task_helper():
    try:
        with open("list.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError:
        return {}

def save():
    with open("list.json", "w") as f:
        json.dump("list.json", f, indent=2)


def main():
    if len(sys.argv) < 2:
        print("Usage: Korar [command] [options]")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Enter a task.")
            return
        description = " ".join(sys.argv[2:])
        tasks = task_helper()

        new_task = {
            "number": len(tasks)+1,
            "description": description,
            "status": "todo",
            "createdAt": datetime.datetime.now().isoformat(),
            "updatedAt": datetime.datetime.now().isoformat(),
        }

        tasks.append(new_task)
        save_tasks = tasks
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

    if command == "update":
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

    elif command == ["mark-complete", "mark-in-progress"]:
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


