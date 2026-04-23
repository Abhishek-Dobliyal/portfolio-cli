import { ref, computed, onMounted, onUnmounted } from 'vue'

const GET_URL    = 'https://portfolio-backend.koyeb.app/get-stats'
const UPDATE_URL = 'https://portfolio-backend.koyeb.app/update-stats'
const TIMEOUT_MS = 8000
const SITE_STATUS = Object.freeze({
    loading: 'loading',
    ready: 'ready',
    asleep: 'asleep',
})

export function useSiteStats() {
    const status       = ref(SITE_STATUS.loading)
    const rawStats     = ref(null)
    const sessionStart = Date.now()
    const todayKey     = new Date().toISOString().slice(0, 10)
    let updateSent = false

    const todayCount = computed(() => {
        if (!rawStats.value) return 0
        return rawStats.value.current_day_cnt?.[todayKey] ?? 0
    })

    const avgSession = computed(() => {
        if (!rawStats.value) return 'N/A'
        const secs = Math.round(rawStats.value.avg_session_seconds ?? 0)
        if (secs < 60) return `${secs}s`
        return `${Math.floor(secs / 60)}m ${secs % 60}s`
    })

    function buildPayload(sessionSeconds) {
        const base = rawStats.value
        if (!base) return null

        const newVisitorsCnt = (base.visitors_cnt ?? 0) + 1
        const newConnectCnt = (base.connect_attempt_cnt ?? 0) + 1

        const newCurrentDay = { ...(base.current_day_cnt ?? {}) }
        newCurrentDay[todayKey] = (newCurrentDay[todayKey] ?? 0) + 1

        const todayTotal = newCurrentDay[todayKey]
        let newMaxVisits = { ...(base.max_visits ?? {}) }
        if (todayTotal > (newMaxVisits.cnt ?? 0)) {
            newMaxVisits = { cnt: todayTotal, date: todayKey }
        }

        const oldAvg = base.avg_session_seconds ?? 0
        const oldCnt = base.connect_attempt_cnt  ?? 0
        const newAvg = oldCnt === 0
            ? sessionSeconds
            : ((oldAvg * oldCnt) + sessionSeconds) / (oldCnt + 1)

        return {
            visitors_cnt:        newVisitorsCnt,
            tab_stats:           base.tab_stats ?? {},
            max_visits:          newMaxVisits,
            current_day_cnt:     newCurrentDay,
            connect_attempt_cnt: newConnectCnt,
            avg_session_seconds: Math.round(newAvg * 100) / 100,
        }
    }

    async function postUpdate() {
        if (updateSent || !rawStats.value) return
        updateSent = true

        const sessionSeconds = Math.round((Date.now() - sessionStart) / 1000)
        const payload = buildPayload(sessionSeconds)
        if (!payload) return

        try {
            await fetch(UPDATE_URL, {
                method:    'POST',
                keepalive: true,
                headers:   { 'Content-Type': 'application/json' },
                body:      JSON.stringify(payload),
            })

            rawStats.value = payload
        } catch (err) {
            console.warn('[useSiteStats] update failed silently:', err)
        }
    }

    function onVisibilityChange() {
        if (document.visibilityState === 'hidden') postUpdate()
    }

    async function init() {
        const controller = new AbortController()
        const timerId = setTimeout(() => controller.abort(), TIMEOUT_MS)

        try {
            const res = await fetch(GET_URL, { signal: controller.signal })

            if (!res.ok) throw new Error(`HTTP ${res.status}`)
            const json = await res.json()

            if (json?.data) {
                rawStats.value = json.data
                status.value = SITE_STATUS.ready
            } else {
                status.value = SITE_STATUS.asleep
            }
        } catch {
            status.value = SITE_STATUS.asleep
        } finally {
            clearTimeout(timerId)
        }
    }

    onMounted(() => {
        init()
        window.addEventListener('beforeunload', postUpdate)
        document.addEventListener('visibilitychange', onVisibilityChange)
    })

    onUnmounted(() => {
        window.removeEventListener('beforeunload', postUpdate)
        document.removeEventListener('visibilitychange', onVisibilityChange)
    })

    return { status, rawStats, todayCount, avgSession }
}
