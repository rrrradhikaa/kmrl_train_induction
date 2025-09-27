import React, { useState, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';

const DepotMap = () => {
  const [depotLayout, setDepotLayout] = useState([]);
  const [selectedBay, setSelectedBay] = useState(null);
  const [trainPositions, setTrainPositions] = useState([]);
  const [viewMode, setViewMode] = useState('physical'); // physical or logical
  const { get, loading, error } = useApi();

  // Sample depot layout - in real app, this would come from backend
  const physicalLayout = [
    { id: 'bay-1', type: 'service', position: { x: 50, y: 50 }, capacity: 2, trains: [] },
    { id: 'bay-2', type: 'service', position: { x: 150, y: 50 }, capacity: 2, trains: [] },
    { id: 'bay-3', type: 'maintenance', position: { x: 250, y: 50 }, capacity: 1, trains: [] },
    { id: 'bay-4', type: 'cleaning', position: { x: 350, y: 50 }, capacity: 1, trains: [] },
    { id: 'bay-5', type: 'stabling', position: { x: 50, y: 150 }, capacity: 3, trains: [] },
    { id: 'bay-6', type: 'stabling', position: { x: 150, y: 150 }, capacity: 3, trains: [] },
    { id: 'bay-7', type: 'inspection', position: { x: 250, y: 150 }, capacity: 1, trains: [] },
    { id: 'bay-8', type: 'service', position: { x: 350, y: 150 }, capacity: 2, trains: [] },
  ];

  const logicalLayout = [
    { id: 'service-zone', type: 'zone', name: 'Service Ready', position: { x: 100, y: 80 }, bays: ['bay-1', 'bay-2', 'bay-8'] },
    { id: 'maintenance-zone', type: 'zone', name: 'Maintenance', position: { x: 300, y: 80 }, bays: ['bay-3', 'bay-7'] },
    { id: 'prep-zone', type: 'zone', name: 'Preparation', position: { x: 100, y: 180 }, bays: ['bay-4', 'bay-5', 'bay-6'] },
  ];

  useEffect(() => {
    fetchDepotData();
    // Simulate real-time updates
    const interval = setInterval(fetchDepotData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchDepotData = async () => {
    // Fetch current train positions from backend
    const stablingData = await get('/stabling/');
    if (stablingData) {
      setTrainPositions(stablingData);
      updateBayOccupancy(stablingData);
    }
  };

  const updateBayOccupancy = (stablingData) => {
    const updatedLayout = physicalLayout.map(bay => ({
      ...bay,
      trains: stablingData.filter(train => train.bay_position === bay.id)
    }));
    setDepotLayout(updatedLayout);
  };

  const getBayColor = (bayType) => {
    const colors = {
      service: 'bg-green-200 border-green-400',
      maintenance: 'bg-yellow-200 border-yellow-400',
      cleaning: 'bg-blue-200 border-blue-400',
      stabling: 'bg-gray-200 border-gray-400',
      inspection: 'bg-orange-200 border-orange-400',
      zone: 'bg-purple-100 border-purple-300'
    };
    return colors[bayType] || 'bg-gray-200 border-gray-400';
  };

  const getTrainStatusColor = (trainStatus) => {
    const colors = {
      active: 'bg-green-500',
      under_maintenance: 'bg-yellow-500',
      standby: 'bg-blue-500',
      cleaning: 'bg-purple-500'
    };
    return colors[trainStatus] || 'bg-gray-500';
  };

  const renderPhysicalView = () => (
    <div className="relative w-full h-96 bg-gray-100 rounded-lg border-2 border-gray-300">
      {/* Track Lines */}
      <div className="absolute inset-0">
        {/* Main track lines */}
        <div className="absolute top-20 left-0 right-0 h-1 bg-gray-400"></div>
        <div className="absolute top-40 left-0 right-0 h-1 bg-gray-400"></div>
        <div className="absolute top-60 left-0 right-0 h-1 bg-gray-400"></div>
        
        {/* Vertical connectors */}
        <div className="absolute left-20 top-0 bottom-0 w-1 bg-gray-400"></div>
        <div className="absolute left-40 top-0 bottom-0 w-1 bg-gray-400"></div>
        <div className="absolute right-20 top-0 bottom-0 w-1 bg-gray-400"></div>
      </div>

      {/* Bays */}
      {depotLayout.map((bay) => (
        <div
          key={bay.id}
          className={`absolute border-2 rounded-lg cursor-pointer transition-all hover:scale-105 ${
            getBayColor(bay.type)
          } ${selectedBay?.id === bay.id ? 'ring-4 ring-blue-400' : ''}`}
          style={{
            left: `${bay.position.x}px`,
            top: `${bay.position.y}px`,
            width: '80px',
            height: '60px'
          }}
          onClick={() => setSelectedBay(bay)}
        >
          <div className="p-1 text-xs">
            <div className="font-medium">{bay.id.toUpperCase()}</div>
            <div className="text-gray-600 capitalize">{bay.type}</div>
            <div className="flex justify-center mt-1">
              {bay.trains.slice(0, 3).map((train, index) => (
                <div
                  key={index}
                  className={`w-3 h-3 rounded-full mx-1 ${getTrainStatusColor(train.status)}`}
                  title={`Train ${train.train_id}`}
                ></div>
              ))}
              {bay.trains.length > 3 && (
                <div className="text-xs text-gray-500">+{bay.trains.length - 3}</div>
              )}
            </div>
          </div>
        </div>
      ))}

      {/* Legend */}
      <div className="absolute bottom-2 left-2 bg-white p-2 rounded-lg shadow-md text-xs">
        <div className="font-medium mb-1">Legend</div>
        <div className="flex flex-wrap gap-2">
          <div className="flex items-center"><div className="w-3 h-3 bg-green-200 mr-1"></div>Service</div>
          <div className="flex items-center"><div className="w-3 h-3 bg-yellow-200 mr-1"></div>Maintenance</div>
          <div className="flex items-center"><div className="w-3 h-3 bg-blue-200 mr-1"></div>Cleaning</div>
          <div className="flex items-center"><div className="w-3 h-3 bg-gray-200 mr-1"></div>Stabling</div>
        </div>
      </div>
    </div>
  );

  const renderLogicalView = () => (
    <div className="relative w-full h-96 bg-gray-50 rounded-lg border-2 border-gray-300">
      {logicalLayout.map((zone) => (
        <div
          key={zone.id}
          className="absolute border-2 border-dashed rounded-lg bg-opacity-50 cursor-pointer"
          style={{
            left: `${zone.position.x}px`,
            top: `${zone.position.y}px`,
            width: '200px',
            height: '120px',
            backgroundColor: getBayColor(zone.type).split(' ')[0].replace('bg-', 'bg-')
          }}
        >
          <div className="p-3">
            <div className="font-medium text-lg">{zone.name}</div>
            <div className="text-sm text-gray-600 mt-1">
              Contains {zone.bays.length} bays
            </div>
            <div className="mt-2 text-xs">
              {zone.bays.map(bayId => {
                const bay = depotLayout.find(b => b.id === bayId);
                return bay ? (
                  <div key={bayId} className="flex justify-between">
                    <span>{bayId.toUpperCase()}</span>
                    <span>{bay.trains.length}/{bay.capacity}</span>
                  </div>
                ) : null;
              })}
            </div>
          </div>
        </div>
      ))}

      {/* Connection lines would be drawn here in a more advanced version */}
    </div>
  );

  if (loading) return <div className="flex justify-center items-center h-96">Loading depot map...</div>;
  if (error) return <div className="text-red-600">Error loading depot map: {error}</div>;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">KMRL Depot Map</h2>
          <p className="text-gray-600">Real-time train positions and bay occupancy</p>
        </div>
        
        <div className="flex space-x-2">
          <button
            onClick={() => setViewMode('physical')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              viewMode === 'physical' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Physical View
          </button>
          <button
            onClick={() => setViewMode('logical')}
            className={`px-4 py-2 rounded-lg transition-colors ${
              viewMode === 'logical' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Logical View
          </button>
          <button 
            onClick={fetchDepotData}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
          >
            Refresh
          </button>
        </div>
      </div>

      {/* Map Container */}
      <div className="mb-6">
        {viewMode === 'physical' ? renderPhysicalView() : renderLogicalView()}
      </div>

      {/* Selected Bay Details */}
      {selectedBay && (
        <div className="mt-6 p-4 bg-blue-50 rounded-lg">
          <h3 className="font-medium text-blue-900 mb-2">
            {selectedBay.id.toUpperCase()} - {selectedBay.type.charAt(0).toUpperCase() + selectedBay.type.slice(1)} Bay
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="font-medium">Capacity:</span> {selectedBay.capacity} trains
            </div>
            <div>
              <span className="font-medium">Occupied:</span> {selectedBay.trains.length} trains
            </div>
            <div>
              <span className="font-medium">Available:</span> {selectedBay.capacity - selectedBay.trains.length} spots
            </div>
            <div>
              <span className="font-medium">Utilization:</span> {((selectedBay.trains.length / selectedBay.capacity) * 100).toFixed(1)}%
            </div>
          </div>
          
          {selectedBay.trains.length > 0 && (
            <div className="mt-3">
              <h4 className="font-medium text-blue-800 mb-1">Current Trains:</h4>
              <div className="flex flex-wrap gap-2">
                {selectedBay.trains.map(train => (
                  <span key={train.id} className="bg-white px-2 py-1 rounded text-xs border">
                    Train {train.train_id} ({train.status})
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Statistics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
        <div className="bg-green-50 p-3 rounded-lg text-center">
          <div className="text-2xl font-bold text-green-600">
            {depotLayout.filter(b => b.type === 'service').reduce((sum, b) => sum + b.trains.length, 0)}
          </div>
          <div className="text-sm text-green-800">Service Ready</div>
        </div>
        <div className="bg-yellow-50 p-3 rounded-lg text-center">
          <div className="text-2xl font-bold text-yellow-600">
            {depotLayout.filter(b => b.type === 'maintenance').reduce((sum, b) => sum + b.trains.length, 0)}
          </div>
          <div className="text-sm text-yellow-800">In Maintenance</div>
        </div>
        <div className="bg-blue-50 p-3 rounded-lg text-center">
          <div className="text-2xl font-bold text-blue-600">
            {depotLayout.filter(b => b.type === 'cleaning').reduce((sum, b) => sum + b.trains.length, 0)}
          </div>
          <div className="text-sm text-blue-800">Being Cleaned</div>
        </div>
        <div className="bg-gray-50 p-3 rounded-lg text-center">
          <div className="text-2xl font-bold text-gray-600">
            {depotLayout.reduce((sum, b) => sum + b.trains.length, 0)}
          </div>
          <div className="text-sm text-gray-800">Total in Depot</div>
        </div>
      </div>
    </div>
  );
};

export default DepotMap;