import shutil
from datetime import datetime
from pathlib import Path


#for numbering a files which have same names 
filenumber = [0,]


#giving a file unique name with date and number of the file
def unique_filename(filenumber: list):
    number = filenumber.pop()
    filenumber.append(number + 1)
    new_filename = datetime.strftime(datetime.now(), 
                                    f"%d.%m.%Y_(%H-%M-%S)_FILENUMBER={filenumber[0]}")
    return new_filename


#if file in destination folder have same name as event file, 
#func will rename it and move to the destination folder
def move_renamed_file(src_path: str, path_destination: str):
    path = Path(src_path)
    fileformat = path.suffix
    new_filename = unique_filename(filenumber)
    new_path_to_file = Path(path_destination).joinpath(f"{new_filename}{fileformat}")
    return (
            shutil.move(src_path, new_path_to_file),
            print(f'RENAMED AND MOVED: [{src_path}] --> [{new_path_to_file}]')
            )


#checking if event file have image's format if True,
#folder for images will created and event file will moved to created folder
def move_to_image_dir(src_path: str, path_destination: str, img_formats: list, temporary_formats: list):
    path = Path(src_path)
    filename, fileformat = path.name, path.suffix
    if not fileformat in temporary_formats:
        if fileformat in img_formats:
            new_path_to_file = Path(path_destination).joinpath('Images')
            new_path_to_file.mkdir(exist_ok=True)
            try:
                return (
                    shutil.move(src_path, new_path_to_file),
                    print(f"MOVED: [{src_path}] --> [{new_path_to_file}/{filename}]")
                    )
            except (shutil.Error, FileExistsError):
                return move_renamed_file(src_path, str(new_path_to_file))
        else:
            new_path_to_file = Path(path_destination).joinpath(fileformat.upper())
            new_path_to_file.mkdir(exist_ok=True)
            try:
                return (
                    shutil.move(src_path, new_path_to_file),
                    print(f"MOVED: [{src_path}] --> [{path_destination}/{filename}]")
                    )
            except (shutil.Error, FileExistsError):
                return move_renamed_file(src_path, str(new_path_to_file))
