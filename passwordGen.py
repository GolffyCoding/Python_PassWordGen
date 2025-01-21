import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import string
import pyperclip

# ฟังก์ชันสำหรับสุ่มรหัสผ่าน
def generate_password():
    try:
        length = int(entry_length.get())
        if length <= 0:
            raise ValueError("Length must be positive")
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        entry_password.delete(0, tk.END)
        entry_password.insert(0, password)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid length.")
        


# ฟังก์ชันสำหรับบันทึกรหัสผ่าน
def save_password():
    password = entry_password.get()
    if not password:
        messagebox.showwarning("Empty Password", "Please generate a password first.")
        return

    name = simpledialog.askstring("Save Password", "Enter a name for this password:")
    if not name:
        messagebox.showwarning("No Name", "Password not saved without a name.")
        return

    try:
        with open("saved_passwords.txt", "a") as file:
            file.write(f"{name}: {password}\n")
        messagebox.showinfo("Saved", "Password saved successfully!")
        listbox_passwords.insert(tk.END, name)
    except Exception as e:
        messagebox.showerror("Error", f"Could not save password: {e}")

# ฟังก์ชันสำหรับการคัดลอกรหัสผ่าน
def copy_password():
    selected = listbox_passwords.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a saved password.")
        return

    name = listbox_passwords.get(selected[0])
    try:
        with open("saved_passwords.txt", "r") as file:
            for line in file:
                if line.startswith(f"{name}: "):
                    password = line.split(f"{name}: ")[1].strip()
                    pyperclip.copy(password)
                    messagebox.showinfo("Copied", "Password copied to clipboard!")
                    return
        messagebox.showerror("Not Found", "Password not found in the file.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not copy password: {e}")

# การตั้งค่า GUI
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("400x400")

# ความยาวรหัสผ่าน
frame_length = tk.Frame(root)
frame_length.pack(pady=10)
tk.Label(frame_length, text="Password Length:").pack(side=tk.LEFT)
entry_length = tk.Entry(frame_length, width=5)
entry_length.insert(0, "16")
entry_length.pack(side=tk.LEFT)

# แสดงรหัสผ่าน
frame_password = tk.Frame(root)
frame_password.pack(pady=10)
tk.Label(frame_password, text="Generated Password:").pack(side=tk.LEFT)
entry_password = tk.Entry(frame_password, width=30)
entry_password.pack(side=tk.LEFT)

# ปุ่ม Generate
btn_generate = tk.Button(root, text="Generate Password", command=generate_password)
btn_generate.pack(pady=10)

# ปุ่ม Save
btn_save = tk.Button(root, text="Save Password", command=save_password)
btn_save.pack(pady=10)

# รายการรหัสผ่านที่บันทึกไว้
frame_list = tk.Frame(root)
frame_list.pack(pady=10)
tk.Label(frame_list, text="Saved Passwords:").pack()
listbox_passwords = tk.Listbox(frame_list, width=40, height=10)
listbox_passwords.pack()

# ปุ่ม Copy
btn_copy = tk.Button(root, text="Copy Password", command=copy_password)
btn_copy.pack(pady=10)

root.mainloop()
