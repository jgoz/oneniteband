from helpers import RestFlask

app = RestFlask(__name__)

@app.get('/')
def get_hello_world():
    return "Hello Whirrled!"

@app.post('/')
def post_hello_world():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
