import os
import boto3
from warcio.archiveiterator import ArchiveIterator

# Ensure the directory exists
download_dir = 'file'
os.makedirs(download_dir, exist_ok=True)

s3 = boto3.client('s3')

bucket_name = 'commoncrawl'
prefix = 'crawl-data/CC-MAIN-2018-17/segments/1524125937193.1/wet/'

# List objects within the prefix
response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

# Download and parse each WARC file
for obj in response.get('Contents', []):
    key = obj['Key']
    filename = os.path.join(download_dir, key.split('/')[-1])
    print(f'Downloading {filename}')
    s3.download_file(bucket_name, key, filename)

print(f"All files have been downloaded and saved to the '{download_dir}' directory.")
