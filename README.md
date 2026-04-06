# HireSense-AI---NLP-Powered-Resume-Analyzer

> An intelligent resume parsing and job description matching web app built with Python and Streamlit.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56-red?logo=streamlit)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-1.27-green)
![NLP](https://img.shields.io/badge/NLP-TF--IDF-orange)

---

## 📌 Overview

**HireSense AI** is an NLP-powered resume analyzer that helps recruiters and job seekers instantly evaluate how well a resume matches a job description. It extracts key information from PDF resumes and computes a match score using TF-IDF similarity and skill overlap analysis.

---

## ✨ Features

- 📄 **PDF Resume Parsing** — Extracts text from PDF resumes using PyMuPDF
- 👤 **Candidate Info Extraction** — Automatically detects name, email, phone, and location
- 🛠️ **Skill Extraction** — Identifies technical skills across programming, frameworks, databases, DevOps, and ML
- 🎓 **Education Parsing** — Detects degree, institution, and GPA
- 💼 **Experience Detection** — Extracts work experience sections
- 🎯 **Match Score** — Combines TF-IDF similarity and skill overlap to generate an overall match percentage
- ✅ **Matched & Missing Skills** — Shows which skills align with the job description and which are missing
- 🌐 **Interactive Web UI** — Clean, real-time interface built with Streamlit

---

<img width="1902" height="963" alt="image" src="https://github.com/user-attachments/assets/5c7e79b5-48e1-44d9-a1b7-3218ceaafc40" />


## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/HireSense-AI.git
cd HireSense-AI/resume_analyzer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the app**
```bash
streamlit run app.py
```

4. Open your browser at `http://localhost:8501`

---

## 📦 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core language |
| Streamlit | Web interface |
| PyMuPDF (fitz) | PDF text extraction |
| Scikit-learn | TF-IDF vectorization |
| Pandas & NumPy | Data processing |
| Regex (re) | Information extraction |

---

## 📁 Project Structure

```
HireSense-AI/
│
├── resume_analyzer/
│   ├── app.py              # Main Streamlit application
│   ├── requirements.txt    # Project dependencies
│   └── README.md           # Project documentation
```

---

## 🧠 How It Works

1. User uploads a **PDF resume**
2. User pastes a **Job Description**
3. App extracts text using **PyMuPDF**
4. **Regex patterns** identify candidate info, skills, education, and experience
5. **TF-IDF vectorization** computes text similarity between resume and JD
6. **Skill overlap** is calculated between extracted skills and JD keywords
7. A **weighted match score** is generated and displayed

---

## 📊 Match Score Formula

```
Match Score = (TF-IDF Similarity × 0.5) + (Skill Overlap × 0.5)
```

---

## 🌐 Live Demo

> Coming soon — deploying to Streamlit Cloud

---

## 🙋‍♀️ Author

**Valluru Manju Priya**
- 📧 vallurumanjupriya4321@gmail.com
- 📱 +91-6305198106
- 📍 Guntur, Andhra Pradesh

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
