# Resume Parser Project

## Overview
This project is a Python-based resume parsing tool that converts resume text into structured JSON data. It uses advanced natural language processing techniques to extract key information from resumes.

## Features
- Extract personal information (name, email, phone, location)
- Identify technical skills
- Parse work experience
- Extract educational background
- Capture project details
- Collect certifications

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/resume-parser.git
cd resume-parser
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage
1. Place your resume in Markdown format as `resume.md`
2. Run the parser
```bash
python resume_parser.py
```
3. The parsed data will be saved as `parsed_resume.json`

## Components
- `ResumeParser`: Main class for parsing resume
- Multiple extraction methods for different resume sections
- Flexible parsing using regex and spaCy NLP

## Future Improvements
- Support for multiple file formats (PDF, DOCX)
- More advanced NLP techniques
- Machine learning-based information extraction