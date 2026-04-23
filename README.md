# portfolio-cli

A terminal-style personal portfolio built with Vue 3 and Vite. The app presents portfolio content through interactive CLI commands, animated visual effects, live profile stats, and site analytics.

## Features

- Terminal-inspired portfolio interface
- Command-driven navigation with aliases and suggestions
- Animated particle background and visual easter eggs
- Live GitHub, LeetCode, and Chess.com profile stats
- Site statistics backed by a lightweight external API
- Responsive layout for desktop and mobile

## Tech Stack

- Vue 3
- Vite
- Vue Router
- Tailwind CSS
- Three.js

## Getting Started

### Prerequisites

- Node.js 18+
- npm

### Install

```bash
npm install
```

### Run Locally

```bash
npm run dev
```

### Build for Production

```bash
npm run build
```

### Preview the Production Build

```bash
npm run preview
```

## Available Commands

The portfolio UI includes commands such as:

- `/about`
- `/skills`
- `/projects`
- `/timeline`
- `/stats`
- `/profiles`
- `/site`
- `/contact`
- `/links`
- `/help`

Some commands also support shortcuts and aliases inside the app.

## Deployment

This project can be deployed directly to Netlify.

Recommended Netlify settings:

- Build command: `npm run build`
- Publish directory: `dist`

If deploying to a subpath instead of the site root, update the Vite `base` setting in `vite.config.js`.

## Notes

- `node_modules/` and `dist/` are intentionally excluded from version control
- Site stats depend on the external backend configured in `src/composables/useSiteStats.js`
