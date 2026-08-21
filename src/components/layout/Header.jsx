import React from 'react';

export default function Header({ activeNav, setActiveNav, onOpenChat }) {
  const logoUrl = "https://lh3.googleusercontent.com/aida-public/AB6AXuDtqKJj23wxqVgID2_7bKSk1E1UpVdMNH3_-s7yMkGvF5-7RtnfV0s0jPQ97MWmJKijEKBzoQpeHs4C0PTUXbjHTKrGAPuo7TuRR7IxaqAoT3po29Ak3PdQtWJxfUGdZNMkGZ0F9vqlU2jq82Cg1AkDXE2cb32mwYzYUhTmxxoGQM74e3tOt06r_gIRuvolHUr2sMf-8Gwtlk_XpGxGebvmh-SYaCQUaGxTvB557WVIvjz19g6dPsDMcw";
  const profileUrl = "https://lh3.googleusercontent.com/aida-public/AB6AXuDUxMrDS8laDWVDF7FBGbt7yFu5nxAOUbcYX42-N8awfV5jxxUS2Zh0qgInv2UUgtG6CMCH17AedOZsRw5i3Rxu3qi4yaqJDFPlv45ZpAnLZ7C_CR0lppDQhiCMlJ9EqjWjUpS_ekhvhH9EhoYHgGX9BDli6h5UmzgQeaCpNwdyl253oITKOlsVnzZWG3tTI8bMuzBgyOJAaEAfebXwDnI8ffmVXmA5AqxWDo5OGI-3BrdxCZBBTIfkxA";

  const navItems = [
    { id: 'home', label: 'Home' },
    { id: 'services', label: 'Services' },
    { id: 'support', label: 'Support' },
    { id: 'about', label: 'About' }
  ];

  return (
    <header className="fixed top-0 w-full z-50 bg-surface/80 backdrop-blur-xl shadow-[0_2px_15px_rgba(233,30,99,0.06)] border-b border-primary-container/40">
      <div className="h-20 max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop flex items-center justify-between">
        
        {/* Brand Logo & Name */}
        <div className="flex items-center gap-3.5 cursor-pointer" onClick={() => setActiveNav('home')}>
          <img 
            alt="MAA Logo" 
            className="h-8 w-auto object-contain" 
            src={logoUrl} 
          />
          <span className="font-headline-sm text-headline-sm text-primary font-bold tracking-tight">MAA</span>
        </div>

        {/* Navigation Links */}
        <nav className="hidden md:flex items-center gap-8">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveNav(item.id)}
              className={`transition-colors text-label-md font-label-md ${
                activeNav === item.id 
                  ? 'text-secondary font-bold border-b-2 border-secondary pb-1' 
                  : 'text-on-surface-variant hover:text-secondary'
              }`}
            >
              {item.label}
            </button>
          ))}
        </nav>

        {/* Right Actions */}
        <div className="flex items-center gap-3">
          {/* Quick Chat Launcher Button */}
          <button 
            onClick={onOpenChat}
            className="hidden sm:flex items-center gap-2 bg-primary-container/60 hover:bg-primary-container text-secondary px-4 py-2 rounded-full text-label-md font-label-md font-bold transition-all duration-300 active:scale-95 border border-primary-fixed-dim/40"
          >
            <span className="material-symbols-outlined text-[18px]" style={{ fontVariationSettings: "'FILL' 1" }}>favorite</span>
            AI Companion
          </button>

          <button 
            className="p-2 text-on-surface-variant hover:text-secondary transition-colors rounded-full hover:bg-surface-container"
            aria-label="Search"
          >
            <span className="material-symbols-outlined text-[22px]">search</span>
          </button>
          
          <img 
            alt="Profile" 
            className="w-10 h-10 rounded-full object-cover border-2 border-primary-container shadow-sm" 
            src={profileUrl} 
          />
        </div>
      </div>
    </header>
  );
}
