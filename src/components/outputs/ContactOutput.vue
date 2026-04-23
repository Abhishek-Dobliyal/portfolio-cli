<template>
    <div>
        <p class="text-term-text-muted mb-3">Available at:</p>
        <p class="text-term-text">
            GitHub:
            <a :href="profile.socials.github" target="_blank" rel="noopener noreferrer" class="term-link">github.com/Abhishek-Dobliyal</a>
        </p>
        <p class="text-term-text">
            LinkedIn:
            <a :href="profile.socials.linkedin" target="_blank" rel="noopener noreferrer" class="term-link">linkedin.com/in/abhishek-dobliyal</a>
        </p>
        <p class="text-term-text">
            LeetCode:
            <a :href="profile.socials.leetcode" target="_blank" rel="noopener noreferrer" class="term-link">leetcode.com/u/1nnOcent/</a>
        </p>
    </div>
</template>

<script setup>
import { profile } from '@/data/profile.js'
</script>
