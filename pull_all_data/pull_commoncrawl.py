import requests
import gzip
import io
from warcio.archiveiterator import ArchiveIterator

def fetch_warc_file(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    return response.raw

def extract_records(warc_stream):
    with gzip.GzipFile(fileobj=warc_stream) as f:
        for record in ArchiveIterator(f):
            if record.rec_type == 'response':
                url = record.rec_headers.get_header('WARC-Target-URI')
                content_type = record.http_headers.get_header('Content-Type')
                content = record.content_stream().read().decode('utf-8', errors='replace')
                yield url, content_type, content

if __name__ == "__main__":
    warc_url = 'https://data.commoncrawl.org/crawl-data/CC-MAIN-2018-17/segments/1524125937193.1/warc/CC-MAIN-20180420081400-20180420101400-00000.warc.gz'
    warc_stream = fetch_warc_file(warc_url)
    for url, content_type, content in extract_records(warc_stream):
        print(url, content_type, content[:200])  # Print the first 200 characters of content for preview
