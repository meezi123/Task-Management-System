from task_model import StatusEnum
def notify_status_change(task_id: int, new_status:StatusEnum ):
    # Log to file
    with open("task_notifications.log", "a") as f:
        f.write(f"Task {task_id} status changed to '{new_status.value}'\n")
