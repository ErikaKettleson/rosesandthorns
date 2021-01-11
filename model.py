from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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


class Ratings(db.Model):
    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True
                          )
    call_sid = db.Column(db.String)
    rating = db.Column(db.Integer)
    date = Column(DateTime, default=func.now())
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    users = db.relationship('User')

    def __repr__(self):
        return '<Entries entries_id=%s call_sid=%s rating=%s date=%s user_id=%s>' % (
            self.entries_id,
            self.call_sid,
            self.rating,
            self.date,
            self.user_id
        )


class Entries(db.Model):
    __tablename__ = "entries"

    entries_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True
                           )
    call_sid = db.Column(db.String)
    transcription_sid = db.Column(db.String)
    recording_sid = db.Column(db.String)
    entry_type = db.Column(db.String)
    date = Column(DateTime, default=func.now())
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    users = db.relationship('User')

    def __repr__(self):
        return '<Entries entries_id=%s call_sid=%s transcription_sid=%s \
            recording_sid=%s entry_type=%s date=%s user_id=%s>' % (
            self.entries_id,
            self.call_sid,
            self.transcription_sid,
            self.recording_sid,
            self.entry_type,
            self.date,
            self.user_id
        )
