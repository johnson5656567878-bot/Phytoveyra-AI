/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/lib/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        agri: {
          dark: '#022c22',
          card: '#042f26',
          panel: '#064e3b',
          accent: '#10b981',
          teal: '#0d9488',
          amber: '#f59e0b',
          red: '#ef4444'
        }
      }
    },
  },
  plugins: [],
}
