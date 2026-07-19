import sqlite3  
import csv
import os
from dotenv import load_dotenv
load_dotenv()
import kaggle

# loaded environment variables
# call kaggle api to download sqlite db and unzip

kaggle.api.dataset_download_files('hugomathien/soccer', path='.', unzip=True)

database = 'database.sqlite' #database file to convert goes here

conn = sqlite3.connect(database)

cursor = conn.cursor()

# Get all table names in DB
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
rows = cursor.fetchall()

# Make CSV for each table for pandas when doing ML
for row in rows:
    print(row[0])
    cursor.execute(f"SELECT * FROM {row[0]}")
    rows = cursor.fetchall()
    headers = [description[0] for description in cursor.description]
    with open(f'{row[0]}.csv', 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

cursor.close()
conn.close()
