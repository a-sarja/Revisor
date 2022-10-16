import os


def delete_file(filepath):

    if not os.path.exists(filepath):
        return

    os.remove(path=filepath)


def read_file(filepath):
    if not os.path.exists(filepath):
        return None

    with open(filepath, "rb") as file:
        file_content = file.read()

    return file_content
