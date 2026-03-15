'use client'

import React, { useEffect } from 'react'
import { errorReporter } from '@/services/errorReporter'

export function ErrorReporterProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Initialize error reporting on client side
    errorReporter.setupGlobalErrorHandlers()
    console.log('[ErrorReporter] Global error handlers initialized')
  }, [])

  return <>{children}</>
}
