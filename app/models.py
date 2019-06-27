from datetime import datetime
from app import db
import hashlib, binascii, os


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def __repr__(self):
        return f'< User \
            {self.username} \
            {self.password_hash} >'

    def hash_password(password):
        salt = hashlib.sha256(os.environ.get('SECRET_KEY').encode('ascii')).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      password.encode('utf-8'),
                                      salt,
                                      100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def verify_password(stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password


class Macbook(db.Model):
    __tablename__ = 'macbooks'

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(32), index=True, unique=True)
    cpu = db.Column(db.String(32))
    cpu_cores = db.Column(db.Integer)
    cpu_clock = db.Column(db.String(16))
    ram = db.Column(db.String(16))
    location = db.Column(db.String(16))
    systems = db.relationship('System_Info', backref='systems', lazy='dynamic')
    apps = db.relationship('Application', backref='applications', lazy='dynamic')


    def __repr__(self):
        return f'< Macbook \
            {self.serial_number} \
            {self.cpu} \
            {self.cpu_cores} \
            {self.cpu_clock} \
            {self.ram} >'

    def verify_duplicate_serial(serial_number):
        stored_serial_number = Macbook.query.filter_by(serial_number=serial_number).first()
        if stored_serial_number is None:
            return None
        else:
            return serial_number == stored_serial_number.serial_number


class System_Info(db.Model):
    __tablename__ = 'system_info'

    id = db.Column(db.Integer, primary_key=True)
    os_version = db.Column(db.String(255))
    kernel_version = db.Column(db.String(255))
    hostname = db.Column(db.String(255))
    usernames = db.Column(db.String(255))
    date_stored = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    macbook_id = db.Column(db.Integer, db.ForeignKey('macbooks.id'))

    def __repr__(self):
        return f'< System Info \
            {self.os_version} \
            {self.kernel_version} \
            {self.hostname} \
            {self.usernames} \
            {self.date_stored} >'


class Application(db.Model):
    __tablename__ = 'apps'

    id = db.Column(db.Integer, primary_key=True)
    application_name = db.Column(db.String(255))
    pkg_source = db.Column(db.String(128))
    last_modified = db.Column(db.DateTime, index=True)
    macbook_id = db.Column(db.Integer, db.ForeignKey('macbooks.id'))
    versions = db.relationship('Application_Version', backref='versions', lazy='dynamic')

    def __repr__(self):
        return f'< Apps \
            {self.application_name} \
            {self.last_modified} \
            {self.pkg_source} \
            {self.macbook_id} >'

    def verify_duplicate_app(serial, app_name):
        check_app = Application.query.filter_by(application_name=app_name, macbook_id=serial.id).first()
        if check_app is None:
            return None
        else:
            return check_app.application_name == app_name


class Application_Version(db.Model):
    __tablename__ = 'app_versions'

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(255))
    date_stored = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'))

    def __repr__(self):
        return f'< Version \
            {self.version} \
            {self.date_stored} \
            {self.app_id} >'
