'use client'

import React, { useEffect, useRef } from 'react'
import Link from 'next/link'
import * as THREE from 'three'
import Canvas3D from './Canvas3D'

export default function LandingPage() {
  return (
    <main className="w-full min-h-screen bg-gradient-to-b from-dark via-dark-secondary to-dark overflow-hidden">
      {/* 3D Canvas Background */}
      <Canvas3D />

      {/* Content Overlay */}
      <div className="relative z-10 w-full h-screen flex items-center justify-center">
        <div className="text-center px-4 md:px-8 lg:px-16 fade-in-up">
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold mb-6 glow">
            Prompt <span className="text-accent">Optimization</span>
          </h1>
          
          <p className="text-lg md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Stop manually editing prompts. Let AI find the perfect prompt automatically.
          </p>

          <div className="flex flex-col md:flex-row gap-4 justify-center mb-12">
            <Link
              href="/dashboard"
              className="px-8 py-3 bg-accent text-dark font-bold rounded-lg hover:bg-opacity-90 transition-all transform hover:scale-105 inline-block"
            >
              Dashboard
            </Link>
            <button className="px-8 py-3 border-2 border-accent text-accent font-bold rounded-lg hover:bg-accent hover:text-dark transition-all">
              Learn More
            </button>
          </div>

          {/* Feature Highlights */}
          <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            <div className="p-6 bg-dark-secondary bg-opacity-50 backdrop-blur-md rounded-lg border border-accent border-opacity-20 hover:border-opacity-50 transition-all">
              <div className="text-3xl mb-3">📝</div>
              <h3 className="text-xl font-bold mb-2">Define Signature</h3>
              <p className="text-gray-400">Specify your task contract with clear inputs and outputs</p>
            </div>

            <div className="p-6 bg-dark-secondary bg-opacity-50 backdrop-blur-md rounded-lg border border-accent border-opacity-20 hover:border-opacity-50 transition-all">
              <div className="text-3xl mb-3">⚙️</div>
              <h3 className="text-xl font-bold mb-2">Run Program</h3>
              <p className="text-gray-400">Execute your optimization logic with training data</p>
            </div>

            <div className="p-6 bg-dark-secondary bg-opacity-50 backdrop-blur-md rounded-lg border border-accent border-opacity-20 hover:border-opacity-50 transition-all">
              <div className="text-3xl mb-3">📊</div>
              <h3 className="text-xl font-bold mb-2">Measure Success</h3>
              <p className="text-gray-400">Define metrics to automatically evaluate results</p>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2 z-10 animate-bounce">
        <div className="text-accent text-2xl">↓</div>
      </div>
    </main>
  )
}
