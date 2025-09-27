import React, { useState, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';

const BrandingStatus = ({ isOpen, onClose, brandingData }) => {
  const [contracts, setContracts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedContract, setSelectedContract] = useState(null);
  const [showUpdateModal, setShowUpdateModal] = useState(false);
  const [hoursToAdd, setHoursToAdd] = useState('');
  const { get, post, loading: apiLoading } = useApi();

  useEffect(() => {
    if (isOpen) {
      fetchContractsNeedExposure();
    }
  }, [isOpen]);

  const fetchContractsNeedExposure = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await get('/branding/need-exposure');
      setContracts(data || []);
    } catch (err) {
      setError('Failed to fetch contracts');
      console.error('Error fetching contracts:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAllContracts = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await get('/branding/');
      setContracts(data || []);
    } catch (err) {
      setError('Failed to fetch contracts');
      console.error('Error fetching contracts:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateExposure = async (contractId) => {
    if (!hoursToAdd || isNaN(hoursToAdd) || parseInt(hoursToAdd) <= 0) {
      setError('Please enter a valid number of hours');
      return;
    }

    try {
      await post(`/branding/${contractId}/exposure`, { hours: parseInt(hoursToAdd) });
      setShowUpdateModal(false);
      setSelectedContract(null);
      setHoursToAdd('');
      fetchContractsNeedExposure(); // Refresh data
    } catch (err) {
      setError('Failed to update exposure hours');
      console.error('Error updating exposure:', err);
    }
  };

  const calculateExposureGap = (contract) => {
    const required = contract.exposure_hours_required || 0;
    const fulfilled = contract.exposure_hours_fulfilled || 0;
    const gap = required - fulfilled;
    const percentage = required > 0 ? Math.round((fulfilled / required) * 100) : 0;
    
    return { gap, percentage };
  };

  const getContractStatus = (contract) => {
    const { gap, percentage } = calculateExposureGap(contract);
    
    if (gap <= 0) return { status: 'Compliant', color: 'green' };
    if (percentage >= 80) return { status: 'Good', color: 'blue' };
    if (percentage >= 60) return { status: 'Need Attention', color: 'yellow' };
    return { status: 'At Risk', color: 'red' };
  };

  const getStatusColor = (status) => {
    const colors = {
      'Compliant': 'bg-green-100 text-green-800',
      'Good': 'bg-blue-100 text-blue-800',
      'Need Attention': 'bg-yellow-100 text-yellow-800',
      'At Risk': 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-6xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center border-b border-gray-200 px-6 py-4">
          <h2 className="text-xl font-semibold text-gray-900">Branding Contracts Management</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl font-bold"
          >
            ×
          </button>
        </div>
        
        <div className="p-6">
          {/* Summary Stats */}
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Contract Exposure Summary</h3>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="text-2xl font-bold text-red-600">
                  {contracts.filter(contract => getContractStatus(contract).status === 'At Risk').length}
                </div>
                <div className="text-sm text-red-700">At Risk Contracts</div>
              </div>
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <div className="text-2xl font-bold text-yellow-600">
                  {contracts.filter(contract => getContractStatus(contract).status === 'Need Attention').length}
                </div>
                <div className="text-sm text-yellow-700">Need Attention</div>
              </div>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="text-2xl font-bold text-blue-600">
                  {contracts.filter(contract => getContractStatus(contract).status === 'Good').length}
                </div>
                <div className="text-sm text-blue-700">Good Standing</div>
              </div>
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <div className="text-2xl font-bold text-green-600">
                  {contracts.filter(contract => getContractStatus(contract).status === 'Compliant').length}
                </div>
                <div className="text-sm text-green-700">Compliant</div>
              </div>
            </div>
          </div>

          {/* Filter Buttons */}
          <div className="flex space-x-4 mb-6">
            <button
              onClick={fetchContractsNeedExposure}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Show Contracts Needing Exposure
            </button>
            <button
              onClick={fetchAllContracts}
              className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
            >
              Show All Contracts
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
              <div className="flex items-center">
                <div className="text-red-600 text-lg mr-2">❌</div>
                <div className="text-red-700 text-sm">{error}</div>
              </div>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="flex justify-center items-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          )}

          {/* Contracts Table */}
          {!loading && (
            <div>
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                Contracts ({contracts.length} total)
              </h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Contract ID
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Train ID
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Status
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Exposure Hours
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Progress
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Gap
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {contracts.map((contract) => {
                      const { gap, percentage } = calculateExposureGap(contract);
                      const statusInfo = getContractStatus(contract);
                      
                      return (
                        <tr key={contract.contract_id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            CT-{contract.contract_id}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            TR-{contract.train_id}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(statusInfo.status)}`}>
                              {statusInfo.status}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {contract.exposure_hours_fulfilled || 0}/{contract.exposure_hours_required || 0}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div 
                                className={`h-2 rounded-full ${
                                  statusInfo.color === 'red' ? 'bg-red-500' :
                                  statusInfo.color === 'yellow' ? 'bg-yellow-500' :
                                  statusInfo.color === 'blue' ? 'bg-blue-500' : 'bg-green-500'
                                }`}
                                style={{ width: `${Math.min(percentage, 100)}%` }}
                              ></div>
                            </div>
                            <div className="text-xs text-gray-500 mt-1">{percentage}%</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            <span className={gap > 0 ? 'text-red-600 font-medium' : 'text-green-600 font-medium'}>
                              {gap > 0 ? `-${gap}h` : 'Completed'}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <button
                              onClick={() => {
                                setSelectedContract(contract);
                                setShowUpdateModal(true);
                              }}
                              className="text-blue-600 hover:text-blue-900 mr-3"
                            >
                              Update Hours
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                    {contracts.length === 0 && !loading && (
                      <tr>
                        <td colSpan="7" className="px-6 py-4 text-center text-sm text-gray-500">
                          No contracts found.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
        
        <div className="border-t border-gray-200 px-6 py-4">
          <button
            onClick={onClose}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Close
          </button>
        </div>
      </div>

      {/* Update Exposure Hours Modal */}
      {showUpdateModal && selectedContract && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-60">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Update Exposure Hours - Contract CT-{selectedContract.contract_id}
            </h3>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Hours to Add
              </label>
              <input
                type="number"
                min="1"
                value={hoursToAdd}
                onChange={(e) => setHoursToAdd(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter hours"
              />
            </div>

            <div className="bg-gray-50 p-3 rounded-lg mb-4">
              <div className="text-sm text-gray-600">
                Current: {selectedContract.exposure_hours_fulfilled || 0}h / {selectedContract.exposure_hours_required || 0}h
              </div>
              <div className="text-sm text-gray-600">
                After update: {(selectedContract.exposure_hours_fulfilled || 0) + parseInt(hoursToAdd || 0)}h / {selectedContract.exposure_hours_required || 0}h
              </div>
            </div>

            <div className="flex space-x-3">
              <button
                onClick={() => handleUpdateExposure(selectedContract.contract_id)}
                disabled={apiLoading}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
              >
                {apiLoading ? 'Updating...' : 'Update Hours'}
              </button>
              <button
                onClick={() => {
                  setShowUpdateModal(false);
                  setSelectedContract(null);
                  setHoursToAdd('');
                }}
                className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BrandingStatus;