import tkinter as tk
from tkinter import messagebox, ttk
from db import register_user, login_user, add_task, get_tasks_by_user, delete_task, complete_task, reset_tasks


class TodoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.attributes('-fullscreen', True)  # Fullscreen mode

        # Variables to store user inputs
        self.username_input = None
        self.password_input = None
        self.user_id = None  # To track the logged-in user

        self.create_login_widgets()

    def create_login_widgets(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create login/register UI
        tk.Label(self.root, text="Username").pack(pady=5)
        self.username_input = tk.Entry(self.root, width=40)
        self.username_input.pack(pady=5)

        tk.Label(self.root, text="Password").pack(pady=5)
        self.password_input = tk.Entry(self.root, show="*", width=40)
        self.password_input.pack(pady=5)

        self.login_button = tk.Button(self.root, text="Login", command=self.login_user)
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(self.root, text="Register", command=self.register_user)
        self.register_button.pack(pady=5)

    def create_todo_widgets(self):
        # Clear login/register UI
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create task management UI
        self.task_list_frame = tk.Frame(self.root)
        self.task_list_frame.place(relx=0, rely=0, relwidth=1, relheight=0.6)

        # Treeview to display tasks in columns
        columns = ('ID', 'Task', 'Description', 'Date Added', 'Status')
        self.task_listbox = ttk.Treeview(self.task_list_frame, columns=columns, show='headings')
        self.task_listbox.heading('ID', text='ID')
        self.task_listbox.heading('Task', text='Task')
        self.task_listbox.heading('Description', text='Description')
        self.task_listbox.heading('Date Added', text='Date Added')
        self.task_listbox.heading('Status', text='Status')

        # Define column widths
        self.task_listbox.column('ID', width=50)
        self.task_listbox.column('Task', width=150)
        self.task_listbox.column('Description', width=200)
        self.task_listbox.column('Date Added', width=150)
        self.task_listbox.column('Status', width=100)

        self.task_listbox.pack(fill=tk.BOTH, expand=True, pady=10)

        # Control frame for adding, deleting tasks, etc.
        self.control_frame = tk.Frame(self.root)
        self.control_frame.place(rely=0.6, relwidth=1, relheight=0.4)

        # Task input fields
        tk.Label(self.control_frame, text="Task Name").grid(row=0, column=0, padx=10, pady=10)
        self.task_input = tk.Entry(self.control_frame, width=30)
        self.task_input.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.control_frame, text="Task Description").grid(row=1, column=0, padx=10, pady=10)
        self.task_description_input = tk.Entry(self.control_frame, width=30)
        self.task_description_input.grid(row=1, column=1, padx=10, pady=10)

        # Add Task button
        self.add_button = tk.Button(self.control_frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=2, column=0, padx=10, pady=10)

        # Delete Task button
        self.delete_button = tk.Button(self.control_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=1, padx=10, pady=10)

        # Complete Task button
        self.complete_button = tk.Button(self.control_frame, text="Complete Task", command=self.complete_task)
        self.complete_button.grid(row=2, column=2, padx=10, pady=10)

        # Reset Task button
        self.reset_button = tk.Button(self.control_frame, text="Reset Tasks", command=self.reset_tasks)
        self.reset_button.grid(row=3, column=0, padx=10, pady=10)

        # Exit button
        self.exit_button = tk.Button(self.control_frame, text="Exit", command=self.root.quit)
        self.exit_button.grid(row=3, column=1, padx=10, pady=10)

        # Load tasks for logged-in user
        self.load_tasks()

    def load_tasks(self):
        # Clear current tasks in the list
        for i in self.task_listbox.get_children():
            self.task_listbox.delete(i)

        if self.user_id:
            tasks = get_tasks_by_user(self.user_id)
            for task in tasks:
                status = 'Completed' if task[4] else 'Pending'
                self.task_listbox.insert('', tk.END, values=(task[0], task[1], task[2], task[3], status))

    def add_task(self):
        task_name = self.task_input.get()
        task_description = self.task_description_input.get()

        if task_name and task_description and self.user_id:
            print(f"Adding task: {task_name}, Description: {task_description}, User ID: {self.user_id}")
            add_task(self.user_id, task_name, task_description)
            self.load_tasks()
            self.task_input.delete(0, tk.END)
            self.task_description_input.delete(0, tk.END)
        else:
            messagebox.showerror("Input Error", "Please enter a task name and description.")

    def delete_task(self):
        selected_item = self.task_listbox.selection()
        if selected_item:
            task_id = self.task_listbox.item(selected_item)['values'][0]
            delete_task(task_id)
            self.load_tasks()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def complete_task(self):
        selected_item = self.task_listbox.selection()
        if selected_item:
            task_id = self.task_listbox.item(selected_item)['values'][0]
            complete_task(task_id)
            self.load_tasks()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as complete.")

    def reset_tasks(self):
        reset_tasks(self.user_id)
        self.load_tasks()

    def register_user(self):
        username = self.username_input.get()
        password = self.password_input.get()

        if username and password:
            success, message = register_user(username, password)
            messagebox.showinfo("Registration", message)
        else:
            messagebox.showerror("Input Error", "Please enter a username and password.")

    def login_user(self):
        username = self.username_input.get()
        password = self.password_input.get()

        if username and password:
            user_id = login_user(username, password)
            if user_id is not None:
                self.user_id = user_id
                self.create_todo_widgets()
            else:
                messagebox.showerror("Login Error", "Invalid username or password.")
        else:
            messagebox.showerror("Input Error", "Please enter a username and password.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListApp(root)
    root.mainloop()
