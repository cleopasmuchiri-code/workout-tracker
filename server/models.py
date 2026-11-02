from sqlalchemy.orm import validates

from config import db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    workouts = db.relationship(
        "Workout", back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def password(self):
        raise AttributeError("Password is write-only")

    @password.setter
    def password(self, plain_text):
        self._password_hash = bcrypt.generate_password_hash(plain_text).decode("utf-8")

    def authenticate(self, plain_text):
        return bcrypt.check_password_hash(self._password_hash, plain_text)

    @validates("username")
    def validate_username(self, key, value):
        if not value or not value.strip():
            raise ValueError("Username is required")
        return value.strip()


class Workout(db.Model):
    __tablename__ = "workouts"
    __table_args__ = (
        db.CheckConstraint("duration_minutes > 0", name="ck_workout_duration_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    notes = db.Column(db.Text)
    duration_minutes = db.Column(db.Integer)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="workouts")

    @validates("title")
    def validate_title(self, key, value):
        if not value or not value.strip():
            raise ValueError("Title is required")
        return value.strip()

    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("duration_minutes must be greater than 0")
        return value
