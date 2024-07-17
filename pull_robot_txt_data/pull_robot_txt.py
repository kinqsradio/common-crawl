import boto3

def list_first_robotstxt_file(bucket, prefix):
    s3 = boto3.client('s3')
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        if 'Contents' in page:
            for obj in page['Contents']:
                if '/robotstxt/' in obj['Key']:
                    return obj['Key']  # Return the first file found
        else:
            print(f"No contents found for prefix: {prefix}")
    return None

def list_robotstxt_files(bucket, prefix):
    s3 = boto3.client('s3')
    warc_files = []
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        if 'Contents' in page:
            for obj in page['Contents']:
                if '/robotstxt/' in obj['Key']:
                    warc_files.append(obj['Key'])
        else:
            print(f"No contents found for prefix: {prefix}")
    return warc_files

if __name__ == "__main__":
    bucket_name = 'commoncrawl'
    prefix = 'crawl-data/CC-MAIN-2024-26/segments/'
    warc_files = list_robotstxt_files(bucket_name, prefix)
    if warc_files:
        for warc_file in warc_files:
            print(warc_file)
    else:
        print("No WARC files found.")
