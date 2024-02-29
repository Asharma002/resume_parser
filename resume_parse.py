
    
import streamlit as st
import fitz
import re
import json
def main():
    # def save_uploaded_file(uploaded_file):
    #     with open("temp_resume.pdf", "wb") as f:
    #         f.write(uploaded_file.getbuffer())
    # return "temp_resume.pdf"
    def extract_text_from_pdf(pdf_path):
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        return text

    def extract_name(resume_text):
        lines = resume_text.split("\n")
        for line in lines:
            if line.strip() != "":
                name = line.title()  
                return name

    def extract_email(resume_text):
        email = re.findall(r'\S+@\S+', resume_text)
        if email:
            return email[0]

    def extract_phone_number(resume_text):
        phone = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', resume_text)
        if phone:
            phone_number = phone[0].replace("(", "").replace(")", "")
            return phone_number

    def get_headings(resume_text):
        lines = resume_text.split("\n")
        allowed_headings = ['Experience Highlights', 'Work Experience', 'Publications [Conference]', 'Achievements', 'Areas of Leadership', 'Career Summary', 'Experience', 'Summary', 'Employment History', 'Professional Background', 'Professional History', 'Areas of Experience', 'Areas of Specialization', 'Technical Skills', 'Career', 'Certifications', 'Work Experience', 'Areas of Expertise', 'Areas of Strength', 'Areas of Knowledge', 'Career Experience', 'Languages', 'Profile', 'Publications', 'Skills Summary', 'Areas of Interest', 'References', 'Research', 'Professional Experience', 'Achievements', 'Experience Profile', 'Areas of Responsibility', 'Areas of Concentration', 'Projects', 'Skills', 'Career Highlights', 'Areas of Competence', 'Professional Profile', 'Core Competencies', 'Areas of Focus', 'Experience Summary', 'Employment', 'Objective', 'Core Strengths', 'Interests', 'Work History', 'Courses', 'Professional Summary', 'Strengths', 'Professional Skills', 'Education', 'Career Profile', 'Internship Experience', 'Publications', 'Conference', 'Journal', 'Activities', 'Research', 'ACADEMIC ACTIVITIES','SKILLS','EDUCATION']
        headings = []
        for line in lines:
            if line.strip() != "":
                if line in allowed_headings:
                    headings.append(line)
        if len(headings) == 0:
            headings.append("Summary")
        return headings

    def get_links(resume_text,path2pdf):
        urls = []
        for page in fitz.open(path2pdf):
            for link in page.get_links():
                try:
                    urls.append(link['uri'])
                except:
                    pass
        return urls

    def format_content(resume_text):
        data = {x:[] for x in  get_headings(resume_text)}
    
        if len(data) > 1:
            lines = resume_text.split("\n")
            current_heading = ""
            for line in lines:
                if line.strip() in get_headings(resume_text):
                    current_heading = line.strip()
                    data[current_heading] = []
                elif current_heading and line.strip():
                    clean_line = ''.join(char for char in line if ord(char) < 128)
                    clean_line = clean_line.replace("\n", " ")  # Replace newline characters with spaces
                    data[current_heading].append(clean_line.strip())

        else:       

            resume_text = resume_text.replace("\n", " ")
            # resume_text = lines.strip()

            data["Summary"].append(resume_text)
        return data

    def print_heading_data(content):
        for key in content.keys():
            print(f"{key} ----------\n {content[key]}") 
    st.title("Resume Information Extractor")

    # File uploader
    pdf= st.file_uploader("Upload a PDF", type=["pdf"])
    if  pdf:
        with open(pdf.name, "wb") as f:
            f.write(pdf.read())
        path2pdf = pdf.name
        # text = extract_text_from_pdf(path2pdf)
        

        resume_text = extract_text_from_pdf(path2pdf)
        name = extract_name(resume_text)
        email = extract_email(resume_text)
        phone = extract_phone_number(resume_text)
        headings = get_headings(resume_text)
        urls = get_links(resume_text,path2pdf)
        content = format_content(resume_text)


        st.write("Extracted Information:")
        st.write(f"Name: {name}")
        st.write(f"Email: {email}")
        st.write(f"Phone: {phone}")
        # st.write(f"Heading: {headings}")
        st.write(f"Links: {urls}")
        st.write("Heading Data:")
        st.write(content)
        # os.remove(pdf_path)

if __name__ == "__main__":

    main()