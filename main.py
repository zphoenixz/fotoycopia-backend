from flask import Flask

import driveApiABM

app = Flask(__name__)
PORT = 5000 #8000
DEBUG = True #True

@app.errorhandler(404)
def not_found(error):
    return "Not Found"

@app.route('/', methods = ['GET'])
def index():
    return "Hola gente de aca mundo0"

@app.route('/get_all_not_trashed', methods = ['GET'])
def getAllData():
    print("entre 0")
    ManageABM = driveApiABM.ABM()
    allNotTrasedDocs = ManageABM.getAllNotTrashedDocs()
    print("entre 4")
    return allNotTrasedDocs


if __name__ == '__main__':
    app.run(port = PORT, debug = DEBUG)