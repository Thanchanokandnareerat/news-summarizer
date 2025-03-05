from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import re
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    url = data.get('url', '').strip()

    if not url:
        return jsonify({'error': 'No URL provided'}), 400  

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    # ลองโหลดใหม่ 3 ครั้งถ้าล้มเหลว
    for i in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                break  
        except requests.exceptions.RequestException as e:
            print(f"Retrying ({i+1}/3)...")
            time.sleep(3)  

    if response.status_code != 200:
        return jsonify({'error': f'Failed to fetch article (HTTP {response.status_code})'}), 400

    soup = BeautifulSoup(response.content, 'html.parser')

    paragraphs = soup.find_all('p')
    article_text = ' '.join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 50])

    if not article_text:
        return jsonify({'error': 'Failed to extract text from the article'}), 400

    # ✅ สรุปข่าวแบบ Extractive (3 ประโยคแรก)
    sentences = re.split(r'(?<=\w[.!?])\s', article_text)
    summary_text = ' '.join(sentences[:3])

    # ✅ แปลข้อความแบบเต็ม
    full_translation = GoogleTranslator(source='en', target='th').translate(article_text)

    # ✅ แปลเฉพาะสรุปข่าว
    summary_translation = GoogleTranslator(source='en', target='th').translate(summary_text)

    # ✅ ดึงคำศัพท์สำคัญ
    words = re.findall(r'\b[A-Za-z]{5,}\b', article_text)
    words = list(set(words))  
    translated_words = {word: GoogleTranslator(source='en', target='th').translate(word) for word in words[:20]}  

    return jsonify({
        'full_text': article_text,  
        'full_translation': full_translation,  
        'summary': summary_text,  
        'summary_translation': summary_translation,  
        'vocabulary': translated_words  
    })

if __name__ == '__main__':
    app.run(debug=True)