# AI-Driven Code Reviewer 🚀

An automated code review system developed as part of the **Infosys Springboard Internship**. This tool helps developers and students identify code smells, unused dependencies, and provides AI-powered suggestions to improve code quality.

## 📌 Project Overview
The **AI-Driven Code Reviewer** leverages Python's Abstract Syntax Tree (AST) for deep static analysis and integrates with Large Language Models (LLMs) via Groq to provide real-time feedback.

---

## ✨ Key Features (Milestone 1)
* **Static Code Analysis:** Automatically detects **unused imports** and **unused variables** to keep the codebase clean.
* **AI Technical Review:** Uses the `llama-3.1-8b-instant` model on **Groq** to provide 2-line professional feedback on code logic.
* **FastAPI Integration:** Offers a robust and fast API endpoint for code analysis.
* **Security First:** Implements environment variable management for API keys using `python-dotenv`.

---

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
* **AI Engine:** [Groq Cloud API](https://console.groq.com/) (Llama 3.1)
* **Logic:** `ast` (Abstract Syntax Trees)

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone [https://github.com/naveen-rondla-2005/AI-Code-Reviewer.git](https://github.com/naveen-rondla-2005/AI-Code-Reviewer.git)
cd AI-Code-Reviewer