import os
import boto3 as boto3
from flask import Flask, request, jsonify
import traceback

import file_utils
from utils import calculate_hash


app = Flask(__name__)
LOCAL_TEMP_FOLDER = "/home/abhiram/Desktop/CY7900/upload_files/"  # Change it to the /tmp/<revisor> in prod environment


class AwsClient:

    def __init__(self):
        self._aws_client = "s3"
        self._bucket_name = "revisorfiles"

    def get_s3_client(self):
        return boto3.resource(self._aws_client)

    def upload_file(self, file_path, name):
        s3_object = self.get_s3_client()
        return s3_object.meta.client.upload_file(file_path, self._bucket_name, name)


@app.route('/upload-file', methods=['POST'])
def upload_file():

    if 'user_file' not in request.files:
        return jsonify({
            "code": -1004,
            "message": "File not present in the user request!"
        }), 400

    try:
        file_to_uploaded = request.files['user_file']
        file_to_uploaded.save(os.path.join(LOCAL_TEMP_FOLDER, file_to_uploaded.filename))
        file_path = LOCAL_TEMP_FOLDER + str(file_to_uploaded.filename)
        sha256_digest = calculate_hash(file_path=file_path)

        aws_client = AwsClient()
        aws_client.upload_file(file_path=file_path, name=str(sha256_digest))

        # After successful upload, delete it from local - Make it async later (Maybe have a cron job that runs periodically to delete all the files from the LOCAL_TEMP_PATH)
        file_utils.delete_file(filepath=file_path)

        return jsonify({
            "code": 1004,
            "message": "File is successfully uploaded and sent for scanning"
        }), 200

    except Exception as ex:

        traceback.print_exception(ex)
        return jsonify({
            "code": -1000,
            "message": "Error in uploading the file!" + str(ex)
        }), 400


@app.route('/login', methods=['POST'])
def login():
    return {
        "code": 1000,
        "message": "Welcome to Revisor - The Next Generation AV Engine!"
    }


@app.route('/', methods=['GET'])
def test():
    return {
        "code": 1000,
        "message": "Welcome to Revisor - The Next Generation AV Engine!"
    }


if __name__ == "__main__":

    port = int(os.environ.get('REVISOR_SERVER_PORT', 5000))
    app.run(debug=True, host='127.0.0.1', port=port)
