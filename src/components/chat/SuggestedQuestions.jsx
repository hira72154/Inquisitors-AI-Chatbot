import React from 'react';

export default function SuggestedQuestions({ questions, onSelectQuestion }) {
  if (!questions || questions.length === 0) return null;

  // Icon mapping for suggested chips
  const getIcon = (text) => {
    const lower = text.toLowerCase();
    if (lower.includes('health')) return 'local_hospital';
    if (lower.includes('home')) return 'home';
    if (lower.includes('companion') || lower.includes('talk')) return 'psychology';
    if (lower.includes('exercise') || lower.includes('breathe')) return 'self_improvement';
    return 'favorite';
  };

  return (
    <div className="flex w-full justify-start pl-0 md:pl-16 animate-slideUp my-2">
      <div className="flex flex-wrap gap-2">
        {questions.map((q, idx) => (
          <button
            key={idx}
            onClick={() => onSelectQuestion(q)}
            className="bg-primary-container text-on-primary-container hover:bg-primary hover:text-on-primary transition-colors duration-300 px-4 py-2 rounded-full font-label-md flex items-center gap-2 shadow-sm text-xs md:text-sm active:scale-95"
          >
            <span className="material-symbols-outlined text-[16px]">
              {getIcon(q)}
            </span>
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}
