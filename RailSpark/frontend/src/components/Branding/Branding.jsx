import React, { useState, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';

const Branding = () => {
  const [contracts, setContracts] = useState([]);
  const [filter, setFilter] = useState('all');
  const [showNewContractModal, setShowNewContractModal] = useState(false);
  const [newContractData, setNewContractData] = useState({
    advertiser_name: '',
    contract_value: '',
    start_date: '',
    end_date: '',
    exposure_hours_required: '',
    exposure_hours_fulfilled: 0,
    train_id: '',
    status: 'active'
  });
  const [trains, setTrains] = useState([]);
  const { get, post, put, patch, delete: deleteApi, loading, error } = useApi();

  // Fetch branding contracts from backend
  const fetchContracts = async () => {
    const response = await get('/branding/');
    if (response) {
      setContracts(response);
    }
  };

  // Fetch active contracts only
  const fetchActiveContracts = async () => {
    const response = await get('/branding/active');
    if (response) {
      setContracts(response);
    }
  };

  // Fetch contracts needing exposure
  const fetchContractsNeedExposure = async () => {
    const response = await get('/branding/need-exposure');
    if (response) {
      setContracts(response);
    }
  };

  // Fetch trains for assignment
  const fetchTrains = async () => {
    const response = await get('/trains');
    if (response) {
      setTrains(response);
    }
  };

  // Create new branding contract
  const createContract = async () => {
    const response = await post('/branding/', newContractData);
    if (response) {
      setShowNewContractModal(false);
      setNewContractData({
        advertiser_name: '',
        contract_value: '',
        start_date: '',
        end_date: '',
        exposure_hours_required: '',
        exposure_hours_fulfilled: 0,
        train_id: '',
        status: 'active'
      });
      fetchContracts();
    }
  };

  // Update contract
  const updateContract = async (contractId, updateData) => {
    const response = await put(`/branding/${contractId}`, updateData);
    if (response) {
      fetchContracts();
    }
  };

  // Update exposure hours
  const updateExposureHours = async (contractId, hours) => {
    const response = await patch(`/branding/${contractId}/exposure`, {
      exposure_hours: hours
    });
    if (response) {
      fetchContracts();
    }
  };

  // Delete contract
  const deleteContract = async (contractId) => {
    if (window.confirm('Are you sure you want to delete this contract?')) {
      const response = await deleteApi(`/branding/${contractId}`);
      if (response) {
        fetchContracts();
      }
    }
  };

  useEffect(() => {
    fetchContracts();
    fetchTrains();
  }, []);

  // Apply filters
  const filteredContracts = contracts.filter(contract => {
    if (filter === 'all') return true;
    if (filter === 'active') return contract.status === 'active';
    if (filter === 'needs_exposure') return contract.exposure_hours_fulfilled < contract.exposure_hours_required;
    return contract.status === filter;
  });

  const getStatusBadge = (status) => {
    const statusConfig = {
      active: { color: 'bg-green-100 text-green-800', label: 'Active' },
      expired: { color: 'bg-red-100 text-red-800', label: 'Expired' },
      completed: { color: 'bg-blue-100 text-blue-800', label: 'Completed' },
      cancelled: { color: 'bg-gray-100 text-gray-800', label: 'Cancelled' }
    };
    const config = statusConfig[status] || statusConfig.active;
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color}`}>
        {config.label}
      </span>
    );
  };

  const getExposureProgress = (contract) => {
    const progress = (contract.exposure_hours_fulfilled / contract.exposure_hours_required) * 100;
    return Math.min(progress, 100);
  };

  const getExposureColor = (progress) => {
    if (progress >= 90) return 'bg-green-500';
    if (progress >= 70) return 'bg-yellow-500';
    if (progress >= 50) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR'
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const isContractExpiring = (endDate) => {
    const daysUntilExpiry = Math.ceil((new Date(endDate) - new Date()) / (1000 * 60 * 60 * 24));
    return daysUntilExpiry <= 7;
  };

  if (loading) return <div className="flex justify-center items-center h-64">Loading branding contracts...</div>;
  if (error) return <div className="text-red-600">Error loading contracts: {error}</div>;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-6 gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Branding Contracts</h2>
          <p className="text-gray-600">Manage advertising contracts and exposure tracking</p>
        </div>
        
        <div className="flex flex-col sm:flex-row gap-3">
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Contracts</option>
            <option value="active">Active</option>
            <option value="needs_exposure">Needs Exposure</option>
            <option value="expired">Expired</option>
            <option value="completed">Completed</option>
          </select>
          
          <button 
            onClick={() => fetchActiveContracts()}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
          >
            Active Contracts
          </button>
          
          <button 
            onClick={() => fetchContractsNeedExposure()}
            className="bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 transition-colors"
          >
            Needs Exposure
          </button>
          
          <button 
            onClick={() => setShowNewContractModal(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            + New Contract
          </button>
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-green-50 p-4 rounded-lg text-center">
          <div className="text-2xl font-bold text-green-600">
            {contracts.filter(c => c.status === 'active').length}
          </div>
          <div className="text-sm text-green-800">Active</div>
        </div>
        <div className="bg-orange-50 p-4 rounded-lg text-center">
          <div className="text-2xl font-bold text-orange-600">
            {contracts.filter(c => c.exposure_hours_fulfilled < c.exposure_hours_required).length}
          </div>
          <div className="text-sm text-orange-800">Need Exposure</div>
        </div>
        <div className="bg-blue-50 p-4 rounded-lg text-center">
          <div className="text-2xl font-bold text-blue-600">
            {formatCurrency(contracts.reduce((sum, c) => sum + (c.contract_value || 0), 0))}
          </div>
          <div className="text-sm text-blue-800">Total Value</div>
        </div>
        <div className="bg-red-50 p-4 rounded-lg text-center">
          <div className="text-2xl font-bold text-red-600">
            {contracts.filter(c => isContractExpiring(c.end_date)).length}
          </div>
          <div className="text-sm text-red-800">Expiring Soon</div>
        </div>
      </div>

      {/* Contracts Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white">
          <thead>
            <tr className="bg-gray-50">
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Advertiser
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Train
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Contract Value
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Exposure Progress
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Period
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filteredContracts.map((contract) => {
              const progress = getExposureProgress(contract);
              const isExpiring = isContractExpiring(contract.end_date);
              
              return (
                <tr key={contract.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="text-sm font-medium text-gray-900">{contract.advertiser_name}</div>
                    <div className="text-sm text-gray-500">Contract #{contract.id}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {contract.train?.train_number || `Train ${contract.train_id}`}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {formatCurrency(contract.contract_value)}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-2">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${getExposureColor(progress)}`}
                          style={{ width: `${progress}%` }}
                        ></div>
                      </div>
                      <span className="text-xs text-gray-600 whitespace-nowrap">
                        {contract.exposure_hours_fulfilled}h / {contract.exposure_hours_required}h
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">
                      {formatDate(contract.start_date)} - {formatDate(contract.end_date)}
                    </div>
                    {isExpiring && (
                      <div className="text-xs text-red-600">Expiring soon!</div>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {getStatusBadge(contract.status)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button
                      onClick={() => updateExposureHours(contract.id, contract.exposure_hours_fulfilled + 1)}
                      className="text-blue-600 hover:text-blue-900"
                    >
                      +1h
                    </button>
                    <button className="text-gray-600 hover:text-gray-900">
                      Edit
                    </button>
                    <button 
                      onClick={() => deleteContract(contract.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        
        {filteredContracts.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">📢</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No Branding Contracts</h3>
            <p className="text-gray-600 mb-4">
              {filter === 'all' 
                ? "No branding contracts found. Create your first contract to get started."
                : `No ${filter} contracts found.`
              }
            </p>
            <button 
              onClick={() => setShowNewContractModal(true)}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Create New Contract
            </button>
          </div>
        )}
      </div>

      {/* New Contract Modal */}
      {showNewContractModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
            <div className="p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Create New Branding Contract</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Advertiser Name *
                  </label>
                  <input
                    type="text"
                    value={newContractData.advertiser_name}
                    onChange={(e) => setNewContractData({...newContractData, advertiser_name: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter advertiser name"
                    required
                  />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Contract Value *
                    </label>
                    <input
                      type="number"
                      value={newContractData.contract_value}
                      onChange={(e) => setNewContractData({...newContractData, contract_value: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="₹ Amount"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Exposure Hours Required *
                    </label>
                    <input
                      type="number"
                      value={newContractData.exposure_hours_required}
                      onChange={(e) => setNewContractData({...newContractData, exposure_hours_required: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Hours"
                      required
                    />
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Start Date *
                    </label>
                    <input
                      type="date"
                      value={newContractData.start_date}
                      onChange={(e) => setNewContractData({...newContractData, start_date: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      End Date *
                    </label>
                    <input
                      type="date"
                      value={newContractData.end_date}
                      onChange={(e) => setNewContractData({...newContractData, end_date: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Assign to Train *
                  </label>
                  <select
                    value={newContractData.train_id}
                    onChange={(e) => setNewContractData({...newContractData, train_id: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  >
                    <option value="">Select a train</option>
                    {trains.map(train => (
                      <option key={train.id} value={train.id}>
                        {train.train_number} - {train.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              
              <div className="flex justify-end space-x-3 mt-6">
                <button
                  onClick={() => setShowNewContractModal(false)}
                  className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  onClick={createContract}
                  disabled={!newContractData.advertiser_name || !newContractData.train_id || !newContractData.start_date || !newContractData.end_date}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                  Create Contract
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Branding;