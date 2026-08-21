import React from 'react';

export default function Footer() {
  const logoUrl = "https://lh3.googleusercontent.com/aida-public/AB6AXuDtqKJj23wxqVgID2_7bKSk1E1UpVdMNH3_-s7yMkGvF5-7RtnfV0s0jPQ97MWmJKijEKBzoQpeHs4C0PTUXbjHTKrGAPuo7TuRR7IxaqAoT3po29Ak3PdQtWJxfUGdZNMkGZ0F9vqlU2jq82Cg1AkDXE2cb32mwYzYUhTmxxoGQM74e3tOt06r_gIRuvolHUr2sMf-8Gwtlk_XpGxGebvmh-SYaCQUaGxTvB557WVIvjz19g6dPsDMcw";

  return (
    <footer className="w-full bg-surface-container py-section-gap mt-section-gap">
      <div className="max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop flex flex-col md:flex-row justify-between items-start gap-12">
        <div className="max-w-xs">
          <div className="flex items-center gap-3 mb-6">
            <img 
              alt="MAA Logo" 
              className="h-6 w-auto" 
              src={logoUrl} 
            />
            <span className="font-headline-sm text-headline-sm text-primary">MAA</span>
          </div>
          <p className="text-body-md font-body-md text-on-surface-variant">
            A digital embrace designed to provide warmth, support, and emotional comfort through AI technology.
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-12">
          <div className="flex flex-col gap-4">
            <h4 className="font-label-md text-label-md text-on-surface font-bold">Platform</h4>
            <a className="text-label-md font-label-md text-on-surface-variant hover:text-secondary" href="#">Companion</a>
            <a className="text-label-md font-label-md text-on-surface-variant hover:text-secondary" href="#">Journal</a>
            <a className="text-label-md font-label-md text-on-surface-variant hover:text-secondary" href="#">Resources</a>
          </div>
          
          <div className="flex flex-col gap-4">
            <h4 className="font-label-md text-label-md text-on-surface font-bold">Company</h4>
            <a className="text-label-md font-label-md text-on-surface-variant hover:text-secondary" href="#">Mission</a>
            <a className="text-label-md font-label-md text-on-surface-variant hover:text-secondary" href="#">Ethics</a>
            <a className="text-label-md font-label-md text-on-surface-variant hover:text-secondary" href="#">Contact</a>
          </div>
        </div>
      </div>

      <div className="max-w-container-max mx-auto px-margin-mobile md:px-margin-desktop border-t border-outline-variant mt-12 pt-8 text-center text-label-sm font-label-sm text-on-surface-variant">
        © 2026 MAA. Designed with empathy and patience.
      </div>
    </footer>
  );
}
