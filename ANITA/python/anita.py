import connexion
from flask_cors import CORS
from check.precondition import check_preconditions

# Create the application instance
app = connexion.App(__name__, specification_dir='./')
CORS(app.app)

# Read the swagger.yml file to configure the endpoints
app.add_api("swagger/conf.yml")
app.add_api("swagger/data.yml")
app.add_api('swagger/swagger.yml')
app.add_api('swagger/resources.yml')
app.add_api("swagger/softwarequality.yml")

if __name__ == "__main__":
    status = check_preconditions()

    if status:
        print("OK")
        #app.run(host='0.0.0.0', port=5000, debug=True)
        pass

