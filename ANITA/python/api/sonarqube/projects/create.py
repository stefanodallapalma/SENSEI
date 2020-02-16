import requests
import random
import string

create_url = "/api/projects/create"

def create_project(url, name_project):
    request_url = url + create_url
    params = {"key":randomString(), "name":name_project}

    request = requests.post(request_url, params)
    json_response = request.json()

    return json_response

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))