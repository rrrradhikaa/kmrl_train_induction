export default function Dashboard() {
  return (
    <div className="p-6 space-y-6">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
        <div className="bg-green-100 p-4 rounded-xl shadow text-center">
          <h2 className="text-xl font-bold text-green-700">12</h2>
          <p>Total Trains</p>
        </div>
        <div className="bg-blue-100 p-4 rounded-xl shadow text-center">
          <h2 className="text-xl font-bold text-blue-700">8</h2>
          <p>Ready for Induction</p>
        </div>
        <div className="bg-yellow-100 p-4 rounded-xl shadow text-center">
          <h2 className="text-xl font-bold text-yellow-700">3</h2>
          <p>Pending Maintenance</p>
        </div>
        <div className="bg-red-100 p-4 rounded-xl shadow text-center">
          <h2 className="text-xl font-bold text-red-700">5m</h2>
          <p>Avg Delay Today</p>
        </div>
        <div className="bg-purple-100 p-4 rounded-xl shadow text-center">
          <h2 className="text-xl font-bold text-purple-700">92%</h2>
          <p>AI Confidence</p>
        </div>
      </div>

      {/* Train Status Table */}
      <div className="bg-white p-6 rounded-xl shadow">
        <h2 className="text-lg font-bold mb-4">Train Status</h2>
        <table className="min-w-full border-collapse">
          <thead>
            <tr className="bg-gray-100">
              <th className="border p-2 text-left">Train ID</th>
              <th className="border p-2 text-left">Status</th>
              <th className="border p-2 text-left">Next Slot</th>
              <th className="border p-2 text-left">Driver</th>
              <th className="border p-2 text-left">AI Confidence</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="border p-2">Train #101</td>
              <td className="border p-2">Ready</td>
              <td className="border p-2">10:30 AM</td>
              <td className="border p-2">Driver A</td>
              <td className="border p-2">95%</td>
            </tr>
            <tr>
              <td className="border p-2">Train #102</td>
              <td className="border p-2">Maintenance</td>
              <td className="border p-2">-</td>
              <td className="border p-2">Driver B</td>
              <td className="border p-2">80%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}         
