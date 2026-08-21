import React from 'react';

export default function RAGSourceCard({ ragCard }) {
  if (!ragCard) return null;

  return (
    <div className="bg-surface-container text-on-surface rounded-2xl rounded-tl-none px-6 py-5 shadow-sm relative w-full mt-2 border border-outline-variant/40">
      <div className="bg-surface rounded-xl p-4 flex flex-col gap-2 shadow-inner">
        
        {/* Card Title & Icon */}
        <div className="flex items-center gap-2 mb-1">
          <span className="material-symbols-outlined text-secondary text-sm md:text-base">
            {ragCard.icon || 'flight'}
          </span>
          <h4 className="font-label-md font-bold text-on-surface">
            {ragCard.title || 'Travel Assistance Core Services'}
          </h4>
        </div>

        {/* Card Checklist */}
        {ragCard.items && (
          <ul className="list-disc list-inside font-body-md text-on-surface-variant space-y-1 ml-2">
            {ragCard.items.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        )}
      </div>

      {/* RAG Knowledge Attribution Footer */}
      <div className="mt-4 flex items-center justify-between border-t border-outline-variant pt-3">
        <div className="flex items-center gap-1.5 text-label-sm text-on-surface-variant">
          <span className="material-symbols-outlined text-[16px] text-secondary">auto_awesome</span>
          <span>{ragCard.source || 'Based on MAA Knowledge Base'}</span>
        </div>
        <a 
          className="text-label-sm text-secondary hover:underline font-bold transition-colors" 
          href="#"
          onClick={(e) => { e.preventDefault(); alert(`Source Document: ${ragCard.source || 'MAA Internal RAG KB'}`); }}
        >
          [View source]
        </a>
      </div>
    </div>
  );
}
