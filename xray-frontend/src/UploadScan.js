import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function UploadScan() {
  const [formData, setFormData] = useState({
    patient_id: '',
    body_part: '',
    scan_date: '',
    institution: '',
    description: '',
    diagnosis: '',
    tags: '',
    image: null,
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, files } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'file' ? files[0] : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData();

    for (let key in formData) {
      if (key === 'tags') {
        const tagList = formData.tags
          .split(',')
          .map((tag) => tag.trim())
          .filter((tag) => tag);
        data.append('tags', JSON.stringify(tagList)); // ✅ send as valid JSON array
      } else {
        data.append(key, formData[key]);
      }
    }

    try {
      await axios.post('http://localhost:8000/api/scans/', data);
      alert('Upload successful!');
      navigate('/');
    } catch (error) {
      console.error('❌ Upload failed with errors:', error.response?.data || error.message);
      alert('Upload failed. Please check the fields and try again.');
    }
  };

  return (
    <div className="container fade-up" style={{ maxWidth: '600px', margin: '0 auto' }}>
    <h1 className="page-title">Upload New Scan</h1> 
      <form onSubmit={handleSubmit} className="card" style={{ padding: '20px' }}>
        <div style={{ marginBottom: '12px' }}>
          <label>PATIENT ID:</label>
          <input
            type="text"
            name="patient_id"
            value={formData.patient_id}
            onChange={handleChange}
            placeholder="e.g. 21L6084"
            required
          />
        </div>

        <div style={{ marginBottom: '12px' }}>
          <label>BODY PART:</label>
          <input
            type="text"
            name="body_part"
            value={formData.body_part}
            onChange={handleChange}
            placeholder="e.g. Chest"
            required
          />
        </div>

        <div style={{ marginBottom: '12px' }}>
          <label>SCAN DATE:</label>
          <input
            type="date"
            name="scan_date"
            value={formData.scan_date}
            onChange={handleChange}
            required
          />
        </div>

        <div style={{ marginBottom: '12px' }}>
          <label>INSTITUTION:</label>
          <input
            type="text"
            name="institution"
            value={formData.institution}
            onChange={handleChange}
            placeholder="e.g. Mayo Clinic"
            required
          />
        </div>

        <div style={{ marginBottom: '12px' }}>
          <label>DESCRIPTION:</label>
          <input
            type="text"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="e.g. Lower lobe opacity"
            required
          />
        </div>

        <div style={{ marginBottom: '12px' }}>
          <label>DIAGNOSIS:</label>
          <input
            type="text"
            name="diagnosis"
            value={formData.diagnosis}
            onChange={handleChange}
            placeholder="e.g. Pneumonia"
            required
          />
        </div>

        <div style={{ marginBottom: '12px' }}>
          <label>TAGS:</label>
          <input
            type="text"
            name="tags"
            value={formData.tags}
            onChange={handleChange}
            placeholder="e.g. lung, infection, opacity"
          />
        </div>

        <div style={{ marginBottom: '12px' }}>
          <label>Image File:</label>
          <input type="file" name="image" onChange={handleChange} required />
        </div>

        <button type="submit">Upload</button>
      </form>
    </div>
  );
}

export default UploadScan;
