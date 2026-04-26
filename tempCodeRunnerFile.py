from flask import Flask, render_template, request, jsonify, send_file
import db_handler
from pdf_generator import ScriptoriumPDF
import os

app = Flask(__name__)
OUTPUT_DIR = 'generated_manuals'

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
    form_data['has_page_numbers'] = 'has_page_numbers' in request.form # Nested logic handled by HTML/PDF

    sub_id = form_data.get('subject_id')
    conn = db_handler.get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name FROM subjects WHERE id = %s", (sub_id,))
    res = cursor.fetchone()
    if res: form_data['subject_name'] = res['name']
    cursor.close()
    conn.close()

    def get_images(key):
        paths = []
        if key in request.files:
            for i, f in enumerate(request.files.getlist(key)):
                if f.filename:
                    p = os.path.join(OUTPUT_DIR, f"temp_{key}_{i}_{f.filename}")
                    f.save(p)
                    paths.append(p)
        return paths

    proc_paths = get_images('proc_images')
    out_paths = get_images('output_images')

    # 4. Final Generation
    base_path = os.path.abspath(os.path.dirname(__file__))
    filename = f"{form_data.get('name', 'User').replace(' ', '_')}_Manual.pdf"
    filepath = os.path.join(base_path, OUTPUT_DIR, filename)

    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    try:
        pdf = ScriptoriumPDF(form_data)
        pdf.generate(filepath, proc_images=proc_paths, out_images=out_paths)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        print(e)
        return f"Error: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)