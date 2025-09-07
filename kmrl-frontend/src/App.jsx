import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Layout (persistent sidebar)
import Layout from "./components/Layout";

// Pages
import Dashboard1 from "./pages/Dashboard1";
import TrainDetails from "./pages/TrainDetails";
import Scheduler from "./pages/Scheduler";
import Reports from "./pages/Reports";
import Alerts from "./pages/Alerts";

function App() {
  return (
    <Router>
      <Routes>
        {/* Wrap all pages inside the Layout (sidebar + main content) */}
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard1 />} />          {/* Dashboard shows at "/" */}
          <Route path="train-details" element={<TrainDetails />} />
          <Route path="scheduler" element={<Scheduler />} />
          <Route path="reports" element={<Reports />} />
          <Route path="alerts" element={<Alerts />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App; 