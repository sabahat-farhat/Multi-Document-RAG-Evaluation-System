import { useState, useEffect } from "react";
import { Brain } from "lucide-react";
import { getDocuments } from "./api";
import DocumentUploader from "./components/DocumentUploader";
import DocumentList from "./components/DocumentList";
import QueryPanel from "./components/QueryPanel";

export default function App() {
  const [documents, setDocuments] = useState([]);
  const [selectedDocId, setSelectedDocId] = useState(null);

  useEffect(() => {
    getDocuments()
      .then((res) => setDocuments(res.data.documents))
      .catch(() => {});
  }, []);

  const handleUploadSuccess = (data) => {
    setDocuments((prev) => [
      ...prev,
      { doc_id: data.doc_id, source_file: data.filename },
    ]);
  };

  const handleDelete = (docId) => {
    setDocuments((prev) => prev.filter((d) => d.doc_id !== docId));
    if (selectedDocId === docId) setSelectedDocId(null);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center gap-3">
          <Brain className="text-blue-400" size={28} />
          <div>
            <h1 className="text-lg font-semibold">RAG Evaluation System</h1>
            <p className="text-slate-500 text-xs">Multi-document Q&A with RAGAS scoring</p>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8 grid grid-cols-[300px_1fr] gap-8">
        <aside className="space-y-6">
          <section>
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-3">
              Upload Document
            </h2>
            <DocumentUploader onUploadSuccess={handleUploadSuccess} />
          </section>

          <section>
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-3">
              Documents ({documents.length})
            </h2>
            <p className="text-xs text-slate-500 mb-2">Click a document to filter queries to it</p>
            <DocumentList
              documents={documents}
              onDelete={handleDelete}
              selectedDocId={selectedDocId}
              onSelect={setSelectedDocId}
            />
          </section>
        </aside>

        <section>
          <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-3">
            Ask a Question
          </h2>
          <QueryPanel selectedDocId={selectedDocId} />
        </section>
      </main>
    </div>
  );
}
