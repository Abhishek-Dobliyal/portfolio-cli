<template>
    <div class="space-y-4">
        <p class="text-accent font-bold">[ Platform Profiles ]</p>

        <div class="profile-card">
            <div class="flex items-center gap-2 mb-2">
                <span class="text-yellow-400 font-bold text-sm">LeetCode</span>
                <span v-if="!loading.leetcode" class="badge-chip text-xs">
                    {{ data.leetcode.badge }}
                </span>
                <span
                    v-if="loading.leetcode"
                    class="text-term-text-dim text-xs animate-pulse"
                    >fetching...</span
                >
            </div>
            <div v-if="!loading.leetcode" class="grid grid-cols-3 gap-2">
                <div class="stat-cell">
                    <div class="text-xl font-bold text-accent count-up">
                        {{ data.leetcode.solved }}
                    </div>
                    <div class="text-term-text-dim text-xs">Solved</div>
                </div>
                <div class="stat-cell">
                    <div class="text-xl font-bold text-accent">
                        {{ data.leetcode.contestRating }}
                    </div>
                    <div class="text-term-text-dim text-xs">Contest Rating</div>
                </div>
                <div class="stat-cell">
                    <div class="text-xl font-bold text-accent">
                        {{ data.leetcode.topPercent }}
                    </div>
                    <div class="text-term-text-dim text-xs">Top %</div>
                </div>
            </div>
            <div v-if="errors.leetcode" class="text-term-text-dim text-xs">
                {{ errors.leetcode }}
            </div>
        </div>

        <div class="profile-card">
            <div class="flex items-center gap-2 mb-2">
                <span class="text-purple-400 font-bold text-sm">GitHub</span>
                <span
                    v-if="loading.github"
                    class="text-term-text-dim text-xs animate-pulse"
                    >fetching...</span
                >
            </div>
            <div v-if="!loading.github" class="grid grid-cols-3 gap-2">
                <div class="stat-cell">
                    <div class="text-xl font-bold text-accent">
                        {{ data.github.repositories }}
                    </div>
                    <div class="text-term-text-dim text-xs">Repos</div>
                </div>
                <div class="stat-cell">
                    <div class="text-xl font-bold text-accent">
                        {{ data.github.followers }}
                    </div>
                    <div class="text-term-text-dim text-xs">Followers</div>
                </div>
                <div class="stat-cell">
                    <div class="text-sm font-bold text-accent truncate">
                        {{ data.github.username }}
                    </div>
                    <div class="text-term-text-dim text-xs">Handle</div>
                </div>
            </div>
            <div v-if="errors.github" class="text-term-text-dim text-xs">
                {{ errors.github }}
            </div>
        </div>

        <div class="profile-card">
            <div class="flex items-center gap-2 mb-2">
                <span class="text-green-400 font-bold text-sm">Chess.com</span>
                <span
                    v-if="loading.chess"
                    class="text-term-text-dim text-xs animate-pulse"
                    >fetching...</span
                >
            </div>
            <div v-if="!loading.chess" class="grid grid-cols-3 gap-2">
                <div class="stat-cell">
                    <div class="text-xl font-bold text-accent">
                        {{ data.chess.rating }}
                    </div>
                    <div class="text-term-text-dim text-xs">Rapid Rating</div>
                </div>
                <div class="stat-cell">
                    <div class="text-xl font-bold text-accent">
                        {{ data.chess.tactics }}
                    </div>
                    <div class="text-term-text-dim text-xs">Tactics Best</div>
                </div>
                <div class="stat-cell">
                    <div class="text-sm font-bold text-accent capitalize">
                        {{ data.chess.league }}
                    </div>
                    <div class="text-term-text-dim text-xs">League</div>
                </div>
            </div>
            <div v-if="errors.chess" class="text-term-text-dim text-xs">
                {{ errors.chess }}
            </div>
        </div>
    </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'

const LEETCODE_USERNAME = '1nnOcent'
const LEETCODE_PROFILE_API = `https://alfa-leetcode-api.onrender.com/${LEETCODE_USERNAME}/profile`
const LEETCODE_CONTEST_API = `https://alfa-leetcode-api.onrender.com/${LEETCODE_USERNAME}/contest`
const GITHUB_API = 'https://api.github.com/users/Abhishek-Dobliyal'
const CHESS_API = {
    profile: 'https://api.chess.com/pub/player/1nn0c3nt',
    stats: 'https://api.chess.com/pub/player/1nn0c3nt/stats',
}

const FALLBACKS = {
    leetcode: {
        solved: '900+',
        contestRating: 'N/A',
        topPercent: 'N/A',
        badge: 'N/A',
    },
    github: {
        username: 'Abhishek-Dobliyal',
        followers: 'N/A',
        repositories: 'N/A',
    },
    chess: { rating: 'N/A', tactics: 'N/A', league: 'N/A' },
}

const loading = reactive({ leetcode: true, github: true, chess: true })
const errors = reactive({ leetcode: null, github: null, chess: null })
const data = reactive({
    leetcode: { ...FALLBACKS.leetcode },
    github: { ...FALLBACKS.github },
    chess: { ...FALLBACKS.chess },
})

async function fetchJson(url) {
    const response = await fetch(url)

    if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
    }

    return response.json()
}

function formatContestRating(rating) {
    return Number.isFinite(rating) ? Math.round(rating) : FALLBACKS.leetcode.contestRating
}

function formatTopPercentage(topPercentage) {
    return Number.isFinite(topPercentage)
        ? `Top ${topPercentage}%`
        : FALLBACKS.leetcode.topPercent
}

async function fetchLeetcode() {
    try {
        const [profile, contest] = await Promise.all([
            fetchJson(LEETCODE_PROFILE_API),
            fetchJson(LEETCODE_CONTEST_API),
        ])

        data.leetcode = {
            solved: profile.totalSolved ?? FALLBACKS.leetcode.solved,
            contestRating: formatContestRating(contest.contestRating),
            topPercent: formatTopPercentage(contest.contestTopPercentage),
            badge: contest.contestBadges?.name ?? FALLBACKS.leetcode.badge,
        }
    } catch {
        errors.leetcode = 'Using cached data'
    } finally {
        loading.leetcode = false
    }
}

async function fetchGithub() {
    try {
        const json = await fetchJson(GITHUB_API)
        data.github = {
            username: json.login ?? FALLBACKS.github.username,
            followers: json.followers ?? FALLBACKS.github.followers,
            repositories: json.public_repos ?? FALLBACKS.github.repositories,
        }
    } catch {
        errors.github = 'Using cached data'
    } finally {
        loading.github = false
    }
}

async function fetchChess() {
    try {
        const [profileRes, statsRes] = await Promise.all([
            fetchJson(CHESS_API.profile),
            fetchJson(CHESS_API.stats),
        ])
        const profile = await profileRes
        const stats = await statsRes
        data.chess = {
            rating: stats?.chess_rapid?.last?.rating ?? FALLBACKS.chess.rating,
            tactics: stats?.tactics?.highest?.rating ?? FALLBACKS.chess.tactics,
            league: profile?.league ?? FALLBACKS.chess.league,
        }
    } catch {
        errors.chess = 'Using cached data'
    } finally {
        loading.chess = false
    }
}

onMounted(() => {
    Promise.allSettled([fetchLeetcode(), fetchGithub(), fetchChess()])
})
</script>

<style scoped>
.profile-card {
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: 6px;
    padding: 10px 12px;
    background: rgba(16, 185, 129, 0.04);
    transition: border-color 0.2s;
}

.profile-card:hover {
    border-color: rgba(16, 185, 129, 0.4);
}

.stat-cell {
    text-align: center;
    padding: 4px;
}

.badge-chip {
    border: 1px solid rgba(250, 204, 21, 0.25);
    border-radius: 9999px;
    padding: 2px 8px;
    color: #facc15;
    background: rgba(250, 204, 21, 0.08);
}

.count-up {
    animation: countUp 0.4s ease forwards;
}

@keyframes countUp {
    from {
        opacity: 0;
        transform: translateY(6px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
