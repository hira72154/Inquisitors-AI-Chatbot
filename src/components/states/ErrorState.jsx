import React from 'react';

export default function ErrorState({ onRetry }) {
  const errorAssetUrl = "https://lh3.googleusercontent.com/aida-public/AB6AXuC3ghGDGUe_vEr6H5ZrWVAr7SxsLmUVYzx1sqK3UapaQflrTaIrbZ3zcrg4GrsPl0Ztj36p7z46aIHSh9r94yUUPHn7CkctidHxvaQaaCaDzZPhM2mMVy7DQPsgIblw3RLyu22r5BFXC8_RawAW88nNNF98-yMPL3QviH58o8VNUGF4uPhfzBED1HxumH_YRT5UUgB8SptsMLdCDeZ2PoKXSZMC7yy0MRYDD4twcXkx38_w1wZRb5sqXQ";

  return (
    <div className="flex-1 flex flex-col justify-center items-center px-margin-mobile md:px-margin-desktop w-full max-w-[600px] mx-auto animate-fadeIn py-12 text-center">
      <div className="relative w-32 h-32 mb-8">
        <div className="absolute inset-0 bg-error-container rounded-full opacity-30 animate-pulse"></div>
        <img 
          alt="Error Icon" 
          className="w-full h-full object-contain relative z-10 drop-shadow-md" 
          src={errorAssetUrl} 
        />
      </div>

      <h2 className="font-headline-md text-headline-md text-on-surface mb-4">
        Oops, something went wrong <span className="text-secondary inline-block">💗</span>
      </h2>

      <p className="font-body-lg text-body-lg text-on-surface-variant mb-10 max-w-md">
        I'm having a little trouble responding right now. Please take a deep breath and try again when you're ready.
      </p>

      <button 
        onClick={onRetry}
        className="bg-secondary text-on-secondary px-8 py-4 rounded-full font-label-md text-label-md hover:scale-105 active:scale-95 transition-all duration-300 shadow-[0_4px_15px_rgba(233,30,99,0.25)] hover:shadow-[0_8px_25px_rgba(233,30,99,0.35)] flex items-center gap-2"
      >
        <span className="material-symbols-outlined text-[20px]">refresh</span>
        Try Again
      </button>
    </div>
  );
}
