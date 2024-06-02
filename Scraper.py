import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

base_url = "https://eksisozluk.com/eksi-itiraf--1037199?p="

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}

entries = []
page_number = 1

while True:
    url = base_url + str(page_number)
    print(f"Fetching data from page {page_number}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        tittle = soup.find('span', itemprop='name')
        if tittle:
            tittle_text = tittle.text.strip()

        for entry in soup.find_all('li', {'data-id': True}):
            content = entry.find('div', class_='content')
            if content:
                content_text = content.text.strip()
  
            date = entry.find('a', class_='entry-date permalink')
            if date:
                date_text = date.text.strip()
            
            username = entry.find('a', class_='entry-author')
            if username:
                username_text = username.text.strip()

                entries.append([tittle_text, content_text, date_text, username_text])
                print(f"Entry found on page {page_number}: Tittle: {tittle_text}, Date: {date_text}, Username: {username_text}, Content: {content_text[:30]}...")  
            
        page_number += 1
    else:
        print(f"Page {page_number} couldn't be fetched: {response.status_code}")
        break

if not entries:
    print("No entries found on any of the pages.")
else:
    df = pd.DataFrame(entries, columns=['Tittle', 'Content', 'Date', 'Username'])

    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, '%d.%m.%Y %H:%M')
        except ValueError:
            try:
                date_range = date_str.split(' ~ ')
                return datetime.strptime(date_range[0], '%d.%m.%Y %H:%M')
            except ValueError:
                return None

    df['Date'] = df['Date'].apply(parse_date)

    print("DataFrame content:")
    print(df.head())

    df.to_csv('eksiDB.csv', index=False)
    print("Data has been successfully fetched and saved to 'eksiDB.csv' file.")
