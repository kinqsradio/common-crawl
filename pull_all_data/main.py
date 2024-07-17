from pull_commoncrawl import fetch_warc_file, extract_records
from save_to_db import save_to_db
from create_db import create_database, create_table, list_tables

if __name__ == "__main__":
    # Recreate the database and table
    create_database()
    create_table()
    list_tables()

    warc_url = 'https://data.commoncrawl.org/crawl-data/CC-MAIN-2018-17/segments/1524125937193.1/warc/CC-MAIN-20180420081400-20180420101400-00000.warc.gz'
    warc_stream = fetch_warc_file(warc_url)
    for url, content_type, content in extract_records(warc_stream):
        print(f"Saving {url} with content type {content_type}")
        save_to_db(url, content_type, content)
