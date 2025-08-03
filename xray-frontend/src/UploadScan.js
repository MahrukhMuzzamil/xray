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
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, files } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'file' ? files[0] : value,
    }));
    setError(''); // Clear error when user makes changes
  };

  const validateForm = () => {
    if (!formData.patient_id.trim()) {
      setError('Patient ID is required');
      return false;
    }
    if (!formData.body_part.trim()) {
      setError('Body part is required');
      return false;
    }
    if (!formData.scan_date) {
      setError('Scan date is required');
      return false;
    }
    if (!formData.institution.trim()) {
      setError('Institution is required');
      return false;
    }
    if (!formData.description.trim()) {
      setError('Description is required');
      return false;
    }
    if (!formData.diagnosis.trim()) {
      setError('Diagnosis is required');
      return false;
    }
    if (!formData.image) {
      setError('Image file is required');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setError('');

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
      console.log('🚀 Uploading to:', `${process.env.REACT_APP_API_URL}/scans/`);
      console.log('📁 Form data keys:', Array.from(data.keys()));
      console.log('📁 Image file:', formData.image);
      
      const response = await axios.post(`${process.env.REACT_APP_API_URL}/scans/`, data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000, // 30 second timeout
      });

      console.log('✅ Upload successful:', response.data);
      alert('Upload successful!');
      navigate('/');
    } catch (error) {
      console.error('❌ Upload failed:', error);
      console.error('❌ Response data:', error.response?.data);
      console.error('❌ Response status:', error.response?.status);
      console.error('❌ Response headers:', error.response?.headers);
      
      let errorMessage = 'Upload failed. Please check the fields and try again.';
      
      if (error.response?.data) {
        if (typeof error.response.data === 'object') {
          const errors = Object.entries(error.response.data)
            .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
            .join('\n');
          errorMessage = `Upload failed:\n${errors}`;
        } else {
          errorMessage = error.response.data;
        }
      } else if (error.message) {
        errorMessage = `Upload failed: ${error.message}`;
      }
      
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container fade-up" style={{ maxWidth: '600px', margin: '0 auto' }}>
    <h1 className="page-title">Upload New Scan</h1> 
      <form onSubmit={handleSubmit} className="card" style={{ padding: '20px' }}>
        {error && (
          <div style={{ 
            backgroundColor: '#ffebee', 
            color: '#c62828', 
            padding: '10px', 
            borderRadius: '4px', 
            marginBottom: '15px',
            border: '1px solid #ef5350',
            whiteSpace: 'pre-line'
          }}>
            {error}
          </div>
        )}

        <div style={{ marginBottom: '12px' }}>
          <label>PATIENT ID:</label>
          <input
            type="text"
            name="patient_id"
            value={formData.patient_id}
            onChange={handleChange}
            placeholder="e.g. 21L6084"
            required
            disabled={isLoading}
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
            disabled={isLoading}
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
            disabled={isLoading}
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
            disabled={isLoading}
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
            disabled={isLoading}
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
            disabled={isLoading}
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
            disabled={isLoading}
          />
        </div>

        <div style={{ marginBottom: '12px' }}>
          <label>Image File:</label>
          <input 
            type="file" 
            name="image" 
            onChange={handleChange} 
            required 
            disabled={isLoading}
            accept="image/*"
          />
          {formData.image && (
            <p style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>
              Selected: {formData.image.name} ({(formData.image.size / 1024 / 1024).toFixed(2)} MB)
            </p>
          )}
        </div>

        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
    </div>
  );
}

export default UploadScan;