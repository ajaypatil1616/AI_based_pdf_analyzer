from agno.agent import Agent
from agno.models.google import Gemini
import PyPDF2
# import os
# from dotenv import load_dotenv
# load_dotenv()
# api_key = os.environ.get("API_KEY")
import streamlit as st

api_key = st.secrets["API_KEY"]

def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        raise Exception(f"Error reading PDF file: {str(e)}")


def generate_report_sections(text, selected_sections):
    agent = Agent(
        model=Gemini(id="gemini-1.5-flash", api_key=api_key),
        markdown=True,
    )
    results = {}

    if "Summary" in selected_sections:
        summary_response = agent.run(
            f"summerize the following medical report:\n\n{text}"
        )
        results["Summary"] = summary_response.content

    if "Conclusion" in selected_sections:
        conclusion_response = agent.run(
            f"Based on the medical report provided below, what is the conclusion or actual result? "
            f"Provide a clear and concise conclusion:\n\n{text}"
        )
        results["Conclusion"] = conclusion_response.content

    if "Precautions" in selected_sections:
        precautions_response = agent.run(
            f"Based on the medical report below, list bullet points of precautions that should be taken. "
            f"Format the response as bullet points:\n\n{text}"
        )
        results["Precautions"] = precautions_response.content

    if "Recommendations" in selected_sections:
        recommendations_response = agent.run(
            f"Based on the medical report below, provide recommendations for further action. "
            f"Format the response as bullet points if applicable:\n\n{text}"
        )
        results["Recommendations"] = recommendations_response.content

    return results
