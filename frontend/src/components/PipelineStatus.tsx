import { CheckCircle2, Clock } from "lucide-react";

type StatusType = "idle" | "processing" | "done";

interface PipelineStatusProps {
  status: StatusType;
}

const steps: string[] = [
  "YOLO Detection",
  "Gaze / Gesture / Pose / Emotion",
  "CSV Aggregation",
  "ML + LSTM Prediction",
  "LLM Report Generation",
];

export default function PipelineStatus({ status }: PipelineStatusProps) {
  return (
    <div className="card p-6">
      <h2 className="text-xl font-semibold mb-5">Pipeline Status</h2>

      <div className="space-y-4">
        {steps.map((step, index) => {
          const completed =
            status === "done" || (status === "processing" && index < 3);

          return (
            <div key={step} className="flex items-center gap-3">
              {completed ? (
                <CheckCircle2 className="text-emerald-500" size={18} />
              ) : (
                <Clock className="text-slate-400" size={18} />
              )}

              <span className={completed ? "text-slate-900" : "text-slate-500"}>
                {step}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
