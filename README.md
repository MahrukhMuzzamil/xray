# X-ray Medical Image Search

A simple full-stack project for uploading, browsing, and filtering X-ray scans using Django and React.

---

## Requirements

* Python 3.8 or newer
* Node.js 14 or newer
* npm 6 or newer

---

## Backend Setup (Django)

1. Open a terminal and navigate to the backend folder:

   ```
   cd xray_project
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

4. Apply database migrations:

   ```
   python manage.py migrate
   ```

5. (Optional) Create a `media` folder inside `xray_project` and add a file named `sample.jpg`.

6. Seed the database with sample data:

   ```
   python manage.py shell -c "from scans.seed import run; run()"
   ```

7. Start the backend server:

   ```
   python manage.py runserver
   ```

   The backend will be running at:
   `http://127.0.0.1:8000`

---

## Frontend Setup (React)

1. Open a new terminal and navigate to the frontend folder:

   ```
   cd xray-frontend
   ```

2. Install the required Node packages:

   ```
   npm install
   ```

3. Start the frontend development server:

   ```
   npm start
   ```

   The frontend will be running at:
   `http://localhost:3000`


