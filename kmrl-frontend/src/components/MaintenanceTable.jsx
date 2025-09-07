import React from "react";

export default function MaintenanceTable({ history }) {
  return (
    <div className="bg-white rounded-2xl shadow p-4 overflow-auto">
      <h2 className="font-semibold mb-2">Maintenance History</h2>
      <table className="min-w-full border-collapse">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-2 text-left">Date</th>
            <th className="p-2 text-left">Description</th>
          </tr>
        </thead>
        <tbody>
          {history.map((record, i) => {
            const [date, desc] = record.split(": ");
            return (
              <tr key={i} className="border-t">
                <td className="p-2">{date}</td>
                <td className="p-2">{desc}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}


