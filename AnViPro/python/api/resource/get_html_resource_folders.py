from flask import Response
import os

html_page_path = "../resources/html_pages/"

def get_htmp_page_folders():
    folders = []

    for root, dirs, files in os.walk(html_page_path):
        for name in dirs:
            print(name)
            folders.append(name)

    return folders


