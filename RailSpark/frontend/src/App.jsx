import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from './components/Layout/Navbar';
import Sidebar from './components/Layout/Sidebar';
import Dashboard from './pages/Dashboard';
import DataInput from './pages/DataInput';
import TrainStatus from './pages/TrainStatus';
import InductionPlan from './pages/InductionPlan';
import Feedback from './pages/Feedback';
import Chatbot from './pages/Chatbot';
import DepotMap from './pages/DepotMap';
import ARView from './pages/ARView';
import Login from './pages/Login';
import BrandingPage from './pages/Branding';
import MaintenancePage from './pages/MaintenancePage'; 
import Reports from './pages/reports';
import './styles/index.css';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <AuthProvider>
      <Router>
        <div className="h-screen flex flex-col bg-gray-50">
          {/* Login page doesn't show layout */}
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="*"
              element={
                <>
                  <Navbar
                    onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
                    sidebarOpen={sidebarOpen}
                  />
                  <div className="flex flex-1 overflow-hidden">
                    <Sidebar
                      isOpen={sidebarOpen}
                      onClose={() => setSidebarOpen(false)}
                    />
                    <main className="flex-1 overflow-auto p-6">
                      <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/data-input" element={<DataInput />} />
                        <Route path="/train-status" element={<TrainStatus />} />
                        <Route path="/induction-planning" element={<InductionPlan />} />
                        <Route path="/maintenance" element={<MaintenancePage />} /> 
                        <Route path="/branding" element={<BrandingPage />} />
                        <Route path="/feedback" element={<Feedback />} />
                        <Route path="/chatbot" element={<Chatbot />} />
                        <Route path="/depot-map" element={<DepotMap />} />
                        <Route path="/ar-view" element={<ARView />} />
                        <Route path="/reports" element={<Reports />} />
                        <Route path="*" element={<NotFound />} />
                      </Routes>
                    </main>
                  </div>
                </>
              }
            />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

// 404 Not Found component
const NotFound = () => (
  <div className="flex items-center justify-center h-full">
    <div className="text-center">
      <div className="text-6xl mb-4">🔍</div>
      <h1 className="text-4xl font-bold text-gray-800 mb-2">Page Not Found</h1>
      <p className="text-gray-600 mb-6">
        The page you're looking for doesn't exist.
      </p>
      <a href="/" className="btn-primary">
        Go to Dashboard
      </a>
    </div>
  </div>
);

export default App;
