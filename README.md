# 💗 MAA AI Companion — Frontend Module

> An empathetic, responsive, and RAG-ready AI companion chatbot frontend for the **MAA Care Digital Platform**. Built with **React**, **Vite**, and **Tailwind CSS**.

---

## 🌟 Overview

The **MAA AI Companion** module provides a warm, compassionate, and unobtrusive digital assistant designed to deliver emotional support, mental health guidance, and care service information.

The frontend is built to operate seamlessly as an embedded floating widget on any webpage or as a standalone care canvas. It is fully structured to connect directly to RAG-based (Retrieval-Augmented Generation) backend pipelines.

---

## ✨ Key Features

- 🤖 **Floating AI Companion Widget**:
  - Unobtrusive floating avatar located at the bottom-right corner.
  - Smooth breathing animation (`animate-breathe`) and interactive speech bubble (_"Need a little help? 💗"_).
  - Smooth modal toggle with a clear close (`X`) transition.

- 💬 **Interactive Chatbot Canvas**:
  - **Welcome Experience**: Friendly greeting (_"Hi! I'm your MAA Companion 💗"_), description, and initial prompt suggestions.
  - **Message Bubbles**: Styled user bubbles (primary brand color) and left-aligned AI response bubbles.
  - **Suggested Questions**: Quick-action prompt chips (_"What is MAA?"_, _"Tell me about health services"_).
  - **Typing Indicator**: Animated three-dot bounce state (_"MAA is typing"_).
  - **Chat Input Bar**: Auto-resizing textarea, voice microphone toggle, and circular send button.

- 📚 **RAG Knowledge Base UI**:
  - RAG source attribution cards (_"Based on MAA Knowledge Base"_).
  - Clickable `[View source]` document triggers.
  - Structured content checklists (e.g. _Travel Assistance Core Services_).

- 📱 **Mobile & Desktop Responsive**:
  - Compact floating card on desktop.
  - Full-width drawer & mobile navigation bar integration.

- 🔌 **Backend-Ready Architecture**:
  - Modular `ragService.js` handling query parsing and mock response payloads with simulated network latency.
  - Easy 1-line swap for real API integration (`POST /api/v1/chat`).

---

## 🎨 Visual Identity & Brand System

The module strictly preserves the approved MAA brand identity:

- **Primary Color**: `#6b5a60` (Muted Warm Taupe)
- **Secondary Accent**: `#b80049` (Vibrant Deep Magenta)
- **Primary Container**: `#fce4ec` (Soft Pink Backdrop)
- **Background & Surface**: `#fcf9f8` (Warm Off-White)
- **Typography**: `Quicksand` (Headlines), `Inter` (Body & Labels)
- **Aesthetic**: Soft rounded corners (`2rem`), subtle glassmorphic blurs, floating 3D heart elements.

---

## 📁 Project Architecture
