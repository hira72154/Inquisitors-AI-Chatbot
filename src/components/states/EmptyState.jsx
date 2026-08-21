import React from 'react';

export default function EmptyState({ onSelectSuggestion }) {
  const heartAssetUrl = "https://lh3.googleusercontent.com/aida-public/AB6AXuB2jMePGqvmgcClqk2GkWexyoXJAPpqHLdiOHnGCC2jgqL3mu27bYl6gx5o6KiQsj6H1k9Uwd_ZDcmQRKsngUko6_W_dD4eFo4_ABPzReSwv9XsdXQmeCdRTrTl1ARn0RyPNbhiGHnKGdl0e6r_AJ0-H7WLhAE3RMZ2h_Yar4o0dcdoF4JUem962Qr_AB8GlkgDh98Hc6RNFN0m0sD_9QhjKQF_Eq2X0L10qLwFCV2nkxAeZEyDcbE3cg";

  const suggestions = [
    {
      title: "Grounding Exercise",
      text: "Guide me through a quick breathing exercise to calm down.",
      icon: "self_improvement",
      prompt: "Guide me through a quick grounding breathing exercise."
    },
    {
      title: "Daily Affirmation",
      text: "I need a gentle reminder that I'm doing okay today.",
      icon: "favorite",
      prompt: "Give me a daily affirmation for emotional comfort."
    },
    {
      title: "Journal Prompts",
      text: "Give me something thoughtful to write about this evening.",
      icon: "menu_book",
      prompt: "Suggest a thoughtful journal prompt for this evening."
    },
    {
      title: "Explore Resources",
      text: "What kind of support materials are available here?",
      icon: "explore",
      prompt: "What services and support materials does MAA provide?"
    }
  ];

  return (
    <div className="flex-1 flex flex-col justify-center items-center px-margin-mobile md:px-margin-desktop w-full max-w-[800px] mx-auto animate-fadeIn py-8">
      
      {/* Soft Glowing Heart Icon inside sphere */}
      <div className="relative w-24 h-24 mb-8">
        <div className="absolute inset-0 bg-primary-fixed-dim rounded-full opacity-20 animate-pulse"></div>
        <div className="absolute inset-2 bg-primary-fixed rounded-full opacity-40 animate-pulse" style={{ animationDelay: '300ms' }}></div>
        <img 
          alt="MAA AI Heart" 
          className="w-full h-full object-contain relative z-10 drop-shadow-xl" 
          src={heartAssetUrl} 
        />
      </div>

      <h2 className="font-headline-lg text-headline-lg-mobile md:text-headline-lg text-on-surface text-center mb-8 md:mb-12">
        How can I help you today? <span className="text-secondary inline-block hover:scale-110 transition-transform cursor-default">💗</span>
      </h2>

      {/* Suggestion Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 w-full mt-2">
        {suggestions.map((card, index) => (
          <button
            key={index}
            onClick={() => onSelectSuggestion(card.prompt)}
            className="bg-surface-container hover:bg-primary-container group text-left p-6 rounded-2xl transition-all duration-300 shadow-[0_4px_20px_rgba(233,30,99,0.04)] hover:shadow-[0_8px_32px_rgba(233,30,99,0.12)] transform hover:-translate-y-1 relative overflow-hidden active:scale-[0.98]"
          >
            <div className="absolute top-0 right-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity">
              <span className="material-symbols-outlined text-secondary">arrow_outward</span>
            </div>
            
            <div className="w-10 h-10 rounded-full bg-primary-fixed text-primary flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
              <span className="material-symbols-outlined text-[20px]">{card.icon}</span>
            </div>
            
            <h3 className="font-headline-sm text-headline-sm text-on-surface mb-2">{card.title}</h3>
            <p className="font-body-md text-body-md text-on-surface-variant">{card.text}</p>
          </button>
        ))}
      </div>
    </div>
  );
}
