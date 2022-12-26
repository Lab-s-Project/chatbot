import datetime
from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """ User model """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    school_name = db.Column(db.String(255), nullable=False)
    grade = db.Column(db.String(50), nullable=False)
    class_no = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.now(),
                           nullable=False)
    updated_at = db.Column(db.DateTime,
                           default=datetime.datetime.now(),
                           nullable=False)
    status = db.Column(db.Integer, default=1, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.student_id


class Chat(db.Model):
    """ Chat model """

    __tablename__ = "chats"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.now(),
                           nullable=False)
