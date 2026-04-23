<template>
  <canvas ref="canvas" class="absolute inset-0 w-full h-full pointer-events-none"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'

const canvas = ref(null)
let scene, camera, renderer, particles, positions, velocities
let animationId
const particleCount = 50

onMounted(() => {
  initThree()
  animate()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  cancelAnimationFrame(animationId)
  window.removeEventListener('resize', handleResize)
  if (renderer) renderer.dispose()
})

function initThree() {
  const width = window.innerWidth
  const height = window.innerHeight
  
  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)
  camera.position.z = 50
  
  renderer = new THREE.WebGLRenderer({ 
    canvas: canvas.value, 
    alpha: true,
    antialias: true 
  })
  renderer.setSize(width, height)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  
  positions = new Float32Array(particleCount * 3)
  velocities = []
  
  for (let i = 0; i < particleCount; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 80
    positions[i * 3 + 1] = (Math.random() - 0.5) * 60
    positions[i * 3 + 2] = (Math.random() - 0.5) * 20
    velocities.push({
      x: (Math.random() - 0.5) * 0.02,
      y: Math.random() * 0.05 + 0.02,
      z: (Math.random() - 0.5) * 0.01
    })
  }
  
  const geometry = new THREE.BufferGeometry()
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))
  
  const material = new THREE.PointsMaterial({
    size: 3,
    color: 0xff9f43,
    transparent: true,
    opacity: 0.6,
    blending: THREE.AdditiveBlending,
    depthWrite: false
  })
  
  particles = new THREE.Points(geometry, material)
  scene.add(particles)
}

function animate() {
  animationId = requestAnimationFrame(animate)
  
  if (particles) {
    const pos = particles.geometry.attributes.position.array
    
    for (let i = 0; i < particleCount; i++) {
      pos[i * 3] += velocities[i].x
      pos[i * 3 + 1] += velocities[i].y
      pos[i * 3 + 2] += velocities[i].z
      
      // Reset particle if it goes too high
      if (pos[i * 3 + 1] > 30) {
        pos[i * 3] = (Math.random() - 0.5) * 80
        pos[i * 3 + 1] = -30
        pos[i * 3 + 2] = (Math.random() - 0.5) * 20
      }
    }
    
    particles.geometry.attributes.position.needsUpdate = true
  }
  
  renderer.render(scene, camera)
}

function handleResize() {
  if (!camera || !renderer) return
  
  const width = window.innerWidth
  const height = window.innerHeight
  
  camera.aspect = width / height
  camera.updateProjectionMatrix()
  renderer.setSize(width, height)
}
</script>