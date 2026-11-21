import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/nexus-pilot-cortex/',
  title: 'NexusPilot Cortex',
  description: 'Cognitive Telemetry, Persistent Memory Governor & Context Compression Engine for AI Coding Agents',

  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/nexus-pilot-cortex/assets/logo.svg' }],
    ['meta', { name: 'author', content: 'Nishant Shaligram' }],
    ['meta', { name: 'keywords', content: 'ai agent, mcp, model context protocol, claude-mem, headroom, token counter, context compression, prompt caching, antigravity, claude code, cursor ide, windsurf' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'NexusPilot Cortex - Cognitive Engine for AI Agents' }],
    ['meta', { property: 'og:description', content: 'Per-response token telemetry, claude-mem style persistent long-term memory, and headroom-style context compression.' }],
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }]
  ],

  themeConfig: {
    logo: '/assets/logo.svg',
    siteTitle: 'NexusPilot Cortex',

    search: {
      provider: 'local'
    },

    nav: [
      { text: 'Home', link: '/' },
      { text: 'Quickstart', link: '/getting-started/quickstart' },
      { text: 'Architecture', link: '/architecture/telemetry' },
      { text: 'Integrations', link: '/integrations/antigravity' },
      { text: 'Tools Reference', link: '/reference/mcp-tools' }
    ],

    sidebar: [
      {
        text: 'Getting Started',
        collapsed: false,
        items: [
          { text: 'Overview', link: '/' },
          { text: 'Installation', link: '/getting-started/installation' },
          { text: 'Quickstart Guide', link: '/getting-started/quickstart' }
        ]
      },
      {
        text: 'Architecture & Engineering',
        collapsed: false,
        items: [
          { text: 'Token Telemetry Engine', link: '/architecture/telemetry' },
          { text: 'Autonomous Memory Engine', link: '/architecture/memory' },
          { text: 'Context & Headroom Compressor', link: '/architecture/compressor' }
        ]
      },
      {
        text: 'Agent Integrations',
        collapsed: false,
        items: [
          { text: 'Google Antigravity', link: '/integrations/antigravity' },
          { text: 'Claude (Code & Desktop)', link: '/integrations/claude' },
          { text: 'Cursor & Windsurf', link: '/integrations/cursor' }
        ]
      },
      {
        text: 'API & Reference',
        collapsed: false,
        items: [
          { text: 'MCP Tool Catalog', link: '/reference/mcp-tools' },
          { text: 'Supported Models & Pricing', link: '/reference/models' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/nishantshaligram/nexus-pilot-cortex' }
    ],

    footer: {
      message: 'Released under the Apache 2.0 License.',
      copyright: 'Copyright © 2026 Nishant Shaligram'
    }
  }
})
