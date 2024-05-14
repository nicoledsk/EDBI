import os
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description="file organiser")
parser.add_argument("--sort", action="store_true", help='enter "s" to sort files')
args = parser.parse_args()

SUBDIRECTORIES = {
    "DOCUMENTS": [".pdf", ".rtf", ".txt"],
    "AUDIO": [".m4a", ".m4b", ".mp3"],
    "VIDEOS": [".mov", ".MOV" ".avi", ".mp4"],
    "IMAGES": [".jpg", ".jpeg", ".png"],
}

if args.sort:

    def pickDirectory(value: str):
        """This function loops with the dictionary's items and returns the category in which the suffix exists.
        Args:
        Values (iterable): The values of the items in the dictionary represnted as a str.

        Returns:
        Folder based on file extension.

        """
        for category, suffixes in SUBDIRECTORIES.items():
            for suffix in suffixes:
                if suffix == value:
                    return category
                return "MISC"

    # Organising directory. For loop that loops through all the files. usin 'Path' to get file paths
    def organiseDirectory():
        """Loops through every item in the current working directory to get the file type, so we can properly organize it. Path is also pulled for each item so that we can move them.
        Calls function.

        """
        for item in os.scandir():
            if item.is_dir():
                continue
            filePath = Path(item)
            filetype = filePath.suffix.lower()
            directory = pickDirectory(filetype)
            directoryPath = Path(directory)
            if directoryPath.is_dir() != True:
                directoryPath.mkdir()
            filePath.rename(directoryPath.joinpath(filePath))

    organiseDirectory()
