"""
This file contains the declarations of the models.
"""

from dataclasses import dataclass
from surflesson import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.dialects.mysql import TIME

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


users_lessons = db.Table('user_lesson',
                        db.Column('lesson_id', db.Integer, db.ForeignKey('lesson.id'), primary_key=True),
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                        )


@dataclass  # dataclass is used to allow for converting objects to JSON in the webservice
class User(db.Model, UserMixin):
    id: int
    username: str
    id = db.Column(db.Integer, primary_key=True)
    type_of_user = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    lessons = db.relationship('Lesson', secondary=users_lessons, lazy='subquery',
        backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"<User(id='{self.id}', username='{self.username}', email='{self.email}', image_file='{self.image_file}')>"


class LessonType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(280), nullable=False)

    lessons = db.relationship('Lesson', backref='lesson_type', lazy=True)


    def __repr__(self):
        return f"<Lesson_type(id='{self.id}', title='{self.title}', price='{self.price}', content='{self.content}')>"


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #date_for_lesson = db.Column(db.String(100), nullable=False)
    date_for_lesson = db.Column(db.DateTime, nullable=False)
    time_for_lesson = db.Column(db.String(100), nullable=False)
    lesson_type_id = db.Column(db.Integer, db.ForeignKey('lesson_type.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # lesson_types = db.relationship('LessonType',
    #    backref=db.backref('lessons', lazy=True))

    #author = db.relationship('User', backref=db.backref('lessons', lazy=True))

    # lessons = db.relationship('User', secondary=users_lessons, lazy='subquery',
    #      backref=db.backref('users', lazy=True))
    #
#    payment_type = db.Column(db.Integer, nullable=False)
#    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     lesson_type_id = db.Column(db.Integer, db.ForeignKey('lesson_type.id'),
#         nullable=False)


    def __repr__(self):
        return f"<Lesson(id='{self.id}', date_for_lesson='{self.date_for_lesson}', lesson_type_id='{self.lesson_type_id}')>"




@dataclass
class Message(db.Model):
    id: int
    content: str
    author: User

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship(User, backref=db.backref('messages', lazy=True))

    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    lesson = db.relationship(Lesson, backref=db.backref('messages',
                                                    order_by='Message.date_posted.desc()',
                                                    lazy=True,
                                                    cascade="all, delete-orphan"
                                                        ))


    def __repr__(self):
        return f"<Message(id='{self.id}', content='{self.content}', date_posted='{self.date_posted}', user_id='{self.user_id}', lesson_id='{self.lesson_id}')>"




