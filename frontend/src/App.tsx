import { useState } from 'react'
import UploadZone from './components/UploadZone'
import MetricsDashboard from './components/MetricsDashboard'
import type { MetricsResponse } from './services/apiClient'

function App() {
  const [isLoading, setIsLoading] = useState(false)
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileUpload = (file: File) => {
    console.log('File selected:', file.name)
    setError(null) // Limpa erros anteriores
  }

  const handleMetricsReceived = (metrics: MetricsResponse) => {
    console.log('Metrics received:', metrics)
    setMetrics(metrics)
  }

  const handleUploadError = (errorMessage: string) => {
    setError(errorMessage)
    setMetrics(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-100 p-4 sm:p-6">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8 text-center">
          <h1 className="text-3xl sm:text-4xl font-bold text-indigo-800 mb-2">
            MetricFlow Dashboard
          </h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Upload your business CSV data and get instant, actionable insights.
            No spreadsheets. No complex tools. Just clarity.
          </p>
        </header>

        <UploadZone
          onFileUpload={handleFileUpload}
          onMetricsReceived={handleMetricsReceived}
          onUploadError={handleUploadError}
          isLoading={isLoading}
          setIsLoading={setIsLoading}
        />

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-700 font-medium">Error: {error}</p>
          </div>
        )}

        {metrics && <MetricsDashboard metrics={metrics} />}

        {!metrics && !isLoading && !error && (
          <div className="bg-white rounded-xl shadow-lg p-8 text-center">
            <h3 className="text-xl font-medium text-gray-700 mb-2">
              Ready to analyze your data?
            </h3>
            <p className="text-gray-500">
              Upload a CSV file to see your business metrics instantly.
            </p>
          </div>
        )}
      </div>

      <footer className="mt-12 text-center text-gray-500 text-sm">
        <p>MetricFlow — Turn data into insights, fast.</p>
      </footer>
    </div>
  )
}

export default App