<template>
    <div class="space-y-1">
        <p class="text-cyan-400 font-bold warp-text">INITIATING WARP DRIVE...</p>
        <p class="text-term-text-dim text-xs">Fasten your seatbelt.</p>
    </div>
</template>

<style scoped>
.warp-text {
    animation: warpFlicker 0.15s infinite alternate;
    text-shadow: 0 0 10px #06b6d4, 0 0 20px #06b6d4, 0 0 40px #06b6d4;
}
@keyframes warpFlicker {
    0%   { opacity: 1; letter-spacing: 0.05em; }
    100% { opacity: 0.7; letter-spacing: 0.15em; }
}
</style>
