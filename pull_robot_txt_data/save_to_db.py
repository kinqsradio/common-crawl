import boto3
import psycopg2
from warcio.archiveiterator import ArchiveIterator
from io import BytesIO

# Database connection parameters
DB_PARAMS = {
    'dbname': 'common_crawl_robot_txt',
    'user': 'anhdang',
    'password': '',
    'host': 'localhost',
    'port': '5433'
}

# Initialize S3 client
s3 = boto3.client('s3')

def save_to_db(url, content):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO robots_txt (url, content)
        VALUES (%s, %s)
    """, (url, content))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_and_save_warc(bucket, key):
    print(f"Processing WARC file: {key}")  # Print the WARC file being processed
    response = s3.get_object(Bucket=bucket, Key=key)
    with BytesIO(response['Body'].read()) as warc_stream:
        for record in ArchiveIterator(warc_stream):
            if record.rec_type == 'response' and 'robots.txt' in record.rec_headers.get_header('WARC-Target-URI'):
                url = record.rec_headers.get_header('WARC-Target-URI')
                try:
                    content = record.content_stream().read().decode('utf-8')
                except UnicodeDecodeError:
                    print(f"UnicodeDecodeError for URL: {url}. Skipping this record.")
                    continue
                
                print(f"Saving robots.txt from URL: {url}")  # Print the URL of the robots.txt being saved
                save_to_db(url, content)
                print(f"Saved robots.txt from {url}")

if __name__ == "__main__":
    from pull_robot_txt import list_first_robotstxt_file
    
    bucket_name = 'commoncrawl'
    prefix = 'crawl-data/CC-MAIN-2024-26/segments/'
    first_warc_file = list_first_robotstxt_file(bucket_name, prefix)
    
    if first_warc_file:
        fetch_and_save_warc(bucket_name, first_warc_file)
    else:
        print("No WARC files found.")
