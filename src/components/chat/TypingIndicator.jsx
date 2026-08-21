import React from 'react';

export default function TypingIndicator() {
  const avatarUrl = "https://lh3.googleusercontent.com/aida-public/AB6AXuBi_IDME_4eBxiyponNxrSIOhUEzZ4VIRg36P1CLmUv-B4UoDICbgNmOKbLqP4My4RihDzWiyIN0KUSrd_OCQxzvuTU9RK2MujZc7g0DmaCIWfuHG5kE0kGmevp5DpktpkQ5kxp47LWR7OIsTsKAkveRoT8HjXbe4qUXRSe2QgszaaQOSHZ-G3cojDXiJHFNyMIBc3b26wdzoQL1LGrR6f7qEfAvDP6Cw0IIguaC0Mk1Z0QAETvFNXO1Q";

  return (
    <div className="flex w-full justify-start animate-slideUp my-2">
      <div className="flex gap-4 max-w-[90%] md:max-w-[80%] items-center">
        <img 
          alt="MAA Avatar" 
          className="w-10 h-10 rounded-full shadow-sm object-cover shrink-0 border border-primary-container" 
          src={avatarUrl} 
        />
        <div className="bg-surface-container-high rounded-2xl rounded-tl-none px-4 py-3 shadow-sm flex items-center gap-3">
          <span className="text-label-sm text-on-surface-variant font-bold">MAA is typing</span>
          <div className="flex gap-1.5 items-center">
            <div className="w-1.5 h-1.5 bg-secondary rounded-full animate-[bounce_1s_infinite]"></div>
            <div className="w-1.5 h-1.5 bg-secondary rounded-full animate-[bounce_1s_infinite_0.2s]"></div>
            <div className="w-1.5 h-1.5 bg-secondary rounded-full animate-[bounce_1s_infinite_0.4s]"></div>
          </div>
        </div>
      </div>
    </div>
  );
}
