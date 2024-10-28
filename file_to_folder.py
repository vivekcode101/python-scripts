#Files getting moved to its corresponding folder
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


desktop_path = "c:/Users/IAMOPS/OneDrive - Iamops/Desktop"  

file_folders = {
    'Conf' : ['.conf']
    
}


for folder in file_folders.keys():
    folder_path = os.path.join(desktop_path, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def organize_existing_files():
    for filename in os.listdir(desktop_path):
        file_path = os.path.join(desktop_path, filename)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()
            for folder, extensions in file_folders.items():
                if file_ext in extensions:
                    shutil.move(file_path, os.path.join(desktop_path, folder))
                    print(f"Moved existing file {filename} to {folder}")
                    break

class DesktopEventHandler(FileSystemEventHandler):
    def on_created(self, event):

        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            file_ext = os.path.splitext(filename)[1].lower()
            for folder, extensions in file_folders.items():
                if file_ext in extensions:
                    shutil.move(event.src_path, os.path.join(desktop_path, folder))
                    print(f"Moved {filename} to {folder}")
                    break


organize_existing_files()


observer = Observer()
event_handler = DesktopEventHandler()
observer.schedule(event_handler, desktop_path, recursive=False)


observer.start()
print("Watching for new files on the desktop...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
