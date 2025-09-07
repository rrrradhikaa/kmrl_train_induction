import React from "react";
import { Link, Outlet } from "react-router-dom";
import { Home, Train, Calendar, FileText, Bell } from "lucide-react";

export default function Layout() {
  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 text-white flex flex-col p-4 space-y-6">
        <h1 className="text-2xl font-bold mb-6">KMRL Dashboard</h1>
        <nav className="space-y-4">
          <Link to="/" className="w-full flex items-center p-2 hover:bg-gray-700 rounded">
            <Home className="mr-2 h-5 w-5" /> Dashboard
          </Link>
          <Link to="/train-details" className="w-full flex items-center p-2 hover:bg-gray-700 rounded">
            <Train className="mr-2 h-5 w-5" /> Train Details
          </Link>
          <Link to="/scheduler" className="w-full flex items-center p-2 hover:bg-gray-700 rounded">
            <Calendar className="mr-2 h-5 w-5" /> Scheduler
          </Link>
          <Link to="/reports" className="w-full flex items-center p-2 hover:bg-gray-700 rounded">
            <FileText className="mr-2 h-5 w-5" /> Reports
          </Link>
          <Link to="/alerts" className="w-full flex items-center p-2 hover:bg-gray-700 rounded">
            <Bell className="mr-2 h-5 w-5" /> Alerts & Notifications
          </Link>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 bg-gray-100 overflow-auto">
        <Outlet /> {/* This will render the selected page */}
      </div>
    </div>
  );
}    
