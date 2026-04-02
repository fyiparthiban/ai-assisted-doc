# RAG Project Features & Roadmap

This file tracks the features implemented and planned for the RAG AI Assistant.

## Currently Implemented
- [x] **Multi-Model Support**: Toggle between Fast (Llama 8B), Smart (Llama 70B), and Advanced (Qwen 32B).
- [x] **Corrective RAG (C-RAG)**: Uses relevance checks and query rewriting to improve document retrieval.
- [x] **Hybrid Sourcing**: Automatically detects and labels whether an answer came from "Uploaded Documents" or "Internet / General Knowledge".
- [x] **No-Upload Chat**: Allows chatting with the AI before any files are uploaded.
- [x] **Greeting Filter**: Simple greetings like "hi" or "hello" respond instantly without searching documents.
- [x] **UI Visibility Polish**: High-contrast "Brain Power" selector for better usability.

## Planned Features (Roadmap)
- [ ] **Persistent History**: Save chat sessions to a database for later review.
- [ ] **Multi-File Management**: View and delete specific uploaded files from the UI.
- [ ] **Advanced Citations**: Show the exact text snippet (chunk) used from the PDF.
- [ ] **Web Search Integration**: Use a search engine (like Tavily) if documents don't have the answer.
- [ ] **Voice Input/Output**: Speak to the chat and have it read answers back.

---
*Created on 2026-03-30*
