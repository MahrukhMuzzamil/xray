import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Select from 'react-select';
import { Link } from 'react-router-dom';
import skeletonImage from './assets/skeleton.png'; // ✅ Make sure this is inside /src/assets

function ScanList() {
  const [scans, setScans] = useState([]);
  const [search, setSearch] = useState('');
  const [filters, setFilters] = useState({
    body_part: null,
    diagnosis: null,
    institution: null,
  });
  const [options, setOptions] = useState({
    body_parts: [],
    diagnoses: [],
    institutions: [],
  });

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}/scans/`)
.then((res) => {
      const data = Array.isArray(res.data) ? res.data : res.data.results || [];
      console.log('📊 Scans data received:', data);
      setScans(data);

      const bodyParts = [...new Set(data.map((s) => s.body_part))];
      const diagnoses = [...new Set(data.map((s) => s.diagnosis))];
      const institutions = [...new Set(data.map((s) => s.institution))];

      setOptions({
        body_parts: bodyParts.map((bp) => ({ value: bp, label: bp })),
        diagnoses: diagnoses.map((d) => ({ value: d, label: d })),
        institutions: institutions.map((i) => ({ value: i, label: i })),
      });
    });
  }, []);

  useEffect(() => {
   let url = `${process.env.REACT_APP_API_URL}/scans/`;

    const query = [];
    if (search) query.push(`search=${search}`);
    if (filters.body_part) query.push(`body_part=${filters.body_part.value}`);
    if (filters.diagnosis) query.push(`diagnosis=${filters.diagnosis.value}`);
    if (filters.institution) query.push(`institution=${filters.institution.value}`);
    if (query.length) url += '?' + query.join('&');

    axios.get(url).then((res) => {
      const data = Array.isArray(res.data) ? res.data : res.data.results || [];
      setScans(data);
    });
  }, [search, filters]);

  const SkeletonImage = () => (
    <div className="skeleton-right">
      <img src={skeletonImage} alt="skeleton" className="skeleton-figure" />
    </div>
  );

  const handleImageError = (e) => {
    console.error("❌ Failed to load image:", e.target.src);
    e.target.style.display = 'none';
    if (e.target.nextSibling) {
      e.target.nextSibling.style.display = 'block';
    }
  };

  const handleImageLoad = (e) => {
    console.log('✅ Image loaded successfully:', e.target.src);
  };

  return (
    <>
      <SkeletonImage />

      <div className="container">
        <h1 className="page-title">🦴 X-ray Scan Explorer</h1>

        <div className="filter-box">
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search description, diagnosis, tags..."
          />

          <Select
            className="neon-select"
            classNamePrefix="neon-select"
            options={options.body_parts}
            value={filters.body_part}
            onChange={(val) => setFilters((f) => ({ ...f, body_part: val }))}
            placeholder="Filter by Body Part"
            isClearable
            isSearchable
          />
          <Select
            className="neon-select"
            classNamePrefix="neon-select"
            options={options.diagnoses}
            value={filters.diagnosis}
            onChange={(val) => setFilters((f) => ({ ...f, diagnosis: val }))}
            placeholder="Filter by Diagnosis"
            isClearable
            isSearchable
          />
          <Select
            className="neon-select"
            classNamePrefix="neon-select"
            options={options.institutions}
            value={filters.institution}
            onChange={(val) => setFilters((f) => ({ ...f, institution: val }))}
            placeholder="Filter by Institution"
            isClearable
            isSearchable
          />

          <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
            <button
              onClick={() => {
                setSearch('');
                setFilters({ body_part: null, diagnosis: null, institution: null });
              }}
            >
              Clear Filters
            </button>

            <Link to="/upload">
              <button>Upload New Scan</button>
            </Link>
          </div>
        </div>

        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '15px' }}>
          {scans.map((scan) => (
            <Link
              key={scan.id}
              to={`/scan/${scan.id}`}
              className="card fade-up"
              style={{ width: '180px' }}
            >
              <div className="image-wrapper" style={{ position: 'relative' }}>
                {scan.image ? (
                  <>
                    <img
                      src={scan.image}
                      alt="X-ray"
                      className="scan-image"
                      onLoad={handleImageLoad}
                      onError={handleImageError}
                      style={{
                        width: '150px',
                        height: '150px',
                        objectFit: 'cover',
                        borderRadius: '6px',
                        boxShadow: '0 0 10px rgba(0, 188, 212, 0.4)'
                      }}
                    />
                    <div 
                      className="image-placeholder" 
                      style={{
                        display: 'none',
                        width: '150px',
                        height: '150px',
                        backgroundColor: '#f0f0f0',
                        borderRadius: '6px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: '#666',
                        fontSize: '12px',
                        textAlign: 'center'
                      }}
                    >
                      No Image
                    </div>
                  </>
                ) : (
                  <div 
                    className="image-placeholder" 
                    style={{
                      width: '150px',
                      height: '150px',
                      backgroundColor: '#f0f0f0',
                      borderRadius: '6px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: '#666',
                      fontSize: '12px',
                      textAlign: 'center'
                    }}
                  >
                    No Image
                  </div>
                )}
              </div>
              <div style={{ marginTop: '10px' }}>
                <strong>{scan.body_part}</strong>
                <p>{scan.diagnosis}</p>
                <p>{scan.scan_date}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </>
  );
}

export default ScanList;