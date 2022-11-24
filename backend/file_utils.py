import os
import pyminizip


def delete_file(filepath):

    if not os.path.exists(filepath):
        return

    os.remove(path=filepath)


def write_file(filename, path, content):

    if os.path.exists(f'{path}/{filename}'):
        return

    with open(f"{path}/{filename}", "w") as results_fp:
        results_fp.write(str(content))

    return f'{path}/{filename}'


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


def unzip_file(folder, zip_filename, password):

    if not os.path.exists(folder + "/" + zip_filename):
        return False

    compress_level = 9
    return pyminizip.uncompress(folder + "/" + zip_filename, password, folder, compress_level)


def calculate_filesize(filepath):

    if not os.path.exists(filepath):
        return False

    return os.path.getsize(filename=filepath)
