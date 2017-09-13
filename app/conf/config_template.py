import os

from app.conf.base_config import BaseConfig


class ConfigTemplate(BaseConfig):
    """
    Usage: copy this file and name the copy local_config.py (for development) or production_config.py (for production), 
    change class name from ConfigTemplate to LocalConfig (or ProductionConfig). If you want to set up this app locally
    or deploy it to heroku you will need to register an app on twitter to obtain consumer_key and consumer_secret_key.
    """
    DEBUG = True
    OAUTH_CONFIG = {
        'TWITTER': {
            'CONSUMER_KEY': 'my_consumer_key',
            'CONSUMER_SECRET': 'my_consumer_secret_key',
        },
    }
    SECRET_KEY = 'my_secret_key'
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))
