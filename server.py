import logging
from flask import Flask, Response, request, g, render_template
from sqlite3 import dbapi2 as sqlite3
import json

app = Flask(__name__)

DATABASE = '/app/db/database.db'

logger = logging.getLogger('server')
logger.setLevel(logging.DEBUG)

def get_db():
    """
    Opens a new database connection if there is none yet for
    the current application context.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('/app/db/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    logger.debug(query, args)
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/")
def hello():
    res = Response(json.dumps(readFile()))
    res.headers['Content-type'] = 'application/json'
    return res

@app.route("/newUser/<path:username>")
def newUser(username):
    return username + "dick"


@app.route('/users', methods=['get'])
def get_users():
    return str([ (user[0], user[1]) for user in query_db('select * from students')])




@app.route('/newstudent', methods = ['POST', 'GET'])
def new_student():
    if request.method == 'POST':
        try:
            con = get_db()
            query_db('INSERT INTO students (username, bio, score) VALUES (?, ?, ?)',
                (request.json['username'], request.json['bio'], request.json['score']))
            con.commit()
            msg = "Record succesfully added"
        except Exception as e:
            logger.exception(e)
            msg = "error in insert operation"

        finally:
            return msg
    return 'Only Post'


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']

         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute('INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)', (nm,addr,city,pin))
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"

      finally:
         return render_template("./result.html",msg = msg)
         con.close()

def readFile():
    fh = open('/app/scrap/results.json')
    data =  json.load(fh)
    fh.close()
    return data


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
