import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-alpha", 0)
path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text Documents", "*.txt"),))
root.destroy()