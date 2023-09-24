from .Logger import logger
import yaml
import sys
import os

PARAMS = os.environ["PARAMS"]
ENTRY = 0
EXIT = 1
ACTIVATE = 2
DEACTIVATE = 3

STATE_ACTIVATE = True
STATE_DEACTIVATE = False

try:
    with open(PARAMS, 'r') as config_file:
        config_data = yaml.safe_load(config_file)
except FileNotFoundError as file_error:
    logger.logger.error(f"Error: {file_error}")
    sys.exit(1)

postgres = config_data["postgres"]
PG_CREDENTIALS = postgres["credentials"]
PG_HOSTNAME = postgres["hostname"]
PG_DATABASE = postgres["database"]
PG_USER = PG_CREDENTIALS["username"]
PG_PASSWORD = PG_CREDENTIALS["password"]

app = config_data["app"]
APP_CREDENTIALS = app["credentials"]
auth = app["auth"]
AUTH_SECRET = auth["secret"]
AUTH_ALGORITHM = auth["algorithm"]
AUTH_JWT_TIMEOUT = auth["jwt_timeout"]