from __future__ import print_function
import httplib2
import os
import io
import json

import requests

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth

class ABM:

    def __init__(self):
        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/drive-python-quickstart.json
        SCOPES = 'https://www.googleapis.com/auth/drive'
        CLIENT_SECRET_FILE = 'credentials.json'
        APPLICATION_NAME = 'FotoYCopia Backend'
        authInst = auth.auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
        credentials = authInst.getCredentials()
        http = credentials.authorize(httplib2.Http())
        self.drive_service = discovery.build('drive', 'v3', http=http)


    def listFiles(self, size):
        results = self.drive_service.files().list(
            pageSize=size, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print('{0} ({1})'.format(item['name'], item['id']))


    def uploadFile(self, filename, filepath, mimetype):
        file_metadata = {'name': filename,
                        "viewersCanCopyContent": False,  # No body cant print nor copy it
                        # "copyRequiresWriterPermission": boolean,
                        # "writersCanShare": boolean,
                        }
        media = MediaFileUpload(filepath)
        file = self.drive_service.files().create(
            body=file_metadata, media_body=media, fields='id').execute()
        print('File ID: %s' % file.get('id'))


    def downloadFile(self, file_id, filepath):
        request = self.drive_service.files().get_media(fileId=file_id)
        # print("requested files is : ",drive_service.drive_service.files().)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        with io.open(filepath, 'wb') as f:
            fh.seek(0)
            f.write(fh.read())


    def createFolder(self, name):
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.drive_service.files().create(body=file_metadata,
                                            fields='id').execute()
        print('Folder ID: %s' % file.get('id'))


    def searchFile(self, size, query):
        results = self.drive_service.files().list(
            pageSize=size, fields="nextPageToken, files(id, name, kind, mimeType)", q=query).execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(item)
                print('{0} ({1})'.format(item['name'], item['id']))

    # uploadFile('word_doc.doc','word_doc.doc','image/jpeg')
    # downloadFile('1JWWfcomvtmhL1q7VfsgNGDwEGDh0LCet','descargada.doc')#application/msword
    # createFolder('Mi nuevo folder')
    # searchFile(10,"name contains 'Getting'")

    # ---------------------------------------------------------
    # file_id = '1JWWfcomvtmhL1q7VfsgNGDwEGDh0LCet'#.doc file


    def callback(request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        else:
            print("Permission Id: %s" % response.get('id'))


    def makeLinkPublic(self, file_id):
        batch = self.drive_service.new_batch_http_request(callback=callback)
        user_permission = {
            'type': 'anyone',
            'role': 'reader',
        }
        batch.add(self.drive_service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id',
        ))
        batch.execute()


    # "name contains 'Getting'"
    def getAllNotTrashedDocs(self):
        results = self.drive_service.files().list(pageSize=10,
                                        fields="nextPageToken, files(id, name, webViewLink, mimeType)",
                                        q="trashed=False",).execute()
        print(results)
        # items = json.dumps(results['files'][1])
        print(results['files'])

        for item in results['files']:
            print(item['id'], item['name'], item['webViewLink'], item['mimeType'])
        return  json.dumps(results['files'])

