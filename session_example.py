from flask import Flask, session
import logging

# https://www.askpython.com/python-modules/flask/flask-sessions

app = Flask(__name__)
app.secret_key = "xyz"

logging.basicConfig(
    level = "INFO",
    # format = '%(levelname)s %(asctime)s.%(msecs)03d %(module)10s/%(lineno)-5d %(message)s'
    format = '%(levelname)s %(module)13s/%(lineno)-5d %(message)s'
)

log = logging.getLogger("dash_spa")


@app.before_request
def req_session_id():
    if 'Username' in session:
        log.info('before_request %s is already active', session['Username'])
    else:
        session['Username'] = 'Admin  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        log.info('before_request set %s', session['Username'])



@app.route('/setsession')
def setsession():
    if 'Username' in session:
        log.info('session %s', session['Username'])
        return f"Session {session['Username']} is already active"
    else:
        session['Username'] = 'Admin'
        return f"The session has been Set"

@app.route('/getsession')
def getsession():
    if 'Username' in session:
        Username = session['Username']
        return f"Welcome {Username}"
    else:
        return "Welcome Anonymous"

@app.route('/popsession')
def popsession():
    session.pop('Username',None)
    return "Session Deleted"

print(' * Visit http://default:5026/getsession')

app.run(host='0.0.0.0', port=5000)