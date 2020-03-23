from wordcloud import WordCloud #워드클라우드
from konlpy.tag import Twitter #한국어 자연어 처리를 위한 라이브러리
from collections import Counter #명사 출현 빈도를 세기위한 라이브라리
import matplotlib.pyplot as plt#그래프 생성
from flask import Flask, request, jsonify #플라스크 웹 서버 구축을 위한 라이브러리

#플라스크 웹서버 객체를 생성
app = Flask(__name__)

#폰트 경로
font_path='NanumGothic.ttf'

def get_tags(text, max_count, min_Length):
    t = Twitter()
    nouns = t.nouns(text)
    processed = [n for n in nouns if len(n) >= min_Length]
    count = Counter(processed)
    result={}
    for n, c in count.most_common(max_count):
        result[n] = c
    if len(result) == 0:
        result['내용이 없습니다.'] = 1       
    return result

def make_cloud_img(tags, file_name):
    #만들고자하는 워드클라우드의 기본설정
    word_cloud = WordCloud(
        font_path = font_path,
        width = 800,
        height=800,
        background_color='white'
        
    )
    word_cloud=word_cloud.generate_from_frequencies(tags)
    fig = plt.figure(figsize=(10,10))
    plt.imshow(word_cloud)
    plt.axis('off')
    #만들어진 이미지를 파일형태로 저장
    fig.savefig("outputs/{0}.png".format(file_name))

def process_from_text(text, max_count, min_Length, words):
    tags = get_tags(text, max_count, min_Length)
    #단어 가중치 적용
    for n,c in words.items():
        if n in tags:
            tags[n] = tags[n] * int(words[n])
            
    make_cloud_img(tags, "output4")
    
    

@app.route('/process', methods=['GET','POST'])
def process():
    content = request.json
    words={}
    if content['words'] is not None:
        for data in content['words'].values():
            words[data['word']] = data['weight']
    process_from_text(content['text'],content['maxCount'],content['minLength'],words)
    result ={'result': True}
    return jsonify(result)    


if __name__=='__main__':
    app.run('0.0.0.0', port=5000)    

