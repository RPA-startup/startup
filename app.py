# 실행방법
# pip install flask
# python app.py 실행 후 http://127.0.0.1:5000 접속
from flask import Flask, render_template, request
from vector_api import search_events
from database_api import get_events_by_ids

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    question = request.form['search_query']
    
    # 벡터 API 호출
    event_ids = search_events(question)
    
    # 데이터베이스 API 호출
    events = get_events_by_ids(event_ids) if event_ids else []

    return render_template('results.html', events=events)


if __name__ == '__main__':
    app.run(debug=True)
