def test():
    print("testing")
    result = celery_app.send_task(
        "app.tasks.email_tasks.send_email_task",
        args=["mail@gmail.com", "vm-123"]
    )
    return {"task_id": result.id}