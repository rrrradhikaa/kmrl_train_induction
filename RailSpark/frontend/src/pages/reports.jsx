import React, { useState, useEffect } from 'react';
import { useApi } from '../hooks/useApi';
import {
  TrainStatusChart,
  FailurePredictionChart,
  InductionPlanChart,
  BrandingContractsChart,
  MaintenanceTrendsChart,
  UtilizationRateChart,
  KPICards,
  BrandingContractsChartEnhanced
} from '../components/Reports/reports';

const Reports = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [optimizationStats, setOptimizationStats] = useState(null);
  const [failurePredictions, setFailurePredictions] = useState([]);
  const [brandingContracts, setBrandingContracts] = useState([]);
  const [jobCards, setJobCards] = useState([]);
  const [trains, setTrains] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [warnings, setWarnings] = useState([]);
  const { get, loading: apiLoading, error: apiError } = useApi();

  // Generate mock predictions when real data is unavailable
  const generateMockPredictions = (trainsList) => {
    return trainsList.map(train => ({
      train_id: train.id,
      train_number: train.train_number,
      failure_probability: Math.random() * 0.3, // Lower risk for mock data
      risk_level: Math.random() > 0.8 ? 'high' : Math.random() > 0.5 ? 'medium' : 'low',
      predicted_failure_type: 'None',
      confidence: Math.random() * 0.5 + 0.5,
      recommendation: 'Regular maintenance scheduled',
      features: {}
    }));
  };

  // Generate mock optimization stats
  const generateMockStats = (trainsList, jobCardsList) => {
    const totalTrains = trainsList.length;
    const activeTrains = trainsList.filter(t => t.status === 'active').length;
    
    return {
      total_trains: totalTrains,
      active_trains: activeTrains,
      eligible_trains: Math.floor(activeTrains * 0.8),
      planned_service_trains: Math.floor(activeTrains * 0.6),
      planned_standby_trains: Math.floor(activeTrains * 0.2),
      planned_maintenance_trains: Math.floor(activeTrains * 0.2),
      utilization_rate: activeTrains > 0 ? 0.75 : 0
    };
  };

  // Process branding contracts data to handle API response structure
  const processBrandingContracts = (contracts) => {
    if (!contracts || !Array.isArray(contracts)) {
      return [];
    }

    return contracts.map(contract => ({
      id: contract.contract_id || contract.id,
      contract_id: contract.contract_id || contract.id,
      train_id: contract.train_id,
      is_active: contract.is_active !== undefined ? contract.is_active : true,
      exposure_hours_required: contract.exposure_hours_required || 0,
      exposure_hours_fulfilled: contract.exposure_hours_fulfilled || 0,
      start_date: contract.start_date,
      end_date: contract.end_date,
      status: contract.status || 'active'
    }));
  };

  // Fetch all report data with error handling
  const fetchReportData = async () => {
    try {
      setLoading(true);
      setWarnings([]);
      
      // Fetch basic data that should always be available
      const [trainsResponse, contractsResponse, jobCardsResponse] = await Promise.allSettled([
        get('/trains/'),
        get('/branding/'),
        get('/job-cards/')
      ]);

      const trainsData = trainsResponse.status === 'fulfilled' ? trainsResponse.value : [];
      const contractsData = contractsResponse.status === 'fulfilled' ? contractsResponse.value : [];
      const jobCardsData = jobCardsResponse.status === 'fulfilled' ? jobCardsResponse.value : [];

      setTrains(trainsData);
      setBrandingContracts(processBrandingContracts(contractsData));
      setJobCards(jobCardsData);

      // Try to fetch AI data, but use fallbacks if it fails
      try {
        const statsResponse = await get('/ai/optimization-stats');
        if (statsResponse) {
          setOptimizationStats(statsResponse);
        } else {
          throw new Error('No stats data returned');
        }
      } catch (statsError) {
        console.warn('Using mock optimization stats:', statsError.message);
        setOptimizationStats(generateMockStats(trainsData, jobCardsData));
        setWarnings(prev => [...prev, 'Using simulated optimization data (AI service unavailable)']);
      }

      try {
        const predictionsResponse = await get('/ai/failure-predictions');
        if (predictionsResponse && predictionsResponse.length > 0) {
          setFailurePredictions(predictionsResponse);
        } else {
          throw new Error('No prediction data returned');
        }
      } catch (predictionError) {
        console.warn('Using mock predictions:', predictionError.message);
        setFailurePredictions(generateMockPredictions(trainsData));
        setWarnings(prev => [...prev, 'Using simulated prediction data (ML model needs more training data)']);
      }

    } catch (err) {
      console.error('Error fetching report data:', err);
      setError(err.message || 'Failed to fetch report data');
      
      // Provide basic mock data even if everything fails
      const mockTrains = [{ id: 1, train_number: 'KMRL-001', status: 'active' }];
      const mockContracts = [
        {
          contract_id: 1,
          train_id: 1,
          is_active: true,
          exposure_hours_required: 160,
          exposure_hours_fulfilled: 120,
          start_date: '2024-01-01',
          end_date: '2024-12-31'
        },
        {
          contract_id: 2,
          train_id: 2,
          is_active: true,
          exposure_hours_required: 200,
          exposure_hours_fulfilled: 150,
          start_date: '2024-01-01',
          end_date: '2024-12-31'
        }
      ];
      
      setOptimizationStats(generateMockStats(mockTrains, []));
      setFailurePredictions(generateMockPredictions(mockTrains));
      setBrandingContracts(processBrandingContracts(mockContracts));
      setWarnings(prev => [...prev, 'Using demo data - real data unavailable']);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReportData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading reports...</p>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', name: 'Overview', icon: '📊' },
    { id: 'predictions', name: 'Predictive Analytics', icon: '🔮' },
    { id: 'maintenance', name: 'Maintenance', icon: '🔧' },
    { id: 'branding', name: 'Branding', icon: '📝' },
    { id: 'induction', name: 'Induction Plans', icon: '📅' }
  ];

  // Calculate branding-specific statistics
  const brandingStats = {
    totalContracts: brandingContracts.length,
    activeContracts: brandingContracts.filter(c => c.is_active).length,
    contractsNeedingExposure: brandingContracts.filter(c => {
      const fulfilled = c.exposure_hours_fulfilled || 0;
      const required = c.exposure_hours_required || 0;
      return c.is_active && fulfilled < required;
    }).length,
    totalExposureRequired: brandingContracts.reduce((sum, c) => sum + (c.exposure_hours_required || 0), 0),
    totalExposureFulfilled: brandingContracts.reduce((sum, c) => sum + (c.exposure_hours_fulfilled || 0), 0),
    overallProgress: brandingContracts.length > 0 ? 
      (brandingContracts.reduce((sum, c) => sum + (c.exposure_hours_fulfilled || 0), 0) / 
       brandingContracts.reduce((sum, c) => sum + (c.exposure_hours_required || 0), 0)) * 100 : 0
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <div className="space-y-6">
            {/* Warnings */}
            {warnings.length > 0 && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <div className="flex items-center">
                  <span className="text-yellow-600 text-lg mr-2">⚠️</span>
                  <div>
                    <h4 className="font-semibold text-yellow-800">Data Quality Notice</h4>
                    <ul className="text-yellow-700 text-sm mt-1 list-disc list-inside">
                      {warnings.map((warning, index) => (
                        <li key={index}>{warning}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            )}
            
            <KPICards 
              optimizationStats={optimizationStats}
              predictions={failurePredictions}
              contracts={brandingContracts}
            />
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <TrainStatusChart data={optimizationStats} />
              <UtilizationRateChart optimizationStats={optimizationStats} />
            </div>
            
            <div className="grid grid-cols-1 gap-6">
              <FailurePredictionChart predictions={failurePredictions} />
            </div>
          </div>
        );

      case 'predictions':
        return (
          <div className="space-y-6">
            {warnings.some(w => w.includes('prediction')) && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-center">
                  <span className="text-blue-600 text-lg mr-2">💡</span>
                  <div>
                    <p className="text-blue-800 text-sm">
                      <strong>Tip:</strong> The ML model will provide more accurate predictions as more maintenance data is collected.
                    </p>
                  </div>
                </div>
              </div>
            )}
            
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Failure Risk Analysis</h3>
              <FailurePredictionChart predictions={failurePredictions} />
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h4 className="text-lg font-semibold text-gray-800 mb-4">Risk Distribution</h4>
                <div className="space-y-3">
                  {['high', 'medium', 'low'].map(level => {
                    const count = failurePredictions.filter(p => p.risk_level === level).length;
                    const percentage = failurePredictions.length > 0 ? 
                      ((count / failurePredictions.length) * 100).toFixed(1) : 0;
                    
                    return (
                      <div key={level} className="flex justify-between items-center">
                        <span className="capitalize flex items-center">
                          <span 
                            className={`inline-block w-3 h-3 rounded-full mr-2 ${
                              level === 'high' ? 'bg-red-500' :
                              level === 'medium' ? 'bg-yellow-500' : 'bg-green-500'
                            }`}
                          />
                          {level} Risk
                        </span>
                        <span className="font-semibold">
                          {count} trains ({percentage}%)
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
              
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h4 className="text-lg font-semibold text-gray-800 mb-4">Recommendations</h4>
                <div className="space-y-2">
                  {failurePredictions
                    .filter(p => p.risk_level === 'high')
                    .slice(0, 3)
                    .map(pred => (
                      <div key={pred.train_id} className="text-sm p-2 bg-red-50 rounded">
                        <strong>Train {pred.train_number}:</strong> {pred.recommendation}
                      </div>
                    ))
                  }
                  {failurePredictions.filter(p => p.risk_level === 'high').length === 0 && (
                    <p className="text-gray-600 text-sm">No high-risk trains detected.</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        );

      case 'maintenance':
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <MaintenanceTrendsChart jobCards={jobCards} />
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Maintenance Summary</h3>
                <div className="space-y-4">
                  <div className="flex justify-between p-2 bg-gray-50 rounded">
                    <span>Total Jobs:</span>
                    <span className="font-semibold">{jobCards.length}</span>
                  </div>
                  <div className="flex justify-between p-2 bg-yellow-50 rounded">
                    <span>Open Jobs:</span>
                    <span className="font-semibold text-yellow-600">
                      {jobCards.filter(j => j.status === 'open').length}
                    </span>
                  </div>
                  <div className="flex justify-between p-2 bg-green-50 rounded">
                    <span>Closed Jobs:</span>
                    <span className="font-semibold text-green-600">
                      {jobCards.filter(j => j.status === 'closed').length}
                    </span>
                  </div>
                </div>
                
                {jobCards.length === 0 && (
                  <div className="mt-4 p-3 bg-blue-50 rounded text-sm text-blue-800">
                    <strong>Note:</strong> No maintenance job cards found. Create job cards to track maintenance activities.
                  </div>
                )}
              </div>
            </div>
          </div>
        );

      case 'branding':
        return (
          <div className="space-y-6">
            {/* Branding Overview Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Total Contracts</p>
                    <p className="text-2xl font-bold text-gray-900 mt-2">{brandingStats.totalContracts}</p>
                  </div>
                  <div className="bg-blue-500 rounded-full p-3">
                    <span className="text-2xl text-white">📝</span>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Active Contracts</p>
                    <p className="text-2xl font-bold text-gray-900 mt-2">{brandingStats.activeContracts}</p>
                  </div>
                  <div className="bg-green-500 rounded-full p-3">
                    <span className="text-2xl text-white">✅</span>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Need Exposure</p>
                    <p className="text-2xl font-bold text-gray-900 mt-2">{brandingStats.contractsNeedingExposure}</p>
                  </div>
                  <div className="bg-yellow-500 rounded-full p-3">
                    <span className="text-2xl text-white">⏰</span>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-lg p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Overall Progress</p>
                    <p className="text-2xl font-bold text-gray-900 mt-2">
                      {brandingStats.overallProgress.toFixed(1)}%
                    </p>
                  </div>
                  <div className="bg-purple-500 rounded-full p-3">
                    <span className="text-2xl text-white">📊</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Enhanced Branding Contracts Component */}
            <BrandingContractsChartEnhanced contracts={brandingContracts} />
            
            {/* Exposure Progress Details */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Exposure Progress Details</h3>
              <div className="space-y-4 max-h-80 overflow-y-auto">
                {brandingContracts
                  .filter(contract => contract.is_active)
                  .map(contract => {
                    const progress = contract.exposure_hours_required > 0 ? 
                      (contract.exposure_hours_fulfilled / contract.exposure_hours_required) * 100 : 0;
                    const hoursRemaining = contract.exposure_hours_required - contract.exposure_hours_fulfilled;
                    
                    return (
                      <div key={contract.contract_id} className="p-4 border rounded-lg">
                        <div className="flex justify-between items-center mb-2">
                          <span className="font-semibold">Contract CT-{contract.contract_id} (Train {contract.train_id})</span>
                          <span className={`px-2 py-1 text-xs rounded-full ${
                            progress >= 100 ? 'bg-green-100 text-green-800' :
                            progress >= 75 ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'
                          }`}>
                            {progress >= 100 ? 'Completed' : `${progress.toFixed(1)}%`}
                          </span>
                        </div>
                        
                        <div className="mb-2">
                          <div className="flex justify-between text-sm text-gray-600 mb-1">
                            <span>Progress</span>
                            <span>{contract.exposure_hours_fulfilled}h / {contract.exposure_hours_required}h</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full ${
                                progress >= 100 ? 'bg-green-500' :
                                progress >= 75 ? 'bg-yellow-500' : 'bg-red-500'
                              }`}
                              style={{ width: `${Math.min(progress, 100)}%` }}
                            ></div>
                          </div>
                        </div>
                        
                        {progress < 100 && (
                          <div className="text-sm text-gray-600">
                            <strong>Remaining:</strong> {hoursRemaining} hours needed
                          </div>
                        )}
                      </div>
                    );
                  })
                }
                
                {brandingContracts.filter(c => c.is_active).length === 0 && (
                  <div className="text-center py-8 text-gray-500">
                    <span className="text-4xl">📝</span>
                    <p className="mt-2">No active branding contracts found</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        );

      case 'induction':
        return (
          <div className="space-y-6">
            <InductionPlanChart optimizationStats={optimizationStats} />
            
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Induction Plan Details</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">
                    {optimizationStats?.planned_service_trains || 0}
                  </div>
                  <div className="text-sm text-blue-800">Service Trains</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">
                    {optimizationStats?.planned_standby_trains || 0}
                  </div>
                  <div className="text-sm text-green-800">Standby Trains</div>
                </div>
                <div className="text-center p-4 bg-orange-50 rounded-lg">
                  <div className="text-2xl font-bold text-orange-600">
                    {optimizationStats?.planned_maintenance_trains || 0}
                  </div>
                  <div className="text-sm text-orange-800">Maintenance Trains</div>
                </div>
              </div>
              
              {warnings.some(w => w.includes('optimization')) && (
                <div className="mt-4 p-3 bg-blue-50 rounded text-sm text-blue-800">
                  <strong>Note:</strong> AI optimization is currently using simulated data. Real optimization will be available when more operational data is collected.
                </div>
              )}
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Analytics & Reports</h1>
              <p className="text-gray-600 mt-2">Comprehensive insights into train operations and performance</p>
            </div>
            <button 
              onClick={fetchReportData}
              disabled={loading}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center disabled:bg-gray-400"
            >
              🔄 Refresh Data
            </button>
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8 overflow-x-auto">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 whitespace-nowrap ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
            <div className="text-red-600 text-4xl mb-2">⚠️</div>
            <h3 className="text-lg font-semibold text-red-800 mb-2">Error Loading Reports</h3>
            <p className="text-red-700 mb-4">{error}</p>
            <button 
              onClick={fetchReportData}
              className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
            >
              Try Again
            </button>
          </div>
        ) : (
          renderTabContent()
        )}
      </div>
    </div>
  );
};

export default Reports;