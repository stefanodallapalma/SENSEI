from flask import request, Response, json

sonarqube_setup_path = "../resources/sonarqubeConfiguration.json"

def setup():
    host = request.form["host"]
    port = request.form["port"]
    token = request.form["token"]

    sonarqube_dict = {}
    sonarqube_dict["host"] = host
    sonarqube_dict["port"] = port
    sonarqube_dict["token"] = token
    sonarqube_dict["projectKeys"] = {}

    with open(sonarqube_setup_path, 'w') as outfile:
        json.dump(sonarqube_dict, outfile)

    return Response(json.dumps(sonarqube_dict), status=200, mimetype="application/json")


