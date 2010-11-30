import data
from datetime import datetime
from flask import flash, g, redirect, render_template, request, session, url_for
from helpers import RestFlask, templated, check_password, MethodRewriteMiddleware

# Development configuration
DATABASE = 'sqlite:///db/onb-dev.db'
DEBUG = True
SECRET_KEY = 'th1$ is the s0ng that d03$n"t eeennnnnddd!@@@!&%'
USERNAME = 'admin'
PASSWORD = 'default'

app = RestFlask(__name__)
app.config.from_envvar('ONB_SETTINGS', silent=True)
app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)

db = data.Database(app.config.get('DATABASE', DATABASE))

@app.context_processor
def inject_now():
    return dict(now=datetime.now())

@app.template_filter('gigdate')
def gigdate_filter(dt):
    return dt.strftime('%b %d')

@app.get('/')
@templated()
def index():
    return dict(gigs=data.get_upcoming_gigs(db))

@app.get('/bio')
@templated()
def bio():
    return dict(band_bio=data.get_band_bio(db), bios=data.get_member_bios(db))

@app.get('/session')
@templated()
def start_session():
    return None

@app.post('/session')
@templated()
def create_session():
    username, password = request.form['username'], request.form['password']
    user = data.get_admin(db, username)
    try:
        check_password(user, password)
    except:
        return render_template('start_session.html', error='Username and password do not match.', username=username, password=password)
    else:
        session['user'] = dict(username=user.username)
        return session['user']

if __name__ == '__main__':
    def adduser(username, password):
        return data.add_admin(db, username.trim(), password.trim())

    import sys
    if len(sys.argv) == 1:
        app.config.from_object(__name__)
        app.run(host='0.0.0.0', debug=True)
    elif len(sys.argv) == 4 and sys.argv[1] == 'adduser':
        print adduser(sys.argv[2], sys.argv[3])
