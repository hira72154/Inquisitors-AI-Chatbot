/**
 * MAA RAG Service (Mock Implementation)
 * 
 * Future Architecture:
 * User -> MAA Frontend -> Chatbot API -> RAG Pipeline (Retriever + Vector DB) -> LLM -> MAA Response
 * 
 * To replace with real API in future:
 * Update `sendMessageToRAGPipeline(userQuery)` to perform `fetch('/api/v1/chat', { method: 'POST', body: JSON.stringify({ query: userQuery }) })`
 */

const KNOWLEDGE_BASE = [
  {
    keywords: ['service', 'services', 'provide', 'offer', 'help', 'what can you do'],
    response: "MAA brings together several helpful services, including Home & Food, Medicine & Health, Travel Assistance, and AI Companion support. I can tell you more about any of them. 💗",
    ragCard: {
      icon: 'support_agent',
      title: 'MAA Care Core Services',
      items: [
        '24/7 Emotional Companion Support',
        'Home & Food Assistance Coordination',
        'Medical & Mental Health Guidance',
        'Emergency Travel Assistance & Translation'
      ],
      source: 'MAA Knowledge Base - Services Guide v2.4'
    },
    suggestions: ['Tell me about Health', 'Home Services', 'Companion Support']
  },
  {
    keywords: ['travel', 'flight', 'trip', 'assistance', 'emergency evacuation'],
    response: "Here is some more detail on our travel assistance program based on the latest guidelines. ✈️",
    ragCard: {
      icon: 'flight',
      title: 'Travel Assistance Core Services',
      items: [
        '24/7 Itinerary Monitoring',
        'Emergency Medical Evacuation',
        'Real-time Translation Support'
      ],
      source: 'MAA Knowledge Base - Global Travel Protocol'
    },
    suggestions: ['Medical Evacuation Details', 'Language Translation', 'Contact Support']
  },
  {
    keywords: ['health', 'medicine', 'anxiety', 'feelings', 'overwhelmed', 'mental'],
    response: "I hear you. It's completely understandable to feel overwhelmed when things pile up. You're carrying a lot right now. 💗\n\nOur health & wellness services offer gentle guidance, grounding routines, and connection with medical support when needed.",
    ragCard: {
      icon: 'favorite',
      title: 'Wellness & Health Support',
      items: [
        'Daily Guided Grounding & Breathing',
        'Anxiety & Stress Assessment',
        'Caregiver & Professional Hotline Referral'
      ],
      source: 'MAA Health & Emotional Support Handbook'
    },
    suggestions: ['Grounding Exercise', 'Daily Affirmation', 'Speak to Caregiver']
  },
  {
    keywords: ['grounding', 'breathe', 'breathing', 'calm', 'relax'],
    response: "Let's take a peaceful moment together. 🌸\n\nTake a slow, deep breath in through your nose for 4 seconds... hold for 4 seconds... and gently release through your mouth for 6 seconds. You are safe, and you are doing okay.",
    ragCard: {
      icon: 'self_improvement',
      title: 'Grounding Technique (4-4-6)',
      items: [
        'Inhale gently (4 seconds)',
        'Pause & rest (4 seconds)',
        'Exhale completely (6 seconds)',
        'Repeat 3 times'
      ],
      source: 'MAA Mindful Care Library'
    },
    suggestions: ['Try another exercise', 'Daily Affirmation', 'I feel better']
  },
  {
    keywords: ['home', 'food', 'meals', 'daily'],
    response: "MAA Home & Food support connects members with local meal preparation services, nutritional guidance, and gentle reminders for daily living routines. 🏡",
    ragCard: {
      icon: 'home',
      title: 'Home Care & Meal Assistance',
      items: [
        'Nutritious Meal Scheduling',
        'Prescription & Grocery Delivery',
        'Comfort Check-ins'
      ],
      source: 'MAA Home Care Network Manual'
    },
    suggestions: ['Schedule Check-in', 'Medicine Services', 'Back to main menu']
  }
];

export async function sendMessageToRAGPipeline(query, forceStateOverride = null) {
  // Simulate network latency (0.8s to 1.4s) to emulate real LLM/RAG retrieval
  const delay = Math.floor(Math.random() * 600) + 800;
  await new Promise((resolve) => setTimeout(resolve, delay));

  const lowerQuery = query.toLowerCase().trim();

  // Check state overrides for demo testing
  if (forceStateOverride === 'error' || lowerQuery.includes('trigger_error_state')) {
    throw new Error("Unable to connect to MAA Knowledge Base API.");
  }

  if (forceStateOverride === 'unknown' || lowerQuery.includes('trigger_unknown_state')) {
    return {
      type: 'unknown',
      text: "I couldn't find enough information in my MAA knowledge base to give you a reliable answer. Would you like to ask me something about MAA's services? 💗",
      suggestions: ['Tell me about MAA', 'Rephrase my question']
    };
  }

  // Search knowledge base matching keywords
  const matched = KNOWLEDGE_BASE.find(kb => 
    kb.keywords.some(kw => lowerQuery.includes(kw))
  );

  if (matched) {
    return {
      type: 'rag',
      text: matched.response,
      ragCard: matched.ragCard,
      suggestions: matched.suggestions
    };
  }

  // Fallback friendly default response
  return {
    type: 'general',
    text: `Thank you for sharing that with me 💗 I'm here to listen, assist, and provide a comforting presence. We can take this one step at a time.`,
    suggestions: ['What can MAA help me with?', 'Tell me about health services', 'Grounding exercise']
  };
}
