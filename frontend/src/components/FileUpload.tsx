import { Upload, PlayCircle, Loader2, CheckCircle2 } from "lucide-react";
import type { Status } from "../types";

interface Props {
  video: File | null;
  setVideo: (file: File | null) => void;
  onAnalyze: () => void;
  status: Status;
}

export default function FileUpload({
  video,
  setVideo,
  status,
  onAnalyze,
}: Props) {
  const isProcessing = status === "processing";
  const isDisabled = !video || isProcessing;

  return (
    <div className="p-6 border rounded-2xl bg-white shadow-sm">
      <div className="flex items-center gap-3 mb-5">
        <Upload className="text-blue-600" size={28} />
        <div>
          <h2 className="text-xl font-semibold">Upload Discussion Video</h2>
          <p className="text-sm text-slate-500">
            Upload .mp4, .mov, or .avi file to run full analysis.
          </p>
        </div>
      </div>

      <label className="block border-2 border-dashed border-slate-300 rounded-2xl p-8 text-center cursor-pointer hover:bg-slate-50 transition">
        <input
          type="file"
          accept="video/*"
          className="hidden"
          onChange={(e) => setVideo(e.target.files?.[0] || null)}
        />

        <p className="font-medium text-slate-800">
          {video ? video.name : "Click to upload video"}
        </p>
        <p className="text-sm text-slate-500 mt-1">
          The backend runs ML + CV + LLM analysis.
        </p>
      </label>

      <div className="mt-5 flex items-center gap-3">
        <button
          onClick={onAnalyze}
          disabled={isDisabled}
          className={`inline-flex items-center px-5 py-3 rounded-2xl font-medium text-white transition
            ${isDisabled ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"}
          `}
        >
          {isProcessing ? (
            <Loader2 className="mr-2 animate-spin" size={18} />
          ) : (
            <PlayCircle className="mr-2" size={18} />
          )}

          {isProcessing ? "Processing..." : "Run Analysis"}
        </button>

        {status === "done" && (
          <span className="flex items-center text-sm text-green-600">
            <CheckCircle2 size={16} className="mr-1" />
            Analysis completed
          </span>
        )}
      </div>
    </div>
  );
}
