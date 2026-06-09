




import os
import json
import re


from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# LOAD ENV VARIABLES
# -----------------------------


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -----------------------------
# SAFE JSON PARSER
# -----------------------------
def safe_json_parse(text: str):
    if not text:
        raise ValueError("Empty response from LLM")

    text = text.strip()

    # remove markdown blocks if model returns them
    text = text.replace("```json", "")
    text = text.replace("```", "")

    matches = re.findall(r"\{.*\}", text, re.DOTALL)

    if matches:
        text = matches[0]

    return json.loads(text)


# -----------------------------
# QUIZ GENERATION
# -----------------------------
def generate_quiz(
    user_id,
    subject,
    difficulty,
    mcq_count=5,
    short_count=2,
    long_count=1,
    multi_select=False
):

    prompt = f"""
Return ONLY valid JSON.

Generate:

- {mcq_count} MCQs
- {short_count} Short Questions
- {long_count} Long Questions

Subject: {subject}
Difficulty: {difficulty}

JSON FORMAT:

{{
  "mcqs": [
    {{
      "question": "",
      "options": ["", "", "", ""],
      "multi_select": {str(multi_select).lower()},
      "answer": "",
      "explanation": ""
    }}
  ],

  "short_questions": [
    {{
      "question": "",
      "answer": "",
      "keywords": []
    }}
  ],

  "long_questions": [
    {{
      "question": "",
      "answer": "",
      "key_points": []
    }}
  ]
}}

Rules:
- Generate exactly {mcq_count} MCQs
- Generate exactly {short_count} short questions
- Generate exactly {long_count} long questions
- MCQs must contain exactly 4 options
- answer must exactly match one option
- explanation should explain why the answer is correct
- short question answers should be concise
- include important keywords list for short questions
- long question answers should be detailed
- include key_points list for long questions
- Return ONLY JSON
"""
    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict JSON generator. "
                        "Return ONLY valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content

        quiz = safe_json_parse(content)

        return {
            "success": True,
            "quiz": quiz
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
            "raw_output": content if "content" in locals() else None
        }


# -----------------------------
# QUIZ EVALUATION
# -----------------------------
def evaluate_quiz(correct_answers, student_answers):

    score = 0
    results = []

    total = len(correct_answers)

    for question_id, correct in correct_answers.items():

        student = student_answers.get(question_id)

        is_correct = correct == student

        if is_correct:
            score += 1

        results.append(
            {
                "question_id": question_id,
                "correct": correct,
                "student": student,
                "is_correct": is_correct
            }
        )

    return {
        "score": score,
        "total": total,
        "percentage": round(
            (score / total) * 100, 2
        ) if total > 0 else 0,
        "results": results
}

# -----------------------------
# WRITTEN ANSWER EVALUATION
# -----------------------------
def evaluate_written_answer(
    question,
    expected_answer,
    student_answer
):
    prompt = f"""
Question:
{question}

Expected Answer:
{expected_answer}

Student Answer:
{student_answer}

Evaluate the student's answer fairly.

Return ONLY valid JSON:

{{
    "score": 0,
    "out_of": 10,
    "is_correct": true,
    "feedback": "",
    "correct_answer": ""
}}

Rules:
- Score from 0 to 10
- Accept equivalent wording
- Accept paraphrased answers
- Do not require exact matching
- Explain what was missing
- correct_answer should contain a good model answer
- Return ONLY JSON
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an educational evaluator. "
                        "Return ONLY valid JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content

        return safe_json_parse(content)

    except Exception as e:

        return {
            "score": 0,
            "out_of": 10,
            "is_correct": False,
            "feedback": f"Evaluation failed: {str(e)}",
            "correct_answer": expected_answer
        }