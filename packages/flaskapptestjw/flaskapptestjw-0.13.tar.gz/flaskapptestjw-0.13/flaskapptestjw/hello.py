from flask import Flask, request, render_template,redirect, Response

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def index():
    return render_template('index.html')

def start():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    start()