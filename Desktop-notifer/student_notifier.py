import json
import time
import os
from datetime import datetime
from win10toast import ToastNotifier

# ✅ Load tasks from JSON
def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading tasks.json: {e}")
        return []

# ✅ Show notification
def show_notification(toaster, title, icon_path=None):
    try:
        toaster.show_toast(
            "📢 Task Reminder!",
            f"Don't forget: {title}",
            icon_path=icon_path if icon_path and os.path.exists(icon_path) else None,
            duration=6
        )
    except Exception as e:
        print(f"⚠️ Notification error: {e}")

# ✅ Main loop
def main():
    toaster = ToastNotifier()
    notified = set()

    icon_path = os.path.join(os.getcwd(), "notification.ico")
    if not os.path.exists(icon_path):
        icon_path = None

    while True:
        tasks = load_tasks()
        current_time = datetime.now().strftime("%H:%M")  # current time (HH:MM)

        for task in tasks:
            task_id = str(task.get("id", task["title"]))

            # 🔹 Type 1: Time-based task
            if "time" in task:
                if task["time"] == current_time and task_id not in notified:
                    show_notification(toaster, task["title"], icon_path)
                    notified.add(task_id)

            # 🔹 Type 2: Due-soon task
            elif task.get("due_soon") and not task.get("completed") and task_id not in notified:
                show_notification(toaster, task["title"], icon_path)
                notified.add(task_id)

        time.sleep(30)  # check every 30 seconds

if __name__ == "__main__":
    main()
