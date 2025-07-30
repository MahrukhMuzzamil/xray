# X-ray Project Implementation Plan

This document outlines all the changes needed to fulfill the missing requirements for the X-ray project.

## Backend Enhancements

### 1. Requirements.txt Update

File: `xray_project/requirements.txt`

Current state: Empty file

Required content:
```
Django>=4.2
djangorestframework>=3.14
django-filter>=23.2
Pillow>=9.0
django-cors-headers>=4.0
```

### 2. Admin Panel Integration

File: `xray_project/scans/admin.py`

Current state:
```python
from django.contrib import admin

# Register your models here.
```

Required content:
```python
from django.contrib import admin
from .models import XRayScan

@admin.register(XRayScan)
class XRayScanAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'body_part', 'diagnosis', 'scan_date', 'institution')
    list_filter = ('body_part', 'diagnosis', 'institution', 'scan_date')
    search_fields = ('patient_id', 'description', 'diagnosis')
    date_hierarchy = 'scan_date'
```

### 3. Enhanced Views

File: `xray_project/scans/views.py`

Current state:
```python
from rest_framework import viewsets, filters
from .models import XRayScan
from .serializers import XRayScanSerializer
from django_filters.rest_framework import DjangoFilterBackend

class XRayScanViewSet(viewsets.ModelViewSet):
    queryset = XRayScan.objects.all().order_by('-scan_date')
    serializer_class = XRayScanSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['body_part', 'institution', 'diagnosis']
    search_fields = ['description', 'diagnosis', 'tags']
```

Required enhancements:
```python
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import XRayScan
from .serializers import XRayScanSerializer
from django_filters.rest_framework import DjangoFilterBackend

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100

class XRayScanViewSet(viewsets.ModelViewSet):
    queryset = XRayScan.objects.all().order_by('-scan_date')
    serializer_class = XRayScanSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['body_part', 'institution', 'diagnosis']
    search_fields = ['description', 'diagnosis', 'tags']
    ordering_fields = ['scan_date', 'body_part', 'institution']
    ordering = ['-scan_date']
    pagination_class = StandardResultsSetPagination
```

## Frontend Enhancements

### 1. Enhanced ScanList Component

File: `xray-frontend/src/ScanList.js`

Current state:
```javascript
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function ScanList() {
  const [scans, setScans] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
        axios.get(`http://127.0.0.1:8000/api/scans/?search=${search}`)
      .then(res => setScans(res.data));
  }, [search]);

  return (
    <div>
      <h1>X-ray Scans</h1>
      <input
        type="text"
        placeholder="Search description/tags/diagnosis"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        {scans.map(scan => (
          <Link key={scan.id} to={`/scan/${scan.id}`} style={{ margin: 10 }}>
            <img src={`http://localhost:8000${scan.image}`} alt="X-ray" width="150" />
            <p>{scan.body_part} - {scan.diagnosis}</p>
            <p>{scan.scan_date}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default ScanList;
```

Required enhancements:
```javascript
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function ScanList() {
  const [scans, setScans] = useState([]);
  const [search, setSearch] = useState("");
  const [filters, setFilters] = useState({
    institution: "",
    bodyPart: "",
    diagnosis: ""
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchScans = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const params = new URLSearchParams();
        if (search) params.append('search', search);
        if (filters.institution) params.append('institution', filters.institution);
        if (filters.bodyPart) params.append('body_part', filters.bodyPart);
        if (filters.diagnosis) params.append('diagnosis', filters.diagnosis);
        
        const response = await axios.get(`http://127.0.0.1:8000/api/scans/?${params.toString()}`);
        setScans(response.data);
      } catch (err) {
        setError('Failed to fetch scans. Please try again later.');
        console.error('Error fetching scans:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchScans();
  }, [search, filters]);

  const handleFilterChange = (filterName, value) => {
    setFilters(prev => ({
      ...prev,
      [filterName]: value
    }));
  };

  const resetFilters = () => {
    setSearch("");
    setFilters({
      institution: "",
      bodyPart: "",
      diagnosis: ""
    });
  };

  return (
    <div className="scan-list-container">
      <h1>X-ray Scans</h1>
      
      {/* Search and Filters */}
      <div className="search-filters">
        <input
          type="text"
          placeholder="Search description/tags/diagnosis"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="search-input"
        />
        
        <div className="filters">
          <select 
            value={filters.institution} 
            onChange={(e) => handleFilterChange('institution', e.target.value)}
            className="filter-select"
          >
            <option value="">All Institutions</option>
            <option value="Mayo Clinic">Mayo Clinic</option>
            <option value="Johns Hopkins">Johns Hopkins</option>
            <option value="Stanford">Stanford</option>
          </select>
          
          <select 
            value={filters.bodyPart} 
            onChange={(e) => handleFilterChange('bodyPart', e.target.value)}
            className="filter-select"
          >
            <option value="">All Body Parts</option>
            <option value="Chest">Chest</option>
            <option value="Knee">Knee</option>
            <option value="Arm">Arm</option>
          </select>
          
          <select 
            value={filters.diagnosis} 
            onChange={(e) => handleFilterChange('diagnosis', e.target.value)}
            className="filter-select"
          >
            <option value="">All Diagnoses</option>
            <option value="Pneumonia">Pneumonia</option>
            <option value="Fracture">Fracture</option>
            <option value="Normal">Normal</option>
          </select>
          
          <button onClick={resetFilters} className="reset-button">
            Reset Filters
          </button>
        </div>
      </div>

      {/* Loading and Error States */}
      {loading && <div className="loading">Loading scans...</div>}
      {error && <div className="error">{error}</div>}

      {/* Scans Grid */}
      {!loading && !error && (
        <div className="scans-grid">
          {scans.map(scan => (
            <div key={scan.id} className="scan-card">
              <Link to={`/scan/${scan.id}`} className="scan-link">
                <img 
                  src={`http://localhost:8000${scan.image}`} 
                  alt={`${scan.body_part} scan`} 
                  className="scan-thumbnail"
                />
                <div className="scan-info">
                  <h3>{scan.patient_id}</h3>
                  <p><strong>Body Part:</strong> {scan.body_part}</p>
                  <p><strong>Diagnosis:</strong> {scan.diagnosis}</p>
                  <p><strong>Date:</strong> {scan.scan_date}</p>
                  <p><strong>Institution:</strong> {scan.institution}</p>
                </div>
              </Link>
            </div>
          ))}
        </div>
      )}

      {/* Empty State */}
      {!loading && !error && scans.length === 0 && (
        <div className="empty-state">
          <p>No scans found matching your criteria.</p>
        </div>
      )}
    </div>
  );
}

export default ScanList;
```

### 2. Enhanced ScanDetail Component

File: `xray-frontend/src/ScanDetail.js`

Current state:
```javascript
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

function ScanDetail() {
  const { id } = useParams();
  const [scan, setScan] = useState(null);

  useEffect(() => {

axios.get(`http://127.0.0.1:8000/api/scans/${id}/`)
    
      .then(res => setScan(res.data));
  }, [id]);

  if (!scan) return <div>Loading...</div>;

  return (
    <div>
      <h2>Scan Detail: {scan.patient_id}</h2>
      <img src={`http://localhost:8000${scan.image}`} alt="Full X-ray" width="400" />
      <ul>
        <li><strong>Body Part:</strong> {scan.body_part}</li>
        <li><strong>Diagnosis:</strong> {scan.diagnosis}</li>
        <li><strong>Institution:</strong> {scan.institution}</li>
        <li><strong>Scan Date:</strong> {scan.scan_date}</li>
        <li><strong>Description:</strong> {scan.description}</li>
        <li><strong>Tags:</strong> {scan.tags.join(', ')}</li>
      </ul>
    </div>
  );
}

export default ScanDetail;
```

Required enhancements:
```javascript
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

function ScanDetail() {
  const { id } = useParams();
  const [scan, setScan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchScan = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/scans/${id}/`);
        setScan(response.data);
      } catch (err) {
        setError('Failed to fetch scan details. Please try again later.');
        console.error('Error fetching scan:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchScan();
  }, [id]);

  if (loading) return <div className="loading">Loading scan details...</div>;
  
  if (error) return <div className="error">{error}</div>;
  
  if (!scan) return <div className="error">Scan not found.</div>;

  return (
    <div className="scan-detail-container">
      <Link to="/" className="back-link">&larr; Back to Scans</Link>
      
      <div className="scan-detail-content">
        <div className="scan-image-container">
          <img 
            src={`http://localhost:8000${scan.image}`} 
            alt={`X-ray for patient ${scan.patient_id}`}
            className="scan-full-image"
          />
        </div>
        
        <div className="scan-details">
          <h2>Scan Details - {scan.patient_id}</h2>
          
          <div className="detail-grid">
            <div className="detail-item">
              <strong>Body Part:</strong>
              <span>{scan.body_part}</span>
            </div>
            
            <div className="detail-item">
              <strong>Diagnosis:</strong>
              <span>{scan.diagnosis}</span>
            </div>
            
            <div className="detail-item">
              <strong>Institution:</strong>
              <span>{scan.institution}</span>
            </div>
            
            <div className="detail-item">
              <strong>Scan Date:</strong>
              <span>{scan.scan_date}</span>
            </div>
            
            <div className="detail-item full-width">
              <strong>Description:</strong>
              <span>{scan.description}</span>
            </div>
            
            <div className="detail-item full-width">
              <strong>Tags:</strong>
              <div className="tags-container">
                {scan.tags.map((tag, index) => (
                  <span key={index} className="tag">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ScanDetail;
```

### 3. New CSS File for Styling

File: `xray-frontend/src/App.css`

Add comprehensive styling:
```css
/* App.css */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f7fa;
  color: #333;
  line-height: 1.6;
}

/* Header/Navigation */
header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

/* Search and Filters */
.search-filters {
  background: white;
  padding: 1.5rem;
  margin: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.search-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.filters {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
}

.reset-button {
  padding: 0.5rem 1rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.reset-button:hover {
  background-color: #2980b9;
}

/* Scans Grid */
.scans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  padding: 1rem;
}

.scan-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.scan-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.scan-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.scan-thumbnail {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.scan-info {
  padding: 1rem;
}

.scan-info h3 {
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.scan-info p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
}

/* Scan Detail */
.scan-detail-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.back-link {
  display: inline-block;
  margin-bottom: 1rem;
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

.back-link:hover {
  text-decoration: underline;
}

.scan-detail-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.scan-full-image {
  width: 100%;
  height: auto;
  border-radius: 4px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item.full-width {
  grid-column: span 2;
}

.detail-item strong {
  margin-bottom: 0.25rem;
  color: #2c3e50;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.tag {
  background-color: #3498db;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

/* Loading and Error States */
.loading, .error, .empty-state {
  text-align: center;
  padding: 2rem;
  margin: 1rem;
  border-radius: 4px;
}

.loading {
  background-color: #f8f9fa;
  color: #6c757d;
}

.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.empty-state {
  background-color: #e9ecef;
  color: #495057;
}

/* Responsive Design */
@media (max-width: 768px) {
  .scans-grid {
    grid-template-columns: 1fr;
  }
  
  .filters {
    flex-direction: column;
  }
  
  .scan-detail-content {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
  
  .detail-item.full-width {
    grid-column: span 1;
  }
}
```

## Documentation and Testing

### 1. README.md Update

File: `README.md`

Create comprehensive documentation:
```markdown
# X-ray Medical Image Search Platform

A full-stack application for medical professionals to search and manage medical image datasets used in AI model development.

## Features

- Upload and store X-ray scan metadata
- Search and filter X-ray records by metadata
- View a list of X-ray images with relevant metadata
- Detailed view of selected scans

## Tech Stack

### Backend
- Django 4.2+
- Django REST Framework
- SQLite database
- Django Filter for search functionality

### Frontend
- React 18+
- React Router for navigation
- Axios for API requests

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd xray_project
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Seed the database with sample data:
   ```
   python manage.py shell -c "from scans.seed import run; run()"
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd xray-frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

## API Endpoints

- `GET /api/scans/` - List all scans with filtering
- `GET /api/scans/{id}/` - Get details for a specific scan
- `POST /api/scans/` - Create a new scan record

### Query Parameters

- `search` - Search across description, diagnosis, and tags
- `institution` - Filter by institution
- `body_part` - Filter by body part
- `diagnosis` - Filter by diagnosis
- `ordering` - Order results (e.g., `scan_date`, `-scan_date`)

## Project Structure

### Backend
```
xray_project/
├── scans/              # Main app
│   ├── models.py       # XRayScan model
│   ├── views.py        # API views
│   ├── serializers.py  # DRF serializers
│   ├── urls.py         # App URLs
│   └── seed.py         # Sample data generator
├── xray_project/       # Project settings
│   ├── settings.py     # Django settings
│   └── urls.py         # Main URLs
└── manage.py          # Django CLI tool
```

### Frontend
```
xray-frontend/
├── src/
│   ├── components/     # Reusable components
│   ├── pages/          # Page components
│   ├── services/       # API service functions
│   ├── App.js          # Main app component
│   └── index.js        # Entry point
└── public/             # Static assets
```

## Development

### Running Tests

Backend tests:
```
python manage.py test
```

Frontend tests:
```
npm test
```

### Deployment

1. Build the frontend:
   ```
   npm run build
   ```

2. Configure Django for production:
   - Set `DEBUG = False`
   - Update `ALLOWED_HOSTS`
   - Configure a production database
   - Set up a web server (Nginx/Apache)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License.
```

### 2. Testing Plan

Create test files for both backend and frontend:

Backend test file: `xray_project/scans/tests.py`
```python
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import XRayScan

class XRayScanModelTest(TestCase):
    def setUp(self):
        self.scan = XRayScan.objects.create(
            patient_id="P00128",
            body_part="Chest",
            scan_date="2024-09-21",
            institution="Mayo Clinic",
            description="Patient shows signs of pneumonia in the lower left lobe.",
            diagnosis="Pneumonia",
            tags=["lung", "infection", "opacity"]
        )

    def test_scan_str_representation(self):
        self.assertEqual(str(self.scan), "P00128 - Chest")

class XRayScanAPITest(APITestCase):
    def setUp(self):
        self.scan = XRayScan.objects.create(
            patient_id="P00128",
            body_part="Chest",
            scan_date="2024-09-21",
            institution="Mayo Clinic",
            description="Patient shows signs of pneumonia in the lower left lobe.",
            diagnosis="Pneumonia",
            tags=["lung", "infection", "opacity"]
        )

    def test_get_scans_list(self):
        url = reverse('xrayscan-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_scan_detail(self):
        url = reverse('xrayscan-detail', kwargs={'pk': self.scan.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['patient_id'], "P00128")

    def test_search_scans(self):
        url = reverse('xrayscan-list')
        response = self.client.get(url, {'search': 'pneumonia'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

Frontend test files would be created in `xray-frontend/src/__tests__/` directory.

## Deployment Configuration

### Docker Configuration

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./xray_project
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
    volumes:
      - ./xray_project/media:/app/media
    depends_on:
      - db

  frontend:
    build: ./xray-frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000/api

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=xray_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

This implementation plan addresses all missing requirements and provides a complete solution for the X-ray medical image search platform.