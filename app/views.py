from app import app, db, lm
from app.models import User
from app.pagination import Pagination
from flask import (abort, flash, redirect, render_template, request, session,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user
from tweepy import API, OAuthHandler, RateLimitError, TweepError

TWITTER_CONFIG = app.config['OAUTH_CONFIG']['TWITTER']
RESULTS_PER_PAGE = 20


@lm.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


@app.route('/')
def main_page():
    if current_user.is_authenticated:
        return redirect(url_for('see_followers'))
    return render_template('index.html')


@app.route('/auth')
def auth():
    auth = get_auth_handler()
    url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(url)


@app.route('/authorized')
def authorized():
    verifier = request.args.get('oauth_verifier')
    api = get_twitter_api(verifier)
    twitter_user = api.me()
    user = User.query.filter_by(twitter_id=twitter_user.id).first()
    if user:
        update_user_tokens(user, api.auth)
    else:
        user = User.user_from_twitter_data(twitter_user, api.auth)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('see_followers'))


@app.route('/see_followers')
@login_required
def see_followers():
    return render_template('see_followers.html')


@app.route('/fetch_followers')
@login_required
def fetch_followers():
    auth = get_auth_handler(current_user.oauth_token, current_user.oauth_token_secret)
    wait_on_rate_limit = True if request.args.get('wait_on_rate_limit') == u'true' else False
    api = API(auth, wait_on_rate_limit=wait_on_rate_limit)
    session['followers_of_followers'] = get_followers_of_followers(api, api.me())
    return redirect(url_for('view_follower_followers'))


@app.route('/follower_followers', defaults={'page': 1})
@app.route('/follower_followers/page/<int:page>')
@login_required
def view_follower_followers(page):
    followers_for_page = get_followers_for_page(page)
    all_followers_count = len(session['followers_of_followers'])
    if not followers_for_page and page != 1:
        abort(404)
    if all_followers_count <= RESULTS_PER_PAGE:
        pagination = None
    else:
        pagination = Pagination(page, RESULTS_PER_PAGE, all_followers_count)
    return render_template('follower_followers.html', pagination=pagination, followers_of_followers=followers_for_page)


def get_twitter_api(verifier):
    """
    @type verifier: str 
    @rtype: API
    """
    auth = get_auth_handler()
    auth.request_token = session['request_token']
    session.pop('request_token')
    auth.get_access_token(verifier)
    return API(auth)


def get_auth_handler(access_token=None, access_secret=None):
    """
    @type access_token: str | None
    @type access_secret: str | None
    @rtype: OAuthHandler 
    """
    auth = OAuthHandler(TWITTER_CONFIG['CONSUMER_KEY'], TWITTER_CONFIG['CONSUMER_SECRET'])
    if access_token is None or access_secret is None:
        return auth
    auth.set_access_token(access_token, access_secret)
    return auth


def update_user_tokens(user, auth):
    """
    @type user: User 
    @type auth: OAuthHandler
    """
    user.oauth_token = auth.access_token
    user.oauth_token_secret = auth.access_token_secret
    db.session.commit()


def get_followers_of_followers(api, user):
    """
    @type api: API
    @type user: tweepy.models.User
    @rtype: list[dict]
    """
    followers_data = {}
    followers = get_followers(api, user)
    if followers is None:
        flash('Rate limit exceeded, try again in 15 minutes')
        return []
    for follower in followers:
        try:
            follower_followers = get_followers(api, follower)
        except TweepError:
            continue
        if follower_followers is None:
            flash(
                ('Rate limit exceeded, your followers have too many followers but '
                 'we\'ll show you as much of them as we were able to fetch'))
            break
        for follower_follower in follower_followers:
            if followers_data.get(follower_follower.id) is not None:
                followers_data[follower_follower.id]['follows_count'] += 1
            else:
                followers_data[follower_follower.id] = {'user': follower_follower.screen_name, 'follows_count': 1}
    return [follower_follower for follower_follower in followers_data.itervalues()]


def get_followers(api, user):
    """
    @type api: API
    @type user: tweepy.models.User
    @rtype: list[tweepy.models.User]
    """
    try:
        followers = api.followers(user.id)
    except RateLimitError:
        return None
    return followers


def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)
app.jinja_env.globals['url_for_other_page'] = url_for_other_page


def get_followers_for_page(page):
    """
    @type page: int
    @rtype: list[User]
    """
    followers_of_followers = session['followers_of_followers']
    if len(followers_of_followers) == 0 or len(followers_of_followers) <= RESULTS_PER_PAGE:
        return followers_of_followers
    return followers_of_followers[
           (page - 1) * RESULTS_PER_PAGE: min((page * RESULTS_PER_PAGE, len(followers_of_followers)))]


def get_followers_by_twitter_id(api, twitter_id):
    """
    for testing/debugging purposes only
    """
    return api.followers(twitter_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out successfully')
    return redirect(url_for('main_page'))


@app.route('/login')
def login():
    return redirect(url_for('main_page'))
