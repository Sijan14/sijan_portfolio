"""
StrikeThrough - A Command-Line To-Do List
Developed by Md Allama Ikbal Sijan
"""

import random
from tabulate import tabulate
from datetime import datetime
import os

# Randomized motivational messages
messages = [
    "Using a to-do list keeps you organized and focused!",
    "To-do lists help clear your mind and prioritize your goals.",
    "Every great achievement starts with a list of tasks!",
    "A to-do list can transform chaos into clarity.",
    "Achieve more by writing down what you need to do!",
    "Break big tasks into smaller steps with your to-do list!",
    "Every task you check off is a step closer to success!",
    "Stay on top of deadlines with your to-do list!",
    "Productivity starts with a plan. Write it down!",
    "Your to-do list is a roadmap to your goals!"
]

def clear_console():
    """Clears the console screen for better readability."""
    os.system('cls' if os.name == 'nt' else 'clear')

def strikethrough(text):
    """Apply strikethrough to text."""
    return ''.join([f"\u0336{char}" for char in text])

# Task list
tasks = {}


def display_tasks():
    """Displays the task list sorted by due date with proper strikethrough handling and alignment."""

    def calculate_display_length(text):
        """Calculates the display length of a string, ignoring strikethrough characters."""
        return len("".join(c for c in text if c != '\u0336'))

    def parse_due_date(due_date):
        """Parses the due date or returns a placeholder for sorting."""
        try:
            return datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            return datetime.max  # Placeholder for tasks without a valid due date

    # Sort tasks by due date, tasks without a valid due date go at the bottom
    sorted_tasks = sorted(tasks.items(), key=lambda item: parse_due_date(item[1]['due_date']))

    task_rows = []
    max_id_len = len("id")  # Start with the length of the header "id"
    max_task_len = len("task")  # Start with the length of the header "task"
    max_date_len = len("due date")  # Start with the length of the header "due date"

    # Iterate through tasks and subtasks
    for task_id, task_data in sorted_tasks:
        main_task = task_data['name']
        due_date = task_data['due_date']
        subtasks = task_data['subtasks']

        # Handle strikethrough for deleted tasks
        if '\u0336' in main_task:
            main_task = main_task  # Keep the strikethrough characters as is

        # Update max lengths based on the task and subtask lengths
        max_id_len = max(max_id_len, len(task_id))
        max_task_len = max(max_task_len, calculate_display_length(main_task))
        max_date_len = max(max_date_len, len(due_date))

        # Add the main task to the rows
        task_rows.append([task_id, main_task, due_date])

        # Add subtasks to the rows
        for sub_id, sub_name in subtasks.items():
            display_sub_name = " " + sub_name  # Add space for display ONLY
            task_rows.append([sub_id, display_sub_name, ""])

            # Update max lengths for subtasks
            max_id_len = max(max_id_len, len(sub_id))
            max_task_len = max(max_task_len, calculate_display_length(display_sub_name))

    # Recalculate the total length for the table header and rows dynamically
    total_len = max_id_len + max_task_len + max_date_len + 9  # 9 for the column separators
    print("\ncurrent to-do list:")
    print("-" * total_len)
    print(f"| {'id':<{max_id_len}} | {'task':<{max_task_len}} | {'due date':<{max_date_len}} |")
    print("-" * total_len)

    # Print all the task rows with dynamic column widths
    for row in task_rows:
        print(f"| {row[0]:<{max_id_len}} | {row[1]:<{max_task_len}} | {row[2]:<{max_date_len}} |")
        print("-" * total_len)


def show_commands():
    """Displays the list of available commands."""
    print("\ncommands:")
    print(tabulate([
        ["add task", "add a new task"],
        ["add subtask", "add a subtask to an existing task"],
        ["delete task", "delete a task along with its subtasks"],
        ["delete subtask", "delete a specific subtask"],
        ["exit", "exit the to-do list application"]
    ], headers=["Command", "Action"], tablefmt="grid"))

def add_task():
    """Add a new main task with a due date."""
    task_id = f"t{len(tasks) + 1}"
    task_name = input("enter the task name: ")
    due_date = input("enter the due date (yyyy-mm-dd): ")

    tasks[task_id] = {"name": task_name, "due_date": due_date, "subtasks": {}}
    print(f"task '{task_name}' added.")

def add_subtask():
    """Add a subtask under an existing main task."""
    task_id = input("enter the main task id to add a subtask: ")
    if task_id in tasks:
        subtask_id = f"s{len(tasks[task_id]['subtasks']) + 1}"
        subtask_name = input("enter the subtask name: ")
        tasks[task_id]['subtasks'][subtask_id] = subtask_name
        print(f"subtask '{subtask_name}' added to task '{tasks[task_id]['name']}'.")
    else:
        print("task id not found.")

def delete_task():
    """Delete a main task and all its subtasks."""
    task_id = input("enter the task id to delete: ")
    if task_id in tasks:
        tasks[task_id]['name'] = strikethrough(tasks[task_id]['name'])
        tasks[task_id]['due_date'] = strikethrough(tasks[task_id]['due_date'])
        for sub_id in tasks[task_id]['subtasks']:
            tasks[task_id]['subtasks'][sub_id] = strikethrough(tasks[task_id]['subtasks'][sub_id])
        print(f"task '{task_id}' and its subtasks deleted.")
    else:
        print("task id not found.")


def delete_subtask():
    """Delete a subtask from a main task."""
    task_id = input("enter the main task id: ")
    if task_id in tasks:
        subtask_id = input("enter the subtask id to delete: ")
        if subtask_id in tasks[task_id]['subtasks']:
            tasks[task_id]['subtasks'][subtask_id] = strikethrough(tasks[task_id]['subtasks'][subtask_id])
            print(f"subtask '{subtask_id}' deleted.")

            # Check if all subtasks are deleted
            if all(strikethrough(sub) == sub for sub in tasks[task_id]['subtasks'].values()):
                tasks[task_id]['name'] = strikethrough(tasks[task_id]['name'])
                print(f"all subtasks deleted. main task '{task_id}' also marked as deleted.")
        else:
            print("subtask id not found.")
    else:
        print("task id not found.")

def main():
    """Main function to run the to-do list application."""
    clear_console()
    print(random.choice(messages))

    while True:
        display_tasks()
        show_commands()

        choice = input("\nenter a command: ")
        if choice == "add task":
            add_task()
        elif choice == "add subtask":
            add_subtask()
        elif choice == "delete task":
            delete_task()
        elif choice == "delete subtask":
            delete_subtask()
        elif choice == "exit":
            print("come back soon to stay productive!")
            break
        else:
            print("invalid command. please try again.")

        input("\npress enter to continue...")
        clear_console()

if __name__ == "__main__":
    main()
