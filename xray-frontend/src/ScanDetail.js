import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

function ScanDetail() {
  const { id } = useParams();
  const [scan, setScan] = useState(null);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/scans/${id}/`).then((res) => {
      setScan(res.data);
    });
  }, [id]);

  if (!scan) return <div className="container">Loading...</div>;

  return (
    <div className="container fade-up">
     <h1 className="page-title">Scan Detail</h1> 
      <img
        src={scan.image.startsWith('http') ? scan.image : `http://localhost:8000${scan.image}`}
        alt="Full X-ray"
        style={{ maxWidth: '100%', height: 'auto', marginBottom: '20px' }}
      />
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
