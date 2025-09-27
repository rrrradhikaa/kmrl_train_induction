import React, { useState } from 'react';
import { useApi } from '../../hooks/useApi';

const ManualInput = () => {
  const [activeTab, setActiveTab] = useState('train');
  const [formData, setFormData] = useState({});
  const [submissionStatus, setSubmissionStatus] = useState('');
  const [submissionResult, setSubmissionResult] = useState(null);
  const { post, loading } = useApi();

  const tabs = [
    { id: 'train', label: 'Train', icon: '🚆' },
    { id: 'fitness', label: 'Fitness Certificate', icon: '📋' },
    { id: 'job_card', label: 'Job Card', icon: '🔧' },
    { id: 'branding', label: 'Branding Contract', icon: '📢' },
    { id: 'cleaning', label: 'Cleaning Slot', icon: '🧹' },
    { id: 'stabling', label: 'Stabling Geometry', icon: '🅿️' }
  ];

  const trainFormFields = [
    { name: 'train_number', label: 'Train Number', type: 'text', required: true, pattern: '^[A-Z]{2,4}-\\d{3}$', placeholder: 'KMRL-001' },
    { name: 'current_mileage', label: 'Current Mileage (km)', type: 'number', required: true, min: 0 },
    { name: 'last_maintenance_date', label: 'Last Maintenance Date', type: 'date' },
    { name: 'status', label: 'Status', type: 'select', options: ['active', 'under_maintenance', 'retired'], required: true }
  ];

  const fitnessFormFields = [
    { name: 'train_id', label: 'Train ID', type: 'number', required: true, min: 1 },
    { name: 'department', label: 'Department', type: 'select', options: ['Rolling-Stock', 'Signalling', 'Telecom'], required: true },
    { name: 'valid_from', label: 'Valid From', type: 'date', required: true },
    { name: 'valid_until', label: 'Valid Until', type: 'date', required: true },
    { name: 'is_valid', label: 'Is Valid', type: 'checkbox', default: true }
  ];

  const jobCardFormFields = [
    { name: 'train_id', label: 'Train ID', type: 'number', required: true, min: 1 },
    { name: 'work_order_id', label: 'Work Order ID', type: 'text', required: true, placeholder: 'WO-123ABC' },
    { name: 'status', label: 'Status', type: 'select', options: ['open', 'closed'], required: true },
    { name: 'description', label: 'Description', type: 'textarea', placeholder: 'Describe the maintenance work...' }
  ];

  const brandingFormFields = [
    { name: 'train_id', label: 'Train ID', type: 'number', required: true, min: 1 },
    { name: 'advertiser_name', label: 'Advertiser Name', type: 'text', required: true },
    { name: 'exposure_hours_required', label: 'Exposure Hours Required', type: 'number', required: true, min: 1 },
    { name: 'exposure_hours_fulfilled', label: 'Exposure Hours Fulfilled', type: 'number', min: 0, default: 0 },
    { name: 'start_date', label: 'Start Date', type: 'date', required: true },
    { name: 'end_date', label: 'End Date', type: 'date', required: true }
  ];

  const cleaningFormFields = [
    { name: 'train_id', label: 'Train ID', type: 'number', required: true, min: 1 },
    { name: 'slot_time', label: 'Slot Time', type: 'datetime-local', required: true },
    { name: 'bay_number', label: 'Bay Number', type: 'number', required: true, min: 1 },
    { name: 'manpower_required', label: 'Manpower Required', type: 'number', required: true, min: 1 },
    { name: 'status', label: 'Status', type: 'select', options: ['scheduled', 'completed', 'cancelled'], required: true }
  ];

  const stablingFormFields = [
    { name: 'train_id', label: 'Train ID', type: 'number', required: true, min: 1 },
    { name: 'bay_position', label: 'Bay Position', type: 'text', required: true, placeholder: 'A-01' },
    { name: 'stabled_at', label: 'Stabled At', type: 'datetime-local', required: true },
    { name: 'shunting_required', label: 'Shunting Required', type: 'checkbox', default: false }
  ];

  const getFormFields = () => {
    switch (activeTab) {
      case 'train': return trainFormFields;
      case 'fitness': return fitnessFormFields;
      case 'job_card': return jobCardFormFields;
      case 'branding': return brandingFormFields;
      case 'cleaning': return cleaningFormFields;
      case 'stabling': return stablingFormFields;
      default: return [];
    }
  };

  const getEndpoint = () => {
    switch (activeTab) {
      case 'train': return '/trains/';
      case 'fitness': return '/fitness/';
      case 'job_card': return '/job-cards/';
      case 'branding': return '/branding/';
      case 'cleaning': return '/cleaning/';
      case 'stabling': return '/stabling/';
      default: return '';
    }
  };

  const handleInputChange = (fieldName, value) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmissionStatus('submitting');

    const endpoint = getEndpoint();
    const response = await post(endpoint, formData);

    if (response) {
      setSubmissionStatus('success');
      setSubmissionResult(response);
      // Reset form
      setFormData({});
      // Reset form fields to defaults
      getFormFields().forEach(field => {
        if (field.default !== undefined) {
          setFormData(prev => ({ ...prev, [field.name]: field.default }));
        }
      });
    } else {
      setSubmissionStatus('error');
    }
  };

  const renderField = (field) => {
    const value = formData[field.name] ?? field.default ?? '';

    switch (field.type) {
      case 'select':
        return (
          <select
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            required={field.required}
          >
            <option value="">Select {field.label}</option>
            {field.options.map(option => (
              <option key={option} value={option}>
                {option.charAt(0).toUpperCase() + option.slice(1)}
              </option>
            ))}
          </select>
        );

      case 'textarea':
        return (
          <textarea
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            placeholder={field.placeholder}
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        );

      case 'checkbox':
        return (
          <input
            type="checkbox"
            checked={value}
            onChange={(e) => handleInputChange(field.name, e.target.checked)}
            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
        );

      case 'datetime-local':
        return (
          <input
            type="datetime-local"
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            required={field.required}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        );

      default:
        return (
          <input
            type={field.type}
            value={value}
            onChange={(e) => handleInputChange(field.name, e.target.value)}
            placeholder={field.placeholder}
            pattern={field.pattern}
            min={field.min}
            required={field.required}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        );
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Manual Data Input</h2>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {getFormFields().map((field) => (
            <div key={field.name} className={field.type === 'textarea' ? 'md:col-span-2' : ''}>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {field.label}
                {field.required && <span className="text-red-500 ml-1">*</span>}
              </label>
              {renderField(field)}
              {field.pattern && (
                <p className="text-xs text-gray-500 mt-1">Format: {field.pattern.replace('\\', '')}</p>
              )}
            </div>
          ))}
        </div>

        {/* Submission Status */}
        {submissionStatus === 'success' && submissionResult && (
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center">
              <div className="text-green-600 text-lg mr-2">✅</div>
              <div>
                <strong className="text-green-800">Success!</strong>
                <p className="text-green-700 text-sm">
                  {activeTab === 'train' && `Train ${submissionResult.train_number} created successfully.`}
                  {activeTab === 'fitness' && 'Fitness certificate added successfully.'}
                  {activeTab === 'job_card' && 'Job card created successfully.'}
                  {activeTab === 'branding' && 'Branding contract added successfully.'}
                  {activeTab === 'cleaning' && 'Cleaning slot scheduled successfully.'}
                  {activeTab === 'stabling' && 'Stabling geometry recorded successfully.'}
                </p>
              </div>
            </div>
          </div>
        )}

        {submissionStatus === 'error' && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center">
              <div className="text-red-600 text-lg mr-2">❌</div>
              <div>
                <strong className="text-red-800">Error!</strong>
                <p className="text-red-700 text-sm">Failed to submit data. Please check your inputs.</p>
              </div>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Submitting...' : `Add ${tabs.find(t => t.id === activeTab)?.label}`}
          </button>
        </div>
      </form>

      {/* Quick Help */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-medium text-gray-900 mb-2">Quick Tips</h3>
        <ul className="text-sm text-gray-600 space-y-1">
          <li>• Ensure Train ID exists before adding related records</li>
          <li>• Use consistent formatting for Train Numbers (e.g., KMRL-001)</li>
          <li>• Work Order IDs should start with "WO-" prefix</li>
          <li>• Date fields should be in YYYY-MM-DD format</li>
          <li>• DateTime fields should be in YYYY-MM-DDTHH:MM format</li>
          <li>• Bay positions typically follow patterns like "A-01", "B-12"</li>
        </ul>
      </div>
    </div>
  );
};

export default ManualInput;