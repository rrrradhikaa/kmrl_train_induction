import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";

// Sample Data
const performanceData = [
  { train: "Metro-101", speed: 45, delay: 5, mileage: 1200 },
  { train: "Metro-102", speed: 40, delay: 15, mileage: 950 },
  { train: "Metro-103", speed: 50, delay: 0, mileage: 1100 },
];

const maintenanceData = [
  { train: "Metro-101", pending: 1, completed: 2, overdue: 0 },
  { train: "Metro-102", pending: 2, completed: 1, overdue: 1 },
  { train: "Metro-103", pending: 0, completed: 3, overdue: 0 },
];

export default function Reports() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Reports</h1>

      {/* Performance Chart */}
      <div className="bg-white rounded-2xl shadow p-4">
        <h2 className="font-semibold mb-2">Train Performance</h2>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={performanceData}>
            <XAxis dataKey="train" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="speed" fill="#3B82F6" />
            <Bar dataKey="delay" fill="#EF4444" />
            <Bar dataKey="mileage" fill="#10B981" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Maintenance Table */}
      <div className="bg-white rounded-2xl shadow p-4">
        <h2 className="font-semibold mb-2">Maintenance Reports</h2>
        <table className="min-w-full border-collapse">
          <thead className="bg-gray-200">
            <tr>
              <th className="p-2 text-left">Train</th>
              <th className="p-2 text-left">Pending</th>
              <th className="p-2 text-left">Completed</th>
              <th className="p-2 text-left">Overdue</th>
            </tr>
          </thead>
          <tbody>
            {maintenanceData.map((m, i) => (
              <tr key={i} className="border-t">
                <td className="p-2">{m.train}</td>
                <td className="p-2 text-yellow-600">{m.pending}</td>
                <td className="p-2 text-green-600">{m.completed}</td>
                <td className="p-2 text-red-600">{m.overdue}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
} 





