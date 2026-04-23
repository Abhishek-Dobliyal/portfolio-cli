<template>
    <div class="space-y-2">
        <p><a :href="RESUME_URL" target="_blank" class="term-link">resume</a> - View my resume</p>
        <p><a :href="profile.socials.github" target="_blank" class="term-link">github</a> - GitHub profile</p>
        <p><a :href="profile.socials.linkedin" target="_blank" class="term-link">linkedin</a> - LinkedIn profile</p>
        <p><a :href="profile.socials.leetcode" target="_blank" class="term-link">leetcode</a> - LeetCode profile</p>
    </div>
</template>

<script setup>
import { profile, RESUME_URL } from '@/data/profile.js'
</script>
