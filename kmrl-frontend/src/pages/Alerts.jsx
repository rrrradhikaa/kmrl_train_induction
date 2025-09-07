import React from "react";
import AlertCard from "../components/AlertCard";

// Sample data (later replace with API)
const alertsData = [
  { type: "Delay", message: "Metro-102 delayed by 15 mins", severity: "high" },
  { type: "Maintenance", message: "Metro-103 engine check required", severity: "medium" },
  { type: "Staff", message: "Driver absent for Metro-101", severity: "high" },
  { type: "System", message: "AI predicted failure for Metro-102", severity: "medium" },
];

export default function Alerts() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Alerts & Notifications</h1>

      {/* Alerts List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {alertsData.map((alert, i) => (
          <AlertCard key={i} alert={alert} />
        ))}
      </div>
    </div>
  );
}











