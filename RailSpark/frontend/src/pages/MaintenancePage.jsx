import React, { useState } from "react";
import MaintenanceCard from "../components/Maintenance/MaintenanceCard";

const dummyJobs = [
  {
    id: 1,
    title: "Brake Inspection",
    trainNumber: "Train 101",
    description: "Check brake pads and replace worn-out parts.",
    status: "pending",
    dueDate: "2025-09-25",
  },
  {
    id: 2,
    title: "Air Conditioning Check",
    trainNumber: "Train 202",
    description: "Inspect AC units and refill coolant.",
    status: "in_progress",
    dueDate: "2025-09-28",
  },
  {
    id: 3,
    title: "Wheel Alignment",
    trainNumber: "Train 305",
    description: "Align wheels to prevent uneven wear.",
    status: "overdue",
    dueDate: "2025-09-20",
  },
];

const MaintenancePage = () => {
  const [jobs, setJobs] = useState(dummyJobs);

  const handleAction = (id, action) => {
    if (action === "markCompleted") {
      setJobs((prev) =>
        prev.map((job) =>
          job.id === id ? { ...job, status: "completed" } : job
        )
      );
    } else if (action === "viewDetails") {
      alert(`Show details for job ID: ${id}`);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Maintenance Jobs</h1>
        <button className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded shadow">
          + New Job
        </button>
      </header>

      {/* Job List */}
      {jobs.length === 0 ? (
        <div className="text-gray-400 text-center py-12">
          No maintenance jobs available 🚆
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {jobs.map((job) => (
            <MaintenanceCard key={job.id} job={job} onAction={handleAction} />
          ))}
        </div>
      )}
    </div>
  );
};

export default MaintenancePage;
