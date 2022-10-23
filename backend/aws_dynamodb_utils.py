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

    def add_file(self, sha256):
        user_files_table = self.ddb_object.Table('revisor_files')
        return user_files_table.put_item(
            Item={
                'id': sha256,
                'uploaded_timestamp': str(datetime.datetime.now()),
                'scan_status': 0,
                'uploaded_by': 'sarja.a@northeastern.edu',  # This needs to be updated dynamically
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
                'uploaded_timestamp', 'scan_completed_timestamp', 'uploaded_by'
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

    def fetch_data_to_send_email(self):
        user_files_table = self.ddb_object.Table('revisor_files')
        response = user_files_table.scan(
            FilterExpression=Attr("scan_status").eq(2) & Attr('email_status').eq(0)
        )
        if response:
            return response['Items']

    def update_email_status(self, sha256):
        user_files_table = self.ddb_object.Table('revisor_files')
        return user_files_table.update_item(
            Key={
                'id': sha256
            },
            UpdateExpression="SET email_status=:e",
            ExpressionAttributeValues={
                ':e': 2
            },
            ReturnValues="UPDATED_NEW"
        )

    def update_scan_status(self, file_id, status):
        user_files_table = self.ddb_object.Table('revisor_files')

        return user_files_table.update_item(
            Key={'id': file_id},
            UpdateExpression="set scan_status = :s",
            ExpressionAttributeValues={
                ':s': status
            },
            ReturnValues="UPDATED_NEW"
        )

    def get_unscanned_files(self):
        user_files_table = self.ddb_object.Table('revisor_files')
        response = user_files_table.query(
            IndexName='scan_status-index',
            KeyConditionExpression=Key('scan_status').eq(0)
        )
        return response['Items']

    def get_file_details(self, sha256):
        user_files_table = self.ddb_object.Table('revisor_files')
        response = user_files_table.get_item(
            Key={
                'id': sha256
            }
        )
        return response['Item']
