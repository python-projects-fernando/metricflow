import React from 'react';
import MetricCard from './MetricCard';
import RevenueChart from './RevenueChart';
import type { MetricsResponse } from '../services/apiClient';
import { downloadExcel, downloadPdf } from '../services/apiClient';

interface MetricsDashboardProps {
  metrics: MetricsResponse;
  reportId: string;
}

const MetricsDashboard: React.FC<MetricsDashboardProps> = ({ metrics, reportId }) => {

  const handleDownloadExcel = () => {
    if (reportId) {
      downloadExcel(reportId);
    } else {
      console.error("reportId is missing for Excel download.");
    }
  };

  const handleDownloadPdf = () => {
    if (reportId) {
      downloadPdf(reportId);
    } else {
      console.error("reportId is missing for PDF download.");
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-800">Business Metrics</h2>
        <div className="flex space-x-2">
          <button
            onClick={handleDownloadExcel}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
            disabled={!reportId}
          >
            Download Excel
          </button>
          <button
            onClick={handleDownloadPdf}
            className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"
            disabled={!reportId}
          >
            Download PDF
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <MetricCard
          title="Total Revenue"
          value={`$${metrics.total_revenue.toFixed(2)}`}
          description="Sum of completed sales"
          color="green"
        />

        <MetricCard
          title="MoM Growth"
          value={`${metrics.mom_growth_rate.toFixed(2)}%`}
          description="Month-over-month increase"
          color="blue"
        />

        <MetricCard
          title="Avg. Ticket"
          value={`$${metrics.average_ticket.toFixed(2)}`}
          description="Average transaction value"
          color="purple"
        />

        <MetricCard
          title="New Leads"
          value={metrics.total_leads}
          description="Total leads generated"
          color="indigo"
        />
      </div>

      <div className="mb-6">
        <h3 className="text-lg font-medium text-gray-800 mb-3">Monthly Revenue</h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3 mb-6">
          {Object.entries(metrics.monthly_revenue).map(([month, revenue]) => (
            <div key={month} className="bg-gray-50 rounded-lg p-3 text-center">
              <p className="text-xs text-gray-500">{month}</p>
              <p className="font-medium text-gray-900">${revenue.toFixed(2)}</p>
            </div>
          ))}
        </div>
      </div>

      <RevenueChart monthlyRevenue={metrics.monthly_revenue} />
    </div>
  );
};

export default MetricsDashboard;
