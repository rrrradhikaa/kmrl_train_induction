import React, { useState } from 'react';
import { useApi } from '../../hooks/useApi';

const UploadCSV = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [dataType, setDataType] = useState('trains');
  const [uploadStatus, setUploadStatus] = useState('');
  const [uploadResult, setUploadResult] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const { post, loading, error } = useApi();

  const dataTypeOptions = [
    { value: 'trains', label: 'Trains Data', description: 'Upload train information and status' },
    { value: 'fitness', label: 'Fitness Certificates', description: 'Upload fitness certificate data' },
    { value: 'job_cards', label: 'Job Cards', description: 'Upload maintenance job cards' },
    { value: 'branding', label: 'Branding Contracts', description: 'Upload advertising contracts' }
  ];

  const validateCSV = async (file) => {
    try {
      const text = await file.text();
      const lines = text.split('\n').filter(line => line.trim() !== '');
      
      if (lines.length < 2) {
        throw new Error('CSV file appears to be empty or has no data rows');
      }

      // Basic validation - check if we have headers and at least one data row
      const headers = lines[0].split(',').map(header => header.trim());
      if (headers.length === 0 || headers.every(header => header === '')) {
        throw new Error('CSV file missing headers');
      }

      // Check data rows for potential NaN issues
      if (lines.length > 1) {
        const firstDataRow = lines[1].split(',').map(val => val.trim());
        
        // Validate numeric fields (adjust this based on your expected data types)
        const numericValidation = firstDataRow.some((cell, index) => {
          // Skip empty cells and string fields (you might want to customize this)
          if (cell === '' || /[a-zA-Z]/.test(cell)) return false;
          
          const num = parseFloat(cell);
          return !isNaN(num) && isFinite(num);
        });

        if (!numericValidation && firstDataRow.some(cell => cell !== '')) {
          console.warn('CSV contains non-standard numeric values. Proceeding with upload...');
        }
      }

      return true;
    } catch (validationError) {
      throw new Error(`CSV validation failed: ${validationError.message}`);
    }
  };

  const handleFileSelect = async (file) => {
    if (!file) {
      setUploadStatus('error');
      setUploadResult({ error: 'No file selected' });
      return;
    }

    if (file.type !== 'text/csv' && !file.name.toLowerCase().endsWith('.csv')) {
      setUploadStatus('error');
      setUploadResult({ error: 'Please select a valid CSV file' });
      return;
    }

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      setUploadStatus('error');
      setUploadResult({ error: 'File size exceeds 10MB limit' });
      return;
    }

    try {
      // Pre-validate CSV before setting state
      await validateCSV(file);
      setSelectedFile(file);
      setUploadStatus('');
      setUploadResult(null);
    } catch (validationError) {
      setUploadStatus('error');
      setUploadResult({ error: validationError.message });
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    handleFileSelect(file);
  };

  const handleFileInput = (e) => {
    const file = e.target.files[0];
    handleFileSelect(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus('error');
      setUploadResult({ error: 'Please select a file first' });
      return;
    }

    setUploadStatus('uploading');
    setUploadResult(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('data_type', dataType);

      // Remove Content-Type header - let browser set it automatically for FormData
      const response = await post('/upload/csv', formData);

      if (response) {
        setUploadStatus('success');
        setUploadResult(response);
        setSelectedFile(null);
        
        // Safely reset file input
        const fileInput = document.getElementById('file-input');
        if (fileInput) {
          fileInput.value = '';
        }
      } else {
        setUploadStatus('error');
        setUploadResult({ error: error || 'Upload failed without specific error' });
      }
    } catch (uploadError) {
      setUploadStatus('error');
      setUploadResult({ 
        error: uploadError.message || 'Upload failed due to an unexpected error' 
      });
    }
  };

  const downloadTemplate = async (type) => {
    try {
      const response = await fetch(`http://localhost:8000/upload/templates/${type}`);
      
      if (!response.ok) {
        throw new Error(`Failed to download template: ${response.status}`);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${type}_template.csv`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('Error downloading template:', err);
      setUploadStatus('error');
      setUploadResult({ error: `Failed to download template: ${err.message}` });
    }
  };

  const getCurrentDataTypeLabel = () => {
    const option = dataTypeOptions.find(opt => opt.value === dataType);
    return option ? option.label : 'Template';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">CSV Data Upload</h2>

      {/* Data Type Selection */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select Data Type
        </label>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {dataTypeOptions.map((option) => (
            <div
              key={option.value}
              className={`border-2 rounded-lg p-4 cursor-pointer transition-all ${
                dataType === option.value
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => setDataType(option.value)}
            >
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-medium text-gray-900">{option.label}</h3>
                  <p className="text-sm text-gray-600 mt-1">{option.description}</p>
                </div>
                <div className={`w-4 h-4 rounded-full border-2 ${
                  dataType === option.value ? 'bg-blue-500 border-blue-500' : 'border-gray-300'
                }`}></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* File Upload Area */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Upload CSV File
        </label>
        
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-all ${
            isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
          } ${selectedFile ? 'border-green-500 bg-green-50' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          {selectedFile ? (
            <div className="text-green-600">
              <div className="text-4xl mb-2">✅</div>
              <p className="font-medium">{selectedFile.name}</p>
              <p className="text-sm text-green-700">
                {(selectedFile.size / 1024).toFixed(2)} KB
              </p>
              <button
                onClick={() => setSelectedFile(null)}
                className="text-red-600 text-sm mt-2 hover:text-red-800"
              >
                Remove File
              </button>
            </div>
          ) : (
            <>
              <div className="text-4xl mb-2">📁</div>
              <p className="text-gray-600 mb-2">
                Drag and drop your CSV file here, or click to browse
              </p>
              <input
                id="file-input"
                type="file"
                accept=".csv"
                onChange={handleFileInput}
                className="hidden"
              />
              <button
                onClick={() => document.getElementById('file-input')?.click()}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Browse Files
              </button>
              <p className="text-xs text-gray-500 mt-2">
                Only CSV files are supported. Max file size: 10MB
              </p>
            </>
          )}
        </div>
      </div>

      {/* Template Download */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-medium text-gray-900 mb-2">Need a template?</h3>
        <p className="text-sm text-gray-600 mb-3">
          Download a CSV template to ensure your file has the correct format.
        </p>
        <button
          onClick={() => downloadTemplate(dataType)}
          className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors text-sm"
        >
          Download {getCurrentDataTypeLabel()} Template
        </button>
      </div>

      {/* Upload Button and Status */}
      <div className="flex justify-between items-center">
        <div className="flex-1">
          {uploadStatus === 'success' && uploadResult && (
            <div className="text-green-600">
              <strong>Upload successful!</strong> {uploadResult.records_loaded || uploadResult.database_results?.total_records || 0} records processed.
            </div>
          )}
          {uploadStatus === 'error' && (
            <div className="text-red-600">
              <strong>Upload failed:</strong> {uploadResult?.error || error || 'Unknown error occurred'}
            </div>
          )}
          {uploadStatus === 'uploading' && (
            <div className="text-blue-600">
              <strong>Uploading...</strong> Please wait while we process your file.
            </div>
          )}
        </div>
        
        <button
          onClick={handleUpload}
          disabled={loading || !selectedFile || uploadStatus === 'uploading'}
          className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex-shrink-0"
        >
          {loading || uploadStatus === 'uploading' ? 'Uploading...' : 'Upload CSV'}
        </button>
      </div>

      {/* Upload Results */}
      {uploadResult && uploadResult.database_results && (
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h3 className="font-medium text-blue-900 mb-2">Upload Results</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="font-medium">Trains:</span> {uploadResult.database_results.trains_created || 0}
            </div>
            <div>
              <span className="font-medium">Fitness Certs:</span> {uploadResult.database_results.fitness_certs_created || 0}
            </div>
            <div>
              <span className="font-medium">Job Cards:</span> {uploadResult.database_results.job_cards_created || 0}
            </div>
            <div>
              <span className="font-medium">Branding Contracts:</span> {uploadResult.database_results.branding_contracts_created || 0}
            </div>
          </div>
          {uploadResult.database_results.errors && uploadResult.database_results.errors.length > 0 && (
            <div className="mt-3">
              <span className="font-medium text-red-700">Errors:</span>
              <ul className="text-sm text-red-600 mt-1">
                {uploadResult.database_results.errors.map((err, index) => (
                  <li key={index}>• {err}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default UploadCSV;