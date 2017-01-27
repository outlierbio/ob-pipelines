import logging

logger = logging.getLogger('ob-pipelines')

# Create the format
formatter = logging.Formatter('%(asctime)s - %(message)s')

# Add a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)
