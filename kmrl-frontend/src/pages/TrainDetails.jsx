import React, { useEffect, useState } from "react";
import InfoCard from "../components/InfoCard";
import MaintenanceTable from "../components/MaintenanceTable";
import AIPredictionCard from "../components/AIPredictionCard";
import {
  getFitnessCertificates,
  getJobCards,
  getMileageBalancing,
  getBrandingPriorities,
  getCleaningSlots,
  getStablingGeometry,
} from "../api";

export default function TrainDetails() {
  const [fitnessCertificates, setFitnessCertificates] = useState([]);
  const [jobCards, setJobCards] = useState([]);
  const [mileage, setMileage] = useState(null);
  const [branding, setBranding] = useState([]);
  const [cleaning, setCleaning] = useState([]);
  const [stabling, setStabling] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [fitnessRes, jobRes, mileageRes, brandingRes, cleaningRes, stablingRes] =
          await Promise.all([
            getFitnessCertificates(),
            getJobCards(),
            getMileageBalancing(),
            getBrandingPriorities(),
            getCleaningSlots(),
            getStablingGeometry(),
          ]);

        setFitnessCertificates(fitnessRes.data || []);
        setJobCards(jobRes.data || []);
        setMileage(mileageRes.data || null);
        setBranding(brandingRes.data || []);
        setCleaning(cleaningRes.data || []);
        setStabling(stablingRes.data || []);
      } catch (err) {
        console.error("Error fetching train details:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return <div className="p-6">Loading train details...</div>;
  }

  return (
    <div className="p-6 space-y-8">
      <h1 className="text-2xl font-bold">Train Details</h1>

      {/* Top Info Cards (dummy for now, can link to backend later) */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <InfoCard title="Train ID" value="Metro-101" />
        <InfoCard title="Status" value="Running" />
        <InfoCard title="Next Scheduled Stop" value="10:30 AM" />
        <InfoCard title="Driver" value="Driver A" />
      </div>

      {/* Mileage + AI predictions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <InfoCard title="Mileage" value={`${mileage?.mileage || 0} km`} />
        <div className="space-y-4">
          <AIPredictionCard title="Predicted Delay" value="5 min" status="ok" />
          <AIPredictionCard title="Maintenance Needed" value="No" status="ok" />
        </div>
      </div>

      {/* Fitness Certificates */}
      <section>
        <h2 className="text-xl font-semibold mb-2">Fitness Certificates</h2>
        <ul className="list-disc pl-6">
          {fitnessCertificates.map((f, idx) => (
            <li key={idx}>{JSON.stringify(f)}</li>
          ))}
        </ul>
      </section>

      {/* Job Cards */}
      <section>
        <h2 className="text-xl font-semibold mb-2">Job Cards</h2>
        <MaintenanceTable history={jobCards.map((j) => j.description || JSON.stringify(j))} />
      </section>

      {/* Mileage Balancing */}
      <section>
        <h2 className="text-xl font-semibold mb-2">Mileage Balancing</h2>
        <pre className="bg-gray-100 p-2 rounded">{JSON.stringify(mileage, null, 2)}</pre>
      </section>

      {/* Branding Priorities */}
      <section>
        <h2 className="text-xl font-semibold mb-2">Branding Priorities</h2>
        <ul className="list-disc pl-6">
          {branding.map((b, idx) => (
            <li key={idx}>{JSON.stringify(b)}</li>
          ))}
        </ul>
      </section>

      {/* Cleaning Slots */}
      <section>
        <h2 className="text-xl font-semibold mb-2">Cleaning Slots</h2>
        <ul className="list-disc pl-6">
          {cleaning.map((c, idx) => (
            <li key={idx}>{JSON.stringify(c)}</li>
          ))}
        </ul>
      </section>

      {/* Stabling Geometry */}
      <section>
        <h2 className="text-xl font-semibold mb-2">Stabling Geometry</h2>
        <ul className="list-disc pl-6">
          {stabling.map((s, idx) => (
            <li key={idx}>{JSON.stringify(s)}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}
