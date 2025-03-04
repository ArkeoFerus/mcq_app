import streamlit as st
from PyPDF2 import PdfReader
from transformers import pipeline

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file.
    """
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to generate MCQs using Hugging Face Transformers
def generate_mcqs(text, num_questions=5):
    """
    Generates multiple-choice questions (MCQs) from the given text using a pre-trained model.
    """
    prompt = f"""
    Generate {num_questions} multiple-choice questions (MCQs) based on the following text:
    
    {text}
    
    Each question should have 4 options and a correct answer. Format the output as follows:
    
    Question 1: [Question text]
    A) [Option 1]
    B) [Option 2]
    C) [Option 3]
    D) [Option 4]
    Correct Answer: [Correct option]
    
    Repeat for all questions.
    """
    # Load the text generation pipeline
    mcq_pipeline = pipeline("text2text-generation", model="t5-small")
    # Generate MCQs
    response = mcq_pipeline(prompt, max_length=512)
    return response[0]['generated_text']

# Streamlit App
def main():
    st.title("MCQ Generator from PDF")
    st.write("Upload a PDF file, and we'll generate MCQs for you!")

    # File upload
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        # Extract text from PDF
        text = extract_text_from_pdf(uploaded_file)
        st.write("Text extracted from PDF successfully!")

        # Number of questions
        num_questions = st.slider("Number of questions", min_value=1, max_value=10, value=5)

        # Generate MCQs
        if st.button("Generate MCQs"):
            st.write("Generating MCQs...")
            mcqs = generate_mcqs(text, num_questions)
            st.write("### Generated MCQs:")
            st.write(mcqs)

# Run the app
if __name__ == "__main__":
    main()
