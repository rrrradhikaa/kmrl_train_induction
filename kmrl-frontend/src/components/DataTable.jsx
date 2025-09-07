import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const initialData = [
  { id: "Metro-101", status: "Running", nextSlot: "10:30 AM", driver: "Driver A", aiConfidence: 92 },
  { id: "Metro-102", status: "Delayed", nextSlot: "11:00 AM", driver: "Driver B", aiConfidence: 88 },
  { id: "Metro-103", status: "Maintenance", nextSlot: "-", driver: "-", aiConfidence: 0 },
  { id: "Metro-104", status: "Running", nextSlot: "11:30 AM", driver: "Driver C", aiConfidence: 95 },
];

export default function DataTable() {
  const [data, setData] = useState(initialData);
  const [search, setSearch] = useState("");
  const [sortConfig, setSortConfig] = useState({ key: null, direction: "asc" });
  const navigate = useNavigate();

  // Sorting function
  const sortData = (key) => {
    let direction = "asc";
    if (sortConfig.key === key && sortConfig.direction === "asc") direction = "desc";
    setSortConfig({ key, direction });

    const sorted = [...data].sort((a, b) => {
      if (a[key] < b[key]) return direction === "asc" ? -1 : 1;
      if (a[key] > b[key]) return direction === "asc" ? 1 : -1;
      return 0;
    });
    setData(sorted);
  };

  // Filtered data
  const filteredData = data.filter(
    (d) =>
      d.id.toLowerCase().includes(search.toLowerCase()) ||
      d.status.toLowerCase().includes(search.toLowerCase()) ||
      d.driver.toLowerCase().includes(search.toLowerCase())
  );

  // Handlers
  const handleEdit = (trainId) => {
    navigate(`/train-details?id=${trainId}&mode=edit`);
  };

  const handleView = (trainId) => {
    navigate(`/train-details?id=${trainId}`);
  };

  const handleReschedule = (trainId) => {
    navigate(`/scheduler?trainId=${trainId}`);
  };

  return (
    <div className="bg-white rounded-2xl shadow p-4 mt-6">
      <h2 className="text-lg font-bold mb-4">Train Data Table</h2>

      {/* Search */}
      <input
        type="text"
        placeholder="Search by Train, Status, or Driver"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="mb-4 p-2 border rounded w-full"
      />

      {/* Table */}
      <table className="min-w-full table-auto border-collapse">
        <thead>
          <tr className="bg-gray-200">
            <th
              className="p-2 text-left cursor-pointer"
              onClick={() => sortData("id")}
            >
              Train ID {sortConfig.key === "id" ? (sortConfig.direction === "asc" ? "▲" : "▼") : ""}
            </th>
            <th
              className="p-2 text-left cursor-pointer"
              onClick={() => sortData("status")}
            >
              Status {sortConfig.key === "status" ? (sortConfig.direction === "asc" ? "▲" : "▼") : ""}
            </th>
            <th
              className="p-2 text-left cursor-pointer"
              onClick={() => sortData("nextSlot")}
            >
              Next Slot {sortConfig.key === "nextSlot" ? (sortConfig.direction === "asc" ? "▲" : "▼") : ""}
            </th>
            <th
              className="p-2 text-left cursor-pointer"
              onClick={() => sortData("driver")}
            >
              Assigned Driver {sortConfig.key === "driver" ? (sortConfig.direction === "asc" ? "▲" : "▼") : ""}
            </th>
            <th
              className="p-2 text-left cursor-pointer"
              onClick={() => sortData("aiConfidence")}
            >
              AI Confidence {sortConfig.key === "aiConfidence" ? (sortConfig.direction === "asc" ? "▲" : "▼") : ""}
            </th>
            <th className="p-2 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredData.map((train, index) => (
            <tr key={index} className="border-t">
              <td className="p-2">{train.id}</td>
              <td className="p-2">{train.status}</td>
              <td className="p-2">{train.nextSlot}</td>
              <td className="p-2">{train.driver}</td>
              <td className="p-2">{train.aiConfidence}%</td>
              <td className="p-2 space-x-2">
                <button
                  onClick={() => handleEdit(train.id)}
                  className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleView(train.id)}
                  className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
                >
                  View
                </button>
                <button
                  onClick={() => handleReschedule(train.id)}
                  className="bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600"
                >
                  Reschedule
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
} 
