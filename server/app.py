from config import app, db
from models import User, Workout

if __name__ == "__main__":
    app.run(port=5555, debug=True)
