import React, { useState, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';

const TrainStatus = () => {
  const [trainStatus, setTrainStatus] = useState([]);
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedTrain, setSelectedTrain] = useState(null);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const { get, loading, error } = useApi();

  const fetchTrainStatus = async () => {
    const response = await get('/dashboard/train-status');
    if (response) {
      setTrainStatus(response);
    }
  };

  useEffect(() => {
    fetchTrainStatus();
    // Refresh every 30 seconds
    const interval = setInterval(fetchTrainStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  // Sort trains
  const sortedTrains = React.useMemo(() => {
    if (!sortConfig.key) return trainStatus;
    
    return [...trainStatus].sort((a, b) => {
      if (a[sortConfig.key] < b[sortConfig.key]) {
        return sortConfig.direction === 'asc' ? -1 : 1;
      }
      if (a[sortConfig.key] > b[sortConfig.key]) {
        return sortConfig.direction === 'asc' ? 1 : -1;
      }
      return 0;
    });
  }, [trainStatus, sortConfig]);

  const handleSort = (key) => {
    setSortConfig(current => ({
      key,
      direction: current.key === key && current.direction === 'asc' ? 'desc' : 'asc'
    }));
  };

  const filteredTrains = sortedTrains.filter(train => {
    const matchesFilter = filter === 'all' || 
      (filter === 'active' && train.status === 'active') ||
      (filter === 'maintenance' && train.status === 'under_maintenance') ||
      (filter === 'eligible' && train.eligibility === 'eligible') ||
      (filter === 'service' && train.today_induction === 'service');
    
    const matchesSearch = train.train_number.toLowerCase().includes(searchTerm.toLowerCase()) ||
      train.train_id.toString().includes(searchTerm);
    
    return matchesFilter && matchesSearch;
  });

  const getStatusBadge = (status) => {
    const statusConfig = {
      active: { color: 'bg-green-100 text-green-800', label: 'Active' },
      under_maintenance: { color: 'bg-yellow-100 text-yellow-800', label: 'Maintenance' },
      retired: { color: 'bg-gray-100 text-gray-800', label: 'Retired' }
    };
    const config = statusConfig[status] || statusConfig.active;
    return <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>{config.label}</span>;
  };

  const getEligibilityBadge = (eligibility) => {
    const eligibilityConfig = {
      eligible: { color: 'bg-green-100 text-green-800', label: 'Eligible' },
      not_eligible: { color: 'bg-red-100 text-red-800', label: 'Not Eligible' },
      maintenance_required: { color: 'bg-orange-100 text-orange-800', label: 'Maintenance Needed' },
      certificate_expired: { color: 'bg-red-100 text-red-800', label: 'Certificate Expired' },
      unknown: { color: 'bg-gray-100 text-gray-800', label: 'Unknown' }
    };
    const config = eligibilityConfig[eligibility] || eligibilityConfig.unknown;
    return <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>{config.label}</span>;
  };

  const getInductionBadge = (inductionType) => {
    const inductionConfig = {
      service: { color: 'bg-blue-100 text-blue-800', label: 'Service' },
      standby: { color: 'bg-purple-100 text-purple-800', label: 'Standby' },
      maintenance: { color: 'bg-yellow-100 text-yellow-800', label: 'Maintenance' },
      not_scheduled: { color: 'bg-gray-100 text-gray-800', label: 'Not Scheduled' }
    };
    const config = inductionConfig[inductionType] || inductionConfig.not_scheduled;
    return <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>{config.label}</span>;
  };

  const handleTrainClick = (train) => {
    setSelectedTrain(train);
    setShowDetailsModal(true);
  };

  const handleBulkAction = async (action) => {
    // Example bulk actions
    const selectedTrains = filteredTrains; // In real app, you'd have selection checkboxes
    
    switch (action) {
      case 'checkEligibility':
        alert(`Running eligibility check on ${selectedTrains.length} trains...`);
        // await api.bulkCheckEligibility(selectedTrains.map(t => t.train_id));
        break;
      case 'exportData':
        const csvContent = "data:text/csv;charset=utf-8," 
          + ["Train Number,Status,Eligibility,Mileage"].join(",") + "\\n"
          + selectedTrains.map(train => 
              `${train.train_number},${train.status},${train.eligibility},${train.mileage}`
            ).join("\\n");
        
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "train_status_export.csv");
        document.body.appendChild(link);
        link.click();
        break;
      case 'scheduleMaintenance':
        alert(`Scheduling maintenance for ${selectedTrains.length} trains...`);
        // await api.scheduleBulkMaintenance(selectedTrains.map(t => t.train_id));
        break;
    }
  };

  const stats = {
    total: trainStatus.length,
    active: trainStatus.filter(t => t.status === 'active').length,
    eligible: trainStatus.filter(t => t.eligibility === 'eligible').length,
    inService: trainStatus.filter(t => t.today_induction === 'service').length,
    maintenance: trainStatus.filter(t => t.status === 'under_maintenance').length
  };

  if (loading && trainStatus.length === 0) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-2">Loading train status...</span>
      </div>
    );
  }

  if (error) return <div className="text-red-600 bg-red-50 p-4 rounded-lg">Error loading train status: {error}</div>;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      {/* Header with Actions */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Train Status Overview</h2>
        <div className="flex space-x-2">
          <button 
            onClick={() => handleBulkAction('exportData')}
            className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors text-sm"
          >
            Export Data
          </button>
          <button 
            onClick={fetchTrainStatus}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center"
          >
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Refresh
          </button>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
        <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
          <div className="text-2xl font-bold text-blue-600">{stats.total}</div>
          <div className="text-sm text-blue-800">Total Trains</div>
        </div>
        <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
          <div className="text-2xl font-bold text-green-600">{stats.active}</div>
          <div className="text-sm text-green-800">Active Trains</div>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
          <div className="text-2xl font-bold text-purple-600">{stats.eligible}</div>
          <div className="text-sm text-purple-800">Eligible</div>
        </div>
        <div className="bg-orange-50 p-4 rounded-lg border-l-4 border-orange-500">
          <div className="text-2xl font-bold text-orange-600">{stats.inService}</div>
          <div className="text-sm text-orange-800">In Service</div>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg border-l-4 border-yellow-500">
          <div className="text-2xl font-bold text-yellow-600">{stats.maintenance}</div>
          <div className="text-sm text-yellow-800">Maintenance</div>
        </div>
      </div>

      {/* Filters, Search, and Bulk Actions */}
      <div className="flex flex-col md:flex-row gap-4 mb-6">
        <div className="flex flex-wrap gap-2">
          {[
            { key: 'all', label: 'All Trains' },
            { key: 'active', label: 'Active' },
            { key: 'maintenance', label: 'Maintenance' },
            { key: 'eligible', label: 'Eligible' },
            { key: 'service', label: 'In Service' }
          ].map(({ key, label }) => (
            <button
              key={key}
              onClick={() => setFilter(key)}
              className={`px-3 py-2 rounded-lg transition-colors text-sm ${
                filter === key 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {label}
            </button>
          ))}
        </div>
        
        <div className="flex-1">
          <div className="relative">
            <input
              type="text"
              placeholder="Search by train number or ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-4 py-2 pl-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <svg className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
      </div>

      {/* Train Status Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white">
          <thead>
            <tr className="bg-gray-50">
              <th 
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                onClick={() => handleSort('train_number')}
              >
                <div className="flex items-center">
                  Train
                  {sortConfig.key === 'train_number' && (
                    <span className="ml-1">{sortConfig.direction === 'asc' ? '↑' : '↓'}</span>
                  )}
                </div>
              </th>
              <th 
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                onClick={() => handleSort('status')}
              >
                <div className="flex items-center">
                  Status
                  {sortConfig.key === 'status' && (
                    <span className="ml-1">{sortConfig.direction === 'asc' ? '↑' : '↓'}</span>
                  )}
                </div>
              </th>
              <th 
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                onClick={() => handleSort('eligibility')}
              >
                <div className="flex items-center">
                  Eligibility
                  {sortConfig.key === 'eligibility' && (
                    <span className="ml-1">{sortConfig.direction === 'asc' ? '↑' : '↓'}</span>
                  )}
                </div>
              </th>
              <th 
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                onClick={() => handleSort('mileage')}
              >
                <div className="flex items-center">
                  Mileage
                  {sortConfig.key === 'mileage' && (
                    <span className="ml-1">{sortConfig.direction === 'asc' ? '↑' : '↓'}</span>
                  )}
                </div>
              </th>
              <th 
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                onClick={() => handleSort('open_job_cards')}
              >
                <div className="flex items-center">
                  Open Jobs
                  {sortConfig.key === 'open_job_cards' && (
                    <span className="ml-1">{sortConfig.direction === 'asc' ? '↑' : '↓'}</span>
                  )}
                </div>
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Today's Plan
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Branding
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filteredTrains.map((train) => (
              <tr 
                key={train.train_id} 
                className="hover:bg-gray-50 cursor-pointer transition-colors"
                onClick={() => handleTrainClick(train)}
              >
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="text-sm font-medium text-gray-900">
                      {train.train_number}
                    </div>
                    <div className="ml-2 text-sm text-gray-500">
                      ID: {train.train_id}
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {getStatusBadge(train.status)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {getEligibilityBadge(train.eligibility)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {train.mileage.toLocaleString()} km
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-medium ${
                    train.open_job_cards > 0 
                      ? 'bg-red-100 text-red-800' 
                      : 'bg-green-100 text-green-800'
                  }`}>
                    {train.open_job_cards}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center space-x-2">
                    {getInductionBadge(train.today_induction)}
                    {train.today_rank && (
                      <span className="text-xs text-gray-500">#{train.today_rank}</span>
                    )}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-medium ${
                    train.active_branding_contracts > 0 
                      ? 'bg-purple-100 text-purple-800' 
                      : 'bg-gray-100 text-gray-800'
                  }`}>
                    {train.active_branding_contracts}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {filteredTrains.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            {searchTerm ? 'No trains match your search criteria.' : 'No trains available.'}
          </div>
        )}
      </div>

      {/* Summary and Bulk Actions */}
      <div className="mt-4 flex justify-between items-center">
        <div className="text-sm text-gray-600">
          Showing {filteredTrains.length} of {trainStatus.length} trains
        </div>
        <div className="flex space-x-2">
          <button 
            onClick={() => handleBulkAction('checkEligibility')}
            className="text-sm bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
          >
            Check Eligibility
          </button>
          <button 
            onClick={() => handleBulkAction('scheduleMaintenance')}
            className="text-sm bg-yellow-600 text-white px-3 py-1 rounded hover:bg-yellow-700"
          >
            Schedule Maintenance
          </button>
        </div>
      </div>

      {/* Train Details Modal */}
      {showDetailsModal && selectedTrain && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-bold">Train Details - {selectedTrain.train_number}</h3>
                <button 
                  onClick={() => setShowDetailsModal(false)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ×
                </button>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-500">Train ID</label>
                  <p className="text-sm">{selectedTrain.train_id}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Status</label>
                  <p>{getStatusBadge(selectedTrain.status)}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Eligibility</label>
                  <p>{getEligibilityBadge(selectedTrain.eligibility)}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Mileage</label>
                  <p className="text-sm">{selectedTrain.mileage.toLocaleString()} km</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Open Job Cards</label>
                  <p className="text-sm">{selectedTrain.open_job_cards}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Today's Induction</label>
                  <p>{getInductionBadge(selectedTrain.today_induction)}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Branding Contracts</label>
                  <p className="text-sm">{selectedTrain.active_branding_contracts}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Today's Rank</label>
                  <p className="text-sm">{selectedTrain.today_rank || 'N/A'}</p>
                </div>
              </div>
              
              <div className="mt-6 flex justify-end space-x-2">
                <button 
                  onClick={() => setShowDetailsModal(false)}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800"
                >
                  Close
                </button>
                <button 
                  onClick={() => {
                    // Add action for train details
                    alert(`Actions for ${selectedTrain.train_number}`);
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Manage Train
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TrainStatus;