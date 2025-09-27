import React from 'react';

// Color palette for charts
const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];

// Simple Bar Chart Component
const SimpleBarChart = ({ data, width = '100%', height = 300 }) => {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-full" style={{ height }}>
        <p className="text-gray-500">No data available</p>
      </div>
    );
  }

  const maxValue = Math.max(...data.map(item => item.value));
  
  return (
    <div className="simple-bar-chart" style={{ width, height }}>
      {data.map((item, index) => (
        <div key={item.name} className="bar-item" style={{ height: '100%' }}>
          <div className="bar-container">
            <div 
              className="bar" 
              style={{ 
                height: `${(item.value / maxValue) * 100}%`,
                backgroundColor: COLORS[index % COLORS.length]
              }}
            >
              <span className="bar-value">{item.value}</span>
            </div>
            <div className="bar-label">{item.name}</div>
          </div>
        </div>
      ))}
    </div>
  );
};

// Simple Pie Chart Component
const SimplePieChart = ({ data, width = 300, height = 300 }) => {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-full" style={{ height }}>
        <p className="text-gray-500">No data available</p>
      </div>
    );
  }

  const total = data.reduce((sum, item) => sum + item.value, 0);
  
  if (total === 0) {
    return (
      <div className="flex items-center justify-center h-full" style={{ height }}>
        <p className="text-gray-500">No data available</p>
      </div>
    );
  }

  let currentAngle = 0;

  return (
    <div className="simple-pie-chart" style={{ width, height, position: 'relative' }}>
      <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
        <g transform={`translate(${width/2}, ${height/2})`}>
          {data.map((item, index) => {
            const percentage = (item.value / total) * 100;
            const angle = (percentage / 100) * 360;
            const largeArcFlag = angle > 180 ? 1 : 0;
            
            const x1 = Math.cos(currentAngle * Math.PI / 180) * 80;
            const y1 = Math.sin(currentAngle * Math.PI / 180) * 80;
            const x2 = Math.cos((currentAngle + angle) * Math.PI / 180) * 80;
            const y2 = Math.sin((currentAngle + angle) * Math.PI / 180) * 80;
            
            const pathData = [
              `M 0 0`,
              `L ${x1} ${y1}`,
              `A 80 80 0 ${largeArcFlag} 1 ${x2} ${y2}`,
              `Z`
            ].join(' ');
            
            const slice = (
              <path
                key={item.name}
                d={pathData}
                fill={COLORS[index % COLORS.length]}
                stroke="#fff"
                strokeWidth="2"
              />
            );
            
            currentAngle += angle;
            return slice;
          })}
        </g>
      </svg>
      
      {/* Legend */}
      <div className="pie-legend" style={{ position: 'absolute', right: 10, top: 10 }}>
        {data.map((item, index) => (
          <div key={item.name} className="legend-item" style={{ display: 'flex', alignItems: 'center', marginBottom: 5 }}>
            <div 
              className="legend-color" 
              style={{ 
                width: 12, 
                height: 12, 
                backgroundColor: COLORS[index % COLORS.length],
                marginRight: 8 
              }}
            />
            <span className="legend-text" style={{ fontSize: 12 }}>
              {item.name}: {item.value} ({(item.value / total * 100).toFixed(1)}%)
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

// Train Status Chart Component
export const TrainStatusChart = ({ data }) => {
  const statusData = [
    { name: 'Active', value: data?.active_trains || 0 },
    { name: 'Eligible', value: data?.eligible_trains || 0 },
    { name: 'In Maintenance', value: (data?.total_trains || 0) - (data?.active_trains || 0) }
  ];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Train Status Distribution</h3>
      <SimplePieChart data={statusData} />
    </div>
  );
};

// Failure Prediction Chart Component
export const FailurePredictionChart = ({ predictions }) => {
  const riskData = predictions?.map(pred => ({
    name: `Train ${pred.train_number}`,
    value: Math.round(pred.failure_probability * 100)
  })) || [];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Failure Risk Prediction</h3>
      <div style={{ height: 400, overflowX: 'auto' }}>
        <SimpleBarChart data={riskData} height={350} />
      </div>
    </div>
  );
};

// Induction Plan Chart Component
export const InductionPlanChart = ({ optimizationStats }) => {
  const planData = [
    { name: 'Service', value: optimizationStats?.planned_service_trains || 0 },
    { name: 'Standby', value: optimizationStats?.planned_standby_trains || 0 },
    { name: 'Maintenance', value: optimizationStats?.planned_maintenance_trains || 0 }
  ];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Induction Plan Distribution</h3>
      <SimpleBarChart data={planData} />
    </div>
  );
};

// Branding Contracts Chart Component - FIXED VERSION
export const BrandingContractsChart = ({ contracts }) => {
  // Handle empty or undefined contracts
  if (!contracts || !Array.isArray(contracts)) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Branding Contracts Status</h3>
        <div className="flex items-center justify-center h-64">
          <p className="text-gray-500">No branding contracts data available</p>
        </div>
      </div>
    );
  }

  // Process contract data with proper error handling
  const contractData = contracts.reduce((acc, contract) => {
    try {
      // Check different possible property names for active status
      const isActive = contract.is_active !== undefined ? contract.is_active :
                      contract.active !== undefined ? contract.active :
                      contract.status === 'active';
      
      const status = isActive ? 'Active' : 'Inactive';
      acc[status] = (acc[status] || 0) + 1;
    } catch (error) {
      console.error('Error processing contract:', contract, error);
    }
    return acc;
  }, {Active: 0, Inactive: 0});

  const chartData = Object.entries(contractData).map(([name, value]) => ({
    name,
    value
  }));

  // If no data after processing, show message
  if (chartData.length === 0 || chartData.reduce((sum, item) => sum + item.value, 0) === 0) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Branding Contracts Status</h3>
        <div className="flex items-center justify-center h-64">
          <p className="text-gray-500">No active or inactive contracts found</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Branding Contracts Status</h3>
      <SimplePieChart data={chartData} />
      
      {/* Additional contract statistics */}
      <div className="mt-4 grid grid-cols-2 gap-4">
        <div className="text-center p-3 bg-blue-50 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">
            {contracts.filter(contract => {
              const isActive = contract.is_active !== undefined ? contract.is_active :
                             contract.active !== undefined ? contract.active :
                             contract.status === 'active';
              return isActive;
            }).length}
          </div>
          <div className="text-sm text-blue-800">Active Contracts</div>
        </div>
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-gray-600">
            {contracts.filter(contract => {
              const isActive = contract.is_active !== undefined ? contract.is_active :
                             contract.active !== undefined ? contract.active :
                             contract.status === 'active';
              return !isActive;
            }).length}
          </div>
          <div className="text-sm text-gray-800">Inactive Contracts</div>
        </div>
      </div>
    </div>
  );
};

// Branding Contracts Table View
export const BrandingContractsTable = ({ contracts }) => {
  if (!contracts || !Array.isArray(contracts) || contracts.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Branding Contracts</h3>
        <div className="flex items-center justify-center h-32">
          <p className="text-gray-500">No branding contracts available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Branding Contracts Details</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Contract ID
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Train
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
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {contracts.map((contract, index) => {
              const isActive = contract.is_active !== undefined ? contract.is_active :
                             contract.active !== undefined ? contract.active :
                             contract.status === 'active';
              
              const fulfilled = contract.exposure_hours_fulfilled || 0;
              const required = contract.exposure_hours_required || 0;
              const progress = required > 0 ? (fulfilled / required) * 100 : 0;

              return (
                <tr key={contract.id || contract.contract_id || index}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {contract.id || contract.contract_id || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    Train {contract.train_id || 'N/A'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      isActive 
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      {isActive ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {fulfilled}/{required} hrs
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full ${
                          progress >= 100 ? 'bg-green-500' :
                          progress >= 75 ? 'bg-yellow-500' : 'bg-red-500'
                        }`}
                        style={{ width: `${Math.min(progress, 100)}%` }}
                      ></div>
                    </div>
                    <span className="text-xs text-gray-500">{progress.toFixed(1)}%</span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

// Enhanced Branding Contracts Chart with multiple views
export const BrandingContractsChartEnhanced = ({ contracts }) => {
  const [view, setView] = React.useState('chart'); // 'chart' or 'table'

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-800">Branding Contracts</h3>
        <div className="flex space-x-2">
          <button
            onClick={() => setView('chart')}
            className={`px-3 py-1 text-sm rounded ${
              view === 'chart' 
                ? 'bg-blue-500 text-white' 
                : 'bg-gray-200 text-gray-700'
            }`}
          >
            Chart View
          </button>
          <button
            onClick={() => setView('table')}
            className={`px-3 py-1 text-sm rounded ${
              view === 'table' 
                ? 'bg-blue-500 text-white' 
                : 'bg-gray-200 text-gray-700'
            }`}
          >
            Table View
          </button>
        </div>
      </div>

      {view === 'chart' ? (
        <BrandingContractsChart contracts={contracts} />
      ) : (
        <BrandingContractsTable contracts={contracts} />
      )}
    </div>
  );
};

// Maintenance Trends Chart Component
export const MaintenanceTrendsChart = ({ jobCards }) => {
  const monthlyData = jobCards?.reduce((acc, job) => {
    const month = new Date(job.created_at).toLocaleString('default', { month: 'short' });
    acc[month] = (acc[month] || 0) + 1;
    return acc;
  }, {});

  const trendData = Object.entries(monthlyData || {}).map(([name, value]) => ({
    name,
    value
  }));

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Maintenance Jobs Trend</h3>
      <SimpleBarChart data={trendData} />
    </div>
  );
};

// Utilization Rate Chart Component
export const UtilizationRateChart = ({ optimizationStats }) => {
  const utilizationData = [
    { 
      name: 'Utilization Rate', 
      value: optimizationStats?.utilization_rate ? 
        Math.round(optimizationStats.utilization_rate * 100) : 0 
    }
  ];

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Train Utilization Rate</h3>
      <div className="utilization-chart">
        <div 
          className="utilization-bar" 
          style={{ 
            width: `${utilizationData[0].value}%`,
            backgroundColor: utilizationData[0].value > 80 ? '#10B981' : 
                           utilizationData[0].value > 60 ? '#F59E0B' : '#EF4444'
          }}
        >
          <span className="utilization-text">{utilizationData[0].value}%</span>
        </div>
      </div>
      <div className="utilization-labels mt-2 flex justify-between text-sm text-gray-600">
        <span>0%</span>
        <span>50%</span>
        <span>100%</span>
      </div>
    </div>
  );
};

// KPI Cards Component
export const KPICards = ({ optimizationStats, predictions, contracts }) => {
  const highRiskTrains = predictions?.filter(p => p.risk_level === 'high').length || 0;
  
  // Count active contracts safely
  const activeContracts = contracts?.filter(contract => {
    const isActive = contract.is_active !== undefined ? contract.is_active :
                    contract.active !== undefined ? contract.active :
                    contract.status === 'active';
    return isActive;
  }).length || 0;

  // Count contracts needing exposure safely
  const contractsNeedingExposure = contracts?.filter(contract => {
    const fulfilled = contract.exposure_hours_fulfilled || 0;
    const required = contract.exposure_hours_required || 0;
    return fulfilled < required;
  }).length || 0;

  const kpis = [
    {
      title: 'Total Trains',
      value: optimizationStats?.total_trains || 0,
      color: 'bg-blue-500',
      icon: '🚆'
    },
    {
      title: 'Active Trains',
      value: optimizationStats?.active_trains || 0,
      color: 'bg-green-500',
      icon: '✅'
    },
    {
      title: 'High Risk Trains',
      value: highRiskTrains,
      color: 'bg-red-500',
      icon: '⚠️'
    },
    {
      title: 'Active Contracts',
      value: activeContracts,
      color: 'bg-purple-500',
      icon: '📝'
    },
    {
      title: 'Utilization Rate',
      value: optimizationStats?.utilization_rate ? 
        `${(optimizationStats.utilization_rate * 100).toFixed(1)}%` : '0%',
      color: 'bg-orange-500',
      icon: '📊'
    },
    {
      title: 'Contracts Need Exposure',
      value: contractsNeedingExposure,
      color: 'bg-yellow-500',
      icon: '⏰'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      {kpis.map((kpi, index) => (
        <div key={index} className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">{kpi.title}</p>
              <p className="text-2xl font-bold text-gray-900 mt-2">{kpi.value}</p>
            </div>
            <div className={`${kpi.color} rounded-full p-3`}>
              <span className="text-2xl">{kpi.icon}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

// Add CSS styles
const chartStyles = `
.simple-bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 300px;
  padding: 20px 0;
  gap: 10px;
}

.bar-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.bar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  width: 100%;
}

.bar {
  width: 80%;
  min-height: 20px;
  border-radius: 4px 4px 0 0;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  transition: height 0.3s ease;
  position: relative;
}

.bar-value {
  color: white;
  font-weight: bold;
  font-size: 12px;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
  margin-bottom: 5px;
}

.bar-label {
  margin-top: 8px;
  font-size: 12px;
  text-align: center;
  font-weight: 500;
}

.utilization-chart {
  width: 100%;
  height: 40px;
  background-color: #f3f4f6;
  border-radius: 20px;
  overflow: hidden;
  position: relative;
}

.utilization-bar {
  height: 100%;
  border-radius: 20px;
  transition: width 0.5s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 60px;
}

.utilization-text {
  color: white;
  font-weight: bold;
  font-size: 14px;
}

.pie-legend {
  background: white;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border: 1px solid #e5e7eb;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.legend-color {
  width: 12px;
  height: 12px;
  margin-right: 8px;
  border-radius: 2px;
}

.legend-text {
  font-size: 12px;
  color: #374151;
}
`;

// Inject styles only once
if (typeof document !== 'undefined') {
  if (!document.querySelector('style[data-reports-charts]')) {
    const styleSheet = document.createElement('style');
    styleSheet.setAttribute('data-reports-charts', 'true');
    styleSheet.innerText = chartStyles;
    document.head.appendChild(styleSheet);
  }
}

// Export all components
export default {
  TrainStatusChart,
  FailurePredictionChart,
  InductionPlanChart,
  BrandingContractsChart,
  BrandingContractsTable,
  BrandingContractsChartEnhanced,
  MaintenanceTrendsChart,
  UtilizationRateChart,
  KPICards
};