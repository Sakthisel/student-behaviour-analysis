import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

import type { Student, TrendData } from "../types";

interface ResultsChartsProps {
  trendData: TrendData[];
  students: Student[];
}

export default function ResultsCharts({
  trendData,
  students,
}: ResultsChartsProps) {
  const max = Math.max(...students.map((s) => s.gd_score));

  return (
    <div className="grid lg:grid-cols-2 gap-6">
      <div className="p-6 bg-white rounded-2xl shadow-sm border">
        <div className="mb-4">
          <h2 className="text-lg font-semibold text-slate-800">
            Performance Trends
          </h2>
          <p className="text-xs text-slate-500">
            Smooth behavioral evolution over time
          </p>
        </div>

        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={trendData}>
              <defs>
                <linearGradient id="gd" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#6366f1" stopOpacity={0.4} />
                  <stop offset="100%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>

                <linearGradient id="eng" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#10b981" stopOpacity={0.4} />
                  <stop offset="100%" stopColor="#10b981" stopOpacity={0} />
                </linearGradient>

                <linearGradient id="att" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#f59e0b" stopOpacity={0.4} />
                  <stop offset="100%" stopColor="#f59e0b" stopOpacity={0} />
                </linearGradient>
              </defs>

              <CartesianGrid stroke="#f1f5f9" strokeDasharray="3 3" />

              <XAxis
                dataKey="frame"
                tick={{ fill: "#64748b", fontSize: 12 }}
                axisLine={false}
                tickLine={false}
              />

              <YAxis
                tick={{ fill: "#64748b", fontSize: 12 }}
                axisLine={false}
                tickLine={false}
              />

              <Tooltip
                contentStyle={{
                  backgroundColor: "#fff",
                  border: "1px solid #e2e8f0",
                  borderRadius: "10px",
                }}
              />

              <Area
                type="monotone"
                dataKey="gd"
                stroke="#6366f1"
                fill="url(#gd)"
                strokeWidth={2}
              />

              <Area
                type="monotone"
                dataKey="engagement"
                stroke="#10b981"
                fill="url(#eng)"
                strokeWidth={2}
              />

              <Area
                type="monotone"
                dataKey="attention"
                stroke="#f59e0b"
                fill="url(#att)"
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="p-6 bg-white rounded-2xl shadow-sm border">
        <div className="mb-4">
          <h2 className="text-lg font-semibold text-slate-800">
            Student Performance Rank
          </h2>
          <p className="text-xs text-slate-500">Relative GD score comparison</p>
        </div>

        <div className="space-y-3">
          {students.map((s, i) => {
            const percent = (s.gd_score / max) * 100;

            return (
              <div key={i} className="space-y-1">
                <div className="flex justify-between text-xs text-slate-600">
                  <span>Student {s.student_id}</span>
                  <span className="font-medium">{s.gd_score}</span>
                </div>

                <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all duration-700"
                    style={{
                      width: `${percent}%`,
                      background:
                        s.gd_score === max
                          ? "#4ee4b2"
                          : s.gd_score < 3
                            ? "#f16262"
                            : "#696bf0",
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
