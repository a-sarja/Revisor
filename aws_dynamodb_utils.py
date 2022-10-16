import datetime

import boto3
from boto3.dynamodb.conditions import Key, Attr


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
                'scan_completed_timestamp': None,
                'email_status': 0
            }
        )

    def check_if_file_already_scanned(self, sha256):
        user_files_table = self.ddb_object.Table('revisor_files')
        return user_files_table.get_item(
            Key={
                'id': str(sha256)
            }, AttributesToGet=[
                'uploaded_timestamp', 'scan_completed_timestamp', 'report'
            ]
        )

    def signup_user(self, username, first_name, last_name, email, date_of_birth):
        users_table = self.ddb_object.Table('users')
        return users_table.put_item(
            Item={
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'date_of_birth': date_of_birth
            }
        )

    def check_scan_status(self):
        user_files_table = self.ddb_object.Table('revisor_files')
        response = user_files_table.scan(
            FilterExpression=Attr("scan_status").eq(2)
            # & Attr('email_status', 0)
        )
        if response:
            return response['Items']

    def update_email_status(self, sha256):
        user_files_table = self.ddb_object.Table('revisor_files')
        return
