import connexion
from flask_cors import CORS
from check.precondition import check_preconditions

# Create the application instance
app = connexion.App(__name__, specification_dir='./')
CORS(app.app)

# Read the swagger.yml file to configure the endpoints
app.add_api("swagger/v1/software-quality.yml")

if __name__ == "__main__":
    print("Start anita server\n")
    status = check_preconditions()

    if status:
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)