export default function Navbar() {
  return (
    <div className="bg-white border-b border-gray-200 h-14 flex items-center justify-between px-6 shadow-sm">
      {/* Project name */}
      <h1 className="font-semibold text-gray-800">
        KMRL AI Induction Dashboard
      </h1>

      {/* Search + User */}
      <div className="flex items-center space-x-4">
        <input
          type="text"
          placeholder="Search trains, routes..."
          className="border rounded px-3 py-1 text-sm"
        />
        <div className="w-8 h-8 rounded-full bg-gray-400"></div>
      </div>
    </div>
  );
}