# tast 1
import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# Data structure to hold tasks
tasks = []

def load_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            data = json.load(file)
            global tasks
            tasks = data["tasks"]

def save_tasks():
    with open("tasks.json", "w") as file:
        data = {"tasks": tasks}
        json.dump(data, file)

def show_tasks():
    task_list.delete(0, tk.END)
    if not tasks:
        task_list.insert(tk.END, "No tasks found.")
    else:
        sorted_tasks = sorted(tasks, key=lambda x: x["due_date"])
        for idx, task in enumerate(sorted_tasks, 1):
            status = "Completed" if task["status"] else "Incomplete"
            task_list.insert(tk.END, f"{idx}. [{status}] {task['name']} - {task['description']} (Due: {task['due_date']})")

def add_task():
    name = entry_name.get()
    description = entry_description.get()
    due_date_str = entry_due_date.get()

    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Please use the format YYYY-MM-DD.")
        return

    tasks.append({
        "name": name,
        "description": description,
        "due_date": due_date.strftime("%Y-%m-%d"),
        "status": False
    })

    entry_name.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    entry_due_date.delete(0, tk.END)

    show_tasks()
    messagebox.showinfo("Success", "Task added successfully!")

def mark_completed():
    selected_index = task_list.curselection()
    if not selected_index:
        return

    task_num = int(selected_index[0]) + 1

    if 1 <= task_num <= len(tasks):
        task = tasks[task_num - 1]
        task["status"] = True
        show_tasks()
        messagebox.showinfo("Success", "Task marked as completed!")

def create_gui():
    global entry_name, entry_description, entry_due_date, task_list

    root = tk.Tk()
    root.title("Creative To-Do List Application")
    root.geometry("500x400")
    root.configure(bg="#f0f0f0")

    load_tasks()

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", foreground="black", background="#f0f0f0", font=("Helvetica", 12))
    style.configure("TButton", foreground="white", background="#333", font=("Helvetica", 12, "bold"))
    style.map("TButton", background=[("active", "#444")])

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)

    label_name = ttk.Label(frame, text="Task Name:", style="TLabel")
    label_name.grid(row=0, column=0, sticky="w")
    entry_name = ttk.Entry(frame, font=("Helvetica", 12))
    entry_name.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    label_description = ttk.Label(frame, text="Task Description:", style="TLabel")
    label_description.grid(row=1, column=0, sticky="w")
    entry_description = ttk.Entry(frame, font=("Helvetica", 12))
    entry_description.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    label_due_date = ttk.Label(frame, text="Due Date (YYYY-MM-DD):", style="TLabel")
    label_due_date.grid(row=2, column=0, sticky="w")
    entry_due_date = ttk.Entry(frame, font=("Helvetica", 12))
    entry_due_date.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    button_add = ttk.Button(frame, text="Add Task", command=add_task, style="TButton")
    button_add.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    button_mark_completed = ttk.Button(frame, text="Mark Task as Completed", command=mark_completed, style="TButton")
    button_mark_completed.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    task_list = tk.Listbox(frame, bg="white", fg="black", selectbackground="#ddd", selectforeground="black", font=("Helvetica", 12))
    task_list.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=task_list.yview)
    task_list.config(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=4, column=2, sticky="ns")

    show_tasks()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
