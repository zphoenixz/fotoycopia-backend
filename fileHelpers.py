
import requests
import re


class fileHelpers:

    def __init__(self,url):
        self.url = url
        self.r = requests.get(self.url, allow_redirects=True)

    def downloadUrl(self, filename):
        # url = 'http://google.com/favicon.ico'
        open(filename, 'wb').write(self.r.content)

    def wichDocumentTypeIs(self):
        """
        Does the url contain a downloadable resource
        """
        content_type = self.r.headers.get('Content-Type')
        # if 'text' in content_type.lower():
        #     return False
        # if 'html' in content_type.lower():
        #     return False
        # return True
        return content_type

    def sizeOfTheFile(self):
        content_length = self.r.headers.get('Content-Length')
        # if content_length and content_length > 2e8:  # 200 mb approx
        #     return False
        # return True
        return content_length

    def get_filename_from_cd(self):
        cd = self.r.headers.get('content-disposition')
        """
        Get filename from content-disposition
        """
        if not cd:
            return None
        else:
            return cd
