import shutil
from random import randint
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent


path_monitoring = "D:/Users/user/Desktop/a"
path_destination = 'D:/Users/user/Desktop/b'


class MyFileHandler(FileSystemEventHandler):

    def on_modified(self, event:FileModifiedEvent):
        filename = Path(event.src_path).name
        if isinstance(event, FileModifiedEvent):
            try:
                shutil.move(event.src_path, path_destination)
                print(f"MOVED: [{event.src_path}] --> [{path_destination}/{filename}]")
            except (shutil.Error, FileExistsError):
                self.move_renamed_file(event)
        else: 
            print(f"UNEXPECTED EVENT: {event.src_path}=={event.event_type}!")

    def move_renamed_file(self, event:FileModifiedEvent):
        path = Path(event.src_path)
        fileformat = path.suffix
        new_filename = randint(0, 1000000)
        new_path_to_file = Path(path_destination).joinpath(f'{new_filename}{fileformat}')
        try:
            return path.rename(new_path_to_file), print(f'RENAMED AND MOVED: [{event.src_path}] --> [{new_path_to_file}]')
        except FileExistsError as err:
            print(str(err))
            print()
            print("Can't move file to a destination folder!")


event_handler = MyFileHandler()
observer = Observer()
observer.schedule(event_handler, path_monitoring, recursive=True)
observer.start()
print()
print(f'WATCHING:\n-->{path_monitoring}\n...')
observer.join()