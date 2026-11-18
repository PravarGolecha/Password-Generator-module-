# Password Generator

## Overview

Password Generator is a desktop application built with Python and Tkinter. It creates passwords that include at least one character from every character type selected by the user. The project was created as a Python Formative Assessment and is intended for learning about GUI development and basic password generation.

## Features

- Choose uppercase letters (A-Z), lowercase letters (a-z), numbers (0-9), and special characters.
- Select a password length from 7 to 32 characters.
- Generate passwords using Python's cryptographically secure `secrets` module.
- Copy a generated password to the system clipboard.
- View a simple password-strength estimate and clear status messages.
- Optionally use a local `password.png` file as the application icon.

## How It Works

1. The Tkinter window is created and the controls are initialized.
2. The user selects one or more character types and chooses a length.
3. The application adds one random character from each selected character group.
4. It fills the remaining positions from the combined character pool.
5. It securely shuffles the result so that selected character types are not fixed in their original positions.
6. The password is displayed in a read-only text field.
7. If `pyperclip` is available, the Copy button sends the password to the system clipboard.

## Password Strength Logic

The strength bar is an estimate, not a formal cryptographic measurement. It is based on password length and the number of selected character types:

- Length contributes up to 125 points across the configured range.
- Each selected character type contributes 20 points.
- The displayed value is capped at 100.
- Below 40 is Weak.
- From 40 to below 70 is Moderate.
- From 70 upward is Strong.

Actual security also depends on password uniqueness and where the password is stored. Password length and using several character types improve resistance to guessing.

## Libraries and Modules

- **Python 3**: Programming language used for the application.
- **Tkinter**: Standard Python library used to create the desktop GUI.
- **`tkinter.ttk`**: Provides themed buttons, entries, checkboxes, scales, labels, and progress bars.
- **`secrets`**: Generates cryptographically secure random characters and shuffle positions.
- **`string`**: Provides standard uppercase, lowercase, digit, and punctuation character sets.
- **`pathlib`**: Resolves the optional icon file relative to the Python script.
- **`pyperclip`**: Optional third-party library used to copy passwords to the clipboard.

## Project Structure

```text
Password-Generator.py  - Main application source code
README.md              - Project documentation
password.png           - Optional application icon
```

## Requirements

- Python 3.10 or newer is recommended.
- Tkinter must be available in the Python installation.
- `pyperclip` is optional, but it is required for the Copy button to work.

On some Linux distributions, Tkinter may need to be installed separately through the system package manager.

## Setup

Open a terminal in the project directory and install the optional clipboard dependency:

```powershell
python -m pip install pyperclip
```

## Running the Application

From the project directory, run:

```powershell
python "Password-Generator.py"
```

The window can also be opened by double-clicking the Python file if `.py` files are associated with Python on the system.

## Usage

1. Select at least one character type.
2. Move the Length scale to choose 7-32 characters.
3. Click **Generate Password**.
4. Click **Copy** to copy the result if `pyperclip` is installed.

At least one character will be taken from every selected character group. The application prevents password generation when no character type is selected.

## Source Code Logic

The main logic is contained in `build_password()`:

- Character groups are assembled based on checkbox values.
- Selected groups are validated.
- Length is validated between 7 and 32.
- One character is selected securely from every selected group.
- Additional characters are selected from the combined pool.
- The list is shuffled using `secrets.randbelow()` so character positions do not follow a predictable pattern.
- The result is returned as a string.

The GUI functions separate generation, strength display, and clipboard handling. Missing dependencies and missing icons do not prevent the main application window from opening.

## Security Notes

- `secrets` is appropriate for generating passwords and other security-sensitive values.
- Generated passwords are not saved to disk by this project.
- The strength meter is a visual guide only.
- Use a password manager or account provider's secure tools for important or unique account credentials.

## Summary

This project demonstrates Python GUI development, user input validation, secure random selection, basic password-strength feedback, optional external-library integration, and clipboard use. The essential application behavior is contained in one Python file, while this README provides setup, usage, implementation, and security details.
