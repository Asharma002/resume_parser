import unittest
from resume_parse import extract_text_from_pdf, extract_name, extract_email, extract_phone_number, get_headings, get_links

class TestResumeFunctions(unittest.TestCase):

    def setUp(self):
        self.pdf_path = "C:/Users/KIIT/Desktop/resume parser/resume_anshuman_sharma.pdf"
        self.resume_text = extract_text_from_pdf(self.pdf_path)
        

    def test_extract_name(self):
        self.assertIsInstance(extract_name(self.resume_text), str)


    def test_extract_email(self):
        self.assertIsInstance(extract_email(self.resume_text), str)

    def test_extract_phone_number(self):
        expected_phone = "+91 9982394228"
        self.assertEqual(extract_phone_number(self.resume_text), expected_phone)

    def test_get_headings(self):
        expected_headings = ['Education', 'Internship Experience', 'Projects', 'Skills', 'Publications [Conference]', 'ACADEMIC ACTIVITIES']
        self.assertEqual(get_headings(self.resume_text), expected_headings)
    
    def test_format(self):
        self.assertIsInstance(format(self.resume_text), dict)

    
if __name__ == "__main__":
    unittest.main()