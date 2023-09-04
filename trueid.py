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
    
    return selected_links
            

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


print(news())