from datetime import date, timedelta
from random import randint

from faker import Faker

from config import app, db
from models import User, Workout

fake = Faker()

with app.app_context():

    Workout.query.delete()
    User.query.delete()
    db.session.commit()

    users = []
    for name in ["duncan", "david", "cleo"]:
        user = User(username=name)
        user.password = "cleo123"
        users.append(user)
    db.session.add_all(users)
    db.session.commit()

    titles = ["Leg day", "Upper body", "Cardio", "Core", "Full body"]
    for user in users:
        for i in range(8):
            db.session.add(
                Workout(
                    title=titles[i % len(titles)],
                    notes=fake.sentence(),
                    duration_minutes=randint(20, 90),
                    date=date.today() - timedelta(days=i),
                    user=user,
                )
            )
    db.session.commit()
    print("Database seeded!")
