"""Script for checking the storage/space of a bucket.

Usage examples:

    - Checking storage contents
        `python s3_scripts/check_storage.py --option=contents`

    - Checking storage space
        `python s3_scripts/check_storage.py --option=space`
"""
import argparse
import os

from dotenv import load_dotenv

from yc_client import YandexCloudClient

# Enumerating options to use as argument values
OPTION_CONTENTS = "contents"
OPTION_SPACE = "space"

# Help message for arguments
HELP_MSG = f"Available options: ['{OPTION_CONTENTS}', '{OPTION_SPACE}']"

# Creating arguments for script
parser = argparse.ArgumentParser()
parser.add_argument(
    "-o",
    "--option",
    help="Option to check bucket contents or contents with space." + f"\n{HELP_MSG}"
)
args = parser.parse_args()

if __name__ == '__main__':

    # Loading environmental variables
    load_dotenv()
    # Instantiating a client
    client = YandexCloudClient(
        bucket_name=os.environ.get("S3_BUCKET_NAME"),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID_STUDENT'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY_STUDENT'),
    )

    if args.option == OPTION_CONTENTS:
        client.check_storage_contents()
    elif args.option == OPTION_SPACE:
        client.check_storage_space()
    else:
        if args.option is None:
            print("No options specified" + f"\n{HELP_MSG}")
        else:
            print(f"Option '{args.option}' is invalid" + f"\n{HELP_MSG}")
