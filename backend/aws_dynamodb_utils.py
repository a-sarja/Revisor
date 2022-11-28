import datetime

import boto3
from boto3.dynamodb.conditions import Attr


class AwsDynamoDbClient:

    def __init__(self):
        self._aws_client = "dynamodb"
        self._region = "us-east-2"
        self.ddb_object = self.get_dynamodb_client()

    def get_dynamodb_client(self):
        return boto3.resource(self._aws_client, self._region)

    def add_file(self, sha256, user_email, filename):
        user_files_table = self.ddb_object.Table('revisor_files')
        return user_files_table.put_item(
            Item={
                'id': sha256,
                'file_name': filename,
                'uploaded_timestamp': str(datetime.datetime.now()),
                'scan_status': 0,
                'clamav_scan_status': 0,
                'yara_av_scan_status': 0,
                'uploaded_by': str(user_email),
                'email_status': 0
            }
        )

    def check_if_file_already_scanned(self, sha256):
        user_files_table = self.ddb_object.Table('revisor_files')
        return user_files_table.get_item(
            Key={
                'id': str(sha256)
            }, AttributesToGet=[
                'uploaded_timestamp', 'uploaded_by'
            ]
        )

    def fetch_data_to_send_email(self):
        user_files_table = self.ddb_object.Table('revisor_files')
        response = user_files_table.scan(
            FilterExpression=Attr("scan_status").eq(2) & Attr("yara_av_scan_status").eq(2) & Attr("clamav_scan_status").eq(2) & Attr('email_status').eq(0)
        )
        if response:
            return response['Items']

    def update_email_status(self, sha256, email_status):
        user_files_table = self.ddb_object.Table('revisor_files')
        return user_files_table.update_item(
            Key={
                'id': sha256
            },
            UpdateExpression="SET email_status=:e",
            ExpressionAttributeValues={
                ':e': email_status
            },
            ReturnValues="UPDATED_NEW"
        )

    def update_email_info(self, sha256, email_id):
        user_files_table = self.ddb_object.Table('revisor_files')
        return user_files_table.update_item(
            Key={
                'id': sha256
            },
            UpdateExpression="SET uploaded_by=:e",
            ExpressionAttributeValues={
                ':e': email_id
            },
            ReturnValues="UPDATED_NEW"
        )

    def update_scan_status(self, file_id, status, scan_engine):
        key_condition_column = 'scan_status'
        if scan_engine.lower() == 'clamav':
            key_condition_column = 'clamav_scan_status'
        elif scan_engine.lower() == 'yara_av':
            key_condition_column = 'yara_av_scan_status'

        user_files_table = self.ddb_object.Table('revisor_files')

        return user_files_table.update_item(
            Key={'id': file_id},
            UpdateExpression="set " + str(key_condition_column) + " = :s",
            ExpressionAttributeValues={
                ':s': status
            },
            ReturnValues="UPDATED_NEW"
        )

    def get_unscanned_files(self, scan_engine):
        key_condition_column = 'scan_status'
        if scan_engine.lower() == 'clamav':
            key_condition_column = 'clamav_scan_status'
        elif scan_engine.lower() == 'yara_av':
            key_condition_column = 'yara_av_scan_status'

        user_files_table = self.ddb_object.Table('revisor_files')
        response = user_files_table.scan(
            FilterExpression=Attr(key_condition_column).eq(0)
        )
        if response:
            return response['Items']

    def get_file_details(self, sha256):
        user_files_table = self.ddb_object.Table('revisor_files')
        response = user_files_table.get_item(
            Key={
                'id': sha256
            }
        )
        return response['Item']
