<template>
    <div class="space-y-5">
        <div v-for="project in profile.projects" :key="project.title">
            <p class="text-accent font-semibold">{{ project.title }}</p>
            <p class="text-term-text-muted text-sm mt-0.5">{{ project.description }}</p>
            <ul class="mt-1 space-y-0.5">
                <li
                    v-for="(point, i) in project.points"
                    :key="i"
                    class="text-term-text-dim text-xs before:content-['›'] before:text-accent before:mr-1"
                >{{ point }}</li>
            </ul>
            <p class="text-term-text-dim text-xs mt-1">
                <span class="text-accent">tech:</span> {{ project.tech.join(', ') }}
            </p>
        </div>
    </div>
</template>

<script setup>
import { profile } from '@/data/profile.js'
</script>
