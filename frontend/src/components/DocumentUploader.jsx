/*
LEARN: useDropzone is a library hook that handles drag-and-drop file logic.
It gives you getRootProps() and getInputProps() — you spread them onto divs/inputs.
*/
import { useState } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, FileText, Loader } from "lucide-react";
import { uploadDocument } from "../api";

export default function DocumentUploader({ onUploadSuccess }) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState("");

  const onDrop = async (acceptedFiles) => {
    if (!acceptedFiles.length) return;
    setUploading(true);
    setError("");
    try {
      const res = await uploadDocument(acceptedFiles[0], setProgress);
      onUploadSuccess(res.data);
    } catch (e) {
      setError(e.response?.data?.detail || "Upload failed");
    } finally {
      setUploading(false);
      setProgress(0);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "application/pdf": [".pdf"], "text/plain": [".txt"] },
    multiple: false,
  });

  return (
    <div>
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
          isDragActive ? "border-blue-500 bg-blue-950" : "border-slate-600 hover:border-blue-400"
        }`}
      >
        <input {...getInputProps()} />
        <Upload className="mx-auto mb-3 text-blue-400" size={36} />
        <p className="text-slate-300 font-medium">
          {isDragActive ? "Drop file here…" : "Drag & drop a PDF or TXT file"}
        </p>
        <p className="text-slate-500 text-sm mt-1">or click to browse</p>
      </div>

      {uploading && (
        <div className="mt-4">
          <div className="flex items-center gap-2 text-blue-400 mb-2">
            <Loader size={16} className="animate-spin" />
            <span className="text-sm">Processing document… {progress}%</span>
          </div>
          <div className="w-full bg-slate-700 rounded-full h-2">
            <div
              className="bg-blue-500 h-2 rounded-full transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      {error && <p className="text-red-400 text-sm mt-3">{error}</p>}
    </div>
  );
}
