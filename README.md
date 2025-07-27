# Vehicle Parking App – V1 (MAD-1, IIT Madras)
Root folder: **parking_app_24f1001605**

## Tech Stack
- **Backend**: Flask
- **Frontend**: Jinja2, HTML, CSS, Bootstrap, Chart.js
- **Database**: SQLite (SQLAlchemy ORM)
- **Auth**: flask-login (Admin pre-seeded, User can register)

## Features
### Admin
- Add/Edit/Delete Parking Lots (with auto-generated spots)
- Delete only if all spots are free
- View dashboard with:
  - Lots and spot statuses
  - Which user occupies which spot
  - All registered users
  - Summary charts: Occupied vs Available spots per lot, Revenue per lot
- Search by parking spot ID

### User
- Register / Login
- Choose a lot → system allocates first available spot
- Book / Occupy / Release with cost calculated as `ceil(hours) * price_per_hour`
- Dashboard with active booking and history (plus history chart)

### Minimal REST API
- `GET /api/lots`
- `GET /api/spots/<id>`
- `GET /api/reservations/me` (auth required)

## Run Locally

```bash
cd parking_app_24f1001605
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python app.py
```

**Note**: The app runs on port 5000. If you get a port conflict on macOS, try disabling AirPlay Receiver in System Settings.

## Default Admin Credentials
- Username: `admin`
- Password: `admin123`
