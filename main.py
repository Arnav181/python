from tkinter import Tk
from db import create_table
from gui import TodoListApp

if __name__ == "__main__":
    create_table()  # Ensure tables are created
    root = Tk()
    app = TodoListApp(root)
    root.mainloop()
