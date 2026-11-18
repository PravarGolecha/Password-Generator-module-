import secrets
import string
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from tkinter import ttk

try:
    import pyperclip
except ImportError:
    pyperclip = None


MIN_LENGTH = 7
MAX_LENGTH = 32
DEFAULT_LENGTH = 12


def build_password(length, include_upper, include_lower, include_numbers, include_special):
    character_groups = []
    if include_upper:
        character_groups.append(string.ascii_uppercase)
    if include_lower:
        character_groups.append(string.ascii_lowercase)
    if include_numbers:
        character_groups.append(string.digits)
    if include_special:
        character_groups.append(string.punctuation)

    if not character_groups:
        raise ValueError("Select at least one character type.")
    if length < MIN_LENGTH or length > MAX_LENGTH:
        raise ValueError(
            f"Password length must be between {MIN_LENGTH} and {MAX_LENGTH}."
        )

    # Include at least one character from every selected character group.
    password = [secrets.choice(group) for group in character_groups]
    pool = "".join(character_groups)
    password.extend(secrets.choice(pool) for _ in range(length - len(password)))

    # A final shuffle removes the predictable group-at-start pattern.
    shuffled = password[:]
    for index in range(len(shuffled) - 1, 0, -1):
        swap_index = secrets.randbelow(index + 1)
        shuffled[index], shuffled[swap_index] = (
            shuffled[swap_index],
            shuffled[index],
        )
    return "".join(shuffled)


root = tk.Tk()
root.title("Password Generator")
root.geometry("700x360")
root.resizable(False, False)

length_value = tk.IntVar(value=DEFAULT_LENGTH)
upper_case = tk.BooleanVar(value=True)
small_case = tk.BooleanVar(value=True)
num = tk.BooleanVar(value=True)
special_chars = tk.BooleanVar(value=True)
password_value = tk.StringVar()
status_value = tk.StringVar()


def calculate_strength():
    selected_types = sum(
        (
            upper_case.get(),
            small_case.get(),
            num.get(),
            special_chars.get(),
        )
    )
    length = length_value.get()
    score = min(100, (length - MIN_LENGTH) * 5 + selected_types * 20)
    length_progress["value"] = score
    if score < 40:
        strength_label.configure(text="Password strength: Weak", foreground="#b91c1c")
    elif score < 70:
        strength_label.configure(text="Password strength: Moderate", foreground="#a16207")
    else:
        strength_label.configure(text="Password strength: Strong", foreground="#15803d")


def generate_pass():
    try:
        password = build_password(
            length_value.get(),
            upper_case.get(),
            small_case.get(),
            num.get(),
            special_chars.get(),
        )
        password_value.set(password)
        status_value.set("Password generated.")
    except ValueError as error:
        password_value.set("")
        status_value.set(str(error))
        messagebox.showwarning("Invalid options", str(error))


def copy_password():
    password = password_value.get()
    if not password:
        status_value.set("Generate a password before copying.")
        return
    if pyperclip is None:
        status_value.set("Clipboard support is unavailable (pyperclip is not installed).")
        return
    try:
        pyperclip.copy(password)
        status_value.set("Password copied to the clipboard.")
    except pyperclip.PyperclipException:
        status_value.set("Could not access the system clipboard.")


icon_path = Path(__file__).resolve().with_name("password.png")
if icon_path.exists():
    try:
        photo = tk.PhotoImage(file=str(icon_path))
        root.iconphoto(False, photo)
    except tk.TclError:
        pass

title = ttk.Label(
    root,
    text="Password Generator",
    font=("Arial", 18, "bold"),
)
title.place(x=250, y=15)

options_label = ttk.Label(root, text="Character types", font=("Arial", 11, "bold"))
options_label.place(x=70, y=65)

ttk.Checkbutton(
    root, text="A-Z", variable=upper_case, command=calculate_strength
).place(x=70, y=95)
ttk.Checkbutton(
    root, text="a-z", variable=small_case, command=calculate_strength
).place(x=145, y=95)
ttk.Checkbutton(
    root, text="0-9", variable=num, command=calculate_strength
).place(x=220, y=95)
ttk.Checkbutton(
    root,
    text="Special characters",
    variable=special_chars,
    command=calculate_strength,
).place(x=295, y=95)

ttk.Label(root, text="Length", font=("Arial", 11, "bold")).place(x=510, y=65)
length_scale = ttk.Scale(
    root,
    variable=length_value,
    from_=MIN_LENGTH,
    to=MAX_LENGTH,
    orient="horizontal",
    command=lambda _value: calculate_strength(),
)
length_scale.place(x=480, y=95, width=160)
length_display = ttk.Label(root, textvariable=length_value)
length_display.place(x=638, y=65)

style = ttk.Style(root)
style.configure("Password.Horizontal.TProgressbar", thickness=18)
length_progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=560,
    mode="determinate",
    style="Password.Horizontal.TProgressbar",
)
length_progress.place(x=70, y=145)

strength_label = ttk.Label(root, text="Password strength:")
strength_label.place(x=70, y=170)

ttk.Button(root, text="Generate Password", command=generate_pass).place(
    x=275, y=210
)

password_entry = ttk.Entry(
    root,
    textvariable=password_value,
    width=42,
    state="readonly",
)
password_entry.place(x=195, y=255)

ttk.Button(root, text="Copy", command=copy_password).place(x=315, y=295)
ttk.Label(root, textvariable=status_value).place(x=180, y=330)

calculate_strength()
root.mainloop()
