from flask import Flask, render_template
# 실행방법
# pip install flask
# python app.py 실행 후 http://127.0.0.1:5000 접속
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
