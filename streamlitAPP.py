import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
import streamlit as st
from  src.mcqgenerator.mcqgen import generate_evaluation_chain
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

with open('response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)
    
st.title("MCQ Generator App")
with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])
    mcq_count = st.number_input("Number of MCQs to generate", min_value=3, max_value=20)
    subject = st.text_input("Subject")
    quiz_tone = st.pills("Tone", ['simple', 'moderate', 'tough'], selection_mode="single")
    button = st.form_submit_button("Generate MCQs")
    
    if button and uploaded_file is not None and mcq_count and subject and quiz_tone:
        with st.spinner("Processing..."):
            try:
                text = read_file(uploaded_file)
                print('text', text)
                with get_openai_callback() as cb:
                    result = generate_evaluation_chain(
                        {
                            "text": text,
                            "number":mcq_count,
                            "subject":subject,
                            "tone":quiz_tone,
                            "response_json":json.dumps(RESPONSE_JSON)
                        }
                    )
                logging.info(f"Result: {result}")
            except Exception as e:
                logging.error(f"Error: {e}")
                logging.error(traceback.format_exc())
                st.error(f"An error occurred: {e}")
                
    
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")  
        
        if isinstance(result, dict):
            quiz = result.get("quiz")
            review = result.get("review")
            if quiz:
                table_data = get_table_data(quiz)
                if table_data:
                    df = pd.DataFrame(table_data)
                    df.index = df.index + 1
                    st.table(df)
                    st.text_area("Quiz Review", value=review)
                else:
                    logging.error("Error: No quiz data found in the result.")
                    st.error("Failed to parse quiz data.")
    
        else:
            st.error("Unexpected result format. Please check the response structure.")
