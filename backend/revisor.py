import multiprocessing
import os
import re
from flask import Flask, request, jsonify
import traceback

from werkzeug.utils import secure_filename

import file_utils
from aws_dynamodb_utils import AwsDynamoDbClient
from aws_s3_utils import AwsS3Client
from scan_status_monitor import scan_status_monitor
from utils import calculate_hash

app = Flask(__name__)
LOCAL_TEMP_FOLDER = "upload_files/"


@app.route('/upload-file', methods=['POST'])
def upload_file():

    # origin = request.headers.get('Origin', '*')
    try:
        if 'user_file' not in request.files:
            return jsonify({
                "code": -1004,
                "message": "File not present in the user request!"
            }), 400, {"Access-Control-Allow-Origin": '*'}

        file_to_uploaded = request.files['user_file']
        user_email = request.form.get('user_email')
        if not file_to_uploaded or not user_email:
            return jsonify({
                'code': -1000,
                'message': 'Invalid input!'
            }), 400, {"Access-Control-Allow-Origin": '*'}

        regex_email = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(regex_email, user_email):
            return jsonify({
                'code': -1002,
                'message': 'Invalid email input!'
            }), 400, {"Access-Control-Allow-Origin": '*'}

        ddb_client = AwsDynamoDbClient()
        s3_client = AwsS3Client()

        # uploaded_filename = secure_filename(file_to_uploaded.filename)
        uploaded_filename = str(file_to_uploaded.filename)
        file_to_uploaded.save(os.path.join(LOCAL_TEMP_FOLDER, uploaded_filename))
        file_path = LOCAL_TEMP_FOLDER + uploaded_filename
        sha256_digest = calculate_hash(file_path=file_path)

        file_size = file_utils.calculate_filesize(filepath=file_path)
        if not file_size or file_size > 31000000:
            return jsonify({
                'code': -1001,
                'message': 'File size limit exceeded. (Files with size less than 32 MB are allowed for scanning)'
            }), 400, {"Access-Control-Allow-Origin": '*'}

        # Rename the file to be uploaded to sha256 before uploading to S3
        file_path = LOCAL_TEMP_FOLDER + str(sha256_digest)
        os.rename(LOCAL_TEMP_FOLDER + str(uploaded_filename), file_path)

        if file_utils.create_zipfile(folder=LOCAL_TEMP_FOLDER, source_filename=str(uploaded_filename),
                                     zip_filename=str(sha256_digest) + ".zip", password="CY7900"):
            file_path = LOCAL_TEMP_FOLDER + str(sha256_digest) + ".zip"

        # Check if the file is already uploaded
        check_record = ddb_client.check_if_file_already_scanned(sha256=sha256_digest)
        if 'Item' not in check_record:
            s3_client.upload_file(file_path=file_path, name=str(sha256_digest) + "/" + str(sha256_digest))

            # After successful upload, delete it from local - Make it async later (Maybe have a cron job that runs periodically to delete all the files from the LOCAL_TEMP_PATH)
            file_utils.delete_file(filepath=file_path)

            # Create/Update the revisor_files table on dynamodb
            ddb_client.add_file(sha256=str(sha256_digest), user_email=user_email, filename=uploaded_filename)
            return jsonify({
                "code": 1004,
                "message": "File is successfully uploaded and sent for scanning"
            }), 200, {"Access-Control-Allow-Origin": '*'}

        else:
            # File already scanned
            # Delete it from local
            file_utils.delete_file(filepath=file_path)

            # Update the database
            if user_email and sha256_digest:
                ddb_client.update_email_status(sha256=sha256_digest, email_status=0)
                ddb_client.update_email_info(sha256=sha256_digest, email_id=user_email)
            else:
                raise Exception("Some error in processing - code: -1009")

            return jsonify({
                "code": 1004,
                "message": "File already in the database",
                "report": str(check_record['Item'])
            }), 200, {"Access-Control-Allow-Origin": '*'}

    except Exception as ex:

        traceback.print_exception(ex)  # Will remove it later - Needed for debugging
        return jsonify({
            "code": -1000,
            "message": "Error in uploading the file!" + str(ex)
        }), 400, {"Access-Control-Allow-Origin": '*'}


# Health check API
@app.route('/', methods=['GET'])
def test():

    # Start the scan status monitoring process, and keep it running as a separate process parallely
    scan_proc = multiprocessing.Process(target=scan_status_monitor)
    scan_proc.start()

    # origin = request.headers.get('Origin', '*')
    return jsonify({
        "code": 1000,
        "message": "Welcome to Revisor - The Next Generation AV Engine!"
    }), 200, {"Access-Control-Allow-Origin": '*'}


if __name__ == "__main__":

    # Create a temporary directory if not exists already
    if not os.path.exists(LOCAL_TEMP_FOLDER):
        os.mkdir(LOCAL_TEMP_FOLDER)

    port = int(os.environ.get('REVISOR_SERVER_PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
