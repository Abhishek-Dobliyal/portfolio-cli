<template>
  <div class="typewriter-container">
    <pre class="text-accent font-mono text-xs leading-tight" :style="{ minHeight: lineCount * 1.2 + 'em' }"><span>{{ displayedText }}</span><span class="cursor-blink text-accent">▋</span></pre>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  text: {
    type: String,
    required: true
  },
  speed: {
    type: Number,
    default: 30
  },
  delay: {
    type: Number,
    default: 500
  }
})

const displayedText = ref('')
const lineCount = ref(1)
let typeTimerId = null
let startDelayId = null

onMounted(() => {
  resetTyping(props.delay)
})

watch(() => props.text, () => {
  resetTyping()
})

onUnmounted(() => {
  clearTypingTimers()
})

function clearTypingTimers() {
  if (startDelayId !== null) {
    clearTimeout(startDelayId)
    startDelayId = null
  }

  if (typeTimerId !== null) {
    clearInterval(typeTimerId)
    typeTimerId = null
  }
}

function resetTyping(delay = 0) {
  clearTypingTimers()
  displayedText.value = ''
  lineCount.value = 1

  if (!props.text) {
    return
  }

  if (delay > 0) {
    startDelayId = setTimeout(() => {
      startDelayId = null
      typeText()
    }, delay)
    return
  }

  typeText()
}

function typeText() {
  const fullText = props.text
  let index = 0

  typeTimerId = setInterval(() => {
    if (index >= fullText.length) {
      clearInterval(typeTimerId)
      typeTimerId = null
      return
    }

    displayedText.value += fullText[index]
    lineCount.value = displayedText.value.split('\n').length

    index++
  }, props.speed)
}
</script>

<style scoped>
.typewriter-container {
  display: block;
  max-width: 100%;
  overflow-x: auto;
}

pre {
  white-space: pre;
  overflow-x: auto;
}

.cursor-blink {
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
</style>
