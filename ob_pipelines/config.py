import os
import os.path as op

import yaml
from logging import getLogger

import ob_pipelines

log = getLogger(__name__)

# All configuration is matched to an AWS_PROFILE
AWS_PROFILE = os.environ.get('AWS_PROFILE', 'default')
CONFIG_FILE = op.join(op.dirname(op.dirname(ob_pipelines.__file__)), 'config.yaml')
if op.exists(CONFIG_FILE):
    with open(CONFIG_FILE) as f:
        cfg = yaml.load(f)[AWS_PROFILE]
    cfg['AWS_PROFILE'] = AWS_PROFILE
else:
    log.warning("Config file wasn't found")
    cfg = {}


class ConfigManager:
    def __init__(self, config):
        self.config = config

    def get(self, option, default=None):
        return self.config.get(option, default)

    @property
    def db_connection(self):
        return self.get('DB_CONNECTION', "mongomock://localhost")


settings = ConfigManager(cfg)