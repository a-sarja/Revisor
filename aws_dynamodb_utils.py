import datetime

import boto3


class AwsDynamoDbClient:

    def __init__(self):
        self._aws_client = "dynamodb"
        self._region = "us-east-1"
        self.ddb_object = self.get_dynamodb_client()

    def get_dynamodb_client(self):
        return boto3.resource(self._aws_client, self._region)

    def update_files_table(self, s3_path, sha256):
        user_files_table = self.ddb_object.Table('revisor_files')
        return user_files_table.put_item(
            Item={
                'id': sha256,
                's3_url': s3_path,
                'uploaded_timestamp': str(datetime.datetime.now()),
                'scan_status': 0,
                'report': None,
                'uploaded_by': 'Test',
                'scan_completed_timestamp': None
            }
        )

    def check_if_file_already_scanned(self, sha256):
        user_files_table = self.ddb_object.Table('revisor_files')
        return user_files_table.get_item(
            Key={
                'id': str(sha256)
            }, AttributesToGet=[
                'uploaded_date', 'scanned_date', 'report'
            ]
        )
