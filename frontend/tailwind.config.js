/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        theme: {
          primary: "rgb(var(--theme-primary) / <alpha-value>)",
          primaryDark: "rgb(var(--theme-primary-dark) / <alpha-value>)",
          bg: "rgb(var(--bg-main) / <alpha-value>)",
          card: "rgb(var(--bg-card) / <alpha-value>)",
          text: {
            primary: "rgb(var(--text-primary) / <alpha-value>)",
            secondary: "rgb(var(--text-secondary) / <alpha-value>)",
          },
        },
      },
    },
  },
}
