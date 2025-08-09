import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith('.pdf'):
        try:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF file: {e}")
        
    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')
    
    else:
        raise ValueError("Unsupported file format. Please upload a .pdf or .txt file.")
    
def get_table_data(quiz_str):
    try:
        quiz_data = json.loads(quiz_str)
        quiz_table_data = []
        
        for key, val in quiz_data.items():
            mcq = val.get("mcq")
            options = " | ".join([
                f"{option_key} : {option_val}" for option_key, option_val in val.get("options").items()
            ])
            # print(options)
            correct = val.get("correct")
            
            quiz_table_data.append({
                "Question": mcq,
                "Options": options,
                "Correct Answer": correct
            }) 
            
        return quiz_table_data
        
    except Exception as e:
        traceback.print_exc()
        return False
    