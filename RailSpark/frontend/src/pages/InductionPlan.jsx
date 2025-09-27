import React from 'react';
import InductionPlan from '../components/Dashboard/InductionPlan';

const InductionPlanPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Induction Planning</h1>
          <p className="text-gray-600 mt-2">
            Create and manage train induction plans using AI optimization
          </p>
        </div>

        {/* Induction Plan Component */}
        <InductionPlan />
      </div>
    </div>
  );
};

export default InductionPlanPage;