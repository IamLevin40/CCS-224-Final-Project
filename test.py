import tkinter as tk
from tkinter import filedialog

# Hide the root window
root = tk.Tk()
root.withdraw()

# Open file dialog
file_path = filedialog.askopenfilename(title="Select a text file", filetypes=[("Text Files", "*.txt")])

if file_path:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            print("File contents:\n")
            print(content)
    except Exception as e:
        print(f"Failed to read file: {e}")
else:
    print("No file was selected.")
