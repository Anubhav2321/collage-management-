import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
from pypdf import PdfReader
import docx

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def _clean_json_response(response_text):
    if "```" in response_text:
        pattern = r"```json(.*?)```"
        match = re.search(pattern, response_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            return response_text.replace("```json", "").replace("```", "").strip()
    return response_text.strip()

def extract_text_from_file(file_obj, file_ext):
    text = ""
    try:
        if file_ext == '.pdf':
            reader = PdfReader(file_obj)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif file_ext == '.docx':
            doc = docx.Document(file_obj)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif file_ext == '.txt':
            if hasattr(file_obj, 'read'):
                try: text = file_obj.read().decode('utf-8')
                except: 
                    file_obj.seek(0)
                    text = file_obj.read().decode('latin-1')
            else:
                with open(file_obj, 'r', encoding='utf-8') as f:
                    text = f.read()
    except Exception as e:
        print(f"Error extracting text: {e}")
    return text

# --- 1. QUIZ GENERATOR ---
def generate_quiz_from_doc(file_obj, file_ext):
    text = extract_text_from_file(file_obj, file_ext)
    text = text[:20000] 
    
    if not text.strip(): return []

    prompt = f"""
    You are an expert examiner. Based on the provided text, create a 30-mark quiz.
    Create exactly 30 Multiple Choice Questions (MCQs).
    
    OUTPUT RULES:
    1. Return ONLY valid JSON.
    2. JSON format: {{ "questions": [ {{ "question": "...", "options": ["A","B","C","D"], "answer": 0 }} ] }}
    
    TEXT:
    {text}
    """

    try:
        # UPDATED MODEL: llama-3.1-8b-instant
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a strict JSON generator API."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        raw_content = completion.choices[0].message.content
        cleaned_content = _clean_json_response(raw_content)
        quiz_data = json.loads(cleaned_content)
        
        if "questions" in quiz_data: return quiz_data["questions"]
        elif isinstance(quiz_data, list): return quiz_data
        return []
        
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return []

# --- 2. AI TUTOR (CHATBOT) ---
def ask_ai_tutor(student_question, student_level="Intermediate"):
    system_prompt = f"""
    You are a helpful AI Tutor named 'Learning-365 AI'.
    Student Level: {student_level}.
    Keep answers concise.
    """

    try:
        # UPDATED MODEL: llama-3.3-70b-versatile
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": student_question}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        print(f"AI Tutor Error: {e}")
        return "Sorry, I am currently undergoing maintenance (Model Update). Please try again later."