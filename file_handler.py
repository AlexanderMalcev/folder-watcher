import os
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


path = "D:/Users/user/Desktop/a"
path_destination = 'D:/Users/user/Desktop/b'


class MyFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        new_filename = datetime.strftime(datetime.now(), "%d.%m.%Y in %H-%M-%S")
        for filename in os.listdir(path):
            file_exist = os.path.isfile(f"{path_destination}/{new_filename}")
            _, file_format = os.path.splitext(filename)
            if not file_exist:
                old_path_to_file = os.path.join(path, filename)
                new_path_to_file = os.path.join(path_destination, f"{new_filename}{file_format}")
                print(f'HANDLED: {os.rename(old_path_to_file, new_path_to_file)} --> {os.listdir(path_destination)[-1]}')


event_handler = MyFileHandler()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()
print()
print(f'HANDLING:\n-->{path} \n...')


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

