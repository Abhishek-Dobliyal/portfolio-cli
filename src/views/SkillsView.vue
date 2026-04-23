<template>
  <div class="skills-view min-h-screen py-32 px-6">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-16">
        <h1 
          class="re8-heading text-4xl md:text-5xl mb-6"
          v-motion
          :initial="{ opacity: 0, y: 20 }"
          :enter="{ opacity: 1, y: 0 }"
        >
          Technical Arsenal
        </h1>
        <p 
          class="font-outfit text-re8-text-muted text-lg max-w-2xl mx-auto"
          v-motion
          :initial="{ opacity: 0, y: 20 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 200 } }"
        >
          {{ skillsData.intro }}
        </p>
      </div>

      <!-- Skills Grid by Category -->
      <div class="grid md:grid-cols-2 gap-8">
        <div 
          v-for="(category, catIndex) in skillsData.categories" 
          :key="category.name"
          class="re8-card p-8"
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :visible="{ opacity: 1, y: 0, transition: { delay: catIndex * 100 + 300 } }"
        >
          <div class="flex items-center gap-4 mb-6">
            <div 
              class="w-12 h-12 rounded-lg flex items-center justify-center"
              :style="{ backgroundColor: category.color + '20', border: `1px solid ${category.color}40` }"
            >
              <span :style="{ color: category.color }" v-html="category.icon"></span>
            </div>
            <h2 class="font-cinzel text-xl text-re8-parchment">{{ category.name }}</h2>
          </div>
          
          <div class="flex flex-wrap gap-2">
            <span 
              v-for="skill in category.skills" 
              :key="skill.name"
              class="px-3 py-2 border border-re8-border rounded-md text-re8-text-muted text-sm flex items-center gap-2 hover:border-re8-candle transition-colors duration-300" style="background-color: #0f1115"
            >
              <span 
                class="w-2 h-2 rounded-full"
                :style="{ backgroundColor: category.color }"
              ></span>
              {{ skill.name }}
              <span 
                v-if="skill.level"
                class="text-xs text-re8-text-dim ml-1"
              >
                ({{ skill.level }})
              </span>
            </span>
          </div>
        </div>
      </div>

      <!-- Tools & Technologies -->
      <div class="re8-card p-8 mt-8">
        <h2 class="font-cinzel text-xl text-re8-parchment mb-6">Tools & Technologies</h2>
        <div class="flex flex-wrap gap-3">
          <span 
            v-for="tool in skillsData.tools" 
            :key="tool"
            class="px-4 py-2 border border-re8-border rounded-lg text-re8-text-muted text-sm hover:border-re8-candle transition-colors duration-300 cursor-default" style="background-color: #0f1115"
          >
            {{ tool }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const skillsData = {
  intro: "My technical expertise spans multiple domains - from backend systems to data engineering. I believe in using the right tool for the job, and I'm always expanding my toolkit.",
  categories: [
    {
      name: 'Languages',
      color: '#ff9f43',
      icon: '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/></svg>',
      skills: [
        { name: 'Python', level: 'Expert' },
        { name: 'JavaScript' },
        { name: 'TypeScript' },
        { name: 'Go' },
        { name: 'SQL' },
        { name: 'Java' }
      ]
    },
    {
      name: 'Frameworks & Libraries',
      color: '#06b6d4',
      icon: '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>',
      skills: [
        { name: 'Vue.js' },
        { name: 'React' },
        { name: 'FastAPI' },
        { name: 'Flask' },
        { name: 'Gin' },
        { name: 'Express' }
      ]
    },
    {
      name: 'Data Engineering',
      color: '#8b5cf6',
      icon: '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"/></svg>',
      skills: [
        { name: 'Apache Spark' },
        { name: 'Apache Airflow' },
        { name: 'Delta Lake' },
        { name: 'Snowflake' },
        { name: 'BigQuery' },
        { name: 'Databricks' }
      ]
    },
    {
      name: 'Cloud & Infrastructure',
      color: '#10b981',
      icon: '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/></svg>',
      skills: [
        { name: 'AWS' },
        { name: 'Google Cloud' },
        { name: 'Docker' },
        { name: 'Kubernetes' },
        { name: 'Terraform' },
        { name: 'Git' }
      ]
    }
  ],
  tools: [
    'Git', 'Docker', 'Kubernetes', 'Jenkins', 'GitHub Actions', 
    'Terraform', 'Datadog', 'Grafana', 'Jira', 'Confluence',
    'VS Code', 'PyCharm', 'Postman', 'DBeaver', 'Tableau'
  ]
}
</script>