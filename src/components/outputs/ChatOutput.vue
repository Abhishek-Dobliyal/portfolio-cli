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
            <div
                v-if="displayedResponse"
                class="chat-markdown text-term-text break-words"
                v-html="renderedResponse"
            ></div>
            <p v-else class="text-term-text whitespace-pre-wrap break-words">{{ loadingMessage }}</p>
            <span v-if="showCursor" class="chat-cursor"></span>
            <p v-if="status === 'streaming'" class="text-term-text-muted text-xs animate-pulse">streaming response...</p>
            <p v-else-if="status === 'error'" class="text-error text-xs">{{ error }}</p>
        </div>
    </div>
</template>

<script setup>
import { computed, onUnmounted, ref, watch } from 'vue'
import { marked } from 'marked'

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

const renderer = new marked.Renderer()
renderer.link = ({ href, title, tokens }) => {
    const text = parser.parseInline(tokens)
    const safeHref = href ?? '#'
    const titleAttr = title ? ` title="${escapeHtml(title)}"` : ''
    return `<a href="${escapeAttribute(safeHref)}" target="_blank" rel="noopener noreferrer"${titleAttr}>${text}</a>`
}
const parser = new marked.Parser()

marked.setOptions({
    gfm: true,
    breaks: true,
    renderer,
})

const loadingMessage = computed(() => {
    if (props.status === 'error') return ''
    return 'Thinking...'
})

const renderedResponse = computed(() => marked.parse(escapeHtml(displayedResponse.value)))

const showCursor = computed(() => {
    return props.mode === 'stream' && props.status !== 'error' && displayedResponse.value.length > 0
})

function stopTyping() {
    if (typingTimerId !== null) {
        clearTimeout(typingTimerId)
        typingTimerId = null
    }
}

function escapeHtml(value) {
    return value
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
}

function escapeAttribute(value) {
    return escapeHtml(value).replaceAll('"', '&quot;')
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
.chat-markdown :deep(p) {
    margin: 0;
    white-space: pre-wrap;
}

.chat-markdown :deep(p + p),
.chat-markdown :deep(ul),
.chat-markdown :deep(ol),
.chat-markdown :deep(pre),
.chat-markdown :deep(blockquote) {
    margin-top: 0.5rem;
}

.chat-markdown :deep(ul),
.chat-markdown :deep(ol) {
    padding-left: 1.25rem;
}

.chat-markdown :deep(li + li) {
    margin-top: 0.25rem;
}

.chat-markdown :deep(a) {
    color: #10b981;
    text-decoration: underline;
}

.chat-markdown :deep(code) {
    padding: 0.05rem 0.25rem;
    border-radius: 0.25rem;
    background: rgba(16, 185, 129, 0.12);
    color: #6ee7b7;
}

.chat-markdown :deep(pre) {
    overflow-x: auto;
    padding: 0.75rem;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 0.375rem;
    background: rgba(255, 255, 255, 0.03);
}

.chat-markdown :deep(pre code) {
    padding: 0;
    background: transparent;
}

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
