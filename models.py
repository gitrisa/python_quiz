from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))

    last_score = db.Column(db.Integer)

    best_score = db.Column(db.Integer)

class Prediction(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    filename = db.Column(
        db.String(200)
    )

    prediction = db.Column(
        db.String(100)
    )

    confidence = db.Column(
        db.Float
    )