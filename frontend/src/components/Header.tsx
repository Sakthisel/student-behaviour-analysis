import { BrainCircuit } from "lucide-react";

export default function Header() {
  return (
    <header className="sticky top-0 z-20 bg-white/90 backdrop-blur border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-3">
        <div className="h-11 w-11 rounded-2xl bg-primary text-white flex items-center justify-center">
          <BrainCircuit size={24} />
        </div>

        <div>
          <h1 className="text-2xl font-bold text-slate-900">
            Student Behaviour Analysis
          </h1>
          <p className="text-sm text-slate-500">
            Computer Vision + Machine Learning + LSTM + LLM Report Generation
          </p>
        </div>
      </div>
    </header>
  );
}
