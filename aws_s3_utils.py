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

    def download_file(self, file_path, name):
        remote_csv_filename = name + "/" + str(name) + "_results.csv"
        remote_summary_filename = name + "/" + str(name) + "_summary.txt"
        csv_local = file_path + str(name) + "_results.csv"
        summary_local = file_path + str(name) + "_summary.txt"

        # Downloading the results and summary files from s3
        self.s3_object.meta.client.download_file(self._bucket_name, remote_csv_filename, csv_local)
        self.s3_object.meta.client.download_file(self._bucket_name, remote_summary_filename, summary_local)

        return csv_local, summary_local

    @property
    def bucket_name(self):
        return self._bucket_name
