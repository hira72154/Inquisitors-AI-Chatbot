import React from 'react';

export default function UnknownKnowledgeState({ onAskServices, onRephrase }) {
  const searchAssetUrl = "https://lh3.googleusercontent.com/aida-public/AB6AXuDv0W3wZeXMdFKckmv95D9cZPNSYaUsGfwEhcXctMxTUUxIo_lmODdE9gVipavfzNjjDTntR-MGo7shnAJWmgnat7RF7r5QR3wiHAbuNgses5AFBiLm-G98DAjXAEDNn5EhMzsUO4F0D3iwO_ywr3w477mWvfLQVp-FxYaOtAOfGK3AchUc1tvCqi4mTckPAuAZOm7e7HYDpnDbW86UYm3nl6gZ5Bym1Y-4z50Kqil_HFbrD7pqbHGkDQ";

  return (
    <div className="flex-1 flex flex-col justify-center items-center px-margin-mobile md:px-margin-desktop w-full max-w-[600px] mx-auto animate-fadeIn py-12 text-center">
      
      <div className="relative w-32 h-32 mb-8 group">
        <div className="absolute inset-0 bg-tertiary-container rounded-full opacity-30 transition-all duration-500 group-hover:scale-110"></div>
        <img 
          alt="Search Icon" 
          className="w-full h-full object-contain relative z-10 transition-transform duration-500 group-hover:rotate-12 drop-shadow-md" 
          src={searchAssetUrl} 
        />
      </div>

      <h2 className="font-headline-md text-headline-md text-on-surface mb-4">
        I'm not sure about that one yet <span className="text-tertiary inline-block">💗</span>
      </h2>

      <p className="font-body-lg text-body-lg text-on-surface-variant mb-10 max-w-md">
        I couldn't find enough information in my MAA knowledge base to give you a reliable answer. Would you like to ask me something about MAA's services?
      </p>

      <div className="flex flex-col sm:flex-row gap-4 justify-center w-full max-w-md">
        <button 
          onClick={onAskServices}
          className="bg-primary-container text-secondary px-8 py-4 rounded-full font-label-md text-label-md hover:bg-tertiary-fixed transition-colors duration-300 flex items-center justify-center gap-2 shadow-sm active:scale-95"
        >
          <span className="material-symbols-outlined text-[20px]">info</span>
          Tell me about MAA
        </button>
        
        <button 
          onClick={onRephrase}
          className="bg-surface hover:bg-surface-container-high border border-outline-variant/50 text-on-surface px-8 py-4 rounded-full font-label-md text-label-md transition-colors duration-300 flex items-center justify-center gap-2 shadow-sm active:scale-95"
        >
          <span className="material-symbols-outlined text-[20px]">edit</span>
          Rephrase my question
        </button>
      </div>
    </div>
  );
}
