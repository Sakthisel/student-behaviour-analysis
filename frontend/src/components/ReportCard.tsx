import { FileText } from "lucide-react";

interface ReportCardProps {
  report: string;
}

export default function ReportCard({ report }: ReportCardProps) {
  return (
    <div className="card p-6 h-full">
      <div className="flex items-center gap-3 mb-4">
        <FileText className="text-primary" size={26} />
        <h2 className="text-xl font-semibold">LLM Report</h2>
      </div>

      <p className="text-sm leading-7 text-slate-600 whitespace-pre-line">
        {report}
      </p>
    </div>
  );
}
