<template>
    <div>
        <div v-for="(skills, category) in profile.skills" :key="category" class="mb-3">
            <p class="text-accent mb-1 capitalize">[{{ category }}]</p>
            <p class="text-term-text-muted">{{ skills.join(', ') }}</p>
        </div>
    </div>
</template>

<script setup>
import { profile } from '@/data/profile.js'
</script>
