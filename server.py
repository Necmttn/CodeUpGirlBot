from flask import Flask, Response, request
import json


app = Flask(__name__)


@app.route("/")
def hello():
    res = Response(json.dumps(readFile()))
    res.headers['Content-type'] = 'application/json'
    return res

@app.route("/newUser/<path:username>")
def newUser(username):
    return username + "dick"


@app.route('/add', methods=['POST'])
def add_entry():
    asd = request.data
    print(json.loads(asd))
    return asd


def readFile():
    fh = open('/app/results.json')
    data =  json.load(fh)
    fh.close()
    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
