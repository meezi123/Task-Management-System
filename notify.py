def notify_status_change(task_id: int, new_status: str):
    # Option 1: Print to console
    print(f"[NOTIFY] Task {task_id} status changed to '{new_status}'")

    # Option 2: Log to file
    with open("task_notifications.log", "a") as f:
        f.write(f"Task {task_id} status changed to '{new_status}'\n")
