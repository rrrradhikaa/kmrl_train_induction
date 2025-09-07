// src/components/InfoCard.jsx
import React from "react";

export default function InfoCard({ title, value }) {
  return (
    <div className="bg-white rounded-2xl shadow p-4 flex flex-col items-center justify-center">
      <h2 className="text-gray-500 text-sm">{title}</h2>
      <p className="text-2xl font-bold">{value}</p>
    </div>
  );
}



