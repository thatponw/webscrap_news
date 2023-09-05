from decouple import config
import openai
import sqlite3
from tokenizers import Tokenizer, models, pre_tokenizers, decoders, processors


openai.api_type = "azure"
openai.api_version = "2023-05-15" 
openai.api_base = 'https://spldatainnovation01.openai.azure.com/'  # Your Azure OpenAI resource's endpoint value.
openai.api_key = config("AZURE_OPENAI_KEY")

# กำหนด API key ของคุณที่นี่
api_key = config("AZURE_OPENAI_KEY")

# เชื่อมต่อกับ SQLite และดึงข้อมูล
def connect_to_database():
    conn = sqlite3.connect(r'C:\thatsapon\database\SQLite\db_ThirdParty.db')  # แทน 'your_database.db' ด้วยชื่อฐานข้อมูลของคุณ
    cursor = conn.cursor()
    query = "SELECT * FROM news_property"  # แทน 'your_table' ด้วยชื่อตารางของคุณ
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

# สร้างคำถามสำหรับ GPT
def generate_question(news_data):
    # อาจต้องปรับเปลี่ยนตามโครงสร้างของข้อมูลในฐานข้อมูลของคุณ
    # ตัวอย่าง: "Translate the following English text to French: '{input_data}'"
    return f"เกิดอะไรขึ้นวันที่นี้ '{news_data[1]}'?"

# เรียกใช้ GPT-3
def call_gpt(question):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="test-01",
        prompt=question,
        max_tokens=50
    )
    answer = response.choices[0].text
    return answer

# ดึงข้อมูลจากฐานข้อมูล
data = connect_to_database()

# สร้างคำถามสำหรับ GPT และรับคำตอบ
for news_data in data:
    question = generate_question(news_data)
    gpt_response = call_gpt(question)
    
    # แสดงคำตอบจาก GPT
    print("Question:", question)
    print("Answer:", gpt_response)





