<template>
    <div class="space-y-3 text-sm">
        <p class="text-accent font-bold">[ Portfolio Assistant ]</p>

        <div v-if="mode === 'usage'" class="space-y-2">
            <p class="text-term-text">Ask about Abhishek's background, work, projects, or skills.</p>
            <p class="text-term-text-muted text-xs">
                Example: <span class="text-accent">/chat What kind of work do you do at Uber?</span>
            </p>
        </div>

        <div v-else class="space-y-2">
            <p class="text-term-text whitespace-pre-wrap break-words">{{ response || loadingMessage }}</p>
            <p v-if="status === 'streaming'" class="text-term-text-muted text-xs animate-pulse">streaming response...</p>
            <p v-else-if="status === 'error'" class="text-error text-xs">{{ error }}</p>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    mode:     { type: String, default: 'stream' },
    status:   { type: String, default: 'idle' },
    response: { type: String, default: '' },
    error:    { type: String, default: '' },
})

const loadingMessage = computed(() => {
    if (props.status === 'error') return ''
    return 'Thinking...'
})
</script>
