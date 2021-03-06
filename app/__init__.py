from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


import os
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir,ADMINS,MAIL_SERVER,MAIL_PORT,MAIL_USERNAME,MAIL_PASSWORD
from flask_mail import Mail

mail = Mail(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

oid = OpenID(app, os.path.join(basedir, 'tmp'))

#To be set when we have an email server, and so can enable email logging of errors
mail_errors = False

if not app.debug and mail_errors:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME,MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER,MAIL_PORT),'noreply@' +MAIL_SERVER,ADMINS, 'microblog error', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log','a',1*1024*1024,10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')


from app import views,models
