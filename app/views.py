from app import app

@app.route('/')
def index():
    return "Welcome to my Flask App!", 200

@app.route('/healthcheck')
def healthcheck():
    return "Server is running!", 200
