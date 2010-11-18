from data import Database, get_page_content
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

db = Database(app.config.get('DATABASE', DATABASE))

@app.context_processor
def inject_now():
    return dict(now=datetime.now())

@app.get('/')
@templated()
def index():
    content = dict([[c.key, c.text] for c in get_page_content(db, 'index')])
    return dict(content=content)

if __name__ == '__main__':
    app.config.from_object(__name__)
    app.run(host='0.0.0.0', debug=True)
