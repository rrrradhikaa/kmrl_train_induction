import React from 'react';
import UploadCSV from '../components/DataInput/UploadCSV';
import ManualInput from '../components/DataInput/ManualInput';

const DataInput = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Data Input</h1>
            <p className="text-gray-600">
              Upload and manage train data through CSV files or manual entry
            </p>
          </div>
          <div className="text-right">
            <div className="text-4xl mb-2">📥</div>
            <div className="text-sm text-gray-500">Multiple input methods supported</div>
          </div>
        </div>
      </div>

      {/* CSV Upload Section */}
      <UploadCSV />

      {/* Manual Input Section */}
      <ManualInput />

      {/* Data Management Tips */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-medium text-blue-900 mb-3">Data Management Best Practices</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800">
          <div>
            <strong>📁 CSV Upload Tips:</strong>
            <ul className="mt-1 space-y-1">
              <li>• Use the provided templates for correct formatting</li>
              <li>• Ensure all required columns are present</li>
              <li>• Validate dates in YYYY-MM-DD format</li>
              <li>• Keep file sizes under 10MB for optimal performance</li>
            </ul>
          </div>
          <div>
            <strong>✍️ Manual Entry Tips:</strong>
            <ul className="mt-1 space-y-1">
              <li>• Verify train IDs exist before adding related records</li>
              <li>• Use consistent formatting for train numbers</li>
              <li>• Double-check date ranges for validity</li>
              <li>• Save frequently to avoid data loss</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="font-medium text-gray-900 mb-4">Recent Data Activity</h3>
        <div className="space-y-3">
          {[
            { action: 'CSV Upload', description: 'trains.csv', time: '2 minutes ago', status: 'success' },
            { action: 'Manual Entry', description: 'Added fitness certificate', time: '15 minutes ago', status: 'success' },
            { action: 'CSV Upload', description: 'job_cards.csv', time: '1 hour ago', status: 'warning' },
          ].map((activity, index) => (
            <div key={index} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
              <div className="flex items-center">
                <span className={`w-3 h-3 rounded-full mr-3 ${
                  activity.status === 'success' ? 'bg-green-500' : 
                  activity.status === 'warning' ? 'bg-yellow-500' : 'bg-red-500'
                }`}></span>
                <div>
                  <div className="font-medium text-gray-900">{activity.action}</div>
                  <div className="text-sm text-gray-600">{activity.description}</div>
                </div>
              </div>
              <div className="text-sm text-gray-500">{activity.time}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DataInput;