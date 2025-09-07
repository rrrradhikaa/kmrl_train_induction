import React from "react";

export default function AIPredictionCard({ title, value, status }) {
  const statusColor = status === "warning" ? "bg-yellow-200 text-yellow-800" :
                      status === "ok" ? "bg-green-200 text-green-800" : "bg-red-200 text-red-800";

  return (
    <div className={`bg-white rounded-2xl shadow p-4 flex justify-between items-center`}>
      <div>
        <h2 className="font-semibold">{title}</h2>
        <p className="mt-1 text-lg">{value}</p>
      </div>
      <span className={`px-2 py-1 rounded-full font-bold ${statusColor}`}>{status.toUpperCase()}</span>
    </div>
  );
}

