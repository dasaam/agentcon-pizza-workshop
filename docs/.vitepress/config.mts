import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "🍕 Contoso Pizza Workshop",
  description: "Contoso Pizza",
  ignoreDeadLinks: true,
  head: [['link', { rel: 'icon', href: '/favicon.ico' }]],
  lang: 'en-US',
  lastUpdated: true,
  locales: {
    root: {
      label: 'English',
      lang: 'en'
    },
    es: {
      label: 'Español',
      lang: 'es',
      themeConfig: {
        sidebar: [
          { 
            text: 'Bienvenida',
            items: [
              { text: 'Comenzar', link: '/es/index' },
              { text: 'Acerca del taller', link: '/es/about' },
            ]
          },
          {
            text: 'Configuración',
            items: [
              { text: 'Configuración del Entorno de Desarrollo', link: '/es/dev-environment' }
            ]
          },
          {
            text: 'Taller',
            items: [
              { text: '1. Configurar Microsoft Foundry', link: '/es/1_microsoft-foundry' },
              { text: '2. Crea tu primer agente', link: '/es/2_create-agent' },
              { text: '3. Agregar instrucciones', link: '/es/3_add-instructions' },
              { text: '4. Agregar conocimiento', link: '/es/4_add-knowledge' },
              { text: '5. Agregar herramienta de estimación', link: '/es/5_add-tool' },
              { text: '6. Integración de MCP', link: '/es/6_add-mcp' },
            ]
          },
          {
            text: 'Recursos',
            items: [
              { text: 'Servidor MCP de Pizza', link: '/es/pizza-mcp' },
              { text: 'Azure Classroom', link: '/es/get-azure' }
            ]
          },
          { text: 'Licencia', link: '/es/license' },
          { text: '✉️ Contacto y Retroalimentación', link: '/es/contact-feedback' }
        ],
        socialLinks: [
          { icon: 'github', link: 'https://github.com/GlobalAICommunity/agentcon-pizza-workshop' }
        ],
        search: {
          provider: 'local'
        }
      }
    }
  },
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config

    sidebar: [
      { 
        text: 'Welcome',
        items: [
          { text: 'Get started', link: '/index' },
          { text: 'About the workshop', link: '/about' },
        ]
      },
      {
        text: 'Setup',
        items: [
          
          { text: 'Developer Environment Setup', link: '/dev-environment' }
        ]
      },
      {
        text: 'Workshop',
        items: [
          { text: '1. Setup Microsoft Foundry', link: '/1_microsoft-foundry' },
          { text: '2. Create your first agent', link: '/2_create-agent' },
          { text: '3. Add instructions', link: '/3_add-instructions' },
          { text: '4. Add knowledge', link: '/4_add-knowledge' },
          { text: '5. Add estimation tool', link: '/5_add-tool' },
          { text: '6. Integrating MCP', link: '/6_add-mcp' },
        ]
      },
      {
        text: 'Resources',
        items: [
          { text: 'Pizza MCP server', link: '/pizza-mcp' },
          { text: 'Azure Classroom', link: '/get-azure' }
        ]
      },
      { text: 'License', link: '/license' },
      { text: '✉️ Contact & Feedback', link: '/contact-feedback' }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/GlobalAICommunity/agentcon-pizza-workshop' }
    ],
    search: {
      provider: 'local'
    }
  },
  
})
