import json
import os
from flask import Flask, request, jsonify
import traceback

import file_utils
from aws_dynamodb_utils import AwsDynamoDbClient
from aws_s3_utils import AwsS3Client
from utils import calculate_hash


app = Flask(__name__)
LOCAL_TEMP_FOLDER = "/home/abhiram/Desktop/CY7900/upload_files/"  # Change it to the /tmp/<revisor> in prod environment


@app.route('/upload-file', methods=['POST'])
def upload_file():

    if 'user_file' not in request.files:
        return jsonify({
            "code": -1004,
            "message": "File not present in the user request!"
        }), 400

    try:
        ddb_client = AwsDynamoDbClient()
        s3_client = AwsS3Client()

        file_to_uploaded = request.files['user_file']
        file_to_uploaded.save(os.path.join(LOCAL_TEMP_FOLDER, file_to_uploaded.filename))
        file_path = LOCAL_TEMP_FOLDER + str(file_to_uploaded.filename)
        sha256_digest = calculate_hash(file_path=file_path)

        # Rename the file to be uploaded to sha256 before uploading to S3
        file_path = LOCAL_TEMP_FOLDER + str(sha256_digest)
        os.rename(LOCAL_TEMP_FOLDER + str(file_to_uploaded.filename), file_path)

        if file_utils.create_zipfile(folder=LOCAL_TEMP_FOLDER, source_filename=str(file_to_uploaded.filename), zip_filename=str(sha256_digest) + ".zip", password="CY7900"):
            file_path = LOCAL_TEMP_FOLDER + str(sha256_digest) + ".zip"

        # Check if the file is already uploaded
        check_record = ddb_client.check_if_file_already_scanned(sha256=sha256_digest)
        if 'Item' not in check_record:
            s3_client.upload_file(file_path=file_path, name=str(sha256_digest) + "/" + str(sha256_digest))

            # After successful upload, delete it from local - Make it async later (Maybe have a cron job that runs periodically to delete all the files from the LOCAL_TEMP_PATH)
            file_utils.delete_file(filepath=file_path)

            # Create/Update the revisor_files table on dynamodb
            ddb_client.add_file(sha256=str(sha256_digest))
            return jsonify({
                "code": 1004,
                "message": "File is successfully uploaded and sent for scanning"
            }), 200

        else:
            # File already scanned
            return jsonify({
                "code": 1004,
                "message": "File already in the database",
                "report": str(check_record['Item'])
            }), 200

    except Exception as ex:

        traceback.print_exception(ex)  # Will remove it later - Needed for debugging
        return jsonify({
            "code": -1000,
            "message": "Error in uploading the file!" + str(ex)
        }), 400


@app.route('/login', methods=['POST'])
def login():
    return jsonify({
        "code": 1000,
        "message": "Welcome to Revisor - The Next Generation AV Engine!"
    }), 200


@app.route('/register', methods=['POST'])
def signup():

    if request.method == "POST":
        input_data = json.loads(request.get_data().decode().strip())

        username = input_data['username']
        first_name = input_data['firstName']
        last_name = input_data['lastName']
        email = input_data['email']
        date_of_birth = input_data['dateOfBirth']

        if not username or not first_name or not last_name or not email or not date_of_birth:
            return jsonify({
                "code": -1001,
                "message": "Invalid inputs"
            }), 400

    return jsonify({
        "code": 1000,
        "message": "Welcome to Revisor - The Next Generation AV Engine!"
    }), 200


@app.route('/', methods=['GET'])
def test():
    return jsonify({
        "code": 1000,
        "message": "Welcome to Revisor - The Next Generation AV Engine!"
    }), 200


if __name__ == "__main__":

    port = int(os.environ.get('REVISOR_SERVER_PORT', 5000))
    app.run(debug=True, host='127.0.0.1', port=port)
