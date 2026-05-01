import axios from "axios";
import { type AnalyzeResponse } from "../types";

const API = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

export const analyzeVideo = async (file: File): Promise<AnalyzeResponse> => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await axios.post<AnalyzeResponse>(`${API}/analyze`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return res.data;
};
