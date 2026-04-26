from fpdf import FPDF
import os

class ScriptoriumPDF(FPDF):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.set_auto_page_break(auto=True, margin=15)

        self.set_title(f"Lab Record - {self.data.get('subject_name')}")
        self.set_author(self.data.get('name', 'Scriptorium'))

    def header(self):

        if self.page_no() > 1:
            self.set_font('Times', 'I', 8)
            sub = self.data.get('subject_name', 'Laboratory Record')
            self.cell(0, 10, f"Practical File: {sub}", 0, 0, 'R')
            self.ln(10)

    def footer(self):
    
        if self.data.get('has_page_numbers'):
            self.set_y(-15)
            self.set_font('Times', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def create_front_page(self):
        self.add_page()
       
        self.rect(5, 5, 200, 287)

        base_dir = os.path.abspath(os.path.dirname(__file__))
        logo_path = os.path.join(base_dir, 'static', 'images', 'gne_logo.png')
        
        if os.path.exists(logo_path):
            self.image(logo_path, x=85, y=20, w=40)
        else:
            self.set_xy(85, 20)
            self.set_font("Times", 'B', 12)
            self.cell(40, 40, "GNDEC LOGO", border=1, align='C')

        self.set_y(70)
        self.set_font("Times", 'B', 18)
        self.cell(0, 15, "GURU NANAK DEV ENGINEERING COLLEGE", ln=True, align='C')
        self.set_font("Times", 'B', 14)
        self.cell(0, 10, "LUDHIANA, PUNJAB", ln=True, align='C')
        
        self.ln(10)
        self.set_font("Times", 'B', 16)
        dept_text = f"DEPARTMENT OF {self.data.get('branch', '').upper()}"
        self.cell(0, 10, dept_text, ln=True, align='C')

        self.set_y(130)
        self.set_font("Times", 'BU', 18)
        self.cell(0, 10, "LABORATORY RECORD", ln=True, align='C')
        self.set_font("Times", 'B', 14)
        self.cell(0, 10, self.data.get('subject_name', '').upper(), ln=True, align='C')

        self.set_y(180)
        self.set_font("Times", 'B', 12)
        
        y_start = self.get_y()
    
        self.set_x(30)
        self.cell(75, 8, "Submitted By:", ln=0)
     
        self.set_x(120)
        self.cell(75, 8, "Submitted To:", ln=1)

        self.set_font("Times", "", 12)
        student_info = (f"Name: {self.data.get('name')}\n"
                        f"URN: {self.data.get('urn')}\n"
                        f"CRN: {self.data.get('crn')}")
        
        self.set_xy(30, y_start + 8)
        self.multi_cell(75, 8, student_info)
        
        self.set_xy(120, y_start + 8)
        self.multi_cell(75, 8, f"{self.data.get('teacher')}\nAssistant Professor")

    def add_index_page(self):
        self.add_page()
        self.set_font("Times", 'B', 18)
        self.cell(0, 20, "INDEX", ln=True, align='C')
        
        self.set_font("Times", 'B', 12)
        self.cell(15, 10, "S.No", border=1, align='C')
        self.cell(105, 10, "Experiment Name", border=1, align='C')
        self.cell(35, 10, "Date", border=1, align='C')
        self.cell(35, 10, "Sign", border=1, ln=True, align='C')
        
        for i in range(1, 14):
            self.cell(15, 11, str(i), border=1, align='C')
            self.cell(105, 11, "", border=1)
            self.cell(35, 11, "", border=1)
            self.cell(35, 11, "", border=1, ln=True)

    def add_content_section(self, title, text, images=None):
        if (text and text.strip()) or images:
            self.add_page()
            self.set_font("Times", 'B', 16)
            self.cell(0, 10, title, ln=True)
            self.ln(5)
            
            if text:
                font_family = "Courier" if title == "PROCEDURE" else "Times"
                self.set_font(font_family, '', 11)
                self.multi_cell(0, 7, text)
                self.ln(10)
            
            if images:
                for img_path in images:
                    if os.path.exists(img_path):
                        if self.get_y() > 220:
                            self.add_page()
                        self.image(img_path, x=35, w=140)
                        self.ln(10)

    def generate(self, filepath, proc_images=None, out_images=None):
        self.create_front_page()
        if self.data.get('has_index'):
            self.add_index_page()
        
        self.add_content_section("AIM", self.data.get('aim'))
        
        if self.data.get('has_theory'):
            self.add_content_section("THEORY", self.data.get('theory'))
            
        self.add_content_section("PROCEDURE", self.data.get('procedure'), proc_images)
        self.add_content_section("OUTPUT / RESULT", self.data.get('output'), out_images)
        
        self.output(filepath)
