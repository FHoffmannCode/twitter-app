import os

from app.conf.base_config import BaseConfig


class ProductionConfig(BaseConfig):
    OAUTH_CONFIG = {
        'TWITTER': {
            'CONSUMER_KEY': 'KGZDf9ht7lRw6QD7if2pzxypf',
            'CONSUMER_SECRET': '5eflrjZ8n0AVwha16mCLzm2B3br8fT3MU4ktrAYkdPRwv4jc19',
            'CALLBACK_URL': 'https://twitter-followers-app.herokuapp.com/'
        },
    }
    SECRET_KEY = 'FCkJFRS5BXpoWFpo5FQvwCu85B7HQpMo'
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))
