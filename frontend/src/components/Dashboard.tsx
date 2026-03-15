'use client'

import React, { useEffect, useState } from 'react'
import Link from 'next/link'
import { projectsAPI } from '@/services/api'
import { useAuth } from '@/context/AuthContext'
import { Project } from '@/types'

export default function Dashboard() {
  const { user, logout } = useAuth()
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showNewProjectForm, setShowNewProjectForm] = useState(false)
  const [newProject, setNewProject] = useState({ name: '', description: '' })

  useEffect(() => {
    loadProjects()
  }, [])

  const loadProjects = async () => {
    try {
      setLoading(true)
      const response = await projectsAPI.list()
      setProjects(response.data)
      setError(null)
    } catch (err) {
      setError('Erro ao carregar projetos')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateProject = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await projectsAPI.create(newProject)
      setNewProject({ name: '', description: '' })
      setShowNewProjectForm(false)
      loadProjects()
    } catch (err) {
      setError('Erro ao criar projeto')
      console.error(err)
    }
  }

  const handleDeleteProject = async (id: number) => {
    if (confirm('Tem certeza que deseja deletar este projeto?')) {
      try {
        await projectsAPI.delete(id)
        loadProjects()
      } catch (err) {
        setError('Erro ao deletar projeto')
        console.error(err)
      }
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-dark via-dark-secondary to-dark">
      {/* Top Bar */}
      <div className="border-b border-accent border-opacity-20 px-4 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div>
            <h2 className="text-xl font-bold text-white">Prompt Optimization Platform</h2>
          </div>
          <div className="flex items-center gap-6">
            {user && (
              <div className="text-sm text-slate-400">
                Logged in as <span className="font-semibold text-slate-200">{user.username || user.email}</span>
              </div>
            )}
            <Link
              href="/dashboard/monitoring"
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition-all text-sm font-medium"
            >
              System Monitoring
            </Link>
            {user && (
              <button
                onClick={() => {
                  logout()
                  window.location.href = '/'
                }}
                className="px-4 py-2 border border-slate-600 text-slate-300 rounded hover:bg-slate-700 transition-all text-sm font-medium"
              >
                Logout
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-5xl font-bold mb-4 glow">
            Meus <span className="text-accent">Projetos</span>
          </h1>
          <p className="text-gray-400 text-lg">
            Gerencie suas otimizações de prompts
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-900 bg-opacity-50 border border-red-500 rounded-lg text-red-200">
            {error}
          </div>
        )}

        {/* New Project Button */}
        <div className="mb-8">
          <button
            onClick={() => setShowNewProjectForm(!showNewProjectForm)}
            className="px-6 py-3 bg-accent text-dark font-bold rounded-lg hover:bg-opacity-90 transition-all"
          >
            + Novo Projeto
          </button>
        </div>

        {/* New Project Form */}
        {showNewProjectForm && (
          <div className="mb-12 p-6 bg-dark-secondary border border-accent border-opacity-30 rounded-lg">
            <h2 className="text-2xl font-bold mb-6">Criar Novo Projeto</h2>
            <form onSubmit={handleCreateProject} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Nome do Projeto</label>
                <input
                  type="text"
                  required
                  value={newProject.name}
                  onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
                  className="w-full px-4 py-2 bg-dark border border-accent border-opacity-20 rounded text-white placeholder-gray-500 focus:outline-none focus:border-opacity-100"
                  placeholder="Ex: Otimização de Customer Service"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Descrição</label>
                <textarea
                  value={newProject.description}
                  onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
                  className="w-full px-4 py-2 bg-dark border border-accent border-opacity-20 rounded text-white placeholder-gray-500 focus:outline-none focus:border-opacity-100"
                  placeholder="Descrição do projeto..."
                  rows={3}
                />
              </div>
              <div className="flex gap-4">
                <button
                  type="submit"
                  className="px-6 py-2 bg-accent text-dark font-bold rounded hover:bg-opacity-90 transition-all"
                >
                  Criar
                </button>
                <button
                  type="button"
                  onClick={() => setShowNewProjectForm(false)}
                  className="px-6 py-2 border border-accent text-accent rounded hover:bg-accent hover:text-dark transition-all"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Projects Grid */}
        {loading ? (
          <div className="text-center py-12">
            <p className="text-gray-400">Carregando projetos...</p>
          </div>
        ) : projects.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-400 text-lg">Nenhum projeto criado ainda</p>
            <p className="text-gray-500 mt-2">Clique em &quot;Novo Projeto&quot; para começar</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <div
                key={project.id}
                className="p-6 bg-dark-secondary border border-accent border-opacity-20 rounded-lg hover:border-opacity-50 transition-all hover:shadow-lg hover:shadow-accent/20"
              >
                <h3 className="text-xl font-bold mb-2">{project.name}</h3>
                <p className="text-gray-400 text-sm mb-4">{project.description || 'Sem descrição'}</p>
                
                <div className="mb-4 text-xs text-gray-500">
                  Criado em: {new Date(project.created_at).toLocaleDateString('pt-BR')}
                </div>

                <div className="flex gap-2">
                  <Link
                    href={`/dashboard/projects/${project.id}`}
                    className="flex-1 px-4 py-2 bg-accent text-dark font-bold rounded text-center hover:bg-opacity-90 transition-all"
                  >
                    Abrir
                  </Link>
                  <button
                    onClick={() => handleDeleteProject(project.id)}
                    className="px-4 py-2 border border-red-500 text-red-400 rounded hover:bg-red-900 hover:bg-opacity-20 transition-all"
                  >
                    Deletar
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  )
}
