import os
from pathlib import Path
curDir = os.getcwd()
print(curDir)
SUBDIRECTORIES = {
    "DOCUMENTS": ['.pdf', '.rtf', '.txt'],
    "AUDIO": ['.m4a', '.m4b', '.mp3'],
    "VIDEOS": ['.mov', '.avi', '.mp4'],
    "IMAGES": ['.jpg', '.jpeg', '.png']
}
def pickDirectory(value):
    for category, suffixes in SUBDIRECTORIES.items():
        for suffix in suffixes:
            if suffix == value:
                return category
            return 'MISC'
print(pickDirectory('.pdf'))
def organiseDirectory():
    for item in os.scandir():
        filePath = Path(item)
        filetype = filePath.suffix.lower()
        directory = pickDirectory(filetype)
        directoryPath = Path(directory)
        if directoryPath.is_dir() != True:
            directoryPath.mkdir()
        filePath.rename(directoryPath.joinpath(filePath))