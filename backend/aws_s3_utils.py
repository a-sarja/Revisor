import boto3


class AwsS3Client:

    def __init__(self):
        self._aws_client = "s3"
        self._bucket_name = "revisorfiles"
        self.s3_object = self.get_s3_client()

    def get_s3_client(self):
        return boto3.resource(self._aws_client)

    def upload_file(self, file_path, name):
        return self.s3_object.meta.client.upload_file(file_path, self._bucket_name, name)

    def download_file(self, s3_file_name, local_file_name):
        return self.s3_object.meta.client.download_file(self.bucket_name, s3_file_name, local_file_name)

    @property
    def bucket_name(self):
        return self._bucket_name
