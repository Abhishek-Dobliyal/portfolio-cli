<template>
    <div class="space-y-3">
        <p class="text-accent font-bold">Career Timeline</p>
        <div class="relative border-l-2 border-accent ml-2 space-y-5">
            <div v-for="(exp, index) in timelineData" :key="index" class="relative pl-4">
                <div class="absolute -left-[9px] w-4 h-4 rounded-full bg-accent"></div>
                <p class="text-accent text-sm">{{ exp.duration }}</p>
                <p class="text-term-text font-semibold">{{ exp.role }} @ {{ exp.company }}</p>
                <p class="text-term-text-muted text-xs mt-1">{{ exp.description }}</p>
                <ul class="mt-1 space-y-0.5">
                    <li
                        v-for="(point, i) in exp.points"
                        :key="i"
                        class="text-term-text-muted text-xs before:content-['›'] before:text-accent before:mr-1"
                    >{{ point }}</li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup>
import { timelineData } from '@/data/profile.js'
</script>
