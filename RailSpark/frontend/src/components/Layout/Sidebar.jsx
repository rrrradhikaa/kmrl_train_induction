import React, { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useApi } from '../../hooks/useApi';

const Sidebar = ({ isOpen, onClose }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { get, post } = useApi();
  const [summaryData, setSummaryData] = useState({
    activeTrains: 0,
    scheduledTrains: 0,
    maintenanceTrains: 0,
    brandedTrains: 0
  });
  const [loading, setLoading] = useState(false);

  // Prevent body scroll when sidebar is open on mobile
  useEffect(() => {
    if (isOpen) {
      document.body.classList.add('no-scroll');
    } else {
      document.body.classList.remove('no-scroll');
    }

    return () => {
      document.body.classList.remove('no-scroll');
    };
  }, [isOpen]);

  // Close sidebar when route changes (mobile)
  useEffect(() => {
    if (isOpen) {
      onClose();
    }
  }, [location.pathname]);

  // Fetch summary data
  const fetchSummaryData = async () => {
    try {
      setLoading(true);
      
      // Fetch all necessary data in parallel
      const [trainsResponse, inductionResponse, jobCardsResponse, brandingResponse] = await Promise.allSettled([
        get('/trains/'),
        get('/induction/today'),
        get('/job-cards/open'),
        get('/branding/active')
      ]);

      const trains = trainsResponse.status === 'fulfilled' ? trainsResponse.value : [];
      const todaysPlan = inductionResponse.status === 'fulfilled' ? inductionResponse.value : [];
      const openJobs = jobCardsResponse.status === 'fulfilled' ? jobCardsResponse.value : [];
      const activeContracts = brandingResponse.status === 'fulfilled' ? brandingResponse.value : [];

      // Calculate summary data
      const activeTrains = trains.filter(train => train.status === 'active').length;
      const scheduledTrains = todaysPlan.length;
      const maintenanceTrains = openJobs.length;
      const brandedTrains = activeContracts.length;

      setSummaryData({
        activeTrains,
        scheduledTrains,
        maintenanceTrains,
        brandedTrains
      });

    } catch (error) {
      console.error('Error fetching summary data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSummaryData();
    
    // Refresh data every 5 minutes
    const interval = setInterval(fetchSummaryData, 300000);
    return () => clearInterval(interval);
  }, []);

  // Quick action handlers
  const handleQuickAction = async (action) => {
    try {
      switch (action) {
        case "generate_plan":
          await generateTodaysPlan();
          break;
        case "check_alerts":
          checkMaintenanceAlerts();
          break;
        case "view_report":
          viewPerformanceReport();
          break;
        default:
          break;
      }
    } catch (error) {
      console.error(`Error in quick action ${action}:`, error);
    }
    
    // Close sidebar on mobile after action
    if (isOpen) onClose();
  };

  // Generate today's induction plan
  const generateTodaysPlan = async () => {
    try {
      const response = await post('/ai/generate-plan', {
        plan_date: new Date().toISOString().split('T')[0],
        constraints: {
          max_service_trains: 10
        }
      });
      
      if (response) {
        // Navigate to induction planning page with the generated plan
        navigate('/induction-planning', { 
          state: { 
            generatedPlan: response,
            message: "Today's induction plan generated successfully!" 
          } 
        });
      }
    } catch (error) {
      console.error('Error generating plan:', error);
      alert('Failed to generate plan. Please try again.');
    }
  };

  // Check maintenance alerts
  const checkMaintenanceAlerts = () => {
    // Navigate to maintenance page with alerts filter
    navigate('/maintenance', { 
      state: { 
        showAlerts: true,
        filter: 'open'
      } 
    });
  };

  // View performance report
  const viewPerformanceReport = () => {
    navigate('/reports');
  };

  // Refresh summary data
  const handleRefreshData = () => {
    fetchSummaryData();
  };

  const navigation = [
    {
      name: 'Dashboard',
      href: '/',
      icon: '📊',
      description: 'System overview and analytics'
    },
    {
      name: 'Train Status',
      href: '/train-status',
      icon: '🚆',
      description: 'View all trains and their status'
    },
    {
      name: 'Induction Planning',
      href: '/induction-planning',
      icon: '📋',
      description: 'Create and manage induction plans'
    },
    {
      name: 'Data Input',
      href: '/data-input',
      icon: '📥',
      description: 'Upload and manage train data'
    },
    {
      name: 'Maintenance',
      href: '/maintenance',
      icon: '🔧',
      description: 'Job cards and maintenance scheduling'
    },
    {
      name: 'AI Assistant',
      href: '/chatbot',
      icon: '🤖',
      description: 'Get help and run scenarios'
    },
    {
      name: 'Depot Map',
      href: '/depot-map',
      icon: '🗺️',
      description: 'Visual depot layout and positioning'
    },
    {
      name: 'AR View',
      href: '/ar-view',
      icon: '👓',
      description: 'Augmented reality inspection'
    },
    {
      name: 'Reports',
      href: '/reports',
      icon: '📈',
      description: 'Analytics and performance reports'
    },
    {
      name: 'Feedback',
      href: '/feedback',
      icon: '💬',
      description: 'Share feedback and suggestions'
    }
  ];

  const isActiveLink = (href) => {
    if (href === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(href);
  };

  return (
    <>
      {/* Mobile overlay with backdrop blur */}
      {isOpen && (
        <div
          className="sidebar-overlay backdrop-blur"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      {/* Sidebar Container */}
      <div
        className={`sidebar-container ${
          isOpen ? 'sidebar-visible' : 'sidebar-hidden'
        }`}
        role="navigation"
        aria-label="Main navigation"
      >
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex-shrink-0">
            <div className="flex items-center justify-between h-16 px-4 bg-gray-800 border-b border-gray-700">
              <div className="flex items-center">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center shadow-lg">
                  <span className="text-white font-bold text-xl">🚆</span>
                </div>
                <div className="ml-3">
                  <span className="text-xl font-bold text-white block">RailSpark</span>
                  <span className="text-xs text-gray-400 block">v1.0</span>
                </div>
              </div>
              
              {/* Refresh and Close buttons */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={handleRefreshData}
                  disabled={loading}
                  className="p-1 text-gray-400 hover:text-white transition-colors disabled:opacity-50"
                  aria-label="Refresh data"
                  title="Refresh data"
                >
                  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </button>
                
                <button
                  onClick={onClose}
                  className="mobile-menu-btn"
                  aria-label="Close navigation menu"
                >
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          {/* Scrollable Content Area */}
          <div className="flex-1 overflow-y-auto">
            {/* Navigation */}
            <nav className="mt-6 px-4">
              <div className="space-y-2">
                {navigation.map((item) => {
                  const isActive = isActiveLink(item.href);
                  
                  return (
                    <Link
                      key={item.name}
                      to={item.href}
                      className={`nav-item ${
                        isActive ? 'nav-item-active' : 'nav-item-inactive'
                      }`}
                      onClick={() => {
                        // Close sidebar on mobile after navigation
                        if (window.innerWidth < 1024) {
                          onClose();
                        }
                      }}
                      aria-current={isActive ? 'page' : undefined}
                    >
                      <span className="text-lg mr-3 flex-shrink-0" aria-hidden="true">
                        {item.icon}
                      </span>
                      <div className="flex-1 min-w-0">
                        <div className="font-medium truncate">{item.name}</div>
                        <div className={`nav-item-description ${
                          isActive ? 'nav-item-description-active' : 'nav-item-description-inactive'
                        } truncate`}>
                          {item.description}
                        </div>
                      </div>
                      {isActive && (
                        <span 
                          className="ml-auto w-2 h-2 bg-white rounded-full flex-shrink-0"
                          aria-hidden="true"
                        />
                      )}
                    </Link>
                  );
                })}
              </div>
            </nav>

            {/* System Status */}
            <div className="mt-8 px-4">
              <div className="card bg-gray-800 border-gray-700 p-4">
                <h3 className="text-sm font-medium text-white mb-3 flex items-center">
                  <span className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></span>
                  System Status
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-gray-400">API Status</span>
                    <span className="flex items-center">
                      <span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                      <span className="text-xs text-green-400 font-medium">Online</span>
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-gray-400">Database</span>
                    <span className="flex items-center">
                      <span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                      <span className="text-xs text-green-400 font-medium">Connected</span>
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-gray-400">AI Services</span>
                    <span className="flex items-center">
                      <span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                      <span className="text-xs text-green-400 font-medium">Active</span>
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-gray-400">Last Sync</span>
                    <span className="text-xs text-gray-400">
                      {new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="mt-4 px-4">
              <div className="card bg-gray-800 border-gray-700 p-4">
                <h3 className="text-sm font-medium text-white mb-3 flex items-center">
                  <span className="text-yellow-400 mr-2">⚡</span>
                  Quick Actions
                </h3>
                <div className="space-y-2">
                  <button 
                    onClick={() => handleQuickAction("generate_plan")}
                    disabled={loading}
                    className="w-full text-left text-xs text-gray-300 hover:text-white p-2 rounded bg-gray-700 hover:bg-gray-600 transition-all duration-200 flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <span className="mr-2">🚀</span>
                    Generate Today's Plan
                  </button>
                  <button 
                    onClick={() => handleQuickAction("check_alerts")}
                    className="w-full text-left text-xs text-gray-300 hover:text-white p-2 rounded bg-gray-700 hover:bg-gray-600 transition-all duration-200 flex items-center"
                  >
                    <span className="mr-2">⚠️</span>
                    Check Maintenance Alerts
                  </button>
                  <button 
                    onClick={() => handleQuickAction("view_report")}
                    className="w-full text-left text-xs text-gray-300 hover:text-white p-2 rounded bg-gray-700 hover:bg-gray-600 transition-all duration-200 flex items-center"
                  >
                    <span className="mr-2">📊</span>
                    View Performance Report
                  </button>
                </div>
              </div>
            </div>

            {/* Statistics Summary */}
            <div className="mt-4 px-4">
              <div className="card bg-gray-800 border-gray-700 p-4">
                <div className="flex justify-between items-center mb-3">
                  <h3 className="text-sm font-medium text-white">Today's Summary</h3>
                  {loading && (
                    <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-white"></div>
                  )}
                </div>
                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div className="text-center p-2 bg-gray-700 rounded">
                    <div className="text-green-400 font-bold">{summaryData.activeTrains}</div>
                    <div className="text-gray-400">Active Trains</div>
                  </div>
                  <div className="text-center p-2 bg-gray-700 rounded">
                    <div className="text-blue-400 font-bold">{summaryData.scheduledTrains}</div>
                    <div className="text-gray-400">Scheduled</div>
                  </div>
                  <div className="text-center p-2 bg-gray-700 rounded">
                    <div className="text-yellow-400 font-bold">{summaryData.maintenanceTrains}</div>
                    <div className="text-gray-400">Maintenance</div>
                  </div>
                  <div className="text-center p-2 bg-gray-700 rounded">
                    <div className="text-purple-400 font-bold">{summaryData.brandedTrains}</div>
                    <div className="text-gray-400">Branded</div>
                  </div>
                </div>
                <div className="mt-2 text-xs text-gray-500 text-center">
                  Updated: {new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                </div>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="flex-shrink-0 p-4 border-t border-gray-700 bg-gray-800">
            <div className="text-center">
              <div className="text-xs text-gray-400 mb-1">
                RailSpark Induction System
              </div>
              <div className="text-xs text-gray-500">
                KMRL • {new Date().getFullYear()}
              </div>
              <div className="mt-2 flex justify-center space-x-3">
                <button 
                  className="text-gray-500 hover:text-gray-300 transition-colors"
                  aria-label="Settings"
                  onClick={() => navigate('/settings')}
                >
                  ⚙️
                </button>
                <button 
                  className="text-gray-500 hover:text-gray-300 transition-colors"
                  aria-label="Help"
                  onClick={() => navigate('/help')}
                >
                  ❓
                </button>
                <button 
                  className="text-gray-500 hover:text-gray-300 transition-colors"
                  aria-label="Notifications"
                  onClick={() => navigate('/notifications')}
                >
                  🔔
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        .sidebar-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.5);
          z-index: 40;
        }
        
        .sidebar-container {
          position: fixed;
          top: 0;
          left: 0;
          bottom: 0;
          width: 280px;
          background: #1f2937;
          z-index: 50;
          transition: transform 0.3s ease;
        }
        
        .sidebar-visible {
          transform: translateX(0);
        }
        
        .sidebar-hidden {
          transform: translateX(-100%);
        }
        
        .mobile-menu-btn {
          display: block;
          color: #9ca3af;
        }
        
        .nav-item {
          display: flex;
          align-items: center;
          padding: 0.75rem;
          border-radius: 0.5rem;
          transition: all 0.2s;
          text-decoration: none;
        }
        
        .nav-item-active {
          background: #374151;
          color: white;
        }
        
        .nav-item-inactive {
          color: #9ca3af;
          hover: background: #374151;
        }
        
        .nav-item-description {
          font-size: 0.75rem;
        }
        
        .nav-item-description-active {
          color: #d1d5db;
        }
        
        .nav-item-description-inactive {
          color: #6b7280;
        }
        
        .card {
          border-radius: 0.5rem;
          border: 1px solid;
        }
        
        @media (min-width: 1024px) {
          .sidebar-container {
            transform: translateX(0);
            position: relative;
          }
          
          .sidebar-overlay {
            display: none;
          }
          
          .mobile-menu-btn {
            display: none;
          }
        }
        
        .no-scroll {
          overflow: hidden;
        }
      `}</style>
    </>
  );
};

export default Sidebar;