/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin');
module.exports = {
  content: ['./src/**/*.{html,ts,scss}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Primary colors
        // Primary colors (matching the dark mode)
        primaryTail: '#ef4444', // slightly brighter red
        secondaryTail: '#f87171', // lighter warm red
        accentTail: '#fca5a5', // soft accent
        infoTail: '#fddfaf', // warm info color

        // Light mode
        bgLight: '#fefefe', // soft white background
        surfaceLight: '#fff5f5', // very light warm surface
        textLight: '#4b1c1c', // dark reddish-brown for readability

        // Dark mode
        bgDark: '#42000b',
        surfaceDark: '#f5e6d3',
        textDark: '#3b1f1c',
        primaryDarkTail: '#b83232',
        secondaryDarkTail: '#8a2e2e',
        accentDarkTail: '#c04848',
        infoDarkTail: '#d4b16f',

        // Status colors
        successTail: '#16A34A',
        warningTail: '#F59E0B',
        dangerTail: '#DC2626',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heading: ['Poppins', 'sans-serif'],
      },
      fontSize: {
        base: ['1rem', { lineHeight: '1.5rem' }],
        lg: ['1.125rem', { lineHeight: '1.75rem' }],
        xl: ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
        '5xl': ['3rem', { lineHeight: '1' }],
      },
      fontWeight: {
        normal: '400',
        medium: '500',
        semibold: '600',
        bold: '700',
      },
      lineHeight: {
        normal: '1.5',
        relaxed: '1.625',
        loose: '2',
      },
      letterSpacing: {
        tight: '-0.025em',
        normal: '0',
        wide: '0.025em',
      },
    },
  },
  plugins: [
    plugin(function ({ addVariant }) {
      // 👇 This adds a new variant that works like dark mode
      addVariant('legacy', '.legacy &');
    }),
  ],
};
