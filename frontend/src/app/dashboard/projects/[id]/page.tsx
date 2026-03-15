'use client'

import ProjectDetail from '@/components/ProjectDetail'
import { ProtectedRoute } from '@/components/ProtectedRoute'
import { useParams } from 'next/navigation'

export default function ProjectPage() {
  const params = useParams()
  const projectId = parseInt(params.id as string)

  return (
    <ProtectedRoute>
      <ProjectDetail projectId={projectId} />
    </ProtectedRoute>
  )
}
