# FastAPI Weather Service

A simple microservice built with FastAPI, SQLAlchemy, and Docker that **collects weather data every hour** and provides an API to retrieve hourly temperature and conditions for a specific day.

## 📦 Features

* **Hourly data collection**: Automatically fetches current weather from OpenWeather One Call API at the top of every hour (e.g., 00:00, 01:00, 02:00, etc.).
* **Persistent storage**: Saves records in SQLite via SQLAlchemy with the following fields:

  * **city**: City name
  * **timestamp**: Time of the reading
  * **temp**: Temperature (Kelvin)
  * **weather\_main**: Main weather condition (e.g., Rain, Clouds)
* **API endpoint**: `GET /history?day=YYYY-MM-DD` returns an array of hourly records for the given date.
* **Authentication**: Requests must include a constant 32-character `x-token` header.
* **Swagger UI**: Interactive documentation available at `/docs`.

## 🚀 Quick Start with Docker

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```

2. **Copy and configure environment**

   ```bash
   cp .env.example .env
   # Edit .env and fill in your values
   ```

3. **Build and run**

   ```bash
   docker-compose up --build -d
   ```

4. **Verify**

   * Open Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   * Example request:

     ```bash
     curl -H "x-token: $EXPECTED_TOKEN" \
          "http://127.0.0.1:8000/history?day=$(date +%F)"
     ```

That’s it — the service will start collecting data immediately and then at the top of every hour.

## 🛠 Local Development (Without Docker)

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy and configure `.env`:

   ```bash
   cp .env.example .env
   ```

3. Run the application:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 🔧 Environment Variables (`.env`)

| Variable        | Description                                              |
| --------------- | -------------------------------------------------------- |
| CITY\_NAME      | City name (e.g., "Kiev")                                 |
| CITY\_LAT       | City latitude                                            |
| CITY\_LON       | City longitude                                           |
| API\_KEY        | Your OpenWeather API key                                 |
| EXPECTED\_TOKEN | 32-character token required in `x-token` header          |
| DATABASE\_URL   | SQLAlchemy database URL (e.g., `sqlite:///./weather.db`) |

## 📂 Project Structure

```
FastAPIWeatherService/
├── .env.example         # Example environment file
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── app
    ├── db.py            # Database connection and setup
    ├── models.py        # SQLAlchemy ORM models
    └── main.py          # FastAPI application
```

## 📄 License

MIT © <Vladislav Drozd>
