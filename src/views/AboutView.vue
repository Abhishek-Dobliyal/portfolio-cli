<template>
  <div class="about-view min-h-screen py-32 px-6">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-16">
        <h1 
          class="re8-heading text-4xl md:text-5xl mb-6"
          v-motion
          :initial="{ opacity: 0, y: 20 }"
          :enter="{ opacity: 1, y: 0 }"
        >
          About Me
        </h1>
        <p 
          class="font-outfit text-re8-text-muted text-lg max-w-2xl mx-auto"
          v-motion
          :initial="{ opacity: 0, y: 20 }"
          :enter="{ opacity: 1, y: 0, transition: { delay: 200 } }"
        >
          {{ aboutData.intro }}
        </p>
      </div>

      <!-- Bio Cards -->
      <div class="space-y-6">
        <div 
          v-for="(section, index) in aboutData.sections" 
          :key="section.title"
          class="re8-card p-8"
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :visible="{ opacity: 1, y: 0, transition: { delay: index * 100 + 300 } }"
        >
          <h2 class="font-cinzel text-xl text-re8-parchment mb-4">{{ section.title }}</h2>
          <p class="font-outfit text-re8-text-muted leading-relaxed">{{ section.content }}</p>
        </div>
      </div>

      <!-- Interests -->
      <div class="re8-card p-8 mt-8">
        <h2 class="font-cinzel text-xl text-re8-parchment mb-6">Interests & Hobbies</h2>
        <div class="flex flex-wrap gap-3">
          <span 
            v-for="interest in aboutData.interests" 
            :key="interest"
            class="px-4 py-2 bg-re8-bg-soft border border-re8-border rounded-lg text-re8-text-muted text-sm"
          >
            {{ interest }}
          </span>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
        <div 
          v-for="(stat, index) in stats" 
          :key="stat.label"
          class="re8-card p-6 text-center"
          v-motion
          :initial="{ opacity: 0, scale: 0.9 }"
          :visible="{ opacity: 1, scale: 1, transition: { delay: index * 50 } }"
        >
          <p class="font-cinzel text-2xl text-re8-candle mb-1">{{ stat.value }}</p>
          <p class="font-outfit text-xs uppercase tracking-wider text-re8-text-dim">{{ stat.label }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const aboutData = {
  intro: "I'm a Software Engineer at Uber with 3+ years of experience focused on data engineering and backend systems. I love solving complex problems and building scalable solutions that impact millions of users.",
  sections: [
    {
      title: "Professional Journey",
      content: "Currently serving as a Software Engineer at Uber, working on data pipelines and analytics infrastructure. Previously held internships at Uber, Zuma (YC'21), and Samsung Research India, where I gained hands-on experience with various tech stacks and learned the importance of building robust, scalable systems."
    },
    {
      title: "What Drives Me",
      content: "I'm passionate about using technology to solve real-world problems. Every line of code I write is an opportunity to make someone's life a little easier, whether it's optimizing a data pipeline that processes terabytes of data or building a feature that improves the user experience for millions of riders."
    },
    {
      title: "Continuous Learning",
      content: "Technology evolves rapidly, and I believe in staying curious. I'm always exploring new frameworks, languages, and methodologies to enhance my problem-solving toolkit. This mindset has helped me adapt quickly to new challenges and deliver impact in diverse domains."
    }
  ],
  interests: [
    'Data Engineering', 'Backend Development', 'Machine Learning', 
    'System Design', 'Code Optimization', 'Chess', 'Football',
    'Tech Exploring', 'Music', 'Gaming'
  ]
}

const stats = [
  { value: '3+', label: 'Years YOE' },
  { value: '10M+', label: 'Users Impacted' },
  { value: '50TB+', label: 'Data Processed' },
  { value: '750+', label: 'LeetCode Solved' }
]
</script>