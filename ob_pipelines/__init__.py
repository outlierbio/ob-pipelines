import logging
import os

logger = logging.getLogger('ob-pipelines')

# Create the format
formatter = logging.Formatter('%(asctime)s - %(message)s')

# Add a console handler
ch = logging.StreamHandler()
ch.setLevel(os.environ.get('LOGGING_LEVEL') or logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
