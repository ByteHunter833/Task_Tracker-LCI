

# Task Tracker

A simple task tracker application built with Django. This project allows users to add, update, delete, and manage tasks from the command line interface (CLI). Tasks are stored in a database and can be exported to a JSON file for easy backup or transfer.

## Features

- Add, update, delete tasks
- Mark tasks as "in progress" or "done"
- List all tasks or filter tasks by their status:
  - All tasks
  - Tasks that are done
  - Tasks that are not done
  - Tasks that are in progress
- Data is stored in a Django database and saved to a JSON file

## Installation

### Prerequisites

- Python 3.8 or higher
- Django 3.x or higher

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/task-tracker.git
   cd task-tracker
   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:

   ```bash
   python manage.py migrate
   ```

5. (Optional) Load existing tasks from JSON file:
   ```bash
   python manage.py task load_json
   ```

## Usage

After setting up your project, you can start using the Task Tracker through the Django management commands.

### Available Commands

- **Add a task:**

  ```bash
  python manage.py task add --title "Task Title"
  ```

- **Update a task:**

  ```bash
  python manage.py task update --id <task_id> --title "New Task Title"
  ```

- **Delete a task:**

  ```bash
  python manage.py task delete --id <task_id>
  ```

- **Update task status (e.g., mark as done):**

  ```bash
  python manage.py task status --id <task_id> --status done
  ```

- **List all tasks:**

  ```bash
  python manage.py task list
  ```

- **List tasks by status:**

  ```bash
  python manage.py task list --status done
  python manage.py task list --status not_done
  python manage.py task list --status in_progress
  ```

- **Export tasks to a JSON file:**

  ```bash
  python manage.py task save_json
  ```

- **Load tasks from a JSON file:**
  ```bash
  python manage.py task load_json
  ```

## File Structure

```
task-tracker/
├── task/                           # App containing task management logic
│   ├── migrations/
│   ├── models.py                   # Model definition for Task
│   ├── management/
│   │   └── commands/
│   │       └── task.py             # Custom management commands for task handling
├── tasks.json                      # JSON file storing tasks (generated by `save_json`)
├── manage.py                       # Django management script
└── requirements.txt                # List of Python dependencies
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
=======
# Task_Tracker-LCI
Task manager created with Django
>>>>>>> 63c21f7969385df78383ddddb934639c4ea50016
