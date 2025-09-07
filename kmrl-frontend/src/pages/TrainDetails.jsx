import React from "react";
import InfoCard from "../components/InfoCard";
import MaintenanceTable from "../components/MaintenanceTable";
import AIPredictionCard from "../components/AIPredictionCard";

// Sample data (replace later with API)
const trainData = {
  id: "Metro-101",
  status: "Running",
  nextSlot: "10:30 AM",
  driver: "Driver A",
  mileage: 1200,
  maintenanceHistory: [
    "01-09-2025: Engine check",
    "15-08-2025: Brake maintenance",
    "01-08-2025: Wheel alignment"
  ],
  aiPredictions: {
    delay: { value: "5 min", status: "ok" },
    maintenanceNeeded: { value: "No", status: "ok" }
  }
};

export default function TrainDetails() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Train Details</h1>

      {/* Top Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <InfoCard title="Train ID" value={trainData.id} />
        <InfoCard title="Status" value={trainData.status} />
        <InfoCard title="Next Scheduled Stop" value={trainData.nextSlot} />
        <InfoCard title="Driver" value={trainData.driver} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Mileage */}
        <InfoCard title="Mileage" value={`${trainData.mileage} km`} />

        {/* AI Predictions */}
        <div className="space-y-4">
          <AIPredictionCard 
            title="Predicted Delay" 
            value={trainData.aiPredictions.delay.value} 
            status={trainData.aiPredictions.delay.status} 
          />
          <AIPredictionCard 
            title="Maintenance Needed" 
            value={trainData.aiPredictions.maintenanceNeeded.value} 
            status={trainData.aiPredictions.maintenanceNeeded.status} 
          />
        </div>
      </div>

      {/* Maintenance Table */}
      <MaintenanceTable history={trainData.maintenanceHistory} />
    </div>
  );
}












