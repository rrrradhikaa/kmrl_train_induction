import React from 'react';
import Branding from '../components/Branding/Branding';

const BrandingPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Branding</h1>
          <p className="text-gray-600 mt-2">
            Advertising contracts and exposure tracking
          </p>
        </div>

        {/* Branding Component */}
        <Branding />
      </div>
    </div>
  );
};

export default BrandingPage;