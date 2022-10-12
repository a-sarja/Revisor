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

        # Check if the file is already uploaded
        check_record = ddb_client.check_if_file_already_scanned(sha256=sha256_digest)

        if 'Item' not in check_record:
            s3_client.upload_file(file_path=file_path, name=str(sha256_digest))

            # After successful upload, delete it from local - Make it async later (Maybe have a cron job that runs periodically to delete all the files from the LOCAL_TEMP_PATH)
            file_utils.delete_file(filepath=file_path)

            s3_path = "https://" + str(s3_client.bucket_name) + ".s3.amazonaws.com/" + str(sha256_digest).lower()

            # Create/Update the revisor_files table on dynamodb
            ddb_client.update_files_table(s3_path=s3_path, sha256=str(sha256_digest))

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


@app.route('/', methods=['GET'])
def test():
    return jsonify({
        "code": 1000,
        "message": "Welcome to Revisor - The Next Generation AV Engine!"
    }), 200


if __name__ == "__main__":

    port = int(os.environ.get('REVISOR_SERVER_PORT', 5000))
    app.run(debug=True, host='127.0.0.1', port=port)
