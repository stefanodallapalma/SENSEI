import logging, logging.config, os
import connexion
from flask_cors import CORS

# Create the application instance
app = connexion.App(__name__, specification_dir='./')
CORS(app.app)

# Read the swagger.yml file to configure the endpoints
app.add_api("swagger/v1/marketplaces.yml")
app.add_api("swagger/v1/status.yml")
app.add_api("swagger/v1/trend-analysis.yml")


def config_log():
    logname = "anita.log"

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


def resource_precondition():
    # Resource dir names
    dir = "trend_analysis"

    # Resource directories
    onlydirs = [f for f in os.listdir(resource_path) if os.path.isdir(join(resource_path, f))]

    folders_created = []

    if dir not in onlydirs:
        os.mkdir(os.path.join(resource_path, dir))
        folders_created.append(dir)

        # Create folder paths
        ta_path = os.path.join(resource_path, dir)
        markets_path = os.path.join(ta_path, "markets")
        os.mkdir(markets_path)

        market_list = [market.name.lower() for market in Market if market.value != 0]
        for market in market_list:
            os.mkdir(os.path.join(markets_path, market))

    return True


if __name__ == "__main__":
    config_log()
    logger = logging.getLogger("server")

    logger.info("Start anita server")

    # Preconditions
    status = resource_precondition()

    if status:
        logger.info("INFO")
        logger.info("HOST: " + os.environ["FLASK_HOST"])
        logger.info("PORT: " + os.environ["FLASK_PORT"])
        app.run(host=os.environ["FLASK_HOST"], port=int(os.environ["FLASK_PORT"]), debug=True, use_reloader=False)
