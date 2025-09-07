import React from "react";

export default function DashboardCards({ cards }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
      {cards.map((card, i) => (
        <div
          key={i}
          className={`bg-white rounded-2xl shadow p-4 text-center`}
        >
          <h2 className="font-semibold">{card.title}</h2>
          <p className="text-2xl font-bold">{card.value}</p>
        </div>
      ))}
    </div>
  );
}
