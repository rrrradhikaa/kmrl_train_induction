import React from "react";

export default function AlertCard({ alert }) {
  // Determine colors based on severity
  const severityStyles = {
    high: "bg-red-100 border border-red-400 text-red-700",
    medium: "bg-yellow-100 border border-yellow-400 text-yellow-700",
    low: "bg-green-100 border border-green-400 text-green-700",
  };

  return (
    <div
      className={`px-4 py-3 rounded-lg shadow flex justify-between items-center ${severityStyles[alert.severity]}`}
    >
      <div>
        <span className="font-semibold">{alert.type}:</span> {alert.message}
      </div>
      <div className="font-bold uppercase">{alert.severity}</div>
    </div>
  );
}
