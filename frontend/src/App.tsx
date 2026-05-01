import { useMemo, useState } from "react";
import { motion } from "framer-motion";
import { BarChart3, Users } from "lucide-react";

import Header from "./components/Header";
import FileUpload from "./components/FileUpload";
import PipelineStatus from "./components/PipelineStatus";
import { TrendingUp } from "lucide-react";

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
            />
          </motion.div>

          <PipelineStatus status={status} />
        </section>

        <section className="grid md:grid-cols-4 gap-4">
          <div className="p-5 rounded-2xl bg-white border shadow-sm hover:shadow-md transition">
            <div className="flex items-center justify-between">
              <p className="text-xs text-slate-500">Participants</p>
              <Users className="text-indigo-500" size={18} />
            </div>

            <p className="text-2xl font-semibold text-slate-800 mt-2">
              {summary.participants}
            </p>

            <div className="mt-3 h-1.5 bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full w-3/4 bg-indigo-500 rounded-full" />
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-white border shadow-sm hover:shadow-md transition">
            <div className="flex items-center justify-between">
              <p className="text-xs text-slate-500">Avg Attention</p>
              <TrendingUp className="text-emerald-500" size={18} />
            </div>

            <p className="text-2xl font-semibold text-slate-800 mt-2">
              {summary.attention}
            </p>

            <div className="mt-3 h-1.5 bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full w-2/3 bg-emerald-500 rounded-full" />
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-white border shadow-sm hover:shadow-md transition">
            <div className="flex items-center justify-between">
              <p className="text-xs text-slate-500">Avg Engagement</p>
              <BarChart3 className="text-blue-500" size={18} />
            </div>

            <p className="text-2xl font-semibold text-slate-800 mt-2">
              {summary.engagement}
            </p>

            <div className="mt-3 h-1.5 bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full w-1/2 bg-blue-500 rounded-full" />
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-white border shadow-sm hover:shadow-md transition">
            <div className="flex items-center justify-between">
              <p className="text-xs text-slate-500">Avg GD Score</p>
              <BarChart3 className="text-amber-500" size={18} />
            </div>

            <p className="text-2xl font-semibold text-slate-800 mt-2">
              {summary.gd}
            </p>

            <div className="mt-3 h-1.5 bg-slate-100 rounded-full overflow-hidden">
              <div className="h-full w-4/5 bg-amber-500 rounded-full" />
            </div>
          </div>
        </section>

        <ResultsCharts trendData={trendData} students={students} />
        <ResultsTable students={students} />
        <ReportCard report={report} />
      </main>
    </div>
  );
}
