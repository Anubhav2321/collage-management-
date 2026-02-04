import random
import re
import os
from pypdf import PdfReader
from docx import Document
from django.conf import settings

def extract_text_from_file(file_path):
    """
    যেকোনো PDF বা DOCX ফাইল থেকে টেক্সট বের করার ফাংশন।
    """
    text = ""
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == '.pdf':
            reader = PdfReader(file_path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        
        elif ext == '.docx':
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        
        else:
            # For .txt or other formats
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
                
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

    return text

def generate_quiz_from_text(text, num_questions=5):
    """
    টেক্সট থেকে সাধারণ লজিক ব্যবহার করে MCQ প্রশ্ন তৈরির ফাংশন।
    (Note: ভালো ফলাফলের জন্য OpenAI/Gemini API ব্যবহার করা উচিত, 
    তবে এখানে আমি Python Logic দিয়ে বানিয়ে দিচ্ছি যাতে API Key ছাড়াই কাজ করে)
    """
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    questions = []
    
    # এমন বাক্য খুঁজবো যাতে গুরুত্বপূর্ণ কিওয়ার্ড আছে (যেমন: is, are, called, defined)
    keywords = ['is a', 'is the', 'are', 'means', 'defined as', 'refers to', 'known as']
    
    valid_sentences = [s.strip() for s in sentences if len(s.split()) > 5 and len(s.split()) < 30]
    
    # Shuffle to get random parts of the chapter
    random.shuffle(valid_sentences)

    for sentence in valid_sentences:
        if len(questions) >= num_questions:
            break
            
        for key in keywords:
            if key in sentence:
                try:
                    # Logic: "Python is a programming language" -> Q: "Python ___ a programming language?"
                    parts = sentence.split(key, 1)
                    if len(parts) == 2:
                        subject = parts[0].strip()
                        definition = parts[1].strip().strip('.')
                        
                        # প্রশ্ন তৈরি
                        question_text = f"What {key} {definition}?"
                        if len(subject.split()) > 4: # Subject যদি খুব বড় হয়, তাহলে উল্টে দেব
                            question_text = f"{subject} {key} _____________."
                            correct_ans = definition
                        else:
                            question_text = f"What {key} {definition}?"
                            correct_ans = subject

                        # ডামি অপশন তৈরি (ভুল উত্তর)
                        options = [correct_ans, "None of the above", "Variable", "Function"]
                        random.shuffle(options)
                        
                        # সঠিক উত্তরের ইনডেক্স বের করা
                        ans_idx = options.index(correct_ans)
                        
                        questions.append({
                            'question': question_text,
                            'options': options,
                            'answer': ans_idx  # 0, 1, 2, or 3
                        })
                        break
                except:
                    continue

    # যদি ফাইল থেকে যথেষ্ট প্রশ্ন না পাওয়া যায়, তবে কিছু ডিফল্ট প্রশ্ন দেওয়া হবে
    if len(questions) < 2:
        questions.append({
            'question': 'Could not extract enough context. Select the topic type:',
            'options': ['Programming', 'History', 'Science', 'General'],
            'answer': 0
        })

    return questions