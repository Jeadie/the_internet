const colors = require('tailwindcss/colors')

module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
    colors: {
        test: colors.indigo,
        white: colors.white,
        grey: colors.grey,
        gray: colors.gray,
        red: colors.rose, 
    }
  },
  plugins: [],
}
