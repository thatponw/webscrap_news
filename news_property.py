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

        # ตรวจสอบให้แน่ใจว่ามีลิงก์ตำแหน่งที่ 17 หรือไม่
        if len(links) >= 18:  # เนื่องจากเริ่มต้นนับที่ 0
            link_index = links[18].get("href")
            # print(link_index)

        return link_index
    
def news():
    url = str('https://www.bangkokbiznews.com'+str(property()))
    r = requests.get(url)
    r.text[:200]

    s = BeautifulSoup(r.text,'lxml')

    d=s.find('div',{'id':'content'})

    p_tag = d.find_all('p')

    content_list = []  # สร้างลิสต์เพื่อเก็บเนื้อหาข่าว

    for i in p_tag:
        content = i.get_text()
        content = content.replace('\n', '').replace('\xa0', '')
        content_list.append(content)
    
    return content_list  # คืนค่าเนื้อหาข่าวที่ถูกเก็บในรูปแบบของลิสต์
