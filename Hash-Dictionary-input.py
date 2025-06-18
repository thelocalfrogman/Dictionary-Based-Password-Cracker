# Authors:
#   William
#   George

#Prompts the user for the file containing the hashes, and the dictionary of words.

from pathlib import Path

file_path = 'a'
dic_path = 'a'

def whathash(file_path):
    file_path = input("Please enter the hashes file path: ")

    path = Path(file_path)
    if path.exists():
        print(f"The file path '{file_path}' is valid.")
        file_name = file_path
        file_extension = Path(file_name).suffix
        print(f"The file extension is: {file_extension}")
        return file_path
    else:
        print(f"The file path '{file_path}' does not exist. Please check and try again.")
        whathash()

def whatdic(dic_path):
    dic_path = input("Please enter the dictionary file path: ")

    path = Path(dic_path)
    if path.exists():
        print(f"The file path '{dic_path}' is valid.")
        file_name = dic_path
        file_extension = Path(file_name).suffix
        print(f"The file extension is: {file_extension}")
        return dic_path
    else:
        print(f"The file path '{dic_path}' does not exist. Please check and try again.")
        whatdic()

file_path = whathash(file_path)
dic_path = whatdic(dic_path)