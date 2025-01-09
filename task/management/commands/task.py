import os
import json
from django.core.management.base import BaseCommand
from task.models import Task
from datetime import datetime
from django.utils import timezone

JSON_FILE = "tasks.json"

def save_to_json():
    """Сохраняет все задачи в JSON-файл."""
    tasks = Task.objects.all().values("id", "title", "status", "created_at")
    for task in tasks:
        if timezone.is_aware(task["created_at"]):
                task["created_at"] = task["created_at"].astimezone(timezone.get_current_timezone())
        else:
            task["created_at"] = timezone.make_aware(task["created_at"])

        task["created_at"] = task["created_at"].strftime('%Y-%m-%d %H:%M:%S')
    with open(JSON_FILE, "w") as file:
        json.dump(list(tasks), file, indent=4)

def load_from_json():
    """Загружает задачи из JSON-файла в базу данных."""
    if not os.path.exists(JSON_FILE):
        return
    with open(JSON_FILE, "r") as file:
        tasks = json.load(file)
        for task in tasks:
            if task["created_at"]:
                task["created_at"] = datetime.strptime(task["created_at"], '%Y-%m-%d %H:%M:%S')
                task["created_at"] = timezone.make_aware(task["created_at"])

            Task.objects.update_or_create(
                id=task["id"],
                defaults={"title": task["title"], "status": task["status"], "created_at": task["created_at"]}
            )


class Command(BaseCommand):
    help = 'Task Tracker CLI'
    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help="Action to perform: add, update, delete, list, status")
        parser.add_argument('--id', type=int, help="ID of the task (for update, delete, or status)")
        parser.add_argument('--title', type=str, help="Title of the task (for add or update)")
        parser.add_argument('--status', type=str, choices=['not_done', 'in_progress', 'done'], help="Status of the task")
    def handle(self, *args, **kwargs):
        load_from_json()  # Загружаем данные из JSON при запуске

        action = kwargs['action']

        if action == 'add':
            self.add_task(kwargs['title'])
        elif action == 'update':
            self.update_task(kwargs['id'], kwargs['title'])
        elif action == 'delete':
            self.delete_task(kwargs['id'])
        elif action == 'status':
            self.update_status(kwargs['id'], kwargs['status'])
        elif action == 'list':
            self.list_tasks(kwargs.get('status'))
        else:
            self.stdout.write(self.style.ERROR("Unknown action"))

    def add_task(self, title):
        if not title:
            self.stdout.write(self.style.ERROR("Title is required to add a task"))
            return
        task = Task.objects.create(title=title)
        save_to_json()  # Сохраняем в JSON после добавления
        self.stdout.write(self.style.SUCCESS(f"Task added: {task.title} (ID: {task.id})"))

    def update_task(self, task_id, title):
        if not task_id or not title:
            self.stdout.write(self.style.ERROR("Task ID and title are required to update a task"))
            return
        try:
            task = Task.objects.get(id=task_id)
            task.title = title
            task.save()
            save_to_json()  # Сохраняем в JSON после обновления
            self.stdout.write(self.style.SUCCESS(f"Task updated: {task.title} (ID: {task.id})"))
        except Task.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Task with ID {task_id} does not exist"))

    def delete_task(self, task_id):
        if not task_id:
            self.stdout.write(self.style.ERROR("Task ID is required to delete a task"))
            return
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            save_to_json()  # Сохраняем в JSON после удаления
            self.stdout.write(self.style.SUCCESS(f"Task deleted (ID: {task_id})"))
        except Task.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Task with ID {task_id} does not exist"))

    def update_status(self, task_id, status):
        if not task_id or not status:
            self.stdout.write(self.style.ERROR("Task ID and status are required to update a task's status"))
            return
        try:
            task = Task.objects.get(id=task_id)
            task.status = status
            task.save()
            save_to_json()  # Сохраняем в JSON после обновления статуса
            self.stdout.write(self.style.SUCCESS(f"Task status updated: {task.title} -> {task.get_status_display()}"))
        except Task.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Task with ID {task_id} does not exist"))

    def list_tasks(self, status=None):
        tasks = Task.objects.all()
        if status:
            tasks = tasks.filter(status=status)
        if tasks.exists():
            for task in tasks:
                self.stdout.write(f"{task.id}: {task.title} - {task.get_status_display()}")
        else:
            self.stdout.write("No tasks found")
