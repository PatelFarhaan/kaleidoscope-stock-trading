# Kaleidoscope

A full-stack stock trading blotter application built with Flask and MongoDB. Users can register, log in, and execute buy/sell trades on simulated equities, with real-time portfolio tracking and transaction history.

## Tech Stack

- **Language:** Python 3.8+
- **Framework:** Flask
- **Database:** MongoDB (via MongoEngine ODM)
- **Authentication:** Flask-Login
- **Serialization:** Flask-Marshmallow
- **Forms:** Flask-WTF
- **Frontend:** Bootstrap, jQuery, Moment.js

## Features

- User registration and authentication with hashed passwords
- Trade blotter for executing buy and sell orders
- Support for position-based and quantity-based order types
- Real-time portfolio holdings tracking
- Transaction history log
- Initial test data population with sample equities (SPY, QQQ, HYG)
- Custom error pages (403, 404, 405, 500)

## Prerequisites

- Python 3.8 or higher
- MongoDB running locally or a remote MongoDB instance
- pip

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Kaleidoscope
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the environment file and configure:
   ```bash
   cp .env.example .env
   ```

5. Ensure MongoDB is running:
   ```bash
   mongod
   ```

## Environment Variables

| Variable      | Description                  | Default                    |
|---------------|------------------------------|----------------------------|
| `SECRET_KEY`  | Flask session secret key     | `change-me-in-production`  |
| `MONGODB_URI` | MongoDB connection string    | `mongodb://localhost/trade` |
| `FLASK_ENV`   | Flask environment mode       | `development`              |
| `FLASK_DEBUG` | Enable debug mode            | `1`                        |

## How to Run

```bash
python app.py
```

The server will start at `http://127.0.0.1:5000`.

## API Endpoints

| Method | Endpoint          | Description                        | Auth Required |
|--------|-------------------|------------------------------------|---------------|
| GET    | `/`               | Login page                         | No            |
| POST   | `/`               | Process login                      | No            |
| GET    | `/register`       | Registration page                  | No            |
| POST   | `/register`       | Create new user                    | No            |
| GET    | `/trade-blotter`  | View trade blotter and portfolio   | Yes           |
| POST   | `/trade-blotter`  | Execute a trade                    | Yes           |
| GET    | `/logout`         | Log out current user               | Yes           |

## Project Structure

```
Kaleidoscope/
├── app.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── common_utilities/
│   ├── __init__.py                 # Configuration constants
│   ├── blotter.py                  # Trade execution logic
│   └── data_populate.py            # Initial data seeding
├── project/
│   ├── __init__.py                 # Flask app factory and config
│   ├── models.py                   # MongoDB document models
│   ├── error/
│   │   └── error_handler.py        # Custom error handlers
│   ├── trade/
│   │   ├── __init__.py
│   │   ├── views.py                # Trade routes and logic
│   │   └── serializer.py           # Marshmallow schemas
│   ├── templates/                  # Jinja2 HTML templates
│   └── static/                     # CSS, JS, fonts
├── .env.example                    # Environment variable template
├── .gitignore                      # Git ignore rules
├── Dockerfile                      # Container configuration
├── Makefile                        # Common development commands
└── README.md                       # Project documentation
```

## License

MIT License
