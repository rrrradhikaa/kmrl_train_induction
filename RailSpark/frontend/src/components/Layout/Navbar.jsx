import React, { useState, useContext, useEffect } from 'react';
import { AuthContext } from '../../contexts/AuthContext';

const Navbar = ({ onToggleSidebar, sidebarOpen }) => {
  const { user, logout } = useContext(AuthContext);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  
  // State for dynamic data
  const [trainStats, setTrainStats] = useState({
    totalTrains: 0,
    activeTrains: 0,
    inService: 0,
    maintenance: 0
  });
  
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch train statistics
  const fetchTrainStats = async () => {
    try {
      // Replace with your actual API endpoint
      const response = await fetch('/api/trains/stats');
      const data = await response.json();
      setTrainStats({
        totalTrains: data.total || 0,
        activeTrains: data.active || 0,
        inService: data.inService || 0,
        maintenance: data.maintenance || 0
      });
    } catch (error) {
      console.error('Error fetching train stats:', error);
      // Fallback to default values
      setTrainStats({
        totalTrains: 0,
        activeTrains: 0,
        inService: 0,
        maintenance: 0
      });
    }
  };

  // Fetch notifications
  const fetchNotifications = async () => {
    try {
      // Replace with your actual API endpoint
      const response = await fetch('/api/notifications');
      const data = await response.json();
      setNotifications(data || []);
    } catch (error) {
      console.error('Error fetching notifications:', error);
      setNotifications([]);
    } finally {
      setLoading(false);
    }
  };

  // Mark notification as read
  const markAsRead = async (notificationId) => {
    try {
      await fetch(`/api/notifications/${notificationId}/read`, {
        method: 'PUT'
      });
      // Update local state
      setNotifications(prev => prev.map(n => 
        n.id === notificationId ? { ...n, read: true } : n
      ));
    } catch (error) {
      console.error('Error marking notification as read:', error);
    }
  };

  // Mark all notifications as read
  const markAllAsRead = async () => {
    try {
      await fetch('/api/notifications/mark-all-read', {
        method: 'PUT'
      });
      setNotifications(prev => prev.map(n => ({ ...n, read: true })));
    } catch (error) {
      console.error('Error marking all notifications as read:', error);
    }
  };

  // Fetch data on component mount
  useEffect(() => {
  fetchTrainStats();
  fetchNotifications();

  // Start intervals
  const statsInterval = setInterval(fetchTrainStats, 30000);
  const notificationsInterval = setInterval(fetchNotifications, 60000);

  // Refresh when user switches back to tab
  const handleVisibilityChange = () => {
    if (document.visibilityState === 'visible') {
      fetchTrainStats();
      fetchNotifications();
    }
  };

  document.addEventListener('visibilitychange', handleVisibilityChange);

  // Cleanup on unmount
  return () => {
    clearInterval(statsInterval);
    clearInterval(notificationsInterval);
    document.removeEventListener('visibilitychange', handleVisibilityChange);
  };
}, []);


  const unreadCount = notifications.filter(n => !n.read).length;

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'warning': return '⚠️';
      case 'error': return '❌';
      case 'success': return '✅';
      case 'info': return 'ℹ️';
      default: return '📢';
    }
  };

  const getNotificationColor = (type) => {
    switch (type) {
      case 'warning': return 'text-yellow-600 bg-yellow-50';
      case 'error': return 'text-red-600 bg-red-50';
      case 'success': return 'text-green-600 bg-green-50';
      case 'info': return 'text-blue-600 bg-blue-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const handleNotificationClick = (notification) => {
    if (!notification.read) {
      markAsRead(notification.id);
    }
    // Add additional click handling logic here
    // e.g., navigate to relevant page
  };

  return (
    <nav className="bg-white shadow-lg border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Left side - Logo and menu button */}
          <div className="flex items-center">
            <button
              onClick={onToggleSidebar}
              className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
            >
              <span className="sr-only">Open sidebar</span>
              {sidebarOpen ? (
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>

            <div className="flex items-center ml-4">
              <div className="flex-shrink-0">
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                    <span className="text-white font-bold text-lg">🚆</span>
                  </div>
                  <div className="ml-3">
                    <h1 className="text-xl font-bold text-gray-900">RailSpark</h1>
                    <p className="text-xs text-gray-500">KMRL Induction System</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Center - Quick stats */}
          <div className="hidden md:flex items-center space-x-6">
            <div className="text-center">
              <div className="text-sm font-medium text-gray-900">{trainStats.totalTrains}</div>
              <div className="text-xs text-gray-500">Total Trains</div>
            </div>
            <div className="text-center">
              <div className="text-sm font-medium text-green-600">{trainStats.activeTrains}</div>
              <div className="text-xs text-gray-500">Active</div>
            </div>
            <div className="text-center">
              <div className="text-sm font-medium text-blue-600">{trainStats.inService}</div>
              <div className="text-xs text-gray-500">In Service</div>
            </div>
            <div className="text-center">
              <div className="text-sm font-medium text-yellow-600">{trainStats.maintenance}</div>
              <div className="text-xs text-gray-500">Maintenance</div>
            </div>
          </div>

          {/* Right side - User menu and notifications */}
          <div className="flex items-center space-x-4">
            {/* Notifications */}
            <div className="relative">
              <button
                onClick={() => setShowNotifications(!showNotifications)}
                className="p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 relative"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                {unreadCount > 0 && (
                  <span className="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full">
                    {unreadCount}
                  </span>
                )}
              </button>

              {/* Notifications dropdown */}
              {showNotifications && (
                <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-xl border border-gray-200 z-50">
                  <div className="p-4 border-b border-gray-200">
                    <div className="flex justify-between items-center">
                      <h3 className="text-lg font-medium text-gray-900">Notifications</h3>
                      {unreadCount > 0 && (
                        <span 
                          className="text-sm text-blue-600 cursor-pointer hover:text-blue-800"
                          onClick={markAllAsRead}
                        >
                          Mark all as read
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="max-h-96 overflow-y-auto">
                    {loading ? (
                      <div className="p-4 text-center text-gray-500">Loading notifications...</div>
                    ) : notifications.length > 0 ? (
                      notifications.map((notification) => (
                        <div
                          key={notification.id}
                          onClick={() => handleNotificationClick(notification)}
                          className={`p-4 border-b border-gray-100 hover:bg-gray-50 cursor-pointer ${
                            !notification.read ? 'bg-blue-50' : ''
                          }`}
                        >
                          <div className="flex items-start space-x-3">
                            <span className="text-lg">{getNotificationIcon(notification.type)}</span>
                            <div className="flex-1 min-w-0">
                              <p className="text-sm text-gray-900">{notification.message}</p>
                              <p className="text-xs text-gray-500 mt-1">
                                {new Date(notification.timestamp).toLocaleTimeString()} • {new Date(notification.timestamp).toLocaleDateString()}
                              </p>
                            </div>
                            {!notification.read && (
                              <span className="w-2 h-2 bg-blue-600 rounded-full"></span>
                            )}
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="p-4 text-center text-gray-500">
                        No new notifications
                      </div>
                    )}
                  </div>
                  <div className="p-2 border-t border-gray-200">
                    <button className="w-full text-center text-sm text-blue-600 hover:text-blue-800 py-2">
                      View all notifications
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* User menu */}
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center space-x-3 p-2 rounded-md text-gray-700 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full flex items-center justify-center">
                    <span className="text-white font-medium text-sm">
                      {user?.username?.charAt(0).toUpperCase() || 'U'}
                    </span>
                  </div>
                </div>
                <div className="hidden md:block">
                  <div className="text-sm font-medium text-gray-900">
                    {user?.username || 'Operator'}
                  </div>
                  <div className="text-xs text-gray-500 capitalize">
                    {user?.role || 'operator'}
                  </div>
                </div>
                <svg className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {/* User dropdown menu */}
              {showUserMenu && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl border border-gray-200 z-50">
                  <div className="p-4 border-b border-gray-200">
                    <div className="text-sm font-medium text-gray-900">{user?.username || 'Operator'}</div>
                    <div className="text-xs text-gray-500">{user?.email || `${user?.role || 'operator'}@kmrl.org`}</div>
                  </div>
                  <div className="py-1">
                    <a href="/profile" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                      👤 Profile Settings
                    </a>
                    <a href="/preferences" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                      ⚙️ Preferences
                    </a>
                    <a href="/help" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                      ❓ Help & Support
                    </a>
                  </div>
                  <div className="py-1 border-t border-gray-200">
                    <button
                      onClick={logout}
                      className="block w-full text-left px-4 py-2 text-sm text-red-700 hover:bg-red-50"
                    >
                      🚪 Sign out
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Overlay for dropdowns */}
      {(showUserMenu || showNotifications) && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => {
            setShowUserMenu(false);
            setShowNotifications(false);
          }}
        ></div>
      )}
    </nav>
  );
};

export default Navbar;
