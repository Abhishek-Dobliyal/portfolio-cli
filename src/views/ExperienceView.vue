<template>
  <div class="experience-view min-h-screen py-32 px-6">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-16">
        <h1 
          class="re8-heading text-4xl md:text-5xl mb-6"
          v-motion
          :initial="{ opacity: 0, y: 20 }"
          :enter="{ opacity: 1, y: 0 }"
        >
          Experience
        </h1>
        <p 
          class="font-outfit text-re8-text-muted text-lg max-w-2xl mx-auto"
          v-motion
          :initial="{ opacity: 0, y: 20 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 200 } }"
        >
          {{ experienceData.intro }}
        </p>
      </div>

      <!-- Timeline -->
      <div class="relative">
        <!-- Timeline Line -->
        <div class="absolute left-8 top-0 bottom-0 w-px bg-re8-border md:left-1/2"></div>

        <!-- Experience Items -->
        <div 
          v-for="(exp, index) in experienceData.experiences" 
          :key="exp.company"
          class="relative mb-8 last:mb-0"
        >
          <div 
            class="re8-card p-8 md:ml-12 md:mr-0"
            :class="index % 2 === 0 ? 'md:mr-auto md:pr-16' : 'md:ml-12 md:pl-16'"
            v-motion
            :initial="{ opacity: 0, x: index % 2 === 0 ? -30 : 30 }"
            :visible="{ opacity: 1, x: 0, transition: { delay: index * 100 + 300 } }"
          >
            <!-- Company Icon -->
            <div 
              class="absolute -left-4 top-8 w-8 h-8 rounded-lg flex items-center justify-center md:hidden"
              :style="{ backgroundColor: exp.color + '20', border: `1px solid ${exp.color}40` }"
            >
              <span class="font-cinzel text-sm" :style="{ color: exp.color }">{{ exp.initials[0] }}</span>
            </div>
            
            <!-- Desktop Timeline Dot -->
            <div 
              class="hidden md:block absolute top-8 w-4 h-4 rounded-full border-2 border-re8-candle bg-re8-bg"
              :class="index % 2 === 0 ? '-right-2' : '-left-2'"
              :style="{ borderColor: exp.color }"
            ></div>

            <!-- Content -->
            <div class="flex flex-col md:flex-row md:items-center gap-4 mb-4">
              <div class="flex-grow">
                <h2 class="font-cinzel text-xl text-re8-parchment">{{ exp.role }}</h2>
                <p class="font-outfit text-re8-candle">{{ exp.company }}</p>
              </div>
              <span 
                class="font-outfit text-xs uppercase tracking-wider px-3 py-1 rounded"
                :style="{ backgroundColor: exp.color + '20', color: exp.color, border: `1px solid ${exp.color}40` }"
              >
                {{ exp.duration }}
              </span>
            </div>

            <!-- Location -->
            <p class="font-outfit text-sm text-re8-text-dim mb-4 flex items-center gap-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              {{ exp.location }}
            </p>

            <!-- Key Achievements -->
            <ul class="space-y-3">
              <li 
                v-for="achievement in exp.achievements" 
                :key="achievement"
                class="font-outfit text-sm text-re8-text-muted flex items-start gap-3"
              >
                <span class="w-1.5 h-1.5 rounded-full bg-re8-candle mt-2 flex-shrink-0"></span>
                {{ achievement }}
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Education Section -->
      <div class="mt-16">
        <h2 class="re8-heading text-2xl mb-8 text-center">Education</h2>
        <div class="space-y-6">
          <div 
            v-for="edu in experienceData.education" 
            :key="edu.degree"
            class="re8-card p-6 flex flex-col md:flex-row md:items-center gap-4"
            v-motion
            :initial="{ opacity: 0, y: 20 }"
            :visible="{ opacity: 1, y: 0, transition: { delay: 100 } }"
          >
            <div class="flex-grow">
              <h3 class="font-cinzel text-lg text-re8-parchment">{{ edu.degree }}</h3>
              <p class="font-outfit text-sm text-re8-text-muted">{{ edu.school }}</p>
            </div>
            <span class="font-outfit text-sm text-re8-text-dim">{{ edu.year }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const experienceData = {
  intro: "My professional journey has been shaped by incredible opportunities at leading tech companies. Each role has contributed to my growth as a software engineer.",
  experiences: [
    {
      role: 'Software Engineer',
      company: 'Uber',
      initials: 'U',
      duration: 'June 2023 - Present',
      location: 'San Francisco, CA',
      color: '#ff9f43',
      achievements: [
        'Developed migration pipeline for 56 CDS datasets (10 TB, ORC to Parquet) for seamless data management',
        'Designed and implemented retrieval workflow from Terrablob to HDFS, achieving 85% reduction in retrieval time',
        'Transformed Airports intermediate dataset into reporting dataset for global airport trip insights',
        'Worked on engineering excellence items including FTDQ automation and custom partition range sensors'
      ]
    },
    {
      role: 'Software Engineer Intern',
      company: 'Zuma (YC\'21)',
      initials: 'Z',
      duration: 'May 2023 - July 2023',
      location: 'Bangalore, India',
      color: '#8b5cf6',
      achievements: [
        'Developed TourTypes API from ground up to retrieve all tour types for communities',
        'Integrated UIF client services for seamless third-party interactions',
        'Implemented CancelLead API to automatically cancel stale leads',
        'Wrote essential unit tests for key packages in Yardi Integrations'
      ]
    },
    {
      role: 'Software Engineer Intern',
      company: 'Uber',
      initials: 'U',
      duration: 'May 2022 - July 2022',
      location: 'San Francisco, CA',
      color: '#ff9f43',
      achievements: [
        'Worked with Customer Obsession team to proactively resolve cancellation issues',
        'Integrated Proactive Outreach platform with Policy Engine service',
        'Built Deterministic Trigger Controller from scratch for automation checks',
        'Developed workflow to automatically target desired riders'
      ]
    },
    {
      role: 'Research Intern',
      company: 'Samsung (SRIB)',
      initials: 'S',
      duration: 'August 2021 - April 2022',
      location: 'Bangalore, India',
      color: '#06b6d4',
      achievements: [
        'Worked on Samsung Verification System for Camera Sensors',
        'Experimented with camera source files validation and parsing techniques',
        'Developed GUI interface for validation of camera source and UX documents',
        'Incorporated report generation and log parsing scripts'
      ]
    }
  ],
  education: [
    {
      degree: 'Bachelor of Technology in Computer Science',
      school: 'Vellore Institute of Technology (VIT), Vellore',
      year: '2019 - 2023'
    },
    {
      degree: 'High School (PCM)',
      school: 'Delhi Public School, R.K. Puram',
      year: '2017 - 2019'
    }
  ]
}
</script>