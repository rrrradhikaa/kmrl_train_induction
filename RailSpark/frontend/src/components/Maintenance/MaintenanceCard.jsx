import React, { useState, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';

const Maintenance = () => {
  const [jobCards, setJobCards] = useState([]);
  const [filter, setFilter] = useState('all');
  const [showNewJobModal, setShowNewJobModal] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);
  const [newJobData, setNewJobData] = useState({
    work_order_id: '',
    description: '',
    train_id: ''
  });
  const [trains, setTrains] = useState([]);
  const { get, post, put, patch, del, loading, error } = useApi();

  // Fetch job cards from backend
  const fetchJobCards = async () => {
    const response = await get('/job-cards/');
    if (response) {
      setJobCards(response);
    }
  };

  // Fetch open job cards only
  const fetchOpenJobCards = async () => {
    const response = await get('/job-cards/open');
    if (response) {
      setJobCards(response);
    }
  };

  // Fetch trains for assignment
  const fetchTrains = async () => {
    const response = await get('/trains');
    if (response) {
      setTrains(response);
    }
  };

  // Create new job card
  const createJobCard = async () => {
    const response = await post('/job-cards/', newJobData);
    if (response) {
      setShowNewJobModal(false);
      setNewJobData({
        work_order_id: '',
        description: '',
        train_id: ''
      });
      fetchJobCards(); // Refresh the list
    }
  };

  // Update job card
  const updateJobCard = async (jobId, updateData) => {
    const response = await put(`/job-cards/${jobId}`, updateData);
    if (response) {
      fetchJobCards();
    }
  };

  // Close job card
  const closeJobCard = async (jobId) => {
    const response = await patch(`/job-cards/${jobId}/close`);
    if (response) {
      fetchJobCards();
    }
  };

  // Delete job card
  const deleteJobCard = async (jobId) => {
    if (window.confirm('Are you sure you want to delete this job card?')) {
      const response = await del(`/job-cards/${jobId}`);
      if (response) {
        fetchJobCards();
      }
    }
  };

  // Open job details modal
  const openJobDetails = (job) => {
    setSelectedJob(job);
    setShowDetailsModal(true);
  };

  // Close job details modal
  const closeJobDetails = () => {
    setShowDetailsModal(false);
    setSelectedJob(null);
  };

  useEffect(() => {
    fetchJobCards();
    fetchTrains();
  }, []);

  // Apply filters
  const filteredJobCards = jobCards.filter(job => {
    if (filter === 'all') return true;
    return job.status === filter;
  });

  const getStatusBadge = (status) => {
    const statusConfig = {
      open: { color: 'bg-yellow-100 text-yellow-800', label: 'Open' },
      closed: { color: 'bg-gray-100 text-gray-800', label: 'Closed' }
    };
    const config = statusConfig[status] || statusConfig.open;
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color}`}>
        {config.label}
      </span>
    );
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) return <div className="flex justify-center items-center h-screen">Loading job cards...</div>;
  if (error) return <div className="text-red-600 p-4">Error loading job cards: {error}</div>;

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      {/* Main Container - Full Screen */}
      <div className="bg-white rounded-lg shadow-lg h-[calc(100vh-2rem)] flex flex-col ">
        {/* Header */}
        <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center p-6 border-b border-gray-200">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">Job Cards</h2>
            <p className="text-gray-600">Manage maintenance job cards</p>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-3 mt-4 lg:mt-0">
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Jobs</option>
              <option value="open">Open Jobs</option>
              <option value="closed">Closed Jobs</option>
            </select>
            
            <button 
              onClick={() => fetchOpenJobCards()}
              className="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 transition-colors"
            >
              View Open Jobs
            </button>
            
            <button 
              onClick={() => setShowNewJobModal(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              + New Job Card
            </button>
          </div>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-2 gap-4 p-6 border-b border-gray-200">
          <div className="bg-yellow-50 p-4 rounded-lg text-center border border-yellow-200">
            <div className="text-2xl font-bold text-yellow-600">
              {jobCards.filter(j => j.status === 'open').length}
            </div>
            <div className="text-sm text-yellow-800">Open</div>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg text-center border border-gray-200">
            <div className="text-2xl font-bold text-gray-600">
              {jobCards.filter(j => j.status === 'closed').length}
            </div>
            <div className="text-sm text-gray-800">Closed</div>
          </div>
        </div>

        {/* Job Cards Table - Flexible Height */}
        <div className="flex-1 overflow-hidden p-6">
          <div className="h-full flex flex-col">
            <div className="overflow-x-auto flex-1">
              <table className="min-w-full bg-white">
                <thead className="bg-gray-50 sticky top-0">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Job Card ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Work Order ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Description
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Train
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Created
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {filteredJobCards.map((job) => (
                    <tr key={job.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-mono text-gray-900">JC-{job.id}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">{job.work_order_id}</div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm text-gray-500 truncate max-w-xs">{job.description || 'No description'}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">
                          {job.train?.train_number || `Train ${job.train_id}`}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {getStatusBadge(job.status)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm text-gray-900">{formatDate(job.created_at)}</div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                        <button 
                          onClick={() => openJobDetails(job)}
                          className="text-blue-600 hover:text-blue-900 px-2 py-1 rounded hover:bg-blue-50 transition-colors"
                        >
                          Details
                        </button>
                        
                        {job.status === 'open' && (
                          <button
                            onClick={() => closeJobCard(job.id)}
                            className="text-green-600 hover:text-green-900 px-2 py-1 rounded hover:bg-green-50 transition-colors"
                          >
                            Close
                          </button>
                        )}
                        
                        {job.status === 'open' && (
                          <button 
                            onClick={() => deleteJobCard(job.id)}
                            className="text-red-600 hover:text-red-900 px-2 py-1 rounded hover:bg-red-50 transition-colors"
                          >
                            Delete
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              
              {filteredJobCards.length === 0 && (
                <div className="text-center py-12 h-full flex items-center justify-center">
                  <div className="max-w-md">
                    <div className="text-gray-400 text-6xl mb-4">📋</div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No Job Cards Found</h3>
                    <p className="text-gray-600 mb-4">
                      {filter === 'all' 
                        ? "No job cards found. Create your first job card to get started."
                        : `No ${filter} job cards found.`
                      }
                    </p>
                    
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* New Job Card Modal */}
      {showNewJobModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
            <div className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Create New Job Card</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Work Order ID *
                  </label>
                  <input
                    type="text"
                    value={newJobData.work_order_id}
                    onChange={(e) => setNewJobData({...newJobData, work_order_id: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter work order ID"
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    value={newJobData.description}
                    onChange={(e) => setNewJobData({...newJobData, description: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter job description"
                    rows="3"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Assign to Train *
                  </label>
                  <select
                    value={newJobData.train_id}
                    onChange={(e) => setNewJobData({...newJobData, train_id: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    <option value="">Select a train</option>
                    {trains.map(train => (
                      <option key={train.id} value={train.id}>
                        {train.train_number} - {train.name || `Train ${train.id}`}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              
              <div className="flex justify-end space-x-3 mt-6">
                <button
                  onClick={() => setShowNewJobModal(false)}
                  className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={createJobCard}
                  disabled={!newJobData.work_order_id || !newJobData.train_id}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                >
                  Create Job Card
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Job Details Modal */}
      {showDetailsModal && selectedJob && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold text-gray-800">
                  Job Card Details - JC-{selectedJob.id}
                </h3>
                <button
                  onClick={closeJobDetails}
                  className="text-gray-400 hover:text-gray-600 text-2xl transition-colors"
                >
                  ×
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Basic Information */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-lg text-gray-700">Basic Information</h4>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-500">Work Order ID</label>
                    <p className="text-lg font-semibold">{selectedJob.work_order_id}</p>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-500">Description</label>
                    <p className="text-gray-700 mt-1 p-2 bg-gray-50 rounded">
                      {selectedJob.description || 'No description provided'}
                    </p>
                  </div>
                </div>

                {/* Status & Assignment */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-lg text-gray-700">Status & Assignment</h4>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-500">Status</label>
                    <div className="mt-1">{getStatusBadge(selectedJob.status)}</div>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-500">Assigned Train</label>
                    <p className="text-lg">
                      {selectedJob.train?.train_number || `Train ${selectedJob.train_id}`}
                    </p>
                  </div>
                </div>
              </div>

              {/* Timestamps */}
              <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-500">Created</label>
                  <p className="text-sm">{formatDateTime(selectedJob.created_at)}</p>
                </div>
                {selectedJob.closed_at && (
                  <div>
                    <label className="text-sm font-medium text-gray-500">Closed</label>
                    <p className="text-sm">{formatDateTime(selectedJob.closed_at)}</p>
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              <div className="flex justify-end gap-3 mt-6 pt-4 border-t">
                <button
                  onClick={closeJobDetails}
                  className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Close
                </button>
                
                {selectedJob.status === 'open' && (
                  <button
                    onClick={() => {
                      closeJobCard(selectedJob.id);
                      closeJobDetails();
                    }}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                  >
                    Close Job Card
                  </button>
                )}
                
                {selectedJob.status === 'open' && (
                  <button
                    onClick={() => {
                      deleteJobCard(selectedJob.id);
                      closeJobDetails();
                    }}
                    className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                  >
                    Delete Job Card
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Maintenance;