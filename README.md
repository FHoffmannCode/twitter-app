# twitter-app
App that shows followers of user's followers

App can work locally or run on heroku however to use it by yourself you must register your own app on twitter and fill config files with
consumer and consumer secret keys.

I'm going to assume that you know how to register new app on heroku and how to use heroku CLI. 
If not visit - https://devcenter.heroku.com/articles/getting-started-with-python#introduction

1. Registering app on twitter:
  a) just set right callback url - http://127.0.0.1:5000/authorized or <heroku app url>/authorized.

2. Configuring app:
  in app/conf dir there are two files - base_conf.py and config_template.py. Rename config_template.py and ConfigTemplate class
  to local_config.py and LocalConfig.py and fill in the customer and customer secret keys with keys that twitter gave you
  when you registered an app there. Fill in secret key value - it can be anything you want, just make sure its complicated
  if you want to deploy this app - its needed to secure Flask session.
  
3. init db - locally just run python db_create.py, heroku:
  a) set up db - 'heroku addons:create heroku-postgresql'
  b) init db - 'heroku run init'

4. start the app: local - python run.py, heroku - heroku ps:scale web=1

NOTE: 
This app is meant to work with 'average' person account which means that if by any chance you're extremely popular and have like 1k followers it may not work properly. Why? In theory if you run app locally it SHOULD be able to fetch every single follower of your followers even if you have many of them but it will take a very long time due to Twitter API limits and there's significant chance that a connection error will occur during this time. On heroku though app wont be able to bypass limits because of heroku's custom 30s timeout. This can be fixed with moving this task to background worker but I think it'd be an overkill for such app.
