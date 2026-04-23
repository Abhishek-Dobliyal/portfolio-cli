<template>
    <div class="space-y-3">
        <p class="text-term-text">{{ profile.intro }}</p>

        <p class="text-term-text-muted">
            Currently working at
            <span class="text-accent">{{ profile.company }}</span>
            as a {{ profile.role }} on the
            <span class="text-accent">{{ profile.team }}</span> team
            in {{ profile.location }}.
        </p>

        <div>
            <p class="text-accent text-xs mb-1">// interests</p>
            <p class="text-term-text-muted text-sm">{{ profile.interests }}</p>
        </div>

        <div>
            <p class="text-accent text-xs mb-1">// outside the terminal</p>
            <p class="text-term-text-muted text-sm">{{ profile.hobbies }}</p>
        </div>
    </div>
</template>

<script setup>
import { profile } from '@/data/profile.js'
</script>
