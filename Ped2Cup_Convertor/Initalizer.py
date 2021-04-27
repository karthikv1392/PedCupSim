_Author_ = "Karthik Vaidhyanathan"

# class to load configurations from config file

from configparser import ConfigParser
import traceback
from Custom_Logger import logger


CONFIG_FILE = "settings.conf"
CONFIG_SECTION = "settings"

class Initialize():
    def __init__(self):
        # Initliaze configurations
        try:
            parser = ConfigParser()
            parser.read(CONFIG_FILE)
            self.data_path = parser.get(CONFIG_SECTION, "data_path")
            self.data_file = parser.get(CONFIG_SECTION,"data_file")
            self.config_json = parser.get(CONFIG_SECTION, "config_json")
            self.output_path = parser.get(CONFIG_SECTION, "output_path")

        except Exception as e:
            logger.error(e)