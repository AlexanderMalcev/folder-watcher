from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from pathandler import move_to_folder


path_monitoring = "D:/Users/user/Desktop/a"
path_destination = 'D:/Users/user/Desktop/b'


temporary_formats = [
    '.tmp', '.crdownload', 
    '.partial', '.opdownload',
    ]


img_formats = [
    '.jpg', '.jpeg', '.png', '.svg',
    '.gif', '.tiff', '.bmp', '.raw',
    '.psd',
]


class MyFileHandler(FileSystemEventHandler):

    def on_modified(self, event: FileModifiedEvent):
        fileformat = Path(event.src_path).suffix
        if isinstance(event, FileModifiedEvent):
            try:
                if not fileformat in temporary_formats:
                    if fileformat in img_formats:
                        move_to_folder(event.src_path, path_destination, folder_name="Images")
                    else:
                        move_to_folder(event.src_path, path_destination, folder_name=fileformat.upper())
            except FileNotFoundError:
                #I have found that on_modified events can 'fire' twice for the same file.
                #I solved this with just pass the exception
                pass
        else: 
            print(f"UNEXPECTED EVENT: {event.src_path}=={event.event_type}!")


event_handler = MyFileHandler()
observer = Observer()
observer.schedule(event_handler, path_monitoring)
observer.start()
print()
print(f'WATCHING:\n-->{path_monitoring}\n...')
observer.join()