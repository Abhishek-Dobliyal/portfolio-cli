export const RESUME_URL =
    'https://drive.google.com/file/d/1h1MEm_h5jmMzcSxRpa4lmwktLdaww2wD/view'

export const BLOG_URL =
    'https://www.uber.com/gb/en/blog/from-archival-to-access/'

export const profile = {
    intro: 'Backend and data engineer at Uber, currently based in Amsterdam. I build systems that move and process data at scale — pipelines, APIs, and the unglamorous-but-critical plumbing that keeps things running. I pick up new tech stacks out of curiosity and have a habit of turning that curiosity into side projects.',
    company: 'Uber',
    role: 'Software Engineer II',
    team: 'Capacity & Efficiency',
    location: 'Amsterdam, Netherlands',
    interests: 'I gravitate toward problems that require pulling apart a system and rebuilding it better — whether that is optimising a data pipeline, designing a cleaner API, or just figuring out why something is slow. I enjoy working across the stack and have shipped everything from ML-backed desktop apps to backend services handling real-world traffic.',
    hobbies: 'Outside work: music on loop, horror movies, and football. Also a competitive Call of Duty: Mobile player — currently sitting in the top 4K on the server.',
    skills: {
        languages:  ['Python', 'JavaScript', 'TypeScript', 'Go', 'SQL'],
        frameworks: ['FastAPI', 'Flask', 'Vue.js', 'GoFiber', 'Bootstrap'],
        data:       ['Apache Spark', 'PySpark', 'Apache Airflow', 'MongoDB', 'MySQL'],

    },
    projects: [
        {
            title:       'Calculation Pad',
            description: 'Write a math expression by hand. The model reads it, evaluates it. No keyboard needed.',
            points: [
                'Trained CNNs to recognise handwritten digits and symbols, then chain them into a full expression — 97% accuracy.',
                'Shipped as both a desktop app (Tkinter) and a web app (Streamlit) so it works wherever you are.',
            ],
            tech: ['Python', 'TensorFlow', 'Keras', 'OpenCV', 'Streamlit', 'Tkinter'],
        },
        {
            title:       'Neural Style Transfer',
            description: 'Take any two images — one for content, one for style — and merge them into something new.',
            points: [
                'Built on VGG19 via transfer learning for fast, high-quality stylisation without training from scratch.',
                'Full-stack web app with sliders to dial in the content-to-style ratio in real time.',
            ],
            tech: ['Python', 'TensorFlow', 'Keras', 'FastAPI', 'Vue.js', 'JavaScript'],
        },
        {
            title:       'Falcon',
            description: 'A lightweight remote monitoring tool — control a machine over plain HTTP.',
            points: [
                'Admin web portal to monitor connected systems in real time.',
                'Supports remote screenshots, webcam snaps, and system actions from the browser.',
            ],
            tech: ['Python', 'Flask', 'MongoDB', 'Bootstrap', 'JavaScript'],
        },
    ],
    socials: {
        github:   'https://github.com/Abhishek-Dobliyal',
        linkedin: 'https://linkedin.com/in/abhishekdobliyal',
        leetcode: 'https://leetcode.com/u/1nnOcent/',
    },
}

export const timelineData = [
    {
        year:        'Now',
        duration:    'Apr 2025 – Present',
        role:        'Software Engineer II',
        company:     'Uber — Amsterdam, Netherlands',
        description: 'Moved to Amsterdam to join the Capacity & Efficiency team as a backend and data engineer.',
        points: [
            'Working on backend systems and data pipelines focused on capacity planning and efficiency at scale.',
        ],
    },
    {
        year:        'Jun 2023',
        duration:    'Jun 2023 – Apr 2025',
        role:        'Software Engineer',
        company:     'Uber',
        description: 'Full-stack data and backend engineering across regulatory, compliance, and platform work — shipping at scale across pipelines, APIs, and tooling.',
        points: [
            'Led the revamp of CPUC regulatory reporting — a $4B market in gross bookings — cutting operations team manual effort by ~95% across ~260M processed trips.',
            'Built full-stack web apps for the Global Operations Compliance team automating COLD storage retrieval, jurisdiction backfills, and report management — ~70% reduction in manual work.',
            'Developed a real-time anomaly forecasting API capable of serving up to 5M requests/day across multiple granularities.',
            'Built a near real-time regulatory reporting pipeline pushing ~15K trip records and ~10K partner payments every 4 hours.',
            'Shipped multiple MCP servers for workflow and query automation — one became the org-wide standard, crossing 100 users within 30 days of launch.',
            'Migrated 56 CDS datasets (10 TB, ORC → Parquet) and redesigned the retrieval workflow from Terrablob to HDFS, cutting retrieval time by 85%.',
        ],
    },
    {
        year:        'May 2023',
        duration:    'May 2023 – Jul 2023',
        role:        'SWE Intern',
        company:     "Zuma (YC'21)",
        description: 'Backend intern on the integrations team at a proptech startup backed by Y Combinator.',
        points: [
            'Designed and shipped the TourTypes API — enabling community-level tour type retrieval from the ground up.',
            'Integrated UIF client services to bridge internal systems with third-party platforms.',
            'Built the CancelLead API to automatically expire stale leads and reduce manual overhead.',
            'Wrote unit tests across Yardi Integrations and the UIF client service.',
        ],
    },
    {
        year:        'May 2022',
        duration:    'May 2022 – Jul 2022',
        role:        'SWE Intern',
        company:     'Uber',
        description: 'Joined the Customer Obsession Proactive team — focused on reducing early rider churn.',
        points: [
            'Wired the Proactive Outreach platform into the Policy Engine to fully automate outreach resolution.',
            'Built the Deterministic Trigger Controller from scratch to gate automation on existing coverage checks.',
            'Shipped an end-to-end workflow that automatically identified and targeted at-risk riders.',
        ],
    },
    {
        year:        'Aug 2021',
        duration:    'Aug 2021 – Apr 2022',
        role:        'Research Intern',
        company:     'Samsung SRIB',
        description: 'First industry role — embedded in a research team working on camera sensor validation tooling.',
        points: [
            'Built validation and parsing logic for UX documents and camera source files.',
            'Designed a desktop GUI to streamline the validation workflow for the team.',
            'Added report generation and log parsing directly into the application.',
        ],
    },
]

export const skillBars = [
    { domain: 'Backend',          pct: 70, skills: ['Python', 'Go', 'FastAPI', 'Flask', 'GoFiber', 'REST APIs'] },
    { domain: 'Frontend',         pct: 60, skills: ['HTML/CSS', 'JavaScript', 'Vue.js', 'Tailwind', 'Bootstrap'] },
    { domain: 'Data Engineering', pct: 65, skills: ['Apache Spark', 'PySpark', 'MySQL', 'MongoDB', 'Airflow'] },
]

export const statsConfig = [
    { label: 'Years of Experience', value: 3,  hasSuffix: true  },
    { label: 'Companies',           value: 4,  hasSuffix: false },
    { label: 'Projects Built',      value: 10, hasSuffix: true  },
]

export const availableCommands = [
    '/about', '/skills', '/projects', '/timeline',
    '/contact', '/links', '/resume', '/help', '/clear',
    '/stats', '/profiles', '/whois', '/glitch', '/warp', '/dna', '/site',
]

export const ALIASES = {
    site:     '/site',
    about:    '/about',
    skills:   '/skills',
    projects: '/projects',
    contact:  '/contact',
    links:    '/links',
    help:     '/help',
    clear:    '/clear',
    whois:    '/whois',
    glitch:   '/glitch',
    timeline: '/timeline',
    warp:     '/warp',
    dna:      '/dna',
    stats:    '/stats',
    profiles: '/profiles',
    ls:       '/links',
    whoami:   '/whois',
    man:      '/help',
    pwd:      '/about',
    resume:   '/resume',
    cls:      '/clear',
    ping:     '/contact',
    exp:      '/timeline',
    proj:     '/projects',
    neofetch: '/stats',
    handles:  '/profiles',
    uptime:   '/site',
}
