import streamlit as st
import json
import os
from resume_parser import ResumeParser
from file_converter import FileConverter

# Set page configuration
st.set_page_config(
    page_title="ResumeNija - Resume Parser",
    page_icon="ud83dudcc4",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4257B2;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #3A3B7B;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid #e6e6e6;
        padding-bottom: 0.3rem;
    }
    .info-box {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .highlight {
        background-color: #ffffcc;
        padding: 0.2rem;
        border-radius: 3px;
    }
    .file-info {
        color: #6c757d;
        font-size: 0.9rem;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'parsed_data' not in st.session_state:
    st.session_state.parsed_data = None
if 'uploaded_file_content' not in st.session_state:
    st.session_state.uploaded_file_content = None
if 'file_name' not in st.session_state:
    st.session_state.file_name = None
if 'file_type' not in st.session_state:
    st.session_state.file_type = None
if 'raw_text' not in st.session_state:
    st.session_state.raw_text = None

# Title and description
st.markdown('<h1 class="main-header">ResumeNija - Resume Parser</h1>', unsafe_allow_html=True)
st.markdown(
    """Convert your resume into structured data using advanced NLP techniques. 
    Upload your resume to get started."""
)

# Sidebar
with st.sidebar:
    st.markdown('<h2 class="section-header">Upload Resume</h2>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "md", "txt"])
    
    if uploaded_file is not None:
        # Get file type
        file_extension = uploaded_file.name.split('.')[-1].lower()
        st.session_state.file_type = file_extension
        st.session_state.file_name = uploaded_file.name
        
        # Read and convert file content
        file_content = uploaded_file.read()
        st.session_state.uploaded_file_content = file_content
        
        # Display file info
        st.markdown(f"<p class='file-info'>File: {uploaded_file.name} ({file_extension.upper()} format)</p>", unsafe_allow_html=True)
        
        # Convert to text
        try:
            with st.spinner("Converting file to text..."):
                text_content = FileConverter.convert_to_text(file_content, file_extension)
                st.session_state.raw_text = text_content
                st.success(f"Successfully extracted text from {file_extension.upper()} file")
        except Exception as e:
            st.error(f"Error converting file: {str(e)}")
        
        # Parse button
        if st.session_state.raw_text and st.button("Parse Resume"):
            with st.spinner("Parsing resume..."):
                parser = ResumeParser()
                st.session_state.parsed_data = parser.parse_resume(st.session_state.raw_text)
                st.success("Resume parsed successfully!")
    
    st.markdown('<h2 class="section-header">About</h2>', unsafe_allow_html=True)
    st.info(
        """ResumeNija is a powerful resume parsing tool that uses Natural Language Processing 
        to extract structured information from your resume. It supports PDF, DOCX, Markdown, and TXT files."""
    )

# Main content area
if st.session_state.parsed_data:
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Parsed Data", "Raw Text", "JSON Output"])
    
    with tab1:
        # Personal Information
        st.markdown('<h2 class="section-header">Personal Information</h2>', unsafe_allow_html=True)
        personal_info = st.session_state.parsed_data.get("personal_info", {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Name:** {personal_info.get('name', 'Not found')}")
            st.markdown(f"**Email:** {personal_info.get('email', 'Not found')}")
        with col2:
            st.markdown(f"**Phone:** {personal_info.get('phone', 'Not found')}")
            st.markdown(f"**Location:** {personal_info.get('location', 'Not found')}")
        
        # Skills
        st.markdown('<h2 class="section-header">Skills</h2>', unsafe_allow_html=True)
        skills = st.session_state.parsed_data.get("skills", [])
        if skills:
            st.markdown(', '.join([f"<span class='highlight'>{skill}</span>" for skill in skills]), unsafe_allow_html=True)
        else:
            st.markdown("No skills found")
        
        # Work Experience
        st.markdown('<h2 class="section-header">Work Experience</h2>', unsafe_allow_html=True)
        experiences = st.session_state.parsed_data.get("work_experience", [])
        if experiences:
            for exp in experiences:
                with st.expander(f"{exp.get('job_title', 'Role')} at {exp.get('company', 'Company')}"):
                    st.markdown(f"**Duration:** {exp.get('duration', 'Not specified')}")
        else:
            st.markdown("No work experience found")
        
        # Education
        st.markdown('<h2 class="section-header">Education</h2>', unsafe_allow_html=True)
        education = st.session_state.parsed_data.get("education", [])
        if education:
            for edu in education:
                st.markdown(f"**{edu.get('degree', 'Degree')}** from {edu.get('institution', 'Institution')}")
        else:
            st.markdown("No education information found")
        
        # Projects
        st.markdown('<h2 class="section-header">Projects</h2>', unsafe_allow_html=True)
        projects = st.session_state.parsed_data.get("projects", [])
        if projects:
            for project in projects:
                with st.expander(project.get('name', 'Project')):
                    st.markdown(project.get('description', 'No description available'))
        else:
            st.markdown("No projects found")
        
        # Certifications
        st.markdown('<h2 class="section-header">Certifications</h2>', unsafe_allow_html=True)
        certifications = st.session_state.parsed_data.get("certifications", [])
        if certifications:
            for cert in certifications:
                st.markdown(f"- {cert}")
        else:
            st.markdown("No certifications found")
    
    with tab2:
        # Raw Text
        st.markdown('<h2 class="section-header">Raw Text from Resume</h2>', unsafe_allow_html=True)
        st.text_area("Extracted Text", st.session_state.raw_text, height=400)
    
    with tab3:
        # JSON Output
        st.markdown('<h2 class="section-header">JSON Output</h2>', unsafe_allow_html=True)
        st.json(st.session_state.parsed_data)
        
        # Download button for JSON
        json_str = json.dumps(st.session_state.parsed_data, indent=2)
        st.download_button(
            label="Download JSON",
            data=json_str,
            file_name="parsed_resume.json",
            mime="application/json"
        )

elif st.session_state.raw_text and not st.session_state.parsed_data:
    # Show the uploaded content but not yet parsed
    st.markdown('<h2 class="section-header">Extracted Text from Resume</h2>', unsafe_allow_html=True)
    st.text_area("Resume Content", st.session_state.raw_text, height=300)
    st.info("Click 'Parse Resume' in the sidebar to extract information from this resume.")

else:
    # Initial state - no file uploaded
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown(
        """### Getting Started
        1. Upload your resume using the sidebar (PDF, DOCX, Markdown, or TXT)
        2. Review the extracted text
        3. Click 'Parse Resume' to extract structured information
        4. View the parsed data and download as JSON
        
        **Supported File Formats:**
        - PDF (.pdf)
        - Microsoft Word (.docx)
        - Markdown (.md)
        - Plain Text (.txt)
        """
    )
    st.markdown('</div>', unsafe_allow_html=True)
