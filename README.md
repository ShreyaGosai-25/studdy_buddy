# Study_Sync
#  AI-POWERED STUDENT PRODUCTIVITY SYSTEM

## Table of Contents
- Overview  
- Features  
- System Architecture  
- Key Components  
  - Timetable Generator  
  - Task Tracker  
  - Study & Quiz System  
  - AI Assistant  
- UI/UX and Web Deployment  
- Installation and Usage  
- Project Structure  
- License  

---

# 1. Overview

STUDDYBUDDY is a modular AI-powered student productivity system designed to improve academic efficiency through structured planning, practice, and intelligent assistance.

The system integrates four core modules:

- Timetable Generation System  
- Task Tracking System  
- Quiz and MCQ Generator  
- AI Academic Assistant  

Each module is independent but connected under a unified interface.

---

# 2. Features

## Smart Academic Planning
- Personalized timetable generation  
- Subject-wise scheduling  
- Exam-focused planning mode  

## Task Management System
- Daily academic task tracking  
- Progress monitoring  
- Priority-based organization  

## Study & Quiz Engine
- Automatic MCQ generation  
- Topic-based learning quizzes  
- Difficulty-based question control  

## AI Assistant
- Academic question answering  
- Context-aware responses  
- Retrieval-based knowledge system  

---

# 3. System Architecture

Input (User Actions / Study Preferences / Queries)  
→ Module Selection Layer  
→ Processing Engine (Per Module)  
→ AI/Logic Layer  
→ Output Renderer (Streamlit UI)  

Each module operates independently and communicates through a shared UI layer.

---

# 4. Key Components

---

## 4.1 Timetable Generator

### Description
Generates structured study schedules based on user-defined constraints.

### Workflow
User Inputs → Subject Analysis → Time Allocation Engine → Schedule Generator → Output Timetable

### Input
- Subjects list  
- Study hours per day  
- Exam priorities  
- Optional constraints (breaks, weak subjects)  

### Output
- Daily schedule  
- Weekly timetable  
- Revision slots  

---

## 4.2 Task Tracker

### Description
A lightweight academic task management system for tracking daily progress.

### Workflow
Task Input → Storage Layer → Status Update Engine → Dashboard Renderer  

### Features
- Add tasks  
- Mark complete / pending  
- Priority tagging  
- Progress tracking  

### Output
- Task dashboard  
- Completion status summary  

---

## 4.3 Study & Quiz System

### Description
Generates MCQs and quizzes from topics or study material.

### Workflow
Input Text/Topic → Processing Layer → Question Generator → Options Builder → Answer Key Output  

### Features
- MCQ generation  
- Topic-based quiz creation  
- Difficulty control  
- Answer validation  

### Output
- Question sets  
- Answer keys  
- Optional scoring system  

---

## 4.4 AI Assistant

### Description
A retrieval-augmented AI chatbot for academic question answering.

### Workflow
User Query  
→ Embedding Model  
→ Vector Database (FAISS)  
→ Context Retrieval  
→ LLM Response Generation  

### Components
- FAISS vector database  
- HuggingFace embeddings  
- LLM via CTransformers / LLaMA-based model  
- Prompt engineering layer  

### Output
- Context-aware answers  
- Subject explanations  
- Exam-oriented responses  

---

# 5. UI/UX and Web Deployment

- Built using Streamlit  
- Sidebar-based module navigation  
- Simple input-driven interface  
- Real-time output rendering  
- Lightweight and responsive UI  

  

---

# 6. Installation and Usage

## Prerequisites
- Python 3.10+  
- pip  
- Streamlit  

---

## Setup



```bash
##run
git clone https://github.com/your-username/studdybuddy.git
cd studdybuddy
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt

```
## Run Application

After completing the setup, start the Streamlit app using the following command:

```bash
streamlit run app.py
```

link:
https://studdybuddy-cpgybh5ygxjun3ansyrqdh.streamlit.app/

