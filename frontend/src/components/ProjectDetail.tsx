'use client'

import React, { useEffect, useState } from 'react'
import Link from 'next/link'
import {
  projectsAPI,
  signaturesAPI,
  datasetsAPI,
  metricsAPI,
  programsAPI,
  optimizationAPI,
} from '@/services/api'
import { Project, Signature, Dataset, Metric, Program, OptimizationRun } from '@/types'

interface ProjectDetailProps {
  projectId: number
}

export default function ProjectDetail({ projectId }: ProjectDetailProps) {
  const [project, setProject] = useState<Project | null>(null)
  const [signatures, setSignatures] = useState<Signature[]>([])
  const [datasets, setDatasets] = useState<Dataset[]>([])
  const [metrics, setMetrics] = useState<Metric[]>([])
  const [programs, setPrograms] = useState<Program[]>([])
  const [runs, setRuns] = useState<OptimizationRun[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'overview' | 'optimizations'>('overview')

  useEffect(() => {
    loadProjectData()
  }, [projectId])

  const loadProjectData = async () => {
    try {
      setLoading(true)
      const [projectRes, sigsRes, datsRes, metricsRes, progsRes, runsRes] = await Promise.all([
        projectsAPI.get(projectId),
        signaturesAPI.list(projectId),
        datasetsAPI.list(projectId),
        metricsAPI.list(projectId),
        programsAPI.list(projectId),
        optimizationAPI.listRuns(projectId),
      ])

      setProject(projectRes.data)
      setSignatures(sigsRes.data)
      setDatasets(datsRes.data)
      setMetrics(metricsRes.data)
      setPrograms(progsRes.data)
      setRuns(runsRes.data)
      setError(null)
    } catch (err) {
      setError('Erro ao carregar dados do projeto')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleStartOptimization = async () => {
    if (signatures.length === 0 || datasets.length === 0 || metrics.length === 0 || programs.length === 0) {
      setError('Você precisa de Signature, Dataset, Metric e Program para iniciar uma otimização')
      return
    }

    const initialPrompt = prompt('Digite o prompt inicial para otimizar:')
    if (!initialPrompt) return

    try {
      await optimizationAPI.startRun({
        project_id: projectId,
        signature_id: signatures[0].id,
        program_id: programs[0].id,
        metric_id: metrics[0].id,
        dataset_id: datasets[0].id,
        initial_prompt: initialPrompt,
      })
      loadProjectData()
    } catch (err) {
      setError('Erro ao iniciar otimização')
      console.error(err)
    }
  }

  if (loading) {
    return <div className="text-center py-12 text-gray-400">Carregando...</div>
  }

  if (!project) {
    return <div className="text-center py-12 text-red-400">Projeto não encontrado</div>
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-dark via-dark-secondary to-dark">
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="mb-8">
          <Link href="/dashboard" className="text-accent hover:underline">
            ← Voltar
          </Link>
          <h1 className="text-4xl font-bold mt-4 mb-2">{project.name}</h1>
          <p className="text-gray-400">{project.description}</p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-900 bg-opacity-50 border border-red-500 rounded-lg text-red-200">
            {error}
          </div>
        )}

        {/* Tabs */}
        <div className="flex gap-4 mb-8 border-b border-accent border-opacity-20">
          <button
            onClick={() => setActiveTab('overview')}
            className={`px-6 py-3 font-bold transition-all ${
              activeTab === 'overview'
                ? 'text-accent border-b-2 border-accent'
                : 'text-gray-400 hover:text-accent'
            }`}
          >
            Configuração
          </button>
          <button
            onClick={() => setActiveTab('optimizations')}
            className={`px-6 py-3 font-bold transition-all ${
              activeTab === 'optimizations'
                ? 'text-accent border-b-2 border-accent'
                : 'text-gray-400 hover:text-accent'
            }`}
          >
            Otimizações ({runs.length})
          </button>
        </div>

        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div>
            <button
              onClick={handleStartOptimization}
              className="mb-12 px-6 py-3 bg-accent text-dark font-bold rounded-lg hover:bg-opacity-90 transition-all"
            >
              ▶ Iniciar Nova Otimização
            </button>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Signatures */}
              <div className="p-6 bg-dark-secondary border border-accent border-opacity-20 rounded-lg">
                <h3 className="text-xl font-bold mb-4">
                  Signatures ({signatures.length})
                </h3>
                {signatures.length === 0 ? (
                  <p className="text-gray-400">Nenhuma signature criada</p>
                ) : (
                  <ul className="space-y-2">
                    {signatures.map((sig) => (
                      <li key={sig.id} className="text-gray-300">
                        • {sig.name}
                      </li>
                    ))}
                  </ul>
                )}
              </div>

              {/* Datasets */}
              <div className="p-6 bg-dark-secondary border border-accent border-opacity-20 rounded-lg">
                <h3 className="text-xl font-bold mb-4">Datasets ({datasets.length})</h3>
                {datasets.length === 0 ? (
                  <p className="text-gray-400">Nenhum dataset criado</p>
                ) : (
                  <ul className="space-y-2">
                    {datasets.map((ds) => (
                      <li key={ds.id} className="text-gray-300">
                        • {ds.name} ({ds.examples.length} exemplos)
                      </li>
                    ))}
                  </ul>
                )}
              </div>

              {/* Metrics */}
              <div className="p-6 bg-dark-secondary border border-accent border-opacity-20 rounded-lg">
                <h3 className="text-xl font-bold mb-4">Métricas ({metrics.length})</h3>
                {metrics.length === 0 ? (
                  <p className="text-gray-400">Nenhuma métrica criada</p>
                ) : (
                  <ul className="space-y-2">
                    {metrics.map((met) => (
                      <li key={met.id} className="text-gray-300">
                        • {met.name} ({met.metric_type})
                      </li>
                    ))}
                  </ul>
                )}
              </div>

              {/* Programs */}
              <div className="p-6 bg-dark-secondary border border-accent border-opacity-20 rounded-lg">
                <h3 className="text-xl font-bold mb-4">Programs ({programs.length})</h3>
                {programs.length === 0 ? (
                  <p className="text-gray-400">Nenhum program criado</p>
                ) : (
                  <ul className="space-y-2">
                    {programs.map((prog) => (
                      <li key={prog.id} className="text-gray-300">
                        • {prog.name}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Optimizations Tab */}
        {activeTab === 'optimizations' && (
          <div>
            {runs.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-gray-400 text-lg">Nenhuma otimização iniciada</p>
              </div>
            ) : (
              <div className="space-y-6">
                {runs.map((run) => (
                  <Link
                    key={run.id}
                    href={`/dashboard/optimizations/${run.id}`}
                    className="block p-6 bg-dark-secondary border border-accent border-opacity-20 rounded-lg hover:border-opacity-50 transition-all"
                  >
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h4 className="text-lg font-bold">Otimização #{run.id}</h4>
                        <p className="text-gray-400 text-sm mt-1">
                          Status: <span className={`font-bold ${
                            run.status === 'completed' ? 'text-green-400' :
                            run.status === 'running' ? 'text-yellow-400' :
                            run.status === 'failed' ? 'text-red-400' :
                            'text-gray-400'
                          }`}>
                            {run.status}
                          </span>
                        </p>
                      </div>
                      {run.best_score && (
                        <div className="text-right">
                          <div className="text-2xl font-bold text-accent">
                            {(run.best_score * 100).toFixed(1)}%
                          </div>
                          <div className="text-gray-400 text-sm">Score</div>
                        </div>
                      )}
                    </div>
                    <p className="text-gray-300 text-sm mb-2">
                      Iterações: {run.iterations}/5
                    </p>
                    <p className="text-gray-400 text-xs truncate">
                      Prompt: {run.initial_prompt.substring(0, 80)}...
                    </p>
                  </Link>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
