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
            <p class="text-term-text whitespace-pre-wrap break-words">
                {{ displayedResponse || loadingMessage }}<span v-if="showCursor" class="chat-cursor"></span>
            </p>
            <p v-if="status === 'streaming'" class="text-term-text-muted text-xs animate-pulse">streaming response...</p>
            <p v-else-if="status === 'error'" class="text-error text-xs">{{ error }}</p>
        </div>
    </div>
</template>

<script setup>
import { computed, onUnmounted, ref, watch } from 'vue'

const props = defineProps({
    mode:     { type: String, default: 'stream' },
    status:   { type: String, default: 'idle' },
    response: { type: String, default: '' },
    error:    { type: String, default: '' },
})

const TYPEWRITER_STEP = 3
const TYPEWRITER_DELAY_MS = 16
const displayedResponse = ref('')
let typingTimerId = null

const loadingMessage = computed(() => {
    if (props.status === 'error') return ''
    return 'Thinking...'
})

const showCursor = computed(() => props.mode === 'stream' && props.status !== 'error')

function stopTyping() {
    if (typingTimerId !== null) {
        clearTimeout(typingTimerId)
        typingTimerId = null
    }
}

function animateResponse() {
    stopTyping()

    const remainingText = props.response.slice(displayedResponse.value.length)
    if (!remainingText) return

    const nextLength = displayedResponse.value.length + TYPEWRITER_STEP
    displayedResponse.value = props.response.slice(0, nextLength)

    if (displayedResponse.value.length < props.response.length) {
        typingTimerId = window.setTimeout(animateResponse, TYPEWRITER_DELAY_MS)
    }
}

watch(() => props.response, (nextResponse) => {
    if (nextResponse.length < displayedResponse.value.length) {
        displayedResponse.value = nextResponse
    }

    animateResponse()
}, { immediate: true })

watch(() => props.status, (nextStatus) => {
    if (nextStatus === 'error') {
        stopTyping()
    }
})

onUnmounted(() => {
    stopTyping()
})
</script>

<style scoped>
.chat-cursor {
    display: inline-block;
    width: 0.5em;
    height: 1.05em;
    margin-left: 0.1em;
    background: #10b981;
    vertical-align: text-bottom;
    animation: chatCursorBlink 1s step-end infinite;
}

@keyframes chatCursorBlink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0; }
}
</style>
