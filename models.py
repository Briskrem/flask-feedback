from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False )
    password = db.Column(db.Text, nullable=False )
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode('utf8')
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user:
            print(user.username)
            print(user.password)
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


    
class Feedback(db.Model):

    __tablename__='feedbacks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # it references the username instead of the id this time around.
    username = db.Column(db.ForeignKey('users.username', ondelete='CASCADE'))
    
    usr = db.relationship('User', backref=backref("feedbacks", cascade="all, delete-orphan"))
