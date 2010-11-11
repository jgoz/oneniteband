from helpers import RestFlask, templated

app = RestFlask(__name__)

@app.get('/')
@templated()
def index():
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
