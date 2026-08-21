import React from 'react';

export default function FloatingCompanion({ isOpen, onToggle }) {
  const avatarUrl = "https://lh3.googleusercontent.com/aida-public/AB6AXuBi_IDME_4eBxiyponNxrSIOhUEzZ4VIRg36P1CLmUv-B4UoDICbgNmOKbLqP4My4RihDzWiyIN0KUSrd_OCQxzvuTU9RK2MujZc7g0DmaCIWfuHG5kE0kGmevp5DpktpkQ5kxp47LWR7OIsTsKAkveRoT8HjXbe4qUXRSe2QgszaaQOSHZ-G3cojDXiJHFNyMIBc3b26wdzoQL1LGrR6f7qEfAvDP6Cw0IIguaC0Mk1Z0QAETvFNXO1Q";

  if (isOpen) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end pointer-events-auto group">
      
      {/* Subtle Speech Bubble Tooltip */}
      <div className="bg-surface-container-lowest px-3.5 py-2 rounded-2xl rounded-br-none shadow-[0_4px_16px_rgba(233,30,99,0.12)] mb-2.5 animate-bounce origin-bottom-right transition-all border border-primary-container/60 flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-secondary animate-pulse"></span>
        <p className="text-label-sm font-label-sm text-on-surface font-medium whitespace-nowrap">
          Need a little help? 💗
        </p>
      </div>

      {/* Cute Floating AI Companion Robot Button */}
      <button
        onClick={onToggle}
        className="w-14 h-14 rounded-full bg-surface-container-lowest shadow-[0_6px_24px_rgba(233,30,99,0.22)] flex items-center justify-center hover:scale-110 active:scale-95 transition-transform duration-300 relative overflow-hidden border-2 border-primary-container/80 animate-breathe"
        aria-label="Open MAA AI Companion Chatbot"
      >
        <img 
          alt="MAA Companion Robot" 
          className="w-12 h-12 object-cover rounded-full drop-shadow-sm" 
          src={avatarUrl} 
        />
        <div className="absolute top-0 right-0 w-3.5 h-3.5 bg-secondary rounded-full border-2 border-surface flex items-center justify-center">
          <span className="w-1 h-1 bg-white rounded-full"></span>
        </div>
      </button>
    </div>
  );
}
