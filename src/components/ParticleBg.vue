<template>
  <canvas ref="canvas" class="fixed inset-0 pointer-events-none z-0 opacity-25"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'

const canvas = ref(null)
let scene, camera, renderer, particles, glow
let animationId
let mouseX = 0, mouseY = 0
let mode = 'normal' // 'normal' | 'warp' | 'dna'
const effectTimeoutIds = []
const effectIntervalIds = []

const particleCount = 60

onMounted(() => {
  initThree()
  animate()
  window.addEventListener('resize', handleResize)
  window.addEventListener('mousemove', handleMouseMove)
  window.addEventListener('touchmove', handleTouchMove)
})

onUnmounted(() => {
  cancelAnimationFrame(animationId)
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('touchmove', handleTouchMove)
  effectTimeoutIds.forEach(clearTimeout)
  effectIntervalIds.forEach(clearInterval)
  if (renderer) renderer.dispose()
})

function handleMouseMove(e) {
  mouseX = (e.clientX / window.innerWidth) * 2 - 1
  mouseY = -(e.clientY / window.innerHeight) * 2 + 1
}

function handleTouchMove(e) {
  if (e.touches.length > 0) {
    mouseX = (e.touches[0].clientX / window.innerWidth) * 2 - 1
    mouseY = -(e.touches[0].clientY / window.innerHeight) * 2 + 1
  }
}

function initThree() {
  const width = window.innerWidth
  const height = window.innerHeight

  scene = new THREE.Scene()
  scene.fog = new THREE.FogExp2(0x0d0d0d, 0.003)

  camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)
  camera.position.z = 50

  renderer = new THREE.WebGLRenderer({ canvas: canvas.value, alpha: true, antialias: true })
  renderer.setSize(width, height)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5))

  const positions = new Float32Array(particleCount * 3)
  const velocities = []

  for (let i = 0; i < particleCount; i++) {
    positions[i * 3]     = (Math.random() - 0.5) * 80
    positions[i * 3 + 1] = (Math.random() - 0.5) * 50
    positions[i * 3 + 2] = (Math.random() - 0.5) * 20

    const angle = Math.random() * Math.PI * 2
    const speed = Math.random() * 0.05 + 0.03
    velocities.push({
      x: Math.cos(angle) * speed * 0.3,
      y: speed,
      z: Math.sin(angle) * speed * 0.1,
    })
  }

  const geometry = new THREE.BufferGeometry()
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3))

  const material = new THREE.PointsMaterial({
    size: 1.5,
    color: 0x10b981,
    transparent: true,
    opacity: 0.5,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  })

  particles = new THREE.Points(geometry, material)
  particles.userData = { velocities }
  scene.add(particles)

  const glowMaterial = new THREE.MeshBasicMaterial({ color: 0x10b981, transparent: true, opacity: 0.15 })
  glow = new THREE.Mesh(new THREE.SphereGeometry(3, 16, 16), glowMaterial)
  glow.position.set(0, 0, -5)
  scene.add(glow)
}

function animate() {
  animationId = requestAnimationFrame(animate)
  const time = Date.now() * 0.001

  if (particles) {
    const pos  = particles.geometry.attributes.position.array
    const vels = particles.userData.velocities

    if (mode === 'normal') {
      for (let i = 0; i < particleCount; i++) {
        const dx   = mouseX * 30 - pos[i * 3]
        const dy   = mouseY * 20 - pos[i * 3 + 1]
        const dist = Math.sqrt(dx * dx + dy * dy)
        if (dist < 15) {
          pos[i * 3]     += dx * 0.002
          pos[i * 3 + 1] += dy * 0.002
        }

        pos[i * 3]     += vels[i].x
        pos[i * 3 + 1] += vels[i].y * 2
        pos[i * 3 + 2] += vels[i].z

        if (pos[i * 3 + 1] > 25) {
          pos[i * 3]     = (Math.random() - 0.5) * 80
          pos[i * 3 + 1] = -25
          pos[i * 3 + 2] = (Math.random() - 0.5) * 20
        }

        if (pos[i * 3] > 45)  pos[i * 3] = -45
        if (pos[i * 3] < -45) pos[i * 3] = 45
      }
      particles.geometry.attributes.position.needsUpdate = true
    }

    if (mode === 'warp') {
      for (let i = 0; i < particleCount; i++) {
        pos[i * 3]     += vels[i].x
        pos[i * 3 + 1] += vels[i].y * 0.2
        pos[i * 3 + 2] += vels[i].z

        if (pos[i * 3 + 2] > 60) {
          pos[i * 3]     = (Math.random() - 0.5) * 80
          pos[i * 3 + 1] = (Math.random() - 0.5) * 50
          pos[i * 3 + 2] = -20
        }
      }
      particles.geometry.attributes.position.needsUpdate = true
    }
  }

  if (glow) {
    glow.position.x += (mouseX * 25 - glow.position.x) * 0.08
    glow.position.y += (mouseY * 15 - glow.position.y) * 0.08
    glow.material.opacity = 0.1 + Math.sin(time * 2) * 0.05
  }

  camera.position.x += Math.sin(time * 0.3) * 0.01
  camera.position.y += Math.cos(time * 0.2) * 0.005

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

function warp() {
  if (mode !== 'normal') return
  mode = 'warp'

  const pos  = particles.geometry.attributes.position.array
  const vels = particles.userData.velocities

  vels.forEach((v, i) => {
    v._origX = v.x
    v._origY = v.y
    v._origZ = v.z
    v.z = Math.random() * 5 + 3
    v.x = (pos[i * 3]     / 80) * 0.5
    v.y = (pos[i * 3 + 1] / 50) * 0.5
  })

  particles.material.color.set(0x00ffff)
  particles.material.opacity = 0.9
  particles.material.size = 3

  const resetTimeoutId = setTimeout(() => {
    vels.forEach(v => { v.x = v._origX; v.y = v._origY; v.z = v._origZ })
    for (let i = 0; i < particleCount; i++) {
      pos[i * 3 + 2] = (Math.random() - 0.5) * 20
    }
    particles.material.color.set(0x10b981)
    particles.material.opacity = 0.5
    particles.material.size = 1.5
    mode = 'normal'
  }, 1800)
  effectTimeoutIds.push(resetTimeoutId)
}

function dna() {
  if (mode !== 'normal') return
  mode = 'dna'

  const pos = particles.geometry.attributes.position.array

  const originals = Array.from({ length: particleCount }, (_, i) => ({
    x: pos[i * 3], y: pos[i * 3 + 1], z: pos[i * 3 + 2],
  }))

  const targets = Array.from({ length: particleCount }, (_, i) => {
    const t      = (i / particleCount) * Math.PI * 6 - Math.PI * 3
    const strand = i % 2 === 0 ? 1 : -1
    return {
      x: Math.cos(t + strand * Math.PI) * 8,
      y: t * 2.5,
      z: Math.sin(t + strand * Math.PI) * 8,
    }
  })

  particles.material.color.set(0x00ffff)
  particles.material.opacity = 0.85
  particles.material.size = 2.5

  const formInterval = setInterval(() => {
    for (let i = 0; i < particleCount; i++) {
      pos[i * 3]     += (targets[i].x - pos[i * 3])     * 0.1
      pos[i * 3 + 1] += (targets[i].y - pos[i * 3 + 1]) * 0.1
      pos[i * 3 + 2] += (targets[i].z - pos[i * 3 + 2]) * 0.1
    }
    particles.geometry.attributes.position.needsUpdate = true
  }, 16)
  effectIntervalIds.push(formInterval)

  const spinTimeoutId = setTimeout(() => {
    clearInterval(formInterval)
    let angle = 0
    const spinInterval = setInterval(() => {
      angle += 0.02
      for (let i = 0; i < particleCount; i++) {
        const t      = (i / particleCount) * Math.PI * 6 - Math.PI * 3
        const strand = i % 2 === 0 ? 1 : -1
        pos[i * 3]     = Math.cos(t + strand * Math.PI + angle) * 8
        pos[i * 3 + 2] = Math.sin(t + strand * Math.PI + angle) * 8
      }
      particles.geometry.attributes.position.needsUpdate = true
    }, 16)
    effectIntervalIds.push(spinInterval)

    const restoreTimeoutId = setTimeout(() => {
      clearInterval(spinInterval)
      let steps = 0
      const restoreInterval = setInterval(() => {
        steps++
        for (let i = 0; i < particleCount; i++) {
          pos[i * 3]     += (originals[i].x - pos[i * 3])     * 0.07
          pos[i * 3 + 1] += (originals[i].y - pos[i * 3 + 1]) * 0.07
          pos[i * 3 + 2] += (originals[i].z - pos[i * 3 + 2]) * 0.07
        }
        particles.geometry.attributes.position.needsUpdate = true
        if (steps > 60) {
          clearInterval(restoreInterval)
          particles.material.color.set(0x10b981)
          particles.material.opacity = 0.5
          particles.material.size = 1.5
          mode = 'normal'
        }
      }, 16)
      effectIntervalIds.push(restoreInterval)
    }, 2500)
    effectTimeoutIds.push(restoreTimeoutId)
  }, 1000)
  effectTimeoutIds.push(spinTimeoutId)
}

defineExpose({ warp, dna })
</script>
