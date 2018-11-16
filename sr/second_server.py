from flask import Flask


app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>hello from SECOND SERVER </h1>'




if __name__ == '__main__':
    app.run(use_reloader=True, port=8080)
