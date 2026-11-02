# Workout Tracker API

A Flask REST API for tracking personal workouts. Users sign up, log in, and
manage their own workouts. Authentication uses server-side sessions (signed
cookies) and passwords are hashed with bcrypt. Users can only see and change
their own data.

## Tech stack

Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Bcrypt, Marshmallow, Faker, SQLite

## Installation

1. Clone the repository and move into it:
   ```bash
   git clone https://github.com/cleopasmuchiri-code/workout-tracker.git
   cd workout-tracker
   ```
2. Install dependencies and open the environment (Python 3.11 recommended):
   ```bash
   pipenv install
   pipenv shell
   ```
3. Set up the database and seed it:
   ```bash
   cd server
   flask db upgrade head
   python seed.py
   ```

The seed creates three users (`cleo`, `duncan`, `david`), all with the password
`cleo123`, and 8 workouts for each.

## Running the app

From the `server/` directory:

```bash
python app.py
```

The API runs at `http://localhost:5555`.

For production, set a secret key first: `export SECRET_KEY="your-long-random-string"`

## Endpoints

### Authentication

| Method | Path | Description | Success | Errors |
|---|---|---|---|---|
| POST | `/signup` | Create a user and log them in. Body: `username`, `password` | 201 | 400, 422 |
| POST | `/login` | Log in. Body: `username`, `password` | 200 | 401 |
| DELETE | `/logout` | Log out (clears the session) | 204 | |
| GET | `/check_session` | Return the logged-in user | 200 | 401 |

### Workouts (login required)

| Method | Path | Description | Success | Errors |
|---|---|---|---|---|
| GET | `/workouts` | List your workouts, paginated: `?page=1&per_page=5` | 200 | 401 |
| POST | `/workouts` | Create a workout. Body: `title` (required), `notes`, `duration_minutes`, `date` | 201 | 400, 401, 422 |
| PATCH | `/workouts/<id>` | Update part of one of your workouts | 200 | 400, 401, 404, 422 |
| DELETE | `/workouts/<id>` | Delete one of your workouts | 204 | 401, 404 |

A request for another user's workout returns 404.

### Paginated response format

```json
{
  "page": 1,
  "per_page": 5,
  "total": 8,
  "pages": 2,
  "items": [ ... ]
}
```
