from flask import Flask, render_template, request, jsonify, send_file
import db_handler
from pdf_generator import ScriptoriumPDF
import os

app = Flask(__name__)

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(BASE_PATH, 'generated_manuals')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_subjects', methods=['POST'])
def get_subjects():
    data = request.json
    return jsonify(db_handler.get_subjects(data.get('year'), data.get('branch')))

@app.route('/get_teachers', methods=['POST'])
def get_teachers():
    data = request.json
    return jsonify(db_handler.get_teachers(data.get('subject_id')))

@app.route('/generate_manual', methods=['POST'])
def generate_manual():
    form_data = request.form.to_dict()
    
    form_data['has_index'] = 'has_index' in request.form
    form_data['has_theory'] = 'has_theory' in request.form
    form_data['has_page_numbers'] = 'has_page_numbers' in request.form

    sub_id = form_data.get('subject_id')
    subjects = db_handler.get_subjects(form_data.get('year'), form_data.get('branch'))
    subject_name = next((s['name'] for s in subjects if str(s['id']) == str(sub_id)), "Laboratory Record")
    form_data['subject_name'] = subject_name

    def get_images(key):
        paths = []
        if key in request.files:
            for i, f in enumerate(request.files.getlist(key)):
                if f.filename:
                    safe_filename = f"temp_{key}_{i}_{f.filename.replace(' ', '_')}"
                    p = os.path.join(OUTPUT_DIR, safe_filename)
                    f.save(p)
                    paths.append(p)
        return paths

    proc_paths = get_images('proc_images')
    out_paths = get_images('output_images')

    safe_user_name = form_data.get('name', 'User').replace(' ', '_')
    filename = f"{safe_user_name}_Manual.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        pdf = ScriptoriumPDF(form_data)
        pdf.generate(filepath, proc_images=proc_paths, out_images=out_paths)
        
        response = send_file(filepath, as_attachment=True)
        
        for p in proc_paths + out_paths:
            if os.path.exists(p):
                os.remove(p)
                
        return response

    except Exception as e:
        print(f"Deployment Error: {e}")
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
