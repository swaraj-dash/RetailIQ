/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#F5F8FC',
        surface: '#FFFFFF',
        'text-primary': '#001F5A',
        'text-secondary': '#475569',
        primary: {
          DEFAULT: '#2662EC',
          hover: '#164BDB',
          light: '#EBF1FD',
        },
        cyan: {
          DEFAULT: '#08C2FF',
          surface: '#EAF9FF',
          border: '#B6EEFF',
        },
        navy: {
          900: '#00133A',
          800: '#001F5A',
          700: '#062B75',
          600: '#0A3995',
        },
        border: '#DCE4F0',
        success: {
          DEFAULT: '#166534',
          surface: '#ECFDF3',
          border: '#BBF7D0',
        },
        review: {
          DEFAULT: '#9A3412',
          surface: '#FFF7ED',
          border: '#FED7AA',
        },
        error: {
          DEFAULT: '#B91C1C',
          surface: '#FEF2F2',
          border: '#FECACA',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
      boxShadow: {
        card: '0 2px 10px rgba(0, 31, 90, 0.06)',
        dropdown: '0 10px 25px -5px rgba(0, 31, 90, 0.1), 0 8px 10px -6px rgba(0, 31, 90, 0.06)',
      },
      borderRadius: {
        card: '12px',
        input: '8px',
      },
    },
  },
  plugins: [],
}
