import boto3
from botocore.config import Config
from botocore.exceptions import ReadTimeoutError
import psycopg2
from warcio.archiveiterator import ArchiveIterator
from io import BytesIO
from bs4 import BeautifulSoup
import time

# Database connection parameters
DB_PARAMS = {
    'dbname': 'common_crawl_robot_txt',
    'user': 'anhdang',
    'password': '',
    'host': 'localhost',
    'port': '5433'
}

# Increase the timeout settings
config = Config(
    retries={
        'max_attempts': 10,
        'mode': 'standard'
    },
    connect_timeout=10,
    read_timeout=60
)

# Initialize S3 client with increased timeout settings
s3 = boto3.client('s3', config=config)

def save_to_db(url, content):
    # Remove null bytes from content
    content = content.replace('\x00', '')

    # Skip content that appears to be HTML as they are not robots.txt files
    if is_html(content):
        print(f"Skipping HTML content for URL: {url}")
        return
    
    # Remove excessive whitespace
    content = '\n'.join(line for line in content.splitlines() if line.strip())
    
    # Skip empty or blank content
    if not content.strip():
        print(f"Skipping empty or blank content for URL: {url}")
        return
    
    # Verify that the content is a robots.txt file
    if not is_robots_txt(content):
        print(f"Content does not appear to be a robots.txt file for URL: {url}")
        return

    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO robots_txt (url, content)
        VALUES (%s, %s)
    """, (url, content))
    conn.commit()
    cursor.close()
    conn.close()

def is_html(content):
    """Check if the content is HTML using BeautifulSoup."""
    soup = BeautifulSoup(content, "html.parser")
    return bool(soup.find())

def is_robots_txt(content):
    """Check if the content has typical robots.txt directives."""
    directives = ["User-agent", "Disallow", "Allow", "Sitemap"]
    for line in content.splitlines():
        if any(directive in line for directive in directives):
            return True
    return False

def fetch_and_save_warc(bucket, key):
    print(f"Processing WARC file: {key}")  # Print the WARC file being processed
    attempt = 0
    max_retries = 5
    while attempt < max_retries:
        try:
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
            break  # Exit the retry loop if successful
        except ReadTimeoutError:
            attempt += 1
            print(f"ReadTimeoutError on attempt {attempt} for WARC file: {key}. Retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff

    if attempt == max_retries:
        print(f"Failed to process WARC file: {key} after {max_retries} attempts")


if __name__ == "__main__":
    from pull_robot_txt import list_first_robotstxt_file
    
    bucket_name = 'commoncrawl'
    prefix = 'crawl-data/CC-MAIN-2024-26/segments/'
    first_warc_file = list_first_robotstxt_file(bucket_name, prefix)
    
    if first_warc_file:
        fetch_and_save_warc(bucket_name, first_warc_file)
    else:
        print("No WARC files found.")
