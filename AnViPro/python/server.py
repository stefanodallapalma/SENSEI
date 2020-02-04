import connexion
from flask_cors import CORS

# Create the application instance

app = connexion.App(__name__, specification_dir='./')
CORS(app.app)

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')
app.add_api('resources.yml')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

