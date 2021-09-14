import logging, logging.config, os
import connexion
from flask_cors import CORS

# Create the application instance
app = connexion.App(__name__, specification_dir='./')
CORS(app.app)

# Read the swagger.yml file to configure the endpoints
app.add_api("swagger/country.yml")
app.add_api("swagger/general.yml")


def config_log():
    logname = "anita-backend-platform.log"

    # Create logger
    logging.basicConfig(filename=logname, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)

    # add the handler to the root logger
    logging.getLogger('').addHandler(console)


if __name__ == "__main__":
    config_log()
    logger = logging.getLogger("server_platform")

    logger.info("Start anita platform server")

    logger.info("INFO")
    logger.info("HOST: " + os.environ["PLATFORM_FLASK_HOST"])
    logger.info("PORT: " + os.environ["PLATFORM_FLASK_PORT"])
    app.run(host=os.environ["PLATFORM_FLASK_HOST"], port=int(os.environ["PLATFORM_FLASK_PORT"]), debug=True,
            use_reloader=False)

