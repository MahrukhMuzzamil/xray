import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ScanList from './ScanList';
import ScanDetail from './ScanDetail';
import UploadScan from './UploadScan';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ScanList />} />
        <Route path="/scan/:id" element={<ScanDetail />} />
        <Route path="/upload" element={<UploadScan />} />
      </Routes>
    </Router>
  );
}

export default App;
