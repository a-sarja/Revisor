import os
import pyminizip


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


def create_zipfile(folder, source_filename, zip_filename, password):

    if not os.path.exists(folder + "/" + source_filename):
        return False

    compress_level = 9
    pyminizip.compress(folder + "/" + source_filename, None, folder + "/" + zip_filename, password, compress_level)

    # Delete the source file after zipping
    delete_file(filepath=folder + "/" + source_filename)

    return True


def unzip_file(folder, target_filename, zip_filename, password):

    if not os.path.exists(folder + "/" + zip_filename):
        return False

    compress_level = 9
    pyminizip.uncompress(folder + "/" + zip_filename, password, target_filename, compress_level)

    return True
