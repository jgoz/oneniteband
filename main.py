from datetime import datetime
from helpers import RestFlask, templated

app = RestFlask(__name__)

@app.context_processor
def inject_now():
    return dict(now=datetime.now())

@app.get('/')
@templated()
def index():
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
