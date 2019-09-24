from utils import config, log
from random import randrange
from .template_mailer import TemplateMailer

from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from app import app

VERIFICATION_TEMPLATE = """
Hi {{name}}

You recently requested to create a Dash/SPA account. In order to complete
the registration process please enter the following code:

        {{code}}
                          
This code is only valid for the next 30  minutes. 

If you did not request an account, please ignore this
email or reply to let us know.
"""

FORGOT_TEMPLATE = """

You recently requested to reset the password on your Dash/SPA account. In order
to complete the reset process please enter the following code:

        {{code}}
                          
This code is only valid for the next 30  minutes. 

If you did not request an account, please ignore this
email or reply to let us know.
"""

mail_options = config.get('mail_options')
user_db = config.get('user_db')

def randomCode(length=4):
    return ''.join([chr(randrange(10) + 65) for n in range(length)])

class AdminLoginManager(LoginManager):

    def __init__(self, app=None, add_context_processor=True):
        super().__init__(app, add_context_processor)

        self.code = None
        self.email = None

        app.config['SQLALCHEMY_DATABASE_URI'] = user_db.database_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.db = SQLAlchemy()
        self.db.init_app(app)

        self.User = self.user_model(self.db)
        self.user_loader(self.load_user)


    def register(self, name, email, password, terms):

        log.info('register [name: %s, email: %s, password: %s, terms: %s]', name, email, password, terms)

        user = self.User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user:
            return False

        self.code = randomCode()
        self.name = name
        self.email = email
        self.password = password

        mailer = TemplateMailer(VERIFICATION_TEMPLATE, {'name' : name, 'code': self.code})
        mailer.send(mail_options.sender, email, 'Password verification')
        return True

    def validate(self, code):

        if self.code and (self.code == code):

            new_user = self.User(email=self.email, name=self.name, password=generate_password_hash(self.password, method='sha256'))

            self.db.session.add(new_user)
            self.db.session.commit()

            return True

        return False

    def login(self, email, password, remember):
        log.info('login [email: %s, password: %s, remember: %s]', email, password, remember)

        user = self.User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return False

        log.info('Valid user %s', user)
        login_user(user, remember=remember)
        return True

    def change_password(self, email, password):
        user = self.User.query.filter_by(email=email).first()

        if user:
            user.password = generate_password_hash(password, method='sha256')
            self.db.session.add(user)
            self.db.session.commit()
            return True

        return False

    def forgot(self, email):

        log.info('forgot [email: %s]', email)

        user = self.User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user is None:
            return False

        self.code = randomCode(4)
        self.email = email

        log.info('code: %s', self.code)

        mailer = TemplateMailer(FORGOT_TEMPLATE, {'code': self.code})
        mailer.send(mail_options.sender, email, 'Password verification')

        return True

    def forgot_code_valid(self, code, email=None):
        if email and email != self.email:
            return False
        return self.code == code.upper()

    def get_email(self):
        return self.email

    def reload_user(self, user=None):
        log.info('reload_user user=%s', user)
        super().reload_user(user)
        return current_user


    def load_user(self, user_id):
        log.info('load_user: %s', user_id)
        return self.User.query.get(int(user_id))

    def logout_user(self):
        log.info('logout_user')
        logout_user()


    def user_model(self, db):

        class _User(UserMixin, db.Model):
            id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
            email = db.Column(db.String(100), unique=True)
            password = db.Column(db.String(100))
            name = db.Column(db.String(1000))  

        return _User

login_manager = AdminLoginManager(app.server)
