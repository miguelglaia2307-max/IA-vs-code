'use client'

import React, { useEffect, useRef } from 'react'
import * as THREE from 'three'

export default function Canvas3D() {
  const containerRef = useRef<HTMLDivElement>(null)
  const sceneRef = useRef<THREE.Scene | null>(null)
  const cameraRef = useRef<THREE.PerspectiveCamera | null>(null)
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null)
  const particlesRef = useRef<THREE.Points | null>(null)

  useEffect(() => {
    if (!containerRef.current) return

    // Scene setup
    const scene = new THREE.Scene()
    sceneRef.current = scene

    // Camera setup
    const width = window.innerWidth
    const height = window.innerHeight
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)
    camera.position.z = 30
    cameraRef.current = camera

    // Renderer setup
    const canvas = document.createElement('canvas')
    containerRef.current.appendChild(canvas)
    const renderer = new THREE.WebGLRenderer({ 
      canvas, 
      antialias: true, 
      alpha: true,
      powerPreference: 'high-performance'
    })
    renderer.setSize(width, height)
    renderer.setClearColor(0x000000, 0)
    renderer.setPixelRatio(window.devicePixelRatio)
    rendererRef.current = renderer

    // Lighting
    const light = new THREE.PointLight(0x00d9ff, 1)
    light.position.set(10, 10, 10)
    scene.add(light)

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.3)
    scene.add(ambientLight)

    // Create particle system
    const particleCount = 1000
    const particlesGeometry = new THREE.BufferGeometry()
    const positions = new Float32Array(particleCount * 3)
    const velocities = new Float32Array(particleCount * 3)

    for (let i = 0; i < particleCount; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 100
      positions[i * 3 + 1] = (Math.random() - 0.5) * 100
      positions[i * 3 + 2] = (Math.random() - 0.5) * 100

      velocities[i * 3] = (Math.random() - 0.5) * 0.5
      velocities[i * 3 + 1] = (Math.random() - 0.5) * 0.5
      velocities[i * 3 + 2] = (Math.random() - 0.5) * 0.5
    }

    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
    particlesGeometry.setAttribute('velocity', new THREE.BufferAttribute(velocities, 3))

    const particlesMaterial = new THREE.PointsMaterial({
      color: 0x00d9ff,
      size: 0.5,
      sizeAttenuation: true,
      transparent: true,
      opacity: 0.6,
    })

    const particles = new THREE.Points(particlesGeometry, particlesMaterial)
    scene.add(particles)
    particlesRef.current = particles

    // Create some floating geometries
    const geometries = [
      new THREE.IcosahedronGeometry(5, 4),
      new THREE.OctahedronGeometry(5),
      new THREE.TetrahedronGeometry(5),
    ]

    geometries.forEach((geom, index) => {
      const material = new THREE.MeshPhongMaterial({
        color: new THREE.Color().setHSL(0.5, 1, 0.5 + index * 0.1),
        wireframe: true,
        emissive: 0x00d9ff,
        emissiveIntensity: 0.3,
      })

      const mesh = new THREE.Mesh(geom, material)
      mesh.position.x = (index - 1) * 20
      mesh.position.z = -10
      mesh.rotation.x = Math.random() * Math.PI
      mesh.rotation.y = Math.random() * Math.PI
      scene.add(mesh)
    })

    // Handle window resize
    const handleResize = () => {
      const newWidth = window.innerWidth
      const newHeight = window.innerHeight
      camera.aspect = newWidth / newHeight
      camera.updateProjectionMatrix()
      renderer.setSize(newWidth, newHeight)
    }

    window.addEventListener('resize', handleResize)

    // Animation loop
    let animationId: number
    const animate = () => {
      animationId = requestAnimationFrame(animate)

      // Rotate and move particles
      const positions = particlesGeometry.attributes.position.array as Float32Array
      const velocities = particlesGeometry.attributes.velocity.array as Float32Array

      for (let i = 0; i < particleCount; i++) {
        positions[i * 3] += velocities[i * 3]
        positions[i * 3 + 1] += velocities[i * 3 + 1]
        positions[i * 3 + 2] += velocities[i * 3 + 2]

        // Wrap around
        if (positions[i * 3] > 50) positions[i * 3] = -50
        if (positions[i * 3] < -50) positions[i * 3] = 50
        if (positions[i * 3 + 1] > 50) positions[i * 3 + 1] = -50
        if (positions[i * 3 + 1] < -50) positions[i * 3 + 1] = 50
        if (positions[i * 3 + 2] > 50) positions[i * 3 + 2] = -50
        if (positions[i * 3 + 2] < -50) positions[i * 3 + 2] = 50
      }
      particlesGeometry.attributes.position.needsUpdate = true

      // Rotate meshes
      scene.children.forEach((child) => {
        if (child instanceof THREE.Mesh) {
          child.rotation.x += 0.001
          child.rotation.y += 0.002
        }
      })

      renderer.render(scene, camera)
    }

    animate()

    return () => {
      window.removeEventListener('resize', handleResize)
      cancelAnimationFrame(animationId)
      renderer.dispose()
      containerRef.current?.removeChild(canvas)
    }
  }, [])

  return (
    <div
      ref={containerRef}
      className="absolute top-0 left-0 w-full h-screen overflow-hidden"
      style={{ 
        background: 'linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%)'
      }}
    />
  )
}
