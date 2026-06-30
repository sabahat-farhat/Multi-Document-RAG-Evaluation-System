/*
LEARN: This is the main chat-like interface.
"ground_truth" is the optional correct answer the user provides for RAGAS evaluation.
When run_evaluation=true, the backend calls RAGAS and returns faithfulness/relevancy scores.
*/
import { useState } from "react";
import { Send, Loader, ChevronDown, ChevronUp } from "lucide-react";
import { queryDocuments } from "../api";
import EvaluationScores from "./EvaluationScores";

export default function QueryPanel({ selectedDocId }) {
  const [question, setQuestion] = useState("");
  const [groundTruth, setGroundTruth] = useState("");
  const [runEval, setRunEval] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [showSources, setShowSources] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await queryDocuments({
        question,
        doc_id: selectedDocId || null,
        ground_truth: runEval && groundTruth ? groundTruth : null,
        run_evaluation: runEval,
      });
      setResult(res.data);
    } catch (e) {
      setError(e.response?.data?.detail || "Query failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      {selectedDocId && (
        <p className="text-xs text-blue-400 bg-blue-950 px-3 py-1.5 rounded-lg">
          Searching within selected document only
        </p>
      )}

      <form onSubmit={handleSubmit} className="space-y-3">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about your documents…"
          rows={3}
          className="w-full bg-slate-800 border border-slate-600 rounded-xl px-4 py-3 text-slate-100 placeholder-slate-500 resize-none focus:outline-none focus:border-blue-500"
        />

        <div className="flex items-center gap-3">
          <label className="flex items-center gap-2 text-sm text-slate-400 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={runEval}
              onChange={(e) => setRunEval(e.target.checked)}
              className="accent-blue-500"
            />
            Run RAGAS evaluation
          </label>
        </div>

        {runEval && (
          <input
            value={groundTruth}
            onChange={(e) => setGroundTruth(e.target.value)}
            placeholder="Ground truth answer (optional — enables context_precision score)"
            className="w-full bg-slate-800 border border-slate-600 rounded-lg px-4 py-2.5 text-slate-100 placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500"
          />
        )}

        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-40 text-white px-5 py-2.5 rounded-xl font-medium transition-colors"
        >
          {loading ? <Loader size={16} className="animate-spin" /> : <Send size={16} />}
          {loading ? "Thinking…" : "Ask"}
        </button>
      </form>

      {error && <p className="text-red-400 text-sm">{error}</p>}

      {result && (
        <div className="space-y-4">
          <div className="bg-slate-800 rounded-xl p-5">
            <p className="text-xs text-slate-500 mb-2 uppercase tracking-wide">Answer</p>
            <p className="text-slate-100 leading-relaxed whitespace-pre-wrap">{result.answer}</p>
          </div>

          {result.evaluation && <EvaluationScores scores={result.evaluation} />}

          {result.sources?.length > 0 && (
            <div>
              <button
                onClick={() => setShowSources(!showSources)}
                className="flex items-center gap-1 text-sm text-slate-400 hover:text-slate-200"
              >
                {showSources ? <ChevronUp size={15} /> : <ChevronDown size={15} />}
                {result.sources.length} source chunk{result.sources.length !== 1 ? "s" : ""}
              </button>
              {showSources && (
                <div className="mt-3 space-y-2">
                  {result.sources.map((s, i) => (
                    <div key={i} className="bg-slate-800 rounded-lg p-3 border-l-2 border-blue-700">
                      <p className="text-xs text-slate-500 mb-1">
                        {s.source_file} · page {s.page + 1}
                      </p>
                      <p className="text-slate-300 text-sm">{s.content}…</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
