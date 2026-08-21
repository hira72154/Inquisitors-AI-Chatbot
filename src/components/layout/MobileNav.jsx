import React from 'react';

export default function MobileNav({ activeTab, setActiveTab, onToggleChat }) {
  return (
    <nav className="md:hidden fixed bottom-0 w-full z-40 pb-safe bg-surface/90 backdrop-blur-xl shadow-[0_-1px_8px_rgba(233,30,99,0.08)] border-t border-outline-variant/30">
      <div className="flex justify-around items-center h-16 px-4">
        
        {/* Home */}
        <button
          onClick={() => setActiveTab('home')}
          className={`flex flex-col items-center justify-center w-14 h-14 transition-all ${
            activeTab === 'home' 
              ? 'text-secondary bg-primary-container/40 rounded-xl' 
              : 'text-on-surface-variant'
          }`}
        >
          <span className="material-symbols-outlined">home</span>
          <span className="font-label-sm text-[10px]">Home</span>
        </button>

        {/* Explore */}
        <button
          onClick={() => setActiveTab('explore')}
          className={`flex flex-col items-center justify-center w-14 h-14 transition-all ${
            activeTab === 'explore' 
              ? 'text-secondary bg-primary-container/40 rounded-xl' 
              : 'text-on-surface-variant'
          }`}
        >
          <span className="material-symbols-outlined">explore</span>
          <span className="font-label-sm text-[10px]">Explore</span>
        </button>

        {/* Center Floating Robot Launcher Button */}
        <div className="relative -top-5">
          <button 
            onClick={onToggleChat}
            className="w-14 h-14 bg-secondary text-on-secondary rounded-full flex items-center justify-center shadow-lg shadow-secondary/30 active:scale-95 transition-transform hover:scale-105"
            aria-label="Open MAA AI Companion"
          >
            <span className="material-symbols-outlined text-3xl">smart_toy</span>
          </button>
        </div>

        {/* Library */}
        <button
          onClick={() => setActiveTab('resources')}
          className={`flex flex-col items-center justify-center w-14 h-14 transition-all ${
            activeTab === 'resources' 
              ? 'text-secondary bg-primary-container/40 rounded-xl' 
              : 'text-on-surface-variant'
          }`}
        >
          <span className="material-symbols-outlined">book</span>
          <span className="font-label-sm text-[10px]">Library</span>
        </button>

        {/* Profile */}
        <button
          onClick={() => setActiveTab('profile')}
          className={`flex flex-col items-center justify-center w-14 h-14 transition-all ${
            activeTab === 'profile' 
              ? 'text-secondary bg-primary-container/40 rounded-xl' 
              : 'text-on-surface-variant'
          }`}
        >
          <span className="material-symbols-outlined">account_circle</span>
          <span className="font-label-sm text-[10px]">Profile</span>
        </button>

      </div>
    </nav>
  );
}
