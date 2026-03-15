'use client'

import React, { useEffect, useState } from 'react'
import Link from 'next/link'
import api from '@/services/api'
import { ProtectedRoute } from '@/components/ProtectedRoute'
import { useAuth } from '@/context/AuthContext'

interface ErrorRecord {
  timestamp: string
  type: string
  message: string
  context?: Record<string, any>
}

interface DashboardData {
  total_recent_errors: number
  error_counts: Record<string, number>
  ai_agent_healthy: boolean
  recent_errors: ErrorRecord[]
  user: {
    id: number
    username: string
    email: string
  }
}

export default function MonitoringDashboard() {
  const { logout } = useAuth()
  const [dashboard, setDashboard] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [aiHealth, setAiHealth] = useState(false)
  const [refreshInterval, setRefreshInterval] = useState<NodeJS.Timeout | null>(null)

  useEffect(() => {
    loadDashboard()
    
    // Auto-refresh every 10 seconds
    const interval = setInterval(loadDashboard, 10000)
    setRefreshInterval(interval)
    
    return () => {
      if (interval) clearInterval(interval)
    }
  }, [])

  const loadDashboard = async () => {
    try {
      const response = await api.get('/api/monitoring/dashboard')
      setDashboard(response.data)
      setAiHealth(response.data.ai_agent_healthy)
      setError(null)
    } catch (err) {
      setError('Failed to load monitoring dashboard')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    logout()
    window.location.href = '/'
  }

  if (loading) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen flex items-center justify-center bg-slate-900">
          <div className="text-white text-xl">Loading dashboard...</div>
        </div>
      </ProtectedRoute>
    )
  }

  return (
    <ProtectedRoute>
      <main className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-800">
        {/* Top Bar */}
        <div className="border-b border-blue-500 border-opacity-20 px-4 py-4 sticky top-0 z-50 bg-slate-900 bg-opacity-95">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-white">System Monitoring</h1>
              <p className="text-slate-400 text-sm">Real-time error tracking & AI diagnostics</p>
            </div>
            <div className="flex items-center gap-4">
              <div className={`flex items-center gap-2 px-3 py-2 rounded ${aiHealth ? 'bg-green-500 bg-opacity-20' : 'bg-red-500 bg-opacity-20'}`}>
                <div className={`w-2 h-2 rounded-full ${aiHealth ? 'bg-green-500' : 'bg-red-500'}`}></div>
                <span className={aiHealth ? 'text-green-400' : 'text-red-400'}>
                  {aiHealth ? 'AI Agent Active' : 'AI Agent Offline'}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="px-4 py-2 border border-slate-600 text-slate-300 rounded hover:bg-slate-700 transition-all"
              >
                Logout
              </button>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 py-8">
          {error && (
            <div className="mb-6 p-4 bg-red-500 bg-opacity-10 border border-red-500 rounded text-red-400">
              {error}
            </div>
          )}

          {dashboard && (
            <>
              {/* Stats Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="p-6 bg-slate-800 border border-slate-700 rounded-lg">
                  <div className="text-slate-400 text-sm font-medium">Total Recent Errors</div>
                  <div className="text-4xl font-bold text-white mt-2">{dashboard.total_recent_errors}</div>
                  <div className="text-xs text-slate-500 mt-2">Last 20 errors tracked</div>
                </div>

                <div className="p-6 bg-slate-800 border border-slate-700 rounded-lg">
                  <div className="text-slate-400 text-sm font-medium">Error Types</div>
                  <div className="text-4xl font-bold text-white mt-2">
                    {Object.keys(dashboard.error_counts).length}
                  </div>
                  <div className="text-xs text-slate-500 mt-2">Unique error types</div>
                </div>

                <div className={`p-6 border rounded-lg ${aiHealth ? 'bg-green-500 bg-opacity-10 border-green-500 border-opacity-30' : 'bg-red-500 bg-opacity-10 border-red-500 border-opacity-30'}`}>
                  <div className={aiHealth ? 'text-green-400 text-sm font-medium' : 'text-red-400 text-sm font-medium'}>
                    AI Agent Status
                  </div>
                  <div className={`text-4xl font-bold mt-2 ${aiHealth ? 'text-green-400' : 'text-red-400'}`}>
                    {aiHealth ? 'Healthy' : 'Offline'}
                  </div>
                  <div className="text-xs text-slate-500 mt-2">Auto-analysis enabled</div>
                </div>
              </div>

              {/* Error Breakdown */}
              {Object.keys(dashboard.error_counts).length > 0 && (
                <div className="mb-8 p-6 bg-slate-800 border border-slate-700 rounded-lg">
                  <h2 className="text-xl font-bold text-white mb-4">Error Breakdown</h2>
                  <div className="space-y-3">
                    {Object.entries(dashboard.error_counts).map(([errorType, count]) => (
                      <div key={errorType} className="flex justify-between items-center p-3 bg-slate-700 rounded">
                        <span className="text-slate-300">{errorType}</span>
                        <span className="px-3 py-1 bg-blue-500 bg-opacity-30 text-blue-400 rounded text-sm font-medium">
                          {count} occurrences
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Recent Errors */}
              <div className="p-6 bg-slate-800 border border-slate-700 rounded-lg">
                <div className="flex justify-between items-center mb-4">
                  <h2 className="text-xl font-bold text-white">Recent Errors</h2>
                  <button
                    onClick={loadDashboard}
                    className="px-3 py-1 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded transition-all"
                  >
                    Refresh
                  </button>
                </div>

                {dashboard.recent_errors.length === 0 ? (
                  <p className="text-slate-400 text-center py-8">No recent errors - system is healthy!</p>
                ) : (
                  <div className="space-y-3">
                    {dashboard.recent_errors.map((err, idx) => (
                      <div key={idx} className="p-4 bg-slate-700 rounded border border-slate-600">
                        <div className="flex justify-between items-start mb-2">
                          <span className="font-mono text-sm text-red-400">{err.type}</span>
                          <span className="text-xs text-slate-500">
                            {new Date(err.timestamp).toLocaleTimeString()}
                          </span>
                        </div>
                        <p className="text-slate-300 text-sm mb-2">{err.message}</p>
                        {err.context && Object.keys(err.context).length > 0 && (
                          <details className="text-xs text-slate-400 cursor-pointer">
                            <summary className="hover:text-slate-300">Context</summary>
                            <pre className="mt-2 p-2 bg-slate-600 rounded text-slate-200 overflow-auto">
                              {JSON.stringify(err.context, null, 2)}
                            </pre>
                          </details>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Info Section */}
              <div className="mt-8 p-6 bg-slate-800 border border-slate-700 rounded-lg">
                <h3 className="text-lg font-bold text-white mb-4">About AI Error Recovery</h3>
                <ul className="space-y-2 text-slate-300 text-sm">
                  <li>✓ All errors are automatically logged and analyzed by our AI agent</li>
                  <li>✓ The system provides root cause analysis and fix suggestions</li>
                  <li>✓ Critical errors trigger immediate notifications</li>
                  <li>✓ Dashboard updates every 10 seconds</li>
                  <li>✓ Historical data helps identify patterns and recurring issues</li>
                </ul>
              </div>

              {/* Back to Dashboard */}
              <div className="mt-8">
                <Link
                  href="/dashboard"
                  className="inline-block px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded transition-all"
                >
                  ← Back to Dashboard
                </Link>
              </div>
            </>
          )}
        </div>
      </main>
    </ProtectedRoute>
  )
}
