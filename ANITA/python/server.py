import logging, logging.config, os
from logging.handlers import TimedRotatingFileHandler
import connexion
from flask_cors import CORS
from precondition import check_preconditions

# Create the application instance
app = connexion.App(__name__, specification_dir='./')
CORS(app.app)

# Read the swagger.yml file to configure the endpoints
app.add_api("swagger/v1/software-quality.yml")
app.add_api("swagger/v1/marketplaces.yml")
app.add_api("swagger/v1/status.yml")


def config_log():
    logname = "anita.log"

    # Create logger
    logging.basicConfig(filename=logname, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # set up logging to console
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)

    # add the handler to the root logger
    logging.getLogger('').addHandler(console)


if __name__ == "__main__":
    config_log()
    logger = logging.getLogger("server")

    logger.info("Start anita server")

    # Preconditions
    status = check_preconditions()

    if status:
        logger.info("INFO")
        logger.info("HOST: " + os.environ["FLASK_HOST"])
        logger.info("PORT: " + os.environ["FLASK_PORT"])
        app.run(host=os.environ["FLASK_HOST"], port=int(os.environ["FLASK_PORT"]), debug=True, use_reloader=False)
