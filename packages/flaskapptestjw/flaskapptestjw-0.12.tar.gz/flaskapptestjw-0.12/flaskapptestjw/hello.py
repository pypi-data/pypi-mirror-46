from flask import Flask, request, render_template,redirect, Response
from flask_s3 import FlaskS3

app = Flask(__name__)
app.config['FLASKS3_BUCKET_NAME'] = 'flaskapptest.jw.com'
s3 = FlaskS3(app)


@app.route('/')
def index():
    return render_template('index.html')

def start():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    start()