/*
LEARN: This file centralizes all API calls to the FastAPI backend.
axios is like fetch() but with better error handling and cleaner syntax.
BASE_URL points to our FastAPI server running on port 8000.
*/
import axios from "axios";

const BASE_URL = "http://localhost:8000";

export const api = axios.create({ baseURL: BASE_URL });

export const uploadDocument = (file, onProgress) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/documents/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
    onUploadProgress: (e) => onProgress?.(Math.round((e.loaded * 100) / e.total)),
  });
};

export const getDocuments = () => api.get("/documents/");

export const deleteDocument = (docId) => api.delete(`/documents/${docId}`);

export const queryDocuments = (payload) => api.post("/query/", payload);
