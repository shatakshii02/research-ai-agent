# 🔎 AI Research Agent – Internship Assignment

This project is a simple **AI Research Assistant** built as part of my internship take-home task.

It takes a user query, finds relevant sources online, extracts their content, summarizes it using an LLM, saves the results into a database, and provides a Streamlit web UI to view current and past reports.

---

## 🛠 How It Works

### Architecture
User → Streamlit UI → SerpAPI (search) → Trafilatura/PyPDF (extract)
→ Groq LLaMA3 (summarize) → SQLite DB (save) → Streamlit history view


- **Search**: Uses [SerpAPI](https://serpapi.com/) to fetch top web results for the query.  
- **Extract**: Cleans article text via [Trafilatura](https://trafilatura.readthedocs.io/) and [PyPDF](https://pypdf.readthedocs.io/) for PDFs.  
- **Summarize**: Uses [Groq API](https://console.groq.com) with **LLaMA-3.1-8B Instant** to produce a structured Markdown report with key findings and links.  
- **Store**: Saves reports to a lightweight **SQLite database**.  
- **UI**: Streamlit web app with:
  - Input box for new queries  
  - Sidebar listing past reports  
  - Click to open and view saved reports  

---

## ▶️ How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/<your-username>/research-ai-agent.git
   cd research-ai-agent

2. Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate   # on Windows
source venv/bin/activate  # on macOS/Linux


3. Install dependencies:
pip install -r requirements.txt


4. Create a .env file in the project root:
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
SERPAPI_KEY=your_serpapi_key


5. Run the app:
streamlit run app.py

Open the browser at http://localhost:8501


📝 Example Results
Query: What is Agentic AI and Generative AI?

Report (summarized):

Definition of Agentic AI: AI systems that autonomously make decisions and pursue goals with limited supervision.

Primary Function of Generative AI: Produces new content (text, images, code, etc.).

Key Difference: Agentic AI is proactive and goal-driven; Generative AI is reactive and input-driven.

Complexity: Agentic AI handles multi-step, adaptive goals; Generative AI focuses on narrow tasks.

Collaboration: Agentic AI may use Generative AI for content creation or communication.

Adaptability: Agentic AI adjusts plans dynamically in changing situations.

Limitations of Generative AI: Output reflects biases of training data.

Autonomy: Raises questions of ethics and accountability.

Takeaway:
Agentic AI = autonomous action toward goals.
Generative AI = creation of new content.
They complement each other but serve distinct purposes.

🤝 AI Assistance

I used AI help (ChatGPT) for:

Setting up the project structure

Debugging .env issues

Replacing OpenAI GPT with Groq LLaMA-3

Drafting this README

All core implementation and testing were done by me.

📌 Tech Stack

LLM: Groq LLaMA-3.1-8B Instant

Search: SerpAPI (Google results)

Extract: Trafilatura, PyPDF

Database: SQLite

Frontend: Streamlit