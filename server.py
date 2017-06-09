from flask import Flask, Response
import json


app = Flask(__name__)


@app.route("/")
def hello():
    res = Response(json.dumps(readFile()))
    res.headers['Content-type'] = 'application/json'
    return res


def readFile():
    fh = open('/app/results.json')
    data =  json.load(fh)
    fh.close()
    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
