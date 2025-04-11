import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

FILENAME = "tasks.csv"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.task_var = tk.StringVar()
        self.df = pd.DataFrame(columns=["Task"])    

        self.setup_widgets()
        self.load_tasks()

    def setup_widgets(self):
        tk.Label(self.root, text="Enter Task:").pack(pady=5)
        tk.Entry(self.root, textvariable=self.task_var, width=30).pack(pady=5)
        tk.Button(self.root, text="Add Task", command=self.add_task).pack(pady=5)
        tk.Button(self.root, text="Remove Selected", command=self.remove_task).pack(pady=5)
        tk.Button(self.root, text="Save Tasks", command=self.save_tasks).pack(pady=5)
        tk.Button(self.root, text="Complete Task", command=self.complete_task).pack(pady=5)


        self.listbox = tk.Listbox(self.root, width=45, height=10)
        self.listbox.pack(pady=10)

    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            self.df = pd.concat([self.df, pd.DataFrame({"Task": [task]})], ignore_index=True)
            self.listbox.insert(tk.END, task)
            #reset the text variable to ""
            self.task_var.set("")
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty.")

    def remove_task(self):
        try:
            index = self.listbox.curselection()[0]
            self.listbox.delete(index)
            self.df.drop(index, inplace=True)
            self.df.reset_index(drop=True, inplace=True)
        except IndexError:
            messagebox.showwarning("Selection Error", "No task selected to remove.")

    def complete_task(self):
        try:
            index = self.listbox.curselection()[0]
            task = self.listbox.get(index)
            task += " IS COMPLETED"
            self.listbox.delete(index)
            self.listbox.insert(index, task)
        except IndexError:
            messagebox.showwarning("Selection Error", "No task selected to complete.")


    def save_tasks(self):
        self.df.to_csv(FILENAME, index=False)
        messagebox.showinfo("Saved", "Tasks saved using pandas.")

    def load_tasks(self):
        if os.path.exists(FILENAME):
            self.df = pd.read_csv(FILENAME)
            for task in self.df["Task"]:
                self.listbox.insert(tk.END, task)

if __name__ == "__main__":
    window = tk.Tk()
    window.title("To-Do List with Pandas")
    window.geometry("800x800")
    app = TodoApp(window)
    window.mainloop()


