import React, { useState, useEffect } from 'react';
import { useApi } from '../hooks/useApi';
import TrainStatus from '../components/Dashboard/TrainStatus';
import InductionPlan from '../components/Dashboard/InductionPlan';
import MaintenanceAlerts from '../components/Dashboard/MaintenanceAlerts';
import BrandingStatus from '../components/Dashboard/BrandingStatus';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');
  const [showMaintenanceModal, setShowMaintenanceModal] = useState(false);
  const [showBrandingModal, setShowBrandingModal] = useState(false);
  const { get, loading, error } = useApi();

  const fetchDashboardData = async () => {
    const data = await get('/dashboard/overview');
    if (data) {
      setDashboardData(data);
    }
  };

  useEffect(() => {
    fetchDashboardData();
    // Refresh data every 2 minutes
    const interval = setInterval(fetchDashboardData, 120000);
    return () => clearInterval(interval);
  }, []);

  const handleViewMaintenanceDetails = () => {
    setShowMaintenanceModal(true);
  };

  const handleViewBrandingDetails = () => {
    setShowBrandingModal(true);
  };

  const handleCloseModals = () => {
    setShowMaintenanceModal(false);
    setShowBrandingModal(false);
  };

  if (loading && !dashboardData) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-center">
          <div className="text-red-600 text-lg mr-2">❌</div>
          <div>
            <h3 className="text-red-800 font-medium">Error Loading Dashboard</h3>
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        </div>
        <button 
          onClick={fetchDashboardData}
          className="mt-4 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg shadow-lg p-6 text-white">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold mb-2">RailSpark Dashboard</h1>
            <p className="text-blue-100">AI-Driven Train Induction Planning & Scheduling</p>
            <div className="flex items-center mt-4 space-x-4 text-sm">
              <span className="bg-blue-500 bg-opacity-50 px-3 py-1 rounded-full">
                🟢 System Online
              </span>
              <span className="bg-green-500 bg-opacity-50 px-3 py-1 rounded-full">
                {dashboardData?.summary?.active_trains || 0} Active Trains
              </span>
              <span className="bg-yellow-500 bg-opacity-50 px-3 py-1 rounded-full">
                Last updated: {new Date().toLocaleTimeString()}
              </span>
            </div>
          </div>
          <div className="text-right">
            <div className="text-4xl mb-2">🚆</div>
            <button 
              onClick={fetchDashboardData}
              className="bg-white bg-opacity-20 hover:bg-opacity-30 text-white px-4 py-2 rounded-lg transition-colors"
            >
              Refresh Data
            </button>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      {dashboardData && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                <span className="text-2xl">🚆</span>
              </div>
              <div>
                <div className="text-2xl font-bold text-gray-900">{dashboardData.summary.total_trains}</div>
                <div className="text-sm text-gray-600">Total Trains</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                <span className="text-2xl">✅</span>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-600">{dashboardData.summary.eligible_trains}</div>
                <div className="text-sm text-gray-600">Eligible for Service</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mr-3">
                <span className="text-2xl">⚡</span>
              </div>
              <div>
                <div className="text-2xl font-bold text-yellow-600">{dashboardData.today_plan.service_trains}</div>
                <div className="text-sm text-gray-600">In Service Today</div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-4">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mr-3">
                <span className="text-2xl">📊</span>
              </div>
              <div>
                <div className="text-2xl font-bold text-purple-600">{dashboardData.summary.utilization_rate}%</div>
                <div className="text-sm text-gray-600">Utilization Rate</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab Navigation */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8 px-6">
            {[
              { id: 'overview', label: 'Overview', icon: '📊' },
              { id: 'trains', label: 'Train Status', icon: '🚆' },
              { id: 'induction', label: 'Induction Plan', icon: '📋' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm whitespace-nowrap flex items-center ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span className="mr-2 text-lg">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Alerts Section */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <span className="text-yellow-600 text-lg mr-2">⚠️</span>
                    <h3 className="font-medium text-yellow-800">Maintenance Alerts</h3>
                  </div>
                  <p className="text-yellow-700 text-sm">
                    {dashboardData?.maintenance?.trains_need_maintenance || 0} trains require maintenance attention
                  </p>
                  <button 
                    onClick={handleViewMaintenanceDetails}
                    className="mt-2 text-yellow-600 hover:text-yellow-800 text-sm font-medium"
                  >
                    View Details →
                  </button>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <span className="text-blue-600 text-lg mr-2">📢</span>
                    <h3 className="font-medium text-blue-800">Branding Status</h3>
                  </div>
                  <p className="text-blue-700 text-sm">
                    {dashboardData?.branding?.contracts_need_exposure || 0} contracts need exposure attention
                  </p>
                  <button 
                    onClick={handleViewBrandingDetails}
                    className="mt-2 text-blue-600 hover:text-blue-800 text-sm font-medium"
                  >
                    View Details →
                  </button>
                </div>
              </div>

              {/* Today's Plan Summary */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="font-medium text-gray-900 mb-3">Today's Induction Plan</h3>
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <div className="text-2xl font-bold text-blue-600">{dashboardData?.today_plan?.service_trains || 0}</div>
                    <div className="text-sm text-gray-600">Service Trains</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-purple-600">{dashboardData?.today_plan?.standby_trains || 0}</div>
                    <div className="text-sm text-gray-600">Standby Trains</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-green-600">{dashboardData?.today_plan?.total_planned || 0}</div>
                    <div className="text-sm text-gray-600">Total Planned</div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'trains' && <TrainStatus />}
          {activeTab === 'induction' && <InductionPlan />}
        </div>
      </div>

      {/* Predictive Analytics */}
      {dashboardData && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Predictive Analytics</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 border border-gray-200 rounded-lg">
              <div className="text-3xl font-bold text-red-600 mb-2">
                {dashboardData.risk_assessment?.high_risk_trains || 0}
              </div>
              <div className="text-sm text-gray-600">High Risk Trains</div>
              <div className="text-xs text-red-500 mt-1">Needs Immediate Attention</div>
            </div>
            <div className="text-center p-4 border border-gray-200 rounded-lg">
              <div className="text-3xl font-bold text-yellow-600 mb-2">
                {dashboardData.maintenance?.open_job_cards || 0}
              </div>
              <div className="text-sm text-gray-600">Open Job Cards</div>
              <div className="text-xs text-yellow-500 mt-1">Pending Maintenance</div>
            </div>
            <div className="text-center p-4 border border-gray-200 rounded-lg">
              <div className="text-3xl font-bold text-green-600 mb-2">
                {dashboardData.branding?.contracts_need_exposure || 0}
              </div>
              <div className="text-sm text-gray-600">Contracts at Risk</div>
              <div className="text-xs text-green-500 mt-1">Branding Exposure</div>
            </div>
          </div>
        </div>
      )}

      {/* Maintenance Details Modal */}
      {showMaintenanceModal && (
        <MaintenanceAlerts 
          isOpen={showMaintenanceModal}
          onClose={handleCloseModals}
          maintenanceData={dashboardData?.maintenance}
        />
      )}

      {/* Branding Details Modal */}
      {showBrandingModal && (
        <BrandingStatus 
          isOpen={showBrandingModal}
          onClose={handleCloseModals}
          brandingData={dashboardData?.branding}
        />
      )}
    </div>
  );
};

export default Dashboard;