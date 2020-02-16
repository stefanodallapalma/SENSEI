from flask import Response, json
import os

html_page_path = "../resources/html_pages/"

def get_html_page_folders():
    folders = os.listdir(html_page_path)

    json_return = json.dumps(folders)
    status_code = 200

    resp = Response(response=json_return, status=status_code, mimetype="application/json")

    return resp


