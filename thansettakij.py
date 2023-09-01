import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import *
import sqlite3

def property():
    # ลิงก์ที่คุณต้องการดึงข้อมูล
    link_to_scrape = "https://www.thansettakij.com/category/real-estate"  # แทนที่ด้วยลิงก์ที่คุณต้องการดึงข้อมูล

    # ดึงเนื้อหาจากลิงก์
    response = requests.get(link_to_scrape)
    html_content = response.text

    # ตรวจสอบสถานะการเชื่อมต่อ 200 คือเชื่อมต่อสำเร็จ
    if response.status_code == 200:
        # สร้างตัวแปร BeautifulSoup เพื่อวิเคราะห์ HTML ของลิงก์
        soup = BeautifulSoup(html_content, "html.parser")

        tag_list = soup.find_all('a')
        selected_links = []

        # ตรวจสอบให้แน่ใจว่ามีลิงก์ตำแหน่งที่ 18 หรือไม่
        for i in range(8,13) :
            if i < len(tag_list):  # เนื่องจากเริ่มต้นนับที่ 0
                selected_links.append(tag_list[i].get("href"))
                
        return selected_links


def news():
    url_list = property()
    news_list = []  # สร้างลิสต์เพื่อเก็บข่าวทั้งหมด

    for idx, link in enumerate(url_list, start=1):
        url = f'https://www.thansettakij.com{link}'
        r = requests.get(url)
        r.text[:200]

        s = BeautifulSoup(r.text, 'lxml')

        d = s.find('div', {'class': 'detail'})

        p_tag = d.find_all('p')

        content = ''  # สร้างตัวแปรเพื่อเก็บเนื้อหาข่าว

        for i in p_tag:
            paragraph = i.get_text()
            paragraph = paragraph.replace('\n', '').replace('\xa0', '')
            content += paragraph

        
        news_list.append(content)

    return news_list


def news_time():

    news_list = []  # สร้างลิสต์เพื่อเก็บข้อมูลข่าวทั้งหมด

    for idx, link in enumerate(property(), start=1):
        url = f'https://www.thansettakij.com{link}'
        r = requests.get(url)
        r.text[:200]

        s = BeautifulSoup(r.text, 'lxml')

        d = s.find('div', {'class': 'date'})
        date_text = d.get_text(strip=True)

        news_list.append(date_text)

    return news_list


def title_news() :
    url_list = property()
    news_list = []  # สร้างลิสต์เพื่อเก็บข่าวทั้งหมด

    for idx, link in enumerate(url_list, start=1):
        url = f'https://www.thansettakij.com{link}'
        r = requests.get(url)
        r.text[:200]

        s = BeautifulSoup(r.text, 'lxml')

        d = s.find('div', {'class': 'card-title'})

        p_tag = d.find('h1')

        content = ''  # สร้างตัวแปรเพื่อเก็บเนื้อหาข่าว

        for i in p_tag:
            paragraph = i.get_text()
            paragraph = paragraph.replace('\n', '').replace('\xa0', '')
            content += paragraph

        
        news_list.append(content)

    return news_list

current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

data = {
    'date_news' : news_time(),
    'from_web' : 'ฐานเศรษกิจ',
    'Title_news' : title_news(),
    'content_news' : news(),
    'created_on' : current_datetime,
}

df = pd.DataFrame(data)

connection = sqlite3.connect(r'C:\thatsapon\database\SQLite\db_ThirdParty.db')
cursor = connection.cursor()

for index, row in df.iterrows():
    cursor.execute('''SELECT * FROM news_property WHERE date_news = ? AND content_news = ?''',
                   (row['date_news'], row['content_news']))
    existing_data = cursor.fetchall()

    if not existing_data:
        cursor.execute('''INSERT INTO news_property (date_news, from_web, Title_news, content_news, created_on) VALUES (?, ?, ?, ?, ?)''', 
                       (row['date_news'], row['from_web'], row['Title_news'], row['content_news'], row['created_on']))
        connection.commit()

connection.close()
