# 실행방법
# pip install flask
# python app.py 실행 후 http://127.0.0.1:5000 접속
from flask import Flask, render_template, request
from database_api import connect_db, get_data, disconnect_db
from vector_api import search_events
import config

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    question = request.form['search_query']
    
    # 벡터 API를 통해 eventid 리스트 가져오기
    event_ids = search_events(question)
    
    if event_ids:
        # 데이터베이스에서 해당 eventid에 대한 정보 가져오기
        conn, cur = connect_db()
        placeholders = ', '.join(['%s'] * len(event_ids))
        query = f"SELECT * FROM event WHERE EventID IN ({placeholders})"
        cur.execute(query, tuple(event_ids))
        events = cur.fetchall()
        disconnect_db(conn, cur)
    else:
        events = []

    return render_template('results.html', events=events)

if __name__ == '__main__':
    app.run(debug=True)
