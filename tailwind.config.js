/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        // Terminal Theme
        'term-bg': '#0d0d0d',
        'term-bg-light': '#141414',
        'term-bg-card': '#1a1a1a',
        'term-border': '#2a2a2a',
        'term-border-light': '#3a3a3a',
        'term-text': '#e5e5e5',
        'term-text-muted': '#888888',
        'term-text-dim': '#555555',
        // Accent colors (like Claude/Opencode)
        'term-accent': '#10b981',
        'term-accent-dim': '#059669',
        'term-accent-glow': 'rgba(16, 185, 129, 0.3)',
        'term-prompt': '#f59e0b',
        'term-error': '#ef4444',
        'term-link': '#3b82f6',
      },
      fontFamily: {
        'mono': ['JetBrains Mono', 'Fira Code', 'Monaco', 'Menlo', 'Consolas', 'monospace'],
      },
      boxShadow: {
        'term-glow': '0 0 30px rgba(16, 185, 129, 0.2)',
        'term-glow-sm': '0 0 15px rgba(16, 185, 129, 0.15)',
        'term-card': '0 4px 20px rgba(0, 0, 0, 0.5)',
        'term-card-hover': '0 8px 30px rgba(0, 0, 0, 0.6)',
      },
      animation: {
        'blink': 'blink 1s step-end infinite',
        'type': 'type 2s steps(20) forwards',
        'fade-in': 'fadeIn 0.3s ease forwards',
        'slide-up': 'slideUp 0.4s ease forwards',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
      },
      keyframes: {
        blink: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 15px rgba(16, 185, 129, 0.15)' },
          '50%': { boxShadow: '0 0 25px rgba(16, 185, 129, 0.3)' },
        }
      }
    }
  },
  plugins: []
}