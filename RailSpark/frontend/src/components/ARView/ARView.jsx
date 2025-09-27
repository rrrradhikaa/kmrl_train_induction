import React, { useState, useRef, useEffect } from 'react';
import { useApi } from '../../hooks/useApi';

const ARView = () => {
  const [isArSupported, setIsArSupported] = useState(false);
  const [arStatus, setArStatus] = useState('idle'); // idle, loading, active, error
  const [selectedTrain, setSelectedTrain] = useState(null);
  const [trainData, setTrainData] = useState([]);
  const [overlayInfo, setOverlayInfo] = useState(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const { get, loading } = useApi();

  // Simulated AR data - in real app, this would come from computer vision
  const simulatedTrains = [
    { id: 1, number: 'KMRL-001', position: { x: 100, y: 150 }, status: 'active', mileage: 15200 },
    { id: 2, number: 'KMRL-002', position: { x: 250, y: 120 }, status: 'maintenance', mileage: 13800 },
    { id: 3, number: 'KMRL-003', position: { x: 400, y: 180 }, status: 'active', mileage: 16500 },
    { id: 4, number: 'KMRL-004', position: { x: 550, y: 90 }, status: 'cleaning', mileage: 14200 },
  ];

  useEffect(() => {
    checkArSupport();
    fetchTrainData();
  }, []);

  const checkArSupport = () => {
    // Check if browser supports basic AR features
    const supportsAr = 'xr' in navigator;
    setIsArSupported(supportsAr);
    
    if (!supportsAr) {
      setArStatus('error');
    }
  };

  const fetchTrainData = async () => {
    const data = await get('/dashboard/train-status');
    if (data) {
      setTrainData(data);
    } else {
      // Fallback to simulated data
      setTrainData(simulatedTrains);
    }
  };

  const startArExperience = async () => {
    setArStatus('loading');
    
    try {
      // Simulate AR initialization
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // In a real app, this would initialize WebXR or AR.js
      setArStatus('active');
      startSimulatedAr();
      
    } catch (error) {
      setArStatus('error');
      console.error('AR initialization failed:', error);
    }
  };

  const startSimulatedAr = () => {
    // Simulated AR experience since we can't run real AR in this environment
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    const drawArOverlay = () => {
      if (arStatus !== 'active') return;
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Draw simulated train markers
      simulatedTrains.forEach(train => {
        const isSelected = selectedTrain?.id === train.id;
        
        // Draw marker circle
        ctx.fillStyle = getStatusColor(train.status);
        ctx.beginPath();
        ctx.arc(train.position.x, train.position.y, 15, 0, 2 * Math.PI);
        ctx.fill();
        
        // Draw border if selected
        if (isSelected) {
          ctx.strokeStyle = '#3B82F6';
          ctx.lineWidth = 3;
          ctx.stroke();
        }
        
        // Draw train number
        ctx.fillStyle = 'white';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(train.number.substring(6), train.position.x, train.position.y + 4);
      });
      
      requestAnimationFrame(drawArOverlay);
    };
    
    drawArOverlay();
  };

  const getStatusColor = (status) => {
    const colors = {
      active: '#10B981', // green
      maintenance: '#F59E0B', // yellow
      cleaning: '#3B82F6', // blue
      standby: '#8B5CF6' // purple
    };
    return colors[status] || '#6B7280'; // gray
  };

  const handleCanvasClick = (e) => {
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    // Find clicked train
    const clickedTrain = simulatedTrains.find(train => {
      const distance = Math.sqrt(Math.pow(x - train.position.x, 2) + Math.pow(y - train.position.y, 2));
      return distance <= 15;
    });
    
    if (clickedTrain) {
      setSelectedTrain(clickedTrain);
      setOverlayInfo(clickedTrain);
      
      // Find additional data from trainData
      const fullData = trainData.find(t => t.train_number === clickedTrain.number);
      if (fullData) {
        setOverlayInfo({ ...clickedTrain, ...fullData });
      }
    } else {
      setSelectedTrain(null);
      setOverlayInfo(null);
    }
  };

  const stopArExperience = () => {
    setArStatus('idle');
    setSelectedTrain(null);
    setOverlayInfo(null);
  };

  if (loading) return <div className="flex justify-center items-center h-96">Loading AR view...</div>;

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Augmented Reality View</h2>
          <p className="text-gray-600">Visualize train data in physical space</p>
        </div>
        
        <div className="flex space-x-2">
          {arStatus === 'idle' && (
            <button
              onClick={startArExperience}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Start AR Experience
            </button>
          )}
          {arStatus === 'active' && (
            <button
              onClick={stopArExperience}
              className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
            >
              Stop AR
            </button>
          )}
          <button 
            onClick={fetchTrainData}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
          >
            Refresh Data
          </button>
        </div>
      </div>

      {/* AR Status Message */}
      {!isArSupported && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <div className="flex items-center">
            <div className="text-yellow-600 text-lg mr-2">⚠️</div>
            <div>
              <strong className="text-yellow-800">AR Not Supported</strong>
              <p className="text-yellow-700 text-sm">
                Your browser doesn't support AR features. Showing simulated experience.
              </p>
            </div>
          </div>
        </div>
      )}

      {arStatus === 'loading' && (
        <div className="flex flex-col items-center justify-center h-96 bg-gray-100 rounded-lg mb-6">
          <div className="text-6xl mb-4">📱</div>
          <div className="text-xl font-medium text-gray-700 mb-2">Initializing AR Experience</div>
          <div className="flex space-x-2">
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
          </div>
          <p className="text-gray-600 mt-4">Point your camera at the depot area...</p>
        </div>
      )}

      {/* AR Canvas */}
      {arStatus === 'active' && (
        <div className="relative mb-6">
          <div className="bg-black rounded-lg overflow-hidden">
            {/* Simulated camera feed placeholder */}
            <div 
              className="w-full h-96 bg-gradient-to-br from-gray-900 to-gray-700 relative"
              style={{ backgroundImage: 'url("data:image/svg+xml,%3Csvg width=\"100\" height=\"100\" viewBox=\"0 0 100 100\" xmlns=\"http://www.w3.org/2000/svg\"%3E%3Cpath d=\"M0 0h100v100H0z\" fill=\"%23333\"/%3E%3Cpath d=\"M20 20h60v60H20z\" fill=\"none\" stroke=\"%23666\" stroke-width=\"2\"/%3E%3C/svg%3E")' }}
            >
              <canvas
                ref={canvasRef}
                width={800}
                height={400}
                className="absolute inset-0 w-full h-full cursor-crosshair"
                onClick={handleCanvasClick}
              />
            </div>
          </div>
          
          {/* Instructions */}
          <div className="absolute top-4 left-4 bg-black bg-opacity-50 text-white p-2 rounded text-sm">
            👆 Click on train markers for details
          </div>
        </div>
      )}

      {/* Train Information Overlay */}
      {overlayInfo && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <h3 className="font-bold text-blue-900 text-lg mb-2">{overlayInfo.number} - Train Details</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="font-medium">Status:</span>
              <span className={`ml-2 px-2 py-1 rounded-full text-xs ${
                overlayInfo.status === 'active' ? 'bg-green-100 text-green-800' :
                overlayInfo.status === 'maintenance' ? 'bg-yellow-100 text-yellow-800' :
                'bg-blue-100 text-blue-800'
              }`}>
                {overlayInfo.status}
              </span>
            </div>
            <div>
              <span className="font-medium">Mileage:</span> {overlayInfo.mileage?.toLocaleString()} km
            </div>
            <div>
              <span className="font-medium">Last Maintenance:</span> 
              {overlayInfo.last_maintenance ? new Date(overlayInfo.last_maintenance).toLocaleDateString() : 'N/A'}
            </div>
            <div>
              <span className="font-medium">Eligibility:</span>
              <span className={`ml-2 px-2 py-1 rounded-full text-xs ${
                overlayInfo.eligibility === 'eligible' ? 'bg-green-100 text-green-800' :
                'bg-red-100 text-red-800'
              }`}>
                {overlayInfo.eligibility || 'Unknown'}
              </span>
            </div>
          </div>
          
          {overlayInfo.open_job_cards > 0 && (
            <div className="mt-2 text-red-600 text-sm">
              ⚠️ {overlayInfo.open_job_cards} open job card(s) - Maintenance needed
            </div>
          )}
        </div>
      )}

      {/* AR Features List */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gray-50 p-4 rounded-lg">
          <div className="text-3xl mb-2">🎯</div>
          <h3 className="font-medium text-gray-900 mb-1">Real-time Tracking</h3>
          <p className="text-sm text-gray-600">See train positions and status overlaid on camera view</p>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg">
          <div className="text-3xl mb-2">📊</div>
          <h3 className="font-medium text-gray-900 mb-1">Live Data Overlay</h3>
          <p className="text-sm text-gray-600">Access maintenance schedules and fitness status instantly</p>
        </div>
        <div className="bg-gray-50 p-4 rounded-lg">
          <div className="text-3xl mb-2">🔍</div>
          <h3 className="font-medium text-gray-900 mb-1">Quick Inspection</h3>
          <p className="text-sm text-gray-600">Identify trains needing immediate attention</p>
        </div>
      </div>

      {/* Demo Notice */}
      {arStatus === 'idle' && (
        <div className="mt-6 p-4 bg-purple-50 rounded-lg">
          <h3 className="font-medium text-purple-900 mb-2">Demo Mode</h3>
          <p className="text-sm text-purple-700">
            This is a simulated AR experience. In production, this would use your device's camera 
            and AR capabilities to overlay train information onto the real-world depot view.
          </p>
        </div>
      )}
    </div>
  );
};

export default ARView;