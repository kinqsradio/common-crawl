from pull_robot_txt import list_first_robotstxt_file, list_robotstxt_files
from save_to_db import fetch_and_save_warc
from create_db import create_database, create_table, list_tables

if __name__ == "__main__":
    # Recreate the database and table
    create_database()
    create_table()
    list_tables()
    
    bucket_name = 'commoncrawl'
    prefix = 'crawl-data/CC-MAIN-2024-26/segments/'
    # warc_files = list_robotstxt_files(bucket_name, prefix)
    # for warc_file in warc_files:
    #     fetch_and_save_warc(bucket_name, warc_file)
    
    first_warc_file = list_first_robotstxt_file(bucket_name, prefix)
    if first_warc_file:
        fetch_and_save_warc(bucket_name, first_warc_file)
    else:
        print("No WARC files found.")

    
    
