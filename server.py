import logging
import requests
from flask import Flask, Response, request, g
from sqlite3 import dbapi2 as sqlite3
import json


app = Flask(__name__)


DATABASE = '/app/db/database.db'
SCHEMA_STD = '/app/db/schema.sql'
SLACK_HOOK = 'https://hooks.slack.com/services/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'


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

    db.row_factory = sqlite3.Row
    return db


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(SCHEMA_STD, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/codeupgirl', methods = ['POST', 'GET'])
def handleCommand():
    if request.method == 'POST':
        try:
            command = request.form['command']
            on_func = {
                '/newstudent': on_new_user,
                '/deletestudent': on_delete_user,
                '/allstudents': on_all_students
            }[command]
            on_func(request.form['text'])
            msg = 'recieved'
        except Exception as e:
            logger.exception(e)
            msg = 'problemo'

        finally:
            return msg


def on_delete_user(text):
    con = get_db()
    query_db("UPDATE students \
             SET isactive=0 \
             WHERE username=? ",
             ( text, ) )
    con.commit()
    msg = 'Student deleted *{}*'.format(text)
    send_message(msg)


def on_new_user(text):
    if not text:
        send_message('`Looks like you forgot something. ( pro tip: username.`')
        return

    con = get_db()
    query_db('INSERT OR REPLACE INTO students (username, isactive) VALUES (?, ?)',
             (text, 1))
    con.commit()
    msg = 'New Student Added 😎 ! Say hi to *{}*'.format(text)
    send_message(msg)


def on_all_students(text):
    message = ''

    for student in query_db('SELECT name, score FROM results ORDER BY NOT score'):
        message += '`👸 {:<20} ❤️  {:<10} `\n'.format(student[0], student[1])

    send_message(message)


def send_message(message):
    requests.post(SLACK_HOOK, json = {'text': message})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", debug=True)
