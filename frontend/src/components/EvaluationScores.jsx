/*
LEARN: This is the "dashboard" part of the project title.
RadialBarChart from recharts visualizes 0–1 scores as gauge-style arcs.
Color coding: green ≥ 0.7, yellow ≥ 0.4, red < 0.4
*/
import { RadialBarChart, RadialBar, ResponsiveContainer, Tooltip } from "recharts";

const METRICS = [
  {
    key: "faithfulness",
    label: "Faithfulness",
    description: "Is the answer grounded in the retrieved context? (catches hallucinations)",
  },
  {
    key: "answer_relevancy",
    label: "Answer Relevancy",
    description: "Does the answer actually address the question?",
  },
  {
    key: "context_precision",
    label: "Context Precision",
    description: "Did retrieval fetch the right chunks? (requires ground truth)",
  },
];

function scoreColor(val) {
  if (val === null) return "#475569";
  if (val >= 0.7) return "#22c55e";
  if (val >= 0.4) return "#eab308";
  return "#ef4444";
}

function ScoreGauge({ label, value, description }) {
  const data = [{ name: label, value: value !== null ? value * 100 : 0 }];
  const color = scoreColor(value);

  return (
    <div className="bg-slate-800 rounded-xl p-4 flex flex-col items-center">
      <div className="w-24 h-24">
        <ResponsiveContainer width="100%" height="100%">
          <RadialBarChart
            innerRadius="60%"
            outerRadius="100%"
            data={data}
            startAngle={180}
            endAngle={0}
          >
            <RadialBar dataKey="value" fill={color} background={{ fill: "#1e293b" }} />
          </RadialBarChart>
        </ResponsiveContainer>
      </div>
      <p className="text-2xl font-bold mt-1" style={{ color }}>
        {value !== null ? value.toFixed(2) : "N/A"}
      </p>
      <p className="text-slate-300 text-sm font-medium mt-1">{label}</p>
      <p className="text-slate-500 text-xs text-center mt-1 leading-snug">{description}</p>
    </div>
  );
}

export default function EvaluationScores({ scores }) {
  return (
    <div>
      <p className="text-xs text-slate-500 uppercase tracking-wide mb-3">RAGAS Evaluation</p>
      <div className="grid grid-cols-3 gap-3">
        {METRICS.map((m) => (
          <ScoreGauge
            key={m.key}
            label={m.label}
            value={scores[m.key] ?? null}
            description={m.description}
          />
        ))}
      </div>
    </div>
  );
}
