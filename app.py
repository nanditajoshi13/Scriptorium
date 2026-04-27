import os
import uuid
from flask import Flask, render_template, request, jsonify, send_file
from db_handler import get_subjects, get_teachers
from pdf_generator import generate_manual

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
MANUALS_FOLDER = os.path.join(BASE_DIR, 'generated_manuals')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MANUALS_FOLDER, exist_ok=True)

BRANCH_MAP = {
    "IT": "Information Technology", 
    "CSE": "Computer Science Engineering", 
    "ECE": "Electronics and Communication Engineering"
}

@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/get_subjects_list/<int:year>/<branch>')
def get_subjects_list(year, branch): 
    return jsonify(get_subjects(year, branch))

@app.route('/get_teachers_list/<int:subject_id>')
def get_teachers_list(subject_id): 
    return jsonify(get_teachers(subject_id))

@app.route('/upload-img', methods=['POST'])
def upload_img():
    f = request.files.get('file')
    if f:
        filename = f"{uuid.uuid4()}_{f.filename}"
        path = os.path.join(UPLOAD_FOLDER, filename)
        f.save(path)
        return jsonify({"status": "success", "path": path})
    return jsonify({"status": "error"}), 400

@app.route('/generate', methods=['POST'])
def generate():
    b_short = request.form.get('branch')
    
    data = {
        'name': request.form.get('name'), 
        'urn': request.form.get('urn'), 
        'crn': request.form.get('crn'),
        'class_sec': request.form.get('class_sec'), 
        'branch_short': b_short,
        'branch_full': BRANCH_MAP.get(b_short, b_short), 
        'subject': request.form.get('subject_name'),
        'teacher': request.form.get('teacher'), 
        'needs_index': 'needs_index' in request.form,
        'index_page_col': 'index_page_col' in request.form, 
        'experiments': []
    }

    nums = request.form.getlist('exp_number[]')
    aims = request.form.getlist('exp_aim[]')
    apps = request.form.getlist('exp_apparatus[]')
    theos = request.form.getlist('exp_theory[]')
    codes = request.form.getlist('exp_code[]')

    for i in range(len(nums)):
        data['experiments'].append({
            'number': nums[i], 
            'aim': aims[i], 
            'apparatus': apps[i] if i < len(apps) else "", 
            'theory': theos[i] if i < len(theos) else "", 
            'code': codes[i],
            'include_theory': f'include_theory[{i}]' in request.form, 
            'include_apparatus': f'include_apparatus[{i}]' in request.form,
            'images': request.form.getlist(f'exp_images[{i}][]')
        })

    pdf_path = generate_manual(data)
    
    full_path = os.path.abspath(pdf_path)
    if os.path.exists(full_path):
        return send_file(full_path, as_attachment=True)
    return "Error: Generated file not found.", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
