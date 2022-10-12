import os


def delete_file(filepath):

    if not os.path.exists(filepath):
        return

    os.remove(path=filepath)
