import React, { useRef, useEffect } from 'react';
import ChatHeader from './ChatHeader';
import MessageBubble from './MessageBubble';
import SuggestedQuestions from './SuggestedQuestions';
import TypingIndicator from './TypingIndicator';
import ChatInput from './ChatInput';

export default function ChatWidget({ 
  isOpen, 
  onClose, 
  messages, 
  isTyping, 
  onSendMessage, 
  suggestedQuestions, 
  onReset 
}) {
  const avatarUrl = "https://lh3.googleusercontent.com/aida-public/AB6AXuBi_IDME_4eBxiyponNxrSIOhUEzZ4VIRg36P1CLmUv-B4UoDICbgNmOKbLqP4My4RihDzWiyIN0KUSrd_OCQxzvuTU9RK2MujZc7g0DmaCIWfuHG5kE0kGmevp5DpktpkQ5kxp47LWR7OIsTsKAkveRoT8HjXbe4qUXRSe2QgszaaQOSHZ-G3cojDXiJHFNyMIBc3b26wdzoQL1LGrR6f7qEfAvDP6Cw0IIguaC0Mk1Z0QAETvFNXO1Q";

  const chatContainerRef = useRef(null);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, isTyping, isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed bottom-0 right-0 sm:bottom-6 sm:right-6 z-50 w-full h-[100vh] sm:h-[560px] sm:w-[390px] bg-surface-container-lowest sm:rounded-[2rem] shadow-[0_12px_40px_rgba(233,30,99,0.18)] flex flex-col overflow-hidden origin-bottom-right transition-all duration-300 border border-primary-container/80">
      
      {/* Header */}
      <ChatHeader onClose={onClose} onReset={onReset} />

      {/* Chat Conversation Area */}
      <div 
        ref={chatContainerRef} 
        className="flex-1 overflow-y-auto p-4 bg-surface flex flex-col gap-3.5 scroll-smooth"
      >
        {/* Welcome State when starting a new conversation */}
        {messages.length === 0 && (
          <div className="flex flex-col items-center text-center mt-2 mb-2 animate-fadeIn">
            <div className="w-16 h-16 rounded-full bg-primary-container mb-3 overflow-hidden shadow-sm border border-primary-fixed-dim/60 p-0.5">
              <img 
                alt="MAA Companion Robot" 
                className="w-full h-full object-cover rounded-full" 
                src={avatarUrl} 
              />
            </div>
            
            <h4 className="text-headline-sm font-headline-sm text-on-surface mb-1 text-lg">
              Hi! I'm your MAA Companion 💗
            </h4>
            
            <p className="text-body-md font-body-md text-on-surface-variant px-2 mb-5 text-sm">
              I'm here to listen, assist, and provide a comforting presence. How can I support you today?
            </p>

            <div className="w-full flex flex-col gap-2 mt-auto text-left">
              <p className="text-label-sm font-label-sm text-on-surface-variant ml-1 text-xs">Suggested questions:</p>
              
              <button 
                onClick={() => onSendMessage("What is MAA?")}
                className="bg-surface-container/80 hover:bg-primary-container text-on-surface px-3.5 py-2.5 rounded-xl text-left text-body-md text-xs md:text-sm transition-colors shadow-sm active:scale-[0.98] border border-outline-variant/20"
              >
                What is MAA?
              </button>
              
              <button 
                onClick={() => onSendMessage("What services does MAA provide?")}
                className="bg-surface-container/80 hover:bg-primary-container text-on-surface px-3.5 py-2.5 rounded-xl text-left text-body-md text-xs md:text-sm transition-colors shadow-sm active:scale-[0.98] border border-outline-variant/20"
              >
                What services does MAA provide?
              </button>
              
              <button 
                onClick={() => onSendMessage("How can MAA help me?")}
                className="bg-surface-container/80 hover:bg-primary-container text-on-surface px-3.5 py-2.5 rounded-xl text-left text-body-md text-xs md:text-sm transition-colors shadow-sm active:scale-[0.98] border border-outline-variant/20"
              >
                How can MAA help me?
              </button>

              <button 
                onClick={() => onSendMessage("Tell me more about MAA")}
                className="bg-surface-container/80 hover:bg-primary-container text-on-surface px-3.5 py-2.5 rounded-xl text-left text-body-md text-xs md:text-sm transition-colors shadow-sm active:scale-[0.98] border border-outline-variant/20"
              >
                Tell me more about MAA
              </button>
            </div>
          </div>
        )}

        {/* Message Stream */}
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}

        {/* Typing Indicator */}
        {isTyping && <TypingIndicator />}

        {/* Suggested Prompt Chips */}
        {!isTyping && messages.length > 0 && suggestedQuestions && suggestedQuestions.length > 0 && (
          <SuggestedQuestions 
            questions={suggestedQuestions} 
            onSelectQuestion={onSendMessage} 
          />
        )}
      </div>

      {/* Input Bar */}
      <ChatInput onSendMessage={onSendMessage} isTyping={isTyping} />
    </div>
  );
}
