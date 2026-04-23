<template>
    <div>
        <p class="text-error">Command not found: {{ command }}</p>
        <div v-if="suggestions?.length" class="text-term-text-dim mt-1 text-xs">
            Did you mean:
            <span
                v-for="s in suggestions"
                :key="s"
                class="text-accent cursor-pointer hover:underline ml-1"
                @click="$emit('select', s)"
            >{{ s }}</span>
        </div>
        <p v-else class="text-term-text-dim mt-1">
            Type <span class="text-accent">/help</span> to see available commands
        </p>
    </div>
</template>

<script setup>
defineProps({
    command:     { type: String, required: true },
    suggestions: { type: Array, default: () => [] },
})
defineEmits(['select'])
</script>
