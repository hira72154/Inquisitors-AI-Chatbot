import React from 'react';

export default function ChatHeader({ onClose, onReset }) {
  return (
    <div className="bg-primary-container/80 backdrop-blur-md px-5 py-3.5 flex items-center justify-between border-b border-primary-fixed-dim/40 shrink-0">
      
      {/* Brand & Online Status */}
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-full bg-surface-container-lowest flex items-center justify-center shadow-sm border border-primary-fixed-dim">
          <span className="text-secondary material-symbols-outlined text-[20px]" style={{ fontVariationSettings: "'FILL' 1" }}>
            favorite
          </span>
        </div>
        <div>
          <h3 className="text-label-md font-label-md text-on-primary-container font-bold">MAA Companion</h3>
          <div className="flex items-center gap-1.5 mt-0.5">
            <span className="w-2 h-2 rounded-full bg-secondary animate-pulse"></span>
            <span className="text-[10px] font-label-sm text-on-primary-container/80 uppercase tracking-wide font-semibold">
              Online
            </span>
          </div>
        </div>
      </div>

      {/* Header Actions */}
      <div className="flex items-center gap-1.5">
        <button
          onClick={onReset}
          title="New Conversation"
          className="w-8 h-8 rounded-full bg-surface-container-lowest/70 hover:bg-surface-container-lowest flex items-center justify-center text-on-primary-container transition-colors"
          aria-label="New Conversation"
        >
          <span className="material-symbols-outlined text-[18px]">refresh</span>
        </button>
        
        {/* Clearly Visible Close X Button */}
        <button
          onClick={onClose}
          title="Close Chatbot"
          className="w-8 h-8 rounded-full bg-surface-container-lowest hover:bg-secondary hover:text-white flex items-center justify-center text-on-primary-container transition-colors shadow-sm"
          aria-label="Close Chatbot"
        >
          <span className="material-symbols-outlined text-[18px] font-bold">close</span>
        </button>
      </div>
    </div>
  );
}
