import streamlit as st
import base64
from gemini_process import extract_text_from_pdf, generate_report_sections

def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()

    bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .title-text {{
        color: #ffffff;
        font-size: 2.8rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }}
    .subtext {{
        color: #e0e0e0;
        font-size: 1.2rem;
        text-align: center;
    }}
    .report-section {{
        background-color: rgba(255, 255, 255, 0.2);
        padding: 15px;
        border-radius: 10px;
        color: #ffffff;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }}
    .section-header {{
        color: #ffcc00;
        font-size: 1.4rem;
        margin: 15px 0;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

set_background("background.jpg")

st.markdown("<div class='title-text'>Medical Report Summarizer</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtext'>Upload a medical report (PDF) and choose which outputs to generate.</div>",
    unsafe_allow_html=True,
)


selected_sections = st.multiselect(
    "Select outputs to generate:",
    options=["Summary", "Conclusion", "Precautions", "Recommendations"],
    default=["Summary"],  
)

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    with st.expander("📄 View Full Original Report"):
        text = extract_text_from_pdf(uploaded_file)
        st.text_area("Original Text", text, height=200)

    if st.button("Generate Report"):
        if not selected_sections:
            st.error("Please select at least one output option.")
        else:
            with st.spinner("Generating results..."):
                try:
                    text = extract_text_from_pdf(uploaded_file)
                    report_sections = generate_report_sections(text, selected_sections)
                    
                
                    for section, content in report_sections.items():
                        st.markdown(f"<div class='section-header'>🔍 {section}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div class='report-section'>{content}</div>", unsafe_allow_html=True)
                           
                    complete_report = ""
                    for section in selected_sections:
                        complete_report += f"{section}:\n{report_sections.get(section, '')}\n\n"
                        
                    st.download_button("⬇️ Download Complete Report", complete_report, "report_summary.txt", "text/plain")
                except Exception as e:
                    st.error(f"Error: {e}")

st.markdown("<br><hr><center>🩺 Made for Healthcare </center>", unsafe_allow_html=True)