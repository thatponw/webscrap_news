import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import *
import sqlite3

def property():
    # ลิงก์ที่คุณต้องการดึงข้อมูล
    link_to_scrape = "https://news.trueid.net/property"  # แทนที่ด้วยลิงก์ที่คุณต้องการดึงข้อมูล

    # ดึงเนื้อหาจากลิงก์
    response = requests.get(link_to_scrape)
    html_content = response.text

    # ตรวจสอบสถานะการเชื่อมต่อ 200 คือเชื่อมต่อสำเร็จ
    if response.status_code == 200:
        # สร้างตัวแปร BeautifulSoup เพื่อวิเคราะห์ HTML ของลิงก์
        soup = BeautifulSoup(html_content, "html.parser")

        # ตัวอย่างการดึงข้อมูลจากลิงก์
        # ข้อมูลที่ต้องการอาจแตกต่างกันขึ้นอยู่กับโครงสร้าง HTML ของลิงก์นั้น ๆ
        # ในตัวอย่างนี้เราจะดึงลิงก์ที่อยู่ในตำแหน่งที่ 17 ของรายการลิงก์ทั้งหมดที่อยู่ในแท็ก <a>
        links = soup.find_all("a")
        selected_links = []

        # ตรวจสอบให้แน่ใจว่ามีลิงก์ตำแหน่งที่ 18 หรือไม่
        for i in range(1, len(links)):  # ตรวจสอบลิงก์ในช่วง 1-49
            if i < len(links):  # ตรวจสอบว่ามีลิงก์ในตำแหน่งที่ i
                link = links[i].get("href")
                if link.startswith("/detail/"):
                    selected_links.append(link)
    
    return selected_links[::2]
            

def news():
    url_list = property()
    news_list = []  # สร้างลิสต์เพื่อเก็บข่าวทั้งหมด

    for idx, link in enumerate(url_list, start=1):
        url = f'https://news.trueid.net{link}'
        r = requests.get(url)
        r.text[:200]

        s = BeautifulSoup(r.text, 'lxml')

        d = s.find('section', {'class': 'style__ContentDetailBox-sc-150i3lj-0 style-sc-150i3lj-1 cfsjBk fIDjqN'})

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
        url = f'https://news.trueid.net{link}'
        r = requests.get(url)
        r.text[:200]

        s = BeautifulSoup(r.text, 'lxml')

        d = s.find('span', {'class': 'text'})
        date_text = d.get_text(strip=True).replace('(', '').replace(')', '')

        news_list.append(date_text)

    return news_list  # คืนค่าลิสต์ข้อมูลข่าวทั้งหมด


def convert_k_to_int(k_str):
    # ตรวจสอบว่าสตริง k_str มี 'K' หรือไม่
    if 'K' in k_str:
        # ตัดออกตัวอักษร 'K' และแปลงค่าเป็นทศนิยม
        k_str = k_str.replace('K', '')
        float_value = float(k_str)
        # แปลงเป็นจำนวนเต็ม (โดยการคูณด้วย 1000)
        int_value = int(float_value * 1000)
        return int_value
    else:
        # ถ้าไม่มี 'K' ในสตริง แปลงเป็นจำนวนเต็มโดยตรง
        return int(k_str)


def news_views():

    news_list = []  # สร้างลิสต์เพื่อเก็บข้อมูลข่าวทั้งหมด

    for idx, link in enumerate(property(), start=1):
        url = f'https://news.trueid.net{link}'
        r = requests.get(url)
        r.text[:200]

        s = BeautifulSoup(r.text, 'lxml')

        # ใช้ find_all เพื่อหาทุกอิลิเมนต์ <span> ที่ตรงตามเงื่อนไข
        spans = s.find_all('span', {'class': 'text'})
        
        # ตรวจสอบว่ามีตำแหน่งที่สองหรือไม่
        if spans:
            views_text = spans[1].get_text(strip=True)
            # ใช้ convert_k_to_int() เพื่อแปลงข้อมูล
            news_list.append(convert_k_to_int(views_text))
        else:
            news_list.append(None)

    return news_list[::1]  # คืนค่าลิสต์ข้อมูลข่าวทั้งหมด


def title_news() :

    url_list = property()
    news_list = []  # สร้างลิสต์เพื่อเก็บข่าวทั้งหมด

    for idx, link in enumerate(url_list, start=1):
        url = f'https://news.trueid.net{link}'
        r = requests.get(url)
        r.text[:200]

        s = BeautifulSoup(r.text, 'lxml')

        p_tag = s.find('h1', {'class': 'global__TitleArtileStyle-sc-10c7lju-11 jhpyER'})

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
    'from_web' : 'ทรูไอดี',
    'Title_news' : title_news(),
    'content_news' : news(),
    'created_on' : current_datetime,
    'views' : news_views()
}

df = pd.DataFrame(data)

connection = sqlite3.connect(r'C:\thatsapon\database\SQLite\db_ThirdParty.db')
cursor = connection.cursor()

for index, row in df.iterrows():
    cursor.execute('''SELECT * FROM news_property WHERE date_news = ? AND content_news = ?''',
                   (row['date_news'], row['content_news']))
    existing_data = cursor.fetchall()

    if not existing_data:
        cursor.execute('''INSERT INTO news_property (date_news, from_web, Title_news, content_news, created_on, views) VALUES (?, ?, ?, ?, ?, ?)''', 
                       (row['date_news'], row['from_web'], row['Title_news'], row['content_news'], row['created_on'], row['views']))
        connection.commit()

connection.close()