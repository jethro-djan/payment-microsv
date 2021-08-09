from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_marshmallow import Marshmallow

app = Flask(__name__)
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(120))
    password = db.Column(db.String(60))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<User %r>' % User.username

class UserSchema(ma.Schema):
    class Meta:
        fields = ("name", "email", "created_at", "links")

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True, unique=True)
    payment_amt = db.Column(db.String)
    trans_created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("transactions", lazy=True))

    def __repr__(self):
        return '<Transaction %r>' % Transaction.transaction_id

class TransactionSchema(ma.Schema):
    class Meta:
        fields = ("transaction_id", "payment_amt", "trans_created_at")