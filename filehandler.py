import os
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


path = "D:/Users/user/Desktop/a"
path_destination = 'D:/Users/user/Desktop/b'


class MyFileHandler(FileSystemEventHandler):
    filenumber = 0
    def on_modified(self, event):
        new_filename = datetime.strftime(datetime.now(), f"%d.%m.%Y_(%H-%M-%S)_FILENUMBER={str(self.filenumber)}")
        for filename in os.listdir(path):
            self.filenumber += 1
            _, file_format = os.path.splitext(filename)
            old_path_to_file = os.path.join(path, filename)
            new_path_to_file = os.path.join(path_destination, f"{new_filename}{file_format}")
            os.rename(old_path_to_file, new_path_to_file)
            print(f'HANDLED: [{old_path_to_file}] --> [{new_path_to_file}]')


event_handler = MyFileHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()
print()
print(f'WATCHING:\n-->{path}\n...')
observer.join()