import os
from holoniq.utils import config, log
from random import randrange
from cachetools import TTLCache
from .template_mailer import TemplateMailer

from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy_utils import database_exists

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

class VerificationRecord:

    def __init__(self, name, email, password):
        self.code = randomCode()
        self.name = name
        self.email = email
        self.password = password

def randomCode(length=4):
    return ''.join([chr(randrange(10) + 65) for n in range(length)])

class AdminLoginManager(LoginManager):

    def __init__(self, app=None, add_context_processor=True):
        super().__init__(app, add_context_processor)

        self.app = app

        self.verification_cache = TTLCache(maxsize=1000, ttl=30*60)
        self.test_mode = os.environ.get("FLASK_ENV", "production") == "test"

        app.config['SQLALCHEMY_DATABASE_URI'] = user_db.database_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.db = SQLAlchemy()
        self.db.init_app(app)

        self.User = self.user_model(self.db)
        self.user_loader(self.load_user)

        if not database_exists(user_db.database_uri):
            app.app_context().push()
            self.db.create_all()
            self.db.session.commit()
            # self.add_user("admin", "admin@holoniq.com", "passme99")


    def flask_context(self, fn):
        def _wrapper(*args, **kwargs):
            ctx = None
            try:
                ctx = self.app.app_context()
                ctx.push()
                return fn(*args, **kwargs)
            finally:
                ctx.pop()
        return _wrapper

    def database_uri(self):
        return self.app.config['SQLALCHEMY_DATABASE_URI']

    def is_test(self):
        return self.test_mode

    def isAdmin(self):

        try:
            return 'admin' in current_user.role
        except Exception:
            pass

        return False

    def delete_user(self, email):

        @self.flask_context
        def _delete_user():
            user = self.User.query.filter_by(email=email).first()

            if not user:
                raise Exception('Invalid user')

            self.db.session.delete(user)
            self.db.session.commit()

        return _delete_user()

    def add_user(self, name, email, password, role=[]):

        @self.flask_context
        def _add_user():

            roles = ','.join(role) if isinstance(role, list) else role

            new_user = self.User(email=email, name=name, password=generate_password_hash(password, method='sha256'), role=roles)
            self.db.session.add(new_user)
            self.db.session.commit()
            return True

        return  _add_user()


    def update_user(self, id, name, email, password, role=[]):

        @self.flask_context
        def _update_user():

            user = self.User.query.filter_by(id=id).first()

            if not user:
                raise Exception('Invalid user')

            user.role = ','.join(role) if isinstance(role, list) else role
            user.password = generate_password_hash(password, method='sha256')
            user.name = name
            user.email = email


            self.db.session.add(user)
            self.db.session.commit()
            return True

        return  _update_user()

    def register(self, name, email, password, terms):
        log.info('register [name: %s, email: %s, password: %s, terms: %s]', name, email, password, terms)

        user = self.User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user:
            return False

        verification_record = VerificationRecord(name, email, password)
        self.verification_cache[email] = verification_record

        mailer = TemplateMailer(VERIFICATION_TEMPLATE, {'name' : name, 'code': verification_record.code})
        mailer.send(mail_options.sender, email, 'Password verification', self.is_test())

        return True

    def validate(self, email, code):

        if not email in self.verification_cache:
            return False

        vrec = self.verification_cache[email]

        if vrec.code == code:

            new_user = self.User(email=vrec.email, name=vrec.name, password=generate_password_hash(vrec.password, method='sha256'))

            self.db.session.add(new_user)
            self.db.session.commit()

            self.verification_cache[email] = None

            return True

        return False

    def login(self, email, password, remember):
        log.info('login [email: %s, password: %s, remember: %s]', email, password, remember)

        user = self.User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return False

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
        mailer.send(mail_options.sender, email, 'Password verification', self.is_test())

        return True

    def forgot_code_valid(self, code, email=None):
        if email and email != self.email:
            return False
        return self.code == code.upper()

    def get_email(self):
        return self.email

    def reload_user(self, user=None):
        # log.info('reload_user user=%s', user)
        super().reload_user(user)
        return current_user

    def load_user(self, user_id):
        user = self.User.query.get(int(user_id))
        # log.info('load_user: id=%s, email=%s', user_id, user.email)
        return user

    def logout_user(self):
        log.info('logout_user')
        logout_user()

    def user_count(self):

        @self.flask_context
        def _user_count():
            return self.User.query.count()

        return _user_count()

    def users(self):

        @self.flask_context
        def _users():
            return self.User.query.all()

        return _users()

    def user_model(self, db):

        class _User(UserMixin, db.Model):
            id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
            email = db.Column(db.String(100), unique=True)
            password = db.Column(db.String(100))
            name = db.Column(db.String(1000))
            role = db.Column(db.String(100))

        return _User
