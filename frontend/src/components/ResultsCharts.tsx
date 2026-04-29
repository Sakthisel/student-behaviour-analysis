import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
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
  return (
    <div className="grid lg:grid-cols-2 gap-6">
      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-4">Score Trends</h2>

        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="frame" />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="attention"
                stroke="#0e2941"
                strokeWidth={2}
              />
              <Line
                type="monotone"
                dataKey="engagement"
                stroke="#2563eb"
                strokeWidth={2}
              />
              <Line
                type="monotone"
                dataKey="gd"
                stroke="#16a34a"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-4">Student-wise GD Score</h2>

        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={students}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="student_id" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="gd_score" fill="#0e2941" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
