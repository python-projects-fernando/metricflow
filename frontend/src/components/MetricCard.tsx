import React from 'react'

interface MetricCardProps {
  title: string
  value: string | number
  description?: string
  color?: 'green' | 'blue' | 'purple' | 'indigo'
  icon?: React.ReactNode
}

const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  description,
  color = 'indigo',
  icon
}) => {
  const colorClasses = {
    green: 'bg-green-50 text-green-800 border-green-200',
    blue: 'bg-blue-50 text-blue-800 border-blue-200',
    purple: 'bg-purple-50 text-purple-800 border-purple-200',
    indigo: 'bg-indigo-50 text-indigo-800 border-indigo-200'
  }

  const bgColorClass = colorClasses[color]

  return (
    <div className={`bg-white rounded-lg shadow p-4 border ${bgColorClass} hover:shadow-md transition-shadow`}>
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-medium text-gray-500">{title}</h3>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
        </div>
        {icon && <div className="text-gray-400">{icon}</div>}
      </div>
      {description && (
        <p className="text-xs text-gray-500 mt-2">{description}</p>
      )}
    </div>
  )
}

export default MetricCard