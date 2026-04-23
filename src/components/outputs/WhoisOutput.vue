<template>
    <div class="space-y-2 text-sm">
        <div class="grid grid-cols-[80px_1fr] gap-1">
            <span class="text-term-text-dim">Name:</span>
            <span class="text-term-text">Abhishek Dobliyal</span>
            <span class="text-term-text-dim">Role:</span>
            <span class="text-term-text">Software Engineer II @ Uber</span>
            <span class="text-term-text-dim">Team:</span>
            <span class="text-term-text">Capacity & Efficiency</span>
            <span class="text-term-text-dim">Location:</span>
            <span class="text-term-text">Amsterdam, Netherlands</span>
            <span class="text-term-text-dim">Focus:</span>
            <span class="text-term-text">Backend + Data Engineering</span>
            <span class="text-term-text-dim">Stack:</span>
            <span class="text-term-text"
                >Python, Go, TypeScript, SQL, Spark</span
            >
            <span class="text-term-text-dim">Visits:</span>
            <span class="text-term-text">{{ visitorCount }} visitors</span>
            <span class="text-term-text-dim">Session:</span>
            <span class="text-term-text">{{ visitorId }}</span>
            <span class="text-term-text-dim">Uptime:</span>
            <span class="text-term-text">3+ years professional</span>
        </div>
    </div>
</template>

<script setup>
defineProps({
    visitorCount: { type: [Number, String], default: '...' },
    visitorId:    { type: String, required: true },
});
</script>
