from flask import Flask
from flask import render_template
from flask import request
from models import db
from models import User
from models import Prediction
from flask import session
import os
import tensorflow as tf
from predict import predict_image

app = Flask(__name__)

app.secret_key = "pythonquiz2026"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.db"

db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        username = request.form["username"]

        q1 = request.form.get("q1")
        q2 = request.form.get("q2")
        q3 = request.form.get("q3")
        q4 = request.form.get("q4")
        q5 = request.form.get("q5")

        score = 0

        if q1 == "A":
            score += 1

        if q2 == "B":
            score += 1

        if q3 == "A":
            score += 1

        if q4 == "C":
            score += 1

        if q5 == "B":
            score += 1

        user = User.query.filter_by(
        username=username
    ).first()

        if user is None:

            user = User(
                username=username,
                last_score=score,
                best_score=score
            )

            db.session.add(user)

        else:

            user.last_score = score

            if score > user.best_score:

                user.best_score = score

        db.session.commit()
        session["username"] = username

        return render_template(
            "result.html",
            username=username,
            score=score,
            best_score=user.best_score,
            last_score=user.last_score)

    highest_user = User.query.order_by(
        User.best_score.desc()
    ).first()

    if highest_user:
        highest_score = highest_user.best_score
    else:
        highest_score = 0

    current_best = 0

    if "username" in session:

        current_user = User.query.filter_by(
            username=session["username"]
        ).first()

        if current_user:
            current_best = current_user.best_score

    return render_template(
        "index.html",
        best_score=highest_score,
        current_best=current_best
    )

@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        image = request.files["image"]

        if image.filename != "":

            os.makedirs("uploads", exist_ok=True)

            filepath = os.path.join(
                "uploads",
                image.filename
            )

            image.save(filepath)

            # -------------------------
            # Dummy Prediction
            # -------------------------

            prediction, confidence = predict_image(filepath)

            confidence = str(confidence) + "%"

            # -------------------------
            # Simpan ke Database
            # -------------------------

            new_prediction = Prediction(

                filename=image.filename,

                prediction=prediction,

                confidence=float(confidence[:-1])

            )

            db.session.add(new_prediction)

            db.session.commit()

            # -------------------------
            # Tampilkan hasil
            # -------------------------

            return render_template(

                "prediction.html",

                filename=image.filename,

                prediction=prediction,

                confidence=confidence

            )

    return render_template("upload.html")

@app.route("/check")
def check():

    predictions = Prediction.query.all()

    for p in predictions:

        print(
            p.filename,
            p.prediction,
            p.confidence
        )

    return "Done"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)