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

        
# print(property())
print(property())