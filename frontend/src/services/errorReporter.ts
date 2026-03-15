/**
 * Error Reporter Service
 * Sends frontend errors to backend for monitoring and AI analysis
 */

import api from './api'

interface ErrorReport {
  errorType: string
  message: string
  context?: Record<string, any>
  traceback?: string
  timestamp: string
  url: string
  userAgent: string
}

class ErrorReporter {
  private reportBacklog: ErrorReport[] = []
  private maxBacklogSize = 50

  /**
   * Report an error to the backend
   */
  async reportError(
    errorType: string,
    message: string,
    context?: Record<string, any>,
    traceback?: string
  ): Promise<void> {
    const report: ErrorReport = {
      errorType,
      message,
      context,
      traceback,
      timestamp: new Date().toISOString(),
      url: typeof window !== 'undefined' ? window.location.href : '',
      userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : '',
    }

    // Store in backlog
    this.reportBacklog.push(report)
    if (this.reportBacklog.length > this.maxBacklogSize) {
      this.reportBacklog.shift()
    }

    // Try to send to backend
    try {
      await api.post('/api/monitoring/errors/report', report)
    } catch (err) {
      console.error('Failed to report error to backend:', err)
      // Backlog is retained for later retry
    }
  }

  /**
   * Handle global error events
   */
  setupGlobalErrorHandlers() {
    // Handle uncaught errors
    if (typeof window !== 'undefined') {
      window.addEventListener('error', (event) => {
        this.reportError(
          'UncaughtError',
          event.message,
          {
            filename: event.filename,
            lineno: event.lineno,
            colno: event.colno,
            source: 'window.error'
          },
          event.error?.stack
        )
      })

      // Handle unhandled promise rejections
      window.addEventListener('unhandledrejection', (event) => {
        this.reportError(
          'UnhandledPromiseRejection',
          String(event.reason),
          { source: 'unhandledrejection' },
          event.reason?.stack
        )
      })
    }
  }

  /**
   * Get error backlog
   */
  getBacklog(): ErrorReport[] {
    return [...this.reportBacklog]
  }

  /**
   * Clear error backlog
   */
  clearBacklog() {
    this.reportBacklog = []
  }
}

// Global instance
export const errorReporter = new ErrorReporter()

// Setup global handlers on init
if (typeof window !== 'undefined') {
  errorReporter.setupGlobalErrorHandlers()
}
