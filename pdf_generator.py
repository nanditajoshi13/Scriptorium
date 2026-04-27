import os
import re
import html
import base64
import uuid
from fpdf import FPDF

class ScriptoriumPDF(FPDF):
    def __init__(self, data):
        super().__init__()
        self.data = data
    
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        
        os.makedirs(os.path.join(self.base_dir, 'static', 'uploads'), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, 'generated_manuals'), exist_ok=True)

        try:
            self.add_font("Times", "", "TIMES.TTF", uni=True)
            self.add_font("Times", "B", "TIMESBD.TTF", uni=True)
            self.add_font("Times", "I", "TIMESI.TTF", uni=True)
            self.add_font("Times", "BI", "TIMESBI.TTF", uni=True)
        except Exception as e: 
            print(f"Font Load Error: {e}")
            
        self.set_auto_page_break(auto=True, margin=15)

    def write_rich_text(self, html_text):
        """Sequential parser: Prevents overlapping and handles mixed formatting."""
        if not html_text: return

        html_text = re.sub(r'<(span|p|u|div)[^>]*>', r'<\1>', html_text)
        html_text = html_text.replace('</p>', '\n').replace('<br>', '\n').replace('<br/>', '\n')

        parts = re.split(r'(<(?:b|i|u|strong|em|li|ol|ul|img|/b|/i|/u|/strong|/em|/li|/ol|/ul)>)', html_text)
        
        is_b, is_i, is_u = False, False, False
        list_stack = [] 
        bullet_count = 0

        for part in parts:
            if not part: continue
            tag = part.lower()
            
            if tag in ['<b>', '<strong>']: is_b = True
            elif tag in ['</b>', '</strong>']: is_b = False
            elif tag in ['<i>', '<em>']: is_i = True
            elif tag in ['</i>', '<em>']: is_i = False
            elif tag == '<u>': is_u = True
            elif tag == '</u>': is_u = False
            
            elif tag == '<ol>': 
                list_stack.append('ol')
                bullet_count = 0
            elif tag == '<ul>': 
                list_stack.append('ul')
            elif tag in ['</ol>', '</ul>']: 
                if list_stack: list_stack.pop()
                self.ln(2) 
            elif tag == '<li>':
                self.ln(6) 
                prefix = f"  {bullet_count + 1}. " if (list_stack and list_stack[-1] == 'ol') else "  - "
                if list_stack and list_stack[-1] == 'ol': bullet_count += 1
                self.set_font("Times", "B", 12)
                self.write(7, prefix)
            
            elif '<img' in tag:
                src_match = re.search(r'src="data:image\/([^;]+);base64,([^"]+)"', part)
                if src_match:
                    try:
                        ext, img_data = src_match.group(1), src_match.group(2)
                        tmp_fn = f"tmp_{uuid.uuid4()}.{ext}"
                        tmp_path = os.path.join(self.base_dir, 'static', 'uploads', tmp_fn)
                        with open(tmp_path, 'wb') as f: 
                            f.write(base64.b64decode(img_data))
                        self.ln(10)
                        self.image(tmp_path, x=45, w=120)
                        self.ln(10)
                    except: pass
            
            elif not part.startswith('<'):
                style = ""
                if is_b: style += "B"
                if is_i: style += "I"
                if is_u: style += "U"
                self.set_font("Times", style, 12)
                
                clean_text = html.unescape(part)
                text_segments = clean_text.split('\n')
                for i, segment in enumerate(text_segments):
                    if segment.strip() or segment == ' ':
                        self.write(7, segment)
                    if i < len(text_segments) - 1:
                        self.ln(7)

    def add_front_page(self):
        self.add_page()
   
        self.set_font("Times", "B", 20)
        self.cell(0, 15, self.data['subject'].upper(), 0, 1, 'C')
        self.set_font("Times", "", 14)
        self.cell(0, 10, "Practical File", 0, 1, 'C')
        self.ln(5)
        
        self.set_font("Times", "", 12)
        award = "SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENT FOR\nTHE AWARD OF THE DEGREE OF"
        self.multi_cell(0, 7, award, 0, 'C')
        self.ln(5)
        
        self.set_font("Times", "B", 16)
        self.cell(0, 10, "BACHELOR OF TECHNOLOGY", 0, 1, 'C')
        self.cell(0, 10, f"({self.data['branch_full'].upper()})", 0, 1, 'C')

        logo = os.path.join(self.base_dir, 'static', 'images', 'gne_logo.png')
        if os.path.exists(logo): 
            self.image(logo, x=75, y=90, w=60)
        
        self.set_y(180)
        y_start = self.get_y()
        self.set_font("Times", "B", 12)
        self.set_xy(35, y_start); self.cell(70, 10, "SUBMITTED BY:", 0, 0, 'L')
        self.set_xy(125, y_start); self.cell(0, 10, "SUBMITTED TO:", 0, 1, 'L')
        
        self.set_font("Times", "", 12)
        names = [f"Name: {self.data['name']}", f"URN: {self.data['urn']}", f"CRN: {self.data['crn']}", f"Class: {self.data['class_sec']}"]
        for i, text in enumerate(names):
            self.set_xy(35, y_start + 10 + (i*6))
            self.cell(70, 6, text, 0, 0, 'L')
        self.set_xy(125, y_start + 10)
        self.cell(0, 6, self.data['teacher'], 0, 0, 'L')

        self.set_y(-55)
        self.set_font("Times", "B", 11)
        dept_info = f"DEPARTMENT OF {self.data['branch_full'].upper()}\nGURU NANAK DEV ENGINEERING COLLEGE, LUDHIANA"
        self.multi_cell(0, 6, dept_info, 0, 'C')
        
        self.set_font("Times", "B", 9)
        self.cell(0, 10, "(an autonomous college under UGC ACT)", 0, 1, 'C')
        
        self.set_font("Times", "", 10)
        self.cell(0, 5, "JAN - JUNE, 2026", 0, 1, 'C')

    def add_index_page(self, show_pg):
        self.add_page()
        self.set_font("Times", "B", 16)
        self.cell(0, 15, "INDEX", 0, 1, 'C')
        self.ln(5)
        self.set_font("Times", "B", 10)
        w_name = 85 if show_pg else 115
        self.cell(12, 10, "S.No", 1, 0, 'C'); self.cell(w_name, 10, "Name of Experiment", 1, 0, 'C')
        if show_pg: self.cell(20, 10, "Page No", 1, 0, 'C')
        self.cell(30, 10, "Date", 1, 0, 'C'); self.cell(38, 10, "Remarks", 1, 1, 'C')
        for _ in range(15):
            self.cell(12, 10, "", 1, 0); self.cell(w_name, 10, "", 1, 0)
            if show_pg: self.cell(20, 10, "", 1, 0)
            self.cell(30, 10, "", 1, 0); self.cell(38, 10, "", 1, 1)

    def add_experiment(self, exp_data, first_exp):
        if first_exp: self.add_page()
        else: self.ln(15)
        if self.get_y() > 220: self.add_page()
        
        self.set_font("Times", "B", 16)
        self.cell(0, 10, f"EXPERIMENT - {exp_data['number']}", 0, 1, 'C')
        self.ln(5)

        self.set_font("Times", "B", 12); self.write(10, "AIM: ")
        self.set_font("Times", "", 12); self.write(10, exp_data['aim']); self.ln(12)
        
        if exp_data.get('include_apparatus'):
            self.set_font("Times", "B", 12); self.cell(0, 10, "APPARATUS / REQUIREMENTS:", 0, 1, 'L')
            self.write_rich_text(exp_data['apparatus']); self.ln(5)
        if exp_data.get('include_theory'):
            self.set_font("Times", "B", 12); self.cell(0, 10, "THEORY:", 0, 1, 'L')
            self.write_rich_text(exp_data['theory']); self.ln(5)
        
        self.set_font("Times", "B", 12); self.cell(0, 10, "SOURCE CODE:", 0, 1, 'L')
        self.set_font("Courier", "", 10); self.set_fill_color(245, 245, 245)
        self.multi_cell(0, 5, exp_data['code'], 1, 'L', True); self.ln(5)
        
        self.set_font("Times", "B", 12); self.cell(0, 10, "OUTPUT:", 0, 1, 'L')
        if exp_data.get('images'):
            for img in exp_data['images']:
                if os.path.exists(img): self.image(img, x=20, w=170); self.ln(5)

def generate_manual(data):
    pdf = ScriptoriumPDF(data)
    pdf.add_front_page()
    if data.get('needs_index'): 
        pdf.add_index_page(data.get('index_page_col'))
    for i, exp in enumerate(data['experiments']): 
        pdf.add_experiment(exp, (i==0))
    
    fn = os.path.join(pdf.base_dir, 'generated_manuals', f"{data['name'].replace(' ','_')}_Manual.pdf")
    pdf.output(fn)
    return fn
