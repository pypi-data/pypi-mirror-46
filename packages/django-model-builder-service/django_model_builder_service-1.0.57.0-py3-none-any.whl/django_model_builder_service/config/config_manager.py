import os

from django_model_builder_service.common.logger import get_logger


class ConfigManager:
    logger = get_logger()

    CONFIG_SERVICE_PREFIX = 'CONFIG_SERVICE'
    MODEL_CONFIG_PREFIX = 'MODEL_CONFIG_'

    def __init__(self, config_dict=None):
        if config_dict:
            self.__config_dict = config_dict
            return

        self.__config_dict = {}

        env_vars = os.environ
        for var in env_vars:
            if var.startswith(self.CONFIG_SERVICE_PREFIX):
                val = env_vars[var]

                key = var.replace(self.CONFIG_SERVICE_PREFIX + '_', '')
                if self.is_model_config_key(key):
                    key = key.replace(self.MODEL_CONFIG_PREFIX, '')
                    if 'model' not in self.__config_dict:
                        self.__config_dict['model'] = {}
                    self.__config_dict['model'][key.lower()] = val

                else:
                    self.__config_dict[key.lower()] = val

        self.logger.info('Config object: {}'.format(self.__config_dict))

    def is_model_config_key(self, key):
        return key.startswith(self.MODEL_CONFIG_PREFIX)

    def get_config_val(self, key):
        return self.__config_dict[key]

    def get_config_val_with_default(self, key, default):
        try:
            return self.get_config_val(key)
        except KeyError as e:
            self.logger.warning('No config key: {}. return default value: {}'.format(key, default))
            return default

    def is_config_key_exists(self, key):
        try:
            self.get_config_val(key)
            return True
        except KeyError as e:
            return False

    def get_config_dict(self):
        return self.__config_dict
