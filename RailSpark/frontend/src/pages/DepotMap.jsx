import React from 'react';
import DepotMap from '../components/DepotMap/DepotMap';

const DepotMapPage = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Depot Map</h1>
            <p className="text-gray-600">
              Interactive visualization of train positions, bay occupancy, and depot layout
            </p>
          </div>
          <div className="text-right">
            <div className="text-4xl mb-2">🗺️</div>
            <div className="text-sm text-gray-500">Real-time tracking</div>
          </div>
        </div>
      </div>

      {/* Depot Map Component */}
      <DepotMap />

      {/* Legend and Controls */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-medium text-gray-900 mb-3">Map Legend</h3>
          <div className="space-y-2 text-sm">
            <div className="flex items-center">
              <div className="w-4 h-4 bg-green-200 rounded mr-2"></div>
              <span>Service Bays - Ready for passenger service</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 bg-yellow-200 rounded mr-2"></div>
              <span>Maintenance Bays - Under repair/inspection</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 bg-blue-200 rounded mr-2"></div>
              <span>Cleaning Bays - Being cleaned/prepared</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 bg-gray-200 rounded mr-2"></div>
              <span>Stabling Bays - Parked/on standby</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-medium text-gray-900 mb-3">Quick Actions</h3>
          <div className="space-y-2">
            <button className="w-full text-left p-2 rounded bg-gray-50 hover:bg-gray-100 transition-colors text-sm">
              🔄 Optimize Stabling Arrangement
            </button>
            <button className="w-full text-left p-2 rounded bg-gray-50 hover:bg-gray-100 transition-colors text-sm">
              📋 Generate Shunting Schedule
            </button>
            <button className="w-full text-left p-2 rounded bg-gray-50 hover:bg-gray-100 transition-colors text-sm">
              ⚡ Check Bay Availability
            </button>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-medium text-gray-900 mb-3">Depot Statistics</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span>Total Bays:</span>
              <span className="font-medium">8</span>
            </div>
            <div className="flex justify-between">
              <span>Occupied Bays:</span>
              <span className="font-medium">6</span>
            </div>
            <div className="flex justify-between">
              <span>Available Capacity:</span>
              <span className="font-medium text-green-600">25%</span>
            </div>
            <div className="flex justify-between">
              <span>Shunting Required:</span>
              <span className="font-medium text-yellow-600">2 trains</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DepotMapPage;