'use client'

import React, { useEffect, useState } from 'react'
import Link from 'next/link'
import { optimizationAPI } from '@/services/api'
import { OptimizationRun, PromptVariation } from '@/types'

interface OptimizationDetailProps {
  runId: number
}

export default function OptimizationDetail({ runId }: OptimizationDetailProps) {
  const [run, setRun] = useState<OptimizationRun | null>(null)
  const [variations, setVariations] = useState<PromptVariation[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [autoRefresh, setAutoRefresh] = useState(true)

  useEffect(() => {
    loadData()
    
    let interval: NodeJS.Timeout | null = null
    if (autoRefresh) {
      interval = setInterval(loadData, 3000) // Refresh every 3 seconds
    }

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [autoRefresh])

  const loadData = async () => {
    try {
      const [runRes, varsRes] = await Promise.all([
        optimizationAPI.getRun(runId),
        optimizationAPI.getVariations(runId),
      ])

      setRun(runRes.data)
      setVariations(varsRes.data)
      setError(null)

      // Stop auto-refresh if optimization is complete
      if (runRes.data.status === 'completed' || runRes.data.status === 'failed') {
        setAutoRefresh(false)
      }
    } catch (err) {
      setError('Erro ao carregar dados da otimização')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleStopOptimization = async () => {
    if (confirm('Tem certeza que deseja parar a otimização?')) {
      try {
        await optimizationAPI.stopRun(runId)
        setAutoRefresh(false)
        loadData()
      } catch (err) {
        setError('Erro ao parar otimização')
        console.error(err)
      }
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'text-green-400'
      case 'running':
        return 'text-yellow-400'
      case 'failed':
        return 'text-red-400'
      default:
        return 'text-gray-400'
    }
  }

  if (loading) {
    return <div className="text-center py-12 text-gray-400">Carregando...</div>
  }

  if (!run) {
    return <div className="text-center py-12 text-red-400">Otimização não encontrada</div>
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-dark via-dark-secondary to-dark">
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="mb-8">
          <Link
            href={`/dashboard/projects/${run.project_id}`}
            className="text-accent hover:underline"
          >
            ← Voltar para Projeto
          </Link>
          <h1 className="text-4xl font-bold mt-4 mb-2">Otimização #{run.id}</h1>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-900 bg-opacity-50 border border-red-500 rounded-lg text-red-200">
            {error}
          </div>
        )}

        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-12">
          <div className="p-6 bg-dark-secondary border border-accent border-opacity-20 rounded-lg">
            <div className="text-gray-400 text-sm font-medium mb-2">Status</div>
            <div className={`text-2xl font-bold ${getStatusColor(run.status)}`}>
              {run.status}
            </div>
          </div>

          <div className="p-6 bg-dark-secondary border border-accent border-opacity-20 rounded-lg">
            <div className="text-gray-400 text-sm font-medium mb-2">Score</div>
            <div className="text-2xl font-bold text-accent">
              {run.best_score ? (run.best_score * 100).toFixed(1) + '%' : 'N/A'}
            </div>
          </div>

          <div className="p-6 bg-dark-secondary border border-accent border-opacity-20 rounded-lg">
            <div className="text-gray-400 text-sm font-medium mb-2">Iterações</div>
            <div className="text-2xl font-bold">{run.iterations}/5</div>
          </div>

          <div className="p-6 bg-dark-secondary border border-accent border-opacity-20 rounded-lg">
            <div className="text-gray-400 text-sm font-medium mb-2">Variações</div>
            <div className="text-2xl font-bold">{variations.length}</div>
          </div>
        </div>

        {/* Control Buttons */}
        {run.status === 'running' && (
          <div className="mb-12">
            <button
              onClick={handleStopOptimization}
              className="px-6 py-3 bg-red-900 text-red-200 font-bold rounded-lg hover:bg-red-800 transition-all"
            >
              ⏹ Parar Otimização
            </button>
          </div>
        )}

        {/* Initial Prompt */}
        <div className="mb-12 p-6 bg-dark-secondary border border-accent border-opacity-20 rounded-lg">
          <h2 className="text-xl font-bold mb-4">Prompt Inicial</h2>
          <div className="p-4 bg-dark border border-gray-600 rounded text-gray-300 whitespace-pre-wrap">
            {run.initial_prompt}
          </div>
        </div>

        {/* Best Prompt */}
        {run.best_prompt && (
          <div className="mb-12 p-6 bg-dark-secondary border border-accent border-opacity-20 rounded-lg">
            <h2 className="text-xl font-bold mb-4 text-accent">Melhor Prompt Encontrado</h2>
            <div className="p-4 bg-dark border border-accent border-opacity-40 rounded text-gray-300 whitespace-pre-wrap">
              {run.best_prompt}
            </div>
            <div className="mt-4 text-sm text-gray-400">
              Score: {(run.best_score! * 100).toFixed(1)}%
            </div>
          </div>
        )}

        {/* Optimization Results */}
        {run.results && run.results.length > 0 && (
          <div className="mb-12">
            <h2 className="text-2xl font-bold mb-6">Progresso por Iteração</h2>
            <div className="space-y-6">
              {run.results.map((result: any, idx: number) => (
                <div key={idx} className="p-6 bg-dark-secondary border border-accent border-opacity-20 rounded-lg">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-lg font-bold">Iteração {result.iteration + 1}</h3>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-accent">
                        {(result.best_score * 100).toFixed(1)}%
                      </div>
                    </div>
                  </div>

                  <div className="mb-4">
                    <div className="text-sm text-gray-400 mb-2">Variações nesta iteração:</div>
                    <div className="space-y-2">
                      {result.variations.map((variation: any, vidx: number) => (
                        <div
                          key={vidx}
                          className="p-3 bg-dark border border-gray-600 rounded text-sm"
                        >
                          <div className="flex justify-between mb-2">
                            <span className="text-gray-400">Variação {variation.index + 1}</span>
                            <span className="text-accent font-bold">
                              {(variation.score * 100).toFixed(1)}%
                            </span>
                          </div>
                          <p className="text-gray-400 text-xs">{variation.prompt}</p>
                        </div>
                      ))}
                    </div>
                  </div>

                  {result.best_in_iteration && (
                    <div className="p-3 bg-accent bg-opacity-10 border border-accent border-opacity-40 rounded text-sm">
                      <div className="font-bold text-accent mb-2">Melhor nesta iteração:</div>
                      <p className="text-gray-300 text-xs whitespace-pre-wrap">
                        {result.best_in_iteration}
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* All Variations */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-6">Todas as Variações</h2>
          {variations.length === 0 ? (
            <p className="text-gray-400">Nenhuma variação gerada ainda</p>
          ) : (
            <div className="space-y-3">
              {variations.map((variation) => (
                <div key={variation.id} className="p-4 bg-dark-secondary border border-accent border-opacity-20 rounded">
                  <div className="flex justify-between mb-2">
                    <div className="text-sm text-gray-400">
                      Iteração {variation.iteration} • ID: {variation.id}
                    </div>
                    <div className="text-accent font-bold">
                      {(variation.score * 100).toFixed(1)}%
                    </div>
                  </div>
                  <p className="text-gray-300 text-sm">{variation.prompt.substring(0, 200)}...</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
