import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

function ScanDetail() {
  const { id } = useParams();
  const [scan, setScan] = useState(null);
  const [imageError, setImageError] = useState(false);
  const [imageLoading, setImageLoading] = useState(true);

  useEffect(() => {
    //axios.get(`https://xray-backend-391z.onrender.com/api/scans/${id}/`)
    const apiUrl = process.env.REACT_APP_API_URL || 'https://xray-backend-391z.onrender.com/api';
    axios.get(`${apiUrl}/scans/${id}/`)
      .then((res) => {
        console.log(' Scan data received:', res.data);
        setScan(res.data);
        setImageLoading(true);
        setImageError(false);
      })
      .catch((err) => {
        console.error("❌ Failed to fetch scan detail:", err);
      });
  }, [id]);

  const handleImageLoad = () => {
    console.log('✅ Image loaded successfully');
    setImageLoading(false);
    setImageError(false);
  };

  const handleImageError = (e) => {
    console.error("❌ Failed to load image:", e.target.src);
    setImageError(true);
    setImageLoading(false);
  };

  if (!scan) return <div className="container">Loading...</div>;

  return (
    <div className="container fade-up">
      <h1 className="page-title">Scan Detail</h1>
      
      {scan.image && !imageError && (
        <div className="image-container">
          {imageLoading && (
            <div style={{ 
              textAlign: 'center', 
              padding: '20px',
              color: '#666'
            }}>
              Loading image...
            </div>
          )}
          <img
            src={scan.image}
            alt="Full X-ray"
            className="detail-image"
            onLoad={handleImageLoad}
            onError={handleImageError}
            style={{
              maxWidth: '800px',
              height: 'auto',
              marginBottom: '20px',
              borderRadius: '8px',
              boxShadow: '0 0 15px rgba(0, 188, 212, 0.6)',
              display: imageLoading ? 'none' : 'block'
            }}
          />
        </div>
      )}

      {imageError && (
        <div className="image-error">
          <p>⚠️ Image could not be loaded</p>
          <p>Image URL: {scan.image}</p>
          <p>Please check if the URL is accessible in your browser.</p>
          <button 
            onClick={() => {
              setImageError(false);
              setImageLoading(true);
            }}
            style={{ marginTop: '10px' }}
          >
            Try Again
          </button>
        </div>
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