from urllib import parse
from dash_spa.logging import log
from dash_spa import config
from random import randrange

from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy_utils import database_exists

from .admin_page import AdminPage
from .template_mailer import TemplateMailer
from .synchronised_cache import SynchronisedTTLCache
from .views.common import USER

from dash_spa.spa_current_user import set_current_user


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

options = config.get('login_manager')

class VerificationRecord:

    def __init__(self, name, email, password):
        self.code = self.randomCode()
        self.name = name
        self.email = email
        self.password = password
        set_current_user(current_user)

    def randomCode(self, length=4):
        return ''.join([chr(randrange(10) + 65) for n in range(length)])

class AdminLoginManager(LoginManager):

    enabled = options.get("enabled", False)

    def __init__(self, app=None, add_context_processor=True, slug='/admin'):
        super().__init__(app, add_context_processor)

        self.app = app
        self.slug = slug

        self.verification_cache = SynchronisedTTLCache(maxsize=1000, ttl=30*60)

        app.config['SQLALCHEMY_DATABASE_URI'] = options.database_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.db = SQLAlchemy()
        self.db.init_app(app)

        self.User = self.user_model(self.db)
        self.user_loader(self.load_user)

        if not database_exists(options.database_uri):
            app.app_context().push()
            self.db.create_all()
            self.db.session.commit()

        views = AdminPage(self)


    def path_for(self, endpoint, args=None):
        path = endpoint
        if args:
            path += '?' + parse.urlencode(args)
        return f"{self.slug}/{path}"


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
        return options.get('test', False)

    def isAdmin(self):
        try:
            return 'admin' in current_user.role
        except Exception:
            pass

        return False

    def get_user(self, email):

        @self.flask_context
        def _get_user():
            return self.User.query.filter_by(email=email).first()

        return _get_user()

    def delete_user(self, email):

        @self.flask_context
        def _delete_user():
            user = self.get_user(email)

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

    def create_verification_record(self, name, email, password):
        verification_record = VerificationRecord(name, email, password)
        self.verification_cache[email] = verification_record
        return verification_record

    def get_verification_record(self, email):
        if not email in self.verification_cache:
            return None
        return self.verification_cache[email]


    def register(self, name, email, password, terms):
        log.info('register [name: %s, email: %s, password: %s, terms: %s]', name, email, password, terms)

        user = self.get_user(email) # if this returns a user, then the email already exists in database

        if user:
            return USER.USER_ALLREADY_EXISTS

        vrec = self.create_verification_record(name, email, password)

        if options.verify_users:
            mailer = TemplateMailer(VERIFICATION_TEMPLATE, {'name' : name, 'code': vrec.code})
            mailer.send(email, 'Password verification', self.is_test())
            return USER.EMAIL_SENT
        else:
            self.validate(email, vrec.code)
            return USER.VALIDATED


    def validate(self, email, code):
        vrec = self.get_verification_record(email)
        if vrec and vrec.code == code:

            new_user = self.User(email=vrec.email, name=vrec.name, password=generate_password_hash(vrec.password, method='sha256'))

            self.db.session.add(new_user)
            self.db.session.commit()

            self.verification_cache[email] = None

            return USER.VALIDATED

        return USER.VALIDATION_FAILED

    def login(self, email, password, remember):
        log.info('login [email: %s, password: %s, remember: %s]', email, password, remember)

        user = self.get_user(email)

        if not user or not check_password_hash(user.password, password):
            return False

        login_user(user, remember=remember)
        return True

    def change_password(self, email, password):
        user = self.get_user(email)

        if user:
            user.password = generate_password_hash(password, method='sha256')
            self.db.session.add(user)
            self.db.session.commit()
            return True

        return False

    def forgot(self, email):

        log.info('forgot [email: %s]', email)

        user = self.get_user(email) # if this returns a user, then the email already exists in database

        if user is None:
            return False

        verification_record = VerificationRecord(user.name, user.email, user.password)
        self.verification_cache[email] = verification_record

        log.info('code: %s', verification_record.code)

        mailer = TemplateMailer(FORGOT_TEMPLATE, {'code': verification_record.code})
        mailer.send(email, 'Password verification', self.is_test())

        return True

    def forgot_code_valid(self, code, email):

        if not email in self.verification_cache:
            return False

        vrec = self.verification_cache[email]
        return vrec.code == code.upper()

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

