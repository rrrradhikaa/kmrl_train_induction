import React from 'react';
import ARView from '../components/ARView/ARView';

const ARViewPage = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Augmented Reality View</h1>
            <p className="text-gray-600">
              Experience train data overlaid on real-world depot view using AR technology
            </p>
          </div>
          <div className="text-right">
            <div className="text-4xl mb-2">👓</div>
            <div className="text-sm text-gray-500">Advanced visualization</div>
          </div>
        </div>
      </div>

      {/* AR View Component */}
      <ARView />

      {/* AR Features */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-medium text-gray-900 mb-3">AR Capabilities</h3>
          <div className="space-y-3 text-sm text-gray-700">
            <div className="flex items-center">
              <span className="text-green-600 text-lg mr-2">✅</span>
              <span>Real-time train tracking and identification</span>
            </div>
            <div className="flex items-center">
              <span className="text-green-600 text-lg mr-2">✅</span>
              <span>Maintenance status overlay</span>
            </div>
            <div className="flex items-center">
              <span className="text-green-600 text-lg mr-2">✅</span>
              <span>Fitness certificate status display</span>
            </div>
            <div className="flex items-center">
              <span className="text-green-600 text-lg mr-2">✅</span>
              <span>Branding contract information</span>
            </div>
            <div className="flex items-center">
              <span className="text-blue-600 text-lg mr-2">🔜</span>
              <span>Interactive maintenance scheduling (Coming Soon)</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="font-medium text-gray-900 mb-3">Usage Instructions</h3>
          <div className="space-y-2 text-sm text-gray-700">
            <div className="bg-blue-50 p-3 rounded-lg">
              <strong>Step 1:</strong> Point your device camera at the depot area
            </div>
            <div className="bg-green-50 p-3 rounded-lg">
              <strong>Step 2:</strong> Wait for train recognition and data overlay
            </div>
            <div className="bg-yellow-50 p-3 rounded-lg">
              <strong>Step 3:</strong> Tap on train markers for detailed information
            </div>
            <div className="bg-purple-50 p-3 rounded-lg">
              <strong>Step 4:</strong> Use voice commands or on-screen controls
            </div>
          </div>
        </div>
      </div>

      {/* Technical Requirements */}
      <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-lg p-6">
        <h3 className="font-medium text-purple-900 mb-3">Technical Requirements</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-purple-800">
          <div>
            <strong>📱 Device Requirements:</strong>
            <ul className="mt-1 space-y-1">
              <li>• iOS 12+ or Android 8+</li>
              <li>• ARCore/ARKit compatible device</li>
              <li>• Rear-facing camera</li>
              <li>• Gyroscope and accelerometer</li>
            </ul>
          </div>
          <div>
            <strong>🌐 Network Requirements:</strong>
            <ul className="mt-1 space-y-1">
              <li>• Stable internet connection</li>
              <li>• GPS/Location services enabled</li>
              <li>• Camera permissions granted</li>
              <li>• WebXR support enabled</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ARViewPage;