// src/components/ChartCard.jsx
import React from "react";

export default function ChartCard({ title, children }) {
  return (
    <div className="bg-white rounded-2xl shadow p-4">
      <h2 className="font-semibold mb-2">{title}</h2>
      {children}
    </div>
  );
}
