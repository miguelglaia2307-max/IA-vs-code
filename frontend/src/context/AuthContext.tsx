'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'
import { User, AuthContextType } from '@/types'
import api from '@/services/api'

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  // Load token from localStorage on mount
  useEffect(() => {
    const savedToken = localStorage.getItem('token')
    if (savedToken) {
      setToken(savedToken)
      // Note: JWT token is now handled by axios interceptor in api.ts
      // No need to manually set headers here
      
      // Try to fetch current user
      fetchCurrentUser(savedToken)
    } else {
      setLoading(false)
    }
  }, [])

  const fetchCurrentUser = async (authToken: string) => {
    try {
      const response = await api.get('/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      })
      setUser(response.data)
    } catch (error) {
      console.error('Failed to fetch current user:', error)
      localStorage.removeItem('token')
      setToken(null)
    } finally {
      setLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    try {
      setLoading(true)
      const response = await api.post('/api/auth/login', {
        email,
        password
      })
      const { access_token, user: userData } = response.data
      
      setToken(access_token)
      setUser(userData)
      localStorage.setItem('token', access_token)
      // Note: JWT token is now handled by axios interceptor in api.ts
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const register = async (email: string, username: string, password: string) => {
    try {
      setLoading(true)
      const response = await api.post('/api/auth/register', {
        email,
        username,
        password
      })
      const userData = response.data
      setUser(userData)
      
      // Auto-login after registration
      await login(email, password)
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('token')
    // Note: Authorization header will be removed automatically by axios interceptor
    // since token is no longer in localStorage
  }

  const value: AuthContextType = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    isAuthenticated: !!token && !!user
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
