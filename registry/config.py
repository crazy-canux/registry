import os
import logging
from configparser import ConfigParser


logger = logging.getLogger(__name__)


class Config(object):

    def __init__(self, config_path="/etc/registry/registry.ini"):
        self.config_path = config_path
        self._load()

    def get_mode(self):
        return self._get_option_value("env", "mode", "client")

    def get_port(self):
        return self._get_option_value("env", "port", "8080")

    def get_path(self):
        return self._get_option_value("storage", "path", "")

    def get_registry_dir(self):
        return self._get_option_value("storage", "registry", "")

    def _get_options(self, section):
        return self.parser.options(section)

    def _get_option_value(self, section_name, option_name, default_value):
        try:
            if not self.parser.has_option(section_name, option_name):
                return default_value

            option_type = str(type(default_value))
            option_value = self.parser.get(section_name, option_name)
            if "bool" in option_type:
                if option_value == "":
                    return default_value
                option_value = self.parser.getboolean(section_name, option_name)
            elif "int" in option_type:
                if option_value == "":
                    return default_value
                option_value = self.parser.getint(section_name, option_name)

            return option_value

        except Exception as e:
            logger.exception("Failed to get value of [%s]:%s, e=%s" % \
                             (section_name, option_name, e))
            return default_value

    def _set_option_value(self, section_name, option_name, option_value):
        try:
            self.parser.set(section_name, option_name, str(option_value))
            self._save()
        except Exception as e:
            logger.exception("Failed to set value of [%s]:%s, e=%s" % \
                             (section_name, option_name, e))

    def _load(self):
        self.parser = ConfigParser()
        if not os.path.exists(self.config_path):
            return

        with open(self.config_path, "r") as config_file:
            self.parser.read_file(config_file)

    def _save(self):
        if not os.path.exists("/etc/registry"):
            os.makedirs("/etc/registry")
        with open(self.config_path, "w") as config_file:
            self.parser.write(config_file)
