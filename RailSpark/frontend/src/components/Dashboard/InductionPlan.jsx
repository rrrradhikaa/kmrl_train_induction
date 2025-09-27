import React, { useState, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';

const InductionPlan = () => {
  const [inductionPlan, setInductionPlan] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [planStats, setPlanStats] = useState(null);
  const [brandingScore, setBrandingScore] = useState(75);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState(null);
  const { get, post, loading, error } = useApi();

  const fetchInductionPlan = async (date = selectedDate) => {
    const response = await get(`/induction/date/${date}`);
    if (response) {
      setInductionPlan(response);
      calculateStats(response);
    }
  };

  const generateNewPlan = async () => {
    try {
      const response = await post('/ai/generate-plan', {
        plan_date: selectedDate
      });
      
      if (response) {
        await post('/induction/bulk', response);
        fetchInductionPlan();
      }
    } catch (error) {
      console.error('Error:', error);
      setError('Cannot generate plan due to backend issues. Please contact support.');
    }
  };

  const calculateStats = (plan) => {
    const stats = {
      service: plan.filter(p => p.induction_type === 'service').length,
      standby: plan.filter(p => p.induction_type === 'standby').length,
      maintenance: plan.filter(p => p.induction_type === 'maintenance').length,
      approved: plan.filter(p => p.approved_by).length,
      total: plan.length
    };
    setPlanStats(stats);
  };

  const approvePlan = async (planId) => {
    const userId = 1;
    await post(`/induction/${planId}/approve?approved_by=${userId}`);
    fetchInductionPlan();
  };

  const approveAll = async () => {
    try {
      const userId = 1;
      const approvalPromises = inductionPlan
        .filter(plan => !plan.approved_by)
        .map(plan => 
          post(`/induction/${plan.id}/approve?approved_by=${userId}`)
        );
      
      await Promise.all(approvalPromises);
      fetchInductionPlan();
      alert(`Successfully approved ${approvalPromises.length} plans!`);
    } catch (error) {
      console.error('Error approving all plans:', error);
      alert(`Failed to approve all plans: ${error.message}`);
    }
  };

  // Details Modal Functions
  const openPlanDetails = (plan) => {
    setSelectedPlan(plan);
    setShowDetailsModal(true);
  };

  const closePlanDetails = () => {
    setShowDetailsModal(false);
    setSelectedPlan(null);
  };

  // Format datetime for display
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

  useEffect(() => {
    fetchInductionPlan();
  }, [selectedDate]);

  const getInductionTypeBadge = (type) => {
    const typeConfig = {
      service: { color: 'bg-blue-100 text-blue-800', icon: '🚆' },
      standby: { color: 'bg-purple-100 text-purple-800', icon: '⏳' },
      maintenance: { color: 'bg-yellow-100 text-yellow-800', icon: '🔧' }
    };
    const config = typeConfig[type] || typeConfig.service;
    return (
      <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${config.color}`}>
        <span className="mr-2">{config.icon}</span>
        {type.charAt(0).toUpperCase() + type.slice(1)}
      </span>
    );
  };

  const getApprovalStatus = (plan) => {
    if (plan.approved_by) {
      return <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">Approved</span>;
    }
    return <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-yellow-100 text-yellow-800">Pending</span>;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) return <div className="flex justify-center items-center h-64">Loading induction plan...</div>;
  if (error) return <div className="text-red-600">Error loading induction plan: {error}</div>;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-6 gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Induction Plan</h2>
          <p className="text-gray-600">{formatDate(selectedDate)}</p>
        </div>
        
        <div className="flex flex-col sm:flex-row gap-3">
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          
          <div className="flex items-center gap-2 bg-gray-50 px-3 py-2 rounded-lg">
            <label htmlFor="brandingScore" className="text-sm text-gray-600 whitespace-nowrap">
              Branding Score:
            </label>
            <input
              id="brandingScore"
              type="number"
              min="0"
              max="100"
              value={brandingScore}
              onChange={(e) => setBrandingScore(parseInt(e.target.value) || 75)}
              className="w-16 px-2 py-1 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 text-sm"
            />
          </div>
          
          <button 
            onClick={generateNewPlan}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
            disabled={loading}
          >
            {loading ? 'Generating...' : 'Generate New Plan'}
          </button>
          <button 
            onClick={() => fetchInductionPlan()}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Refresh
          </button>
        </div>
      </div>

      {/* Statistics */}
      {planStats && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
          <div className="bg-blue-50 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-blue-600">{planStats.service}</div>
            <div className="text-sm text-blue-800">Service Trains</div>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-purple-600">{planStats.standby}</div>
            <div className="text-sm text-purple-800">Standby Trains</div>
          </div>
          <div className="bg-yellow-50 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-yellow-600">{planStats.maintenance}</div>
            <div className="text-sm text-yellow-800">Maintenance</div>
          </div>
          <div className="bg-green-50 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-green-600">{planStats.approved}</div>
            <div className="text-sm text-green-800">Approved</div>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg text-center">
            <div className="text-2xl font-bold text-gray-600">{planStats.total}</div>
            <div className="text-sm text-gray-800">Total Planned</div>
          </div>
        </div>
      )}

      {/* Approval Actions */}
      {inductionPlan.length > 0 && (
        <div className="mb-6 p-4 bg-gray-50 rounded-lg">
          <div className="flex justify-between items-center">
            <div>
              <span className="font-medium">Plan Approval Status: </span>
              {planStats && (
                <span className={planStats.approved === planStats.total ? 'text-green-600' : 'text-yellow-600'}>
                  {planStats.approved} of {planStats.total} approved
                </span>
              )}
            </div>
            {planStats && planStats.approved < planStats.total && (
              <button 
                onClick={approveAll}
                className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors text-sm"
              >
                Approve All
              </button>
            )}
          </div>
        </div>
      )}

      {/* Induction Plan Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white">
          <thead>
            <tr className="bg-gray-50">
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rank</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Train</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reason</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Score</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {inductionPlan.map((plan) => (
              <tr key={plan.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">#{plan.rank}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">
                    {plan.train?.train_number || `Train ${plan.train_id}`}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {getInductionTypeBadge(plan.induction_type)}
                </td>
                <td className="px-6 py-4">
                  <div className="text-sm text-gray-900 max-w-xs truncate" title={plan.reason}>
                    {plan.reason || 'No reason provided'}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900">
                    {plan.score ? `${(plan.score * 100).toFixed(1)}%` : 'N/A'}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {getApprovalStatus(plan)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  {!plan.approved_by && (
                    <button
                      onClick={() => approvePlan(plan.id)}
                      className="text-green-600 hover:text-green-900 mr-3"
                    >
                      Approve
                    </button>
                  )}
                  <button 
                    onClick={() => openPlanDetails(plan)}
                    className="text-blue-600 hover:text-blue-900"
                  >
                    Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {inductionPlan.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">📋</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No Induction Plan</h3>
            <p className="text-gray-600 mb-4">No induction plan has been generated for this date.</p>
            <button 
              onClick={generateNewPlan}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              disabled={loading}
            >
              {loading ? 'Generating...' : 'Generate Plan'}
            </button>
          </div>
        )}
      </div>

      {/* Plan Summary */}
      {inductionPlan.length > 0 && (
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h4 className="font-medium text-blue-900 mb-2">Plan Summary</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-blue-800">
            <div><strong>Service Trains:</strong> {planStats?.service} trains for passenger service</div>
            <div><strong>Standby Trains:</strong> {planStats?.standby} trains on standby</div>
            <div><strong>Maintenance:</strong> {planStats?.maintenance} trains scheduled for maintenance</div>
          </div>
        </div>
      )}

      {/* Details Modal */}
      {showDetailsModal && selectedPlan && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            {/* Modal Header */}
            <div className="flex justify-between items-center p-6 border-b">
              <h3 className="text-xl font-bold text-gray-800">
                Plan Details - Train {selectedPlan.train?.train_number || selectedPlan.train_id}
              </h3>
              <button
                onClick={closePlanDetails}
                className="text-gray-400 hover:text-gray-600 text-2xl"
              >
                ×
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Basic Information */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-lg text-gray-700">Basic Information</h4>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-500">Rank</label>
                    <p className="text-lg font-semibold">#{selectedPlan.rank}</p>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-500">Induction Type</label>
                    <div className="mt-1">{getInductionTypeBadge(selectedPlan.induction_type)}</div>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-500">Plan Date</label>
                    <p className="text-lg">{formatDate(selectedPlan.plan_date)}</p>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-500">Score</label>
                    <p className="text-lg">
                      {selectedPlan.score ? `${(selectedPlan.score * 100).toFixed(1)}%` : 'N/A'}
                    </p>
                  </div>
                </div>

                {/* Status & Approval Information */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-lg text-gray-700">Status & Approval</h4>
                  
                  <div>
                    <label className="text-sm font-medium text-gray-500">Approval Status</label>
                    <div className="mt-1">{getApprovalStatus(selectedPlan)}</div>
                  </div>
                  
                  {selectedPlan.approved_by && (
                    <>
                      <div>
                        <label className="text-sm font-medium text-gray-500">Approved By</label>
                        <p className="text-lg">User #{selectedPlan.approved_by}</p>
                      </div>
                      
                      <div>
                        <label className="text-sm font-medium text-gray-500">Approved At</label>
                        <p className="text-lg">{formatDateTime(selectedPlan.approved_at)}</p>
                      </div>
                    </>
                  )}
                  
                  <div>
                    <label className="text-sm font-medium text-gray-500">Created At</label>
                    <p className="text-lg">{formatDateTime(selectedPlan.created_at)}</p>
                  </div>
                </div>
              </div>

              {/* Reason Section */}
              <div className="mt-6">
                <label className="text-sm font-medium text-gray-500">Reason</label>
                <p className="mt-2 p-4 bg-gray-50 rounded-lg text-gray-700">
                  {selectedPlan.reason || 'No reason provided'}
                </p>
              </div>

              {/* Train Details (if available) */}
              {selectedPlan.train && (
                <div className="mt-6">
                  <h4 className="font-semibold text-lg text-gray-700 mb-4">Train Information</h4>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    <div>
                      <label className="text-sm font-medium text-gray-500">Train Number</label>
                      <p className="font-semibold">{selectedPlan.train.train_number}</p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-500">Capacity</label>
                      <p>{selectedPlan.train.capacity || 'N/A'}</p>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-gray-500">Status</label>
                      <p>{selectedPlan.train.status || 'N/A'}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="flex justify-end gap-3 p-6 border-t">
              <button
                onClick={closePlanDetails}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 font-medium"
              >
                Close
              </button>
              {!selectedPlan.approved_by && (
                <button
                  onClick={() => {
                    approvePlan(selectedPlan.id);
                    closePlanDetails();
                  }}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium"
                >
                  Approve Plan
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default InductionPlan;