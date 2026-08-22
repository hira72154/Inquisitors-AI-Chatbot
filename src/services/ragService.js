const API_URL = "/api";

export async function sendMessageToRAGPipeline(message) {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: "frontend-user",
      session_id: "maa-session-001",
      message: message,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Backend error: ${errorText}`);
  }

  const data = await response.json();

  return {
    text: data.reply,
    suggestions: getSuggestions(message),
    ragCard: null,
    sources: data.sources || [],
  };
}

function getSuggestions(message) {
  const text = message.toLowerCase();

  if (text.includes("travel") || text.includes("trip")) {
    return [
      "How do I plan a trip?",
      "What emergency travel support is available?",
      "What are the popular destinations?",
    ];
  }

  if (
    text.includes("medicine") ||
    text.includes("health") ||
    text.includes("medical")
  ) {
    return [
      "What medicines are available?",
      "How can I order medicine?",
      "What health services does MAA provide?",
    ];
  }

  if (
    text.includes("food") ||
    text.includes("grocery") ||
    text.includes("meal")
  ) {
    return [
      "What food services are available?",
      "Can MAA help with groceries?",
      "What home-made food is available?",
    ];
  }

  return [
    "What services does MAA provide?",
    "How can MAA help me?",
    "Tell me about Travel Assistance",
  ];
}
