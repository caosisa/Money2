from flask import Flask, request
from konlpy.tag import Hannanum
from collections import Counter
import re
import math

app = Flask(__name__)

def analyze_text(text):
    # 형태소 분석기 초기화
    okt = Hannanum()

    # 공백 제외 글자수 계산
    text_without_spaces = re.sub(r'\s+', '', text)
    char_count = len(text_without_spaces)

    # 형태소 분석
    morphs = okt.nouns(text)

    # 형태소 빈도 계산
    morph_counts = Counter(morphs)

    return char_count, morph_counts

def generate_html(char_count, morph_counts, keyword, keyword_count):
    # 형태소 빈도수를 내림차순으로 정렬
    sorted_morph_counts = sorted(morph_counts.items(), key=lambda item: item[1], reverse=True)

    # HTML 템플릿 생성
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>형태소 분석 결과</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            .info-block {{
                border: 1px solid #dddddd;
                padding: 10px;
                margin-bottom: 20px;
                background-color: #f9f9f9;
            }}
            table {{
                border-collapse: collapse;
                width: 80%;
            }}
            th, td {{
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .red {{
                color: red;
            }}
            .blue {{
                color: blue;
            }}
            .yellow {{
                background-color: yellow;
            }}
        </style>
    </head>
    <body>
        <div class="info-block">
            <p><strong>키워드:</strong> {keyword}</p>
            <p><strong>키워드 반복 횟수:</strong> {keyword_count}</p>
            <p><strong>공백 제외 글자수:</strong> {char_count}</p>
        </div>
        <h3>형태소 빈도수:</h3>
        <table>
            <tr>
                <th>형태소</th>
                <th>빈도수</th>
                <th>형태소</th>
                <th>빈도수</th>
                <th>형태소</th>
                <th>빈도수</th>
                <th>형태소</th>
                <th>빈도수</th>
                <th>형태소</th>
                <th>빈도수</th>
            </tr>"""

    rows = math.ceil(len(sorted_morph_counts) / 5)

    for i in range(rows):
        html_content += "<tr>"
        for j in range(5):
            if i * 5 + j < len(sorted_morph_counts):
                morph, count = sorted_morph_counts[i * 5 + j]
                class_name = ''
                if morph == keyword:
                    class_name = 'yellow'
                elif count >= 10:
                    class_name = 'red'
                elif count >= 5:
                    class_name = 'blue'
                html_content += f"<td class='{class_name}'>{morph}</td><td class='{class_name}'>{count}</td>"
            else:
                html_content += "<td></td><td></td>"
        html_content += "</tr>"

    html_content += """
        </table>
    </body>
    </html>
    """

    return html_content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        keyword = request.form['keyword']
        char_count, morph_counts = analyze_text(text)
        keyword_count = morph_counts.get(keyword, 0)
        html_result = generate_html(char_count, morph_counts, keyword, keyword_count)
        return html_result

    return '''
        <!doctype html>
        <html lang="ko">
        <head>
            <meta charset="utf-8">
            <title>형태소 분석기</title>
        </head>
        <body>
            <h1>형태소 분석기</h1>
            <form method="post">
                <label for="text">분석할 텍스트:</label><br>
                <textarea id="text" name="text" rows="4" cols="50"></textarea><br><br>
                <label for="keyword">키워드:</label><br>
                <input type="text" id="keyword" name="keyword"><br><br>
                <input type="submit" value="분석">
            </form>
        </body>
        </html>
    '''


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)