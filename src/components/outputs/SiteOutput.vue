<template>
    <div class="space-y-3 text-sm">
        <p class="text-accent font-bold">[ Site Statistics ]</p>

        <div v-if="status === 'loading'">
            <p class="text-term-text-muted animate-pulse">pinging server...</p>
        </div>

        <div v-else-if="status === 'asleep'" class="space-y-2">
            <p class="text-term-prompt">&gt;&gt; stats server is hibernating on free tier.</p>
            <p class="text-term-text-muted text-xs">
                run <span class="text-accent">/site</span> again in ~30 seconds once it wakes up.
            </p>
        </div>

        <div v-else-if="status === 'ready'" class="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div class="stat-cell">
                <div class="text-2xl font-bold text-accent">{{ rawStats.visitors_cnt }}</div>
                <div class="text-term-text-dim text-xs mt-0.5">Total Visitors</div>
            </div>
            <div class="stat-cell">
                <div class="text-2xl font-bold text-accent">{{ todayCount }}</div>
                <div class="text-term-text-dim text-xs mt-0.5">Today</div>
            </div>
            <div class="stat-cell">
                <div class="text-2xl font-bold text-accent">{{ rawStats.max_visits.cnt }}</div>
                <div class="text-term-text-dim text-xs mt-0.5">Peak Day</div>
                <div class="text-term-text-dim text-xs">{{ rawStats.max_visits.date }}</div>
            </div>
            <div class="stat-cell">
                <div class="text-2xl font-bold text-accent">{{ avgSession }}</div>
                <div class="text-term-text-dim text-xs mt-0.5">Avg Session</div>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    status:     { type: String,  required: true },
    rawStats:   { type: Object,  default: null  },
    todayCount: { type: Number,  default: 0     },
    avgSession: { type: String,  default: 'N/A' },
})
</script>

<style scoped>
.stat-cell {
    background: rgba(16, 185, 129, 0.04);
    border: 1px solid rgba(16, 185, 129, 0.15);
    border-radius: 6px;
    padding: 10px 12px;
    text-align: center;
}
</style>
