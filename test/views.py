from test.main import app

@app.route("/")
def index():
    return "HelloWorld"