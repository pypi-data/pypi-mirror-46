import boto3

class S3Utiltiy():

    def __init__(self):
        self.client = None
        print("Successful")


    def configure(self, access_key, secret_key):
        self.client = boto3.client(
            aws_access_key_id = access_key,
            aws_secret_access_key = secret_key,
            service_name = "s3"
        )

    def get_buckets(self):
        response = self.client.list_bucket()
        print(response)
        return response