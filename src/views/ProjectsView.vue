<template>
  <div class="projects-view min-h-screen py-32 px-6">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-16">
        <h1 
          class="re8-heading text-4xl md:text-5xl mb-6"
          v-motion
          :initial="{ opacity: 0, y: 20 }"
          :enter="{ opacity: 1, y: 0 }"
        >
          Notable Works
        </h1>
        <p 
          class="font-outfit text-re8-text-muted text-lg max-w-2xl mx-auto"
          v-motion
          :initial="{ opacity: 0, y: 20 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 200 } }"
        >
          {{ projectsData.intro }}
        </p>
      </div>

      <!-- Projects Grid -->
      <div class="grid md:grid-cols-2 gap-8">
        <div 
          v-for="(project, index) in projectsData.projects" 
          :key="project.title"
          class="re8-card p-8 group transition-all duration-500"
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :visible="{ opacity: 1, y: 0, transition: { delay: index * 100 + 300 } }"
        >
          <!-- Project Header -->
          <div class="flex items-start justify-between mb-6">
            <div 
              class="w-14 h-14 rounded-lg flex items-center justify-center transition-all duration-300 group-hover:scale-110"
              :style="{ backgroundColor: project.color + '20', border: `1px solid ${project.color}40` }"
            >
              <span 
                class="font-cinzel text-2xl" 
                :style="{ color: project.color }"
              >
                {{ project.initials }}
              </span>
            </div>
            <div class="flex gap-2">
              <a 
                v-if="project.github" 
                :href="project.github" 
                target="_blank"
                class="w-10 h-10 rounded-lg flex items-center justify-center text-re8-text-dim hover:text-re8-candle hover:border-re8-candle transition-all duration-300" style="background-color: #0f1115; border: 1px solid #2a2d35"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-2.597 8.206-6.086 8.206-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </a>
              <a 
                v-if="project.demo" 
                :href="project.demo" 
                target="_blank"
                class="w-10 h-10 rounded-lg flex items-center justify-center text-re8-text-dim hover:text-re8-candle hover:border-re8-candle transition-all duration-300" style="background-color: #0f1115; border: 1px solid #2a2d35"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>
            </div>
          </div>

          <!-- Project Title & Description -->
          <h2 class="font-cinzel text-xl text-re8-parchment mb-3 group-hover:text-re8-candle transition-colors duration-300">
            {{ project.title }}
          </h2>
          <p class="font-outfit text-re8-text-muted mb-6">{{ project.description }}</p>

          <!-- Key Features -->
          <ul class="space-y-2 mb-6">
            <li 
              v-for="feature in project.features" 
              :key="feature"
              class="font-outfit text-sm text-re8-text-dim flex items-start gap-2"
            >
              <span class="w-1 h-1 rounded-full bg-re8-candle mt-2 flex-shrink-0"></span>
              {{ feature }}
            </li>
          </ul>

          <!-- Tech Stack -->
          <div class="flex flex-wrap gap-2 pt-4 border-t border-re8-border">
            <span 
              v-for="tech in project.tech" 
              :key="tech"
              class="px-3 py-1 bg-re8-bg-soft border border-re8-border rounded-full text-xs text-re8-text-dim"
            >
              {{ tech }}
            </span>
          </div>
        </div>
      </div>

      <!-- More Projects Link -->
      <div class="text-center mt-12">
        <a 
          href="https://github.com/Abhishek-Dobliyal" 
          target="_blank"
          class="re8-button inline-flex items-center gap-2"
        >
          <span>View All on GitHub</span>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
const projectsData = {
  intro: "Projects are where theory meets practice. Here are some highlights from my journey in building solutions for real-world problems.",
  projects: [
    {
      initials: 'CP',
      title: 'Calculation Pad',
      description: 'An intelligent math calculator that recognizes handwritten mathematical expressions and evaluates them using deep learning.',
      color: '#ff9f43',
      features: [
        'Trained Convolutional Neural Networks to recognize handwritten digits and mathematical symbols with 97% accuracy',
        'Built both desktop (Tkinter) and web (Streamlit) interfaces',
        'Model trained on MNIST dataset extended with custom operators',
        'Achieved real-time inference with sub-second response time'
      ],
      tech: ['Python', 'TensorFlow', 'Keras', 'OpenCV', 'Streamlit', 'Tkinter'],
      github: 'https://github.com/Abhishek-Dobliyal/Calculation-Pad'
    },
    {
      initials: 'NS',
      title: 'Neural Style Transfer',
      description: 'Deep learning-powered application that applies artistic styles from one image to another while preserving content.',
      color: '#8b5cf6',
      features: [
        'Implemented style transfer using VGG19 pre-trained model',
        'Built REST API using FastAPI for seamless integration',
        'Created web interface with Vue.js for user-friendly experience',
        'Added content-style ratio control for customizable outputs'
      ],
      tech: ['Python', 'Keras', 'FastAPI', 'Vue.js', 'TensorFlow'],
      github: 'https://github.com/Abhishek-Dobliyal/Neural-Style-Transfer'
    },
    {
      initials: 'F',
      title: 'Falcon - Remote Monitor',
      description: 'A remote system monitoring tool that enables administrators to monitor and control client systems via HTTP.',
      color: '#06b6d4',
      features: [
        'Built web portal for real-time system monitoring',
        'Features include webcam capture, screenshot capture, process management',
        'Implemented secure client-server communication using JWT',
        'Deployed with MongoDB for efficient data storage'
      ],
      tech: ['Python', 'Flask', 'MongoDB', 'Bootstrap', 'JavaScript'],
      github: 'https://github.com/Abhishek-Dobliyal/Falcon'
    },
    {
      initials: 'SC',
      title: 'Smart Contact',
      description: 'Android application that uses NFC and QR codes for instant contact sharing with smart profile cards.',
      color: '#10b981',
      features: [
        'Built with Android Studio and Kotlin',
        'NFC tag and QR code generation for contact sharing',
        'Secure local storage using Room Database',
        'Material Design 3 compliant UI'
      ],
      tech: ['Kotlin', 'Android', 'NFC', 'QR Codes', 'Room DB'],
      github: 'https://github.com/Abhishek-Dobliyal/Smart-Contact'
    }
  ]
}
</script>