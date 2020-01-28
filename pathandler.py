import shutil
from typing import Union, Optional
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
def move_renamed_file(src_path: Union[str, Path], path_destination: Union[str, Path]):
    fileformat = Path(src_path).suffix
    new_filename = unique_filename(filenumber)
    new_path_to_file = Path(path_destination).joinpath(f"{new_filename}{fileformat}")
    return (
            shutil.move(src_path, new_path_to_file),
            print(f'RENAMED AND MOVED: [{src_path}] --> [{new_path_to_file}]')
            )


def move_to_folder(src_path: Union[str, Path], dst_path: Union[str, Path], folder_name: Optional[str]=None):
    if not folder_name is None:
        new_path_to_file = Path(dst_path).joinpath(folder_name)
        if not new_path_to_file.exists():
            new_path_to_file.mkdir(exist_ok=True)
        try:
            return (
                shutil.move(src_path, new_path_to_file),
                print(f"MOVED: [{src_path}] --> [{new_path_to_file}]")
            )
        except (shutil.Error, FileExistsError):
            return move_renamed_file(src_path, new_path_to_file)
    shutil.move(src_path, dst_path)