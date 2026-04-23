<template>
    <div class="space-y-2">
        <p class="text-term-text">Opening resume in a new tab...</p>
        <p class="text-term-text-dim text-sm">
            If nothing opened, use
            <a :href="RESUME_URL" target="_blank" rel="noopener noreferrer" class="term-link">this resume link</a>.
        </p>
    </div>
</template>

<script setup>
import { RESUME_URL } from '@/data/profile.js'
</script>
