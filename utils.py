import hashlib


def calculate_hash(file_path):

    BUF_SIZE = 65536  # let's read stuff in 64kb chunks!
    sha256 = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break

            sha256.update(data)

            return sha256.hexdigest()
