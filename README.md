X-ray Medical Image Search
A simple full-stack project for uploading, browsing, and filtering X-ray scans.

Requirements
Python 3.8 or newer

Node.js 14+

npm 6+

Backend Setup (Django)
Open terminal and go into the backend folder:

bash
Copy
Edit
cd xray_project
Create and activate a virtual environment:

On Windows:

nginx
Copy
Edit
python -m venv venv
venv\Scripts\activate
On macOS/Linux:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
Install Python packages:

nginx
Copy
Edit
pip install -r requirements.txt
Run database migrations:

nginx
Copy
Edit
python manage.py migrate
(Optional) Add a sample.jpg inside a new media folder.

Seed the database:

scss
Copy
Edit
python manage.py shell -c "from scans.seed import run; run()"
Start the backend server:

nginx
Copy
Edit
python manage.py runserver
Visit the backend at:
http://127.0.0.1:8000

Frontend Setup (React)
Open a new terminal and go into the frontend folder:

bash
Copy
Edit
cd xray-frontend
Install dependencies:

nginx
Copy
Edit
npm install
Start the frontend server:

sql
Copy
Edit
npm start
Visit the frontend at:
http://localhost:3000