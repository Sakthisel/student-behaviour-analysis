import type { Student } from "../types";

type EngagementLevel = "LOW" | "MEDIUM" | "HIGH";

interface BadgeProps {
  value: EngagementLevel;
}

function Badge({ value }: BadgeProps) {
  const classes: Record<EngagementLevel, string> = {
    LOW: "bg-red-100 text-red-700",
    MEDIUM: "bg-amber-100 text-amber-700",
    HIGH: "bg-emerald-100 text-emerald-700",
  };

  return (
    <span
      className={`px-3 py-1 rounded-full text-xs font-semibold ${classes[value]}`}
    >
      {value}
    </span>
  );
}

interface ResultsTableProps {
  students: Student[];
}

export default function ResultsTable({ students }: ResultsTableProps) {
  return (
    <div className="card p-6">
      <h2 className="text-xl font-semibold mb-4">Student Results</h2>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="border-b text-left text-slate-500">
            <tr>
              <th className="py-3">Student ID</th>
              <th>Attention</th>
              <th>Engagement</th>
              <th>GD Score</th>
              <th>ML Engagement</th>
            </tr>
          </thead>

          <tbody>
            {students.map((student) => (
              <tr
                key={student.student_id}
                className="border-b last:border-none"
              >
                <td className="py-3 font-medium">{student.student_id}</td>
                <td>{student.attention_score}</td>
                <td>{student.engagement_score}</td>
                <td>{student.gd_score}</td>
                <td>
                  <Badge value={student.ml_engagement} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
