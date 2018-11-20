from flask import Flask

import driveApiABM
import fileHelpers

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
    ManageABM = driveApiABM.ABM()
    allNotTrasedDocs = ManageABM.getAllNotTrashedDocs()
    return allNotTrasedDocs

@app.route('/load_file', methods = ['GET'])
def uploadFile():
    ManageABM = driveApiABM.ABM()
    allNotTrasedDocs = ManageABM.uploadFile('redes.pdf','https://firebasestorage.googleapis.com/v0/b/booking-d6940.appspot.com/o/Archivos%2F9i2712eflcasmolcb579anraae?alt=media&token=1e0aa3dc-d5e4-41d9-b737-01f4dabbee8a','application/vnd.google-apps.document')
    return allNotTrasedDocs

@app.route('/download_file', methods = ['GET'])
def downloadFile():
    ManageABM = driveApiABM.ABM()
    ManageABM.downloadFile('1VN4uxGmvwduIt0P6WzfvqEpAmsAogpMt','descargada.jpg')#application/msword

    ManageABM.uploadFile('descargada.jpg','descargada.jpg','image/jpeg')
    return "Descargado de drive y Subido a drive"

#This should be a post
@app.route('/probar', methods = ['GET'])
def tryFile():
    url = "https://firebasestorage.googleapis.com/v0/b/booking-d6940.appspot.com/o/Archivos%2F9i2712eflcasmolcb579anraae?alt=media&token=1e0aa3dc-d5e4-41d9-b737-01f4dabbee8a','application/vnd.google-apps.document"
    # # url = urllib.parse.quote_plus(url)
    # print(url)
    fileAux = fileHelpers.fileHelpers(url)
    documentType = fileAux.wichDocumentTypeIs()
    fileSize = fileAux.sizeOfTheFile()
    fileName = fileAux.get_filename_from_cd()
    # print("Downloading! ")
    fileAux.downloadUrl("descargue.pdf")

    ManageABM = driveApiABM.ABM()
    fileId = ManageABM.uploadFile('descargue.pdf','descargue.pdf', documentType)
    ManageABM.makeLinkPublic(fileId)
    # r = requests.get(url, allow_redirects=True)  # to get content after redirection
    # pdf_url = r.url # 'https://media.readthedocs.org/pdf/django/latest/django.pdf'
    # with open('file_name.pdf', 'wb') as f:
    #     f.write(r.content)

    return "Is downloable? -> " + str(documentType) + " - Size of the file is -> " + str(fileSize) + " - FileName is suposed to be -> " + str(fileName)

if __name__ == '__main__':
    app.run(port = PORT, debug = DEBUG)