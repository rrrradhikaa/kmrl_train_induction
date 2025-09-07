// src/components/Sidebar.jsx
import { Link } from "react-router-dom";

export default function sidebar() {
  return (
    <div className="w-64 bg-gray-800 text-white h-screen p-4">
      {/* Navigation links */}
      <nav className="space-y-2">
        <Link to="/dashboard" className="block hover:bg-gray-700 p-2 rounded">Dashboard</Link>
        <Link to="/traindetails" className="block hover:bg-gray-700 p-2 rounded">Train Details</Link>
        <Link to="/scheduler" className="block hover:bg-gray-700 p-2 rounded">Scheduler</Link>
        <Link to="/reports" className="block hover:bg-gray-700 p-2 rounded">Reports</Link>
        <Link to="/alerts" className="block hover:bg-gray-700 p-2 rounded">Alerts</Link>
      </nav>
    </div>
  );
} 


