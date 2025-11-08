import React, { useState, useRef } from 'react'
import type {ChangeEvent} from 'react'
import { uploadCsv, type MetricsResponse } from '../services/apiClient'

interface UploadZoneProps {
  onFileUpload: (file: File) => void
  onMetricsReceived: (metrics: MetricsResponse) => void
  onUploadError: (error: string) => void
  isLoading: boolean
  setIsLoading: (loading: boolean) => void
}

const UploadZone: React.FC<UploadZoneProps> = ({
  onFileUpload,
  onMetricsReceived,
  onUploadError,
  isLoading,
  setIsLoading
}) => {
  const [fileName, setFileName] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Função para lidar com o arquivo (comum ao clique e ao drag & drop)
  const handleFile = (file: File) => {
    if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
      onUploadError('Please select a CSV file.')
      return
    }
    setFileName(file.name)
    onFileUpload(file)

    // Envia o arquivo para a API
    setIsLoading(true)
    uploadCsv(file)
      .then(metrics => {
        onMetricsReceived(metrics)
      })
      .catch(error => {
        console.error('Upload error:', error)
        onUploadError(error.message || 'Upload failed')
      })
      .finally(() => {
        setIsLoading(false)
      })
  }

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      handleFile(file)
    }
  }

  const triggerFileSelect = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click()
    }
  }

  // Drag & Drop handlers
  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault(); // Necessário para permitir o drop
    e.stopPropagation();
  }

  const handleDragEnter = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    // Aqui você pode mudar o estilo para indicar que o drop é aceito
    // Ex: adicionar uma classe CSS ou mudar a borda
  }

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    // Reverter o estilo
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();

    const droppedFiles = e.dataTransfer.files;
    if (droppedFiles.length > 0) {
      const file = droppedFiles[0];
      handleFile(file);
    }
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-800">Upload CSV</h2>
        {isLoading && (
          <span className="bg-yellow-100 text-yellow-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
            Processing...
          </span>
        )}
      </div>

      <div
        className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-indigo-400 transition-colors cursor-pointer"
        onClick={triggerFileSelect}
        onDragOver={handleDragOver}    // ← Adicione esta linha
        onDragEnter={handleDragEnter}  // ← Adicione esta linha
        onDragLeave={handleDragLeave}  // ← Adicione esta linha
        onDrop={handleDrop}            // ← Adicione esta linha
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".csv"
          className="hidden"
        />

        {fileName ? (
          <div className="text-center">
            <p className="text-gray-700 font-medium">{fileName}</p>
            <p className="text-sm text-gray-500 mt-1">Click to change file</p>
          </div>
        ) : (
          <>
            <p className="text-gray-500 mb-2">Drag & drop your file here</p>
            <p className="text-sm text-gray-400 mb-4">or</p>
            <button
              type="button"
              className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
            >
              Browse Files
            </button>
          </>
        )}
      </div>

      <p className="text-sm text-gray-500 mt-3">
        Expected columns: <code className="bg-gray-100 px-1 rounded">date</code>,{' '}
        <code className="bg-gray-100 px-1 rounded">amount</code>,{' '}
        <code className="bg-gray-100 px-1 rounded">category</code>,{' '}
        <code className="bg-gray-100 px-1 rounded">status</code> (optional)
      </p>
    </div>
  )
}

export default UploadZone