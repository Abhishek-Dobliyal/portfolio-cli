<template>
    <div class="space-y-3">
        <p class="text-accent font-bold mb-2">[ Career Stats ]</p>

        <div class="flex flex-wrap justify-center gap-8 sm:gap-14">
            <div v-for="stat in counters" :key="stat.label" class="w-24 sm:w-32 text-center">
                <div class="text-2xl sm:text-3xl font-bold text-accent">
                    {{ stat.display }}
                </div>
                <div class="text-term-text-dim text-xs mt-1">{{ stat.label }}</div>
            </div>
        </div>

        <div class="mt-4 space-y-4">
            <p class="text-term-text-dim text-xs">[ Skills Proficiency ]</p>
            <div v-for="bar in skillBars" :key="bar.domain" class="space-y-1">
                <div class="flex items-center justify-between text-xs">
                    <span class="text-term-text font-medium">{{ bar.domain }}</span>
                    <span class="text-accent">{{ bar.pct }}%</span>
                </div>
                <div class="rounded-full h-1.5 overflow-hidden" style="background: rgba(255,255,255,0.07)">
                    <div
                        class="h-full rounded-full skill-bar-fill"
                        :style="{ width: bar.pct + '%' }"
                    ></div>
                </div>
                <div class="flex flex-wrap gap-x-3 gap-y-1 pt-1">
                    <span
                        v-for="(skill, si) in bar.skills"
                        :key="skill"
                        class="text-term-text-dim text-xs skill-tag"
                        :style="{ animationDelay: (0.8 + si * 0.07) + 's' }"
                    >· {{ skill }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { skillBars, statsConfig } from '@/data/profile.js'

const counters = ref(statsConfig.map(s => ({
    label:   s.label,
    value:   s.value,
    display: s.hasSuffix ? '0+' : '0',
    hasSuffix: s.hasSuffix,
})))
const counterTimerIds = []

onMounted(() => {
    counters.value.forEach((stat, idx) => {
        let current = 0
        const end    = stat.value
        const suffix = stat.hasSuffix ? '+' : ''
        const step   = Math.ceil(end / (1200 / 30))
        const timer  = setInterval(() => {
            current = Math.min(current + step, end)
            counters.value[idx].display = current + suffix
            if (current >= end) clearInterval(timer)
        }, 30)

        counterTimerIds.push(timer)
    })
})

onUnmounted(() => {
    counterTimerIds.forEach(clearInterval)
})
</script>

<style scoped>
.skill-bar-fill {
    background: #10b981;
    box-shadow: 0 0 6px rgba(16, 185, 129, 0.4);
    animation: growBar 1.2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
@keyframes growBar {
    from { width: 0% !important; opacity: 0.4; }
    to   { opacity: 1; }
}
.skill-tag {
    opacity: 0;
    animation: tagFadeIn 0.2s ease forwards;
}
@keyframes tagFadeIn {
    from { opacity: 0; transform: translateY(3px); }
    to   { opacity: 1; transform: translateY(0); }
}
</style>
