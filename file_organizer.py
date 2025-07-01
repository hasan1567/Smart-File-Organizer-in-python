import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import csv

def organize_files(folder):
    if not os.path.isdir(folder):
        messagebox.showerror("Error", "Invalid folder selected.")
        return

    for file in os.listdir(folder):
        filepath = os.path.join(folder, file)
        if os.path.isfile(filepath):
            ext = file.split('.')[-1].lower()
            target_dir = os.path.join(folder, ext + "_files")
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(filepath, os.path.join(target_dir, file))
    messagebox.showinfo("Done", "Files organized by type.")

def bulk_rename(folder, prefix):
    if not os.path.isdir(folder):
        messagebox.showerror("Error", "Invalid folder selected.")
        return

    files = sorted(os.listdir(folder))
    renamed = []
    for i, filename in enumerate(files, 1):
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath):
            ext = filename.split('.')[-1]
            new_name = f"{prefix}_{i}.{ext}"
            new_path = os.path.join(folder, new_name)
            os.rename(filepath, new_path)
            renamed.append((filename, new_name))

    if renamed:
        log_path = os.path.join(folder, "rename_log.csv")
        with open(log_path, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Original Name", "New Name"])
            writer.writerows(renamed)
        messagebox.showinfo("Done", f"Renamed {len(renamed)} files.\nLog saved to rename_log.csv")
    else:
        messagebox.showinfo("Nothing", "No files to rename.")

# === GUI ===
def choose_folder():
    folder = filedialog.askdirectory()
    folder_var.set(folder)

def run_organize():
    organize_files(folder_var.get())

def run_rename():
    bulk_rename(folder_var.get(), prefix_var.get())

app = tk.Tk()
app.title("🗂️ Smart File Organizer & Renamer")
app.geometry("400x300")

tk.Label(app, text="Select Folder").pack(pady=5)
folder_var = tk.StringVar()
tk.Entry(app, textvariable=folder_var, width=40).pack()
tk.Button(app, text="Browse", command=choose_folder).pack(pady=5)

tk.Label(app, text="Rename Prefix").pack(pady=5)
prefix_var = tk.StringVar(value="file")
tk.Entry(app, textvariable=prefix_var, width=20).pack()

tk.Button(app, text="📁 Organize Files by Type", command=run_organize, bg="lightblue").pack(pady=10)
tk.Button(app, text="✍ Bulk Rename Files", command=run_rename, bg="lightgreen").pack(pady=5)

tk.Label(app, text="Developed by Hasan", fg="gray").pack(pady=10)
app.mainloop()
