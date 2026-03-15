import Dashboard from '@/components/Dashboard'
import { ProtectedRoute } from '@/components/ProtectedRoute'

export const metadata = {
  title: 'Dashboard - Prompt Optimization',
  description: 'Gerencie seus projetos de otimização de prompts',
}

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  )
}
