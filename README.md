# 🚀 NeuralCompile: AI-Driven Code Intelligence Engine

An advanced multi-language code analysis and execution platform developed during the **Infosys Springboard Internship**. It integrates static analysis with Large Language Models (LLMs) to provide real-time debugging, optimization, and structural visualization.

---

## 📌 Project Overview
**NeuralCompile** streamlines the developer workflow by combining deep **AST (Abstract Syntax Tree)** analysis with high-speed AI inference. It doesn't just find bugs; it visualizes the logic and persists execution history for better developer productivity.

## ✨ Key Features

### 🧠 1. AI-Powered Debugging & Review
* **Static Analysis:** Uses Python’s `ast` module to detect unused variables, imports, and PEP8 compliance issues.
* **LLM Orchestration:** Powered by **LangChain** and **Groq API** (`llama-3.1-8b`) for ultra-low latency logic suggestions (<500ms).
* **Semantic Review:** Goes beyond syntax to identify logical flaws and provide professional-grade code refactoring.

### 📊 2. Logic & Flow Visualization
* **Dynamic CFG:** Automatically generates **Control Flow Graphs** to visualize complex loops and conditional execution paths.
* **Algorithm Visualizer:** Provides step-by-step logic transparency for DSA-based code snippets.

### 💾 3. Data Persistence & Performance
* **Synchronized History:** Uses **SQLite** to store chat history and the latest **10 code execution logs**.
* **State Management:** Built with **Reflex**, ensuring a reactive full-stack experience entirely in Python.
* **Optimized Inference:** Leverages **Groq**'s LPU for near-instantaneous generative AI feedback.

---

## 🛠️ Tech Stack
| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **Frontend/Backend** | Reflex (Full-stack Python Framework) |
| **AI Orchestration** | LangChain |
| **LLM Inference** | Groq Cloud API (Llama 3.1) |
| **Database** | SQLite |
| **Core Logic** | AST, PyTorch (Evaluation) |

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher
- Groq API Key

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/naveen-rondla-2005/NeuralCompile.git](https://github.com/naveen-rondla-2005/NeuralCompile.git)
cd NeuralCompile

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
