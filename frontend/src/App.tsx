import React, { useState } from 'react'
import UploadZone from './components/UploadZone'
import MetricsDashboard from './components/MetricsDashboard'
import type { MetricsResponse } from './services/apiClient'

function App() {
  const [isLoading, setIsLoading] = useState(false)
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null)

  const handleFileUpload = (file: File) => {
    console.log('File selected:', file.name)
    // Agora o upload é feito dentro do componente UploadZone
  }

  const handleMetricsReceived = (metrics: MetricsResponse) => {
    console.log('Metrics received:', metrics)
    setMetrics(metrics)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-100 p-6">
      <div className="max-w-4xl mx-auto">
        <header className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-indigo-800 mb-2">MetricFlow Dashboard</h1>
          <p className="text-gray-600">Upload your CSV and get instant metrics</p>
        </header>

        <UploadZone
          onFileUpload={handleFileUpload}
          onMetricsReceived={handleMetricsReceived}
          isLoading={isLoading}
          setIsLoading={setIsLoading}
        />

        {metrics && <MetricsDashboard metrics={metrics} />}
      </div>
    </div>
  )
}

export default App