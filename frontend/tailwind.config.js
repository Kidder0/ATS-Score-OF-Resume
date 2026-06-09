/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      colors: {
        ink: '#18212f',
        panel: '#f7f8fb',
        line: '#d7dce5',
        accent: '#147a70',
        amber: '#b7791f',
      },
    },
  },
  plugins: [],
};

