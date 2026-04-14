import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Open Avatar Chat',
  description: '模块化的交互数字人对话实现',
  base: (process.env.VITEPRESS_BASE as '/' | `/${string}/`) || '/',
  ignoreDeadLinks: [/^https?:\/\/localhost/],

  locales: {
    root: {
      label: '中文',
      lang: 'zh-CN',
      themeConfig: {
        nav: [
          { text: '指南', link: '/guide/introduction' },
          { text: '快速开始', link: '/getting-started/' },
          { text: '参考', link: '/reference/configuration' },
          { text: 'Beta', link: '/beta/' },
        ],
        sidebar: {
          '/guide/': [
            {
              text: '指南',
              items: [
                { text: '简介', link: '/guide/introduction' },
                { text: '工作原理', link: '/guide/how-it-works' },
                { text: '部署要求', link: '/guide/deployment' },
              ],
            },
          ],
          '/getting-started/': [
            {
              text: '快速开始',
              items: [
                { text: '总览', link: '/getting-started/' },
                { text: 'LiteAvatar', link: '/getting-started/liteavatar' },
                { text: 'LAM', link: '/getting-started/lam' },
                { text: 'MuseTalk', link: '/getting-started/musetalk' },
                { text: 'FlashHead', link: '/getting-started/flashhead' },
                { text: 'Docker 部署', link: '/getting-started/docker' },
              ],
            },
          ],
          '/reference/': [
            {
              text: '参考',
              items: [
                { text: '配置说明', link: '/reference/configuration' },
                { text: '预置模式', link: '/reference/preset-modes' },
              ],
            },
            {
              text: 'Handler 参考',
              items: [
                { text: '概览', link: '/reference/handlers/' },
              ],
            },
            {
              text: 'ASR（语音识别）',
              collapsed: false,
              items: [
                { text: 'SenseVoice', link: '/reference/handlers/asr/sensevoice' },
              ],
            },
            {
              text: 'LLM（大语言模型）',
              collapsed: false,
              items: [
                { text: 'OpenAI 兼容', link: '/reference/handlers/llm/openai-compatible' },
                { text: 'Qwen-Omni', link: '/reference/handlers/llm/qwen-omni' },
                { text: 'Dify', link: '/reference/handlers/llm/dify' },
              ],
            },
            {
              text: 'Agent（智能体）',
              collapsed: false,
              items: [
                { text: 'Chat Agent', link: '/reference/handlers/agent/chat-agent' },
              ],
            },
            {
              text: 'TTS（语音合成）',
              collapsed: false,
              items: [
                { text: '百炼 CosyVoice', link: '/reference/handlers/tts/bailian-cosyvoice' },
                { text: 'CosyVoice 本地', link: '/reference/handlers/tts/cosyvoice-local' },
                { text: 'Edge TTS', link: '/reference/handlers/tts/edge-tts' },
              ],
            },
            {
              text: 'VAD（语音活动检测）',
              collapsed: false,
              items: [
                { text: 'SileroVAD', link: '/reference/handlers/vad/silero-vad' },
                { text: 'Smart Turn', link: '/reference/handlers/vad/smart-turn' },
              ],
            },
            {
              text: 'Avatar（数字人）',
              collapsed: false,
              items: [
                { text: 'LiteAvatar', link: '/reference/handlers/avatar/liteavatar' },
                { text: 'LAM', link: '/reference/handlers/avatar/lam' },
                { text: 'MuseTalk', link: '/reference/handlers/avatar/musetalk' },
                { text: 'FlashHead', link: '/reference/handlers/avatar/flashhead' },
              ],
            },
            {
              text: 'Client（客户端）',
              collapsed: false,
              items: [
                { text: 'RTC', link: '/reference/handlers/client/rtc-client' },
                { text: 'WebSocket', link: '/reference/handlers/client/ws-client' },
              ],
            },
            {
              text: 'Manager（监控）',
              collapsed: false,
              items: [
                { text: '监控台', link: '/reference/handlers/manager/data-tool' },
              ],
            },
          ],
          '/beta/': [
            {
              text: 'Beta 功能',
              items: [
                { text: '总览', link: '/beta/' },
                { text: 'Chat Agent (OpenClaw)', link: '/beta/chat-agent' },
              ],
            },
          ],
          '/community/': [
            {
              text: '社区',
              items: [
                { text: '社区资源', link: '/community/' },
                { text: '常见问题', link: '/community/faq' },
              ],
            },
          ],
          '/releases/': [
            {
              text: '版本发布',
              items: [
                { text: '更新日志', link: '/releases/release-notes' },
              ],
            },
          ],
        },
      },
    },
    en: {
      label: 'English',
      lang: 'en-US',
      link: '/en/',
      themeConfig: {
        nav: [
          { text: 'Guide', link: '/en/guide/introduction' },
          { text: 'Getting Started', link: '/en/getting-started/' },
          { text: 'Reference', link: '/en/reference/configuration' },
          { text: 'Beta', link: '/en/beta/' },
        ],
        sidebar: {
          '/en/guide/': [
            {
              text: 'Guide',
              items: [
                { text: 'Introduction', link: '/en/guide/introduction' },
                { text: 'How It Works', link: '/en/guide/how-it-works' },
                { text: 'Deployment', link: '/en/guide/deployment' },
              ],
            },
          ],
          '/en/getting-started/': [
            {
              text: 'Getting Started',
              items: [
                { text: 'Overview', link: '/en/getting-started/' },
                { text: 'LiteAvatar', link: '/en/getting-started/liteavatar' },
                { text: 'LAM', link: '/en/getting-started/lam' },
                { text: 'MuseTalk', link: '/en/getting-started/musetalk' },
                { text: 'FlashHead', link: '/en/getting-started/flashhead' },
                { text: 'Docker', link: '/en/getting-started/docker' },
              ],
            },
          ],
          '/en/reference/': [
            {
              text: 'Reference',
              items: [
                { text: 'Configuration', link: '/en/reference/configuration' },
                { text: 'Preset Modes', link: '/en/reference/preset-modes' },
              ],
            },
            {
              text: 'Handler Reference',
              items: [
                { text: 'Overview', link: '/en/reference/handlers/' },
              ],
            },
            {
              text: 'ASR',
              collapsed: false,
              items: [
                { text: 'SenseVoice', link: '/en/reference/handlers/asr/sensevoice' },
              ],
            },
            {
              text: 'LLM',
              collapsed: false,
              items: [
                { text: 'OpenAI Compatible', link: '/en/reference/handlers/llm/openai-compatible' },
                { text: 'Qwen-Omni', link: '/en/reference/handlers/llm/qwen-omni' },
                { text: 'Dify', link: '/en/reference/handlers/llm/dify' },
              ],
            },
            {
              text: 'Agent',
              collapsed: false,
              items: [
                { text: 'Chat Agent', link: '/en/reference/handlers/agent/chat-agent' },
              ],
            },
            {
              text: 'TTS',
              collapsed: false,
              items: [
                { text: 'Bailian CosyVoice', link: '/en/reference/handlers/tts/bailian-cosyvoice' },
                { text: 'CosyVoice Local', link: '/en/reference/handlers/tts/cosyvoice-local' },
                { text: 'Edge TTS', link: '/en/reference/handlers/tts/edge-tts' },
              ],
            },
            {
              text: 'VAD',
              collapsed: false,
              items: [
                { text: 'SileroVAD', link: '/en/reference/handlers/vad/silero-vad' },
                { text: 'Smart Turn', link: '/en/reference/handlers/vad/smart-turn' },
              ],
            },
            {
              text: 'Avatar',
              collapsed: false,
              items: [
                { text: 'LiteAvatar', link: '/en/reference/handlers/avatar/liteavatar' },
                { text: 'LAM', link: '/en/reference/handlers/avatar/lam' },
                { text: 'MuseTalk', link: '/en/reference/handlers/avatar/musetalk' },
                { text: 'FlashHead', link: '/en/reference/handlers/avatar/flashhead' },
              ],
            },
            {
              text: 'Client',
              collapsed: false,
              items: [
                { text: 'RTC', link: '/en/reference/handlers/client/rtc-client' },
                { text: 'WebSocket', link: '/en/reference/handlers/client/ws-client' },
              ],
            },
            {
              text: 'Manager',
              collapsed: false,
              items: [
                { text: 'Console', link: '/en/reference/handlers/manager/data-tool' },
              ],
            },
          ],
          '/en/beta/': [
            {
              text: 'Beta Features',
              items: [
                { text: 'Overview', link: '/en/beta/' },
                { text: 'Chat Agent (OpenClaw)', link: '/en/beta/chat-agent' },
              ],
            },
          ],
          '/en/community/': [
            {
              text: 'Community',
              items: [
                { text: 'Resources', link: '/en/community/' },
                { text: 'FAQ', link: '/en/community/faq' },
              ],
            },
          ],
          '/en/releases/': [
            {
              text: 'Releases',
              items: [
                { text: 'Release Notes', link: '/en/releases/release-notes' },
              ],
            },
          ],
        },
      },
    },
  },

  themeConfig: {
    socialLinks: [
      { icon: 'github', link: 'https://github.com/HumanAIGC-Engineering/OpenAvatarChat' },
    ],
  },
})
