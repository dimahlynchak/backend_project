from app import app

@app.route('/healthcheck')
def healthcheck():
    return "Server is running!", 200
