<template>
    <div class="space-y-2">
        <div class="font-bold text-base sm:text-lg break-words glitch-neon">
            {{ glitchText }}
        </div>
        <p v-if="!loading && joke.delivery" class="text-pink-400 mt-2 text-sm">
            {{ joke.delivery }}
        </p>
        <div v-if="loading" class="text-term-text-dim text-xs">
            {{ binary }}
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const GLITCH_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*!'
const JOKE_API = 'https://official-joke-api.appspot.com/random_joke'
const FALLBACK = { setup: 'Why do programmers hate nature?', delivery: 'It has too many bugs.' }

const glitchText = ref('ACCESS')
const binary     = ref('')
const joke       = ref({ setup: '', delivery: '' })
const loading    = ref(true)

let interval = null
let revealTimeout = null

function clearAnimationTimers() {
    if (interval) {
        clearInterval(interval)
        interval = null
    }

    if (revealTimeout) {
        clearTimeout(revealTimeout)
        revealTimeout = null
    }
}

function scramble(text) {
    return text.split('').map(ch => {
        if (ch === ' ') return ' '
        return Math.random() > 0.7
            ? GLITCH_CHARS[Math.floor(Math.random() * GLITCH_CHARS.length)]
            : ch
    }).join('')
}

function updateBinary() {
    binary.value = Array(32).fill(0).map(() => Math.random() > 0.5 ? '1' : '0').join('')
}

async function fetchAndAnimate() {
    loading.value = true
    clearAnimationTimers()

    try {
        const res  = await fetch(JOKE_API)
        const data = await res.json()
        joke.value = { setup: data.setup, delivery: data.punchline }
    } catch {
        joke.value = FALLBACK
    }

    interval = setInterval(() => {
        glitchText.value = scramble(joke.value.setup)
        updateBinary()
    }, 100)

    revealTimeout = setTimeout(() => {
        clearAnimationTimers()
        glitchText.value = joke.value.setup
        loading.value = false
    }, 1500)
}

onMounted(fetchAndAnimate)
onUnmounted(clearAnimationTimers)
</script>

<style scoped>
.glitch-neon {
    color: #fff;
    text-shadow:
        0 0 5px #10b981,
        0 0 10px #10b981,
        0 0 20px #10b981,
        0 0 40px #10b981,
        2px 2px 0 #ec4899,
        -2px -2px 0 #06b6d4;
    animation: neonPulse 0.5s ease-in-out infinite alternate;
}
@keyframes neonPulse {
    0% {
        text-shadow:
            0 0 5px #10b981, 0 0 10px #10b981, 0 0 20px #10b981, 0 0 40px #10b981,
            2px 2px 0 #ec4899, -2px -2px 0 #06b6d4;
    }
    100% {
        text-shadow:
            0 0 10px #10b981, 0 0 20px #10b981, 0 0 40px #10b981, 0 0 80px #10b981,
            -2px 2px 0 #ec4899, 2px -2px 0 #06b6d4;
    }
}
</style>
