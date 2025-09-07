import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

// Sample Data
const scheduleData = [
  { train: "Metro-101", mileage: 1200 },
  { train: "Metro-102", mileage: 950 },
  { train: "Metro-103", mileage: 1100 },
];

export default function Scheduler() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Scheduler</h1>

      {/* Top Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-2xl shadow p-4">
          <h2 className="font-semibold">Total Routes Assigned</h2>
          <p className="text-2xl font-bold">10</p>
        </div>
        <div className="bg-white rounded-2xl shadow p-4">
          <h2 className="font-semibold">Maintenance Slots</h2>
          <p className="text-2xl font-bold">3</p>
        </div>
        <div className="bg-white rounded-2xl shadow p-4">
          <h2 className="font-semibold">Conflicts</h2>
          <p className="text-2xl font-bold text-red-600">1</p>
        </div>
      </div>

      {/* Mileage Chart */}
      <div className="bg-white rounded-2xl shadow p-4">
        <h2 className="font-semibold mb-2">Mileage per Train</h2>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={scheduleData}>
            <XAxis dataKey="train" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="mileage" stroke="#3B82F6" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Schedule Table */}
      <div className="bg-white rounded-2xl shadow p-4">
        <h2 className="font-semibold mb-2">Train Schedule</h2>
        <table className="min-w-full border-collapse">
          <thead className="bg-gray-200">
            <tr>
              <th className="p-2 text-left">Train</th>
              <th className="p-2 text-left">Route</th>
              <th className="p-2 text-left">Driver</th>
              <th className="p-2 text-left">Next Slot</th>
              <th className="p-2 text-left">Conflict</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-t">
              <td className="p-2">Metro-101</td>
              <td className="p-2">Route A</td>
              <td className="p-2">Driver A</td>
              <td className="p-2">10:30 AM</td>
              <td className="p-2 text-red-600">Yes</td>
            </tr>
            <tr className="border-t">
              <td className="p-2">Metro-102</td>
              <td className="p-2">Route B</td>
              <td className="p-2">Driver B</td>
              <td className="p-2">11:00 AM</td>
              <td className="p-2 text-green-600">No</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
} 









