import React from 'react';
import RAGSourceCard from './RAGSourceCard';

export default function MessageBubble({ message }) {
  const avatarUrl = "https://lh3.googleusercontent.com/aida-public/AB6AXuBi_IDME_4eBxiyponNxrSIOhUEzZ4VIRg36P1CLmUv-B4UoDICbgNmOKbLqP4My4RihDzWiyIN0KUSrd_OCQxzvuTU9RK2MujZc7g0DmaCIWfuHG5kE0kGmevp5DpktpkQ5kxp47LWR7OIsTsKAkveRoT8HjXbe4qUXRSe2QgszaaQOSHZ-G3cojDXiJHFNyMIBc3b26wdzoQL1LGrR6f7qEfAvDP6Cw0IIguaC0Mk1Z0QAETvFNXO1Q";

  const isUser = message.sender === 'user';

  if (isUser) {
    return (
      <div className="flex w-full justify-end animate-slideUp">
        <div className="max-w-[85%] md:max-w-[70%]">
          <div className="bg-primary text-on-primary rounded-2xl rounded-tr-none px-6 py-4 shadow-sm relative">
            <p className="font-body-lg whitespace-pre-wrap">{message.text}</p>
            <div className="absolute -right-2 top-0 w-4 h-4 bg-primary rounded-bl-full"></div>
          </div>
          <div className="text-right mt-2 text-label-sm text-on-surface-variant opacity-70">
            {message.timestamp || 'Just now'}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex w-full justify-start animate-slideUp">
      <div className="flex gap-4 max-w-[95%] md:max-w-[85%]">
        <img 
          alt="MAA Avatar" 
          className="w-10 h-10 md:w-12 md:h-12 rounded-full shadow-sm object-cover shrink-0 self-end mb-6 border border-primary-container" 
          src={avatarUrl} 
        />
        <div className="flex flex-col gap-2 w-full">
          <div className="bg-surface-container-high text-on-surface rounded-2xl rounded-tl-none px-6 py-4 shadow-sm relative">
            <p className="font-body-lg whitespace-pre-wrap">{message.text}</p>
            <div className="absolute -left-2 top-0 w-4 h-4 bg-surface-container-high rounded-br-full"></div>
          </div>

          {/* If message includes RAG data, render RAG Card */}
          {message.ragCard && (
            <RAGSourceCard ragCard={message.ragCard} />
          )}

          <div className="text-left text-label-sm text-on-surface-variant opacity-70">
            {message.timestamp || 'Just now'}
          </div>
        </div>
      </div>
    </div>
  );
}
