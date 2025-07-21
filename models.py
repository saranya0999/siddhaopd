from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, dataentry, viewer

class CensusEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_date = db.Column(db.Date, nullable=False, unique=True)
    # Morning Old/New Cases
    m_old_male = db.Column(db.Integer)
    m_old_female = db.Column(db.Integer)
    m_old_child = db.Column(db.Integer)
    m_new_male = db.Column(db.Integer)
    m_new_female = db.Column(db.Integer)
    m_new_child = db.Column(db.Integer)
    # Evening Old/New Cases
    e_old_male = db.Column(db.Integer)
    e_old_female = db.Column(db.Integer)
    e_old_child = db.Column(db.Integer)
    e_new_male = db.Column(db.Integer)
    e_new_female = db.Column(db.Integer)
    e_new_child = db.Column(db.Integer)
