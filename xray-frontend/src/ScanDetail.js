import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { config } from './config';

function ScanDetail() {
  const { id } = useParams();
  const [scan, setScan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    
    axios.get(`${config.API_URL}/scans/${id}/`)
      .then((res) => {
        setScan(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("❌ Failed to fetch scan detail:", err);
        setError(err.message);
        setLoading(false);
      });
  }, [id]);

  const handleImageError = (e) => {
    console.error(`Failed to load image: ${scan.image}`);
    e.target.style.display = 'none';
    // Add a placeholder or fallback image
    const fallbackDiv = document.createElement('div');
    fallbackDiv.className = 'detail-image-fallback';
    fallbackDiv.innerHTML = '🦴';
    fallbackDiv.style.cssText = `
      width: 100%;
      height: 300px;
      background: #f0f0f0;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 5rem;
      border-radius: 8px;
      margin-bottom: 20px;
    `;
    e.target.parentNode.insertBefore(fallbackDiv, e.target);
  };

  if (loading) return <div className="container">Loading...</div>;
  if (error) return <div className="container">Error: {error}</div>;
  if (!scan) return <div className="container">Scan not found</div>;

  return (
    <div className="container fade-up">
      <h1 className="page-title">Scan Detail</h1>
      
      {scan.image && (
        <img
          src={scan.image}
          alt="Full X-ray"
          className="detail-image"
          onError={handleImageError}
        />
      )}

      <div className="card">
        <p><strong>Patient ID:</strong> {scan.patient_id}</p>
        <p><strong>Body Part:</strong> {scan.body_part}</p>
        <p><strong>Scan Date:</strong> {scan.scan_date}</p>
        <p><strong>Institution:</strong> {scan.institution}</p>
        <p><strong>Diagnosis:</strong> {scan.diagnosis}</p>
        <p><strong>Description:</strong> {scan.description}</p>
        <p><strong>Tags:</strong> {scan.tags.map((tag, index) => (
          <span key={index} className="tag">{tag}</span>
        ))}</p>
      </div>
    </div>
  );
}

export default ScanDetail;