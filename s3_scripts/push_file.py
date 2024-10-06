"""Script for loading file from local repo to S3-storage.

Usage example:

`python s3_scripts/push_file.py --local-file-path=data/test.parquet --s3-file-path=recsys/test/test.parquet`
"""
import argparse
import os

from dotenv import load_dotenv

from yc_client import YandexCloudClient

parser = argparse.ArgumentParser()
parser.add_argument(
    "-lfp",
    "--local-file-path",
    help="Full path to the file to be uploaded",
)
parser.add_argument(
    "-sfp",
    "--s3-file-path",
    help="Full path to file to be uploaded in S3",
)
args = parser.parse_args()

if __name__ == "__main__":
    
    load_dotenv()

    client = YandexCloudClient(
        bucket_name=os.environ.get("S3_BUCKET_NAME"),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID_STUDENT'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY_STUDENT'),
    )

    client.upload_file(
        local_file_path=args.local_file_path,
        s3_file_path=args.s3_file_path,
    )
