
import logging

LOGGER_NAME_PREFIX = "TUFIN_PS_"
COMMON_LOGGER_NAME = LOGGER_NAME_PREFIX + "COMMON"
MAIL_LOGGER_NAME = LOGGER_NAME_PREFIX + "MAIL"
HELPERS_LOGGER_NAME = LOGGER_NAME_PREFIX + "HELPERS"
REPORTS_LOGGER_NAME = LOGGER_NAME_PREFIX + "REPORTS"
REQUESTS_LOGGER_NAME = LOGGER_NAME_PREFIX + "REQUESTS"
SQL_LOGGER_NAME = LOGGER_NAME_PREFIX + "SQL"
THIRD_PARTY_LOGGER_NAME = LOGGER_NAME_PREFIX + "THIRD_PARTY"
XML_LOGGER_NAME = LOGGER_NAME_PREFIX + "XML"
WEB_LOGGER_NAME = LOGGER_NAME_PREFIX + "WEB"

LOG_LEVEL_SECTION_NAME = "log_levels"

logger_name_to_log_domain = {COMMON_LOGGER_NAME: "COMMON", MAIL_LOGGER_NAME: "MAIL", HELPERS_LOGGER_NAME: "HELPERS",
                             REPORTS_LOGGER_NAME: "REPORTS", REQUESTS_LOGGER_NAME: "REQUESTS", SQL_LOGGER_NAME: "SQL",
                             THIRD_PARTY_LOGGER_NAME: "THIRD_PARTY", XML_LOGGER_NAME: "XML", WEB_LOGGER_NAME: "WEB"}

REGISTERED_LOGGER_NAMES = (COMMON_LOGGER_NAME, HELPERS_LOGGER_NAME, MAIL_LOGGER_NAME, REPORTS_LOGGER_NAME,
                           REQUESTS_LOGGER_NAME, XML_LOGGER_NAME, THIRD_PARTY_LOGGER_NAME, SQL_LOGGER_NAME,
                           WEB_LOGGER_NAME)
LOG_FORMAT = '%(asctime)s - PID:%(process)d - TID:%(thread)d - %(levelname)s - %(module)s - %(name)s - Line %(' \
             'lineno)d - %(message)s'

LOG_FILE_OWNER = "tomcat"
LOG_FILE_GROUP = "apache"
MAX_LOG_BYTES = 512 * 1000 * 1000  # 512MB
MAX_LOG_FILES_BACKUPS = 4
DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_LEVEL_NAME = logging._levelToName[DEFAULT_LOG_LEVEL]
