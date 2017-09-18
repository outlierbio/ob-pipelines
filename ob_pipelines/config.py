import os
import os.path as op

import yaml

import ob_pipelines

# All configuration is matched to an AWS_PROFILE
AWS_PROFILE = os.environ.get('AWS_PROFILE', 'default')
CONFIG_FILE = op.join(op.dirname(ob_pipelines.__file__), '..', 'config.yml')
with open(CONFIG_FILE) as f:
    cfg = yaml.load(f)[AWS_PROFILE]
cfg['AWS_PROFILE'] = AWS_PROFILE
