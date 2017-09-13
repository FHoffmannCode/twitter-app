import datetime
import json

import tweepy
from app import db
from sqlalchemy.types import VARCHAR, TypeDecorator


class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string.

    Usage::

        JSONEncodedDict(255)

    """

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, nullable=False)
    twitter_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    oauth_token = db.Column(db.String(128), index=True, unique=True)
    oauth_token_secret = db.Column(db.String(128), index=True, unique=True)
    followers_of_followers = db.Column(JSONEncodedDict(255), index=True)
    last_update_timestamp = db.Column(db.DateTime, index=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @staticmethod
    def user_from_twitter_data(twitter_user, auth):
        """
        @type twitter_user: tweepy.models.User
        @type: auth: tweepy.OAuthHandler
        """
        return User(
            nickname=twitter_user.screen_name, twitter_id=twitter_user.id, oauth_token=auth.access_token,
            oauth_token_secret=auth.access_token_secret)

    def __repr__(self):
        return '<User %r>' % self.nickname
