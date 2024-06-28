from ALCOAPI.main import app

@app.route("/")
def index():
    return "HelloWorld"