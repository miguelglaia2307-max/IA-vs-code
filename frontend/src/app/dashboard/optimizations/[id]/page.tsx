'use client'

import OptimizationDetail from '@/components/OptimizationDetail'
import { ProtectedRoute } from '@/components/ProtectedRoute'
import { useParams } from 'next/navigation'

export default function OptimizationPage() {
  const params = useParams()
  const runId = parseInt(params.id as string)

  return (
    <ProtectedRoute>
      <OptimizationDetail runId={runId} />
    </ProtectedRoute>
  )
}
