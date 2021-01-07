from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import PhoneNumber

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True
                        )
    phone_number = db.Column(db.Unicode(20))

    def __repr__(self):
        return '<User user_id=%s phone_number=%s>' % (
            self.user_id,
            self.phone_number,
        )


#     user = User(phone_number=PhoneNumber('0401234567', 'FI'))
#     user.phone_number.e164  # u'+358401234567'


class Entries(db.Model):
    __tablename__ = "entries"

    entries_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True
                           )
    date = Column(DateTime, default=func.now())
    rose_transcription_sid = db.Column(db.String)
    rose_recording_sid = db.Column(db.String)
    thorn_transcription_sid = db.Column(db.String)
    thorn_recording_sid = db.Column(db.String)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    users = db.relationship('User')

    def __repr__(self):
        return '<Entries entries_id=%s thorn_transcription_sid=%s thorn_recording_sid=%s \
            rose_transcription_sid=%s rose_recording_sid=%s rating=%s date=%s user_id=%s>' % (
            self.entries_id,
            self.rose_transcription_sid,
            self.rose_recording_sid,
            self.thorn_transcription_sid,
            self.thorn_recording_sid,
            self.rating,
            self.date,
            self.user_id
        )

