"use client";

import { FileText, Download, Trophy, Users, Sparkles } from "lucide-react";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import { useMemo } from "react";

interface ReportCardProps {
  report: string;
}

interface ParsedStudent {
  student_id: string;
  attention: string;
  engagement: string;
  gd: string;
  ml_insight: string;
  strength: string;
  weakness: string;
  recommendation: string;
}

export default function ReportCard({ report }: ReportCardProps) {
  const parseStudentsFromReport = (report: string): ParsedStudent[] => {
    if (!report) return [];
    const cleanReport = report.replace(/\r/g, "").replace(/\n{2,}/g, "\n");
    const chunks = cleanReport.split("Student ID:").slice(1);
    const students: ParsedStudent[] = chunks.map((chunk) => {
      const lines = chunk
        .split("\n")
        .map((l) => l.replace(/\*/g, "").trim())
        .filter(Boolean);

      const id = lines[0]?.split(" ")[0]?.trim() || "unknown";

      const fields: Record<string, string> = {};

      lines.forEach((line) => {
        const parts = line.split(":");
        if (parts.length >= 2) {
          const key = parts[0].trim().toLowerCase();
          const value = parts.slice(1).join(":").trim();
          fields[key] = value;
        }
      });

      return {
        student_id: id,
        attention: fields["attention"] ?? "-",
        engagement: fields["engagement"] ?? "-",
        gd:
          fields["performance (gd)"] ??
          fields["performance"] ??
          fields["gd"] ??
          "-",
        ml_insight: fields["ml insight"] ?? "-",
        strength: fields["strength"] ?? "-",
        weakness: fields["weakness"] ?? "-",
        recommendation: fields["recommendation"] ?? "-",
      };
    });

    const map = new Map<string, ParsedStudent>();

    for (const s of students) {
      map.set(s.student_id, s);
    }

    return Array.from(map.values());
  };

  const students = useMemo(() => {
    return parseStudentsFromReport(report);
  }, [report]);

  const parseReport = (text: string): Record<string, string> => {
    const sections: Record<string, string> = {};
    const split = text.split(/\*\*(.*?)\*\*/g);

    for (let i = 1; i < split.length; i += 2) {
      sections[split[i].trim()] = split[i + 1]?.trim();
    }

    return sections;
  };

  const sections = parseReport(report);

  const getList = (text: string) =>
    text
      ?.split("\n")
      .map((l) => l.replace(/^[*\-\d.\s]+/, "").trim())
      .filter(Boolean);

  const top = getList(sections["TOP PERFORMER:"] || "")?.[0] || "N/A";

  const downloadPdf = async () => {
    const el = document.getElementById("report-card");
    if (!el) return;

    const canvas = await html2canvas(el, { scale: 2 });
    const img = canvas.toDataURL("image/png");

    const pdf = new jsPDF("p", "mm", "a4");
    const w = 190;
    const h = (canvas.height * w) / canvas.width;

    pdf.addImage(img, "PNG", 10, 10, w, h);
    pdf.save("report.pdf");
  };

  return (
    <div
      id="report-card"
      className="p-6 space-y-6 bg-white rounded-3xl shadow-lg border border-slate-100"
    >
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="p-3 rounded-xl bg-blue-50 border border-blue-100">
            <FileText className="text-blue-600" size={20} />
          </div>

          <div>
            <h2 className="text-lg font-semibold text-slate-800">
              AI Performance Dashboard
            </h2>
            <p className="text-xs text-slate-500">Student analytics report</p>
          </div>
        </div>

        <button
          onClick={downloadPdf}
          className="px-4 py-2 rounded-xl bg-blue-600 text-white text-sm hover:bg-blue-700 transition"
        >
          <Download size={16} className="inline mr-1" />
          Export
        </button>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl border bg-white shadow-sm">
          <div className="flex items-center gap-2 text-yellow-600 text-xs">
            <Trophy size={14} /> Top Performer
          </div>
          <p className="mt-2 text-sm font-semibold text-slate-800">{top}</p>
        </div>

        <div className="p-4 rounded-2xl border bg-white shadow-sm">
          <div className="flex items-center gap-2 text-emerald-600 text-xs">
            <Users size={14} /> Students
          </div>
          <p className="mt-2 text-sm font-semibold text-slate-800">
            {getList(sections["RANKING:"] || "").length}
          </p>
        </div>

        <div className="p-4 rounded-2xl border bg-white shadow-sm">
          <div className="flex items-center gap-2 text-blue-600 text-xs">
            <Sparkles size={14} /> Insight
          </div>
          <p className="mt-2 text-sm font-semibold text-slate-800">
            AI Generated
          </p>
        </div>
      </div>

      <div className="p-5 rounded-2xl border bg-white shadow-sm">
        <h3 className="text-sm font-semibold text-slate-700 mb-3">
          Leaderboard
        </h3>

        <div className="space-y-2">
          {getList(sections["RANKING:"] || "").map((item, i) => (
            <div
              key={i}
              className="flex justify-between items-center px-3 py-2 rounded-xl bg-slate-50 border hover:bg-slate-100 transition"
            >
              <span className="text-sm font-medium text-slate-700">
                #{i + 1}
              </span>

              <span
                className={`text-sm font-medium ${
                  i === 0
                    ? "text-yellow-600"
                    : i < 3
                      ? "text-emerald-600"
                      : "text-slate-600"
                }`}
              >
                {item}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="p-5 rounded-2xl border bg-white shadow-sm">
        <h3 className="text-sm font-semibold text-slate-700 mb-4">
          Individual Report
        </h3>

        <div className="grid md:grid-cols-2 gap-4">
          {students.map((s, i) => (
            <div
              key={`${s.student_id}-${i}`}
              className="p-4 rounded-2xl border bg-white shadow-sm hover:shadow-md transition"
            >
              <h4 className="font-semibold text-slate-800 mb-3">
                Student {s.student_id}
              </h4>

              <div className="space-y-2 text-xs text-slate-600">
                <p>
                  <b>Attention:</b> {s.attention}
                </p>
                <p>
                  <b>Engagement:</b> {s.engagement}
                </p>
                <p>
                  <b>GD:</b> {s.gd}
                </p>
                <p>
                  <b>ML Insight:</b> {s.ml_insight}
                </p>
                <p>
                  <b>Strength:</b> {s.strength}
                </p>
                <p>
                  <b>Weakness:</b> {s.weakness}
                </p>
                <p>
                  <b>Recommendation:</b> {s.recommendation}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {sections["FINAL SUMMARY:"] && (
        <div className="p-5 rounded-2xl border bg-blue-50">
          <h3 className="text-sm font-semibold text-blue-700 mb-2">
            AI Insight Summary
          </h3>
          <p className="text-sm text-slate-700 leading-relaxed">
            {sections["FINAL SUMMARY:"]}
          </p>
        </div>
      )}
    </div>
  );
}
