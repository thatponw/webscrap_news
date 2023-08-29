import requests
from bs4 import BeautifulSoup

def property():
    # ลิงก์ที่คุณต้องการดึงข้อมูล
    link_to_scrape = "https://www.bangkokbiznews.com/category/property"  # แทนที่ด้วยลิงก์ที่คุณต้องการดึงข้อมูล

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

        # ตรวจสอบให้แน่ใจว่ามีลิงก์ตำแหน่งที่ 17 หรือไม่
        for i in range(18,35) :
            if i < len(links):  # เนื่องจากเริ่มต้นนับที่ 0
                selected_links.append(links[i].get("href"))
                
        return selected_links
    
def news():
    url_list = property()
    news_list = []  # สร้างลิสต์เพื่อเก็บข่าวทั้งหมด

    for idx, link in enumerate(url_list, start=1):
        url = f'https://www.bangkokbiznews.com{link}'
        r = requests.get(url)
        r.text[:200]

        s = BeautifulSoup(r.text, 'lxml')

        d = s.find('div', {'id': 'content'})

        p_tag = d.find_all('p')

        content = ''  # สร้างตัวแปรเพื่อเก็บเนื้อหาข่าว

        for i in p_tag:
            paragraph = i.get_text()
            paragraph = paragraph.replace('\n', '').replace('\xa0', '')
            content += paragraph

        
        news_list.append(content)

    return news_list
    # แสดงผลลิสต์ของเนื้อหาข่าว
    for idx, news_content in enumerate(news_list, start=1):
        print(f"News {idx}:\n{news_content}\n")

# เรียกใช้ฟังก์ชัน

# print(news())
