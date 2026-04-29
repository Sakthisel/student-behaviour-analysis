import { type LucideIcon } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
}

export default function MetricCard({
  title,
  value,
  icon: Icon,
}: MetricCardProps) {
  return (
    <div className="card p-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-500">{title}</p>
          <p className="text-3xl font-bold mt-1 text-slate-900">{value}</p>
        </div>

        <div className="h-12 w-12 rounded-2xl bg-slate-100 flex items-center justify-center">
          <Icon className="text-primary" size={24} />
        </div>
      </div>
    </div>
  );
}
