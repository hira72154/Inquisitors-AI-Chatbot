/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "primary-fixed": "#f4dce4",
        "primary-fixed-dim": "#d7c1c8",
        "secondary-fixed-dim": "#ffb2be",
        "surface-dim": "#dcd9d9",
        "on-background": "#1b1c1c",
        "inverse-on-surface": "#f3f0f0",
        "outline-variant": "#d0c3c7",
        "on-tertiary": "#ffffff",
        "error-container": "#ffdad6",
        "secondary-container": "#e2165f",
        "on-primary-fixed-variant": "#524249",
        "inverse-surface": "#303030",
        "inverse-primary": "#d7c1c8",
        "on-tertiary-container": "#b93768",
        "tertiary-fixed": "#ffd9e1",
        "on-primary": "#ffffff",
        "secondary": "#b80049",
        "on-error-container": "#93000a",
        "on-secondary-fixed-variant": "#900038",
        "tertiary-fixed-dim": "#ffb1c5",
        "surface-container": "#f0eded",
        "on-error": "#ffffff",
        "on-tertiary-fixed-variant": "#8b0e45",
        "surface-variant": "#e4e2e1",
        "on-secondary-container": "#fffbff",
        "surface-container-highest": "#e4e2e1",
        "on-secondary-fixed": "#400014",
        "background": "#fcf9f8",
        "surface": "#fcf9f8",
        "surface-container-low": "#f6f3f2",
        "surface-bright": "#fcf9f8",
        "tertiary": "#ab2c5d",
        "error": "#ba1a1a",
        "on-secondary": "#ffffff",
        "primary": "#6b5a60",
        "on-primary-fixed": "#25181e",
        "on-tertiary-fixed": "#3f001b",
        "tertiary-container": "#ffe3e8",
        "secondary-fixed": "#ffd9de",
        "on-surface": "#1b1c1c",
        "on-surface-variant": "#4d4447",
        "surface-tint": "#6b5a60",
        "surface-container-lowest": "#ffffff",
        "outline": "#7f7478",
        "primary-container": "#fce4ec",
        "surface-container-high": "#eae7e7",
        "on-primary-container": "#76646b"
      },
      borderRadius: {
        DEFAULT: "1rem",
        lg: "2rem",
        xl: "3rem",
        full: "9999px"
      },
      spacing: {
        gutter: "24px",
        unit: "8px",
        "margin-mobile": "16px",
        "section-gap": "80px",
        "container-max": "1200px",
        "margin-desktop": "48px"
      },
      fontFamily: {
        "headline-lg-mobile": ["Quicksand", "sans-serif"],
        "headline-md": ["Quicksand", "sans-serif"],
        "headline-sm": ["Quicksand", "sans-serif"],
        "headline-lg": ["Quicksand", "sans-serif"],
        "label-sm": ["Inter", "sans-serif"],
        "body-lg": ["Inter", "sans-serif"],
        "body-md": ["Inter", "sans-serif"],
        "label-md": ["Inter", "sans-serif"]
      },
      fontSize: {
        "headline-lg-mobile": ["32px", { lineHeight: "40px", letterSpacing: "-0.02em", fontWeight: "700" }],
        "headline-md": ["32px", { lineHeight: "40px", fontWeight: "600" }],
        "headline-sm": ["24px", { lineHeight: "32px", fontWeight: "600" }],
        "headline-lg": ["48px", { lineHeight: "56px", letterSpacing: "-0.02em", fontWeight: "700" }],
        "label-sm": ["12px", { lineHeight: "16px", fontWeight: "600" }],
        "body-lg": ["18px", { lineHeight: "28px", fontWeight: "400" }],
        "body-md": ["16px", { lineHeight: "24px", fontWeight: "400" }],
        "label-md": ["14px", { lineHeight: "20px", letterSpacing: "0.01em", fontWeight: "500" }]
      },
      keyframes: {
        breathe: {
          '0%, 100%': { transform: 'translateY(0) scale(1)' },
          '50%': { transform: 'translateY(-5px) scale(1.02)' }
        },
        slideUp: {
          from: { opacity: '0', transform: 'translateY(20px)' },
          to: { opacity: '1', transform: 'translateY(0)' }
        },
        fadeIn: {
          from: { opacity: '0', transform: 'translateY(10px)' },
          to: { opacity: '1', transform: 'translateY(0)' }
        }
      },
      animation: {
        breathe: 'breathe 4s ease-in-out infinite',
        slideUp: 'slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards',
        fadeIn: 'fadeIn 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards'
      }
    }
  },
  plugins: []
}
