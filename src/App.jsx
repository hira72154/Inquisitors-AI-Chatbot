import React, { useState } from 'react';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import FloatingCompanion from './components/chat/FloatingCompanion';
import ChatWidget from './components/chat/ChatWidget';
import { sendMessageToRAGPipeline } from './services/ragService';

export default function App() {
  const [activeNav, setActiveNav] = useState('home');

  // Floating Chatbot Widget Open/Close State (Starts closed so user sees only floating robot)
  const [isChatOpen, setIsChatOpen] = useState(false);

  // Conversation Message State
  const [messages, setMessages] = useState([
    {
      id: '1',
      sender: 'user',
      text: 'What services does MAA provide?',
      timestamp: '10:42 AM'
    },
    {
      id: '2',
      sender: 'ai',
      text: 'Of course 💗 MAA brings together several helpful services, including Home & Food, Medicine & Health, Travel Assistance, and AI Companion support.',
      timestamp: '10:42 AM'
    },
    {
      id: '3',
      sender: 'ai',
      text: 'Here is some more detail on our travel assistance program based on the latest guidelines.',
      timestamp: '10:42 AM',
      ragCard: {
        icon: 'flight',
        title: 'Travel Assistance Core Services',
        items: [
          '24/7 Itinerary Monitoring',
          'Emergency Medical Evacuation',
          'Real-time Translation Support'
        ],
        source: 'MAA Knowledge Base - Global Travel Protocol'
      }
    }
  ]);

  const [suggestedQuestions, setSuggestedQuestions] = useState([
    'Tell me about Health',
    'Home Services',
    'Companion Support'
  ]);

  const [isTyping, setIsTyping] = useState(false);

  // Handle User Message Submission
  const handleSendMessage = async (text) => {
    if (!text.trim() || isTyping) return;

    const userMsg = {
      id: Date.now().toString(),
      sender: 'user',
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsTyping(true);

    try {
      const response = await sendMessageToRAGPipeline(text);
      
      const aiMsg = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: response.text,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        ragCard: response.ragCard || null
      };

      setMessages((prev) => [...prev, aiMsg]);
      setSuggestedQuestions(response.suggestions || []);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: 'ai',
          text: "Oops, something went wrong 💗 Please take a deep breath and try again.",
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleResetChat = () => {
    setMessages([]);
    setSuggestedQuestions(['What is MAA?', 'What services does MAA provide?', 'How can MAA help me?']);
  };

  return (
    <div className="min-h-screen bg-background text-on-surface flex flex-col font-body-md relative selection:bg-primary-container selection:text-secondary">
      
      {/* Top Navbar */}
      <Header 
        activeNav={activeNav}
        setActiveNav={setActiveNav}
        onOpenChat={() => setIsChatOpen(true)}
      />

      {/* Completely Plain & Clean Main Body Canvas */}
      <main className="flex-1 flex flex-col items-center justify-center relative min-h-[calc(100vh-140px)]">
        {/* Soft background ambient blurs */}
        <div className="absolute inset-0 pointer-events-none overflow-hidden">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-container/20 rounded-full blur-[120px]"></div>
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-tertiary-container/15 rounded-full blur-[120px]"></div>
        </div>
      </main>

      {/* Floating Cute AI Companion Robot Launcher Button (Bottom-Right) */}
      <FloatingCompanion 
        isOpen={isChatOpen} 
        onToggle={() => setIsChatOpen(true)} 
      />

      {/* Floating AI Companion Chatbot Panel Modal */}
      <ChatWidget 
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        messages={messages}
        isTyping={isTyping}
        onSendMessage={handleSendMessage}
        suggestedQuestions={suggestedQuestions}
        onReset={handleResetChat}
      />

      {/* Footer */}
      <Footer />
    </div>
  );
}
