# Smart Device Management API

## A Django REST Framework project for managing smart devices with PostgreSQL. This API supports device creation, retrieval, updates, and filtering.

# 🛠️ Tech Stack

- Backend: Django, Django REST Framework (DRF), django-filters
- Database: PostgreSQL
- Containerization: Docker (optional)
- Environment Variables: .env

# 📦 Installation & Setup
1. Clone Repository
```bash 
git clone https://github.com/Vaibhav0x/smart_device_platform.git
cd smart_device_plateform
```

2. Setup Virtual Environment 

(macOS / Linux)
```bash 
python3 -m venv venv

source venv/bin/activate
```

On Windows (PowerShell):
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Setup PostgreSQL (Linux/macOS)
Install PostgreSQL
```bash
sudo apt update && sudo apt install postgresql postgresql-contrib -y   # Ubuntu/Debian
brew install postgresql                                               # macOS
```

Create Database & User

```bash
sudo -u postgres psql
CREATE DATABASE smart_devices;
CREATE USER vaibhav WITH PASSWORD 'vaibhav';
ALTER ROLE vaibhav SET client_encoding TO 'utf8';
ALTER ROLE vaibhav SET default_transaction_isolation TO 'read committed';
ALTER ROLE vaibhav SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE smart_devices TO vaibhav;
\q

```

5. Configure .env

Create a file .env in project root:

```bash
POSTGRES_DB=smart_devices
POSTGRES_USER=vaibhav
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DEBUG=True
```

6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create Superuser
```bash
python manage.py createsuperuser
```

8. Run Development Server

```bash
python manage.py runserver
```

9. Base URL : `http://127.0.0.1:8000/api/`

## 📡 Authentication & JWT Flow

Signup (POST)

Endpoint: `/api/signup/`
Body:
```json
{
  "name": "Vaibhav Raj",
  "email": "vaibhav@example.com",
  "password": "vaibhav",
  "role": "user"
}
```


Response:
```json
{
  "message": "User created successfully"
}
```

Login (POST)

Endpoint: `/api/login/`
Body:
```json
{
  "email": "vaibhav@example.com",
  "password": "vaibhav"
}
```

Response:
```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>",
  "user": {
    "id": "d29ffd72-06c3-4774-8042-25b5e937c9c90",
    "name": "Vaibhav",
    "email": "vaibhav@example.com",
    "role": "user"
  }
}
```

Use the access token in Authorization headers for all protected endpoints.

Header format (Postman / client):

`Authorization: Bearer <access_token>`
`Content-Type: application/json`


1. Retrive Devices
GET `/api/devices/`

```json
[
  {
    "id": "dee3c9b6-cb38-419d-9c7c-c479a325c49e",
    "owner": "d29ffd72-06c3-4774-8042-25b5e937cb90",
    "name": "Living Room Light 3",
    "type": "light",
    "status": "active",
    "last_active_at": null,
    "created_at": "2025-08-19T19:05:01.750731Z",
    "updated_at": "2025-08-19T19:05:01.750731Z"
  }
]
```

2. Create Device

POST `/api/devices/`

Request:
```json
{
  "name": "Living Room Light",
  "type": "light",
  "status": "active"
}

```
Response:
```json
{
    "id": "dee3c9b6-cb38-419d-9c7c-c479a325c49e",
    "owner": "d29ffd72-06c3-4774-8042-25b5e937cb90",
    "name": "Living Room Light",
    "type": "light",
    "status": "active",
    "last_active_at": null,
    "created_at": "2025-08-19T19:05:01.750731Z",
    "updated_at": "2025-08-19T19:05:01.750731Z"
}
```


3. Retrieve Single Device

GET `/api/devices/dee3c9b6-cb38-419d-9c7c-c479a325c49e/`

Response:
```json
[
  {
    "id": "dee3c9b6-cb38-419d-9c7c-c479a325c49e",
    "owner": "d29ffd72-06c3-4774-8042-25b5e937cb90",
    "name": "Living Room Light",
    "type": "light",
    "status": "active",
    "last_active_at": null,
    "created_at": "2025-08-19T19:05:01.750731Z",
    "updated_at": "2025-08-19T19:05:01.750731Z"
  }
]
```

4. Update Device

PUT `/api/devices/id/`

5. Partial Update Device

PATCH `/api/devices/id/`

6. Delete Device

DELETE `/api/devices/id/`

7. Device Heartbeart
POST `/devices/id/heartbeat` → Update last_active_at.

Request:
```json
{
  "status": "active"
}

```

7. Filtering & Search

Supports query parameters:

?device_type=Light

?status=ON

?search=Bulb

8. Data & Analytics
Endpoints
`POST` `/devices/:id/logs` → Create log entry.
`GET` `/devices/:id/logs?limit=10` → Fetch last 10 logs.
`GET` `/devices/:id/usage?range=24h` → Aggregated usage.




## 📜 License

MIT License – free to use and modify.
