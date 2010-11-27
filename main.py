import data
from datetime import datetime
from helpers import RestFlask, templated

# Development configuration
DATABASE = 'sqlite:///db/onb-dev.db'
DEBUG = True
SECRET_KEY = 'th1$ is the s0ng that d03$n"t eeennnnnddd!@@@!&%'
USERNAME = 'admin'
PASSWORD = 'default'

app = RestFlask(__name__)
app.config.from_envvar('ONB_SETTINGS', silent=True)

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

if __name__ == '__main__':
    app.config.from_object(__name__)
    app.run(host='0.0.0.0', debug=True)
