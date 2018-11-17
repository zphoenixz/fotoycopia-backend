from flask import Flask


app = Flask(__name__)
PORT = 5000 #8000
DEBUG = False #True

@app.errorhandler(404)
def not_found(error):
    return "Not Found"

@app.route('/', methods = ['GET'])
def index():
    return "Hola gente de aca mundo"

if __name__ == '__main__':
    app.run(port = PORT, debug = DEBUG)