import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from pathandler import move_renamed_file, move_to_image_dir


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
        # path = Path(event.src_path)
        # filename, fileformat = path.name, path.suffix
        if isinstance(event, FileModifiedEvent):
            try:
                # if not fileformat in temporary_formats:
                    # try:
                        move_to_image_dir(event.src_path, path_destination, img_formats, temporary_formats)
                    # except (FileExistsError, shutil.Error):
                    #     move_renamed_file(event.src_path, path_destination)
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