import os
import winshell
import win32com.client

# Path to Python executable inside the virtual environment
python_path = os.path.abspath("venv\\Scripts\\python.exe")

# Path to your app.py
target_script = os.path.abspath("app.py")

# Shortcut name (NO special characters like ?, *, ", :, <, >, |, etc.)
shortcut_name = "Chinmaya Library.lnk"

# Desktop path
desktop = winshell.desktop()
shortcut_path = os.path.join(desktop, shortcut_name)

# Create the shortcut
shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortcut(shortcut_path)
shortcut.TargetPath = python_path
shortcut.Arguments = f'"{target_script}"'
shortcut.WorkingDirectory = os.path.dirname(target_script)
shortcut.IconLocation = python_path  # Optional: use Python icon
shortcut.save()

print(f"✅ Shortcut created on Desktop: {shortcut_path}")
