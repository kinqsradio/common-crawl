import boto3
from save_to_db import fetch_and_save_warc

def list_first_robotstxt_file(bucket, prefix):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        if 'Contents' in page:
            for obj in page['Contents']:
                if '/robotstxt/' in obj['Key']:
                    return obj['Key']
        else:
            print(f"No contents found for prefix: {prefix}")
    return None


def list_and_process_robotstxt_files(bucket, prefix):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        if 'Contents' in page:
            for obj in page['Contents']:
                if '/robotstxt/' in obj['Key']:
                    print(f"Processing WARC file: {obj['Key']}")
                    fetch_and_save_warc(bucket, obj['Key'])
        else:
            print(f"No contents found for prefix: {prefix}")