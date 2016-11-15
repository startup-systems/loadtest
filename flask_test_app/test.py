from flask import Flask
from flask import jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    d = {'result': 4}
    return jsonify(**d)

@app.route("/some_url")
def four():
    d = {'result': 10, 'result2': 20}
    return jsonify(**d)

if __name__ == "__main__":
    app.run()
