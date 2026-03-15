import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import '../styles/globals.css'
import { AuthProvider } from '@/context/AuthContext'
import { ErrorReporterProvider } from '@/context/ErrorReporterProvider'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Prompt Optimization Platform',
  description: 'Automatically optimize your prompts with an intelligent optimization loop',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ErrorReporterProvider>
          <AuthProvider>
            {children}
          </AuthProvider>
        </ErrorReporterProvider>
      </body>
    </html>
  )
}
