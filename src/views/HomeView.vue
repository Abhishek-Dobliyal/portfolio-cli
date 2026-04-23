<template>
    <div class="terminal-view min-h-screen flex flex-col relative z-10">
        <ParticleBg ref="particleBgRef" />

        <header class="terminal-header flex items-center gap-2 px-4 py-3 border-b border-term-border sticky top-0 bg-term-bg z-10">
            <div class="flex gap-2 shrink-0">
                <div class="w-3 h-3 rounded-full bg-term-error"></div>
                <div class="w-3 h-3 rounded-full bg-term-prompt"></div>
                <div class="w-3 h-3 rounded-full bg-term-accent"></div>
            </div>
            <div class="flex-1 text-center text-term-text-dim text-xs">abhishek@portfolio ~</div>
            <div class="text-xs text-term-text-dim hidden sm:block shrink-0">Portfolio CLI v1.0.0</div>
        </header>

        <main
            ref="terminalBody"
            class="terminal-body flex-1 p-2 sm:p-4 overflow-y-auto scrollbar-hidden"
            @click="focusInput"
        >
            <div class="term-output mb-2">
                <Typewriter :text="asciiArt" :speed="15" />
            </div>

            <div class="term-output mb-4">
                <p class="text-term-text">
                    <span class="text-accent">Abhishek Dobliyal</span> — Software Engineer
                </p>
                <p class="text-term-text-muted mt-1">
                    Building scalable solutions at <span class="text-accent">Uber</span>
                </p>
                <p class="text-term-text-dim mt-2 text-sm">
                    3+ years of experience in data engineering & backend development
                </p>
            </div>

            <div class="border-l border-term-border pl-4 mb-4">
                <p class="text-term-text-dim text-sm">
                    Type <span class="text-accent">/help</span> to see available commands
                </p>
            </div>

            <div v-for="(entry, index) in history" :key="index" class="term-output">
                <div class="flex items-start gap-2">
                    <span class="text-prompt">$</span>
                    <span class="text-term-text">{{ entry.command }}</span>
                </div>
                <div class="mt-2 pl-4" :class="{ 'border-l border-term-border': entry.hasOutput }">
                    <component
                        :is="outputComponents[entry.type]"
                        v-if="outputComponents[entry.type]"
                        v-bind="getOutputProps(entry)"
                        @select="handleUnknownSelect"
                    />
                </div>
            </div>

            <div class="term-input-line flex items-start gap-2 mt-4 mb-2">
                <span class="text-prompt">$</span>
                <div class="term-input-wrapper flex-1 relative">
                    <span class="term-input-mirror text-term-text" aria-hidden="true">
                        <template v-if="currentInput">
                            {{ inputBeforeCursor }}<span class="block-cursor"></span>{{ inputAfterCursor }}
                        </template>
                        <template v-else>
                            <span class="block-cursor"></span><span class="text-term-text-dim">Type a command...</span>
                        </template>
                    </span>
                    <input
                        ref="inputRef"
                        :value="currentInput"
                        type="text"
                        class="term-input"
                        placeholder=" "
                        @input="handleInput"
                        @compositionupdate="handleInput"
                        @focus="emptyHint = false"
                        @click="syncCursorPosition"
                        @keyup="syncCursorPosition"
                        @select="syncCursorPosition"
                        @keydown.enter="executeCommand"
                        @keydown.up.prevent="navigateHistory(-1)"
                        @keydown.down.prevent="navigateHistory(1)"
                        @keydown.tab.prevent="handleTabComplete"
                        autocomplete="off"
                        autocorrect="off"
                        autocapitalize="none"
                        spellcheck="false"
                    />
                </div>
            </div>

            <div v-if="cmdSuggestions.length" class="flex flex-wrap gap-2 mb-3">
                <span
                    v-for="cmd in cmdSuggestions"
                    :key="cmd"
                    class="cmd-suggestion text-xs px-3 py-1.5 rounded cursor-pointer"
                    @mousedown.prevent="currentInput = cmd; executeCommand()"
                    @touchend.prevent="currentInput = cmd; executeCommand()"
                >{{ cmd }}</span>
            </div>

        </main>

        <footer class="terminal-footer flex items-center justify-between px-3 sm:px-4 py-2 border-t border-term-border text-xs text-term-text-dim bg-term-bg">
            <div class="flex items-center gap-2 sm:gap-3 text-xs">
                <span>{{ currentTime }}</span>
                <span class="hidden sm:inline">YOE: <span class="text-accent">3+</span></span>
                <span class="hidden sm:inline">Company: <span class="text-accent">Uber</span></span>
                <span>cmds: <span class="text-accent">{{ commandsRun }}</span></span>
            </div>
            <div class="text-xs hidden sm:flex items-center gap-2">
                <span
                    v-if="emptyHint"
                    class="text-term-text-muted hover:text-term-text cursor-pointer"
                    @click="emptyHint = false"
                >Type a command...</span>
                <span v-else class="text-term-text-muted">Tab for autocomplete</span>
            </div>
        </footer>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

import ParticleBg     from '@/components/ParticleBg.vue'
import Typewriter     from '@/components/Typewriter.vue'
import AboutOutput    from '@/components/outputs/AboutOutput.vue'
import SkillsOutput   from '@/components/outputs/SkillsOutput.vue'
import ProjectsOutput from '@/components/outputs/ProjectsOutput.vue'
import ContactOutput  from '@/components/outputs/ContactOutput.vue'
import LinksOutput    from '@/components/outputs/LinksOutput.vue'
import ResumeOutput   from '@/components/outputs/ResumeOutput.vue'
import HelpOutput     from '@/components/outputs/HelpOutput.vue'
import TimelineOutput from '@/components/outputs/TimelineOutput.vue'
import WarpOutput     from '@/components/outputs/WarpOutput.vue'
import DnaOutput      from '@/components/outputs/DnaOutput.vue'
import GlitchOutput   from '@/components/outputs/GlitchOutput.vue'
import StatsOutput    from '@/components/outputs/StatsOutput.vue'
import ProfilesOutput from '@/components/outputs/ProfilesOutput.vue'
import SiteOutput     from '@/components/outputs/SiteOutput.vue'
import ChatOutput     from '@/components/outputs/ChatOutput.vue'
import WhoisOutput    from '@/components/outputs/WhoisOutput.vue'
import UnknownOutput  from '@/components/outputs/UnknownOutput.vue'

import { availableCommands, ALIASES, RESUME_URL } from '@/data/profile.js'
import { useSiteStats } from '@/composables/useSiteStats.js'

const particleBgRef  = ref(null)
const inputRef       = ref(null)
const terminalBody   = ref(null)
const currentInput   = ref('')
const cursorIndex    = ref(0)
const history        = ref([])
const historyIndex   = ref(-1)
const commandHistory = ref([])
const commandsRun    = ref(0)
const currentTime    = ref('')
const emptyHint      = ref(true)
const MAX_SUGGESTIONS = 3
const CLOCK_INTERVAL_MS = 1000
const CHAT_URL = 'https://portfolio-backend.koyeb.app/chat'
let clockTimerId = null

const visitorId = ref(createVisitorId())

const { status: siteStatus, rawStats, todayCount, avgSession } = useSiteStats()

const outputComponents = {
    about: AboutOutput,
    skills: SkillsOutput,
    projects: ProjectsOutput,
    contact: ContactOutput,
    links: LinksOutput,
    resume: ResumeOutput,
    help: HelpOutput,
    timeline: TimelineOutput,
    warp: WarpOutput,
    dna: DnaOutput,
    glitch: GlitchOutput,
    stats: StatsOutput,
    profiles: ProfilesOutput,
    site: SiteOutput,
    chat: ChatOutput,
    whois: WhoisOutput,
    unknown: UnknownOutput,
}

const asciiArt = `

$1⠀⠀⠀⠀⣀⡀
$1⠀⠀⠀⠀⣿⠙⣦⠀⠀⠀⠀⠀⠀⣀⣤⡶⠛⠁
$2⠀⠀⠀⠀⢻⠀⠈⠳⠀⠀⣀⣴⡾⠛⠁⣠⠂⢠⠇
$2⠀⠀⠀⠀⠈⢀⣀⠤⢤⡶⠟⠁⢀⣴⣟⠀⠀⣾
$3⠀⠀⠀⠠⠞⠉⢁⠀⠉⠀⢀⣠⣾⣿⣏⠀⢠⡇
$3⠀⠀⡰⠋⠀⢰⠃⠀⠀⠉⠛⠿⠿⠏⠁⠀⣸⠁
$4⠀⠀⣄⠀⠀⠏⣤⣤⣀⡀⠀⠀⠀⠀⠀⠾⢯⣀
$4⠀⠀⣻⠃⠀⣰⡿⠛⠁⠀⠀⠀⢤⣀⡀⠀⠺⣿⡟⠛⠁
$5⠀⡠⠋⡤⠠⠋⠀⠀⢀⠐⠁⠀⠈⣙⢯⡃⠀⢈⡻⣦
$5⢰⣷⠇⠀⠀⠀⢀⡠⠃⠀⠀⠀⠀⠈⠻⢯⡄⠀⢻⣿⣷
$6⠀⠉⠲⣶⣶⢾⣉⣐⡚⠋⠀⠀⠀⠀⠀⠘⠀⠀⡎⣿⣿⡇
$6⠀⠀⠀⠀⠀⣸⣿⣿⣿⣷⡄⠀⠀⢠⣿⣴⠀⠀⣿⣿⣿⣧
$7⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⠇⠀⢠⠟⣿⠏⢀⣾⠟⢸⣿⡇
$7⠀⠀⢠⣿⣿⣿⣿⠟⠘⠁⢠⠜⢉⣐⡥⠞⠋⢁⣴⣿⣿⠃
$8⠀⠀⣾⢻⣿⣿⠃⠀⠀⡀⢀⡄⠁⠀⠀⢠⡾ᵇʸ ᵗⁿᵏᵃ⠁
$8⠀⠀⠃⢸⣿⡇⠀⢠⣾⡇⢸⡇⠀⠀⠀⡞
$9⠀⠀⠀⠈⢿⡇⡰⠋⠈⠙⠂⠙⠢
$9⠀⠀⠀⠀⠈⢧

      +-----------------------------+
      |
      |    Abhishek Dobliyal
      |    Software Engineer
      |
      |    Portfolio CLI v1.0.0
      |
      +-----------------------------+
`

const cmdSuggestions = computed(() => {
    const input = currentInput.value.trim()
    if (!input.startsWith('/')) return []
    return availableCommands
        .filter(c => c.toLowerCase().startsWith(input.toLowerCase()))
        .slice(0, MAX_SUGGESTIONS)
})

const inputBeforeCursor = computed(() => currentInput.value.slice(0, cursorIndex.value))
const inputAfterCursor = computed(() => currentInput.value.slice(cursorIndex.value))

const COMMAND_HANDLERS = {
    '/about':    () => ({ type: 'about' }),
    '/skills':   () => ({ type: 'skills' }),
    '/projects': () => ({ type: 'projects' }),
    '/contact':  () => ({ type: 'contact' }),
    '/links':    () => ({ type: 'links' }),
    '/help':     () => ({ type: 'help' }),
    '/timeline': () => ({ type: 'timeline' }),
    '/whois':    () => ({ type: 'whois' }),
    '/glitch':   () => ({ type: 'glitch' }),
    '/stats':    () => ({ type: 'stats' }),
    '/profiles': () => ({ type: 'profiles' }),
    '/warp':     () => { particleBgRef.value?.warp(); return { type: 'warp' } },
    '/dna':      () => { particleBgRef.value?.dna();  return { type: 'dna' } },
    '/site':     () => ({ type: 'site' }),
    '/chat':     (args) => {
        if (!args) {
            return { type: 'chat', mode: 'usage', status: 'idle', response: '', error: '' }
        }

        const entry = {
            type: 'chat',
            mode: 'stream',
            prompt: args,
            response: '',
            status: 'streaming',
            error: '',
        }

        void streamChatReply(entry, getChatRequestHistory())
        return entry
    },
    '/resume':   () => { window.open(RESUME_URL, '_blank', 'noopener,noreferrer'); return { type: 'resume' } },
    '/clear':    () => { history.value = []; currentInput.value = ''; return null },
}

function createVisitorId() {
    return `VIS-${Math.random().toString(36).substring(2, 8).toUpperCase()}`
}

function getNormalizedCommand(rawCommand) {
    const trimmedCommand = rawCommand.trim().toLowerCase()
    if (!trimmedCommand) return null

    const prefixedCommand = trimmedCommand.startsWith('/')
        ? trimmedCommand
        : `/${trimmedCommand}`

    return ALIASES[trimmedCommand] ?? ALIASES[prefixedCommand] ?? prefixedCommand
}

function parseCommandInput(rawCommand) {
    const trimmedCommand = rawCommand.trim()
    if (!trimmedCommand) return null

    const [commandToken] = trimmedCommand.split(/\s+/, 1)
    const args = trimmedCommand.slice(commandToken.length).trim()

    return {
        raw: trimmedCommand,
        args,
        normalizedCommand: getNormalizedCommand(commandToken),
    }
}

function updateShareableUrl(command) {
    const url = new URL(window.location.href)

    if (!command || command === '/clear') {
        url.searchParams.delete('cmd')
    } else {
        url.searchParams.set('cmd', command.replace(/^\//, ''))
    }

    window.history.replaceState({}, '', url)
}

function runSharedCommandFromUrl() {
    const sharedCommand = new URLSearchParams(window.location.search).get('cmd')
    if (!sharedCommand) return

    const parsedCommand = parseCommandInput(sharedCommand)
    if (!parsedCommand || !COMMAND_HANDLERS[parsedCommand.normalizedCommand]) {
        updateShareableUrl(null)
        return
    }

    currentInput.value = sharedCommand
    executeCommand()
}

function focusInput() {
    nextTick(() => inputRef.value?.focus())
}

function syncCursorPosition() {
    cursorIndex.value = inputRef.value?.selectionStart ?? currentInput.value.length
}

function handleInput(event) {
    currentInput.value = event.target.value
    cursorIndex.value = event.target.selectionStart ?? currentInput.value.length
}

function updateTime() {
    currentTime.value = new Date().toLocaleTimeString('en-US', {
        hour: '2-digit', minute: '2-digit', hour12: false,
    })
}

function getOutputProps(entry) {
    if (entry.type === 'site') {
        return {
            status: siteStatus.value,
            rawStats: rawStats.value,
            todayCount: todayCount.value,
            avgSession: avgSession.value,
        }
    }

    if (entry.type === 'whois') {
        return {
            visitorCount: rawStats.value?.visitors_cnt ?? '...',
            visitorId: visitorId.value,
        }
    }

    if (entry.type === 'chat') {
        return {
            mode: entry.mode,
            status: entry.status,
            response: entry.response,
            error: entry.error,
        }
    }

    if (entry.type === 'unknown') {
        return {
            command: entry.command,
            suggestions: entry.suggestions,
        }
    }

    return {}
}

function handleUnknownSelect(command) {
    currentInput.value = command
    cursorIndex.value = command.length
    focusInput()
}

function getCommandSuggestions(command) {
    return availableCommands
        .filter(c => c.startsWith(command.toLowerCase().slice(0, 2)))
        .slice(0, MAX_SUGGESTIONS)
}

function pushHistoryEntry(command, entry) {
    entry.command = command
    entry.hasOutput = true
    entry.suggestions ??= []
    history.value.push(entry)
}

function getChatRequestHistory() {
    return history.value.flatMap((entry) => {
        if (entry.type !== 'chat' || entry.mode !== 'stream' || entry.status !== 'done') {
            return []
        }

        return [
            { role: 'user', content: entry.prompt },
            { role: 'assistant', content: entry.response.trim() },
        ]
    })
}

function processChatEvent(eventBlock, entry) {
    const dataLines = eventBlock
        .split('\n')
        .filter(line => line.startsWith('data:'))
        .map(line => line.slice(5).trim())
        .filter(Boolean)

    for (const line of dataLines) {
        if (line === '[DONE]') {
            return true
        }

        const payload = JSON.parse(line)
        if (payload.error) {
            entry.status = 'error'
            entry.error = payload.error
            return true
        }

        const content = payload.choices?.[0]?.delta?.content
        if (content) {
            entry.response += content
        }
    }

    return false
}

async function streamChatReply(entry, priorHistory) {
    try {
        const response = await fetch(CHAT_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: entry.prompt,
                history: priorHistory,
            }),
        })

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`)
        }

        if (!response.body) {
            throw new Error('Missing response stream')
        }

        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        let buffer = ''

        while (true) {
            const { value, done } = await reader.read()
            if (done) break

            buffer += decoder.decode(value, { stream: true })
            const eventBlocks = buffer.split('\n\n')
            buffer = eventBlocks.pop() ?? ''

            for (const eventBlock of eventBlocks) {
                const shouldStop = processChatEvent(eventBlock, entry)
                await nextTick()
                if (shouldStop) {
                    if (entry.status !== 'error') {
                        entry.status = 'done'
                    }

                    scrollToBottom('auto')
                    return
                }
            }

            scrollToBottom('auto')
            await new Promise(resolve => window.requestAnimationFrame(resolve))
        }

        if (buffer.trim()) {
            processChatEvent(buffer, entry)
        }

        if (entry.status !== 'error') {
            entry.status = 'done'
        }

        await nextTick()
    } catch (error) {
        entry.status = 'error'
        entry.error = 'Chat is unavailable right now. Try again shortly or use /contact.'
        console.warn('[chat] request failed:', error)
    } finally {
        scrollToBottom('auto')
    }
}

function executeCommand() {
    const parsedCommand = parseCommandInput(currentInput.value)
    if (!parsedCommand) return

    const { raw, args, normalizedCommand } = parsedCommand

    commandHistory.value.push(raw)
    historyIndex.value = -1

    const handler = COMMAND_HANDLERS[normalizedCommand]

    if (!handler) {
        pushHistoryEntry(raw, {
            type: 'unknown',
            suggestions: getCommandSuggestions(raw),
        })
        currentInput.value = ''
        commandsRun.value++
        updateShareableUrl(null)
        scrollToBottom()
        return
    }

    const result = handler(args)
    if (result === null) {
        updateShareableUrl(null)
        return
    }

    commandsRun.value++
    pushHistoryEntry(raw, result)
    currentInput.value = ''
    cursorIndex.value = 0
    updateShareableUrl(normalizedCommand === '/chat' ? null : normalizedCommand)
    scrollToBottom()
}

function scrollToBottom(behavior = 'smooth') {
    nextTick(() => {
        if (terminalBody.value) {
            terminalBody.value.scrollTo({ top: terminalBody.value.scrollHeight, behavior })
            return
        }

        window.scrollTo({ top: document.documentElement.scrollHeight, behavior })
    })
}

function navigateHistory(direction) {
    if (!commandHistory.value.length) return
    const newIndex = historyIndex.value + direction
    if (newIndex < 0) {
        historyIndex.value = -1
        currentInput.value = ''
        cursorIndex.value = 0
    } else if (newIndex < commandHistory.value.length) {
        historyIndex.value = newIndex
        currentInput.value = commandHistory.value[commandHistory.value.length - 1 - newIndex]
        cursorIndex.value = currentInput.value.length
    }
}

function handleTabComplete() {
    const input = currentInput.value.toLowerCase()
    if (!input) return
    const match = availableCommands.find(cmd => cmd.startsWith(input))
    if (match) {
        currentInput.value = match
        cursorIndex.value = match.length
    }
}

onMounted(() => {
    focusInput()
    updateTime()
    clockTimerId = window.setInterval(updateTime, CLOCK_INTERVAL_MS)
    runSharedCommandFromUrl()
})

onUnmounted(() => {
    if (clockTimerId !== null) {
        clearInterval(clockTimerId)
    }
})
</script>

<style scoped>
.terminal-view {
    background: #0d0d0d;
}

@media (max-width: 640px) {
    .terminal-view { font-size: 13px; }
    pre.text-xs { font-size: 7px !important; }
}

.term-output {
    animation: fadeIn 0.25s ease forwards;
}

.term-output > div > p,
.term-output > div > div { opacity: 0; animation: lineReveal 0.2s ease forwards; }
.term-output > div > p:nth-child(1),  .term-output > div > div:nth-child(1)  { animation-delay: 0.05s; }
.term-output > div > p:nth-child(2),  .term-output > div > div:nth-child(2)  { animation-delay: 0.12s; }
.term-output > div > p:nth-child(3),  .term-output > div > div:nth-child(3)  { animation-delay: 0.19s; }
.term-output > div > p:nth-child(4),  .term-output > div > div:nth-child(4)  { animation-delay: 0.26s; }
.term-output > div > p:nth-child(5),  .term-output > div > div:nth-child(5)  { animation-delay: 0.33s; }
.term-output > div > p:nth-child(6),  .term-output > div > div:nth-child(6)  { animation-delay: 0.40s; }
.term-output > div > p:nth-child(7),  .term-output > div > div:nth-child(7)  { animation-delay: 0.47s; }
.term-output > div > p:nth-child(8),  .term-output > div > div:nth-child(8)  { animation-delay: 0.54s; }
.term-output > div > p:nth-child(n+9),.term-output > div > div:nth-child(n+9){ animation-delay: 0.60s; }

@keyframes lineReveal {
    from { opacity: 0; transform: translateX(-6px); }
    to   { opacity: 1; transform: translateX(0); }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(5px); }
    to   { opacity: 1; transform: translateY(0); }
}

.cmd-suggestion {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #10b981;
    transition: all 0.15s ease;
}
.cmd-suggestion:hover {
    background: rgba(16, 185, 129, 0.3);
    border-color: #10b981;
}
</style>
