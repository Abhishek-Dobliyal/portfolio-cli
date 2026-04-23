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

        <div>
            <p class="text-accent text-xs mb-1">// writing</p>
            <p class="text-term-text-muted text-sm">
                <a :href="BLOG_URL" target="_blank" rel="noopener noreferrer" class="term-link">
                    From Archival to Access: Config-Driven Data Pipelines
                </a>
                <span class="text-term-text-dim"> — Uber Engineering</span>
            </p>
        </div>
    </div>
</template>

<script setup>
import { BLOG_URL, profile } from '@/data/profile.js'
</script>
