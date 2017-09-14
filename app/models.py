import tweepy
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(64), index=True, nullable=False)
    twitter_id = db.Column(db.BigInteger, index=True, unique=True, nullable=False)
    oauth_token = db.Column(db.String(128), index=True, unique=True)
    oauth_token_secret = db.Column(db.String(128), index=True, unique=True)

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
