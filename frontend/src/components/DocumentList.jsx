import { FileText, Trash2 } from "lucide-react";
import { deleteDocument } from "../api";

export default function DocumentList({ documents, onDelete, selectedDocId, onSelect }) {
  const handleDelete = async (docId) => {
    if (!confirm("Remove this document from the vector store?")) return;
    try {
      await deleteDocument(docId);
      onDelete(docId);
    } catch {
      alert("Failed to delete document");
    }
  };

  if (!documents.length) {
    return <p className="text-slate-500 text-sm text-center py-6">No documents uploaded yet.</p>;
  }

  return (
    <ul className="space-y-2">
      {documents.map((doc) => (
        <li
          key={doc.doc_id}
          onClick={() => onSelect(doc.doc_id === selectedDocId ? null : doc.doc_id)}
          className={`flex items-center justify-between p-3 rounded-lg cursor-pointer transition-colors ${
            doc.doc_id === selectedDocId
              ? "bg-blue-900 border border-blue-500"
              : "bg-slate-800 hover:bg-slate-700"
          }`}
        >
          <div className="flex items-center gap-2 min-w-0">
            <FileText size={16} className="text-blue-400 shrink-0" />
            <span className="text-slate-200 text-sm truncate">{doc.source_file}</span>
          </div>
          <button
            onClick={(e) => { e.stopPropagation(); handleDelete(doc.doc_id); }}
            className="text-slate-500 hover:text-red-400 transition-colors shrink-0 ml-2"
          >
            <Trash2 size={15} />
          </button>
        </li>
      ))}
    </ul>
  );
}
