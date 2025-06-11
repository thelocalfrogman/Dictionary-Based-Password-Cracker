# Authors:
#   William
#   George

#Prompts the user for the file containing the hashes, and the dictionary of words.

import os
from pathlib import Path

def whatpath():
    file_path = input("Please enter the file path: ")

    path = Path(file_path)
    if path.exists():
        print(f"The file path '{file_path}' is valid.")
        file_name = file_path
        file_extension = Path(file_name).suffix
        print(f"The file extension is: {file_extension}")
    else:
        print(f"The file path '{file_path}' does not exist. Please check and try again.")
        whatpath()

whatpath()
