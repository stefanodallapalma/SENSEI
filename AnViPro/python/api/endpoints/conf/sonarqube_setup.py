from flask import request, Response, json

sonarqube_setup_path = "../resources/sonarqube_properties.json"

def setup():
    source = request.form["source"]

    sonarqube_dict = {}
    if source == "external":
        host = request.form["host"]
        port = request.form["port"]
        token = request.form["token"]
        user = request.form["user"]
        password = request.form["password"]

        sonarqube_dict["host"] = host
        sonarqube_dict["port"] = port
        sonarqube_dict["token"] = token
        sonarqube_dict["user"] = user
        sonarqube_dict["password"] = password
    else:
        # TO DO
        return Response(json.dumps("INTERNAL SONARQUBE CONFIGURATION NOT BEEN AVAILABLE"), status=400, mimetype="application/json")

    sonarqube_dict["projectKeys"] = {}

    with open(sonarqube_setup_path, 'w') as outfile:
        json.dump(sonarqube_dict, outfile)

    return Response(json.dumps(sonarqube_dict), status=200, mimetype="application/json")


