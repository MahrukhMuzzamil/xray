# X-ray Medical Image Search Platform

A full-stack application for medical professionals to search and manage medical image datasets used in AI model development.

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm 6+

## Setup and Running Instructions

### Backend Setup (Django)

1. Navigate to the backend directory:
   ```
   cd xray_project
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install Python dependencies:
   ```
   pip install Django>=4.2 djangorestframework>=3.14 django-filter>=23.2 Pillow>=9.0 django-cors-headers>=4.0 faker>=18.0
   ```
   
   OR create a requirements.txt file with the following content and install with `pip install -r requirements.txt`:
   ```
   Django>=4.2
   djangorestframework>=3.14
   django-filter>=23.2
   Pillow>=9.0
   django-cors-headers>=4.0
   faker>=18.0
   ```

5. Run database migrations:
   ```
   python manage.py migrate
   ```

6. Create a sample image file for seeding (optional):
   - Create a directory named `media` in the `xray_project` folder
   - Add a sample JPG image named `sample.jpg` to the `media` directory
   - OR modify the seed.py script to not require an image file

7. Seed the database with sample data:
   ```
   python manage.py shell -c "from scans.seed import run; run()"
   ```
   
   Note: If you get an error about a missing sample.jpg file, you can either:
   - Create a sample.jpg file in the media directory
   - Or modify the seed.py script to create dummy data without images

8. Start the development server:
   ```
   python manage.py runserver
   ```
   
   The backend will be available at: http://127.0.0.1:8000

### Frontend Setup (React)

1. Open a new terminal and navigate to the frontend directory:
   ```
   cd xray-frontend
   ```

2. Install Node.js dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```
   
   The frontend will be available at: http://localhost:3000

## Elasticsearch Integration (Bonus Feature)

This application includes optional Elasticsearch integration for enhanced full-text search capabilities across fields like description, diagnosis, and tags.

### Setup Instructions

1. Download and install Elasticsearch from [https://www.elastic.co/downloads/elasticsearch](https://www.elastic.co/downloads/elasticsearch)
2. Start Elasticsearch service
3. Index existing data: `python manage.py index_scans`

With Elasticsearch enabled, the search functionality will provide:
- Better relevance scoring
- Fuzzy matching
- Multi-field search
- Improved performance for large datasets

## Usage

1. Make sure both backend and frontend servers are running
2. Open your browser and go to http://localhost:3000
3. You should see a list of X-ray scans that you can search and filter
4. Click on any scan to view its detailed information

## API Endpoints

- Main API: http://127.0.0.1:8000/api/
- Scans list: http://127.0.0.1:8000/api/scans/
- Scan detail: http://127.0.0.1:8000/api/scans/{id}/

## Project Structure

```
xray_project/
├── xray_project/        # Django project settings
├── scans/              # Main app with models, views, etc.
├── media/              # Uploaded images storage
└── db.sqlite3          # Database file

xray-frontend/
├── src/                # React source code
│   ├── App.js          # Main app component
│   ├── ScanList.js     # Scan listing component
│   └── ScanDetail.js  # Scan detail component
└── public/             # Static assets
```

## Troubleshooting

### Backend Issues

1. If you get "Module not found" errors:
   ```
   pip install django djangorestframework django-filter pillow django-cors-headers faker
   ```

2. If the database doesn't have data:
   ```
   python manage.py shell -c "from scans.seed import run; run()"
   ```

3. If you get an error about a missing sample.jpg file when seeding:
   - Create a `media` directory in the `xray_project` folder
   - Add a sample JPG image named `sample.jpg` to that directory
   - Or modify the `scans/seed.py` script to not require an image file

### Frontend Issues

1. If you get "Module not found" errors:
   ```
   npm install axios react-router-dom
   ```

2. If the frontend can't connect to backend:
   - Make sure the backend is running at http://127.0.0.1:8000
   - Check that CORS is enabled in Django settings

## Stopping the Application

1. To stop the backend server:
   - Press Ctrl+C in the terminal running Django

2. To stop the frontend server:
   - Press Ctrl+C in the terminal running React

3. To deactivate the Python virtual environment:
   ```
   deactivate