import React, { useState } from 'react';
import TrainStatus from '../components/Dashboard/TrainStatus';

const TrainStatusPage = () => {
  const [actionMessage, setActionMessage] = useState('');
  const [isLoading, setIsLoading] = useState({
    checkAll: false,
    generateReport: false,
    showActions: false
  });

  // Function to handle "Check All Trains" button
  const handleCheckAllTrains = async () => {
    setIsLoading(prev => ({ ...prev, checkAll: true }));
    setActionMessage('Running comprehensive fitness checks on all trains...');
    
    // Simulate API call or processing
    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // In a real app, you would call an API here
      // const result = await api.checkAllTrains();
      
      setActionMessage('✅ Fitness checks completed successfully! All trains have been evaluated.');
    } catch (error) {
      setActionMessage('❌ Error running fitness checks. Please try again.');
    } finally {
      setIsLoading(prev => ({ ...prev, checkAll: false }));
    }
  };

  // Function to handle "Generate Report" button
  const handleGenerateReport = async () => {
    setIsLoading(prev => ({ ...prev, generateReport: true }));
    setActionMessage('Generating maintenance status report...');
    
    try {
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Simulate report generation
      const reportData = {
        timestamp: new Date().toLocaleString(),
        totalTrains: 24,
        operational: 20,
        maintenance: 3,
        outOfService: 1
      };
      
      setActionMessage(`📊 Report generated successfully! ${reportData.operational} trains operational, ${reportData.maintenance} under maintenance.`);
      
      // In a real app, you might download the report or show it in a modal
      console.log('Generated Report:', reportData);
      
    } catch (error) {
      setActionMessage('❌ Error generating report. Please try again.');
    } finally {
      setIsLoading(prev => ({ ...prev, generateReport: false }));
    }
  };

  // Function to handle "Show Actions" button
  const handleShowActions = () => {
    setIsLoading(prev => ({ ...prev, showActions: true }));
    setActionMessage('Loading quick actions menu...');
    
    // Simulate loading actions
    setTimeout(() => {
      // In a real app, this would open a modal or dropdown with actions
      const actions = [
        'Bulk maintenance scheduling',
        'Update train statuses',
        'Export train data',
        'Send notifications'
      ];
      
      setActionMessage(`🚀 Quick actions loaded: ${actions.join(', ')}`);
      setIsLoading(prev => ({ ...prev, showActions: false }));
      
      // You could also set state to show a modal with these actions
      // setShowActionsModal(true);
    }, 1000);
  };

  // Clear message after 5 seconds
  React.useEffect(() => {
    if (actionMessage) {
      const timer = setTimeout(() => {
        setActionMessage('');
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [actionMessage]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Train Status</h1>
            <p className="text-gray-600">
              Real-time status, eligibility, and maintenance information for all trains
            </p>
          </div>
          <div className="text-right">
            <div className="text-4xl mb-2">🚆</div>
            <div className="text-sm text-gray-500">Live status updates</div>
          </div>
        </div>
      </div>

      {/* Action Message */}
      {actionMessage && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <div className="text-blue-400">💡</div>
            </div>
            <div className="ml-3">
              <p className="text-sm text-blue-700">{actionMessage}</p>
            </div>
            <button
              onClick={() => setActionMessage('')}
              className="ml-auto text-blue-400 hover:text-blue-600"
            >
              ×
            </button>
          </div>
        </div>
      )}

      {/* Train Status Component */}
      <TrainStatus />

    </div>
  );
};

export default TrainStatusPage;