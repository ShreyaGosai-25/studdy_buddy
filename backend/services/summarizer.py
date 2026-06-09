from groq import Groq
import os
import os
from dotenv import load_dotenv

load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_summary(text):

    if not text.strip():
        return "No notes found."

def generate_summary(text, mode="Quick Revision Sheet"):

    prompt = f"""
You are an expert exam tutor.

Convert the notes into a STRICT STRUCTURED SUMMARY.

MODE: {mode}

OUTPUT FORMAT (MANDATORY):

📌 Topic Overview
- 2 to 3 short sentences only

🧠 Must Remember
• 4-6 bullet points only (no explanations)

📖 Key Terms
• term → meaning (very short)

🎯 Exam Tips
• likely exam questions
• important facts to memorize

RULES:
- No paragraphs
- No extra headings
- Strict formatting only
- Keep exam-focused content only

NOTES:
{text}
"""
    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    temperature=0,
    messages=[{"role": "user", "content": prompt}]
)
    return response.choices[0].message.content