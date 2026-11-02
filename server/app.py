from flask import request, session, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from functools import wraps

from config import app, db
from models import User, Workout
from schemas import UserSchema, WorkoutSchema

user_schema = UserSchema()
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        user = db.session.get(User, user_id) if user_id else None
        if user is None:
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)

    return wrapper


def current_user():
    return db.session.get(User, session["user_id"])


@app.route("/signup", methods=["POST"])
def signup():
    json_data = request.get_json(silent=True)
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    try:
        user = User(username=data["username"])
        user.password = data["password"]
        db.session.add(user)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 422
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username already taken"}), 422

    session["user_id"] = user.id
    return jsonify(user_schema.dump(user)), 201


@app.route("/login", methods=["POST"])
def login():
    json_data = request.get_json(silent=True) or {}
    user = User.query.filter_by(username=json_data.get("username")).first()

    if user is None or not user.authenticate(json_data.get("password", "")):
        return jsonify({"error": "Invalid username or password"}), 401

    session["user_id"] = user.id
    return jsonify(user_schema.dump(user)), 200


@app.route("/logout", methods=["DELETE"])
def logout():
    session.pop("user_id", None)
    return "", 204


@app.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")
    user = db.session.get(User, user_id) if user_id else None

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(user_schema.dump(user)), 200


@app.route("/workouts", methods=["GET"])
@login_required
def get_workouts():
    user = current_user()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)
    per_page = max(1, min(per_page, 50))  # keep it between 1 and 50

    pagination = (
        Workout.query.filter_by(user_id=user.id)
        .order_by(Workout.date.desc(), Workout.id.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return (
        jsonify(
            {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "items": workouts_schema.dump(pagination.items),
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(port=5555, debug=True)
