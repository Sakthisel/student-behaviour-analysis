import { QrCode } from "lucide-react";
import { useState } from "react";

export default function Header() {
  const [showQR, setShowQR] = useState(false);

  return (
    <header className="sticky top-0 z-20 border-b border-slate-200/70 bg-white/80 backdrop-blur-xl">
      <div className="mx-auto max-w-7xl px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div>
            <h1 className="text-xl font-bold text-slate-900">
              Student Behaviour Analysis
            </h1>
            <p className="text-xs text-slate-500">
              Computer Vision + Machine Learning + LSTM + LLM Report Generation
            </p>
          </div>
        </div>

        <div className="relative">
          <button
            onClick={() => setShowQR(!showQR)}
            className="h-10 w-10 flex items-center justify-center rounded-full border border-slate-200 bg-white shadow-sm hover:border-primary"
          >
            <QrCode size={20} className="text-slate-600" />
          </button>

          {showQR && (
            <div className="absolute right-0 mt-3 w-72 rounded-2xl border border-slate-200 bg-white shadow-2xl p-5">
              <p className="text-sm font-semibold text-center text-slate-800 mb-4">
                Scan to Connect
              </p>

              <div className="grid grid-cols-2 gap-4">
                <div className="flex flex-col items-center">
                  <img
                    src="https://api.qrserver.com/v1/create-qr-code/?size=140x140&data=https://sakthivelv-portfolio.netlify.app"
                    alt="Portfolio QR"
                    className="rounded-lg border"
                  />
                  <p className="text-xs text-slate-500 mt-2 text-center">
                    Portfolio
                  </p>
                </div>

                <div className="flex flex-col items-center">
                  <img
                    src="https://api.qrserver.com/v1/create-qr-code/?size=140x140&data=https://linkedin.com/in/sakthiselv"
                    alt="LinkedIn QR"
                    className="rounded-lg border"
                  />
                  <p className="text-xs text-slate-500 mt-2 text-center">
                    LinkedIn
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
