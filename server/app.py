from flask import request, session, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from config import app, db
from models import User, Workout
from schemas import UserSchema, WorkoutSchema

user_schema = UserSchema()
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)


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


if __name__ == "__main__":
    app.run(port=5555, debug=True)
