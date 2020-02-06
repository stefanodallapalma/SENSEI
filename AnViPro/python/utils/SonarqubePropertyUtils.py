import json

sonarqube_setup_path = "../resources/sonarqubeConfiguration.json"


def add_project(name, projectkey, overwrite_name=False):
    with open(sonarqube_setup_path) as json_file:
        data = json.loads(json_file)

    projectKeys = data["projectKeys"]

    if name in projectKeys and overwrite_name is False:
        raise Exception("Project folder already in the dictionary. "
                        "\nInsert another name or set overwrite_name = True")

    if projectkey in projectKeys.values():
        raise Exception("Project key already in the dictionary. "
                        "\nGenerate another project key and retry")

    projectKeys[name] = projectkey
    data["projectKeys"] = projectKeys

    with open(sonarqube_setup_path, 'w') as outfile:
        json.dump(data, outfile)

def delete_project(name):
    with open(sonarqube_setup_path) as json_file:
        data = json.loads(json_file)

    projectKeys = data["projectKeys"]

    if name in projectKeys:
        del projectKeys[name]

    data["projectKeys"] = projectKeys

    with open(sonarqube_setup_path, 'w') as outfile:
        json.dump(data, outfile)



