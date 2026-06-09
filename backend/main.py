




from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel

from backend.services.quiz_llm import (
    generate_quiz,
    evaluate_quiz,
    evaluate_written_answer
)

from backend.vector_db.study_store import (
    add_content,
    add_content_from_file,
    retrieve_context   # ✅ IMPORTANT FIX for summary
)

from backend.services.planner import generate_weekly_timetable
from backend.models.timetable_models import TimetableRequest

app = FastAPI()


# ---------------- STUDY ADD ---------------- #
@app.post("/study/add")
def add_study_content(
    user_id: str = Form(...),
    subject: str = Form(...),
    content: str = Form(""),
    file: UploadFile | None = None
):
    if content:
        add_content(user_id, subject, content)

    if file:
        add_content_from_file(user_id, subject, file)

    return {"status": "content added"}


# ---------------- QUIZ ---------------- #
class QuizRequest(BaseModel):
    user_id: int
    subject: str
    difficulty: str
    mcq_count: int = 5
    short_count: int = 2
    long_count: int = 1
    multi_select: bool = False


@app.post("/quiz/generate")
def quiz_generate(req: QuizRequest):
    try:
        quiz = generate_quiz(
            user_id=req.user_id,
            subject=req.subject,
            difficulty=req.difficulty,
            mcq_count=req.mcq_count,
            short_count=req.short_count,
            long_count=req.long_count,
            multi_select=req.multi_select
        )

        return quiz

    except Exception as e:
        return {
            "success": False,
            "error": "Quiz generation failed",
            "details": str(e)
        }


# ---------------- QUIZ EVAL ---------------- #
class EvalRequest(BaseModel):
    correct_answers: dict
    student_answers: dict


@app.post("/quiz/evaluate")
def evaluate_quiz_api(req: EvalRequest):
    return evaluate_quiz(req.correct_answers, req.student_answers)


class WrittenEvalRequest(BaseModel):
    question: str
    expected_answer: str
    student_answer: str


@app.post("/quiz/evaluate-written")
def evaluate_written_api(req: WrittenEvalRequest):
    return evaluate_written_answer(
        question=req.question,
        expected_answer=req.expected_answer,
        student_answer=req.student_answer
    )


# ---------------- TIMETABLE ---------------- #
@app.post("/timetable/generate")
def generate_timetable_api(request: TimetableRequest):
    return generate_weekly_timetable(request)


# ---------------- SUMMARY FIX (IMPORTANT) ---------------- #
# ---------------- SUMMARY FIX (IMPORTANT) ---------------- #
from backend.services.summarizer import generate_summary   # or correct path

@app.get("/study/summarize")
def summarize(user_id: str, subject: str, mode: str = "Quick Revision Sheet"):

    context = retrieve_context(user_id, subject)

    if not context:
        return {
            "success": False,
            "summary": None,
            "message": "No notes found"
        }

    try:
        # ✅ REAL AI SUMMARY (NOT slicing anymore)
        summary = generate_summary(context, mode)

        return {
            "success": True,
            "summary": summary
        }

    except Exception as e:
        return {
            "success": False,
            "summary": None,
            "message": str(e)
 



        }
    


from groq import Groq
import traceback
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ IMPORTANT: create client ONCE (not inside function)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.post("/study/query")
def study_query(payload: dict):

    try:
        user_id = payload.get("user_id")
        subject = payload.get("subject")
        query = payload.get("query")

        if not query:
            raise HTTPException(status_code=400, detail="Query is empty")

        # 1. Get stored notes safely
        try:
            context = retrieve_context(user_id, subject)
        except Exception:
            context = ""

        if not context:
            context = "No notes available for this subject."

        # 2. SAFE PROMPT
        prompt = f"""
You are an expert tutor.

Use the study notes below to answer the question.

NOTES:
{context}

QUESTION:
{query}

Rules:
- simple explanation
- exam focused
- give examples if needed
"""

        # 3. GROQ CALL (SAFE)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        answer = response.choices[0].message.content

        return {
            "success": True,
            "answer": answer
        }

    except Exception as e:
        print("🔥 ERROR IN /study/query:")
        print(traceback.format_exc())

        return {
            "success": False,
            "error": str(e)
        }