import React, { useState, useRef } from 'react';

export default function ChatInput({ onSendMessage, isTyping }) {
  const [text, setText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const textareaRef = useRef(null);

  const handleSubmit = (e) => {
    if (e) e.preventDefault();
    if (!text.trim() || isTyping) return;
    onSendMessage(text);
    setText('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInput = (e) => {
    setText(e.target.value);
    e.target.style.height = 'auto';
    e.target.style.height = `${Math.min(e.target.scrollHeight, 120)}px`;
  };

  const toggleMic = () => {
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
      alert("Voice recognition is not supported in this browser environment. You can type your message!");
      return;
    }
    
    if (isListening) {
      setIsListening(false);
      return;
    }

    try {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';

      recognition.onstart = () => setIsListening(true);
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setText((prev) => (prev ? `${prev} ${transcript}` : transcript));
        setIsListening(false);
      };
      recognition.onerror = () => setIsListening(false);
      recognition.onend = () => setIsListening(false);

      recognition.start();
    } catch (err) {
      setIsListening(false);
    }
  };

  return (
    <div className="p-4 md:p-6 bg-surface-container-lowest border-t border-outline-variant/50 relative z-10">
      <form onSubmit={handleSubmit} className="max-w-3xl mx-auto relative">
        <textarea
          ref={textareaRef}
          value={text}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          rows={1}
          disabled={isTyping}
          className="w-full bg-primary-container/30 border-0 focus:ring-2 focus:ring-secondary/70 rounded-[1.5rem] py-4 pl-6 pr-24 text-body-md text-on-surface placeholder:text-on-surface-variant/60 resize-none outline-none overflow-hidden block transition-all"
        />

        <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-2">
          {/* Microphone Voice Button */}
          <button
            type="button"
            onClick={toggleMic}
            className={`p-2 transition-colors rounded-full ${
              isListening 
                ? 'text-secondary bg-primary-container animate-pulse' 
                : 'text-on-surface-variant hover:text-secondary'
            }`}
            title={isListening ? "Listening..." : "Speak message"}
          >
            <span className="material-symbols-outlined text-[20px]">
              {isListening ? 'mic_active' : 'mic'}
            </span>
          </button>

          {/* Send Button */}
          <button
            type="submit"
            disabled={!text.trim() || isTyping}
            className={`p-2 bg-secondary text-on-secondary rounded-full shadow-md transition-all duration-300 flex items-center justify-center h-10 w-10 ${
              !text.trim() || isTyping 
                ? 'opacity-40 cursor-not-allowed' 
                : 'hover:scale-105 active:scale-95 shadow-secondary/30'
            }`}
            aria-label="Send Message"
          >
            <span className="material-symbols-outlined text-[20px]">
              send
            </span>
          </button>
        </div>
      </form>

      <div className="text-center mt-3 text-[10px] text-on-surface-variant uppercase tracking-wider font-bold opacity-80">
        MAA AI Companion - Privacy Secured
      </div>
    </div>
  );
}
