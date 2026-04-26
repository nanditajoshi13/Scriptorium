from flask import Flask, render_template, request, jsonify, send_file
import db_handler
from pdf_generator import ScriptoriumPDF
import os

app = Flask(__name__)

# Use absolute paths to ensure the app finds folders on the server
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(BASE_PATH, 'generated_manuals')

# Ensure the output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_subjects', methods=['POST'])
def get_subjects():
    data = request.json
    # Logic is now safely handled inside db_handler
    return jsonify(db_handler.get_subjects(data.get('year'), data.get('branch')))

@app.route('/get_teachers', methods=['POST'])
def get_teachers():
    data = request.json
    return jsonify(db_handler.get_teachers(data.get('subject_id')))

@app.route('/generate_manual', methods=['POST'])
def generate_manual():
    form_data = request.form.to_dict()
    
    # Toggle Flags
    form_data['has_index'] = 'has_index' in request.form
    form_data['has_theory'] = 'has_theory' in request.form
    form_data['has_page_numbers'] = 'has_page_numbers' in request.form

    # FETCH SUBJECT NAME (Updated for SQLite)
    sub_id = form_data.get('subject_id')
    # Reuse the handler to find the subject name safely
    subjects = db_handler.get_subjects(form_data.get('year'), form_data.get('branch'))
    subject_name = next((s['name'] for s in subjects if str(s['id']) == str(sub_id)), "Laboratory Record")
    form_data['subject_name'] = subject_name

    def get_images(key):
        paths = []
        if key in request.files:
            for i, f in enumerate(request.files.getlist(key)):
                if f.filename:
                    # Clean filename to avoid issues on Linux servers
                    safe_filename = f"temp_{key}_{i}_{f.filename.replace(' ', '_')}"
                    p = os.path.join(OUTPUT_DIR, safe_filename)
                    f.save(p)
                    paths.append(p)
        return paths

    proc_paths = get_images('proc_images')
    out_paths = get_images('output_images')

    # Pathing for the PDF
    safe_user_name = form_data.get('name', 'User').replace(' ', '_')
    filename = f"{safe_user_name}_Manual.pdf"
    filepath = os.path.join(OUTPUT_DIR, filename)

    try:
        pdf = ScriptoriumPDF(form_data)
        pdf.generate(filepath, proc_images=proc_paths, out_images=out_paths)
        
        # Send the file to the user
        response = send_file(filepath, as_attachment=True)
        
        # CLEANUP: Delete temporary images after generation to save space
        # We do this after creating the PDF but before returning the response
        for p in proc_paths + out_paths:
            if os.path.exists(p):
                os.remove(p)
                
        return response

    except Exception as e:
        print(f"Deployment Error: {e}")
        return f"Error: {e}", 500

if __name__ == '__main__':
    # '0.0.0.0' allows access from other devices on your local Wi-Fi during testing
    app.run(host='0.0.0.0', port=5000, debug=True)



# from flask import Flask, render_template, request, jsonify, send_file
# import db_handler
# from pdf_generator import ScriptoriumPDF
# import os

# app = Flask(__name__)
# OUTPUT_DIR = 'generated_manuals'

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/get_subjects', methods=['POST'])
# def get_subjects():
#     data = request.json
#     return jsonify(db_handler.get_subjects(data.get('year'), data.get('branch')))

# @app.route('/get_teachers', methods=['POST'])
# def get_teachers():
#     data = request.json
#     return jsonify(db_handler.get_teachers(data.get('subject_id')))

# @app.route('/generate_manual', methods=['POST'])
# def generate_manual():
#     form_data = request.form.to_dict()
    
#     form_data['has_index'] = 'has_index' in request.form
#     form_data['has_theory'] = 'has_theory' in request.form
#     form_data['has_page_numbers'] = 'has_page_numbers' in request.form # Nested logic handled by HTML/PDF

#     sub_id = form_data.get('subject_id')
#     conn = db_handler.get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT name FROM subjects WHERE id = %s", (sub_id,))
#     res = cursor.fetchone()
#     if res: form_data['subject_name'] = res['name']
#     cursor.close()
#     conn.close()

#     def get_images(key):
#         paths = []
#         if key in request.files:
#             for i, f in enumerate(request.files.getlist(key)):
#                 if f.filename:
#                     p = os.path.join(OUTPUT_DIR, f"temp_{key}_{i}_{f.filename}")
#                     f.save(p)
#                     paths.append(p)
#         return paths

#     proc_paths = get_images('proc_images')
#     out_paths = get_images('output_images')

#     # 4. Final Generation
#     base_path = os.path.abspath(os.path.dirname(__file__))
#     filename = f"{form_data.get('name', 'User').replace(' ', '_')}_Manual.pdf"
#     filepath = os.path.join(base_path, OUTPUT_DIR, filename)

#     if not os.path.exists(os.path.dirname(filepath)):
#         os.makedirs(os.path.dirname(filepath))

#     try:
#         pdf = ScriptoriumPDF(form_data)
#         pdf.generate(filepath, proc_images=proc_paths, out_images=out_paths)
#         return send_file(filepath, as_attachment=True)
#     except Exception as e:
#         print(e)
#         return f"Error: {e}", 500

# if __name__ == '__main__':
#     app.run(debug=True)