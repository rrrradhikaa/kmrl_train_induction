import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, PieChart, Pie, Cell, ResponsiveContainer } from "recharts";
import DataTable from "../components/datatable";
import InfoCard from "../components/InfoCard";
import ChartCard from "../components/ChartCard";

const trainSummary = {
  total: 10,
  active: 7,
  pendingMaintenance: 3,
  onTime: 85,
  fuelConsumption: 1200,
};

const mileageData = [
  { train: "Metro-101", mileage: 1200 },
  { train: "Metro-102", mileage: 950 },
  { train: "Metro-103", mileage: 1100 },
];

const brandingData = [
  { name: "Compliant", value: 7 },
  { name: "Non-Compliant", value: 3 },
];

const COLORS = ["#10B981", "#EF4444"];

export default function Dashboard1() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
        <InfoCard title="Total Trains" value={trainSummary.total} />
        <InfoCard title="Active Trains" value={trainSummary.active} />
        <InfoCard title="Pending Maintenance" value={trainSummary.pendingMaintenance} />
        <InfoCard title="On-Time Performance" value={`${trainSummary.onTime}%`} />
        <InfoCard title="Fuel Consumption" value={`${trainSummary.fuelConsumption} L`} />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ChartCard title="Mileage Chart">
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={mileageData}>
              <XAxis dataKey="train" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="mileage" stroke="#3B82F6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Branding Status">
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={brandingData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                {brandingData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {/* Data Table */}
      <div className="mt-6">
        <DataTable />
      </div>
    </div>
  );
}


