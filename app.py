from flask import Flask, render_template, request
from database_api import get_events_with_images
from vector_api import search_events
from openai_api import generate_marketing_suggestions

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    question = request.form['search_query']
    
    # 벡터 API를 통해 eventid 리스트 가져오기
    event_ids = search_events(question)
    
    events = []
    if event_ids:
        # 데이터베이스에서 해당 eventid에 대한 정보 가져오기
        events = get_events_with_images(event_ids)
    
    # OpenAI API를 통해 마케팅 제안 생성
    suggestions = generate_marketing_suggestions(question, events)
    
    return render_template('results.html', events=events, suggestions=suggestions, search_query=question)

@app.route('/regenerate', methods=['POST'])
def regenerate():
    question = request.form['search_query']
    event_ids = request.form.getlist('event_ids')

    # 데이터베이스에서 해당 eventid에 대한 정보 가져오기
    events = get_events_with_images(event_ids)
    
    # OpenAI API를 통해 마케팅 제안 재생성
    suggestions = generate_marketing_suggestions(question, events)
    
    return render_template('results.html', events=events, suggestions=suggestions, search_query=question)

if __name__ == '__main__':
    app.run(debug=True)
