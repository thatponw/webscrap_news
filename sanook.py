import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import *
import sqlite3

def property():
    # ลิงก์ที่คุณต้องการดึงข้อมูล
    link_to_scrape = "https://www.sanook.com/news/tag/%E0%B8%AD%E0%B8%AA%E0%B8%B1%E0%B8%87%E0%B8%AB%E0%B8%B2%E0%B8%A3%E0%B8%B4%E0%B8%A1%E0%B8%97%E0%B8%A3%E0%B8%B1%E0%B8%9E%E0%B8%A2%E0%B9%8C/"  # แทนที่ด้วยลิงก์ที่คุณต้องการดึงข้อมูล

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
        for i in range(81,120) :
            if i < len(tag_list):  # เนื่องจากเริ่มต้นนับที่ 0
                selected_links.append(tag_list[i].get("href"))
                
        return selected_links
    

def news():
    url_list = property()
    news_list = []  # สร้างลิสต์เพื่อเก็บข่าวทั้งหมด

    for idx, link in enumerate(url_list, start=1):
        url = f'{link}'
        r = requests.get(url)
        r.text[:200]

        s = BeautifulSoup(r.text, 'lxml')

        d = s.find('div', {'id': 'EntryReader_0'})

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
        url = f'{link}'
        r = requests.get(url)
        r.text[:200]

        s = BeautifulSoup(r.text, 'lxml')

        d = s.find('span', {'class': 'jsx-1959557358 infoItem'})
        date_text = d.get_text(strip=True).replace('(', '').replace(')', '')


        news_list.append(date_text)

    return news_list  # คืนค่าลิสต์ข้อมูลข่าวทั้งหมด


def news_views():

    news_list = []  # สร้างลิสต์เพื่อเก็บข้อมูลข่าวทั้งหมด

    for idx, link in enumerate(property(), start=1):
        url = f'https://www.sanook.com/news/tag/%E0%B8%AD%E0%B8%AA%E0%B8%B1%E0%B8%87%E0%B8%AB%E0%B8%B2%E0%B8%A3%E0%B8%B4%E0%B8%A1%E0%B8%97%E0%B8%A3%E0%B8%B1%E0%B8%9E%E0%B8%A2%E0%B9%8C/'
        r = requests.get(url)
        r.text[:200]

        s = BeautifulSoup(r.text, 'lxml')

        spans = s.find_all('span', {'class': 'jsx-1818055635 text'})
        
        # เลือกตัวอิลิเมนต์ที่คุณต้องการโดยดัชนี (index)
        for i in range(1, len(spans), 2):
            if i < len(spans):
                views_text = spans[i].get_text(strip=True)
                news_list.append(views_text)
            else:
                news_list.append(None)

    return news_list  # คืนค่าลิสต์ข้อมูลข่าวทั้งหมด


print(news_views())