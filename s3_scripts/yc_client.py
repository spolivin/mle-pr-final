"""Client for Yandex Cloud for basic actions with bucket."""
import boto3


class YandexCloudClient(object):
    """Class for interacting with Yandex Cloud bucket."""

    def __init__(
        self,
        bucket_name,
        aws_access_key_id,
        aws_secret_access_key,
        service_name="s3",
        endpoint_url="https://storage.yandexcloud.net",
    ):
        """Initializes a class instance."""
        # Setting class attributes
        self.bucket_name = bucket_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.service_name = service_name
        self.endpoint_url = endpoint_url

        # Creating a session object
        session = boto3.session.Session()
        self.s3_client = session.client(
            service_name=self.service_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    def check_storage_contents(self):
        """Displays the contents of a bucket."""
        if self.s3_client.list_objects(Bucket=self.bucket_name).get("Contents"):
            for key in self.s3_client.list_objects(Bucket=self.bucket_name)["Contents"]:
                print(key["Key"])

    def check_storage_space(self):
        """Displays the contents of a bucket with memory space."""
        files = []
        sizes = []
        if self.s3_client.list_objects(Bucket=self.bucket_name).get("Contents"):
            for key in self.s3_client.list_objects(Bucket=self.bucket_name)["Contents"]:
                cur_key = key["Key"]
                response = self.s3_client.head_object(
                    Bucket=self.bucket_name, Key=cur_key
                )
                cur_size = response["ContentLength"]
                cur_size_mb = cur_size / (1024**2)
                print(f"file {cur_key} => {cur_size} bytes ({cur_size_mb:.5f} MB)")
                files.append(cur_key)
                sizes.append(cur_size)

        # Computing and printing file sizes
        total_weight = sum(sizes)
        total_weight_gb = total_weight / (1024**3)
        print(
            f"\nTotal weight of all files in bucket = {total_weight} bytes ({total_weight_gb:.2f} GB)\n"
        )

    def download_file(self, s3_file_path, local_file_path):
        """Downloads file from S3-storage to local repository."""
        try:
            self.s3_client.download_file(
                self.bucket_name,
                s3_file_path,
                local_file_path,
            )
        except:
            print("Error occurred while downloading a file from S3")
        else:
            file_downloaded = s3_file_path.split("/")[-1]
            print(f"File '{file_downloaded}' has been downloaded successfully")

    def upload_file(self, local_file_path, s3_file_path):
        """Uploads file from local repository to S3-storage."""
        try:
            self.s3_client.upload_file(
                local_file_path,
                self.bucket_name,
                s3_file_path,
            )
        except:
            print("Error occurred while uploading a file to S3")
        else:
            file_uploaded = local_file_path.split("/")[-1]
            print(f"File '{file_uploaded}' has been uploaded successfully")
