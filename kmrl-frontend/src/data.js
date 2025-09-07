// src/data.js

// Dashboard dummy data
export const dashboardData = {
  totalTrains: 50,
  activeTrains: 35,
  pendingMaintenance: 5,
  mileageData: [
    { train: "Metro-101", mileage: 1200 },
    { train: "Metro-102", mileage: 900 },
    { train: "Metro-103", mileage: 1500 },
  ],
  brandingPriority: [
    { train: "Metro-101", priority: "High" },
    { train: "Metro-102", priority: "Medium" },
  ],
};

// Alerts dummy data
export const alertData = [
  { id: 1, message: "Metro-104 scheduled for maintenance", severity: "High", date: "2025-09-05" },
  { id: 2, message: "Metro-102 inactive for 2 days", severity: "Medium", date: "2025-09-03" },
];

// Scheduler dummy data
export const scheduleData = [
  { train: "Metro-101", route: "A → B", maintenanceSlot: "10:00 AM" },
  { train: "Metro-102", route: "C → D", maintenanceSlot: "11:00 AM" },
];


