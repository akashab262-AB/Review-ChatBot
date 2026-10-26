/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f5ff',
          100: '#e0ebff',
          200: '#c7d9fe',
          300: '#a4bffe',
          400: '#799cfc',
          500: '#5275f8',
          600: '#3553ee',
          700: '#263ed6',
          800: '#2133ad',
          900: '#1e2e88',
          950: '#141d52',
        },
        navy: {
          800: '#152238',
          900: '#0d1626',
          950: '#070c17',
        },
        status: {
          approved: '#10b981',
          approvedBg: '#ecfdf5',
          approvedBorder: '#a7f3d0',
          correction: '#f59e0b',
          correctionBg: '#fffbeb',
          correctionBorder: '#fde68a',
          pending: '#3b82f6',
          pendingBg: '#eff6ff',
          pendingBorder: '#bfdbfe',
          manual: '#8b5cf6',
          manualBg: '#f5f3ff',
          manualBorder: '#ddd6fe',
          overdue: '#ef4444',
          overdueBg: '#fef2f2',
          overdueBorder: '#fecaca',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      boxShadow: {
        card: '0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.05)',
        'card-hover': '0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04)',
        soft: '0 4px 20px -2px rgba(15, 23, 42, 0.05)',
      }
    },
  },
  plugins: [],
}
