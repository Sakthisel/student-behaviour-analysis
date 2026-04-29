import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { BarChart3, Users } from "lucide-react";

import Header from "./components/Header";
import FileUpload from "./components/FileUpload";
import PipelineStatus from "./components/PipelineStatus";
import MetricCard from "./components/MetricCard";
import ResultsCharts from "./components/ResultsCharts";
import ResultsTable from "./components/ResultsTable";
import ReportCard from "./components/ReportCard";

import { analyzeVideo } from "./services/api";
import { sampleStudents, sampleTrend, sampleReport } from "./data/sampleData";
import type { AnalyzeResponse, Student, TrendData, Status } from "./types";

export default function App() {
  const [video, setVideo] = useState<File | null>(null);
  const [status, setStatus] = useState<Status>("idle");
  const [students, setStudents] = useState<Student[]>(sampleStudents);
  const [trendData, setTrendData] = useState<TrendData[]>(sampleTrend);
  const [report, setReport] = useState<string>(sampleReport);
  const [error, setError] = useState<string>("");

  const summary = useMemo(() => {
    const avg = (key: "attention_score" | "engagement_score" | "gd_score") =>
      students.length
        ? (
            students.reduce(
              (sum, student) => sum + Number(student[key] ?? 0),
              0,
            ) / students.length
          ).toFixed(2)
        : "0.00";

    return {
      participants: students.length,
      attention: avg("attention_score"),
      engagement: avg("engagement_score"),
      gd: avg("gd_score"),
    };
  }, [students]);

  const handleAnalyze = async (): Promise<void> => {
    if (!video) return;

    setStatus("processing");
    setError("");

    try {
      const response: AnalyzeResponse = await analyzeVideo(video);

      setStudents(response.students ?? sampleStudents);
      setTrendData(response.trendData ?? sampleTrend);
      setReport(response.report ?? sampleReport);
      setStatus("done");
    } catch (err) {
      console.error(err);
      setError("Backend is not connected. Showing sample results.");
      setStudents(sampleStudents);
      setTrendData(sampleTrend);
      setReport(sampleReport);
      setStatus("done");
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Header />

      <main className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        {error && (
          <div className="rounded-2xl bg-amber-50 border border-amber-200 text-amber-800 p-4 text-sm">
            {error}
          </div>
        )}

        <section className="grid lg:grid-cols-3 gap-6">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            className="lg:col-span-2"
          >
            <FileUpload
              video={video}
              setVideo={setVideo}
              status={status}
              onAnalyze={handleAnalyze}
              loading={false}
            />
          </motion.div>

          <PipelineStatus status={status} />
        </section>

        <section className="grid md:grid-cols-4 gap-4">
          <MetricCard
            title="Participants"
            value={summary.participants}
            icon={Users}
          />
          <MetricCard
            title="Avg Attention"
            value={summary.attention}
            icon={BarChart3}
          />
          <MetricCard
            title="Avg Engagement"
            value={summary.engagement}
            icon={BarChart3}
          />
          <MetricCard
            title="Avg GD Score"
            value={summary.gd}
            icon={BarChart3}
          />
        </section>

        <ResultsCharts trendData={trendData} students={students} />

        <section className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <ResultsTable students={students} />
          </div>

          <ReportCard report={report} />
        </section>
      </main>
    </div>
  );
}
