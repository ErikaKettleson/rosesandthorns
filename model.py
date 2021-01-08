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


class Entries(db.Model):
    __tablename__ = "entries"

    entries_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True
                           )
    call_sid = db.Column(db.String)
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
        return '<Entries entries_id=%s call_sid=%s thorn_transcription_sid=%s thorn_recording_sid=%s \
            rose_transcription_sid=%s rose_recording_sid=%s rating=%s date=%s user_id=%s>' % (
            self.entries_id,
            self.call_sid,
            self.rose_transcription_sid,
            self.rose_recording_sid,
            self.thorn_transcription_sid,
            self.thorn_recording_sid,
            self.rating,
            self.date,
            self.user_id
        )

